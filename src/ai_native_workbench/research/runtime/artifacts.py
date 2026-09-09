"""Artifact commit protocol and durable Input Bindings (Spec 5.5/9.4/11.2).

``commit_artifact`` performs the brief Step 5 protocol in order::

    payload / envelope
    -> digest + metadata   (canonical-JSON sha256 digest, digest completed
                            exactly once via ArtifactEnvelope.with_digest)
    -> committed evidence  (artifact document persisted with the digest)
    -> ARTIFACT_COMMITTED event (the durable fact; execution.jsonl is
                            authoritative, Ruling 4)

The document write is residue-safe (a pre-commit document may be
overwritten), so a crash between the document write and the event append
leaves only residue: the store's committed-artifact read path never sees it
and a retry of the same commit heals the window without duplicating evidence.
A commit whose ARTIFACT_COMMITTED event is already durable replays
idempotently and returns the recorded envelope; a different payload or a
different envelope under the same artifact id raises — artifacts commit
exactly once and are immutable after commit.

Ruling 14: an attempt round commits exactly one output artifact. The commit
path scans the history for ARTIFACT_COMMITTED events naming the attempt after
its last ATTEMPT_STARTED; retry rounds (ATTEMPT_FAILED -> ATTEMPT_STARTED of
the same attempt) open a fresh round and may commit again. Source-acquisition
artifacts (Spec 9: no Workflow Attempt) bind to the Invocation only.

``persist_input_binding`` durably records the Attempt's INPUT_BOUND fact
(Spec 5.5) *before* the attempt starts. Only artifacts already committed to
the binding's own run are eligible — committed-ness is derived from the
run's ARTIFACT_COMMITTED events, never from the presence of a document
(Ruling 4); residue and cross-run artifacts raise ArtifactNotCommittedError.
"""

import uuid
from dataclasses import replace

from .digests import payload_digest
from .domain import (
    ArtifactEnvelope,
    EventEnvelope,
    EventType,
    InputBinding,
    RuntimeContractError,
    utc_now,
)
from .store import RuntimeStore, reduce_events


class ArtifactNotCommittedError(Exception):
    """Raised when an artifact is not a committed artifact of the owning Run.

    Covers residue (a document with no ARTIFACT_COMMITTED event), unknown
    artifact ids and artifacts committed to a different Run. Committed-ness
    is event-derived (Ruling 4); nothing else may ever serve as a step input.
    """


def committed_in_run(store: RuntimeStore, artifact_id: str, run_id: str) -> ArtifactEnvelope:
    """Return the committed envelope of *artifact_id* owned by *run_id*.

    Raises ArtifactNotCommittedError when no ARTIFACT_COMMITTED fact for the
    artifact exists in the run's event history (residue or unknown id).
    Evidence integrity failures — a commit event whose document is missing
    or whose digest does not match — propagate as EvidenceIntegrityError:
    durable evidence is never silently repaired on this path.
    """
    commit = _commit_event_for(store.events(run_id), artifact_id)
    if commit is None:
        raise ArtifactNotCommittedError(
            f"artifact {artifact_id!r} is not a committed artifact of run "
            f"{run_id!r}; only committed artifacts are eligible inputs "
            "(Ruling 4)."
        )
    envelope = store.load_artifact(artifact_id)
    if envelope.run_id != run_id:
        raise ArtifactNotCommittedError(
            f"artifact {artifact_id!r} is committed to run "
            f"{envelope.run_id!r}, not run {run_id!r}."
        )
    return envelope


def commit_artifact(
    store: RuntimeStore, artifact: ArtifactEnvelope, payload: object
) -> ArtifactEnvelope:
    """Commit *payload* as the durable artifact document of *artifact*.

    Returns the committed envelope (payload completed, digest completed).
    The commit is idempotent for the identical envelope/payload pair —
    including across a crash between the document write and the event append
    — and refuses any other reuse of the artifact id.

    Raises RuntimeContractError for non-envelopes, already-digested
    envelopes, non-JSON-able payloads, an unknown Run, contradictions with
    the reduced history (unknown or non-RUNNING invocation, unknown or
    non-RUNNING attempt, lineage mismatch) and Ruling-14 round violations;
    EventConflictError remains the store's authoritative backstop for any
    residual append-time contradiction.
    """
    if not isinstance(artifact, ArtifactEnvelope):
        raise RuntimeContractError(
            f"commit_artifact requires an ArtifactEnvelope (got {artifact!r})."
        )
    if artifact.digest is not None:
        raise RuntimeContractError(
            f"artifact {artifact.artifact_id} is already digested "
            f"({artifact.digest}); digests are completed exactly once at "
            "commit time."
        )
    try:
        digest = payload_digest(payload)
    except (TypeError, ValueError) as exc:
        raise RuntimeContractError(
            f"artifact {artifact.artifact_id} payload is not JSON "
            f"serializable: {exc}"
        ) from exc

    events = store.events(artifact.run_id)
    prior = _commit_event_for(events, artifact.artifact_id)
    if prior is not None:
        recorded = prior.payload.get("digest")
        if recorded != digest:
            raise RuntimeContractError(
                f"artifact {artifact.artifact_id} is already committed with "
                f"digest {recorded!r}; a different payload can never commit "
                "under the same artifact id."
            )
        committed = replace(artifact, payload=payload).with_digest(digest)
        loaded = store.load_artifact(artifact.artifact_id)
        if loaded != committed:
            raise RuntimeContractError(
                f"artifact {artifact.artifact_id} is already committed as a "
                "different envelope; artifact documents are immutable after "
                "their commit event."
            )
        return loaded

    projection = reduce_events(events)
    if artifact.step_id is None:
        _require_running_invocation(projection, artifact.invocation_id, artifact)
    else:
        _require_running_attempt(projection, artifact)
        _enforce_single_commit_per_round(events, artifact)

    committed = replace(artifact, payload=payload).with_digest(digest)
    store.save_artifact(committed)
    store.append_event(
        EventEnvelope(
            event_id=f"evt-{uuid.uuid4().hex}",
            event_type=EventType.ARTIFACT_COMMITTED,
            timestamp=utc_now(),
            run_id=artifact.run_id,
            invocation_id=artifact.invocation_id,
            step_id=artifact.step_id,
            attempt_id=artifact.attempt_id,
            artifact_id=artifact.artifact_id,
            payload={"digest": digest},
        )
    )
    return committed


def persist_input_binding(store: RuntimeStore, binding: InputBinding) -> None:
    """Durably record the INPUT_BOUND fact for *binding* (Spec 5.5).

    The attempt must exist, be PENDING (an input binding precedes the first
    start) and match the binding's lineage; the binding id must be unused;
    every artifact id must be committed to the binding's own run (Ruling 4);
    upstream attempt ids must be known. Replaying the identical binding is a
    no-op; a different binding for an already bound attempt raises.
    """
    if not isinstance(binding, InputBinding):
        raise RuntimeContractError(
            f"persist_input_binding requires an InputBinding (got {binding!r})."
        )
    projection = reduce_events(store.events(binding.run_id))
    for recorded in projection.input_bindings.values():
        if recorded.attempt_id == binding.attempt_id:
            if recorded == binding:
                return None
            raise RuntimeContractError(
                f"attempt {binding.attempt_id} is already durably bound as "
                f"{recorded.input_binding_id!r}; input bindings precede the "
                "first start and are never rewritten."
            )
    if binding.input_binding_id in projection.input_bindings:
        raise RuntimeContractError(
            f"input binding id {binding.input_binding_id!r} is already "
            "recorded in this run."
        )
    attempt = projection.attempts.get(binding.attempt_id)
    if attempt is None:
        raise RuntimeContractError(
            f"INPUT_BOUND references attempt {binding.attempt_id!r}, which "
            "was never created."
        )
    if attempt.status.value != "PENDING":
        raise RuntimeContractError(
            f"INPUT_BOUND: attempt {binding.attempt_id} is "
            f"{attempt.status.value}; input bindings precede the first start."
        )
    if (
        attempt.invocation_id != binding.invocation_id
        or attempt.step_id != binding.step_id
    ):
        raise RuntimeContractError(
            f"INPUT_BOUND lineage (invocation {binding.invocation_id}, step "
            f"{binding.step_id}) does not match attempt {binding.attempt_id}."
        )
    for artifact_id in binding.artifact_ids:
        committed_in_run(store, artifact_id, binding.run_id)
    for upstream_id in binding.upstream_attempt_ids:
        if upstream_id not in projection.attempts:
            raise RuntimeContractError(
                f"INPUT_BOUND names unknown upstream attempt {upstream_id!r}."
            )
    store.append_event(
        EventEnvelope(
            event_id=f"evt-{uuid.uuid4().hex}",
            event_type=EventType.INPUT_BOUND,
            timestamp=utc_now(),
            run_id=binding.run_id,
            invocation_id=binding.invocation_id,
            step_id=binding.step_id,
            attempt_id=binding.attempt_id,
            payload={
                "input_binding_id": binding.input_binding_id,
                "artifact_ids": list(binding.artifact_ids),
                "upstream_attempt_ids": list(binding.upstream_attempt_ids),
            },
        )
    )
    return None


# ---------------------------------------------------------------------------
# commit-path guards
# ---------------------------------------------------------------------------


def _commit_event_for(events, artifact_id: str):
    for event in events:
        if (
            event.event_type is EventType.ARTIFACT_COMMITTED
            and event.artifact_id == artifact_id
        ):
            return event
    return None


def _require_running_invocation(projection, invocation_id: str, artifact) -> None:
    invocation = projection.invocations.get(invocation_id)
    if invocation is None:
        raise RuntimeContractError(
            f"artifact {artifact.artifact_id} references invocation "
            f"{invocation_id!r}, which was never started in run "
            f"{artifact.run_id}."
        )
    if invocation.status.value != "RUNNING":
        raise RuntimeContractError(
            f"artifact {artifact.artifact_id}: invocation {invocation_id} is "
            f"{invocation.status.value}; only RUNNING invocations commit "
            "artifacts."
        )


def _require_running_attempt(projection, artifact) -> None:
    attempt = projection.attempts.get(artifact.attempt_id)
    if attempt is None:
        raise RuntimeContractError(
            f"artifact {artifact.artifact_id} references attempt "
            f"{artifact.attempt_id!r}, which was never created."
        )
    if (
        attempt.invocation_id != artifact.invocation_id
        or attempt.step_id != artifact.step_id
    ):
        raise RuntimeContractError(
            f"artifact {artifact.artifact_id} lineage does not match attempt "
            f"{artifact.attempt_id} (invocation {attempt.invocation_id}, "
            f"step {attempt.step_id})."
        )
    _require_running_invocation(projection, artifact.invocation_id, artifact)
    if attempt.status.value != "RUNNING":
        raise RuntimeContractError(
            f"artifact {artifact.artifact_id}: attempt {artifact.attempt_id} "
            f"is {attempt.status.value}; only RUNNING attempts commit "
            "artifacts."
        )


def _enforce_single_commit_per_round(events, artifact) -> None:
    """Ruling 14: scan commits after the attempt's last ATTEMPT_STARTED."""
    start_index = None
    for index, event in enumerate(events):
        if (
            event.event_type is EventType.ATTEMPT_STARTED
            and event.attempt_id == artifact.attempt_id
            and event.invocation_id == artifact.invocation_id
            and event.step_id == artifact.step_id
        ):
            start_index = index
    for index, event in enumerate(events):
        if (
            event.event_type is EventType.ARTIFACT_COMMITTED
            and event.attempt_id == artifact.attempt_id
            and event.invocation_id == artifact.invocation_id
            and event.step_id == artifact.step_id
            and (start_index is None or index > start_index)
        ):
            raise RuntimeContractError(
                f"attempt {artifact.attempt_id} round already committed "
                f"artifact {event.artifact_id}; an attempt round commits "
                "exactly one artifact (Ruling 14)."
            )
