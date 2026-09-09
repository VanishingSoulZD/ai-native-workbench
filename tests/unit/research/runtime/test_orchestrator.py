"""Unit tests for the Research orchestrator (Task 6 brief Steps 5-6, Spec 5.5/7).

Coverage: the exact attempt start protocol order ATTEMPT_CREATED -> INPUT_BOUND
-> ATTEMPT_STARTED -> Executor; the completion record order
VALIDATION_COMPLETED -> ACCEPTANCE_RECORDED -> ARTIFACT_COMMITTED ->
ATTEMPT_SUCCEEDED (Ruling 14); the evaluated-field disposition payloads
(Task 4 carried note); rejection and executor-failure dispositions with the
Invocation/Run failing durably (never NEEDS_REVISION); the human policy
deferring to the Gate Barrier; barrier stop/replace logic (approval validity
against the current lineage); checkpoints at step boundaries; bounded
completion with BOUNDED_SCOPE; the Task 7 terminal phase seam; and blocked
source acquisition disposing of the Invocation.

The fake executors/transports are the point of the seam (brief: no mocks
except where a fake executor/transport is the point); everything else runs
over the real FileSystemRuntimeStore.
"""

import pytest

from ai_native_workbench.research.runtime import (
    AttemptStatus,
    CaseBinding,
    EntryMode,
    EventType,
    GateDecision,
    InvocationStatus,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.binding import (
    freeze_case_binding,
    load_research_case,
)
from ai_native_workbench.research.runtime.execution import (
    DETERMINISTIC_MODE,
    CandidateOutput,
    DeterministicExecutor,
    ExecutorRegistry,
)
from ai_native_workbench.research.runtime.gates.runtime import GateRuntime
from ai_native_workbench.research.runtime.orchestrator import (
    COMPLETION_ACQUISITION_FAILED,
    COMPLETION_BOUNDED_SCOPE,
    Orchestrator,
)
from ai_native_workbench.research.runtime.source.acquisition import (
    FetchError,
    SourceAcquisitionService,
)
from ai_native_workbench.research.runtime.store import (
    FileSystemRuntimeStore,
    reduce_events,
)
from ai_native_workbench.research.runtime.workflow import build_standard_workflow

RUN_ID = "run-1"


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def make_store(tmp_path) -> FileSystemRuntimeStore:
    return FileSystemRuntimeStore(tmp_path)


def make_run_record(run_id: str = RUN_ID) -> RunRecord:
    return RunRecord(
        run_id=run_id,
        case_id="case-1",
        case_binding=CaseBinding(
            case_id="case-1",
            charter_identity="charter",
            charter_digest="sha256:" + "a" * 64,
            source_declaration_identity="urls",
            source_declaration_digest="sha256:" + "b" * 64,
        ),
        state=RunState.CREATED,
        cumulative_execution_scope=(),
        current_invocation_id=None,
        completion_reason=None,
    )


class RecordingExecutor:
    """Derives the deterministic candidate and records invocation facts."""

    def __init__(self, snapshot):
        self._snapshot = snapshot  # callable() -> tuple[EventType, ...]
        self._inner = DeterministicExecutor()
        self.calls = []

    def execute(self, step, inputs):
        self.calls.append((step.id, inputs, self._snapshot()))
        return self._inner.execute(step, inputs)


class BadCandidateExecutor:
    """Derives a schema-invalid candidate (missing the required 'kind')."""

    def execute(self, step, inputs):
        return CandidateOutput(
            content={"inputs": inputs.artifact_ids, "rows": []},
            schema_identity=step.outputs[0].kind,
            schema_version="1",
            provenance=("mode:deterministic",),
        )


class RaisingExecutor:
    def execute(self, step, inputs):
        raise RuntimeError("executor exploded")


class FailingFetcher:
    def fetch(self, url):
        raise FetchError("UNREACHABLE", f"cannot fetch {url!r}.")


def make_orchestrator(
    store,
    *,
    executor=None,
    domain_checks=None,
    terminal_phase=None,
    acquisition=None,
    cases_dir="cases",
    tmp_path=None,
) -> Orchestrator:
    registry = ExecutorRegistry()
    registry.register(DETERMINISTIC_MODE, executor or DeterministicExecutor())
    return Orchestrator(
        store,
        registry=registry,
        domain_checks=domain_checks,
        terminal_phase=terminal_phase,
        acquisition=acquisition or SourceAcquisitionService(store),
        cases_dir=cases_dir,
    )


def open_invocation(orchestrator, store, scope, run_id=RUN_ID, entry_mode=EntryMode.START):
    store.create_run(make_run_record(run_id=run_id))
    return orchestrator.open_invocation(run_id, scope, entry_mode)


def event_types(store, run_id=RUN_ID):
    return [event.event_type for event in store.events(run_id)]


def events_of_type(store, event_type, run_id=RUN_ID):
    return [event for event in store.events(run_id) if event.event_type is event_type]


def latest_gate(store, run_id=RUN_ID):
    gates = list(reduce_events(store.events(run_id)).gates.values())
    return gates[-1]


def approve_gate(store, gate, gates=None):
    runtime = gates or GateRuntime(store, build_standard_workflow())
    return runtime.decide(gate.gate_id, GateDecision.APPROVED, "human", "ok")


# ---------------------------------------------------------------------------
# Attempt start protocol
# ---------------------------------------------------------------------------


def test_attempt_protocol_event_order(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(orchestrator, store, ("R1",))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    types = event_types(store)
    start = types.index(EventType.ATTEMPT_CREATED)
    assert types[start:] == [
        EventType.ATTEMPT_CREATED,
        EventType.INPUT_BOUND,
        EventType.ATTEMPT_STARTED,
        EventType.VALIDATION_COMPLETED,
        EventType.ACCEPTANCE_RECORDED,
        EventType.ARTIFACT_COMMITTED,
        EventType.ATTEMPT_SUCCEEDED,
        EventType.CHECKPOINT_CREATED,
        EventType.INVOCATION_COMPLETED,
    ]


def test_executor_invoked_after_attempt_started(tmp_path):
    store = make_store(tmp_path)
    snapshots = []

    def snapshot():
        current = tuple(event_types(store))
        snapshots.append(current)
        return current

    executor = RecordingExecutor(snapshot)
    orchestrator = make_orchestrator(store, executor=executor)
    invocation = open_invocation(orchestrator, store, ("R1",))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    assert len(executor.calls) == 1
    step_id, inputs, at_call = executor.calls[0]
    assert step_id == "R1"
    assert inputs.step_id == "R1"
    assert at_call[-1] is EventType.ATTEMPT_STARTED
    assert at_call[-2] is EventType.INPUT_BOUND
    assert at_call[-3] is EventType.ATTEMPT_CREATED


def test_executor_receives_empty_binding_without_upstream(tmp_path):
    store = make_store(tmp_path)
    executor = RecordingExecutor(lambda: ())
    orchestrator = make_orchestrator(store, executor=executor)
    invocation = open_invocation(orchestrator, store, ("R1",))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    _step_id, inputs, _at_call = executor.calls[0]
    assert inputs.artifact_ids == ()
    assert inputs.upstream_attempt_ids == ()


# ---------------------------------------------------------------------------
# Validation / acceptance record shapes
# ---------------------------------------------------------------------------


def test_validation_and_acceptance_payloads_carry_evaluated(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(orchestrator, store, ("R1",))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    validation = events_of_type(store, EventType.VALIDATION_COMPLETED)[0]
    payload = validation.payload
    assert validation.artifact_id is not None
    assert dict(payload["validation"]["schema"]) == {
        "passed": True,
        "evaluated": True,
        "reasons": (),
    }
    assert dict(payload["validation"]["provenance"]) == {
        "passed": True,
        "evaluated": True,
        "reasons": (),
    }
    # No domain hook declared: explicitly not evaluated, never a pass.
    assert dict(payload["validation"]["domain"]) == {
        "passed": False,
        "evaluated": False,
        "reasons": (),
    }
    acceptance = events_of_type(store, EventType.ACCEPTANCE_RECORDED)[0]
    assert acceptance.payload["policy"] == "automatic"
    assert acceptance.payload["disposition"] == "ACCEPTED"
    assert acceptance.payload["validation"]["domain"]["evaluated"] is False


# ---------------------------------------------------------------------------
# Rejection and executor failure dispositions
# ---------------------------------------------------------------------------


def test_rejection_records_disposition_and_fails_run(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store, executor=BadCandidateExecutor())
    invocation = open_invocation(orchestrator, store, ("R1",))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.FAILED
    (attempt,) = projection.attempts.values()
    assert attempt.status is AttemptStatus.FAILED
    assert projection.failure_dispositions[attempt.attempt_id] == (
        "ACCEPTANCE_REJECTED"
    )
    assert projection.invocations[invocation.invocation_id].status is (
        InvocationStatus.FAILED
    )
    # The rejection is recorded durably; nothing half-commits.
    assert events_of_type(store, EventType.VALIDATION_COMPLETED)
    assert events_of_type(store, EventType.ACCEPTANCE_RECORDED)
    assert events_of_type(store, EventType.ATTEMPT_FAILED)
    assert not events_of_type(store, EventType.ARTIFACT_COMMITTED)
    assert projection.artifacts == {}
    completion = events_of_type(store, EventType.INVOCATION_COMPLETED)[0]
    assert completion.payload == {
        "status": "FAILED",
        "completion_reason": "ACCEPTANCE_REJECTED",
    }


def test_executor_exception_fails_attempt_with_disposition(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store, executor=RaisingExecutor())
    invocation = open_invocation(orchestrator, store, ("R1",))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.FAILED
    (attempt,) = projection.attempts.values()
    assert attempt.status is AttemptStatus.FAILED
    assert projection.failure_dispositions[attempt.attempt_id] == "EXECUTOR_FAILED"
    completion = events_of_type(store, EventType.INVOCATION_COMPLETED)[0]
    assert completion.payload["completion_reason"] == "EXECUTOR_FAILED"


# ---------------------------------------------------------------------------
# Gate barriers
# ---------------------------------------------------------------------------


def test_orchestrator_stops_at_h2_with_pending_gate(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(orchestrator, store, ("R1", "R2", "R3", "R4"))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.WAITING_FOR_HUMAN
    assert {attempt.step_id for attempt in projection.attempts.values()} == {
        "R1",
        "R2",
        "R3",
    }
    assert all(
        attempt.status is AttemptStatus.SUCCEEDED
        for attempt in projection.attempts.values()
    )
    (gate,) = projection.gates.values()
    assert gate.logical_gate_id == "H2"
    assert gate.decision is GateDecision.PENDING
    r3_attempt = [
        attempt for attempt in projection.attempts.values() if attempt.step_id == "R3"
    ][0]
    assert gate.review_target.step_id == "R3"
    assert gate.review_target.attempt_id == r3_attempt.attempt_id
    (artifact_id,) = gate.review_target.artifact_ids
    assert artifact_id in projection.artifacts
    # The active Invocation remains RUNNING while the Run waits (Spec 5.2).
    assert projection.invocations[invocation.invocation_id].status is (
        InvocationStatus.RUNNING
    )


def test_human_policy_defers_and_commits_before_h3(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(
        orchestrator, store, ("R1", "R2", "R3", "R4", "R5")
    )
    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)
    approve_gate(store, latest_gate(store))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    projection = reduce_events(store.events(RUN_ID))
    assert {gate.logical_gate_id for gate in projection.gates.values()} == {"H2", "H3"}
    r4_attempt = [
        attempt for attempt in projection.attempts.values() if attempt.step_id == "R4"
    ][0]
    assert r4_attempt.status is AttemptStatus.SUCCEEDED
    r4_acceptance = [
        event
        for event in events_of_type(store, EventType.ACCEPTANCE_RECORDED)
        if event.step_id == "R4"
    ][0]
    assert r4_acceptance.payload["disposition"] == "DEFERRED_TO_HUMAN"
    assert r4_acceptance.payload["policy"] == "human"
    r4_commits = [
        event
        for event in events_of_type(store, EventType.ARTIFACT_COMMITTED)
        if event.attempt_id == r4_attempt.attempt_id
    ]
    assert len(r4_commits) == 1
    h3 = latest_gate(store)
    assert h3.logical_gate_id == "H3"
    assert h3.review_target.attempt_id == r4_attempt.attempt_id
    assert projection.run.state is RunState.WAITING_FOR_HUMAN


def test_mismatched_approval_is_superseded_at_barrier(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(orchestrator, store, ("R1", "R2", "R3", "R4"))
    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)
    prior = latest_gate(store)
    approve_gate(store, prior)

    # A re-execution of R3 changes the lineage the old approval covered.
    orchestrator.continue_execution(RUN_ID, invocation.invocation_id, cut_step="R3")

    projection = reduce_events(store.events(RUN_ID))
    superseded_events = events_of_type(store, EventType.GATE_SUPERSEDED)
    assert len(superseded_events) == 1
    assert superseded_events[0].gate_id == prior.gate_id
    old = projection.gates[prior.gate_id]
    assert old.superseded_by is not None
    replacement = projection.gates[old.superseded_by]
    assert replacement.supersedes == prior.gate_id
    assert replacement.decision is GateDecision.PENDING
    # The replacement reviews the new lineage, never the superseded one.
    r3_attempts = [
        attempt for attempt in projection.attempts.values() if attempt.step_id == "R3"
    ]
    assert len(r3_attempts) == 2
    assert replacement.review_target.attempt_id == r3_attempts[-1].attempt_id
    assert projection.run.state is RunState.WAITING_FOR_HUMAN
    assert not [
        attempt for attempt in projection.attempts.values() if attempt.step_id == "R4"
    ]


# ---------------------------------------------------------------------------
# Checkpoints and bounded completion
# ---------------------------------------------------------------------------


def test_checkpoints_created_at_step_boundaries(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(orchestrator, store, ("R1", "R2", "R3"))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    projection = reduce_events(store.events(RUN_ID))
    checkpoints = {c.step_id: c for c in projection.checkpoints.values()}
    assert set(checkpoints) == {"R1", "R2", "R3"}
    for step_id, attempt in projection.attempts.items():
        checkpoint = checkpoints[attempt.step_id]
        (artifact_id,) = checkpoint.artifact_ids
        assert artifact_id in projection.artifacts
        assert checkpoint.compatibility.workflow_identity == "research-standard"
        assert checkpoint.compatibility.workflow_version == "1.0.0"
        assert checkpoint.compatibility.step_identity == attempt.step_id
        assert checkpoint.compatibility.step_version == "1"
        assert (
            checkpoint.compatibility.runtime_configuration_identity
            == "research-runtime-v1"
        )


def test_bounded_scope_completes_invocation(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(orchestrator, store, ("R1", "R2"))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    projection = reduce_events(store.events(RUN_ID))
    completion = events_of_type(store, EventType.INVOCATION_COMPLETED)[0]
    assert completion.payload == {
        "status": "SUCCEEDED",
        "completion_reason": COMPLETION_BOUNDED_SCOPE,
    }
    assert projection.run.state is RunState.COMPLETED
    assert projection.run.completion_reason == COMPLETION_BOUNDED_SCOPE
    assert projection.run.cumulative_execution_scope == ("R1", "R2")
    assert projection.invocations[invocation.invocation_id].status is (
        InvocationStatus.SUCCEEDED
    )


# ---------------------------------------------------------------------------
# Task 7 terminal phase seam
# ---------------------------------------------------------------------------


def test_terminal_phase_runs_before_completion(tmp_path):
    store = make_store(tmp_path)
    calls = []

    def hook(store_, projection, invocation, attempt):
        calls.append((projection.run.state, invocation.invocation_id, attempt.step_id))

    orchestrator = make_orchestrator(
        store, domain_checks={"R5": lambda content: (True, ())}, terminal_phase=hook
    )
    invocation = open_invocation(
        orchestrator, store, ("R1", "R2", "R3", "R4", "R5")
    )
    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)
    approve_gate(store, latest_gate(store))
    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)
    approve_gate(store, latest_gate(store))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    assert len(calls) == 1
    state, invocation_id, step_id = calls[0]
    assert state is RunState.RUNNING  # before the completion fact
    assert invocation_id == invocation.invocation_id
    assert step_id == "R5"
    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.COMPLETED
    assert projection.run.cumulative_execution_scope == ("R1", "R2", "R3", "R4", "R5")


def test_terminal_phase_skipped_for_bounded_scope(tmp_path):
    store = make_store(tmp_path)
    calls = []

    def hook(store_, projection, invocation, attempt):
        calls.append(attempt.step_id)

    orchestrator = make_orchestrator(store, terminal_phase=hook)
    invocation = open_invocation(orchestrator, store, ("R1", "R2", "R3"))

    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)

    assert calls == []
    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.COMPLETED


def test_canonical_policy_requires_domain_hook(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    invocation = open_invocation(
        orchestrator, store, ("R1", "R2", "R3", "R4", "R5")
    )
    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)
    approve_gate(store, latest_gate(store))
    orchestrator.continue_execution(RUN_ID, invocation.invocation_id)
    approve_gate(store, latest_gate(store))

    with pytest.raises(RuntimeContractError):
        orchestrator.continue_execution(RUN_ID, invocation.invocation_id)


# ---------------------------------------------------------------------------
# Source acquisition disposal
# ---------------------------------------------------------------------------


def _write_case_dir(tmp_path):
    case_dir = tmp_path / "case-1"
    case_dir.mkdir()
    (case_dir / "00-research-charter.md").write_text("# charter\n", encoding="utf-8")
    (case_dir / "inputs").mkdir()
    (case_dir / "inputs" / "urls.yaml").write_text(
        "- id: src-1\n  url: http://example.test/src.txt\n  required: true\n",
        encoding="utf-8",
    )
    return case_dir


def make_bound_run_record(case) -> RunRecord:
    return RunRecord(
        run_id=RUN_ID,
        case_id=case.case_id,
        case_binding=freeze_case_binding(case),
        state=RunState.CREATED,
        cumulative_execution_scope=(),
        current_invocation_id=None,
        completion_reason=None,
    )


def test_blocked_acquisition_fails_invocation_durably(tmp_path):
    case_dir = _write_case_dir(tmp_path)
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(
        store,
        acquisition=SourceAcquisitionService(store, fetcher=FailingFetcher()),
        cases_dir=str(tmp_path),
    )
    case = load_research_case(case_dir)
    store.create_run(make_bound_run_record(case))
    invocation = orchestrator.open_invocation(RUN_ID, ("R1",), EntryMode.START)
    run = reduce_events(store.events(RUN_ID)).run

    result = orchestrator.acquire_sources(run)

    assert result.blocked is True
    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.FAILED
    assert projection.run.completion_reason == COMPLETION_ACQUISITION_FAILED
    assert projection.invocations[invocation.invocation_id].status is (
        InvocationStatus.FAILED
    )
    # Nothing is half-committed (Task 5 guarantee: required failure blocks).
    assert projection.artifacts == {}
    assert not events_of_type(store, EventType.ARTIFACT_COMMITTED)


def test_open_invocation_rejects_barrier_scope(tmp_path):
    store = make_store(tmp_path)
    orchestrator = make_orchestrator(store)
    store.create_run(make_run_record())

    with pytest.raises(RuntimeContractError):
        orchestrator.open_invocation(RUN_ID, ("H2",), EntryMode.START)
