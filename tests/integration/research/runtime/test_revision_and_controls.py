"""Integration tests: revision lifecycle and explicit controls over the real store.

Runs the full Research Runtime lifecycle over a real FileSystemRuntimeStore
(tmp_path): start through H2, human REJECT with a revision target, resume
honoring the revision target, gate supersession on the new path, APPROVE,
and bounded completion. Also covers stranded-state closure via retry/rerun
after an interrupted attempt (crash reconciliation) and run_from
invalidating the old path. Only the transport seam is faked (the brief
explicitly allows a fake executor/transport where that is the point);
execution itself uses the registered DeterministicExecutor.
"""

import uuid
from dataclasses import replace

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
)
from ai_native_workbench.research.runtime.binding import load_research_case
from ai_native_workbench.research.runtime.control import ResearchRuntime
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

RUN_ID = "run-1"
INVOCATION_ID = "inv-1"
TS = "2026-09-09T08:00:00+00:00"
SOURCE_URL = "http://example.test/src.txt"


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def write_case_dir(root):
    case_dir = root / "case-1"
    case_dir.mkdir(exist_ok=True)
    (case_dir / "inputs").mkdir(parents=True, exist_ok=True)
    (case_dir / "00-research-charter.md").write_text("# charter\n", encoding="utf-8")
    (case_dir / "inputs" / "urls.yaml").write_text(
        f"- id: src-1\n  url: {SOURCE_URL}\n  required: true\n",
        encoding="utf-8",
    )
    return case_dir


class FakeFetcher:
    def __init__(self):
        self.requests = []

    def fetch(self, url):
        self.requests.append(url)
        if not self.requests:
            raise FetchError("UNREACHABLE", url)
        return FetchResult(
            status=200, final_url=url, content_type="text/plain", raw=b"canned"
        )


def make_runtime(tmp_path, *, store=None) -> ResearchRuntime:
    store = store or FileSystemRuntimeStore(tmp_path / "store")
    acquisition = SourceAcquisitionService(store, fetcher=FakeFetcher())
    return ResearchRuntime(
        store,
        cases_dir=tmp_path,
        acquisition=acquisition,
        domain_checks={"R5": lambda content: (True, ())},
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


def evt(kind, event_id, run_id=RUN_ID, **overrides):
    return replace(
        EventEnvelope(
            event_id=event_id, event_type=kind, timestamp=TS, run_id=run_id, payload={}
        ),
        **overrides,
    )


def invocation_started_event(run_id=RUN_ID, invocation_id=INVOCATION_ID, **kw):
    return evt(
        EventType.INVOCATION_STARTED,
        f"evt-{run_id}-{invocation_id}-started",
        run_id=run_id,
        invocation_id=invocation_id,
        payload={
            "requested_scope": ["R1", "R2", "R3"],
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


def attempt_created_event(run_id=RUN_ID, invocation_id=INVOCATION_ID, attempt_id="att-1", **kw):
    return evt(
        EventType.ATTEMPT_CREATED,
        f"evt-{run_id}-{attempt_id}-created",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id="R1",
        attempt_id=attempt_id,
        **kw,
    )


def input_bound_event(run_id=RUN_ID, invocation_id=INVOCATION_ID, attempt_id="att-1", **kw):
    return evt(
        EventType.INPUT_BOUND,
        f"evt-{run_id}-{attempt_id}-bound",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id="R1",
        attempt_id=attempt_id,
        payload={
            "input_binding_id": f"ib-{attempt_id}",
            "artifact_ids": [],
            "upstream_attempt_ids": [],
        },
        **kw,
    )


def attempt_started_event(run_id=RUN_ID, invocation_id=INVOCATION_ID, attempt_id="att-1", **kw):
    return evt(
        EventType.ATTEMPT_STARTED,
        f"evt-{run_id}-{attempt_id}-started",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id="R1",
        attempt_id=attempt_id,
        **kw,
    )


def build_interrupted_run(store: FileSystemRuntimeStore) -> None:
    """A RUNNING invocation whose R1 attempt crashed before its terminal fact."""
    store.create_run(make_run_record())
    store.append_event(invocation_started_event())
    store.append_event(attempt_created_event())
    store.append_event(input_bound_event())
    store.append_event(attempt_started_event())
    reconcile_run(store, RUN_ID)


def projection(store: FileSystemRuntimeStore, run_id: str = RUN_ID):
    return reduce_events(store.events(run_id))


def pending_gate(store: FileSystemRuntimeStore, run_id: str = RUN_ID):
    return list(projection(store, run_id).gates.values())[-1]


def attempts_of_step(store: FileSystemRuntimeStore, run_id: str, step_id: str):
    return [
        attempt
        for attempt in projection(store, run_id).attempts.values()
        if attempt.step_id == step_id
    ]


# ---------------------------------------------------------------------------
# Full revision lifecycle
# ---------------------------------------------------------------------------


def test_full_revision_lifecycle_with_bounded_completion(tmp_path):
    case = load_research_case(write_case_dir(tmp_path))
    runtime = make_runtime(tmp_path)
    store = runtime._store
    run = runtime.create_run(case)

    # 1. start: acquisition + R1..R3, then wait at the H2 barrier.
    waiting = runtime.start(run.run_id)
    assert waiting.state is RunState.WAITING_FOR_HUMAN
    state = projection(store, run.run_id)
    invocation_one = list(state.invocations.values())[0]
    assert invocation_one.status is InvocationStatus.RUNNING
    h2 = pending_gate(store, run.run_id)
    assert h2.logical_gate_id == "H2"

    # 2. human REJECT with a revision target: NEEDS_REVISION, no auto-rerun.
    rejected = runtime.decide_gate(
        run.run_id,
        h2.gate_id,
        GateDecision.REJECTED,
        "human",
        "the selection is wrong",
        RevisionTarget(entry_step="R2", reason="selection was wrong"),
    )
    assert rejected.state is RunState.NEEDS_REVISION
    state = projection(store, run.run_id)
    assert state.invocations[invocation_one.invocation_id].status is (
        InvocationStatus.FAILED
    )
    assert state.invocations[invocation_one.invocation_id].completion_reason == (
        "HUMAN_REJECTION"
    )
    attempts_after_reject = len(state.attempts)

    # 3. resume honors the revision target: R2..R5 re-executed, the old H2
    # gate superseded by a fresh one on the new lineage.
    runtime.resume(run.run_id)
    state = projection(store, run.run_id)
    invocations = list(state.invocations.values())
    assert len(invocations) == 2
    assert invocations[-1].entry_mode is EntryMode.RESUME
    assert invocations[-1].requested_scope == ("R2", "R3", "R4", "R5")
    assert state.run.state is RunState.WAITING_FOR_HUMAN
    old_h2 = state.gates[h2.gate_id]
    assert old_h2.superseded_by is not None
    new_h2 = state.gates[old_h2.superseded_by]
    assert new_h2.decision is GateDecision.PENDING
    assert new_h2.review_target.attempt_id == attempts_of_step(
        store, run.run_id, "R3"
    )[-1].attempt_id
    # Historical attempts were never mutated.
    assert len(state.attempts) > attempts_after_reject

    # 4. approve the new path: R4 defers to H3, approve H3, R5 completes.
    runtime.decide_gate(
        run.run_id, new_h2.gate_id, GateDecision.APPROVED, "human", "ok"
    )
    state = projection(store, run.run_id)
    assert state.run.state is RunState.WAITING_FOR_HUMAN
    h3 = pending_gate(store, run.run_id)
    assert h3.logical_gate_id == "H3"
    completed = runtime.decide_gate(
        run.run_id, h3.gate_id, GateDecision.APPROVED, "human", "ok"
    )
    assert completed.state is RunState.COMPLETED
    assert completed.completion_reason == "BOUNDED_SCOPE"
    assert completed.cumulative_execution_scope == ("R2", "R3", "R4", "R5")
    r5 = attempts_of_step(store, run.run_id, "R5")
    assert r5[-1].status is AttemptStatus.SUCCEEDED
    # The whole history is durable and inspectable.
    assert store.events(run.run_id)


# ---------------------------------------------------------------------------
# Stranded-state closure: retry / rerun after an interrupted attempt
# ---------------------------------------------------------------------------


def test_retry_closes_interrupted_attempt(tmp_path):
    store = FileSystemRuntimeStore(tmp_path / "store")
    build_interrupted_run(store)
    runtime = make_runtime(tmp_path, store=store)
    interrupted = attempts_of_step(store, RUN_ID, "R1")[0]
    assert interrupted.status is AttemptStatus.FAILED
    assert projection(store).failure_dispositions[
        interrupted.attempt_id
    ] == "EXECUTION_INTERRUPTED"

    result = runtime.retry(RUN_ID, "R1")

    state = projection(store)
    assert result.state is RunState.COMPLETED
    assert result.completion_reason == "BOUNDED_SCOPE"
    r1_attempts = attempts_of_step(store, RUN_ID, "R1")
    assert len(r1_attempts) == 1
    assert r1_attempts[0].attempt_id == interrupted.attempt_id  # same Attempt
    assert r1_attempts[0].status is AttemptStatus.SUCCEEDED
    assert len(state.invocations) == 1  # same Invocation
    assert state.failure_dispositions == {}  # disposition cleared by the round


def test_rerun_closes_interrupted_attempt_with_new_lineage(tmp_path):
    store = FileSystemRuntimeStore(tmp_path / "store")
    build_interrupted_run(store)
    runtime = make_runtime(tmp_path, store=store)
    interrupted = attempts_of_step(store, RUN_ID, "R1")[0]

    result = runtime.rerun(RUN_ID, "R1")

    state = projection(store)
    assert result.state is RunState.COMPLETED
    r1_attempts = attempts_of_step(store, RUN_ID, "R1")
    assert len(r1_attempts) == 2  # a new Attempt inside the same Invocation
    assert r1_attempts[0].attempt_id == interrupted.attempt_id
    assert r1_attempts[0].status is AttemptStatus.FAILED  # history immutable
    assert r1_attempts[1].status is AttemptStatus.SUCCEEDED
    assert r1_attempts[1].invocation_id == interrupted.invocation_id
    assert len(state.invocations) == 1


# ---------------------------------------------------------------------------
# run_from invalidates the old path
# ---------------------------------------------------------------------------


def test_run_from_invalidates_old_path(tmp_path):
    case = load_research_case(write_case_dir(tmp_path))
    runtime = make_runtime(tmp_path)
    store = runtime._store
    run = runtime.create_run(case)
    runtime.start(run.run_id, until_step="R3")
    old_state = projection(store, run.run_id)
    old_r3_checkpoints = [
        checkpoint
        for checkpoint in old_state.checkpoints.values()
        if checkpoint.step_id == "R3"
    ]
    assert len(old_r3_checkpoints) == 1
    old_r3_attempt = attempts_of_step(store, run.run_id, "R3")[0]
    old_artifacts = dict(old_state.artifacts)

    result = runtime.run_from(run.run_id, "R3")

    state = projection(store, run.run_id)
    assert result.state is RunState.WAITING_FOR_HUMAN
    invocations = list(state.invocations.values())
    assert len(invocations) == 2
    assert invocations[-1].entry_mode is EntryMode.FROM
    assert invocations[-1].from_step == "R3"
    # The old path's checkpoint was invalidated; the new lineage rebuilt.
    assert state.checkpoints[old_r3_checkpoints[0].checkpoint_id].status.value == (
        "INVALIDATED"
    )
    r3_attempts = attempts_of_step(store, run.run_id, "R3")
    assert len(r3_attempts) == 2
    new_r3 = r3_attempts[-1]
    assert new_r3.status is AttemptStatus.SUCCEEDED
    assert new_r3.attempt_id != old_r3_attempt.attempt_id
    # The new path binds the exact entry-boundary checkpoint artifacts.
    r2_checkpoint = [
        checkpoint
        for checkpoint in state.checkpoints.values()
        if checkpoint.step_id == "R2"
    ][0]
    assert r2_checkpoint.status.value == "VALID"
    assert state.input_bindings[new_r3.input_binding_id].artifact_ids == (
        r2_checkpoint.artifact_ids
    )
    # The fresh barrier gate reviews the new lineage.
    gate = pending_gate(store, run.run_id)
    assert gate.logical_gate_id == "H2"
    assert gate.review_target.attempt_id == new_r3.attempt_id
    # Historical attempts/artifacts were never mutated.
    for artifact_id, reference in old_artifacts.items():
        assert state.artifacts[artifact_id] == reference


# ---------------------------------------------------------------------------
# Bounded completion, then resume to extend the scope
# ---------------------------------------------------------------------------


def test_bounded_completion_then_resume_extends_scope(tmp_path):
    case = load_research_case(write_case_dir(tmp_path))
    runtime = make_runtime(tmp_path)
    store = runtime._store
    run = runtime.create_run(case)
    bounded = runtime.start(run.run_id, until_step="R3")
    assert bounded.state is RunState.COMPLETED
    assert bounded.cumulative_execution_scope == ("R1", "R2", "R3")

    waiting = runtime.resume(run.run_id)

    assert waiting.state is RunState.WAITING_FOR_HUMAN
    state = projection(store, run.run_id)
    invocations = list(state.invocations.values())
    assert len(invocations) == 2
    assert invocations[-1].requested_scope == ("R4", "R5")
    # H2 is raised at the extended boundary, reviewing the existing R3 path.
    h2 = pending_gate(store, run.run_id)
    assert h2.logical_gate_id == "H2"
    assert h2.review_target.attempt_id == attempts_of_step(store, run.run_id, "R3")[
        0
    ].attempt_id
    runtime.decide_gate(run.run_id, h2.gate_id, GateDecision.APPROVED, "human", "ok")
    h3 = pending_gate(store, run.run_id)
    assert h3.logical_gate_id == "H3"
    completed = runtime.decide_gate(
        run.run_id, h3.gate_id, GateDecision.APPROVED, "human", "ok"
    )
    assert completed.state is RunState.COMPLETED
    assert completed.cumulative_execution_scope == ("R1", "R2", "R3", "R4", "R5")
