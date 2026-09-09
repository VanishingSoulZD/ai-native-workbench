"""Tests for the runtime event envelope, event vocabulary, and validation."""

from dataclasses import FrozenInstanceError, replace

import pytest

from ai_native_workbench.research.runtime import (
    EVENT_SCHEMA_VERSION,
    EventEnvelope,
    EventSchemaError,
    EventType,
    validate_event,
)

TS = "2026-09-09T00:00:00+00:00"

SPEC_VOCABULARY = {
    "RUN_CREATED",
    "INVOCATION_STARTED",
    "ATTEMPT_CREATED",
    "INPUT_BOUND",
    "ATTEMPT_STARTED",
    "ARTIFACT_COMMITTED",
    "VALIDATION_COMPLETED",
    "ACCEPTANCE_RECORDED",
    "GATE_CREATED",
    "GATE_DECIDED",
    "GATE_SUPERSEDED",
    "ATTEMPT_SUCCEEDED",
    "ATTEMPT_FAILED",
    "CHECKPOINT_CREATED",
    "CHECKPOINT_INVALIDATED",
    "CANONICAL_BINDING_PENDING",
    "CANONICAL_BINDING_COMMITTED",
    "SNAPSHOT_BOUND",
    "INVOCATION_COMPLETED",
    "RUN_STATE_CHANGED",
}


def make_event(**overrides) -> EventEnvelope:
    return replace(
        EventEnvelope(
            event_id="evt-1",
            event_type=EventType.RUN_CREATED,
            timestamp=TS,
            run_id="run-1",
            payload={"state": "CREATED"},
        ),
        **overrides,
    )


def test_event_rejects_unknown_schema_version():
    event = make_event(schema_version=2)
    with pytest.raises(EventSchemaError):
        validate_event(event)


def test_event_accepts_current_schema_version():
    event = make_event()
    assert event.schema_version == EVENT_SCHEMA_VERSION == 1
    assert validate_event(event) is None


def test_event_type_vocabulary_matches_the_spec_list():
    assert {member.name for member in EventType} == SPEC_VOCABULARY
    # Facts, not command intent: every member is a past-tense record.
    assert EventType.RUN_CREATED.value == "RUN_CREATED"


def test_event_rejects_non_integer_schema_version_at_construction():
    with pytest.raises(EventSchemaError):
        make_event(schema_version="1")
    with pytest.raises(EventSchemaError):
        make_event(schema_version=True)


def test_event_requires_event_id_and_run_id():
    with pytest.raises(EventSchemaError):
        make_event(event_id="")
    with pytest.raises(EventSchemaError):
        make_event(run_id="")
    with pytest.raises(EventSchemaError):
        make_event(event_id=123)


def test_event_timestamp_is_required():
    with pytest.raises(EventSchemaError):
        make_event(timestamp="")


def test_event_rejects_unknown_event_type():
    with pytest.raises(EventSchemaError):
        make_event(event_type="NOT_AN_EVENT")


def test_event_lineage_ids_are_optional_but_non_empty_when_present():
    event = make_event(
        invocation_id="inv-1",
        step_id="R1",
        attempt_id="att-1",
        artifact_id="art-1",
        gate_id="gate-1",
    )
    assert event.invocation_id == "inv-1"
    assert event.step_id == "R1"
    assert event.attempt_id == "att-1"
    assert event.artifact_id == "art-1"
    assert event.gate_id == "gate-1"
    with pytest.raises(EventSchemaError):
        make_event(invocation_id="")


def test_event_payload_must_be_a_mapping():
    with pytest.raises(EventSchemaError):
        make_event(payload=["not", "a", "mapping"])
    with pytest.raises(EventSchemaError):
        make_event(payload=None)


def test_event_payload_is_immutable():
    event = make_event(
        payload={"state": "RUNNING", "nested": {"attempt_id": "att-1"}}
    )
    with pytest.raises(TypeError):
        event.payload["state"] = "COMPLETED"
    with pytest.raises(TypeError):
        event.payload["nested"]["attempt_id"] = "att-2"


def test_event_envelope_is_frozen():
    event = make_event()
    with pytest.raises(FrozenInstanceError):
        event.event_type = EventType.RUN_STATE_CHANGED
    with pytest.raises(FrozenInstanceError):
        event.payload = {}


def test_validate_event_detects_unknown_schema_version_zero():
    event = make_event(schema_version=0)
    with pytest.raises(EventSchemaError):
        validate_event(event)
