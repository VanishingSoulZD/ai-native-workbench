"""Control-plane event envelope and vocabulary for the Research Runtime.

Events are immutable facts that have happened (Spec section 10); they never
carry command intent. ``execution.jsonl`` will be the authoritative execution
history, with one ``EventEnvelope`` per line; the envelope here is the shared
shape every event type uses.

``EventEnvelope`` construction enforces the envelope shape (types, non-empty
ids, mapping payload, frozen payload). ``validate_event`` is the public schema
gate used by load/reconciliation paths: it rejects unknown event types,
unknown ``schema_version`` values (only int 1 is supported in v1, Spec 18.2)
and malformed envelopes. Construction deliberately permits
``schema_version != 1`` so that load paths may construct-then-validate, which
is why the version check lives in ``validate_event``.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType

EVENT_SCHEMA_VERSION = 1
"""Current Event schema version (Spec 18.2); unknown versions fail fast."""


class EventSchemaError(Exception):
    """Raised when an event violates the event schema contract."""


class EventType(str, Enum):
    """The full v1 event vocabulary (Spec section 10).

    Values mirror the Spec tokens verbatim. Every member records a fact that
    has happened; there is no command-intent member.
    """

    RUN_CREATED = "RUN_CREATED"
    INVOCATION_STARTED = "INVOCATION_STARTED"
    ATTEMPT_CREATED = "ATTEMPT_CREATED"
    INPUT_BOUND = "INPUT_BOUND"
    ATTEMPT_STARTED = "ATTEMPT_STARTED"
    ARTIFACT_COMMITTED = "ARTIFACT_COMMITTED"
    VALIDATION_COMPLETED = "VALIDATION_COMPLETED"
    ACCEPTANCE_RECORDED = "ACCEPTANCE_RECORDED"
    GATE_CREATED = "GATE_CREATED"
    GATE_DECIDED = "GATE_DECIDED"
    GATE_SUPERSEDED = "GATE_SUPERSEDED"
    ATTEMPT_SUCCEEDED = "ATTEMPT_SUCCEEDED"
    ATTEMPT_FAILED = "ATTEMPT_FAILED"
    CHECKPOINT_CREATED = "CHECKPOINT_CREATED"
    CHECKPOINT_INVALIDATED = "CHECKPOINT_INVALIDATED"
    CANONICAL_BINDING_PENDING = "CANONICAL_BINDING_PENDING"
    CANONICAL_BINDING_COMMITTED = "CANONICAL_BINDING_COMMITTED"
    SNAPSHOT_BOUND = "SNAPSHOT_BOUND"
    INVOCATION_COMPLETED = "INVOCATION_COMPLETED"
    RUN_STATE_CHANGED = "RUN_STATE_CHANGED"


def _require_text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EventSchemaError(f"event {name} must be a non-empty string.")


def _require_optional_text(value: object, name: str) -> None:
    if value is not None:
        _require_text(value, name)


def _deep_freeze(value: object) -> object:
    """Recursively freeze mappings and sequences into immutable equivalents."""
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: _deep_freeze(item) for key, item in value.items()}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class EventEnvelope:
    """The lightweight common event envelope (Spec section 10)."""

    event_id: str
    event_type: EventType
    timestamp: str
    run_id: str
    schema_version: int = EVENT_SCHEMA_VERSION
    invocation_id: str | None = None
    step_id: str | None = None
    attempt_id: str | None = None
    artifact_id: str | None = None
    gate_id: str | None = None
    payload: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.event_id, "event_id")
        if not isinstance(self.event_type, EventType):
            raise EventSchemaError(
                f"event event_type {self.event_type!r} is not a known EventType."
            )
        _require_text(self.timestamp, "timestamp")
        _require_text(self.run_id, "run_id")
        if type(self.schema_version) is not int:
            raise EventSchemaError(
                f"event schema_version must be an int (got {self.schema_version!r})."
            )
        for name in (
            "invocation_id",
            "step_id",
            "attempt_id",
            "artifact_id",
            "gate_id",
        ):
            _require_optional_text(getattr(self, name), name)
        if not isinstance(self.payload, Mapping):
            raise EventSchemaError("event payload must be a mapping.")
        object.__setattr__(self, "payload", _deep_freeze(self.payload))


def validate_event(event: EventEnvelope) -> None:
    """Validate that *event* conforms to the current event schema.

    Raises EventSchemaError for unknown event types, unknown (non-1)
    ``schema_version`` values, empty event_id/run_id/timestamp and malformed
    payloads. Used by event-log load and reconciliation paths so unknown
    schema versions fail fast (Spec 10.2/18.2).
    """
    if not isinstance(event, EventEnvelope):
        raise EventSchemaError(f"validate_event requires an EventEnvelope (got {event!r}).")
    if not isinstance(event.event_type, EventType):
        raise EventSchemaError(
            f"event event_type {event.event_type!r} is not a known EventType."
        )
    if event.schema_version != EVENT_SCHEMA_VERSION:
        raise EventSchemaError(
            f"event {event.event_id} uses unknown schema_version "
            f"{event.schema_version}; only {EVENT_SCHEMA_VERSION} is supported in v1."
        )
    _require_text(event.event_id, "event_id")
    _require_text(event.timestamp, "timestamp")
    _require_text(event.run_id, "run_id")
    for name in (
        "invocation_id",
        "step_id",
        "attempt_id",
        "artifact_id",
        "gate_id",
    ):
        _require_optional_text(getattr(event, name), name)
    if not isinstance(event.payload, Mapping):
        raise EventSchemaError(f"event {event.event_id} payload must be a mapping.")
