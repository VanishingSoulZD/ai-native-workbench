"""Public domain surface of the Research Runtime.

Task 1 contracts: immutable Run/Invocation/Attempt records with pure
transition methods, bindings, artifact envelope, input binding, human gate
records, checkpoints, the event envelope/vocabulary and the domain errors.
"""

from .events import (
    EVENT_SCHEMA_VERSION,
    EventEnvelope,
    EventSchemaError,
    EventType,
    validate_event,
)
from .models import (
    RUNTIME_SCHEMA_VERSION,
    SNAPSHOT_MARKER,
    ArtifactEnvelope,
    AttemptRecord,
    AttemptStatus,
    CaseBinding,
    CheckpointRecord,
    CheckpointStatus,
    CompatibilityIdentity,
    EntryMode,
    ExecutionBinding,
    ExecutionScope,
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
    utc_now,
)

__all__ = [
    "AttemptRecord",
    "AttemptStatus",
    "CaseBinding",
    "CheckpointRecord",
    "CheckpointStatus",
    "CompatibilityIdentity",
    "EVENT_SCHEMA_VERSION",
    "EntryMode",
    "EventEnvelope",
    "EventSchemaError",
    "EventType",
    "ExecutionBinding",
    "ExecutionScope",
    "GateDecision",
    "GateRecord",
    "InputBinding",
    "InvocationRecord",
    "InvocationStatus",
    "RUNTIME_SCHEMA_VERSION",
    "RevisionTarget",
    "ReviewTarget",
    "RunRecord",
    "RunState",
    "RuntimeContractError",
    "SNAPSHOT_MARKER",
    "utc_now",
    "validate_event",
]
