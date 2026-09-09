"""Tests for the Human Gate Runtime (Task 6 brief Steps 1-4, Spec section 13).

Coverage: gate creation binds a concrete committed Artifact/Candidate Set
(never merely a Step or Attempt); APPROVE records a durable whole-set
decision and resolves the derived wait state; REJECT requires a validated
RevisionTarget (the brief's verbatim assertion), records it durably and —
with the control layer's HUMAN_REJECTION invocation completion — moves the
Run to NEEDS_REVISION without auto-rerunning; generic supersession persists
the supersedes/superseded_by relationship facts (never a new Gate state);
and the revision entry boundary is validated against the Workflow
dependency graph (an entry downstream of the barrier's revision boundary
is refused).

The reducer-level NEEDS_REVISION assertion appends the INVOCATION_COMPLETED
fact directly (the invocation-completion authority is the Task 6 control
layer); the Gate Runtime itself only records durable review facts.
"""

import uuid
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    ArtifactEnvelope,
    CaseBinding,
    EntryMode,
    EventEnvelope,
    EventType,
    GateDecision,
    GateRecord,
    ReviewTarget,
    RevisionTarget,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.artifacts import commit_artifact
from ai_native_workbench.research.runtime.gates.runtime import GateRuntime
from ai_native_workbench.research.runtime.store import (
    FileSystemRuntimeStore,
    HUMAN_REJECTION,
    reduce_events,
)
from ai_native_workbench.research.runtime.workflow import build_standard_workflow

CASE_ID = "case-1"
RUN_ID = "run-1"
INVOCATION_ID = "inv-1"
STEP_ID = "R3"
ATTEMPT_ID = "att-1"
ARTIFACT_ID = "art-1"
TS = "2026-09-09T08:00:00+00:00"


# ---------------------------------------------------------------------------
# Shared fixtures/helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def make_store(tmp_path) -> FileSystemRuntimeStore:
    return FileSystemRuntimeStore(tmp_path)


def _case_binding() -> CaseBinding:
    return CaseBinding(
        case_id=CASE_ID,
        charter_identity="charter-001",
        charter_digest="sha256:" + "a" * 64,
        source_declaration_identity="urls-001",
        source_declaration_digest="sha256:" + "b" * 64,
    )


def make_run_record(run_id: str = RUN_ID, **overrides) -> RunRecord:
    defaults = dict(
        run_id=run_id,
        case_id=CASE_ID,
        case_binding=_case_binding(),
        state=RunState.CREATED,
        cumulative_execution_scope=(),
        current_invocation_id=None,
        completion_reason=None,
    )
    defaults.update(overrides)
    return RunRecord(**defaults)


def evt(kind: EventType, event_id: str, **overrides) -> EventEnvelope:
    return replace(
        EventEnvelope(
            event_id=event_id,
            event_type=kind,
            timestamp=TS,
            run_id=RUN_ID,
            payload={},
        ),
        **overrides,
    )


def _execution_binding_payload() -> dict:
    return {
        "workflow_identity": "research-standard",
        "workflow_version": "1.0.0",
        "runtime_configuration_identity": "research-runtime-v1",
        "prompts": {},
        "schemas": {},
    }


def invocation_started_event(
    run_id: str = RUN_ID, invocation_id: str = INVOCATION_ID, **kw
) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_STARTED,
        f"evt-{run_id}-{invocation_id}-started",
        run_id=run_id,
        invocation_id=invocation_id,
        payload={
            "requested_scope": ["R1", "R2", "R3", "R4", "R5"],
            "entry_mode": EntryMode.START.value,
            "execution_binding": _execution_binding_payload(),
        },
        **kw,
    )


def attempt_created_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
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
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
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
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
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


def invocation_completed_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    status: str = "SUCCEEDED",
    completion_reason: str = "BOUNDED_SCOPE",
    **kw,
) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_COMPLETED,
        f"evt-{run_id}-{invocation_id}-completed",
        run_id=run_id,
        invocation_id=invocation_id,
        payload={"status": status, "completion_reason": completion_reason},
        **kw,
    )


def commit_attempt_artifact(
    store: FileSystemRuntimeStore,
    *,
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
    artifact_id: str = ARTIFACT_ID,
    payload: object = None,
) -> ArtifactEnvelope:
    envelope = ArtifactEnvelope(
        artifact_id=artifact_id,
        run_id=run_id,
        invocation_id=invocation_id,
        artifact_schema_id="unit-output",
        artifact_schema_version="1",
        created_at=TS,
        step_id=step_id,
        attempt_id=attempt_id,
        provenance=("mode:test",),
    )
    return commit_artifact(store, envelope, payload or {"kind": "unit-output"})


def build_gate_run(
    store: FileSystemRuntimeStore,
    *,
    run_id: str = RUN_ID,
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
    artifact_id: str = ARTIFACT_ID,
) -> str:
    """create_run + started Invocation + SUCCEEDED attempt with one
    committed artifact; returns the committed artifact id."""
    store.create_run(make_run_record(run_id=run_id))
    store.append_event(invocation_started_event(run_id=run_id))
    store.append_event(
        attempt_created_event(
            run_id=run_id, step_id=step_id, attempt_id=attempt_id
        )
    )
    store.append_event(
        input_bound_event(run_id=run_id, step_id=step_id, attempt_id=attempt_id)
    )
    store.append_event(
        attempt_started_event(run_id=run_id, step_id=step_id, attempt_id=attempt_id)
    )
    commit_attempt_artifact(
        store,
        run_id=run_id,
        step_id=step_id,
        attempt_id=attempt_id,
        artifact_id=artifact_id,
    )
    store.append_event(
        evt(
            EventType.ATTEMPT_SUCCEEDED,
            f"evt-{run_id}-{attempt_id}-succeeded",
            run_id=run_id,
            invocation_id=INVOCATION_ID,
            step_id=step_id,
            attempt_id=attempt_id,
        )
    )
    return artifact_id


def make_target(
    artifact_ids: tuple[str, ...] = (ARTIFACT_ID,),
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
) -> ReviewTarget:
    return ReviewTarget(
        step_id=step_id, attempt_id=attempt_id, artifact_ids=artifact_ids
    )


# ---------------------------------------------------------------------------
# Creation binds a concrete Artifact/Candidate Set
# ---------------------------------------------------------------------------


def test_create_binds_concrete_artifact_set(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    gate = gates.create(RUN_ID, "H2", make_target())

    assert isinstance(gate, GateRecord)
    assert gate.decision is GateDecision.PENDING
    assert gate.reviewer is None and gate.decided_at is None
    assert gate.review_target.artifact_ids == (ARTIFACT_ID,)
    assert gate.review_target.attempt_id == ATTEMPT_ID
    assert gate.review_target.step_id == STEP_ID
    assert gate.logical_gate_id == "H2"
    projection = reduce_events(store.events(RUN_ID))
    assert projection.gates[gate.gate_id] == gate


def test_create_records_durable_gate_created_fact(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    gate = gates.create(RUN_ID, "H2", make_target())

    created = [
        event
        for event in store.events(RUN_ID)
        if event.event_type is EventType.GATE_CREATED
    ]
    assert len(created) == 1
    event = created[0]
    assert event.gate_id == gate.gate_id
    assert event.payload["logical_gate_id"] == "H2"
    # The envelope deep-freezes payload lists into tuples.
    assert dict(event.payload["review_target"]) == {
        "step_id": STEP_ID,
        "attempt_id": ATTEMPT_ID,
        "artifact_ids": (ARTIFACT_ID,),
    }
    # A pending Gate makes the Run wait (derived state, Ruling 10).
    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.WAITING_FOR_HUMAN


def test_create_refuses_uncommitted_artifact(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store, artifact_id="committed-art")
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.create(
            RUN_ID,
            "H2",
            make_target(artifact_ids=("never-committed-art",)),
        )


def test_create_refuses_unknown_attempt(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.create(RUN_ID, "H2", make_target(attempt_id="att-missing"))


def test_create_refuses_step_mismatch_with_attempt(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.create(RUN_ID, "H2", make_target(step_id="R2"))


def test_create_refuses_inactive_run(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    store.append_event(invocation_completed_event())
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.create(RUN_ID, "H2", make_target())


def test_create_refuses_unknown_run(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.create("run-missing", "H2", make_target())


def test_create_refuses_non_target(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.create(RUN_ID, "H2", (ARTIFACT_ID,))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Decisions: APPROVE permits progression; REJECT requires a revision target
# ---------------------------------------------------------------------------


def test_approve_records_decision_and_resolves_wait(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    gate = gates.create(RUN_ID, "H2", make_target())

    decided = gates.decide(gate.gate_id, GateDecision.APPROVED, "reviewer-1", "ok")

    assert decided.decision is GateDecision.APPROVED
    assert decided.reviewer == "reviewer-1"
    assert decided.decided_at is not None
    assert decided.comment == "ok"
    projection = reduce_events(store.events(RUN_ID))
    assert projection.gates[gate.gate_id] == decided
    # The only pending Gate resolved: the Run returns to RUNNING (derived).
    assert projection.run.state is RunState.RUNNING
    decided_events = [
        event
        for event in store.events(RUN_ID)
        if event.event_type is EventType.GATE_DECIDED
    ]
    assert len(decided_events) == 1
    assert decided_events[0].payload["decision"] == "APPROVED"
    assert decided_events[0].payload["reviewer"] == "reviewer-1"


def test_rejected_gate_requires_revision_target(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gate_runtime = GateRuntime(store)
    with pytest.raises(RuntimeContractError):
        gate_runtime.decide("gate-1", GateDecision.REJECTED, "human", "revise", None)


def test_reject_records_revision_target(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    gate = gates.create(RUN_ID, "H2", make_target())

    decided = gates.decide(
        gate.gate_id,
        GateDecision.REJECTED,
        "human",
        "revise the selection",
        RevisionTarget(entry_step="R2", reason="selection was wrong"),
    )

    assert decided.decision is GateDecision.REJECTED
    assert decided.revision_target == RevisionTarget("R2", "selection was wrong")
    decided_events = [
        event
        for event in store.events(RUN_ID)
        if event.event_type is EventType.GATE_DECIDED
    ]
    assert dict(decided_events[0].payload["revision_target"]) == {
        "entry_step": "R2",
        "reason": "selection was wrong",
    }


def test_reject_moves_run_to_needs_revision_and_does_not_autorun(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    gate = gates.create(RUN_ID, "H2", make_target())
    attempts_before = len(reduce_events(store.events(RUN_ID)).attempts)

    gates.decide(
        gate.gate_id,
        GateDecision.REJECTED,
        "human",
        "revise",
        RevisionTarget("R2", "reason"),
    )
    # The control layer's human-rejection completion fact (Task 6 emission
    # contract): the run moves to NEEDS_REVISION.
    store.append_event(
        invocation_completed_event(status="FAILED", completion_reason=HUMAN_REJECTION)
    )

    projection = reduce_events(store.events(RUN_ID))
    assert projection.run.state is RunState.NEEDS_REVISION
    assert len(projection.attempts) == attempts_before
    # No auto-rerun: no ATTEMPT_CREATED fact after the rejection.
    events = store.events(RUN_ID)
    decision_index = next(
        index
        for index, event in enumerate(events)
        if event.event_type is EventType.GATE_DECIDED
    )
    later_attempts = [
        event
        for event in events[decision_index + 1 :]
        if event.event_type is EventType.ATTEMPT_CREATED
    ]
    assert later_attempts == []


def test_approve_with_revision_target_refused(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    gate = gates.create(RUN_ID, "H2", make_target())

    with pytest.raises(RuntimeContractError):
        gates.decide(
            gate.gate_id,
            GateDecision.APPROVED,
            "human",
            "fine",
            RevisionTarget("R2", "but also revise"),
        )


def test_decide_requires_pending_gate(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    gate = gates.create(RUN_ID, "H2", make_target())
    gates.decide(gate.gate_id, GateDecision.APPROVED, "reviewer-1", "ok")

    with pytest.raises(RuntimeContractError):
        gates.decide(gate.gate_id, GateDecision.APPROVED, "reviewer-2", "again")


def test_decide_on_unknown_gate_refused(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.decide("gate-unknown", GateDecision.APPROVED, "human", "ok")


def test_decide_refuses_pending_decision_token(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    gate = gates.create(RUN_ID, "H2", make_target())

    with pytest.raises(RuntimeContractError):
        gates.decide(gate.gate_id, GateDecision.PENDING, "human", "still open")


# ---------------------------------------------------------------------------
# Generic supersession: relationship facts, never a new Gate state
# ---------------------------------------------------------------------------


def test_replace_persists_supersession_relationship(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    prior = gates.create(RUN_ID, "H2", make_target())

    replacement = gates.replace(prior.gate_id, make_target(), "gate-002")

    assert replacement.gate_id == "gate-002"
    assert replacement.supersedes == prior.gate_id
    assert replacement.decision is GateDecision.PENDING
    projection = reduce_events(store.events(RUN_ID))
    assert projection.gates[replacement.gate_id] == replacement
    # The prior record stays writable history with its relationship fact.
    superseded = projection.gates[prior.gate_id]
    assert superseded.superseded_by == "gate-002"
    assert superseded.decision is GateDecision.PENDING
    superseded_events = [
        event
        for event in store.events(RUN_ID)
        if event.event_type is EventType.GATE_SUPERSEDED
    ]
    assert len(superseded_events) == 1
    assert superseded_events[0].gate_id == prior.gate_id
    assert superseded_events[0].payload == {"superseded_by": "gate-002"}


def test_replace_inherits_logical_gate_id(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    prior = gates.create(RUN_ID, "H3", make_target())

    replacement = gates.replace(prior.gate_id, make_target(), "gate-003")

    assert replacement.logical_gate_id == "H3"


def test_replace_refuses_unknown_prior_gate(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)

    with pytest.raises(RuntimeContractError):
        gates.replace("gate-missing", make_target(), "gate-004")


def test_replace_refuses_already_superseded_gate(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    prior = gates.create(RUN_ID, "H2", make_target())
    gates.replace(prior.gate_id, make_target(), "gate-002")

    with pytest.raises(RuntimeContractError):
        gates.replace(prior.gate_id, make_target(), "gate-003")


def test_replace_refuses_self_supersession(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    prior = gates.create(RUN_ID, "H2", make_target())

    with pytest.raises(RuntimeContractError):
        gates.replace(prior.gate_id, make_target(), prior.gate_id)


def test_gate_states_remain_simple(tmp_path):
    # Supersession is a relationship, never a new Gate state (Spec 13.2).
    assert {member.value for member in GateDecision} == {
        "PENDING",
        "APPROVED",
        "REJECTED",
    }


# ---------------------------------------------------------------------------
# Revision boundary validation against the Workflow dependency graph
# ---------------------------------------------------------------------------


def test_revision_entry_downstream_of_barrier_rejected(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store, build_standard_workflow())
    gate = gates.create(RUN_ID, "H2", make_target())

    with pytest.raises(RuntimeContractError):
        gates.decide(
            gate.gate_id,
            GateDecision.REJECTED,
            "human",
            "revise",
            RevisionTarget("R5", "entry sits downstream of R4"),
        )


@pytest.mark.parametrize("entry_step", ["R4", "R3", "R2", "R1"])
def test_revision_entry_ancestor_or_self_accepted(tmp_path, entry_step):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store, build_standard_workflow())
    gate = gates.create(RUN_ID, "H2", make_target())

    decided = gates.decide(
        gate.gate_id,
        GateDecision.REJECTED,
        "human",
        "revise",
        RevisionTarget(entry_step, "reason"),
    )

    assert decided.decision is GateDecision.REJECTED
    assert decided.revision_target.entry_step == entry_step


def test_revision_entry_unknown_step_rejected(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store, build_standard_workflow())
    gate = gates.create(RUN_ID, "H2", make_target())

    with pytest.raises(RuntimeContractError):
        gates.decide(
            gate.gate_id,
            GateDecision.REJECTED,
            "human",
            "revise",
            RevisionTarget("R9", "not a step"),
        )


def test_revision_entry_barrier_id_rejected(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store, build_standard_workflow())
    gate = gates.create(RUN_ID, "H2", make_target())

    with pytest.raises(RuntimeContractError):
        gates.decide(
            gate.gate_id,
            GateDecision.REJECTED,
            "human",
            "revise",
            RevisionTarget("H3", "barriers are never steps"),
        )


# ---------------------------------------------------------------------------
# Review facts stay writable; resolution survives a fresh instance
# ---------------------------------------------------------------------------


def test_decide_superseded_gate_still_records_review_fact(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    prior = gates.create(RUN_ID, "H2", make_target())
    gates.replace(prior.gate_id, make_target(), "gate-002")

    decided = gates.decide(
        prior.gate_id, GateDecision.APPROVED, "human", "old path review"
    )

    # The old Gate record stays writable as a review fact (Ruling 2), but the
    # supersession relationship is never erased.
    assert decided.decision is GateDecision.APPROVED
    assert decided.superseded_by == "gate-002"


def test_gate_resolution_survives_fresh_instance(tmp_path):
    store = make_store(tmp_path)
    build_gate_run(store)
    gates = GateRuntime(store)
    gate = gates.create(RUN_ID, "H2", make_target())

    # A fresh instance mirrors a process restart: the durable gate fact is
    # resolved from the store, not from instance memory.
    restarted = GateRuntime(store)
    decided = restarted.decide(gate.gate_id, GateDecision.APPROVED, "human", "ok")

    assert decided.decision is GateDecision.APPROVED
    projection = reduce_events(store.events(RUN_ID))
    assert projection.gates[gate.gate_id].decision is GateDecision.APPROVED
