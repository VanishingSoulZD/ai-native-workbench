"""Checkpoint persistence, exact validation and downstream invalidation
(Spec 12, Task 3).

A Checkpoint is a durable input-context set for a later Step boundary: it
records only committed Artifact ids plus the exact ``CompatibilityIdentity``
the boundary was produced under. It never serializes process state (Spec 12)
— reuse is always a fresh execution of the Step against the recorded inputs.

- ``create_checkpoint`` persists the CHECKPOINT_CREATED fact. The event
  carries the checkpoint id, its committed artifact ids and the compatibility
  mapping (optional prompt/schema pairs appear only when applicable, per the
  both-or-neither contract). The event timestamp is the checkpoint's own
  ``created_at``, so the reduced record equals the record the caller
  persisted and can later be validated verbatim.
- ``validate_checkpoint`` requires the exact recorded checkpoint (never a
  forged or stale copy) to be VALID and the *expected* CompatibilityIdentity
  to match it exactly on every dimension (Spec 16.3), then re-checks the
  durable evidence of every recorded artifact — a missing document or a
  digest that no longer matches its ARTIFACT_COMMITTED event fails as
  EvidenceIntegrityError, never silent repair.
- ``invalidate_downstream`` records the historical invalidation of every
  VALID checkpoint that a rerun of *step_id* made stale: all steps that
  transitively depend on it (``depends_on`` edges, excluding *step_id*
  itself). Invalidation is append-only CHECKPOINT_INVALIDATED events; prior
  records are never deleted or rewritten, and already INVALIDATED checkpoints
  are left untouched. Returns the invalidated step ids in checkpoint
  creation order, each once.

Signature note: the Task 3 brief lists ``invalidate_downstream(store,
run_id, step_id)``, but the transitive closure over a workflow's dependency
edges requires the workflow graph. The *workflow* parameter is therefore a
keyword-only ``WorkflowDefinition`` extension of the brief's signature
(recorded deviation; positional calls fail fast with TypeError).
"""

import uuid

from ..workflow.composition import WorkflowDefinition
from .artifacts import committed_in_run
from .binding import assert_compatible
from .domain import (
    CheckpointRecord,
    CheckpointStatus,
    CompatibilityIdentity,
    EventEnvelope,
    EventType,
    RuntimeContractError,
    utc_now,
)
from .store import RuntimeStore, reduce_events


def create_checkpoint(store: RuntimeStore, checkpoint: CheckpointRecord) -> CheckpointRecord:
    """Durably record the CHECKPOINT_CREATED fact for *checkpoint*.

    All recorded artifact ids must already be committed to the checkpoint's
    own run (Ruling 4) and the checkpoint id must be unused. Returns the
    recorded checkpoint unchanged.
    """
    if not isinstance(checkpoint, CheckpointRecord):
        raise RuntimeContractError(
            f"create_checkpoint requires a CheckpointRecord (got {checkpoint!r})."
        )
    projection = reduce_events(store.events(checkpoint.run_id))
    if checkpoint.checkpoint_id in projection.checkpoints:
        raise RuntimeContractError(
            f"duplicate CHECKPOINT_CREATED for checkpoint "
            f"{checkpoint.checkpoint_id!r}; checkpoints are created once."
        )
    for artifact_id in checkpoint.artifact_ids:
        committed_in_run(store, artifact_id, checkpoint.run_id)
    store.append_event(
        EventEnvelope(
            event_id=f"evt-{uuid.uuid4().hex}",
            event_type=EventType.CHECKPOINT_CREATED,
            timestamp=checkpoint.created_at,
            run_id=checkpoint.run_id,
            step_id=checkpoint.step_id,
            payload={
                "checkpoint_id": checkpoint.checkpoint_id,
                "artifact_ids": list(checkpoint.artifact_ids),
                "compatibility": _compatibility_payload(checkpoint.compatibility),
            },
        )
    )
    return checkpoint


def validate_checkpoint(
    store: RuntimeStore,
    checkpoint: CheckpointRecord,
    expected: CompatibilityIdentity,
) -> None:
    """Validate *checkpoint* for exact reuse against *expected* (Spec 12).

    The recorded checkpoint must exist and equal *checkpoint* (stale or
    forged copies never validate), must still be VALID, and its recorded
    CompatibilityIdentity must match *expected* exactly on every dimension.
    Every recorded artifact's durable evidence is then re-checked: missing
    documents and digest tampering raise EvidenceIntegrityError.
    """
    if not isinstance(checkpoint, CheckpointRecord) or not isinstance(
        expected, CompatibilityIdentity
    ):
        raise RuntimeContractError(
            "validate_checkpoint requires a CheckpointRecord and a "
            f"CompatibilityIdentity (got {checkpoint!r}, {expected!r})."
        )
    projection = reduce_events(store.events(checkpoint.run_id))
    recorded = projection.checkpoints.get(checkpoint.checkpoint_id)
    if recorded is None:
        raise RuntimeContractError(
            f"checkpoint {checkpoint.checkpoint_id!r} was never durably "
            "recorded in this run."
        )
    if recorded != checkpoint:
        raise RuntimeContractError(
            f"checkpoint {checkpoint.checkpoint_id} does not match the "
            "durably recorded checkpoint; stale or forged records never "
            "validate."
        )
    if recorded.status is not CheckpointStatus.VALID:
        raise RuntimeContractError(
            f"checkpoint {checkpoint.checkpoint_id} is "
            f"{recorded.status.value}; only VALID checkpoints are reusable."
        )
    assert_compatible(expected, recorded.compatibility)
    for artifact_id in recorded.artifact_ids:
        committed_in_run(store, artifact_id, recorded.run_id)
    return None


def invalidate_downstream(
    store: RuntimeStore, run_id: str, step_id: str, *, workflow: WorkflowDefinition
) -> tuple[str, ...]:
    """Invalidate every VALID checkpoint made stale by a rerun of *step_id*.

    A checkpoint is stale when its Step transitively depends on *step_id*
    (WorkflowNode.depends_on edges, excluding *step_id* itself). Appends one
    CHECKPOINT_INVALIDATED event per stale VALID checkpoint — in checkpoint
    creation order — and returns the invalidated step ids in that order,
    each once. A second pass is a no-op; runs without stale checkpoints are
    untouched.
    """
    if not isinstance(workflow, WorkflowDefinition):
        raise RuntimeContractError(
            "invalidate_downstream requires the workflow the step belongs "
            f"to as a keyword-only WorkflowDefinition (got {workflow!r})."
        )
    projection = reduce_events(store.events(run_id))
    step_ids = {node.step.id for node in workflow.steps}
    if step_id not in step_ids:
        raise RuntimeContractError(
            f"step {step_id!r} is not part of workflow {workflow.id!r}."
        )
    downstream = _downstream_steps(workflow, step_id)
    targets = [
        checkpoint
        for checkpoint in projection.checkpoints.values()
        if checkpoint.step_id in downstream
        and checkpoint.status is CheckpointStatus.VALID
    ]
    for checkpoint in targets:
        store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.CHECKPOINT_INVALIDATED,
                timestamp=utc_now(),
                run_id=run_id,
                step_id=checkpoint.step_id,
                payload={"checkpoint_id": checkpoint.checkpoint_id},
            )
        )
    return tuple(dict.fromkeys(checkpoint.step_id for checkpoint in targets))


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _compatibility_payload(identity: CompatibilityIdentity) -> dict:
    """Serialize the identity for a CHECKPOINT_CREATED payload.

    Optional prompt/schema pairs appear only when applicable (both fields of
    a pair are set together or neither appears in the payload).
    """
    payload = {
        "workflow_identity": identity.workflow_identity,
        "workflow_version": identity.workflow_version,
        "step_identity": identity.step_identity,
        "step_version": identity.step_version,
        "runtime_configuration_identity": identity.runtime_configuration_identity,
    }
    if identity.prompt_identity is not None:
        payload["prompt_identity"] = identity.prompt_identity
        payload["prompt_version"] = identity.prompt_version
    if identity.schema_identity is not None:
        payload["schema_identity"] = identity.schema_identity
        payload["schema_version"] = identity.schema_version
    return payload


def _downstream_steps(workflow: WorkflowDefinition, step_id: str) -> set:
    """Transitive dependents of *step_id* over the depends_on edges."""
    dependents: dict[str, list[str]] = {node.step.id: [] for node in workflow.steps}
    for node in workflow.steps:
        for dependency in node.depends_on:
            if dependency in dependents:
                dependents[dependency].append(node.step.id)
    downstream: set = set()
    frontier = list(dependents.get(step_id, ()))
    while frontier:
        current = frontier.pop()
        if current in downstream:
            continue
        downstream.add(current)
        frontier.extend(dependents.get(current, ()))
    return downstream
