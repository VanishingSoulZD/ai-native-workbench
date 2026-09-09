"""Tests for the projection reducer and run.json document codec.

The reducer is a fact-reduction engine: it reconstructs current
Run/Invocation/Attempt/Gate/Checkpoint/artifact/canonical/snapshot state
from the event history alone (durable evidence is verified separately by
reconciliation). Payload contracts exercised here are the v1 contracts the
control-layer emitters (Tasks 6/7) must produce.
"""

import json
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    AttemptStatus,
    ArtifactEnvelope,
    CheckpointStatus,
    EntryMode,
    EventEnvelope,
    EventType,
    GateDecision,
    InvocationStatus,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.store import (
    ProjectionSchemaError,
    RunProjection,
    reduce_events,
    parse_projection,
    serialize_projection,
)

TS = "2026-09-09T00:00:00+00:00"
RUN_ID = "run-1"
DIGEST_A = "sha256:" + "a" * 64
DIGEST_D = "sha256:" + "d" * 64


# ---------------------------------------------------------------------------
# Event builders (the v1 payload contracts)
# ---------------------------------------------------------------------------


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


def run_created_event(**kw) -> EventEnvelope:
    return evt(
        EventType.RUN_CREATED,
        **{
            "event_id": "evt-run-created",
            "payload": {
                "case_id": "case-1",
                "charter_identity": "charter-001",
                "charter_digest": DIGEST_A,
                "source_declaration_identity": "urls-001",
                "source_declaration_digest": DIGEST_A,
            },
            **kw,
        },
    )


def invocation_started_event(**kw) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_STARTED,
        **{
            "event_id": "evt-inv-1",
            "invocation_id": "inv-1",
            "payload": {
                "requested_scope": ["R1"],
                "entry_mode": "START",
                "execution_binding": {
                    "workflow_identity": "research-workflow",
                    "workflow_version": "v1",
                    "runtime_configuration_identity": "runtime-config-001",
                    "prompts": {},
                    "schemas": {},
                },
            },
            **kw,
        },
    )


def attempt_created_event(**kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_CREATED,
        **{
            "event_id": "evt-att-1",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": "att-1",
            "payload": {},
            **kw,
        },
    )


def input_bound_event(**kw) -> EventEnvelope:
    return evt(
        EventType.INPUT_BOUND,
        **{
            "event_id": "evt-ib-1",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": "att-1",
            "payload": {
                "input_binding_id": "ib-1",
                "artifact_ids": [],
                "upstream_attempt_ids": [],
            },
            **kw,
        },
    )


def attempt_started_event(**kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_STARTED,
        **{
            "event_id": "evt-att-start-1",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": "att-1",
            "payload": {},
            **kw,
        },
    )


def artifact_committed_event(**kw) -> EventEnvelope:
    return evt(
        EventType.ARTIFACT_COMMITTED,
        **{
            "event_id": "evt-art-1",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": "att-1",
            "artifact_id": "art-1",
            "payload": {"digest": DIGEST_D},
            **kw,
        },
    )


def attempt_succeeded_event(**kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_SUCCEEDED,
        **{
            "event_id": "evt-att-ok-1",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": "att-1",
            "payload": {},
            **kw,
        },
    )


def gate_created_event(**kw) -> EventEnvelope:
    return evt(
        EventType.GATE_CREATED,
        **{
            "event_id": "evt-gate-1",
            "gate_id": "gate-1",
            "payload": {
                "logical_gate_id": "H2",
                "review_target": {
                    "step_id": "R1",
                    "attempt_id": "att-1",
                    "artifact_ids": ["art-1"],
                },
            },
            **kw,
        },
    )


def gate_decided_event(**kw) -> EventEnvelope:
    return evt(
        EventType.GATE_DECIDED,
        **{
            "event_id": "evt-gate-dec-1",
            "gate_id": "gate-1",
            "payload": {
                "decision": "APPROVED",
                "reviewer": "human",
                "decided_at": TS,
                "comment": "ok",
            },
            **kw,
        },
    )


def invocation_completed_event(**kw) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_COMPLETED,
        **{
            "event_id": "evt-inv-done-1",
            "invocation_id": "inv-1",
            "payload": {"status": "SUCCEEDED", "completion_reason": "BOUNDED_SCOPE"},
            **kw,
        },
    )


def cycle_events() -> tuple[EventEnvelope, ...]:
    """RUN_CREATED -> INVOCATION_STARTED -> R1 attempt cycle -> success."""
    return (
        run_created_event(),
        invocation_started_event(),
        attempt_created_event(),
        input_bound_event(),
        attempt_started_event(),
        artifact_committed_event(),
        attempt_succeeded_event(),
    )


# ---------------------------------------------------------------------------
# Reducer: happy-path state reconstruction
# ---------------------------------------------------------------------------


def test_reduce_run_created_only():
    projection = reduce_events([run_created_event()])
    assert projection.run.state is RunState.CREATED
    assert projection.run.case_id == "case-1"
    assert projection.run.case_binding.charter_identity == "charter-001"
    assert projection.run.cumulative_execution_scope == ()
    assert projection.run.current_invocation_id is None
    assert projection.invocations == {}
    assert projection.attempts == {}
    assert projection.gates == {}
    assert projection.snapshot_binding is None


def test_reduce_invocation_started_moves_run_running():
    projection = reduce_events(
        [run_created_event(), invocation_started_event()]
    )
    assert projection.run.state is RunState.RUNNING
    assert projection.run.current_invocation_id == "inv-1"
    invocation = projection.invocations["inv-1"]
    assert invocation.status is InvocationStatus.RUNNING
    assert invocation.entry_mode is EntryMode.START
    assert invocation.requested_scope == ("R1",)
    assert invocation.execution_binding.workflow_identity == "research-workflow"


def test_reduce_attempt_cycle():
    projection = reduce_events(cycle_events())
    assert projection.run.state is RunState.RUNNING
    attempt = projection.attempts["att-1"]
    assert attempt.status is AttemptStatus.SUCCEEDED
    assert attempt.input_binding_id == "ib-1"
    assert projection.input_bindings["ib-1"].attempt_id == "att-1"
    reference = projection.artifacts["art-1"]
    assert reference.digest == DIGEST_D
    assert reference.attempt_id == "att-1"
    assert reference.step_id == "R1"
    assert reference.committed_at == TS
    assert projection.failure_dispositions == {}


def test_reduce_gate_creation_waits_for_human():
    projection = reduce_events(cycle_events() + (gate_created_event(),))
    assert projection.run.state is RunState.WAITING_FOR_HUMAN
    gate = projection.gates["gate-1"]
    assert gate.decision is GateDecision.PENDING
    assert gate.logical_gate_id == "H2"
    assert gate.review_target.artifact_ids == ("art-1",)


def test_reduce_gate_approval_resumes_run():
    events = cycle_events() + (
        gate_created_event(),
        gate_decided_event(),
    )
    projection = reduce_events(events)
    assert projection.run.state is RunState.RUNNING
    gate = projection.gates["gate-1"]
    assert gate.decision is GateDecision.APPROVED
    assert gate.reviewer == "human"
    assert gate.decided_at == TS


def test_reduce_invocation_completion_completes_bounded_run():
    events = cycle_events() + (
        gate_created_event(),
        gate_decided_event(),
        invocation_completed_event(),
    )
    projection = reduce_events(events)
    assert projection.run.state is RunState.COMPLETED
    assert projection.run.completion_reason == "BOUNDED_SCOPE"
    assert projection.run.cumulative_execution_scope == ("R1",)
    assert projection.run.current_invocation_id is None
    invocation = projection.invocations["inv-1"]
    assert invocation.status is InvocationStatus.SUCCEEDED


def test_reduce_resume_creates_new_invocation():
    events = cycle_events() + (
        gate_created_event(),
        gate_decided_event(),
        invocation_completed_event(),
        evt(
            EventType.INVOCATION_STARTED,
            "evt-inv-2",
            invocation_id="inv-2",
            payload={
                "requested_scope": ["R2"],
                "entry_mode": "RESUME",
                "execution_binding": {
                    "workflow_identity": "research-workflow",
                    "workflow_version": "v1",
                    "runtime_configuration_identity": "runtime-config-001",
                    "prompts": {},
                    "schemas": {},
                },
            },
        ),
    )
    projection = reduce_events(events)
    assert projection.run.state is RunState.RUNNING
    assert projection.run.completion_reason is None
    assert projection.run.cumulative_execution_scope == ("R1",)  # history kept
    assert projection.run.current_invocation_id == "inv-2"
    assert set(projection.invocations) == {"inv-1", "inv-2"}
    assert projection.invocations["inv-2"].entry_mode is EntryMode.RESUME


def test_reduce_invocation_failure_fails_run():
    events = cycle_events() + (
        invocation_completed_event(
            event_id="evt-inv-fail-1",
            payload={"status": "FAILED", "completion_reason": "EXECUTION_ERROR"},
        ),
    )
    projection = reduce_events(events)
    assert projection.run.state is RunState.FAILED
    assert projection.run.completion_reason == "EXECUTION_ERROR"
    assert projection.invocations["inv-1"].status is InvocationStatus.FAILED


def test_reduce_human_rejection_moves_run_needs_revision():
    events = cycle_events() + (
        gate_created_event(),
        gate_decided_event(
            event_id="evt-gate-rej-1",
            payload={
                "decision": "REJECTED",
                "reviewer": "human",
                "decided_at": TS,
                "comment": "revise the analysis",
                "revision_target": {"entry_step": "R2", "reason": "insufficient depth"},
            },
        ),
        invocation_completed_event(
            event_id="evt-inv-rej-1",
            payload={"status": "FAILED", "completion_reason": "HUMAN_REJECTION"},
        ),
    )
    projection = reduce_events(events)
    assert projection.run.state is RunState.NEEDS_REVISION
    assert projection.run.completion_reason is None  # reason lives in the gate
    gate = projection.gates["gate-1"]
    assert gate.decision is GateDecision.REJECTED
    assert gate.revision_target is not None
    assert gate.revision_target.entry_step == "R2"
    assert projection.invocations["inv-1"].status is InvocationStatus.FAILED
    assert projection.invocations["inv-1"].completion_reason == "HUMAN_REJECTION"


def test_reduce_attempt_failure_records_disposition_without_moving_run():
    events = cycle_events()[:5] + (
        evt(
            EventType.ATTEMPT_FAILED,
            "evt-att-fail-1",
            invocation_id="inv-1",
            step_id="R1",
            attempt_id="att-1",
            payload={"disposition": "EXECUTION_INTERRUPTED"},
        ),
    )
    projection = reduce_events(events)
    assert projection.attempts["att-1"].status is AttemptStatus.FAILED
    assert projection.failure_dispositions == {"att-1": "EXECUTION_INTERRUPTED"}
    # Ruling 12: interruption reconciliation stays at ATTEMPT level only.
    assert projection.invocations["inv-1"].status is InvocationStatus.RUNNING
    assert projection.run.state is RunState.RUNNING


def test_reduce_retry_moves_failed_attempt_back_to_running():
    events = cycle_events()[:5] + (
        evt(
            EventType.ATTEMPT_FAILED,
            "evt-att-fail-1",
            invocation_id="inv-1",
            step_id="R1",
            attempt_id="att-1",
            payload={"disposition": "EXECUTION_ERROR"},
        ),
        evt(
            EventType.ATTEMPT_STARTED,
            "evt-att-restart-1",
            invocation_id="inv-1",
            step_id="R1",
            attempt_id="att-1",
            payload={},
        ),
    )
    projection = reduce_events(events)
    assert projection.attempts["att-1"].status is AttemptStatus.RUNNING
    assert projection.attempts["att-1"].input_binding_id == "ib-1"
    # The stale disposition is cleared once a retry round starts.
    assert projection.failure_dispositions == {}


def test_reduce_checkpoint_creation_and_invalidation():
    events = cycle_events() + (
        evt(
            EventType.CHECKPOINT_CREATED,
            "evt-cp-1",
            step_id="R1",
            payload={
                "checkpoint_id": "cp-1",
                "artifact_ids": ["art-1"],
                "compatibility": {
                    "workflow_identity": "research-workflow",
                    "workflow_version": "v1",
                    "step_identity": "r1",
                    "step_version": "1",
                    "runtime_configuration_identity": "runtime-config-001",
                    "prompt_identity": "prompt-r1",
                    "prompt_version": "2",
                },
            },
        ),
        evt(
            EventType.CHECKPOINT_INVALIDATED,
            "evt-cp-inv-1",
            step_id="R1",
            payload={"checkpoint_id": "cp-1"},
        ),
    )
    projection = reduce_events(events)
    checkpoint = projection.checkpoints["cp-1"]
    assert checkpoint.status is CheckpointStatus.INVALIDATED
    assert checkpoint.artifact_ids == ("art-1",)
    assert checkpoint.compatibility.workflow_identity == "research-workflow"
    assert checkpoint.compatibility.prompt_identity == "prompt-r1"
    assert checkpoint.compatibility.prompt_version == "2"


def test_reduce_canonical_and_snapshot_bindings():
    events = cycle_events() + (
        evt(
            EventType.CANONICAL_BINDING_PENDING,
            "evt-cb-pend-1",
            artifact_id="art-1",
            payload={},
        ),
        evt(
            EventType.CANONICAL_BINDING_COMMITTED,
            "evt-cb-com-1",
            artifact_id="art-1",
            payload={},
        ),
        evt(
            EventType.SNAPSHOT_BOUND,
            "evt-snap-1",
            payload={"snapshot_id": "snap-1"},
        ),
    )
    projection = reduce_events(events)
    binding = projection.canonical_bindings["art-1"]
    assert binding.status == "COMMITTED"
    assert binding.updated_at == TS
    assert projection.snapshot_binding is not None
    assert projection.snapshot_binding.snapshot_id == "snap-1"
    assert projection.snapshot_binding.bound_at == TS


def test_reduce_gate_supersession_keeps_waiting_on_replacement():
    events = cycle_events() + (
        evt(
            EventType.GATE_CREATED,
            "evt-gate-1",
            gate_id="gate-1",
            payload={
                "logical_gate_id": "H2",
                "review_target": {
                    "step_id": "R1",
                    "attempt_id": "att-1",
                    "artifact_ids": ["art-1"],
                },
            },
        ),
        # A new execution path creates a replacement gate first...
        evt(
            EventType.GATE_CREATED,
            "evt-gate-2",
            gate_id="gate-2",
            payload={
                "logical_gate_id": "H2",
                "supersedes": "gate-1",
                "review_target": {
                    "step_id": "R1",
                    "attempt_id": "att-1",
                    "artifact_ids": ["art-1"],
                },
            },
        ),
        # ...then the old gate is marked superseded.
        evt(
            EventType.GATE_SUPERSEDED,
            "evt-gate-sup-1",
            gate_id="gate-1",
            payload={"superseded_by": "gate-2"},
        ),
    )
    projection = reduce_events(events)
    assert projection.gates["gate-1"].superseded_by == "gate-2"
    assert projection.gates["gate-2"].supersedes == "gate-1"
    # The replacement gate is still PENDING, so the Run keeps waiting.
    assert projection.run.state is RunState.WAITING_FOR_HUMAN
    decided = reduce_events(
        events + (gate_decided_event(event_id="evt-gate-dec-2", gate_id="gate-2"),)
    )
    assert decided.run.state is RunState.RUNNING


def test_reduce_run_state_changed_is_a_validated_noop():
    """Ruling 10: RUN_STATE_CHANGED is vocabulary-only in v1 and never emitted."""
    events = cycle_events() + (
        evt(
            EventType.RUN_STATE_CHANGED,
            "evt-state-1",
            payload={"state": "RUNNING", "comment": "audit-only record"},
        ),
    )
    projection = reduce_events(events)
    assert projection.run.state is RunState.RUNNING
    baseline = reduce_events(cycle_events())
    assert projection.run == baseline.run


def test_reduce_validation_and_acceptance_are_log_facts_only():
    events = cycle_events() + (
        evt(
            EventType.VALIDATION_COMPLETED,
            "evt-val-1",
            artifact_id="art-1",
            payload={"result": "PASSED"},
        ),
        evt(
            EventType.ACCEPTANCE_RECORDED,
            "evt-acc-1",
            artifact_id="art-1",
            payload={"result": "ACCEPTED", "policy": "automatic"},
        ),
    )
    projection = reduce_events(events)
    assert projection == reduce_events(cycle_events())


def test_reduce_covers_every_event_type_member():
    """Ruling 2: the reducer interprets the full v1 vocabulary."""
    events = cycle_events() + (
        evt(
            EventType.VALIDATION_COMPLETED,
            "evt-val-1",
            artifact_id="art-1",
            payload={},
        ),
        evt(
            EventType.ACCEPTANCE_RECORDED,
            "evt-acc-1",
            artifact_id="art-1",
            payload={},
        ),
        evt(
            EventType.GATE_CREATED,
            "evt-gate-1",
            gate_id="gate-1",
            payload={
                "logical_gate_id": "H2",
                "review_target": {
                    "step_id": "R1",
                    "attempt_id": "att-1",
                    "artifact_ids": ["art-1"],
                },
            },
        ),
        evt(
            EventType.CHECKPOINT_CREATED,
            "evt-cp-1",
            step_id="R1",
            payload={
                "checkpoint_id": "cp-1",
                "artifact_ids": ["art-1"],
                "compatibility": {
                    "workflow_identity": "research-workflow",
                    "workflow_version": "v1",
                    "step_identity": "r1",
                    "step_version": "1",
                    "runtime_configuration_identity": "runtime-config-001",
                },
            },
        ),
        evt(
            EventType.CANONICAL_BINDING_PENDING,
            "evt-cb-pend-1",
            artifact_id="art-1",
            payload={},
        ),
        evt(
            EventType.RUN_STATE_CHANGED,
            "evt-state-1",
            payload={"state": "RUNNING"},
        ),
    )
    projection = reduce_events(events)
    assert projection.gates["gate-1"].decision is GateDecision.PENDING
    assert projection.checkpoints["cp-1"].status is CheckpointStatus.VALID
    assert projection.canonical_bindings["art-1"].status == "PENDING"


def test_reduce_source_acquisition_artifact_has_no_attempt_lineage():
    events = (
        run_created_event(),
        invocation_started_event(),
        artifact_committed_event(
            event_id="evt-src-1",
            artifact_id="src-1",
            step_id=None,
            attempt_id=None,
            payload={"digest": DIGEST_A},
        ),
    )
    projection = reduce_events(events)
    reference = projection.artifacts["src-1"]
    assert reference.step_id is None
    assert reference.attempt_id is None


# ---------------------------------------------------------------------------
# Reducer: history contradictions fail fast
# ---------------------------------------------------------------------------


def test_reduce_requires_run_created_first():
    with pytest.raises(RuntimeContractError):
        reduce_events([invocation_started_event()])


def test_reduce_rejects_empty_log_and_duplicate_run_created():
    with pytest.raises(RuntimeContractError):
        reduce_events([])
    with pytest.raises(RuntimeContractError):
        reduce_events([run_created_event(), run_created_event(event_id="evt-rc-2")])


def test_reduce_rejects_event_for_another_run():
    with pytest.raises(RuntimeContractError):
        reduce_events([run_created_event(), invocation_started_event(run_id="run-9")])


def test_reduce_rejects_attempt_started_without_durable_input_binding():
    """Spec 5.5: ATTEMPT_STARTED requires a prior INPUT_BOUND fact."""
    events = (
        run_created_event(),
        invocation_started_event(),
        attempt_created_event(),
        attempt_started_event(),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_transitions_from_wrong_attempt_status():
    pending_fail = cycle_events()[:3] + (
        evt(
            EventType.ATTEMPT_FAILED,
            "evt-af-1",
            invocation_id="inv-1",
            step_id="R1",
            attempt_id="att-1",
            payload={"disposition": "EXECUTION_ERROR"},
        ),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(pending_fail)
    double_success = cycle_events() + (
        attempt_succeeded_event(event_id="evt-att-ok-2"),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(double_success)


def test_reduce_rejects_unknown_attempt_lineage():
    events = (
        run_created_event(),
        invocation_started_event(),
        artifact_committed_event(),
    )  # art-1 claims attempt att-1 which was never created
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_input_bound_for_unknown_attempt():
    events = (
        run_created_event(),
        invocation_started_event(),
        attempt_created_event(attempt_id="att-other"),
        input_bound_event(),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_binding_to_uncommitted_artifact():
    """Inputs are exact committed Artifact IDs: no residue may be bound."""
    events = cycle_events()[:4] + (
        input_bound_event(
            event_id="evt-ib-bad",
            payload={
                "input_binding_id": "ib-2",
                "artifact_ids": ["ghost-1"],
                "upstream_attempt_ids": [],
            },
        ),
        attempt_started_event(),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_duplicate_attempt_and_duplicate_binding():
    events = cycle_events() + (
        attempt_created_event(event_id="evt-att-dup", attempt_id="att-1"),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)
    double_bind = cycle_events()[:4] + (
        input_bound_event(
            event_id="evt-ib-2",
            payload={
                "input_binding_id": "ib-2",
                "artifact_ids": [],
                "upstream_attempt_ids": [],
            },
        ),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(double_bind)


def test_reduce_rejects_artifact_committed_without_digest():
    events = cycle_events()[:5] + (artifact_committed_event(payload={}),)
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_duplicate_gate_decisions():
    events = cycle_events() + (
        gate_created_event(),
        gate_decided_event(),
        gate_decided_event(event_id="evt-gate-dec-2"),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_decided_gate_without_reviewer():
    events = cycle_events() + (
        gate_created_event(),
        gate_decided_event(payload={"decision": "APPROVED", "decided_at": TS}),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_unknown_invocation_completion_and_wrong_status():
    events = cycle_events() + (
        invocation_completed_event(invocation_id="inv-ghost"),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)
    bad_token = cycle_events() + (
        invocation_completed_event(payload={"status": "COMPLETED"}),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(bad_token)


def test_reduce_rejects_invocation_started_while_previous_active():
    events = (
        run_created_event(),
        invocation_started_event(),
        evt(
            EventType.INVOCATION_STARTED,
            "evt-inv-2",
            invocation_id="inv-2",
            payload={
                "requested_scope": ["R1"],
                "entry_mode": "RESUME",
                "execution_binding": {
                    "workflow_identity": "research-workflow",
                    "workflow_version": "v1",
                    "runtime_configuration_identity": "runtime-config-001",
                    "prompts": {},
                    "schemas": {},
                },
            },
        ),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_canonical_committed_without_pending():
    events = cycle_events() + (
        evt(
            EventType.CANONICAL_BINDING_COMMITTED,
            "evt-cb-com-1",
            artifact_id="art-1",
            payload={},
        ),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_checkpoint_for_unknown_artifact():
    events = cycle_events() + (
        evt(
            EventType.CHECKPOINT_CREATED,
            "evt-cp-1",
            step_id="R1",
            payload={
                "checkpoint_id": "cp-1",
                "artifact_ids": ["ghost-1"],
                "compatibility": {
                    "workflow_identity": "research-workflow",
                    "workflow_version": "v1",
                    "step_identity": "r1",
                    "step_version": "1",
                    "runtime_configuration_identity": "runtime-config-001",
                },
            },
        ),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


def test_reduce_rejects_gate_reviewing_uncommitted_artifact():
    events = cycle_events() + (
        gate_created_event(
            payload={
                "logical_gate_id": "H2",
                "review_target": {
                    "step_id": "R1",
                    "attempt_id": "att-1",
                    "artifact_ids": ["ghost-1"],
                },
            }
        ),
    )
    with pytest.raises(RuntimeContractError):
        reduce_events(events)


# ---------------------------------------------------------------------------
# run.json document codec
# ---------------------------------------------------------------------------


def test_projection_document_round_trip():
    events = cycle_events() + (
        gate_created_event(),
        gate_decided_event(),
        invocation_completed_event(),
    )
    projection = reduce_events(events)
    document = serialize_projection(projection, projection_version=7, updated_at=TS)
    assert document["runtime_schema_version"] == 1
    assert document["projection_version"] == 7
    assert document["updated_at"] == TS
    parsed, version, updated_at = parse_projection(document)
    assert parsed == projection
    assert version == 7
    assert updated_at == TS


def test_projection_document_is_json_serializable():
    projection = reduce_events(cycle_events())
    document = serialize_projection(projection, projection_version=1, updated_at=TS)
    text = json.dumps(document)
    reparsed = parse_projection(json.loads(text))
    assert reparsed[0] == projection


def test_projection_document_serializes_artifact_envelope():
    envelope = ArtifactEnvelope(
        artifact_id="art-1",
        run_id="run-1",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id="att-1",
        artifact_schema_id="evidence-set",
        artifact_schema_version="1",
        created_at=TS,
        digest=DIGEST_D,
        provenance=("provenance-1",),
        payload={"rows": [{"id": 1}, {"id": 2}]},
    )
    document = {
        "runtime_schema_version": 1,
        **{
            "artifact_id": envelope.artifact_id,
            "run_id": envelope.run_id,
            "invocation_id": envelope.invocation_id,
            "artifact_schema_id": envelope.artifact_schema_id,
            "artifact_schema_version": envelope.artifact_schema_version,
            "created_at": envelope.created_at,
            "step_id": envelope.step_id,
            "attempt_id": envelope.attempt_id,
            "digest": envelope.digest,
            "provenance": list(envelope.provenance),
            "payload": envelope.payload,
        },
    }
    text = json.dumps(document)
    assert json.loads(text)["runtime_schema_version"] == 1


def test_parse_projection_rejects_unknown_runtime_schema_version():
    document = serialize_projection(
        reduce_events([run_created_event()]), projection_version=1, updated_at=TS
    )
    document["runtime_schema_version"] = 2
    with pytest.raises(ProjectionSchemaError):
        parse_projection(document)
    document["runtime_schema_version"] = "1"
    with pytest.raises(ProjectionSchemaError):
        parse_projection(document)


def test_parse_projection_rejects_unknown_state_token():
    projection = reduce_events([run_created_event()])
    document = serialize_projection(projection, projection_version=1, updated_at=TS)
    document["run"]["state"] = "BOGUS"
    with pytest.raises(ProjectionSchemaError):
        parse_projection(document)


def test_parse_projection_rejects_unknown_top_level_keys():
    projection = reduce_events([run_created_event()])
    document = serialize_projection(projection, projection_version=1, updated_at=TS)
    document["surprise"] = True
    with pytest.raises(ProjectionSchemaError):
        parse_projection(document)


def test_parse_projection_rejects_malformed_json_types():
    document = serialize_projection(
        reduce_events([run_created_event()]), projection_version=1, updated_at=TS
    )
    document["run"] = "not a record"
    with pytest.raises(ProjectionSchemaError):
        parse_projection(document)


def test_run_projection_freeze_and_fields():
    projection = reduce_events(cycle_events())
    assert isinstance(projection, RunProjection)
    assert projection.runtime_schema_version == 1
