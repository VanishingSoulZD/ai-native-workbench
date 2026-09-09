"""Event reducer and rebuildable ``run.json`` projection codec (Spec 11).

``reduce_events`` is a pure fact-reduction of an event history into the
current ``RunProjection``: Run/Invocation/Attempt state, input bindings,
failure dispositions, Gates, Checkpoints, committed Artifact references,
canonical bindings and the Snapshot binding. Run state is *derived* from the
authoritative domain events (Ruling 10); ``RUN_STATE_CHANGED`` is
vocabulary-only in v1 and reduces to a no-op. History contradictions fail
fast with ``RuntimeContractError`` — the reducer never guesses.

``serialize_projection`` / ``parse_projection`` are the document codec for
``run.json`` (``runtime_schema_version=1`` at the document root; unknown
schema versions fail fast with ``ProjectionSchemaError``).

v1 payload contracts (authority for every Task 3/6/7 emitter):

- RUN_CREATED: payload {case_id, charter_identity, charter_digest,
  source_declaration_identity, source_declaration_digest} (the frozen
  CaseBinding facts; the Run record is rebuilt from them alone).
- INVOCATION_STARTED (lineage invocation_id): payload {requested_scope:
  [step ids], entry_mode: START|RESUME|FROM|UNTIL, from_step?, until_step?,
  execution_binding: {workflow_identity, workflow_version,
  runtime_configuration_identity, prompts: {id: digest}, schemas: {id: digest}}}.
- ATTEMPT_CREATED (lineage invocation_id, step_id, attempt_id): payload {}.
- INPUT_BOUND (same lineage): payload {input_binding_id, artifact_ids:
  [committed artifact ids], upstream_attempt_ids: [attempt ids]}.
- ATTEMPT_STARTED (same lineage): payload {}; the durable Input Binding of
  the Attempt must already be recorded (Spec 5.5). Legal from PENDING and
  from FAILED (retry stays within the same Attempt).
- ARTIFACT_COMMITTED (lineage invocation_id, artifact_id; step_id/attempt_id
  both set or both absent): payload {digest}.
- VALIDATION_COMPLETED / ACCEPTANCE_RECORDED (lineage artifact_id): payload
  executor-owned; log facts only, no derived state in v1.
- GATE_CREATED (lineage gate_id): payload {logical_gate_id, review_target:
  {step_id, attempt_id, artifact_ids}, supersedes?}.
- GATE_DECIDED (lineage gate_id): payload {decision: APPROVED|REJECTED,
  reviewer, decided_at, comment?, revision_target?: {entry_step, reason}}.
- GATE_SUPERSEDED (lineage gate_id): payload {superseded_by: gate_id}.
- ATTEMPT_SUCCEEDED (attempt lineage): payload {}.
- ATTEMPT_FAILED (attempt lineage): payload {disposition} (e.g.
  EXECUTION_INTERRUPTED, Spec 11.3; dispositions live in the payload only).
- CHECKPOINT_CREATED (lineage step_id): payload {checkpoint_id, artifact_ids,
  compatibility: {workflow_identity, workflow_version, step_identity,
  step_version, runtime_configuration_identity, prompt_identity?,
  prompt_version?, schema_identity?, schema_version?}}.
- CHECKPOINT_INVALIDATED (lineage step_id): payload {checkpoint_id}.
- CANONICAL_BINDING_PENDING / CANONICAL_BINDING_COMMITTED (lineage
  artifact_id of a committed artifact): payload {}.
- SNAPSHOT_BOUND: payload {snapshot_id}; the latest binding wins.
- INVOCATION_COMPLETED (lineage invocation_id): payload {status:
  SUCCEEDED|FAILED, completion_reason}; FAILED with completion_reason
  HUMAN_REJECTION derives NEEDS_REVISION (Task 6 emission contract).
- RUN_STATE_CHANGED: vocabulary-only in v1; never emitted, no state effect.

WAITING_FOR_HUMAN is derived: the Run waits iff at least one Gate is PENDING
and not superseded. Attempt failure dispositions are derived per Attempt and
cleared when a retry round starts.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, fields, is_dataclass, replace
from enum import Enum
from types import MappingProxyType

from ..domain import (
    RUNTIME_SCHEMA_VERSION,
    AttemptRecord,
    AttemptStatus,
    CaseBinding,
    CheckpointRecord,
    CheckpointStatus,
    CompatibilityIdentity,
    EntryMode,
    EventEnvelope,
    EventType,
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
)

HUMAN_REJECTION = "HUMAN_REJECTION"
"""Run/Invocation completion_reason token that derives NEEDS_REVISION."""

BINDING_PENDING = "PENDING"
BINDING_COMMITTED = "COMMITTED"
"""Canonical binding view states (durable canonical facts arrive in T7)."""

# run.json document keys (exact set: unknown keys fail fast).
_DOC_KEYS = frozenset(
    {
        "runtime_schema_version",
        "projection_version",
        "updated_at",
        "run",
        "invocations",
        "attempts",
        "failure_dispositions",
        "input_bindings",
        "gates",
        "checkpoints",
        "artifacts",
        "canonical_bindings",
        "snapshot_binding",
    }
)


class ProjectionSchemaError(Exception):
    """Raised when a projection document violates the v1 document schema."""


# ---------------------------------------------------------------------------
# Projection views (derived facts stored in run.json)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArtifactReference:
    """The durable fact of an ARTIFACT_COMMITTED event (Spec 9.4/11.2)."""

    artifact_id: str
    digest: str
    invocation_id: str
    step_id: str | None
    attempt_id: str | None
    committed_at: str


@dataclass(frozen=True)
class CanonicalBindingView:
    """Canonical-boundary state derived from canonical binding events."""

    artifact_id: str
    status: str  # BINDING_PENDING | BINDING_COMMITTED
    updated_at: str


@dataclass(frozen=True)
class SnapshotBindingView:
    """The Snapshot bound to this Run (SNAPSHOT_BOUND, Task 7)."""

    snapshot_id: str
    bound_at: str


@dataclass(frozen=True)
class RunProjection:
    """The current derived state of one Run.

    Maps are immutable snapshots (MappingProxyType). ``run`` is the derived
    RunRecord; every other section is derived per the reducer contracts
    above. ``runtime_schema_version`` mirrors the document root version.
    """

    run: RunRecord
    invocations: Mapping[str, InvocationRecord]
    attempts: Mapping[str, AttemptRecord]
    failure_dispositions: Mapping[str, str]
    input_bindings: Mapping[str, InputBinding]
    gates: Mapping[str, GateRecord]
    checkpoints: Mapping[str, CheckpointRecord]
    artifacts: Mapping[str, ArtifactReference]
    canonical_bindings: Mapping[str, CanonicalBindingView]
    snapshot_binding: SnapshotBindingView | None
    runtime_schema_version: int = RUNTIME_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.run, RunRecord):
            raise RuntimeContractError("RunProjection.run must be a RunRecord.")
        for name in (
            "invocations",
            "attempts",
            "failure_dispositions",
            "input_bindings",
            "gates",
            "checkpoints",
            "artifacts",
            "canonical_bindings",
        ):
            value = getattr(self, name)
            if not isinstance(value, Mapping):
                raise RuntimeContractError(
                    f"RunProjection.{name} must be a mapping of records."
                )
            object.__setattr__(self, name, MappingProxyType(dict(value)))
        if self.snapshot_binding is not None and not isinstance(
            self.snapshot_binding, SnapshotBindingView
        ):
            raise RuntimeContractError(
                "RunProjection.snapshot_binding must be a SnapshotBindingView or None."
            )
        if (
            type(self.runtime_schema_version) is not int
            or self.runtime_schema_version != RUNTIME_SCHEMA_VERSION
        ):
            raise RuntimeContractError(
                "RunProjection carries an unknown runtime_schema_version; "
                "only 1 is supported in v1."
            )


# ---------------------------------------------------------------------------
# Reducer
# ---------------------------------------------------------------------------


def _text(payload: Mapping[str, object], name: str, event: EventEnvelope) -> str:
    value = payload.get(name)
    if not isinstance(value, str) or not value:
        raise RuntimeContractError(
            f"{event.event_type.value} {event.event_id} payload field "
            f"{name!r} must be a non-empty string."
        )
    return value


def _optional_text(
    payload: Mapping[str, object], name: str, event: EventEnvelope
) -> str | None:
    if name not in payload:
        return None
    return _text(payload, name, event)


def _string_list(
    payload: Mapping[str, object], name: str, event: EventEnvelope
) -> tuple[str, ...]:
    value = payload.get(name)
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise RuntimeContractError(
            f"{event.event_type.value} {event.event_id} payload field "
            f"{name!r} must be a list of non-empty strings."
        )
    return tuple(value)


def _token(cls: type[Enum], payload: Mapping[str, object], name: str, event) -> Enum:
    token = _text(payload, name, event)
    try:
        return cls(token)
    except (ValueError, TypeError) as exc:
        raise RuntimeContractError(
            f"{event.event_type.value} {event.event_id} payload field "
            f"{name!r} names unknown {cls.__name__} token {token!r}."
        ) from exc


def _lineage(event: EventEnvelope, *names: str) -> None:
    for name in names:
        if getattr(event, name) is None:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} requires "
                f"{name} lineage; none recorded."
            )


def _binding_map(payload: Mapping[str, object], name: str, event) -> Mapping[str, str]:
    value = payload.get(name, {})
    if not isinstance(value, Mapping) or not all(
        isinstance(key, str) and isinstance(item, str)
        for key, item in value.items()
    ):
        raise RuntimeContractError(
            f"{event.event_type.value} {event.event_id} payload field "
            f"{name!r} must map identities to digests."
        )
    return value


class _Reducer:
    """Sequential event replay with strict fact contracts (see module docs)."""

    def __init__(self, events: Iterable[EventEnvelope]) -> None:
        self._events = tuple(events)
        self._run_id: str | None = None
        self._run: RunRecord | None = None
        self._invocations: dict[str, InvocationRecord] = {}
        self._attempts: dict[str, AttemptRecord] = {}
        self._failure_dispositions: dict[str, str] = {}
        self._bindings: dict[str, InputBinding] = {}
        self._gates: dict[str, GateRecord] = {}
        self._checkpoints: dict[str, CheckpointRecord] = {}
        self._artifacts: dict[str, ArtifactReference] = {}
        self._canonical_bindings: dict[str, CanonicalBindingView] = {}
        self._snapshot_binding: SnapshotBindingView | None = None
        self._run_created_seen = False

    def projection(self) -> RunProjection:
        if self._run is None:
            raise RuntimeContractError(
                "cannot reduce an event history without a RUN_CREATED fact."
            )
        return RunProjection(
            run=self._run,
            invocations=self._invocations,
            attempts=self._attempts,
            failure_dispositions=self._failure_dispositions,
            input_bindings=self._bindings,
            gates=self._gates,
            checkpoints=self._checkpoints,
            artifacts=self._artifacts,
            canonical_bindings=self._canonical_bindings,
            snapshot_binding=self._snapshot_binding,
        )

    # -- replay -------------------------------------------------------------

    def run(self) -> RunProjection:
        if not self._events:
            raise RuntimeContractError(
                "cannot reduce an empty event history: a Run begins with "
                "RUN_CREATED."
            )
        first, *rest = self._events
        self._apply_run_created(first)
        for event in rest:
            if event.run_id != self._run_id:
                raise RuntimeContractError(
                    f"event {event.event_id} belongs to run {event.run_id}, "
                    f"not run {self._run_id}; histories are per-run."
                )
            handler = _HANDLERS[event.event_type]
            handler(self, event)
        return self.projection()

    # -- helpers -------------------------------------------------------------

    def _require_run(self, event: EventEnvelope) -> RunRecord:
        if self._run is None:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} precedes the "
                "RUN_CREATED fact."
            )
        return self._run

    def _attempt(self, event: EventEnvelope) -> AttemptRecord:
        _lineage(event, "invocation_id", "step_id", "attempt_id")
        attempt = self._attempts.get(event.attempt_id)
        if attempt is None:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} references "
                f"attempt {event.attempt_id!r}, which was never created."
            )
        if attempt.invocation_id != event.invocation_id or attempt.step_id != event.step_id:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} lineage "
                f"(invocation {event.invocation_id}, step {event.step_id}) does "
                f"not match attempt {event.attempt_id!r}."
            )
        return attempt

    def _binding_for_attempt(self, attempt_id: str) -> str | None:
        for binding in self._bindings.values():
            if binding.attempt_id == attempt_id:
                return binding.input_binding_id
        return None

    def _sync_wait_state(self) -> None:
        """Derive WAITING_FOR_HUMAN from unresolved Gates (see module docs)."""
        run = self._run
        if run is None or run.state not in (
            RunState.RUNNING,
            RunState.WAITING_FOR_HUMAN,
        ):
            return
        pending = any(
            gate.decision is GateDecision.PENDING and gate.superseded_by is None
            for gate in self._gates.values()
        )
        if pending:
            if run.state is RunState.RUNNING:
                self._run = run.wait_for_human()
        elif run.state is RunState.WAITING_FOR_HUMAN:
            self._run = run.mark_running()

    def _gate(self, event: EventEnvelope) -> GateRecord:
        _lineage(event, "gate_id")
        gate = self._gates.get(event.gate_id)
        if gate is None:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} references gate "
                f"{event.gate_id!r}, which was never created."
            )
        return gate

    def _require_active_run(self, event: EventEnvelope) -> None:
        run = self._require_run(event)
        if run.state not in (RunState.RUNNING, RunState.WAITING_FOR_HUMAN):
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} requires an "
                f"active run; state is {run.state.value}."
            )

    def _complete_invocation(self, event: EventEnvelope) -> None:
        _lineage(event, "invocation_id")
        invocation = self._invocations.get(event.invocation_id)
        if invocation is None:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} references "
                f"invocation {event.invocation_id!r}, which was never started."
            )
        if invocation.status is not InvocationStatus.RUNNING:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id}: invocation "
                f"{event.invocation_id} is already "
                f"{invocation.status.value}."
            )
        payload = event.payload
        status = _token(InvocationStatus, payload, "status", event)
        if status not in (InvocationStatus.SUCCEEDED, InvocationStatus.FAILED):
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} may only complete "
                f"an invocation as SUCCEEDED or FAILED."
            )
        reason = _text(payload, "completion_reason", event)
        run = self._require_run(event)
        if run.state is not RunState.RUNNING:
            raise RuntimeContractError(
                f"{event.event_type.value} {event.event_id} requires a "
                f"RUNNING run; state is {run.state.value}."
            )
        if status is InvocationStatus.SUCCEEDED:
            self._invocations[event.invocation_id] = invocation.succeed()
            self._run = run.complete(reason, execution_scope=invocation.requested_scope)
        else:
            self._invocations[event.invocation_id] = invocation.fail(reason)
            if reason == HUMAN_REJECTION:
                self._run = run.needs_revision()
            else:
                self._run = run.fail(reason)
        self._run = replace(self._run, current_invocation_id=None)

    # -- per-type handlers ---------------------------------------------------

    def _apply_run_created(self, event: EventEnvelope) -> None:
        if event.event_type is not EventType.RUN_CREATED:
            raise RuntimeContractError(
                "an event history must begin with RUN_CREATED "
                f"(got {event.event_type.value})."
            )
        if self._run_created_seen:
            raise RuntimeContractError(
                f"duplicate RUN_CREATED fact {event.event_id}; a Run is "
                "created exactly once."
            )
        self._run_created_seen = True
        self._run_id = event.run_id
        payload = event.payload
        case_binding = CaseBinding(
            case_id=_text(payload, "case_id", event),
            charter_identity=_text(payload, "charter_identity", event),
            charter_digest=_text(payload, "charter_digest", event),
            source_declaration_identity=_text(
                payload, "source_declaration_identity", event
            ),
            source_declaration_digest=_text(
                payload, "source_declaration_digest", event
            ),
        )
        self._run = RunRecord(
            run_id=event.run_id,
            case_id=case_binding.case_id,
            case_binding=case_binding,
            state=RunState.CREATED,
            cumulative_execution_scope=(),
            current_invocation_id=None,
            completion_reason=None,
        )

    def _apply_invocation_started(self, event: EventEnvelope) -> None:
        _lineage(event, "invocation_id")
        if event.invocation_id in self._invocations:
            raise RuntimeContractError(
                f"duplicate INVOCATION_STARTED for invocation "
                f"{event.invocation_id}; invocations are immutable requests."
            )
        payload = event.payload
        binding = payload.get("execution_binding")
        if not isinstance(binding, Mapping):
            raise RuntimeContractError(
                f"{event.event_id} INVOCATION_STARTED payload requires an "
                "execution_binding mapping."
            )
        scope = _string_list(payload, "requested_scope", event)
        if not scope:
            raise RuntimeContractError(
                f"{event.event_id} INVOCATION_STARTED payload "
                "requested_scope must not be empty."
            )
        execution_binding = ExecutionBinding(
            workflow_identity=_text(binding, "workflow_identity", event),
            workflow_version=_text(binding, "workflow_version", event),
            runtime_configuration_identity=_text(
                binding, "runtime_configuration_identity", event
            ),
            prompts=_binding_map(binding, "prompts", event),
            schemas=_binding_map(binding, "schemas", event),
        )
        entry_mode = _token(EntryMode, payload, "entry_mode", event)
        run = self._require_run(event)
        if run.state is RunState.CREATED:
            self._run = run.start()
        elif run.state in (
            RunState.COMPLETED,
            RunState.NEEDS_REVISION,
            RunState.FAILED,
        ):
            self._run = run.begin_resume()
        else:
            raise RuntimeContractError(
                f"{event.event_id} INVOCATION_STARTED: run {run.run_id} "
                f"cannot start an invocation from state {run.state.value}; "
                "resume the run explicitly first."
            )
        self._run = replace(self._run, current_invocation_id=event.invocation_id)
        self._invocations[event.invocation_id] = InvocationRecord(
            invocation_id=event.invocation_id,
            run_id=self._run.run_id,
            requested_scope=scope,
            entry_mode=entry_mode,
            execution_binding=execution_binding,
            status=InvocationStatus.RUNNING,
            from_step=_optional_text(payload, "from_step", event),
            until_step=_optional_text(payload, "until_step", event),
        )

    def _apply_attempt_created(self, event: EventEnvelope) -> None:
        _lineage(event, "invocation_id", "step_id", "attempt_id")
        if event.attempt_id in self._attempts:
            raise RuntimeContractError(
                f"duplicate ATTEMPT_CREATED for attempt {event.attempt_id}."
            )
        # ATTEMPT_CREATED is a pure declaration with envelope lineage: it does
        # not require the Invocation to be started yet (the store-level append
        # idempotency contract appends attempts right after RUN_CREATED).
        # Coherence with the Invocation is enforced at the boundary events
        # (INPUT_BOUND/ATTEMPT_STARTED/ARTIFACT_COMMITTED) that do check it.
        self._attempts[event.attempt_id] = AttemptRecord(
            attempt_id=event.attempt_id,
            run_id=self._require_run(event).run_id,
            invocation_id=event.invocation_id,
            step_id=event.step_id,
            status=AttemptStatus.PENDING,
        )

    def _apply_input_bound(self, event: EventEnvelope) -> None:
        attempt = self._attempt(event)
        if attempt.status is not AttemptStatus.PENDING:
            raise RuntimeContractError(
                f"{event.event_id} INPUT_BOUND: attempt {attempt.attempt_id} "
                "is not PENDING; input bindings precede the first start."
            )
        payload = event.payload
        binding_id = _text(payload, "input_binding_id", event)
        if binding_id in self._bindings:
            raise RuntimeContractError(
                f"duplicate INPUT_BOUND for binding {binding_id!r}."
            )
        if self._binding_for_attempt(attempt.attempt_id) is not None:
            raise RuntimeContractError(
                f"{event.event_id} INPUT_BOUND: attempt {attempt.attempt_id} "
                "is already bound."
            )
        artifact_ids = _string_list(payload, "artifact_ids", event)
        for artifact_id in artifact_ids:
            if artifact_id not in self._artifacts:
                raise RuntimeContractError(
                    f"{event.event_id} INPUT_BOUND binds artifact "
                    f"{artifact_id!r}, which is not a committed artifact; "
                    "inputs are exact committed Artifact IDs (no residue)."
                )
        upstream = _string_list(payload, "upstream_attempt_ids", event)
        for upstream_id in upstream:
            if upstream_id not in self._attempts:
                raise RuntimeContractError(
                    f"{event.event_id} INPUT_BOUND names unknown upstream "
                    f"attempt {upstream_id!r}."
                )
        self._bindings[binding_id] = InputBinding(
            input_binding_id=binding_id,
            run_id=self._require_run(event).run_id,
            invocation_id=event.invocation_id,
            step_id=event.step_id,
            attempt_id=event.attempt_id,
            artifact_ids=artifact_ids,
            upstream_attempt_ids=upstream,
        )

    def _apply_attempt_started(self, event: EventEnvelope) -> None:
        attempt = self._attempt(event)
        binding = attempt.input_binding_id
        if binding is None:
            binding = self._binding_for_attempt(attempt.attempt_id)
        if binding is None:
            raise RuntimeContractError(
                f"{event.event_id} ATTEMPT_STARTED: attempt "
                f"{attempt.attempt_id} has no durable input binding "
                "(Spec 5.5: INPUT_BOUND must precede the first start)."
            )
        self._attempts[attempt.attempt_id] = attempt.mark_running(binding)
        self._failure_dispositions.pop(attempt.attempt_id, None)

    def _apply_artifact_committed(self, event: EventEnvelope) -> None:
        _lineage(event, "invocation_id", "artifact_id")
        if (event.step_id is None) != (event.attempt_id is None):
            raise RuntimeContractError(
                f"{event.event_id} ARTIFACT_COMMITTED step_id and attempt_id "
                "must be set together or both absent (source acquisition)."
            )
        if event.artifact_id in self._artifacts:
            raise RuntimeContractError(
                f"duplicate ARTIFACT_COMMITTED for artifact "
                f"{event.artifact_id}; artifacts commit exactly once."
            )
        digest = _text(event.payload, "digest", event)
        invocation = self._invocations.get(event.invocation_id)
        if invocation is None:
            raise RuntimeContractError(
                f"{event.event_id} ARTIFACT_COMMITTED references unknown "
                f"invocation {event.invocation_id!r}."
            )
        if invocation.status is not InvocationStatus.RUNNING:
            raise RuntimeContractError(
                f"{event.event_id} ARTIFACT_COMMITTED: invocation "
                f"{event.invocation_id} is not RUNNING."
            )
        if event.attempt_id is not None:
            attempt = self._attempt(event)
            if attempt.status is not AttemptStatus.RUNNING:
                raise RuntimeContractError(
                    f"{event.event_id} ARTIFACT_COMMITTED: attempt "
                    f"{attempt.attempt_id} is not RUNNING."
                )
        self._artifacts[event.artifact_id] = ArtifactReference(
            artifact_id=event.artifact_id,
            digest=digest,
            invocation_id=event.invocation_id,
            step_id=event.step_id,
            attempt_id=event.attempt_id,
            committed_at=event.timestamp,
        )

    def _apply_attempt_succeeded(self, event: EventEnvelope) -> None:
        attempt = self._attempt(event)
        self._attempts[attempt.attempt_id] = attempt.mark_succeeded()

    def _apply_attempt_failed(self, event: EventEnvelope) -> None:
        attempt = self._attempt(event)
        disposition = _text(event.payload, "disposition", event)
        self._attempts[attempt.attempt_id] = attempt.mark_failed()
        self._failure_dispositions[attempt.attempt_id] = disposition

    def _apply_gate_created(self, event: EventEnvelope) -> None:
        _lineage(event, "gate_id")
        self._require_active_run(event)
        if event.gate_id in self._gates:
            raise RuntimeContractError(
                f"duplicate GATE_CREATED for gate {event.gate_id}."
            )
        payload = event.payload
        target = payload.get("review_target")
        if not isinstance(target, Mapping):
            raise RuntimeContractError(
                f"{event.event_id} GATE_CREATED payload requires a "
                "review_target mapping."
            )
        artifact_ids = _string_list(target, "artifact_ids", event)
        if not artifact_ids:
            raise RuntimeContractError(
                f"{event.event_id} GATE_CREATED review_target.artifact_ids "
                "must not be empty (a Gate binds exact candidates)."
            )
        for artifact_id in artifact_ids:
            if artifact_id not in self._artifacts:
                raise RuntimeContractError(
                    f"{event.event_id} GATE_CREATED reviews artifact "
                    f"{artifact_id!r}, which is not committed."
                )
        attempt_id = _text(target, "attempt_id", event)
        target_attempt = self._attempts.get(attempt_id)
        if target_attempt is None:
            raise RuntimeContractError(
                f"{event.event_id} GATE_CREATED reviews unknown attempt "
                f"{attempt_id!r}."
            )
        if target_attempt.step_id != _text(target, "step_id", event):
            raise RuntimeContractError(
                f"{event.event_id} GATE_CREATED review_target.step_id does "
                "not match the reviewed attempt."
            )
        supersedes = _optional_text(payload, "supersedes", event)
        if supersedes is not None:
            if supersedes not in self._gates:
                raise RuntimeContractError(
                    f"{event.event_id} GATE_CREATED supersedes unknown gate "
                    f"{supersedes!r}."
                )
        self._gates[event.gate_id] = GateRecord(
            gate_id=event.gate_id,
            run_id=self._require_run(event).run_id,
            logical_gate_id=_text(payload, "logical_gate_id", event),
            review_target=ReviewTarget(
                step_id=target_attempt.step_id,
                attempt_id=attempt_id,
                artifact_ids=artifact_ids,
            ),
            decision=GateDecision.PENDING,
            created_at=event.timestamp,
            supersedes=supersedes,
        )
        self._sync_wait_state()

    def _apply_gate_decided(self, event: EventEnvelope) -> None:
        gate = self._gate(event)
        self._require_active_run(event)
        payload = event.payload
        decision = _token(GateDecision, payload, "decision", event)
        reviewer = _text(payload, "reviewer", event)
        decided_at = _text(payload, "decided_at", event)
        comment = _optional_text(payload, "comment", event)
        revision = payload.get("revision_target")
        revision_target = None
        if revision is not None:
            if not isinstance(revision, Mapping):
                raise RuntimeContractError(
                    f"{event.event_id} GATE_DECIDED revision_target must be "
                    "a mapping."
                )
            revision_target = RevisionTarget(
                entry_step=_text(revision, "entry_step", event),
                reason=_text(revision, "reason", event),
            )
        self._gates[gate.gate_id] = gate.decide(
            decision,
            reviewer,
            decided_at,
            comment=comment,
            revision_target=revision_target,
        )
        self._sync_wait_state()

    def _apply_gate_superseded(self, event: EventEnvelope) -> None:
        gate = self._gate(event)
        self._require_active_run(event)
        superseded_by = _text(event.payload, "superseded_by", event)
        if superseded_by not in self._gates:
            raise RuntimeContractError(
                f"{event.event_id} GATE_SUPERSEDED names unknown replacement "
                f"gate {superseded_by!r}."
            )
        self._gates[gate.gate_id] = gate.mark_superseded_by(superseded_by)
        self._sync_wait_state()

    def _apply_checkpoint_created(self, event: EventEnvelope) -> None:
        _lineage(event, "step_id")
        payload = event.payload
        checkpoint_id = _text(payload, "checkpoint_id", event)
        if checkpoint_id in self._checkpoints:
            raise RuntimeContractError(
                f"duplicate CHECKPOINT_CREATED for checkpoint "
                f"{checkpoint_id!r}."
            )
        artifact_ids = _string_list(payload, "artifact_ids", event)
        if not artifact_ids:
            raise RuntimeContractError(
                f"{event.event_id} CHECKPOINT_CREATED artifact_ids must not "
                "be empty."
            )
        for artifact_id in artifact_ids:
            if artifact_id not in self._artifacts:
                raise RuntimeContractError(
                    f"{event.event_id} CHECKPOINT_CREATED records artifact "
                    f"{artifact_id!r}, which is not committed."
                )
        compatibility = payload.get("compatibility")
        if not isinstance(compatibility, Mapping):
            raise RuntimeContractError(
                f"{event.event_id} CHECKPOINT_CREATED payload requires a "
                "compatibility mapping."
            )
        self._checkpoints[checkpoint_id] = CheckpointRecord(
            checkpoint_id=checkpoint_id,
            run_id=self._require_run(event).run_id,
            step_id=event.step_id,
            artifact_ids=artifact_ids,
            compatibility=CompatibilityIdentity(
                workflow_identity=_text(compatibility, "workflow_identity", event),
                workflow_version=_text(compatibility, "workflow_version", event),
                step_identity=_text(compatibility, "step_identity", event),
                step_version=_text(compatibility, "step_version", event),
                runtime_configuration_identity=_text(
                    compatibility, "runtime_configuration_identity", event
                ),
                prompt_identity=_optional_text(
                    compatibility, "prompt_identity", event
                ),
                prompt_version=_optional_text(
                    compatibility, "prompt_version", event
                ),
                schema_identity=_optional_text(
                    compatibility, "schema_identity", event
                ),
                schema_version=_optional_text(
                    compatibility, "schema_version", event
                ),
            ),
            created_at=event.timestamp,
        )

    def _apply_checkpoint_invalidated(self, event: EventEnvelope) -> None:
        _lineage(event, "step_id")
        checkpoint_id = _text(event.payload, "checkpoint_id", event)
        checkpoint = self._checkpoints.get(checkpoint_id)
        if checkpoint is None:
            raise RuntimeContractError(
                f"{event.event_id} CHECKPOINT_INVALIDATED references unknown "
                f"checkpoint {checkpoint_id!r}."
            )
        if checkpoint.step_id != event.step_id:
            raise RuntimeContractError(
                f"{event.event_id} CHECKPOINT_INVALIDATED lineage does not "
                "match the recorded checkpoint."
            )
        self._checkpoints[checkpoint_id] = checkpoint.invalidate()

    def _apply_canonical_binding_pending(self, event: EventEnvelope) -> None:
        _lineage(event, "artifact_id")
        if event.artifact_id not in self._artifacts:
            raise RuntimeContractError(
                f"{event.event_id} CANONICAL_BINDING_PENDING targets "
                f"artifact {event.artifact_id!r}, which is not committed."
            )
        if event.artifact_id in self._canonical_bindings:
            raise RuntimeContractError(
                f"{event.event_id} CANONICAL_BINDING_PENDING: artifact "
                f"{event.artifact_id} is already bound."
            )
        self._canonical_bindings[event.artifact_id] = CanonicalBindingView(
            artifact_id=event.artifact_id,
            status=BINDING_PENDING,
            updated_at=event.timestamp,
        )

    def _apply_canonical_binding_committed(self, event: EventEnvelope) -> None:
        _lineage(event, "artifact_id")
        binding = self._canonical_bindings.get(event.artifact_id)
        if binding is None or binding.status != BINDING_PENDING:
            raise RuntimeContractError(
                f"{event.event_id} CANONICAL_BINDING_COMMITTED requires a "
                "prior PENDING binding of artifact "
                f"{event.artifact_id!r}."
            )
        self._canonical_bindings[event.artifact_id] = CanonicalBindingView(
            artifact_id=event.artifact_id,
            status=BINDING_COMMITTED,
            updated_at=event.timestamp,
        )

    def _apply_snapshot_bound(self, event: EventEnvelope) -> None:
        self._snapshot_binding = SnapshotBindingView(
            snapshot_id=_text(event.payload, "snapshot_id", event),
            bound_at=event.timestamp,
        )

    def _apply_invocation_completed(self, event: EventEnvelope) -> None:
        self._complete_invocation(event)

    def _apply_validation_completed(self, event: EventEnvelope) -> None:
        _lineage(event, "artifact_id")  # log fact only in v1

    def _apply_acceptance_recorded(self, event: EventEnvelope) -> None:
        _lineage(event, "artifact_id")  # log fact only in v1

    def _apply_run_state_changed(self, event: EventEnvelope) -> None:
        # Ruling 10: vocabulary-only in v1; never emitted, no state effect.
        return None


_HANDLERS: dict[EventType, object] = {
    EventType.RUN_CREATED: _Reducer._apply_run_created,
    EventType.INVOCATION_STARTED: _Reducer._apply_invocation_started,
    EventType.ATTEMPT_CREATED: _Reducer._apply_attempt_created,
    EventType.INPUT_BOUND: _Reducer._apply_input_bound,
    EventType.ATTEMPT_STARTED: _Reducer._apply_attempt_started,
    EventType.ARTIFACT_COMMITTED: _Reducer._apply_artifact_committed,
    EventType.VALIDATION_COMPLETED: _Reducer._apply_validation_completed,
    EventType.ACCEPTANCE_RECORDED: _Reducer._apply_acceptance_recorded,
    EventType.GATE_CREATED: _Reducer._apply_gate_created,
    EventType.GATE_DECIDED: _Reducer._apply_gate_decided,
    EventType.GATE_SUPERSEDED: _Reducer._apply_gate_superseded,
    EventType.ATTEMPT_SUCCEEDED: _Reducer._apply_attempt_succeeded,
    EventType.ATTEMPT_FAILED: _Reducer._apply_attempt_failed,
    EventType.CHECKPOINT_CREATED: _Reducer._apply_checkpoint_created,
    EventType.CHECKPOINT_INVALIDATED: _Reducer._apply_checkpoint_invalidated,
    EventType.CANONICAL_BINDING_PENDING: _Reducer._apply_canonical_binding_pending,
    EventType.CANONICAL_BINDING_COMMITTED: _Reducer._apply_canonical_binding_committed,
    EventType.SNAPSHOT_BOUND: _Reducer._apply_snapshot_bound,
    EventType.INVOCATION_COMPLETED: _Reducer._apply_invocation_completed,
    EventType.RUN_STATE_CHANGED: _Reducer._apply_run_state_changed,
}


def reduce_events(events: Iterable[EventEnvelope]) -> RunProjection:
    """Reduce *events* into the current RunProjection (pure function).

    Raises RuntimeContractError for any history contradiction; unknown event
    schema versions must be rejected by the caller's load path before the
    reducer ever sees them (the store's event log validates on load).
    """
    return _Reducer(events).run()


# ---------------------------------------------------------------------------
# run.json document codec
# ---------------------------------------------------------------------------


def _to_jsonable(value: object) -> object:
    """Recursively convert records/enums/proxies to plain JSON structures."""
    if is_dataclass(value) and not isinstance(value, type):
        return {f.name: _to_jsonable(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {key: _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


def serialize_projection(
    projection: RunProjection, projection_version: int, updated_at: str
) -> dict[str, object]:
    """Serialize *projection* into a plain run.json document dict.

    ``runtime_schema_version=1`` is declared at the document root only;
    unknown projection versions fail fast.
    """
    if not isinstance(projection, RunProjection):
        raise ProjectionSchemaError(
            "serialize_projection requires a RunProjection."
        )
    if type(projection_version) is not int or projection_version < 1:
        raise ProjectionSchemaError(
            "projection_version must be an int >= 1 "
            f"(got {projection_version!r})."
        )
    if not isinstance(updated_at, str) or not updated_at:
        raise ProjectionSchemaError("updated_at must be a non-empty string.")
    return {
        "runtime_schema_version": RUNTIME_SCHEMA_VERSION,
        "projection_version": projection_version,
        "updated_at": updated_at,
        "run": _to_jsonable(projection.run),
        "invocations": _to_jsonable(projection.invocations),
        "attempts": _to_jsonable(projection.attempts),
        "failure_dispositions": _to_jsonable(projection.failure_dispositions),
        "input_bindings": _to_jsonable(projection.input_bindings),
        "gates": _to_jsonable(projection.gates),
        "checkpoints": _to_jsonable(projection.checkpoints),
        "artifacts": _to_jsonable(projection.artifacts),
        "canonical_bindings": _to_jsonable(projection.canonical_bindings),
        "snapshot_binding": _to_jsonable(projection.snapshot_binding),
    }


# -- record decode helpers ----------------------------------------------------


def _record_keys(obj: object, allowed: frozenset[str], label: str) -> dict[str, object]:
    if not isinstance(obj, Mapping):
        raise ProjectionSchemaError(f"{label} must be a JSON object.")
    unknown = set(obj) - set(allowed)
    if unknown:
        raise ProjectionSchemaError(
            f"{label} carries unknown fields {sorted(unknown)}; only the v1 "
            "record shape is supported."
        )
    return obj


def _schema_str(obj: Mapping[str, object], name: str, label: str) -> str:
    value = obj.get(name)
    if not isinstance(value, str) or not value:
        raise ProjectionSchemaError(
            f"{label}.{name} must be a non-empty string."
        )
    return value


def _schema_opt_str(
    obj: Mapping[str, object], name: str, label: str
) -> str | None:
    if name not in obj or obj[name] is None:
        return None
    return _schema_str(obj, name, label)


def _schema_str_list(
    obj: Mapping[str, object], name: str, label: str
) -> tuple[str, ...]:
    value = obj.get(name)
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ProjectionSchemaError(
            f"{label}.{name} must be a list of non-empty strings."
        )
    return tuple(value)


def _schema_enum(cls: type[Enum], obj: Mapping[str, object], name: str, label: str):
    token = _schema_str(obj, name, label)
    try:
        return cls(token)
    except (ValueError, TypeError) as exc:
        raise ProjectionSchemaError(
            f"{label}.{name} names unknown {cls.__name__} token {token!r}."
        ) from exc


def _schema_version(obj: Mapping[str, object], label: str) -> int:
    value = obj.get("runtime_schema_version", RUNTIME_SCHEMA_VERSION)
    if type(value) is not int or value != RUNTIME_SCHEMA_VERSION:
        raise ProjectionSchemaError(
            f"{label} uses unknown runtime_schema_version {value!r}; only "
            f"{RUNTIME_SCHEMA_VERSION} is supported in v1."
        )
    return value


def _construct(label: str, factory, **kwargs):
    try:
        return factory(**kwargs)
    except RuntimeContractError as exc:
        raise ProjectionSchemaError(f"{label}: {exc}") from exc


def _decode_case_binding(obj: Mapping[str, object], label: str) -> CaseBinding:
    record = _record_keys(obj, _CASE_BINDING_KEYS, label)
    return _construct(
        label,
        CaseBinding,
        case_id=_schema_str(record, "case_id", label),
        charter_identity=_schema_str(record, "charter_identity", label),
        charter_digest=_schema_str(record, "charter_digest", label),
        source_declaration_identity=_schema_str(
            record, "source_declaration_identity", label
        ),
        source_declaration_digest=_schema_str(
            record, "source_declaration_digest", label
        ),
    )


def _decode_execution_binding(
    obj: Mapping[str, object], label: str
) -> ExecutionBinding:
    record = _record_keys(obj, _EXECUTION_BINDING_KEYS, label)
    return _construct(
        label,
        ExecutionBinding,
        workflow_identity=_schema_str(record, "workflow_identity", label),
        workflow_version=_schema_str(record, "workflow_version", label),
        runtime_configuration_identity=_schema_str(
            record, "runtime_configuration_identity", label
        ),
        prompts=_schema_str_map(record, "prompts", label),
        schemas=_schema_str_map(record, "schemas", label),
    )


def _schema_str_map(
    obj: Mapping[str, object], name: str, label: str
) -> Mapping[str, str]:
    value = obj.get(name, {})
    if not isinstance(value, Mapping) or not all(
        isinstance(key, str) and isinstance(item, str)
        for key, item in value.items()
    ):
        raise ProjectionSchemaError(
            f"{label}.{name} must map identities to digests."
        )
    return value


def _decode_compatibility(obj: Mapping[str, object], label: str) -> CompatibilityIdentity:
    record = _record_keys(obj, _COMPATIBILITY_KEYS, label)
    return _construct(
        label,
        CompatibilityIdentity,
        workflow_identity=_schema_str(record, "workflow_identity", label),
        workflow_version=_schema_str(record, "workflow_version", label),
        step_identity=_schema_str(record, "step_identity", label),
        step_version=_schema_str(record, "step_version", label),
        runtime_configuration_identity=_schema_str(
            record, "runtime_configuration_identity", label
        ),
        prompt_identity=_schema_opt_str(record, "prompt_identity", label),
        prompt_version=_schema_opt_str(record, "prompt_version", label),
        schema_identity=_schema_opt_str(record, "schema_identity", label),
        schema_version=_schema_opt_str(record, "schema_version", label),
    )


def _decode_review_target(obj: Mapping[str, object], label: str) -> ReviewTarget:
    record = _record_keys(obj, _REVIEW_TARGET_KEYS, label)
    return _construct(
        label,
        ReviewTarget,
        step_id=_schema_str(record, "step_id", label),
        attempt_id=_schema_str(record, "attempt_id", label),
        artifact_ids=_schema_str_list(record, "artifact_ids", label),
    )


def _decode_revision_target(obj: Mapping[str, object], label: str) -> RevisionTarget:
    record = _record_keys(obj, _REVISION_TARGET_KEYS, label)
    return _construct(
        label,
        RevisionTarget,
        entry_step=_schema_str(record, "entry_step", label),
        reason=_schema_str(record, "reason", label),
    )


def _decode_run(obj: object) -> RunRecord:
    label = "run"
    record = _record_keys(obj, _RUN_KEYS, label)
    _schema_version(record, label)
    return _construct(
        label,
        RunRecord,
        run_id=_schema_str(record, "run_id", label),
        case_id=_schema_str(record, "case_id", label),
        case_binding=_decode_case_binding(record["case_binding"], "run.case_binding"),
        state=_schema_enum(RunState, record, "state", label),
        cumulative_execution_scope=_schema_str_list(
            record, "cumulative_execution_scope", label
        ),
        current_invocation_id=_schema_opt_str(
            record, "current_invocation_id", label
        ),
        completion_reason=_schema_opt_str(record, "completion_reason", label),
        runtime_schema_version=record.get(
            "runtime_schema_version", RUNTIME_SCHEMA_VERSION
        ),
    )


def _decode_invocation(obj: object) -> InvocationRecord:
    label = "invocations.<id>"
    record = _record_keys(obj, _INVOCATION_KEYS, label)
    _schema_version(record, label)
    return _construct(
        label,
        InvocationRecord,
        invocation_id=_schema_str(record, "invocation_id", label),
        run_id=_schema_str(record, "run_id", label),
        requested_scope=_schema_str_list(record, "requested_scope", label),
        entry_mode=_schema_enum(EntryMode, record, "entry_mode", label),
        execution_binding=_decode_execution_binding(
            record["execution_binding"], "invocations.execution_binding"
        ),
        status=_schema_enum(InvocationStatus, record, "status", label),
        from_step=_schema_opt_str(record, "from_step", label),
        until_step=_schema_opt_str(record, "until_step", label),
        completion_reason=_schema_opt_str(record, "completion_reason", label),
        runtime_schema_version=record.get(
            "runtime_schema_version", RUNTIME_SCHEMA_VERSION
        ),
    )


def _decode_attempt(obj: object) -> AttemptRecord:
    label = "attempts.<id>"
    record = _record_keys(obj, _ATTEMPT_KEYS, label)
    _schema_version(record, label)
    return _construct(
        label,
        AttemptRecord,
        attempt_id=_schema_str(record, "attempt_id", label),
        run_id=_schema_str(record, "run_id", label),
        invocation_id=_schema_str(record, "invocation_id", label),
        step_id=_schema_str(record, "step_id", label),
        status=_schema_enum(AttemptStatus, record, "status", label),
        input_binding_id=_schema_opt_str(record, "input_binding_id", label),
        runtime_schema_version=record.get(
            "runtime_schema_version", RUNTIME_SCHEMA_VERSION
        ),
    )


def _decode_input_binding(obj: object) -> InputBinding:
    label = "input_bindings.<id>"
    record = _record_keys(obj, _INPUT_BINDING_KEYS, label)
    return _construct(
        label,
        InputBinding,
        input_binding_id=_schema_str(record, "input_binding_id", label),
        run_id=_schema_str(record, "run_id", label),
        invocation_id=_schema_str(record, "invocation_id", label),
        step_id=_schema_str(record, "step_id", label),
        attempt_id=_schema_str(record, "attempt_id", label),
        artifact_ids=_schema_str_list(record, "artifact_ids", label),
        upstream_attempt_ids=_schema_str_list(
            record, "upstream_attempt_ids", label
        ),
    )


def _decode_gate(obj: object) -> GateRecord:
    label = "gates.<id>"
    record = _record_keys(obj, _GATE_KEYS, label)
    revision = record.get("revision_target")
    if revision is not None and not isinstance(revision, Mapping):
        raise ProjectionSchemaError("gates.<id>.revision_target must be a JSON object.")
    return _construct(
        label,
        GateRecord,
        gate_id=_schema_str(record, "gate_id", label),
        run_id=_schema_str(record, "run_id", label),
        logical_gate_id=_schema_str(record, "logical_gate_id", label),
        review_target=_decode_review_target(
            record["review_target"], "gates.review_target"
        ),
        decision=_schema_enum(GateDecision, record, "decision", label),
        created_at=_schema_str(record, "created_at", label),
        reviewer=_schema_opt_str(record, "reviewer", label),
        decided_at=_schema_opt_str(record, "decided_at", label),
        comment=_schema_opt_str(record, "comment", label),
        revision_target=(
            _decode_revision_target(revision, "gates.revision_target")
            if revision is not None
            else None
        ),
        supersedes=_schema_opt_str(record, "supersedes", label),
        superseded_by=_schema_opt_str(record, "superseded_by", label),
    )


def _decode_checkpoint(obj: object) -> CheckpointRecord:
    label = "checkpoints.<id>"
    record = _record_keys(obj, _CHECKPOINT_KEYS, label)
    return _construct(
        label,
        CheckpointRecord,
        checkpoint_id=_schema_str(record, "checkpoint_id", label),
        run_id=_schema_str(record, "run_id", label),
        step_id=_schema_str(record, "step_id", label),
        artifact_ids=_schema_str_list(record, "artifact_ids", label),
        compatibility=_decode_compatibility(
            record["compatibility"], "checkpoints.compatibility"
        ),
        created_at=_schema_str(record, "created_at", label),
        status=_schema_enum(CheckpointStatus, record, "status", label),
    )


def _decode_artifact_reference(obj: object) -> ArtifactReference:
    label = "artifacts.<id>"
    record = _record_keys(obj, _ARTIFACT_REFERENCE_KEYS, label)
    return ArtifactReference(
        artifact_id=_schema_str(record, "artifact_id", label),
        digest=_schema_str(record, "digest", label),
        invocation_id=_schema_str(record, "invocation_id", label),
        step_id=_schema_opt_str(record, "step_id", label),
        attempt_id=_schema_opt_str(record, "attempt_id", label),
        committed_at=_schema_str(record, "committed_at", label),
    )


def _decode_canonical_binding(obj: object) -> CanonicalBindingView:
    label = "canonical_bindings.<id>"
    record = _record_keys(obj, _CANONICAL_BINDING_KEYS, label)
    status = _schema_str(record, "status", label)
    if status not in (BINDING_PENDING, BINDING_COMMITTED):
        raise ProjectionSchemaError(
            f"{label}.status has unknown canonical binding state {status!r}."
        )
    return CanonicalBindingView(
        artifact_id=_schema_str(record, "artifact_id", label),
        status=status,
        updated_at=_schema_str(record, "updated_at", label),
    )


def _decode_snapshot_binding(obj: object) -> SnapshotBindingView:
    label = "snapshot_binding"
    record = _record_keys(obj, _SNAPSHOT_BINDING_KEYS, label)
    return SnapshotBindingView(
        snapshot_id=_schema_str(record, "snapshot_id", label),
        bound_at=_schema_str(record, "bound_at", label),
    )


def _decode_section(
    obj: object, section: str, id_field: str, decode_one
) -> Mapping[str, object]:
    if not isinstance(obj, Mapping):
        raise ProjectionSchemaError(f"{section} must be a JSON object.")
    decoded: dict[str, object] = {}
    for key, value in obj.items():
        record = decode_one(value)
        if getattr(record, id_field) != key:
            raise ProjectionSchemaError(
                f"{section} key {key!r} does not match the recorded "
                f"{id_field} {getattr(record, id_field)!r}."
            )
        decoded[key] = record
    return decoded


# Record field name sets (serialized shape == the frozen dataclass fields).
_CASE_BINDING_KEYS = frozenset(
    {
        "case_id",
        "charter_identity",
        "charter_digest",
        "source_declaration_identity",
        "source_declaration_digest",
    }
)
_EXECUTION_BINDING_KEYS = frozenset(
    {
        "workflow_identity",
        "workflow_version",
        "runtime_configuration_identity",
        "prompts",
        "schemas",
    }
)
_COMPATIBILITY_KEYS = frozenset(
    {
        "workflow_identity",
        "workflow_version",
        "step_identity",
        "step_version",
        "runtime_configuration_identity",
        "prompt_identity",
        "prompt_version",
        "schema_identity",
        "schema_version",
    }
)
_REVIEW_TARGET_KEYS = frozenset({"step_id", "attempt_id", "artifact_ids"})
_REVISION_TARGET_KEYS = frozenset({"entry_step", "reason"})
_RUN_KEYS = frozenset(
    {
        "run_id",
        "case_id",
        "case_binding",
        "state",
        "cumulative_execution_scope",
        "current_invocation_id",
        "completion_reason",
        "runtime_schema_version",
    }
)
_INVOCATION_KEYS = frozenset(
    {
        "invocation_id",
        "run_id",
        "requested_scope",
        "entry_mode",
        "execution_binding",
        "status",
        "from_step",
        "until_step",
        "completion_reason",
        "runtime_schema_version",
    }
)
_ATTEMPT_KEYS = frozenset(
    {
        "attempt_id",
        "run_id",
        "invocation_id",
        "step_id",
        "status",
        "input_binding_id",
        "runtime_schema_version",
    }
)
_INPUT_BINDING_KEYS = frozenset(
    {
        "input_binding_id",
        "run_id",
        "invocation_id",
        "step_id",
        "attempt_id",
        "artifact_ids",
        "upstream_attempt_ids",
    }
)
_GATE_KEYS = frozenset(
    {
        "gate_id",
        "run_id",
        "logical_gate_id",
        "review_target",
        "decision",
        "created_at",
        "reviewer",
        "decided_at",
        "comment",
        "revision_target",
        "supersedes",
        "superseded_by",
    }
)
_CHECKPOINT_KEYS = frozenset(
    {
        "checkpoint_id",
        "run_id",
        "step_id",
        "artifact_ids",
        "compatibility",
        "created_at",
        "status",
    }
)
_ARTIFACT_REFERENCE_KEYS = frozenset(
    {
        "artifact_id",
        "digest",
        "invocation_id",
        "step_id",
        "attempt_id",
        "committed_at",
    }
)
_CANONICAL_BINDING_KEYS = frozenset(
    {"artifact_id", "status", "updated_at"}
)
_SNAPSHOT_BINDING_KEYS = frozenset({"snapshot_id", "bound_at"})


def parse_projection(document: Mapping[str, object]) -> tuple[RunProjection, int, str]:
    """Parse a run.json document into (projection, projection_version,
    updated_at). Unknown document schema versions fail fast."""
    if not isinstance(document, Mapping):
        raise ProjectionSchemaError("run.json must be a JSON object.")
    unknown = set(document) - set(_DOC_KEYS)
    if unknown:
        raise ProjectionSchemaError(
            f"run.json carries unknown top-level fields {sorted(unknown)}."
        )
    missing = set(_DOC_KEYS) - set(document)
    if missing:
        raise ProjectionSchemaError(
            f"run.json is missing top-level fields {sorted(missing)}."
        )
    root = document["runtime_schema_version"]
    if type(root) is not int or root != RUNTIME_SCHEMA_VERSION:
        raise ProjectionSchemaError(
            f"run.json uses unknown runtime_schema_version {root!r}; only "
            f"{RUNTIME_SCHEMA_VERSION} is supported in v1."
        )
    version = document["projection_version"]
    if type(version) is not int or version < 1:
        raise ProjectionSchemaError(
            "run.json projection_version must be an int >= 1 "
            f"(got {version!r})."
        )
    updated_at = document["updated_at"]
    if not isinstance(updated_at, str) or not updated_at:
        raise ProjectionSchemaError(
            "run.json updated_at must be a non-empty string."
        )
    dispositions = document["failure_dispositions"]
    if not isinstance(dispositions, Mapping) or not all(
        isinstance(key, str) and key
        and isinstance(value, str) and value
        for key, value in dispositions.items()
    ):
        raise ProjectionSchemaError(
            "run.json failure_dispositions must map attempt ids to "
            "non-empty disposition strings."
        )
    projection = _construct(
        "run.json",
        RunProjection,
        run=_decode_run(document["run"]),
        invocations=_decode_section(
            document["invocations"], "invocations", "invocation_id", _decode_invocation
        ),
        attempts=_decode_section(
            document["attempts"], "attempts", "attempt_id", _decode_attempt
        ),
        failure_dispositions=dict(dispositions),
        input_bindings=_decode_section(
            document["input_bindings"],
            "input_bindings",
            "input_binding_id",
            _decode_input_binding,
        ),
        gates=_decode_section(document["gates"], "gates", "gate_id", _decode_gate),
        checkpoints=_decode_section(
            document["checkpoints"],
            "checkpoints",
            "checkpoint_id",
            _decode_checkpoint,
        ),
        artifacts=_decode_section(
            document["artifacts"], "artifacts", "artifact_id", _decode_artifact_reference
        ),
        canonical_bindings=_decode_section(
            document["canonical_bindings"],
            "canonical_bindings",
            "artifact_id",
            _decode_canonical_binding,
        ),
        snapshot_binding=(
            _decode_snapshot_binding(document["snapshot_binding"])
            if document["snapshot_binding"] is not None
            else None
        ),
    )
    return projection, version, updated_at
