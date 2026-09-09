"""Public package boundary of the Research Runtime (Step 6, v1).

Task 1 ships the domain contracts every later Runtime layer builds on:
immutable records, enums, bindings, the event envelope and the domain
errors. Keep this surface to what currently exists; later tasks extend it
as their public modules land.
"""

from .domain import (
    EVENT_SCHEMA_VERSION,
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
    EventEnvelope,
    EventSchemaError,
    EventType,
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
    validate_event,
)

__all__ = [
    "EVENT_SCHEMA_VERSION",
    "RUNTIME_SCHEMA_VERSION",
    "SNAPSHOT_MARKER",
    "ArtifactEnvelope",
    "AttemptRecord",
    "AttemptStatus",
    "CaseBinding",
    "CheckpointRecord",
    "CheckpointStatus",
    "CompatibilityIdentity",
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
    "RevisionTarget",
    "ReviewTarget",
    "RunRecord",
    "RunState",
    "RuntimeContractError",
    "utc_now",
    "validate_event",
]
