"""Unit tests for the Research Runtime control plane (Task 6 brief Steps 7-8).

Coverage: the explicit control actions and their invariants —
``start`` is only legal on CREATED runs; ``retry`` stays within the same
Attempt + Invocation; ``rerun`` creates a new Attempt inside the current
Invocation; ``resume`` creates a new Invocation for the same Run (honoring
the revision target on NEEDS_REVISION); ``run_from`` creates a new
Invocation (EntryMode FROM) at an exact-compatible checkpoint boundary and
rebuilds the downstream lineage; ``--until`` produces bounded completion
with completion_reason=BOUNDED_SCOPE; ``decide_gate`` APPROVE continues
execution and REJECT moves the Run to NEEDS_REVISION without auto-rerun.
Illegal actions in the projected state raise RuntimeContractError-family
errors naming the state conflict (Ruling 7).

Real FileSystemRuntimeStore everywhere; the fake transport/executor seams
are the documented injection points.
"""

import uuid
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    AttemptStatus,
    CaseBinding,
    EntryMode,
    EventEnvelope,
    EventType,
    GateDecision,
    InvocationStatus,
    RevisionTarget,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.binding import (
    freeze_case_binding,
    load_research_case,
)
from ai_native_workbench.research.runtime.control import ControlError, ResearchRuntime
from ai_native_workbench.research.runtime.orchestrator import COMPLETION_BOUNDED_SCOPE
from ai_native_workbench.research.runtime.execution import (
    DETERMINISTIC_MODE,
    ExecutorRegistry,
)
from ai_native_workbench.research.runtime.gates.runtime import GateRuntime
from ai_native_workbench.research.runtime.reconciliation import reconcile_run
from ai_native_workbench.research.runtime.source.acquisition import (
    FetchError,
    FetchResult,
    SourceAcquisitionService,
)
from ai_native_workbench.research.runtime.store import (
    FileSystemRuntimeStore,
    reduce_events,
)
from ai_native_workbench.research.runtime.workflow import build_standard_workflow

RUN_ID = "run-1"
INVOCATION_ID = "inv-1"
TS = "2026-09-09T08:00:00+00:00"
SOURCE_URL = "http://example.test/src.txt"


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def write_case_dir(root) -> str:
    case_dir = root / "case-1"
    case_dir.mkdir(exist_ok=True)
    (case_dir / "inputs").mkdir(parents=True, exist_ok=True)
    (case_dir / "00-research-charter.md").write_text("# charter\n", encoding="utf-8")
    (case_dir / "inputs" / "urls.yaml").write_text(
        f"- id: src-1\n  url: {SOURCE_URL}\n  required: true\n",
        encoding="utf-8",
    )
    return str(case_dir)


def load_case(root):
    return load_research_case(write_case_dir(root))


class FakeFetcher:
    """Canned transport seam; ``fail`` flips all fetches to UNREACHABLE."""

    def __init__(self, fail: bool = False):
        self.fail = fail
        self.requests = []

    def fetch(self, url):
        self.requests.append(url)
        if self.fail:
            raise FetchError("UNREACHABLE", f"cannot fetch {url!r}.")
        return FetchResult(
            status=200, final_url=url, content_type="text/plain", raw=b"canned"
        )


def make_runtime(tmp_path, *, fetcher=None, domain_checks=None, store=None) -> ResearchRuntime:
    store = store or FileSystemRuntimeStore(tmp_path / "store")
    acquisition = SourceAcquisitionService(store, fetcher=fetcher or FakeFetcher())
    return ResearchRuntime(
        store,
        cases_dir=tmp_path,
        acquisition=acquisition,
        domain_checks=domain_checks or {"R5": lambda content: (True, ())},
    )


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


def evt(kind: EventType, event_id: str, run_id: str = RUN_ID, **overrides) -> EventEnvelope:
    return replace(
        EventEnvelope(
            event_id=event_id, event_type=kind, timestamp=TS, run_id=run_id, payload={}
        ),
        **overrides,
    )


def invocation_started_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    scope=("R1", "R2", "R3"),
    **kw,
) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_STARTED,
        f"evt-{run_id}-{invocation_id}-started",
        run_id=run_id,
        invocation_id=invocation_id,
        payload={
            "requested_scope": list(scope),
            "entry_mode": EntryMode.START.value,
            "execution_binding": {
                "workflow_identity": "research-standard",
                "workflow_version": "1.0.0",
                "runtime_configuration_identity": "research-runtime-v1",
                "prompts": {},
                "schemas": {},
            },
        },
        **kw,
    )


def attempt_created_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = "R1",
    attempt_id: str = "att-1",
    **kw,
) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_CREATED,
        f"evt-{run_id}-{attempt_id}-created",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        **kw,
    )


def input_bound_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = "R1",
    attempt_id: str = "att-1",
    **kw,
) -> EventEnvelope:
    return evt(
        EventType.INPUT_BOUND,
        f"evt-{run_id}-{attempt_id}-bound",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        payload={
            "input_binding_id": f"ib-{attempt_id}",
            "artifact_ids": [],
            "upstream_attempt_ids": [],
        },
        **kw,
    )


def attempt_started_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = "R1",
    attempt_id: str = "att-1",
    event_id: str | None = None,
    **kw,
) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_STARTED,
        event_id or f"evt-{run_id}-{attempt_id}-started",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        **kw,
    )


def build_stranded_run(store: FileSystemRuntimeStore) -> None:
    """A RUNNING invocation whose R1 attempt crashed before completion."""
    store.create_run(make_run_record())
    store.append_event(invocation_started_event())
    store.append_event(attempt_created_event())
    store.append_event(input_bound_event())
    store.append_event(attempt_started_event())
    reconcile_run(store, RUN_ID)


def projection(store: FileSystemRuntimeStore, run_id: str = RUN_ID):
    return reduce_events(store.events(run_id))


def pending_gate(store: FileSystemRuntimeStore, run_id: str = RUN_ID):
    gates = list(projection(store, run_id).gates.values())
    return gates[-1]


def attempts_of_step(store: FileSystemRuntimeStore, run_id: str, step_id: str):
    return [
        attempt
        for attempt in projection(store, run_id).attempts.values()
        if attempt.step_id == step_id
    ]


# ---------------------------------------------------------------------------
# Run creation and start
# ---------------------------------------------------------------------------


def test_create_run_freezes_case_binding(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)

    run = runtime.create_run(case)

    assert run.state is RunState.CREATED
    assert run.case_id == "case-1"
    assert run.case_binding == freeze_case_binding(case)
    assert runtime._store.load_run(run.run_id) == run


def test_start_acquires_sources_and_waits_at_h2(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)

    result = runtime.start(run.run_id)

    state = projection(runtime._store, run.run_id)
    assert result.state is RunState.WAITING_FOR_HUMAN
    assert state.run.state is RunState.WAITING_FOR_HUMAN
    invocation = state.invocations[state.run.current_invocation_id]
    assert invocation.status is InvocationStatus.RUNNING
    assert invocation.requested_scope == ("R1", "R2", "R3", "R4", "R5")
    assert invocation.entry_mode is EntryMode.START
    assert {attempt.step_id for attempt in state.attempts.values()} == {
        "R1",
        "R2",
        "R3",
    }
    assert all(
        attempt.status is AttemptStatus.SUCCEEDED
        for attempt in state.attempts.values()
    )
    # Acquisition committed a Source Artifact (no attempt lineage) and R1
    # bound it explicitly.
    source_refs = [
        ref
        for ref in state.artifacts.values()
        if ref.step_id is None and ref.attempt_id is None
    ]
    assert len(source_refs) == 1
    r1 = attempts_of_step(runtime._store, run.run_id, "R1")[0]
    binding = state.input_bindings[r1.input_binding_id]
    assert binding.artifact_ids == (source_refs[0].artifact_id,)
    gate = pending_gate(runtime._store, run.run_id)
    assert gate.logical_gate_id == "H2"
    assert gate.decision is GateDecision.PENDING
    r3 = attempts_of_step(runtime._store, run.run_id, "R3")[0]
    assert gate.review_target.attempt_id == r3.attempt_id
    assert len(projection(runtime._store, run.run_id).checkpoints) == 3


def test_bounded_start_completes_with_bounded_scope(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)

    result = runtime.start(run.run_id, until_step="R3")

    state = projection(runtime._store, run.run_id)
    assert result.state is RunState.COMPLETED
    assert result.completion_reason == COMPLETION_BOUNDED_SCOPE
    assert result.cumulative_execution_scope == ("R1", "R2", "R3")
    invocation = list(state.invocations.values())[0]
    assert invocation.status is InvocationStatus.SUCCEEDED
    assert invocation.until_step == "R3"
    assert state.gates == {}


# ---------------------------------------------------------------------------
# Gate decisions
# ---------------------------------------------------------------------------


def test_approve_h2_continues_and_waits_at_h3(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    gate = pending_gate(runtime._store, run.run_id)

    result = runtime.decide_gate(run.run_id, gate.gate_id, GateDecision.APPROVED, "human", "ok")

    state = projection(runtime._store, run.run_id)
    assert result.state is RunState.WAITING_FOR_HUMAN
    r4 = attempts_of_step(runtime._store, run.run_id, "R4")
    assert len(r4) == 1 and r4[0].status is AttemptStatus.SUCCEEDED
    h3 = pending_gate(runtime._store, run.run_id)
    assert h3.logical_gate_id == "H3"
    assert h3.review_target.attempt_id == r4[0].attempt_id
    assert state.run.state is RunState.WAITING_FOR_HUMAN


def test_reject_moves_to_needs_revision_without_rerun(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    gate = pending_gate(runtime._store, run.run_id)
    attempts_before = len(projection(runtime._store, run.run_id).attempts)

    result = runtime.decide_gate(
        run.run_id,
        gate.gate_id,
        GateDecision.REJECTED,
        "human",
        "revise the selection",
        RevisionTarget(entry_step="R2", reason="selection was wrong"),
    )

    state = projection(runtime._store, run.run_id)
    assert result.state is RunState.NEEDS_REVISION
    assert state.run.state is RunState.NEEDS_REVISION
    invocation = list(state.invocations.values())[0]
    assert invocation.status is InvocationStatus.FAILED
    assert invocation.completion_reason == "HUMAN_REJECTION"
    assert len(state.attempts) == attempts_before
    gate = state.gates[gate.gate_id]
    assert gate.decision is GateDecision.REJECTED
    assert gate.revision_target == RevisionTarget("R2", "selection was wrong")


def test_reject_without_revision_target_refused(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    gate = pending_gate(runtime._store, run.run_id)

    with pytest.raises(RuntimeContractError):
        runtime.decide_gate(run.run_id, gate.gate_id, GateDecision.REJECTED, "human", "revise")


# ---------------------------------------------------------------------------
# Revision resume
# ---------------------------------------------------------------------------


def test_resume_honors_revision_target_and_supersedes_gates(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    h2 = pending_gate(runtime._store, run.run_id)
    runtime.decide_gate(
        run.run_id,
        h2.gate_id,
        GateDecision.REJECTED,
        "human",
        "revise",
        RevisionTarget("R2", "selection was wrong"),
    )

    result = runtime.resume(run.run_id)

    state = projection(runtime._store, run.run_id)
    assert result.state is RunState.WAITING_FOR_HUMAN
    invocations = list(state.invocations.values())
    assert len(invocations) == 2
    resume_invocation = invocations[-1]
    assert resume_invocation.entry_mode is EntryMode.RESUME
    assert resume_invocation.requested_scope == ("R2", "R3", "R4", "R5")
    # R2/R3 re-executed with new attempts; the old R2/R3 checkpoints were
    # invalidated and the entry-boundary checkpoint (R1) stayed VALID.
    r2_attempts = attempts_of_step(runtime._store, run.run_id, "R2")
    r3_attempts = attempts_of_step(runtime._store, run.run_id, "R3")
    assert len(r2_attempts) == 2 and len(r3_attempts) == 2
    assert r2_attempts[-1].invocation_id == resume_invocation.invocation_id
    checkpoints = state.checkpoints
    r2_checkpoints = [
        checkpoint
        for checkpoint in checkpoints.values()
        if checkpoint.step_id == "R2"
    ]
    # The old path's checkpoint was invalidated; the re-execution recorded
    # a fresh VALID checkpoint for the new lineage.
    assert sorted(c.status.value for c in r2_checkpoints) == [
        "INVALIDATED",
        "VALID",
    ]
    r1_checkpoints = [
        checkpoint
        for checkpoint in checkpoints.values()
        if checkpoint.step_id == "R1"
    ]
    assert len(r1_checkpoints) == 1 and r1_checkpoints[0].status.value == "VALID"
    # The old H2 gate was superseded by a fresh PENDING gate on the new lineage.
    assert h2.gate_id in state.gates
    old = state.gates[h2.gate_id]
    assert old.superseded_by is not None
    replacement = state.gates[old.superseded_by]
    assert replacement.decision is GateDecision.PENDING
    assert replacement.review_target.attempt_id == r3_attempts[-1].attempt_id


def test_rejected_gate_matching_lineage_refuses_progression(tmp_path):
    # A revision entry at the barrier's downstream step itself (R4) leaves
    # the rejected R3 lineage unchanged: the orchestrator closes the new
    # invocation with HUMAN_REJECTION (the Run derives NEEDS_REVISION) and
    # refuses progression explicitly — a rejection never authorizes work on
    # the lineage it rejected.
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    h2 = pending_gate(runtime._store, run.run_id)
    runtime.decide_gate(
        run.run_id,
        h2.gate_id,
        GateDecision.REJECTED,
        "human",
        "revise",
        RevisionTarget("R4", "redo the decision only"),
    )

    with pytest.raises(RuntimeContractError):
        runtime.resume(run.run_id)

    state = projection(runtime._store, run.run_id)
    assert state.run.state is RunState.NEEDS_REVISION
    assert len(attempts_of_step(runtime._store, run.run_id, "R4")) == 0


def test_revision_lifecycle_reaches_bounded_completion(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    h2 = pending_gate(runtime._store, run.run_id)
    runtime.decide_gate(
        run.run_id,
        h2.gate_id,
        GateDecision.REJECTED,
        "human",
        "revise",
        RevisionTarget("R2", "selection was wrong"),
    )
    runtime.resume(run.run_id)

    def approve_next():
        runtime.decide_gate(
            run.run_id,
            pending_gate(runtime._store, run.run_id).gate_id,
            GateDecision.APPROVED,
            "human",
            "ok",
        )

    approve_next()
    approve_next()

    result = projection(runtime._store, run.run_id).run

    assert result.state is RunState.COMPLETED
    assert result.completion_reason == COMPLETION_BOUNDED_SCOPE
    assert result.cumulative_execution_scope == ("R2", "R3", "R4", "R5")
    assert attempts_of_step(runtime._store, run.run_id, "R5")[-1].status is AttemptStatus.SUCCEEDED


# ---------------------------------------------------------------------------
# Stranded-state closure: retry and rerun
# ---------------------------------------------------------------------------


def test_retry_reuses_same_attempt_and_invocation(tmp_path):
    store = FileSystemRuntimeStore(tmp_path / "store")
    build_stranded_run(store)
    runtime = make_runtime(tmp_path, store=store)
    before = projection(store)
    attempt = attempts_of_step(store, RUN_ID, "R1")[0]
    invocation_id = attempt.invocation_id
    assert attempt.status is AttemptStatus.FAILED

    result = runtime.retry(RUN_ID, "R1")

    state = projection(store)
    assert result.state is RunState.COMPLETED
    assert result.completion_reason == COMPLETION_BOUNDED_SCOPE
    r1_attempts = attempts_of_step(store, RUN_ID, "R1")
    assert len(r1_attempts) == 1  # the same Attempt, re-entered from FAILED
    assert r1_attempts[0].attempt_id == attempt.attempt_id
    assert r1_attempts[0].status is AttemptStatus.SUCCEEDED
    assert r1_attempts[0].invocation_id == invocation_id
    assert len(list(state.invocations.values())) == 1
    assert len(state.invocations[invocation_id].requested_scope) == 3
    # The interruption disposition was cleared by the retry round.
    assert state.failure_dispositions == {}
    assert len(before.attempts) == len(state.attempts) - 2  # R2/R3 new attempts


def test_rerun_creates_new_attempt_same_invocation(tmp_path):
    store = FileSystemRuntimeStore(tmp_path / "store")
    build_stranded_run(store)
    runtime = make_runtime(tmp_path, store=store)
    attempt = attempts_of_step(store, RUN_ID, "R1")[0]
    invocation_id = attempt.invocation_id

    result = runtime.rerun(RUN_ID, "R1")

    state = projection(store)
    assert result.state is RunState.COMPLETED
    r1_attempts = attempts_of_step(store, RUN_ID, "R1")
    assert len(r1_attempts) == 2
    assert r1_attempts[0].attempt_id == attempt.attempt_id
    assert r1_attempts[0].status is AttemptStatus.FAILED  # history never mutates
    assert r1_attempts[1].status is AttemptStatus.SUCCEEDED
    assert r1_attempts[1].invocation_id == invocation_id
    assert len(list(state.invocations.values())) == 1


def test_failed_retry_closes_invocation_durably(tmp_path):
    store = FileSystemRuntimeStore(tmp_path / "store")
    build_stranded_run(store)

    class RaisingExecutor:
        def execute(self, step, inputs):
            raise RuntimeError("still broken")

    registry = ExecutorRegistry()
    registry.register(DETERMINISTIC_MODE, RaisingExecutor())
    acquisition = SourceAcquisitionService(store, fetcher=FakeFetcher())
    runtime = ResearchRuntime(
        store,
        cases_dir=tmp_path,
        acquisition=acquisition,
        registry=registry,
        domain_checks={"R5": lambda content: (True, ())},
    )

    result = runtime.retry(RUN_ID, "R1")

    state = projection(store)
    assert result.state is RunState.FAILED
    assert result.completion_reason == "EXECUTOR_FAILED"
    r1_attempts = attempts_of_step(store, RUN_ID, "R1")
    assert len(r1_attempts) == 1
    assert r1_attempts[0].status is AttemptStatus.FAILED
    assert state.invocations[INVOCATION_ID].status is InvocationStatus.FAILED


# ---------------------------------------------------------------------------
# run_from
# ---------------------------------------------------------------------------


def test_run_from_rebuilds_downstream_and_invalidates(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id, until_step="R3")
    old_state = projection(runtime._store, run.run_id)
    old_r3_checkpoints = [
        checkpoint
        for checkpoint in old_state.checkpoints.values()
        if checkpoint.step_id == "R3"
    ]
    assert len(old_r3_checkpoints) == 1

    result = runtime.run_from(run.run_id, "R3")

    state = projection(runtime._store, run.run_id)
    assert result.state is RunState.WAITING_FOR_HUMAN
    invocations = list(state.invocations.values())
    assert len(invocations) == 2
    assert invocations[-1].entry_mode is EntryMode.FROM
    assert invocations[-1].from_step == "R3"
    assert invocations[-1].requested_scope == ("R3", "R4", "R5")
    # The old path's checkpoint was invalidated; the new R3 rebuilt lineage.
    assert state.checkpoints[old_r3_checkpoints[0].checkpoint_id].status.value == (
        "INVALIDATED"
    )
    r3_attempts = attempts_of_step(runtime._store, run.run_id, "R3")
    assert len(r3_attempts) == 2
    new_r3 = r3_attempts[-1]
    assert new_r3.invocation_id == invocations[-1].invocation_id
    assert new_r3.status is AttemptStatus.SUCCEEDED
    # The entry binding used the exact entry-boundary checkpoint artifacts.
    r2_checkpoint = [
        checkpoint
        for checkpoint in state.checkpoints.values()
        if checkpoint.step_id == "R2"
    ][0]
    assert r2_checkpoint.status.value == "VALID"
    assert state.input_bindings[new_r3.input_binding_id].artifact_ids == (
        r2_checkpoint.artifact_ids
    )
    gate = pending_gate(runtime._store, run.run_id)
    assert gate.logical_gate_id == "H2"
    assert gate.review_target.attempt_id == new_r3.attempt_id
    # Historical attempts/artifacts from the old path were never mutated.
    for artifact_id in old_state.artifacts:
        assert artifact_id in state.artifacts


def test_run_from_without_entry_checkpoint_refused(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id, until_step="R1")

    with pytest.raises(RuntimeContractError):
        runtime.run_from(run.run_id, "R3")


def test_resume_from_bounded_completion_extends_scope(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id, until_step="R3")

    result = runtime.resume(run.run_id)

    state = projection(runtime._store, run.run_id)
    assert result.state is RunState.WAITING_FOR_HUMAN
    invocations = list(state.invocations.values())
    assert len(invocations) == 2
    assert invocations[-1].entry_mode is EntryMode.RESUME
    assert invocations[-1].requested_scope == ("R4", "R5")
    gate = pending_gate(runtime._store, run.run_id)
    assert gate.logical_gate_id == "H2"
    old_r3 = attempts_of_step(runtime._store, run.run_id, "R3")[0]
    assert gate.review_target.attempt_id == old_r3.attempt_id
    assert len(attempts_of_step(runtime._store, run.run_id, "R4")) == 0


def test_resume_from_failed_acquisition_retries(tmp_path):
    case = load_case(tmp_path)
    fetcher = FakeFetcher(fail=True)
    runtime = make_runtime(tmp_path, fetcher=fetcher)
    run = runtime.create_run(case)
    result = runtime.start(run.run_id)

    assert result.state is RunState.FAILED
    assert result.completion_reason == "ACQUISITION_FAILED"
    assert projection(runtime._store, run.run_id).artifacts == {}

    fetcher.fail = False
    resumed = runtime.resume(run.run_id)

    state = projection(runtime._store, run.run_id)
    assert resumed.state is RunState.WAITING_FOR_HUMAN
    source_refs = [
        ref
        for ref in state.artifacts.values()
        if ref.step_id is None and ref.attempt_id is None
    ]
    assert len(source_refs) == 1
    r1 = attempts_of_step(runtime._store, run.run_id, "R1")
    assert len(r1) == 1
    binding = state.input_bindings[r1[0].input_binding_id]
    assert source_refs[0].artifact_id in binding.artifact_ids


# ---------------------------------------------------------------------------
# Deciding a superseded gate never authorizes progression
# ---------------------------------------------------------------------------


def test_decide_on_superseded_gate_records_only(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    prior = pending_gate(runtime._store, run.run_id)
    gates = GateRuntime(runtime._store, build_standard_workflow())
    replacement = gates.replace(
        prior.gate_id,
        prior.review_target,
        f"gate-{uuid.uuid4().hex}",
    )

    result = runtime.decide_gate(
        run.run_id, prior.gate_id, GateDecision.APPROVED, "human", "old path review"
    )

    state = projection(runtime._store, run.run_id)
    # The old gate records the review fact but never authorizes progression:
    # the replacement gate is still PENDING, so the Run still waits.
    assert state.gates[prior.gate_id].decision is GateDecision.APPROVED
    assert state.gates[prior.gate_id].superseded_by == replacement.gate_id
    assert result.state is RunState.WAITING_FOR_HUMAN
    assert state.run.state is RunState.WAITING_FOR_HUMAN
    assert len(attempts_of_step(runtime._store, run.run_id, "R4")) == 0


# ---------------------------------------------------------------------------
# State conflicts are explicit
# ---------------------------------------------------------------------------


def test_start_refuses_non_created_runs(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)

    with pytest.raises(ControlError):
        runtime.start(run.run_id)


def test_resume_refuses_created_and_waiting_runs(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    with pytest.raises(ControlError):
        runtime.resume(run.run_id)
    runtime.start(run.run_id)
    with pytest.raises(ControlError):
        runtime.resume(run.run_id)


def test_retry_refuses_succeeded_attempt(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)

    with pytest.raises(ControlError):
        runtime.retry(run.run_id, "R3")


def test_rerun_refuses_waiting_run(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)

    with pytest.raises(ControlError):
        runtime.rerun(run.run_id, "R3")


def test_run_from_refuses_created_run(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)

    with pytest.raises(RuntimeContractError):
        runtime.run_from(run.run_id, "R3")


def test_run_from_refuses_barrier_entry(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id, until_step="R3")

    with pytest.raises(RuntimeContractError):
        runtime.run_from(run.run_id, "H2")


def test_decide_gate_refuses_foreign_gate(tmp_path):
    case = load_case(tmp_path)
    runtime = make_runtime(tmp_path)
    run = runtime.create_run(case)
    runtime.start(run.run_id)
    gate = pending_gate(runtime._store, run.run_id)
    other_store = FileSystemRuntimeStore(tmp_path / "other-store")
    other_runtime = make_runtime(tmp_path, store=other_store)
    other = other_runtime.create_run(load_case(tmp_path))

    with pytest.raises(ControlError):
        other_runtime.decide_gate(other.run_id, gate.gate_id, GateDecision.APPROVED, "human", "ok")
