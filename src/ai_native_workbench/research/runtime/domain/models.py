"""Immutable domain records for the Research Runtime v1.

Records in this module are frozen and validated in ``__post_init__``. They
expose only pure transition methods that return new records: calling
``run.start()`` never mutates ``run``. Guards embedded in the records protect
domain invariants (an Attempt cannot become RUNNING without a durable input
binding; a Run cannot go CREATED -> COMPLETED directly). Authority over *who
may invoke* a transition (start/resume/retry/rerun) belongs to the Runtime
control layer, not to these records.

Enum values mirror the Spec tokens verbatim (Spec sections 5, 6, 10, 13) so
persisted projections and event payloads stay directly readable.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType


class RuntimeContractError(Exception):
    """Raised when a runtime domain record violates a contract invariant."""


RUNTIME_SCHEMA_VERSION = 1
"""Version of independent runtime persistence documents (Spec section 18.1)."""

SNAPSHOT_MARKER = "SNAPSHOT"
"""Literal scope marker for the snapshot freeze point.

ResearchSnapshot creation is a Runtime-managed freeze operation, not a
Workflow Step (Spec section 14.2), so its scope entry is this literal string
rather than a workflow step id.
"""

# ExecutionScope is the tuple of step ids ("R1", "R2", ...) an Invocation
# requests or a Run has cumulatively executed, plus the optional SNAPSHOT
# marker. Step ids are plain strings; snapshot is never a workflow step.
ExecutionScope = tuple[str, ...]


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _require_text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeContractError(f"{name} must be a non-empty string.")


def _require_optional_text(value: object, name: str) -> None:
    if value is not None:
        _require_text(value, name)


def _require_enum(value: object, kind: type[Enum], name: str) -> None:
    if not isinstance(value, kind):
        raise RuntimeContractError(f"{name} must be a {kind.__name__}.")


def _require_schema_version(value: object) -> None:
    if type(value) is not int or value != RUNTIME_SCHEMA_VERSION:
        raise RuntimeContractError(
            f"runtime_schema_version must be the int {RUNTIME_SCHEMA_VERSION}."
        )


def _require_id_tuple(value: object, name: str, *, allow_empty: bool) -> None:
    if not isinstance(value, tuple):
        raise RuntimeContractError(f"{name} must be a tuple of strings.")
    if not allow_empty and not value:
        raise RuntimeContractError(f"{name} must not be empty.")
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise RuntimeContractError(f"{name} entries must be non-empty strings.")
        if item in seen:
            raise RuntimeContractError(f"{name} must not contain duplicates.")
        seen.add(item)


def _require_mapping(value: object, name: str) -> None:
    if not isinstance(value, Mapping):
        raise RuntimeContractError(f"{name} must be a mapping.")


def _validate_scope(value: object, name: str, *, allow_empty: bool) -> tuple[str, ...]:
    _require_id_tuple(value, name, allow_empty=allow_empty)
    return value


def _merge_scope(existing: tuple[str, ...], additional: tuple[str, ...]) -> tuple[str, ...]:
    """Append steps not already recorded; prior history is never erased."""
    return existing + tuple(step for step in additional if step not in existing)


def utc_now() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class RunState(str, Enum):
    """The six primary Run states (Spec section 6.1)."""

    CREATED = "CREATED"
    RUNNING = "RUNNING"
    WAITING_FOR_HUMAN = "WAITING_FOR_HUMAN"
    NEEDS_REVISION = "NEEDS_REVISION"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class InvocationStatus(str, Enum):
    """Invocation status is intentionally small (Spec section 5.2)."""

    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"


class EntryMode(str, Enum):
    """The control action that created this Invocation (Spec sections 6.4/15).

    ``start``, ``resume``, ``--from`` and ``--until`` each create a new
    Invocation; ``retry`` and ``rerun`` stay inside the current Invocation and
    therefore never produce an EntryMode of their own.
    """

    START = "START"
    RESUME = "RESUME"
    FROM = "FROM"
    UNTIL = "UNTIL"


class AttemptStatus(str, Enum):
    """Attempt execution states only (Spec section 5.4).

    Candidate/Validation/Acceptance are separate result evidence and are
    intentionally not part of this enum.
    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"


class GateDecision(str, Enum):
    """Human Gate decision states (Spec section 13.2)."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class CheckpointStatus(str, Enum):
    """Checkpoint lifecycle is a simple two-value flag.

    Checkpoints never serialize process state and never carry a Gate-style
    state machine (Spec section 12).
    """

    VALID = "VALID"
    INVALIDATED = "INVALIDATED"


# ---------------------------------------------------------------------------
# Bindings
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CaseBinding:
    """Case Definition inputs frozen at Run creation (Spec sections 5.1/16.1).

    Later modifications to the Case do not mutate a Run bound through this
    record. Digest format (e.g. ``sha256:<64 hex>``) is owned by the binding
    loader; the record requires only non-empty identities/digests.
    """

    case_id: str
    charter_identity: str
    charter_digest: str
    source_declaration_identity: str
    source_declaration_digest: str

    def __post_init__(self) -> None:
        for name in (
            "case_id",
            "charter_identity",
            "charter_digest",
            "source_declaration_identity",
            "source_declaration_digest",
        ):
            _require_text(getattr(self, name), name)


@dataclass(frozen=True)
class ExecutionBinding:
    """Execution configuration frozen at Invocation creation (Spec 16.2).

    ``prompts`` and ``schemas`` map each frozen identity to its digest
    (identity -> digest). A workflow may legitimately declare no prompts or
    no schemas, so both default to empty mappings.
    """

    workflow_identity: str
    workflow_version: str
    runtime_configuration_identity: str
    prompts: Mapping[str, str] = field(default_factory=dict)
    schemas: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "workflow_identity",
            "workflow_version",
            "runtime_configuration_identity",
        ):
            _require_text(getattr(self, name), name)
        object.__setattr__(self, "prompts", self._freeze_identity_map(self.prompts, "prompts"))
        object.__setattr__(self, "schemas", self._freeze_identity_map(self.schemas, "schemas"))

    @staticmethod
    def _freeze_identity_map(value: object, name: str) -> MappingProxyType[str, str]:
        _require_mapping(value, name)
        frozen: dict[str, str] = {}
        for identity, digest in value.items():
            _require_text(identity, f"{name} key")
            _require_text(digest, f"{name} digest for {identity!r}")
            frozen[identity] = digest
        return MappingProxyType(frozen)


@dataclass(frozen=True)
class CompatibilityIdentity:
    """The exact-match identity tuple for checkpoint reuse (Spec section 12).

    ``prompt`` and ``schema`` identities apply per step only "when
    applicable", so each must appear as a full (identity, version) pair or
    not at all. Compatibility is deliberately exact: no fuzzy or semantic
    checks exist in v1.
    """

    workflow_identity: str
    workflow_version: str
    step_identity: str
    step_version: str
    runtime_configuration_identity: str
    prompt_identity: str | None = None
    prompt_version: str | None = None
    schema_identity: str | None = None
    schema_version: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "workflow_identity",
            "workflow_version",
            "step_identity",
            "step_version",
            "runtime_configuration_identity",
        ):
            _require_text(getattr(self, name), name)
        _require_optional_text(self.prompt_identity, "prompt_identity")
        _require_optional_text(self.prompt_version, "prompt_version")
        _require_optional_text(self.schema_identity, "schema_identity")
        _require_optional_text(self.schema_version, "schema_version")
        if (self.prompt_identity is None) != (self.prompt_version is None):
            raise RuntimeContractError(
                "prompt_identity and prompt_version must be set together or not at all."
            )
        if (self.schema_identity is None) != (self.schema_version is None):
            raise RuntimeContractError(
                "schema_identity and schema_version must be set together or not at all."
            )


# ---------------------------------------------------------------------------
# Run / Invocation / Attempt
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunRecord:
    """The long-lived execution identity for one Case execution (Spec 5.1)."""

    run_id: str
    case_id: str
    case_binding: CaseBinding
    state: RunState
    cumulative_execution_scope: ExecutionScope
    current_invocation_id: str | None
    completion_reason: str | None
    runtime_schema_version: int = RUNTIME_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.run_id, "run_id")
        _require_text(self.case_id, "case_id")
        if not isinstance(self.case_binding, CaseBinding):
            raise RuntimeContractError("case_binding must be a CaseBinding.")
        _require_enum(self.state, RunState, "state")
        _validate_scope(
            self.cumulative_execution_scope, "cumulative_execution_scope", allow_empty=True
        )
        _require_optional_text(self.current_invocation_id, "current_invocation_id")
        _require_optional_text(self.completion_reason, "completion_reason")
        _require_schema_version(self.runtime_schema_version)

    # -- transitions (Spec section 6.1) ------------------------------------

    def start(self) -> "RunRecord":
        """CREATED -> RUNNING."""
        self._require_state(RunState.CREATED, "start")
        return replace(self, state=RunState.RUNNING)

    def wait_for_human(self) -> "RunRecord":
        """RUNNING -> WAITING_FOR_HUMAN."""
        self._require_state(RunState.RUNNING, "wait_for_human")
        return replace(self, state=RunState.WAITING_FOR_HUMAN)

    def mark_running(self) -> "RunRecord":
        """WAITING_FOR_HUMAN -> RUNNING after a Gate resolves without revision."""
        self._require_state(RunState.WAITING_FOR_HUMAN, "mark_running")
        return replace(self, state=RunState.RUNNING)

    def needs_revision(self, completion_reason: str | None = None) -> "RunRecord":
        """RUNNING -> NEEDS_REVISION (human rejection only, Spec 6.3).

        The authoritative revision reason lives in the rejecting Gate record,
        so the Run-level reason is optional.
        """
        self._require_state(RunState.RUNNING, "needs_revision")
        _require_optional_text(completion_reason, "completion_reason")
        return replace(self, state=RunState.NEEDS_REVISION, completion_reason=completion_reason)

    def fail(self, completion_reason: str) -> "RunRecord":
        """RUNNING -> FAILED with a required disposition (Spec sections 6.3/11.3)."""
        self._require_state(RunState.RUNNING, "fail")
        _require_text(completion_reason, "completion_reason")
        return replace(self, state=RunState.FAILED, completion_reason=completion_reason)

    def complete(
        self, completion_reason: str, execution_scope: ExecutionScope
    ) -> "RunRecord":
        """RUNNING -> COMPLETED for the given bounded scope (Spec 6.2).

        The given scope is merged into ``cumulative_execution_scope``;
        prior history is never erased. COMPLETED never by itself means the
        full lifecycle finished: consumers must inspect scope metadata.
        """
        self._require_state(RunState.RUNNING, "complete")
        _require_text(completion_reason, "completion_reason")
        scope = _validate_scope(execution_scope, "execution_scope", allow_empty=False)
        merged = _merge_scope(self.cumulative_execution_scope, scope)
        return replace(
            self,
            state=RunState.COMPLETED,
            completion_reason=completion_reason,
            cumulative_execution_scope=merged,
        )

    def begin_resume(self) -> "RunRecord":
        """Explicit resume: COMPLETED/NEEDS_REVISION/FAILED -> RUNNING.

        This is the only legal transition out of COMPLETED (Spec 6.1).
        Resuming starts a new phase, so completion metadata is cleared while
        cumulative scope history is preserved.
        """
        if self.state not in (RunState.COMPLETED, RunState.NEEDS_REVISION, RunState.FAILED):
            raise RuntimeContractError(
                f"Run {self.run_id} cannot resume from state {self.state.value}; "
                "explicit resume is legal only from COMPLETED, NEEDS_REVISION or FAILED."
            )
        return replace(self, state=RunState.RUNNING, completion_reason=None)

    def _require_state(self, expected: RunState, operation: str) -> None:
        if self.state is not expected:
            raise RuntimeContractError(
                f"Run {self.run_id} cannot {operation} from state {self.state.value}."
            )


@dataclass(frozen=True)
class InvocationRecord:
    """An immutable execution request boundary (Spec section 5.2).

    Requested scope, entry configuration and ExecutionBinding are frozen at
    creation; an Invocation is never rewritten to describe a later execution
    request. ``from_step``/``until_step`` and ``completion_reason`` are
    optional, so they appear after the required fields.
    """

    invocation_id: str
    run_id: str
    requested_scope: ExecutionScope
    entry_mode: EntryMode
    execution_binding: ExecutionBinding
    status: InvocationStatus
    from_step: str | None = None
    until_step: str | None = None
    completion_reason: str | None = None
    runtime_schema_version: int = RUNTIME_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.invocation_id, "invocation_id")
        _require_text(self.run_id, "run_id")
        _validate_scope(self.requested_scope, "requested_scope", allow_empty=False)
        _require_enum(self.entry_mode, EntryMode, "entry_mode")
        if not isinstance(self.execution_binding, ExecutionBinding):
            raise RuntimeContractError("execution_binding must be an ExecutionBinding.")
        _require_enum(self.status, InvocationStatus, "status")
        _require_optional_text(self.from_step, "from_step")
        _require_optional_text(self.until_step, "until_step")
        _require_optional_text(self.completion_reason, "completion_reason")
        _require_schema_version(self.runtime_schema_version)

    # -- transitions --------------------------------------------------------

    def succeed(self) -> "InvocationRecord":
        """RUNNING -> SUCCEEDED when the requested scope completes."""
        self._require_status(InvocationStatus.RUNNING, "succeed")
        return replace(self, status=InvocationStatus.SUCCEEDED)

    def fail(self, completion_reason: str) -> "InvocationRecord":
        """RUNNING -> FAILED with a required disposition (e.g. HUMAN_REJECTION)."""
        self._require_status(InvocationStatus.RUNNING, "fail")
        _require_text(completion_reason, "completion_reason")
        return replace(self, status=InvocationStatus.FAILED, completion_reason=completion_reason)

    def _require_status(self, expected: InvocationStatus, operation: str) -> None:
        if self.status is not expected:
            raise RuntimeContractError(
                f"Invocation {self.invocation_id} cannot {operation} "
                f"from status {self.status.value}."
            )


@dataclass(frozen=True)
class AttemptRecord:
    """One concrete execution instance of one Workflow Step (Spec 5.4)."""

    attempt_id: str
    run_id: str
    invocation_id: str
    step_id: str
    status: AttemptStatus
    input_binding_id: str | None = None
    runtime_schema_version: int = RUNTIME_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.attempt_id, "attempt_id")
        _require_text(self.run_id, "run_id")
        _require_text(self.invocation_id, "invocation_id")
        _require_text(self.step_id, "step_id")
        _require_enum(self.status, AttemptStatus, "status")
        _require_optional_text(self.input_binding_id, "input_binding_id")
        _require_schema_version(self.runtime_schema_version)

    # -- transitions (Spec sections 5.4/5.5) ---------------------------------

    def mark_running(self, input_binding_id: str | None = None) -> "AttemptRecord":
        """PENDING/FAILED -> RUNNING only with a durable input binding.

        Per Spec 5.5 the Runtime must persist the Input Binding before the
        Attempt enters RUNNING; ``retry`` stays within the same Attempt and
        therefore may re-enter RUNNING from FAILED with an explicit binding.
        """
        if input_binding_id is None:
            raise RuntimeContractError(
                f"Attempt {self.attempt_id} cannot become RUNNING without a "
                "durable input binding."
            )
        _require_text(input_binding_id, "input_binding_id")
        if self.status not in (AttemptStatus.PENDING, AttemptStatus.FAILED):
            raise RuntimeContractError(
                f"Attempt {self.attempt_id} cannot enter RUNNING from status "
                f"{self.status.value}."
            )
        return replace(self, status=AttemptStatus.RUNNING, input_binding_id=input_binding_id)

    def mark_succeeded(self) -> "AttemptRecord":
        """RUNNING -> SUCCEEDED (execution itself succeeded; Spec 5.4)."""
        if self.status is not AttemptStatus.RUNNING:
            raise RuntimeContractError(
                f"Attempt {self.attempt_id} can only succeed from RUNNING "
                f"(current status: {self.status.value})."
            )
        return replace(self, status=AttemptStatus.SUCCEEDED)

    def mark_failed(self) -> "AttemptRecord":
        """RUNNING -> FAILED (Spec 5.4/11.3).

        The Attempt record itself has no completion_reason field (its required
        field list carries only execution state); the failure disposition
        (e.g. EXECUTION_INTERRUPTED) is a fact of the ATTEMPT_FAILED event
        payload emitted by the control layer.
        """
        if self.status is not AttemptStatus.RUNNING:
            raise RuntimeContractError(
                f"Attempt {self.attempt_id} can only fail from RUNNING "
                f"(current status: {self.status.value})."
            )
        return replace(self, status=AttemptStatus.FAILED)


# ---------------------------------------------------------------------------
# Attempt Input Binding
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InputBinding:
    """The durable binding of an Attempt to its concrete inputs (Spec 5.5).

    Stores only concrete, already committed Artifact IDs plus the upstream
    Attempt lineage that produced them. Inputs are exact IDs resolved at
    binding time: there is no implicit "most recent output" resolution and
    no unresolved selector.
    """

    input_binding_id: str
    run_id: str
    invocation_id: str
    step_id: str
    attempt_id: str
    artifact_ids: tuple[str, ...] = ()
    upstream_attempt_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "input_binding_id",
            "run_id",
            "invocation_id",
            "step_id",
            "attempt_id",
        ):
            _require_text(getattr(self, name), name)
        # A step may legitimately have no upstream artifact inputs (e.g. the
        # first workflow step), so both lineage tuples may be empty.
        _require_id_tuple(self.artifact_ids, "artifact_ids", allow_empty=True)
        _require_id_tuple(self.upstream_attempt_ids, "upstream_attempt_ids", allow_empty=True)


# ---------------------------------------------------------------------------
# Artifact envelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArtifactEnvelope:
    """Uniform envelope for every Runtime-managed Artifact (Spec section 9).

    Runtime owns envelope identity, lineage, digest and lifecycle; payload
    semantics belong to the Executor or corresponding Core. Source-acquisition
    artifacts bind to an Invocation without a Workflow Attempt, so
    ``step_id``/``attempt_id`` are both ``None`` for them. The
    ``artifact_schema_id``/``artifact_schema_version`` pair describes the
    *payload* schema and is unrelated to ``runtime_schema_version``
    (Spec 18.3). ``digest`` is completed once at commit time (Task 3 owns the
    commit protocol); before commit the envelope is uncommitted residue and
    must never be used as a downstream input.
    """

    artifact_id: str
    run_id: str
    invocation_id: str
    artifact_schema_id: str
    artifact_schema_version: str
    created_at: str
    step_id: str | None = None
    attempt_id: str | None = None
    digest: str | None = None
    provenance: tuple[str, ...] = ()
    payload: object = None

    def __post_init__(self) -> None:
        for name in (
            "artifact_id",
            "run_id",
            "invocation_id",
            "artifact_schema_id",
            "artifact_schema_version",
            "created_at",
        ):
            _require_text(getattr(self, name), name)
        if (self.step_id is None) != (self.attempt_id is None):
            raise RuntimeContractError(
                "artifact step_id and attempt_id must be set together or both None "
                "(source-acquisition artifacts have no Workflow Attempt)."
            )
        _require_optional_text(self.step_id, "step_id")
        _require_optional_text(self.attempt_id, "attempt_id")
        _require_optional_text(self.digest, "digest")
        _require_id_tuple(self.provenance, "provenance", allow_empty=True)

    def with_digest(self, digest: str) -> "ArtifactEnvelope":
        """Return a copy with the digest completed (the commit operation).

        An Artifact is immutable after commit: the digest may only be
        completed once, from an uncommitted envelope.
        """
        if self.digest is not None:
            raise RuntimeContractError(
                f"Artifact {self.artifact_id} is already committed "
                f"(digest {self.digest}); digests are completed exactly once."
            )
        _require_text(digest, "digest")
        return replace(self, digest=digest)


# ---------------------------------------------------------------------------
# Human Gate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReviewTarget:
    """The concrete Artifact/Candidate Set a Gate binds to (Spec 13.1).

    A Gate never binds merely to a Step or Attempt: it names the exact
    candidates under review, so the artifact set must be non-empty.
    """

    step_id: str
    attempt_id: str
    artifact_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.step_id, "step_id")
        _require_text(self.attempt_id, "attempt_id")
        _require_id_tuple(self.artifact_ids, "artifact_ids", allow_empty=False)


@dataclass(frozen=True)
class RevisionTarget:
    """Minimum re-execution boundary requested by a rejected Gate (Spec 6.5/13.3)."""

    entry_step: str
    reason: str

    def __post_init__(self) -> None:
        _require_text(self.entry_step, "entry_step")
        _require_text(self.reason, "reason")


@dataclass(frozen=True)
class GateRecord:
    """An immutable Human Gate review fact (Spec section 13).

    ``supersedes``/``superseded_by`` record an immutable relational link to
    another Gate ID (Spec 13.2); supersession is a relationship, never a new
    Gate state. Decided facts are whole-set APPROVE/REJECT; partial approval
    is out of scope for v1.
    """

    gate_id: str
    run_id: str
    logical_gate_id: str
    review_target: ReviewTarget
    decision: GateDecision
    created_at: str
    reviewer: str | None = None
    decided_at: str | None = None
    comment: str | None = None
    revision_target: RevisionTarget | None = None
    supersedes: str | None = None
    superseded_by: str | None = None

    def __post_init__(self) -> None:
        for name in ("gate_id", "run_id", "logical_gate_id", "created_at"):
            _require_text(getattr(self, name), name)
        if not isinstance(self.review_target, ReviewTarget):
            raise RuntimeContractError("review_target must be a ReviewTarget.")
        _require_enum(self.decision, GateDecision, "decision")
        _require_optional_text(self.reviewer, "reviewer")
        _require_optional_text(self.decided_at, "decided_at")
        _require_optional_text(self.comment, "comment")
        if self.revision_target is not None and not isinstance(
            self.revision_target, RevisionTarget
        ):
            raise RuntimeContractError("revision_target must be a RevisionTarget.")
        if self.decision is GateDecision.PENDING:
            if self.reviewer is not None or self.decided_at is not None:
                raise RuntimeContractError(
                    f"Pending gate {self.gate_id} cannot carry reviewer/decided_at."
                )
        else:
            if self.reviewer is None or self.decided_at is None:
                raise RuntimeContractError(
                    f"Gate {self.gate_id} decision {self.decision.value} requires "
                    "reviewer and decided_at."
                )
        if self.revision_target is not None and self.decision is not GateDecision.REJECTED:
            raise RuntimeContractError(
                f"Gate {self.gate_id} carries a revision_target but its decision "
                f"is {self.decision.value}; only REJECTED gates request revision."
            )
        for name in ("supersedes", "superseded_by"):
            value = getattr(self, name)
            if value is not None:
                _require_text(value, name)
                if value == self.gate_id:
                    raise RuntimeContractError(
                        f"Gate {self.gate_id} cannot {name} itself."
                    )

    def decide(
        self,
        decision: GateDecision,
        reviewer: str,
        decided_at: str,
        comment: str | None = None,
        revision_target: RevisionTarget | None = None,
    ) -> "GateRecord":
        """Record the whole-set decision on this still-PENDING gate."""
        if self.decision is not GateDecision.PENDING:
            raise RuntimeContractError(
                f"Gate {self.gate_id} is already decided ({self.decision.value}); "
                "review facts are immutable."
            )
        if decision not in (GateDecision.APPROVED, GateDecision.REJECTED):
            raise RuntimeContractError(
                f"Gate {self.gate_id} decision must be APPROVED or REJECTED."
            )
        if revision_target is not None and decision is not GateDecision.REJECTED:
            raise RuntimeContractError(
                f"Gate {self.gate_id} can only carry a revision_target when REJECTED."
            )
        return replace(
            self,
            decision=decision,
            reviewer=reviewer,
            decided_at=decided_at,
            comment=comment if comment is not None else self.comment,
            revision_target=revision_target,
        )

    def mark_superseded_by(self, gate_id: str) -> "GateRecord":
        """Record that this Gate is superseded by a newer-path Gate (13.2).

        Supersession is a single immutable relationship: it can only be set
        once, never on itself.
        """
        if self.superseded_by is not None:
            raise RuntimeContractError(
                f"Gate {self.gate_id} is already superseded by {self.superseded_by}."
            )
        _require_text(gate_id, "gate_id")
        if gate_id == self.gate_id:
            raise RuntimeContractError(f"Gate {self.gate_id} cannot supersede itself.")
        return replace(self, superseded_by=gate_id)


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CheckpointRecord:
    """A durable input-context set for a later Step boundary (Spec 12).

    Checkpoint reuse requires exact compatibility of the recorded
    ``CompatibilityIdentity``; a checkpoint never serializes process state.
    """

    checkpoint_id: str
    run_id: str
    step_id: str
    artifact_ids: tuple[str, ...]
    compatibility: CompatibilityIdentity
    created_at: str
    status: CheckpointStatus = CheckpointStatus.VALID

    def __post_init__(self) -> None:
        for name in ("checkpoint_id", "run_id", "step_id", "created_at"):
            _require_text(getattr(self, name), name)
        _require_id_tuple(self.artifact_ids, "artifact_ids", allow_empty=False)
        if not isinstance(self.compatibility, CompatibilityIdentity):
            raise RuntimeContractError("compatibility must be a CompatibilityIdentity.")
        _require_enum(self.status, CheckpointStatus, "status")

    def invalidate(self) -> "CheckpointRecord":
        """VALID -> INVALIDATED (default when a logical Step is rerun, Spec 12)."""
        if self.status is not CheckpointStatus.VALID:
            raise RuntimeContractError(
                f"Checkpoint {self.checkpoint_id} is already {self.status.value}."
            )
        return replace(self, status=CheckpointStatus.INVALIDATED)
