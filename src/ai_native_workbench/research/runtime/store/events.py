"""Durable append-only event log for one Run (``execution.jsonl``).

The log is the authoritative execution history (Spec section 11): one
``EventEnvelope`` per JSON line, append-only, never rewritten except for the
two sanctioned startup repairs in this module — truncation of a partial
trailing line (a crash mid-append never durably landed, Ruling 11) and
normalizing a missing final newline. Mid-file corruption or duplicate
``event_id`` values are fail-fast ``EventLogError`` conditions, and unknown
event schema versions / unknown run ids raise ``EventSchemaError`` at load
and append so a future-format log is never interpreted.

Append semantics are idempotent per ``event_id``: re-appending the identical
event is a no-op (returns ``False``), while reusing an ``event_id`` with a
different payload raises ``EventConflictError``. Duplicate *logical* facts
with fresh ids are prevented by the store's reduce-before-append guard, not
by this class.
"""

import json
import os
from collections.abc import Mapping
from pathlib import Path

from ..domain import (
    EventEnvelope,
    EventSchemaError,
    EventType,
    validate_event,
)

_ENVELOPE_FIELDS = (
    "event_id",
    "event_type",
    "schema_version",
    "timestamp",
    "run_id",
    "invocation_id",
    "step_id",
    "attempt_id",
    "artifact_id",
    "gate_id",
    "payload",
)


class EventLogError(Exception):
    """Raised when the on-disk log is corrupt beyond startup repair."""


class EventConflictError(Exception):
    """Raised when an append reuses an ``event_id`` with a different payload."""


def _jsonable(value: object) -> object:
    """Recursively convert frozen payload values to JSON-serializable ones."""
    if isinstance(value, Mapping):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def encode_line(event: EventEnvelope) -> str:
    """Serialize one event to a single JSONL line (no trailing newline)."""
    document = {name: _jsonable(getattr(event, name)) for name in _ENVELOPE_FIELDS}
    document["event_type"] = event.event_type.value
    return json.dumps(document, ensure_ascii=False)


def decode_line(line: str, run_id: str) -> EventEnvelope:
    """Parse and validate one JSONL line as an event for *run_id*.

    Raises EventLogError for unparseable text (on-disk corruption) and
    EventSchemaError for valid JSON that violates the event schema (unknown
    schema versions, unknown event types, wrong run, unknown fields).
    """
    try:
        document = json.loads(line)
    except json.JSONDecodeError as exc:
        raise EventLogError(f"unparseable event log line: {exc}") from exc
    if not isinstance(document, dict):
        raise EventSchemaError("event log lines must be JSON objects.")
    unknown = set(document) - set(_ENVELOPE_FIELDS)
    if unknown:
        raise EventSchemaError(
            f"event log line carries unknown fields {sorted(unknown)}; "
            "only the v1 envelope is supported."
        )
    for name in ("event_id", "event_type", "timestamp", "run_id", "payload"):
        if name not in document:
            raise EventSchemaError(f"event log line is missing {name!r}.")
    try:
        event_type = EventType(document["event_type"])
    except ValueError as exc:
        raise EventSchemaError(
            f"event log line names unknown event type "
            f"{document['event_type']!r}."
        ) from exc
    kwargs = dict(document)
    kwargs["event_type"] = event_type
    try:
        envelope = EventEnvelope(**kwargs)
    except TypeError as exc:
        raise EventSchemaError(f"malformed event log line: {exc}") from exc
    validate_event(envelope)
    if envelope.run_id != run_id:
        raise EventSchemaError(
            f"event {envelope.event_id} belongs to run {envelope.run_id}, "
            f"not run {run_id}."
        )
    return envelope


class EventLog:
    """The durable, append-only event history of one Run.

    Constructing a log performs the startup read: partial trailing lines are
    truncated (they never durably landed), mid-file corruption and duplicate
    event ids fail fast, and every surviving line is schema-validated.
    """

    def __init__(self, path: str | os.PathLike[str], run_id: str) -> None:
        self._path = Path(path)
        self._run_id = run_id
        self._events: tuple[EventEnvelope, ...] = ()
        self._by_id: dict[str, EventEnvelope] = {}
        self._load()

    @property
    def path(self) -> Path:
        return self._path

    @property
    def run_id(self) -> str:
        return self._run_id

    @property
    def events(self) -> tuple[EventEnvelope, ...]:
        """The loaded event history, in append order."""
        return self._events

    def get(self, event_id: str) -> EventEnvelope | None:
        """Return the recorded event with *event_id*, or None."""
        return self._by_id.get(event_id)

    def append(self, event: EventEnvelope) -> bool:
        """Durably append *event*; return False when it was already recorded.

        Raises EventSchemaError for schema violations and EventConflictError
        when an ``event_id`` is reused with a different payload.
        """
        validate_event(event)
        if event.run_id != self._run_id:
            raise EventSchemaError(
                f"event {event.event_id} belongs to run {event.run_id}, "
                f"not run {self._run_id}."
            )
        existing = self._by_id.get(event.event_id)
        if existing is not None:
            if existing == event:
                return False
            raise EventConflictError(
                f"event_id {event.event_id} is already recorded with a "
                "different payload."
            )
        self._ensure_trailing_newline()
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(encode_line(event) + "\n")
            handle.flush()
        self._events += (event,)
        self._by_id[event.event_id] = event
        return True

    # -- startup read / repair ------------------------------------------------

    def _load(self) -> None:
        """Read, validate and repair the log file (see module docstring)."""
        if not self._path.exists():
            return
        raw = self._path.read_text(encoding="utf-8")
        if raw == "":
            return
        if raw.endswith("\n"):
            lines = raw[:-1].split("\n")
            dropped_partial = False
        else:
            # The final chunk may be a crash mid-append. A JSON-unparseable
            # tail never durably landed, so it is truncated (Ruling 11). A
            # complete final line without a trailing newline is tolerated
            # (and normalized below); a parseable tail that violates the
            # event schema still fails fast.
            chunks = raw.split("\n")
            partial = chunks.pop()
            dropped_partial = True
            try:
                json.loads(partial)
            except json.JSONDecodeError:
                pass
            else:
                chunks.append(partial)
                dropped_partial = False
            lines = chunks
        events = [decode_line(line, self._run_id) for line in lines]
        by_id: dict[str, EventEnvelope] = {}
        for event in events:
            if event.event_id in by_id:
                raise EventLogError(
                    f"event log {self._path} contains duplicate event_id "
                    f"{event.event_id!r}."
                )
            by_id[event.event_id] = event
        if dropped_partial or not raw.endswith("\n"):
            # Startup repair: drop the partial tail and/or normalize the
            # missing final newline. Rewrites go through a temp file so a
            # crash mid-repair cannot corrupt the log.
            text = "".join(encode_line(event) + "\n" for event in events)
            temporary = self._path.with_name(
                f".{self._path.name}.{os.getpid()}.repair.tmp"
            )
            temporary.write_text(text, encoding="utf-8")
            os.replace(temporary, self._path)
        self._events = tuple(events)
        self._by_id = by_id

    def _ensure_trailing_newline(self) -> None:
        """Append a newline when the file ends mid-line or lacks one.

        A complete final line without a trailing newline is normalized at
        load; this guard covers files written by code outside this class.
        """
        if not self._path.exists():
            return
        with self._path.open("r", encoding="utf-8") as handle:
            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                return
            handle.seek(max(0, handle.tell() - 1))
            last = handle.read(1)
        if last != "\n":
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write("\n")
                handle.flush()
