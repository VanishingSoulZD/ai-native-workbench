"""Startup reconciliation of the three v1 execution crash windows (Spec 11.3).

After a process crash the store may be left in one of three recoverable
states, each detected from durable facts alone (never from speculation):

1. An Attempt is RUNNING with no committed Artifact after its last
   ATTEMPT_STARTED (stranded): a re-execution never durably produced
   evidence, so the missing terminal fact is appended as ATTEMPT_FAILED
   with disposition EXECUTION_INTERRUPTED (Ruling 12: the interruption
   stays at ATTEMPT level — Invocation and Run remain RUNNING).
2. A committed Artifact exists after the Attempt's last ATTEMPT_STARTED
   (durable evidence) but the success event is missing: ATTEMPT_SUCCEEDED
   is appended. Evidence for an Attempt is exactly the ARTIFACT_COMMITTED
   events naming that Attempt strictly after its last ATTEMPT_STARTED;
   source-acquisition commits (no attempt lineage) never count, so a
   retry round can never consume an earlier round's evidence.
3. run.json is stale or missing: it is rebuilt from events.

Order of operations: events (schema fail-fast) -> reduction -> durable
evidence verification (every committed Artifact document must exist and
digest-match, else EvidenceIntegrityError — evidence is never silently
dropped or re-executed) -> missing terminal facts appended in last-
ATTEMPT_STARTED order with fresh emitter-chosen event ids (Ruling 11) ->
final reduction -> projection document rebuilt. A second reconcile is an
idempotent no-op. Reconciliation dispatches by event/fact type so later
tasks extend the crash windows; this module never calls an Executor and
never appends ATTEMPT_STARTED/INVOCATION_STARTED.
"""

import uuid
from dataclasses import dataclass

from .domain import (
    AttemptRecord,
    AttemptStatus,
    EventEnvelope,
    EventType,
    utc_now,
)
from .store import (
    EvidenceIntegrityError,
    FileSystemRuntimeStore,
    RunProjection,
    reduce_events,
)

EXECUTION_INTERRUPTED = "EXECUTION_INTERRUPTED"
"""Disposition of the ATTEMPT_FAILED fact appended for a stranded Attempt
(Spec 11.3)."""


@dataclass(frozen=True)
class ReconciliationOutcome:
    """The result of one reconciliation pass over a Run."""

    projection: RunProjection
    appended_events: tuple[EventEnvelope, ...] = ()


def _stranded_attempts(
    events: tuple[EventEnvelope, ...], projection: RunProjection
) -> list[tuple[int, str]]:
    """Return (last ATTEMPT_STARTED index, attempt_id) per RUNNING Attempt.

    Ordered by the position of each Attempt's last ATTEMPT_STARTED so
    missing facts are appended in execution order.
    """
    last_start: dict[str, int] = {}
    for index, event in enumerate(events):
        if (
            event.event_type is EventType.ATTEMPT_STARTED
            and event.attempt_id is not None
        ):
            last_start[event.attempt_id] = index
    stranded: list[tuple[int, str]] = []
    for attempt_id, attempt in projection.attempts.items():
        if attempt.status is AttemptStatus.RUNNING and attempt_id in last_start:
            stranded.append((last_start[attempt_id], attempt_id))
    stranded.sort(key=lambda pair: pair[0])
    return stranded


def _has_durable_evidence(
    events: tuple[EventEnvelope, ...],
    attempt_id: str,
    after_index: int,
) -> bool:
    """True when an ARTIFACT_COMMITTED names *attempt_id* after *after_index*."""
    for event in events[after_index + 1 :]:
        if (
            event.event_type is EventType.ARTIFACT_COMMITTED
            and event.attempt_id == attempt_id
        ):
            return True
    return False


def _terminal_fact(
    attempt: AttemptRecord, succeeded: bool, attempt_id: str
) -> EventEnvelope:
    invocation_id = attempt.invocation_id
    step_id = attempt.step_id
    payload = {} if succeeded else {"disposition": EXECUTION_INTERRUPTED}
    return EventEnvelope(
        event_id=f"evt-{uuid.uuid4().hex}",
        event_type=(
            EventType.ATTEMPT_SUCCEEDED if succeeded else EventType.ATTEMPT_FAILED
        ),
        timestamp=utc_now(),
        run_id=attempt.run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        payload=payload,
    )


def reconcile_run(
    store: FileSystemRuntimeStore, run_id: str
) -> ReconciliationOutcome:
    """Reconcile one Run after a crash window (see module docstring).

    Idempotent: a second reconcile of an already-reconciled Run appends
    nothing and returns an equal projection. Raises RunNotFoundError for
    unknown runs, EventSchemaError/ProjectionSchemaError for future-format
    events or documents, EvidenceIntegrityError for missing/mismatched
    durable evidence and RuntimeContractError for a history the reducer
    cannot interpret.
    """
    events = store.events(run_id)  # schema fail-fast on load
    projection = reduce_events(events)
    # Durable evidence verification: every committed artifact must have its
    # document present and digest-matched (Ruling 4: no silent drops).
    for artifact_id in projection.artifacts:
        store.load_artifact(artifact_id)

    appended: list[EventEnvelope] = []
    for _index, attempt_id in _stranded_attempts(events, projection):
        attempt = projection.attempts[attempt_id]
        succeeded = _has_durable_evidence(events, attempt_id, _index)
        appended.append(_terminal_fact(attempt, succeeded, attempt_id))
    for event in appended:
        store.append_event(event)

    final_events = store.events(run_id)
    final_projection = reduce_events(final_events)
    store.save_projection(final_projection.run)  # rebuild repairs stale docs
    return ReconciliationOutcome(
        projection=final_projection, appended_events=tuple(appended)
    )
