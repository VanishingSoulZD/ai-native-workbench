"""Tests for the durable execution.jsonl event log.

Covers append-only JSONL semantics, event_id idempotency and conflict
detection, schema/run-identity validation at load and append, and startup
truncation of a partial trailing line (Ruling 11).
"""

import json
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    EVENT_SCHEMA_VERSION,
    EventEnvelope,
    EventSchemaError,
    EventType,
)
from ai_native_workbench.research.runtime.store import (
    EventConflictError,
    EventLog,
    EventLogError,
)

TS = "2026-09-09T00:00:00+00:00"
RUN_ID = "run-1"


def make_event(**overrides) -> EventEnvelope:
    return replace(
        EventEnvelope(
            event_id="evt-1",
            event_type=EventType.RUN_CREATED,
            timestamp=TS,
            run_id=RUN_ID,
            payload={"state": "CREATED"},
        ),
        **overrides,
    )


def make_log(tmp_path) -> EventLog:
    return EventLog(tmp_path / "execution.jsonl", run_id=RUN_ID)


def read_lines(tmp_path):
    path = tmp_path / "execution.jsonl"
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()


def test_empty_log_has_no_events(tmp_path):
    log = make_log(tmp_path)
    assert log.events == ()


def test_append_persists_single_json_line_per_event(tmp_path):
    log = make_log(tmp_path)
    log.append(make_event(event_id="evt-1"))
    log.append(make_event(event_id="evt-2", event_type=EventType.ATTEMPT_CREATED))
    lines = read_lines(tmp_path)
    assert len(lines) == 2
    # Every line parses as one event envelope carrying schema_version=1.
    for line, event in zip(lines, log.events):
        assert json.loads(line)["event_id"] == event.event_id
        assert json.loads(line)["schema_version"] == EVENT_SCHEMA_VERSION


def test_append_and_reload_round_trip_in_order(tmp_path):
    log = make_log(tmp_path)
    events = (
        make_event(event_id="evt-1"),
        make_event(event_id="evt-2", event_type=EventType.ATTEMPT_CREATED),
        make_event(
            event_id="evt-3",
            event_type=EventType.ARTIFACT_COMMITTED,
            payload={"digest": "sha256:" + "d" * 64, "nested": {"k": [1, 2]}},
        ),
    )
    for event in events:
        assert log.append(event) is True
    # A fresh EventLog over the same file is the restart read path.
    reloaded = make_log(tmp_path)
    assert reloaded.events == events


def test_duplicate_event_id_is_idempotent(tmp_path):
    log = make_log(tmp_path)
    event = make_event()
    assert log.append(event) is True
    assert log.append(event) is False  # identical content -> no-op
    assert log.events == (event,)
    assert len(read_lines(tmp_path)) == 1


def test_same_event_id_with_different_payload_is_rejected(tmp_path):
    log = make_log(tmp_path)
    event = make_event()
    log.append(event)
    with pytest.raises(EventConflictError):
        log.append(replace(event, payload={"changed": True}))
    assert log.events == (event,)
    assert len(read_lines(tmp_path)) == 1


def test_append_validates_envelope_schema(tmp_path):
    log = make_log(tmp_path)
    with pytest.raises(EventSchemaError):
        log.append(make_event(schema_version=2))
    with pytest.raises(EventSchemaError):
        log.append(make_event(run_id="other-run"))
    assert log.events == ()


def test_load_rejects_unknown_event_schema_version(tmp_path):
    path = tmp_path / "execution.jsonl"
    line = json.dumps(
        {
            "event_id": "evt-x",
            "event_type": "RUN_CREATED",
            "schema_version": 2,
            "timestamp": TS,
            "run_id": RUN_ID,
            "payload": {},
        }
    )
    path.write_text(line + "\n", encoding="utf-8")
    with pytest.raises(EventSchemaError):
        make_log(tmp_path)


def test_load_rejects_unknown_event_type_token(tmp_path):
    path = tmp_path / "execution.jsonl"
    bad = json.dumps(
        {
            "event_id": "evt-x",
            "event_type": "NOT_A_FACT",
            "schema_version": 1,
            "timestamp": TS,
            "run_id": RUN_ID,
            "payload": {},
        }
    )
    path.write_text(bad + "\n", encoding="utf-8")
    with pytest.raises(EventSchemaError):
        make_log(tmp_path)


def test_load_rejects_event_for_another_run(tmp_path):
    path = tmp_path / "execution.jsonl"
    good = make_event(event_id="evt-1")
    other = json.dumps(
        {
            "event_id": "evt-2",
            "event_type": "RUN_CREATED",
            "schema_version": 1,
            "timestamp": TS,
            "run_id": "run-2",
            "payload": {},
        }
    )
    path.write_text(
        json.dumps(
            {
                "event_id": good.event_id,
                "event_type": good.event_type.value,
                "schema_version": good.schema_version,
                "timestamp": good.timestamp,
                "run_id": good.run_id,
                "payload": dict(good.payload),
            }
        )
        + "\n"
        + other
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(EventSchemaError):
        make_log(tmp_path)


def test_load_fails_on_mid_file_corruption(tmp_path):
    path = tmp_path / "execution.jsonl"
    good = make_event(event_id="evt-1")
    path.write_text(
        json.dumps(
            {
                "event_id": good.event_id,
                "event_type": good.event_type.value,
                "schema_version": good.schema_version,
                "timestamp": good.timestamp,
                "run_id": good.run_id,
                "payload": dict(good.payload),
            }
        )
        + "\n"
        + "this is not json\n"
        + "{\"also\": \"not a complete line\"",
        encoding="utf-8",
    )
    with pytest.raises(EventLogError):
        make_log(tmp_path)


def test_load_fails_on_duplicate_event_ids(tmp_path):
    path = tmp_path / "execution.jsonl"
    first = make_event(event_id="evt-1")
    line = json.dumps(
        {
            "event_id": "evt-1",
            "event_type": first.event_type.value,
            "schema_version": first.schema_version,
            "timestamp": first.timestamp,
            "run_id": first.run_id,
            "payload": dict(first.payload),
        }
    )
    path.write_text(line + "\n" + line + "\n", encoding="utf-8")
    with pytest.raises(EventLogError):
        make_log(tmp_path)


def test_load_truncates_partial_trailing_line(tmp_path):
    path = tmp_path / "execution.jsonl"
    event = make_event(event_id="evt-1")
    first = json.dumps(
        {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "schema_version": event.schema_version,
            "timestamp": event.timestamp,
            "run_id": event.run_id,
            "payload": dict(event.payload),
        }
    )
    # A crash mid-append leaves a partial final line without a trailing newline.
    path.write_text(first + "\n" + '{"event_id": "evt-2", "event_ty', encoding="utf-8")
    log = make_log(tmp_path)
    assert log.events == (event,)
    # The partial tail was truncated; the file now ends cleanly.
    content = path.read_text(encoding="utf-8")
    assert content.endswith("\n")
    assert len(content.splitlines()) == 1


def test_load_truncates_when_whole_file_is_a_partial_line(tmp_path):
    path = tmp_path / "execution.jsonl"
    path.write_text('{"event_id": "evt', encoding="utf-8")
    log = make_log(tmp_path)
    assert log.events == ()
    assert path.read_text(encoding="utf-8") == ""


def test_append_after_truncation_persists_cleanly(tmp_path):
    path = tmp_path / "execution.jsonl"
    first = make_event(event_id="evt-1")
    line = json.dumps(
        {
            "event_id": first.event_id,
            "event_type": first.event_type.value,
            "schema_version": first.schema_version,
            "timestamp": first.timestamp,
            "run_id": first.run_id,
            "payload": dict(first.payload),
        }
    )
    path.write_text(line + "\n" + '{"broken', encoding="utf-8")
    log = make_log(tmp_path)
    second = make_event(event_id="evt-2", event_type=EventType.ATTEMPT_CREATED)
    log.append(second)
    assert log.events == (first, second)
    content = path.read_text(encoding="utf-8")
    assert content.endswith("\n")
    assert len(content.splitlines()) == 2


def test_load_tolerates_missing_final_newline_on_complete_line(tmp_path):
    path = tmp_path / "execution.jsonl"
    event = make_event(event_id="evt-1")
    path.write_text(
        json.dumps(
            {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "schema_version": event.schema_version,
                "timestamp": event.timestamp,
                "run_id": event.run_id,
                "payload": dict(event.payload),
            }
        ),
        encoding="utf-8",
    )
    log = make_log(tmp_path)
    assert log.events == (event,)
    # A later append still keeps single-line-per-event JSONL.
    log.append(make_event(event_id="evt-2", event_type=EventType.ATTEMPT_CREATED))
    assert len(read_lines(tmp_path)) == 2
