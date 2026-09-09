"""Tests for the runtime domain records and their transition guards.

Covers the Task 1 invariants: Run/Invocation/Attempt lifecycle guards,
immutable bindings and scopes, Artifact lineage, explicit Input Binding,
Gate decision/revision/supersession semantics, and Checkpoint compatibility
identity.
"""

from dataclasses import FrozenInstanceError, replace
from datetime import datetime

import pytest

from ai_native_workbench.research.runtime import (
    ArtifactEnvelope,
    AttemptRecord,
    AttemptStatus,
    CaseBinding,
    CheckpointRecord,
    CheckpointStatus,
    CompatibilityIdentity,
    EntryMode,
    ExecutionBinding,
    GateDecision,
    GateRecord,
    InputBinding,
    InvocationRecord,
    InvocationStatus,
    RevisionTarget,
    ReviewTarget,
    RunRecord,
    RunState,
    RuntimeContractError,
    SNAPSHOT_MARKER,
    utc_now,
)

TS = "2026-09-09T00:00:00+00:00"
FULL_SCOPE = ("R1", "R2", "R3", "R4", "R5", SNAPSHOT_MARKER)


def make_case_binding(**overrides) -> CaseBinding:
    return replace(
        CaseBinding(
            case_id="case-1",
            charter_identity="charter-001",
            charter_digest="sha256:" + "a" * 64,
            source_declaration_identity="urls-001",
            source_declaration_digest="sha256:" + "b" * 64,
        ),
        **overrides,
    )


def make_execution_binding(**overrides) -> ExecutionBinding:
    return replace(
        ExecutionBinding(
            workflow_identity="research-workflow",
            workflow_version="v1",
            prompts={"prompt-acquire": "sha256:" + "c" * 64},
            schemas={"evidence-schema": "1"},
            runtime_configuration_identity="runtime-config-001",
        ),
        **overrides,
    )


def make_created_run(**overrides) -> RunRecord:
    return replace(
        RunRecord(
            run_id="run-1",
            case_id="case-1",
            case_binding=make_case_binding(),
            state=RunState.CREATED,
            cumulative_execution_scope=(),
            current_invocation_id=None,
            completion_reason=None,
        ),
        **overrides,
    )


def make_running_run() -> RunRecord:
    return make_created_run().start()


def make_invocation(**overrides) -> InvocationRecord:
    return replace(
        InvocationRecord(
            invocation_id="inv-1",
            run_id="run-1",
            requested_scope=FULL_SCOPE,
            entry_mode=EntryMode.START,
            execution_binding=make_execution_binding(),
            status=InvocationStatus.RUNNING,
            completion_reason=None,
        ),
        **overrides,
    )


def make_attempt(**overrides) -> AttemptRecord:
    return replace(
        AttemptRecord(
            attempt_id="att-1",
            run_id="run-1",
            invocation_id="inv-1",
            step_id="R1",
            status=AttemptStatus.PENDING,
            input_binding_id=None,
        ),
        **overrides,
    )


def make_artifact(**overrides) -> ArtifactEnvelope:
    return replace(
        ArtifactEnvelope(
            artifact_id="art-1",
            run_id="run-1",
            invocation_id="inv-1",
            step_id="R1",
            attempt_id="att-1",
            artifact_schema_id="evidence-set",
            artifact_schema_version="1",
            created_at=TS,
            digest=None,
        ),
        **overrides,
    )


def make_input_binding(**overrides) -> InputBinding:
    return replace(
        InputBinding(
            input_binding_id="ib-1",
            run_id="run-1",
            invocation_id="inv-1",
            step_id="R2",
            attempt_id="att-2",
            artifact_ids=("art-1",),
            upstream_attempt_ids=("att-1",),
        ),
        **overrides,
    )


def make_review_target(**overrides) -> ReviewTarget:
    return replace(
        ReviewTarget(
            step_id="R4",
            attempt_id="att-4",
            artifact_ids=("art-4a", "art-4b"),
        ),
        **overrides,
    )


def make_compatibility(**overrides) -> CompatibilityIdentity:
    return replace(
        CompatibilityIdentity(
            workflow_identity="research-workflow",
            workflow_version="v1",
            step_identity="R3",
            step_version="v1",
            runtime_configuration_identity="runtime-config-001",
        ),
        **overrides,
    )


def make_gate(**overrides) -> GateRecord:
    return replace(
        GateRecord(
            gate_id="gate-1",
            run_id="run-1",
            logical_gate_id="H3",
            review_target=make_review_target(),
            decision=GateDecision.PENDING,
            created_at=TS,
        ),
        **overrides,
    )


def make_checkpoint(**overrides) -> CheckpointRecord:
    return replace(
        CheckpointRecord(
            checkpoint_id="cp-1",
            run_id="run-1",
            step_id="R3",
            artifact_ids=("art-2a", "art-2b"),
            compatibility=make_compatibility(),
            created_at=TS,
        ),
        **overrides,
    )


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


def test_completed_bounded_run_records_scope():
    # Direct CREATED -> COMPLETED is rejected, so the run must have started.
    run = make_created_run().start()
    completed = run.complete(
        completion_reason="BOUNDED_SCOPE",
        execution_scope=FULL_SCOPE,
    )
    assert completed.state is RunState.COMPLETED
    assert completed.completion_reason == "BOUNDED_SCOPE"
    assert completed.cumulative_execution_scope == FULL_SCOPE


def test_run_cannot_complete_directly_from_created():
    run = make_created_run()
    with pytest.raises(RuntimeContractError):
        run.complete(
            completion_reason="BOUNDED_SCOPE",
            execution_scope=FULL_SCOPE,
        )


def test_completed_run_resumes_only_through_explicit_resume_operation():
    completed = make_running_run().complete(
        completion_reason="BOUNDED_SCOPE", execution_scope=FULL_SCOPE
    )
    resumed = completed.begin_resume()
    assert resumed.state is RunState.RUNNING
    assert resumed.completion_reason is None
    # Cumulative scope is durable history: never erased by resume.
    assert resumed.cumulative_execution_scope == FULL_SCOPE


def test_created_run_cannot_resume():
    with pytest.raises(RuntimeContractError):
        make_created_run().begin_resume()


def test_run_start_requires_created_state():
    running = make_created_run().start()
    assert running.state is RunState.RUNNING
    with pytest.raises(RuntimeContractError):
        running.start()
    with pytest.raises(RuntimeContractError):
        make_created_run().complete(
            completion_reason="BOUNDED_SCOPE", execution_scope=FULL_SCOPE
        ).start()


def test_run_waiting_for_human_is_reversible():
    waiting = make_running_run().wait_for_human()
    assert waiting.state is RunState.WAITING_FOR_HUMAN
    resumed = waiting.mark_running()
    assert resumed.state is RunState.RUNNING
    with pytest.raises(RuntimeContractError):
        make_created_run().mark_running()
    with pytest.raises(RuntimeContractError):
        make_running_run().begin_resume()


def test_run_needs_revision_from_running_then_explicit_resume():
    revision = make_running_run().needs_revision()
    assert revision.state is RunState.NEEDS_REVISION
    resumed = revision.begin_resume()
    assert resumed.state is RunState.RUNNING
    with pytest.raises(RuntimeContractError):
        make_created_run().needs_revision()


def test_run_fail_requires_disposition_and_recovery_is_explicit():
    failed = make_running_run().fail(completion_reason="EXECUTION_INTERRUPTED")
    assert failed.state is RunState.FAILED
    assert failed.completion_reason == "EXECUTION_INTERRUPTED"
    with pytest.raises(RuntimeContractError):
        make_running_run().fail(completion_reason="")
    with pytest.raises(RuntimeContractError):
        make_created_run().fail(completion_reason="EXECUTION_INTERRUPTED")
    recovered = failed.begin_resume()
    assert recovered.state is RunState.RUNNING


def test_cumulative_execution_scope_accumulates_across_resume():
    run = make_running_run()
    completed = run.complete(
        completion_reason="BOUNDED_SCOPE", execution_scope=FULL_SCOPE
    )
    resumed = completed.begin_resume()
    extended = resumed.complete(
        completion_reason="BOUNDED_SCOPE",
        execution_scope=("R6", "R7", "R8"),
    )
    assert extended.cumulative_execution_scope == FULL_SCOPE + ("R6", "R7", "R8")


def test_run_completion_scope_is_validated():
    running = make_running_run()
    with pytest.raises(RuntimeContractError):
        running.complete(completion_reason="BOUNDED_SCOPE", execution_scope=())
    with pytest.raises(RuntimeContractError):
        running.complete(
            completion_reason="BOUNDED_SCOPE",
            execution_scope=("R1", "R1"),
        )
    with pytest.raises(RuntimeContractError):
        running.complete(completion_reason="BOUNDED_SCOPE", execution_scope=("",))


def test_run_state_enum_holds_exactly_six_states():
    assert {member.name for member in RunState} == {
        "CREATED",
        "RUNNING",
        "WAITING_FOR_HUMAN",
        "NEEDS_REVISION",
        "FAILED",
        "COMPLETED",
    }


def test_run_record_rejects_empty_ids_and_unknown_schema_version():
    with pytest.raises(RuntimeContractError):
        make_created_run(run_id="")
    with pytest.raises(RuntimeContractError):
        make_created_run(case_id="")
    with pytest.raises(RuntimeContractError):
        make_created_run(runtime_schema_version=2)
    with pytest.raises(RuntimeContractError):
        make_created_run(runtime_schema_version="1")
    with pytest.raises(RuntimeContractError):
        make_created_run(runtime_schema_version=True)


def test_run_record_is_frozen():
    run = make_created_run()
    with pytest.raises(FrozenInstanceError):
        run.state = RunState.RUNNING


def test_snapshot_scope_marker_is_literal_string():
    assert SNAPSHOT_MARKER == "SNAPSHOT"


def test_utc_now_returns_iso_8601_utc_string():
    parsed = datetime.fromisoformat(utc_now())
    assert parsed.tzinfo is not None


# ---------------------------------------------------------------------------
# Invocation
# ---------------------------------------------------------------------------


def test_invocation_scope_and_execution_binding_are_immutable():
    invocation = make_invocation()
    assert invocation.requested_scope == FULL_SCOPE
    assert invocation.execution_binding == make_execution_binding()
    with pytest.raises(FrozenInstanceError):
        invocation.requested_scope = ("R2",)
    with pytest.raises(FrozenInstanceError):
        invocation.execution_binding = make_execution_binding(
            runtime_configuration_identity="other"
        )
    with pytest.raises(TypeError):
        invocation.execution_binding.prompts["prompt-other"] = "x"


def test_invocation_fail_requires_disposition_and_succeed_requires_running():
    failed = make_invocation().fail(completion_reason="HUMAN_REJECTION")
    assert failed.status is InvocationStatus.FAILED
    assert failed.completion_reason == "HUMAN_REJECTION"
    with pytest.raises(RuntimeContractError):
        make_invocation().fail(completion_reason="")
    succeeded = make_invocation().succeed()
    assert succeeded.status is InvocationStatus.SUCCEEDED
    with pytest.raises(RuntimeContractError):
        succeeded.succeed()
    with pytest.raises(RuntimeContractError):
        succeeded.fail(completion_reason="HUMAN_REJECTION")


def test_invocation_status_enum_holds_exactly_three_statuses():
    assert {member.name for member in InvocationStatus} == {
        "RUNNING",
        "FAILED",
        "SUCCEEDED",
    }


def test_invocation_rejects_invalid_entry_mode_and_empty_scope():
    with pytest.raises(RuntimeContractError):
        make_invocation(entry_mode="INVALID")
    with pytest.raises(RuntimeContractError):
        make_invocation(requested_scope=())
    with pytest.raises(RuntimeContractError):
        make_invocation(requested_scope=("R1", "R1"))


def test_invocation_record_is_frozen():
    invocation = make_invocation()
    with pytest.raises(FrozenInstanceError):
        invocation.status = InvocationStatus.SUCCEEDED


# ---------------------------------------------------------------------------
# Attempt
# ---------------------------------------------------------------------------


def test_attempt_cannot_become_running_without_durable_input_binding():
    attempt = make_attempt()
    with pytest.raises(RuntimeContractError):
        attempt.mark_running()


def test_attempt_mark_running_requires_pending_or_failed():
    running = make_attempt().mark_running(input_binding_id="ib-1")
    assert running.status is AttemptStatus.RUNNING
    assert running.input_binding_id == "ib-1"
    with pytest.raises(RuntimeContractError):
        running.mark_running(input_binding_id="ib-1")


def test_failed_attempt_can_retry_with_explicit_binding():
    failed = make_attempt().mark_running(input_binding_id="ib-1").mark_failed()
    assert failed.status is AttemptStatus.FAILED
    retried = failed.mark_running(input_binding_id="ib-2")
    assert retried.status is AttemptStatus.RUNNING
    assert retried.input_binding_id == "ib-2"


def test_attempt_succeeds_only_from_running():
    with pytest.raises(RuntimeContractError):
        make_attempt().mark_succeeded()
    succeeded = make_attempt().mark_running(input_binding_id="ib-1").mark_succeeded()
    assert succeeded.status is AttemptStatus.SUCCEEDED
    with pytest.raises(RuntimeContractError):
        succeeded.mark_running(input_binding_id="ib-1")


def test_attempt_fail_requires_running_state():
    failed = make_attempt().mark_running(input_binding_id="ib-1").mark_failed()
    assert failed.status is AttemptStatus.FAILED
    # The attempt record keeps only execution state: the failure disposition
    # is carried by the ATTEMPT_FAILED event payload, not by the record.
    assert not hasattr(failed, "completion_reason")
    with pytest.raises(RuntimeContractError):
        make_attempt().mark_failed()


def test_attempt_status_enum_has_no_validation_or_acceptance_states():
    assert {member.name for member in AttemptStatus} == {
        "PENDING",
        "RUNNING",
        "FAILED",
        "SUCCEEDED",
    }


def test_attempt_record_is_frozen_and_schema_version_validated():
    attempt = make_attempt()
    with pytest.raises(FrozenInstanceError):
        attempt.status = AttemptStatus.RUNNING
    with pytest.raises(RuntimeContractError):
        make_attempt(runtime_schema_version=0)


# ---------------------------------------------------------------------------
# Artifact envelope and Input Binding
# ---------------------------------------------------------------------------


def test_artifact_lineage_is_explicit():
    artifact = make_artifact()
    assert artifact.run_id == "run-1"
    assert artifact.invocation_id == "inv-1"
    assert artifact.attempt_id == "att-1"
    assert artifact.step_id == "R1"
    assert artifact.artifact_id == "art-1"


def test_artifact_requires_run_and_invocation():
    with pytest.raises(RuntimeContractError):
        make_artifact(run_id="")
    with pytest.raises(RuntimeContractError):
        make_artifact(invocation_id="")


def test_artifact_step_and_attempt_are_paired():
    # Source-acquisition artifacts bind to an invocation without an attempt.
    source_artifact = make_artifact(step_id=None, attempt_id=None)
    assert source_artifact.step_id is None
    assert source_artifact.attempt_id is None
    with pytest.raises(RuntimeContractError):
        make_artifact(step_id="R1", attempt_id=None)
    with pytest.raises(RuntimeContractError):
        make_artifact(step_id=None, attempt_id="att-1")


def test_artifact_digest_is_completed_once_at_commit():
    artifact = make_artifact()
    assert artifact.digest is None
    committed = artifact.with_digest("sha256:" + "d" * 64)
    assert committed.digest == "sha256:" + "d" * 64
    with pytest.raises(RuntimeContractError):
        committed.with_digest("sha256:" + "e" * 64)
    with pytest.raises(RuntimeContractError):
        artifact.with_digest("")


def test_artifact_schema_pair_is_required():
    with pytest.raises(RuntimeContractError):
        make_artifact(artifact_schema_id="")
    with pytest.raises(RuntimeContractError):
        make_artifact(artifact_schema_version="")


def test_input_binding_records_concrete_artifacts_and_upstream_lineage():
    binding = make_input_binding()
    assert binding.input_binding_id == "ib-1"
    assert binding.run_id == "run-1"
    assert binding.invocation_id == "inv-1"
    assert binding.step_id == "R2"
    assert binding.attempt_id == "att-2"
    assert binding.artifact_ids == ("art-1",)
    assert binding.upstream_attempt_ids == ("att-1",)


def test_input_binding_rejects_duplicate_artifact_ids():
    with pytest.raises(RuntimeContractError):
        make_input_binding(artifact_ids=("art-1", "art-1"))
    with pytest.raises(RuntimeContractError):
        make_input_binding(upstream_attempt_ids=("att-1", "att-1"))
    with pytest.raises(RuntimeContractError):
        make_input_binding(artifact_ids=("",))


def test_input_binding_is_frozen():
    binding = make_input_binding()
    with pytest.raises(FrozenInstanceError):
        binding.artifact_ids = ("art-2",)


# ---------------------------------------------------------------------------
# Case and Execution bindings, Compatibility identity
# ---------------------------------------------------------------------------


def test_case_binding_freezes_case_definition_inputs():
    binding = make_case_binding()
    assert binding.case_id == "case-1"
    assert binding.charter_identity == "charter-001"
    assert binding.charter_digest.startswith("sha256:")
    assert binding.source_declaration_identity == "urls-001"
    assert binding.source_declaration_digest.startswith("sha256:")
    with pytest.raises(RuntimeContractError):
        make_case_binding(charter_identity="")
    with pytest.raises(RuntimeContractError):
        make_case_binding(source_declaration_digest="")
    with pytest.raises(FrozenInstanceError):
        binding.case_id = "case-2"


def test_execution_binding_freezes_invocation_configuration_identities():
    binding = make_execution_binding()
    assert binding.workflow_identity == "research-workflow"
    assert binding.workflow_version == "v1"
    assert binding.prompts == {"prompt-acquire": "sha256:" + "c" * 64}
    assert binding.schemas == {"evidence-schema": "1"}
    assert binding.runtime_configuration_identity == "runtime-config-001"
    with pytest.raises(RuntimeContractError):
        make_execution_binding(workflow_version="")
    with pytest.raises(RuntimeContractError):
        make_execution_binding(runtime_configuration_identity="")


def test_compatibility_identity_is_the_exact_match_tuple():
    identity = make_compatibility()
    assert identity.workflow_identity == "research-workflow"
    assert identity.workflow_version == "v1"
    assert identity.step_identity == "R3"
    assert identity.step_version == "v1"
    assert identity.runtime_configuration_identity == "runtime-config-001"
    # Prompt and schema identities are optional but must appear as full pairs.
    with pytest.raises(RuntimeContractError):
        make_compatibility(prompt_version="1")
    with pytest.raises(RuntimeContractError):
        make_compatibility(schema_version="1")
    assert make_compatibility(
        prompt_identity="prompt-r3", prompt_version="1"
    ).prompt_identity == "prompt-r3"
    with pytest.raises(RuntimeContractError):
        make_compatibility(workflow_identity="")


# ---------------------------------------------------------------------------
# Human Gate
# ---------------------------------------------------------------------------


def test_gate_decision_enum_holds_only_pending_approved_rejected():
    assert {member.name for member in GateDecision} == {
        "PENDING",
        "APPROVED",
        "REJECTED",
    }


def test_pending_gate_carries_no_decision_metadata():
    gate = make_gate()
    assert gate.decision is GateDecision.PENDING
    assert gate.reviewer is None
    assert gate.decided_at is None
    with pytest.raises(RuntimeContractError):
        make_gate(reviewer="reviewer-1")
    with pytest.raises(RuntimeContractError):
        make_gate(decided_at=TS)


def test_decided_gate_requires_reviewer_and_decided_at():
    with pytest.raises(RuntimeContractError):
        make_gate(
            decision=GateDecision.APPROVED, reviewer="reviewer-1", decided_at=None
        )
    with pytest.raises(RuntimeContractError):
        make_gate(
            decision=GateDecision.REJECTED,
            reviewer=None,
            decided_at=TS,
            revision_target=RevisionTarget(entry_step="R3", reason="rewrite"),
        )
    decided = make_gate().decide(
        decision=GateDecision.APPROVED,
        reviewer="reviewer-1",
        decided_at=TS,
        comment="looks good",
    )
    assert decided.decision is GateDecision.APPROVED
    assert decided.reviewer == "reviewer-1"
    assert decided.decided_at == TS
    assert decided.comment == "looks good"


def test_gate_cannot_be_decided_twice():
    decided = make_gate().decide(
        decision=GateDecision.REJECTED,
        reviewer="reviewer-1",
        decided_at=TS,
        revision_target=RevisionTarget(entry_step="R3", reason="weak analysis"),
    )
    with pytest.raises(RuntimeContractError):
        decided.decide(
            decision=GateDecision.APPROVED, reviewer="reviewer-2", decided_at=TS
        )
    with pytest.raises(RuntimeContractError):
        make_gate().decide(
            decision=GateDecision.PENDING, reviewer="reviewer-1", decided_at=TS
        )


def test_revision_target_requires_entry_step_and_reason():
    with pytest.raises(RuntimeContractError):
        RevisionTarget(entry_step="", reason="rewrite")
    with pytest.raises(RuntimeContractError):
        RevisionTarget(entry_step="R3", reason="")
    revision = RevisionTarget(entry_step="R3", reason="rewrite analysis")
    assert revision.entry_step == "R3"
    assert revision.reason == "rewrite analysis"


def test_revision_target_only_appears_on_rejected_gate():
    with pytest.raises(RuntimeContractError):
        make_gate(
            decision=GateDecision.APPROVED,
            reviewer="reviewer-1",
            decided_at=TS,
            revision_target=RevisionTarget(entry_step="R3", reason="rewrite"),
        )
    rejected = make_gate().decide(
        decision=GateDecision.REJECTED,
        reviewer="reviewer-1",
        decided_at=TS,
        revision_target=RevisionTarget(entry_step="R3", reason="weak analysis"),
    )
    assert rejected.revision_target == RevisionTarget(entry_step="R3", reason="weak analysis")


def test_review_target_binds_concrete_candidate_set():
    target = make_review_target()
    assert target.step_id == "R4"
    assert target.attempt_id == "att-4"
    assert target.artifact_ids == ("art-4a", "art-4b")
    with pytest.raises(RuntimeContractError):
        make_review_target(artifact_ids=())


def test_gate_supersession_is_a_single_immutable_relationship():
    superseded = make_gate().mark_superseded_by("gate-2")
    assert superseded.superseded_by == "gate-2"
    with pytest.raises(RuntimeContractError):
        superseded.mark_superseded_by("gate-3")
    with pytest.raises(RuntimeContractError):
        make_gate().mark_superseded_by("gate-1")
    with pytest.raises(RuntimeContractError):
        make_gate(gate_id="gate-1", supersedes="gate-1")
    with pytest.raises(RuntimeContractError):
        make_gate(gate_id="gate-1", superseded_by="gate-1")


def test_gate_record_is_frozen():
    gate = make_gate()
    with pytest.raises(FrozenInstanceError):
        gate.decision = GateDecision.APPROVED


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------


def test_checkpoint_carries_compatibility_identity_and_artifact_references():
    checkpoint = make_checkpoint()
    assert checkpoint.checkpoint_id == "cp-1"
    assert checkpoint.run_id == "run-1"
    assert checkpoint.step_id == "R3"
    assert checkpoint.artifact_ids == ("art-2a", "art-2b")
    assert checkpoint.compatibility == make_compatibility()
    assert checkpoint.status is CheckpointStatus.VALID


def test_checkpoint_status_enum_has_two_values():
    assert {member.name for member in CheckpointStatus} == {"VALID", "INVALIDATED"}


def test_checkpoint_invalidates_once():
    invalidated = make_checkpoint().invalidate()
    assert invalidated.status is CheckpointStatus.INVALIDATED
    with pytest.raises(RuntimeContractError):
        invalidated.invalidate()


def test_checkpoint_requires_artifacts_and_input_boundary_step():
    with pytest.raises(RuntimeContractError):
        make_checkpoint(artifact_ids=())
    with pytest.raises(RuntimeContractError):
        make_checkpoint(step_id="")
    with pytest.raises(RuntimeContractError):
        make_checkpoint(run_id="")
    with pytest.raises(FrozenInstanceError):
        make_checkpoint().status = CheckpointStatus.INVALIDATED
