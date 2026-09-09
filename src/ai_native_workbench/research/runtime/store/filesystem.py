"""Durable filesystem-backed runtime store (Spec 11, Task 2).

Layout (per Run)::

    <root>/cases/<case_id>/runs/<run_id>/
        run.json            rebuildable projection (Spec 11.2)
        execution.jsonl     authoritative event history (one event per line)
        artifacts/<artifact_id>/artifact.json

Semantics implemented here:

- ``execution.jsonl`` is authoritative; ``run.json`` is a versioned,
  rebuildable projection refreshed on every append. Store handles are
  per-instance caches (fresh store instances mirror process restarts).
- ``append_event`` guards every append: schema validation, ``event_id``
  idempotency (identical re-append is a no-op; reuse with a different payload
  raises ``EventConflictError``), and a reduce-before-append simulation so a
  new event that contradicts the reduced history is rejected before anything
  is written (Ruling 11). Duplicate logical facts with fresh ids fail the
  same way.
- Artifact documents are residue until their ARTIFACT_COMMITTED event is
  durably in the owning run's log (Ruling 4): pre-commit documents may be
  overwritten; committed documents are immutable and digest-checked on every
  read. Residue never surfaces through ``load_artifact`` or the projection.
- Run/artifact documents each declare ``runtime_schema_version: 1`` at their
  root; unknown schema versions fail fast before any interpretation.

Concurrency: v1 is single-process and sequential. Writes are atomic-ish
(temp file + ``os.replace``); there is no cross-process locking, so
concurrent writers to one Run are outside the v1 contract.
"""

import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..domain import (
    RUNTIME_SCHEMA_VERSION,
    ArtifactEnvelope,
    EventEnvelope,
    EventSchemaError,
    EventType,
    RunRecord,
    RunState,
    RuntimeContractError,
    utc_now,
)
from .events import EventConflictError, EventLog
from .projection import (
    ProjectionSchemaError,
    RunProjection,
    parse_projection,
    reduce_events,
    serialize_projection,
)


class RunNotFoundError(Exception):
    """Raised when a Run is unknown to this store (no run.json / no log)."""


class RunAlreadyExistsError(Exception):
    """Raised by create_run when a Run with the id already exists."""


class ArtifactNotFoundError(Exception):
    """Raised when an artifact is not a committed artifact of this Run."""


class EvidenceIntegrityError(Exception):
    """Raised when durable evidence violates an integrity contract.

    Covers strict decode failures, digest mismatches between the commit
    event and the artifact document, run_id mismatches and unknown artifact
    document schema versions.
    """


class RuntimeStore(Protocol):
    """The runtime store API surface (brief Step 3)."""

    def create_run(self, run: RunRecord) -> None: ...

    def load_run(self, run_id: str) -> RunRecord: ...

    def save_projection(self, run: RunRecord) -> None: ...

    def append_event(self, event: EventEnvelope) -> bool: ...

    def save_artifact(self, artifact: ArtifactEnvelope) -> None: ...

    def load_artifact(self, artifact_id: str) -> ArtifactEnvelope: ...

    def events(self, run_id: str) -> tuple[EventEnvelope, ...]: ...


@dataclass(frozen=True)
class _RunHandle:
    """Per-instance cache of one Run's log and projection state."""

    directory: Path
    log: EventLog
    projection_version: int


def _atomic_write(path: Path, text: str) -> None:
    """Write *text* through a temp file + os.replace (no partial documents)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


class FileSystemRuntimeStore:
    """Filesystem-backed RuntimeStore rooted at *root* (see module docstring)."""

    def __init__(self, root: str | os.PathLike[str]) -> None:
        self._root = Path(root)
        self._handles: dict[str, _RunHandle] = {}

    @property
    def root(self) -> Path:
        return self._root

    # -- run lifecycle -------------------------------------------------------

    def create_run(self, run: RunRecord) -> None:
        """Create the durable layout for a new Run and append RUN_CREATED.

        Raises RuntimeContractError unless the Run is still CREATED and
        RunAlreadyExistsError when the Run already exists (run.json present
        or a non-empty execution log).
        """
        if run.state is not RunState.CREATED:
            raise RuntimeContractError(
                f"create_run requires a CREATED run (got {run.state.value})."
            )
        directory = self._run_directory(run.case_id, run.run_id)
        if directory.exists():
            if (directory / "run.json").exists():
                raise RunAlreadyExistsError(
                    f"run {run.run_id} already exists (run.json present)."
                )
            log_path = directory / "execution.jsonl"
            if log_path.exists() and log_path.read_text(encoding="utf-8") != "":
                raise RunAlreadyExistsError(
                    f"run {run.run_id} already exists (event log is not empty)."
                )
        directory.mkdir(parents=True, exist_ok=True)
        log = EventLog(directory / "execution.jsonl", run.run_id)
        created = EventEnvelope(
            event_id=f"evt-{uuid.uuid4().hex}",
            event_type=EventType.RUN_CREATED,
            timestamp=utc_now(),
            run_id=run.run_id,
            payload={
                "case_id": run.case_binding.case_id,
                "charter_identity": run.case_binding.charter_identity,
                "charter_digest": run.case_binding.charter_digest,
                "source_declaration_identity": (
                    run.case_binding.source_declaration_identity
                ),
                "source_declaration_digest": (
                    run.case_binding.source_declaration_digest
                ),
            },
        )
        log.append(created)
        handle = _RunHandle(directory=directory, log=log, projection_version=0)
        self._handles[run.run_id] = handle
        self._refresh_projection(run.run_id)

    def load_run(self, run_id: str) -> RunRecord:
        """Read and parse run.json; return its RunRecord.

        Raises RunNotFoundError when the projection document is missing (the
        read path never guesses; reconciliation is the repair authority) and
        ProjectionSchemaError for documents violating the v1 schema.
        """
        directory = self._find_run_directory(run_id)
        if directory is None:
            raise RunNotFoundError(f"run {run_id} does not exist.")
        document_path = directory / "run.json"
        if not document_path.exists():
            raise RunNotFoundError(
                f"run {run_id} has no run.json projection; reconcile first."
            )
        try:
            document = json.loads(document_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProjectionSchemaError(
                f"run.json of run {run_id} is not valid JSON: {exc}"
            ) from exc
        projection, _version, _updated_at = parse_projection(document)
        return projection.run

    def save_projection(self, run: RunRecord) -> None:
        """Re-reduce the event history and write run.json from *run*.

        Raises RuntimeContractError when *run* differs from the reduced
        state: the projection document is always derived from events, never
        patched from a caller's stale view.
        """
        reduced = reduce_events(self.events(run.run_id))
        if reduced.run != run:
            raise RuntimeContractError(
                f"save_projection run {run.run_id} does not match the "
                "reduced event history; run.json is derived from events only."
            )
        self._write_projection(run.run_id)

    # -- event append --------------------------------------------------------

    def append_event(self, event: EventEnvelope) -> bool:
        """Durably append *event* to the owning Run's log (guarded).

        Returns False when the identical event is already recorded. Raises
        EventConflictError when the event_id is reused with a different
        payload or when the reduced history rejects the event (duplicate
        logical fact or contradiction), and RunNotFoundError for unknown
        runs.
        """
        handle = self._open_handle(event.run_id)
        existing = handle.log.get(event.event_id)
        if existing is not None:
            if existing == event:
                return False
            raise EventConflictError(
                f"event_id {event.event_id} is already recorded in run "
                f"{event.run_id} with a different payload."
            )
        try:
            reduce_events(handle.log.events + (event,))
        except RuntimeContractError as exc:
            raise EventConflictError(
                f"event {event.event_id} contradicts the recorded history "
                f"of run {event.run_id}: {exc}"
            ) from exc
        handle.log.append(event)
        self._refresh_projection(event.run_id)
        return True

    def events(self, run_id: str) -> tuple[EventEnvelope, ...]:
        """Return the authoritative event history of *run_id*, in order."""
        return self._open_handle(run_id).log.events

    # -- artifact documents ---------------------------------------------------

    def save_artifact(self, artifact: ArtifactEnvelope) -> None:
        """Write the artifact document for *artifact*.

        Pre-commit documents are residue and may be overwritten; once the
        owning run's log records the ARTIFACT_COMMITTED event the document
        is immutable: re-saving the identical envelope is a no-op and any
        other write raises RuntimeContractError.
        """
        run_id = artifact.run_id
        handle = self._open_handle(run_id)
        committed = self._commit_event(handle, artifact.artifact_id)
        path = handle.directory / "artifacts" / artifact.artifact_id / "artifact.json"
        if committed is not None:
            existing = self._read_artifact_document(path, run_id)
            if existing == artifact:
                return
            raise RuntimeContractError(
                f"artifact {artifact.artifact_id} is already committed; "
                "artifact documents are immutable after their commit event."
            )
        _atomic_write(path, json.dumps(_encode_artifact_document(artifact)))

    def load_artifact(self, artifact_id: str) -> ArtifactEnvelope:
        """Load a committed artifact.

        Residue never surfaces (Ruling 4): an artifact document without its
        ARTIFACT_COMMITTED event raises ArtifactNotFoundError, as does an
        unknown artifact id. Committed documents are strictly decoded and
        digest-checked against the commit event; violations raise
        EvidenceIntegrityError.
        """
        for directory in self._all_run_directories():
            run_id = directory.name
            cached = self._handles.get(run_id)
            log = cached.log if cached is not None else self._log_for_directory(directory)
            commit = self._commit_event_in_log(log, artifact_id)
            if commit is None:
                continue
            path = directory / "artifacts" / artifact_id / "artifact.json"
            if not path.exists():
                raise EvidenceIntegrityError(
                    f"artifact {artifact_id} has commit event {commit.event_id} "
                    f"in run {log.run_id} but its document is missing; "
                    "durable evidence is never silently dropped."
                )
            envelope = self._read_artifact_document(path, log.run_id)
            if commit.payload.get("digest") != envelope.digest:
                raise EvidenceIntegrityError(
                    f"artifact {artifact_id} document digest "
                    f"{envelope.digest!r} does not match the digest "
                    f"{commit.payload.get('digest')!r} recorded by commit "
                    f"event {commit.event_id}."
                )
            return envelope
        raise ArtifactNotFoundError(
            f"artifact {artifact_id} is not a committed artifact of any "
            "known run."
        )

    # -- internal helpers ------------------------------------------------------

    def _log_for_directory(self, directory: Path) -> EventLog:
        """Return the EventLog for *directory* (fresh reads; no handle use).

        Used by artifact lookups so committed-ness is always decided from the
        durable log, not from a cached handle.
        """
        run_id = directory.name
        return EventLog(directory / "execution.jsonl", run_id)

    def _commit_event(
        self, handle: _RunHandle, artifact_id: str
    ) -> EventEnvelope | None:
        return self._commit_event_in_log(handle.log, artifact_id)

    @staticmethod
    def _commit_event_in_log(
        log: EventLog, artifact_id: str
    ) -> EventEnvelope | None:
        for event in log.events:
            if (
                event.event_type is EventType.ARTIFACT_COMMITTED
                and event.artifact_id == artifact_id
            ):
                return event
        return None

    def _read_artifact_document(self, path: Path, run_id: str) -> ArtifactEnvelope:
        """Strictly decode one artifact document (integrity-checked)."""
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise EvidenceIntegrityError(
                f"artifact document {path} is not valid JSON: {exc}"
            ) from exc
        if not isinstance(document, dict):
            raise EvidenceIntegrityError(
                f"artifact document {path} must be a JSON object."
            )
        if document.get("runtime_schema_version") != RUNTIME_SCHEMA_VERSION:
            raise EvidenceIntegrityError(
                f"artifact document {path} uses unknown runtime_schema_version "
                f"{document.get('runtime_schema_version')!r}; only "
                f"{RUNTIME_SCHEMA_VERSION} is supported in v1."
            )
        record = document.get("artifact")
        if not isinstance(record, dict):
            raise EvidenceIntegrityError(
                f"artifact document {path} must carry an 'artifact' record."
            )
        envelope = _decode_artifact_record(record, str(path))
        if envelope.run_id != run_id:
            raise EvidenceIntegrityError(
                f"artifact document {path} belongs to run {envelope.run_id}, "
                f"not run {run_id}."
            )
        return envelope

    # -- handle / directory resolution -----------------------------------------

    def _open_handle(self, run_id: str) -> _RunHandle:
        """Return the per-instance handle for *run_id*, opening it when needed.

        Opening reads run.json first (schema fail-fast) and then loads the
        event log. Unknown runs raise RunNotFoundError.
        """
        cached = self._handles.get(run_id)
        if cached is not None:
            return cached
        directory = self._find_run_directory(run_id)
        if directory is None:
            raise RunNotFoundError(f"run {run_id} does not exist.")
        self._validate_projection_document(directory, run_id)
        log = EventLog(directory / "execution.jsonl", run_id)
        handle = _RunHandle(
            directory=directory, log=log, projection_version=self._read_version(directory)
        )
        self._handles[run_id] = handle
        return handle

    def _run_directory(self, case_id: str, run_id: str) -> Path:
        return self._root / "cases" / case_id / "runs" / run_id

    def _find_run_directory(self, run_id: str) -> Path | None:
        """Locate the run directory of *run_id* under any case (glob).

        run_id is a runtime-wide execution identity, so its run directory is
        unique; more than one match is an integrity failure.
        """
        candidates = sorted((self._root / "cases").glob(f"*/runs/{run_id}"))
        if not candidates:
            return None
        if len(candidates) > 1:
            raise RuntimeContractError(
                f"run {run_id} exists under multiple cases: "
                f"{[str(c) for c in candidates]}."
            )
        return candidates[0]

    def _all_run_directories(self) -> tuple[Path, ...]:
        cases = self._root / "cases"
        if not cases.is_dir():
            return ()
        directories: list[Path] = []
        for runs in sorted(cases.glob("*/runs")):
            for run_dir in sorted(runs.iterdir()):
                if run_dir.is_dir():
                    directories.append(run_dir)
        return tuple(directories)

    def _validate_projection_document(self, directory: Path, run_id: str) -> None:
        """Parse run.json when present so unknown schemas fail fast.

        A missing run.json is legal (the projection was lost in a crash;
        reconciliation rebuilds it from events). An *unreadable* run.json —
        invalid JSON or a future schema version — always fails fast: the
        store never interprets a document it cannot prove is v1.
        """
        path = directory / "run.json"
        if not path.exists():
            return
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProjectionSchemaError(
                f"run.json of run {run_id} is not valid JSON: {exc}"
            ) from exc
        parse_projection(document)

    def _read_version(self, directory: Path) -> int:
        """Read the recorded projection_version (0 when no document exists)."""
        path = directory / "run.json"
        if not path.exists():
            return 0
        document = json.loads(path.read_text(encoding="utf-8"))
        version = document["projection_version"]
        return version if isinstance(version, int) else 0

    def _refresh_projection(self, run_id: str) -> None:
        self._write_projection(run_id)

    def _write_projection(self, run_id: str) -> None:
        """Rebuild run.json from the authoritative event history."""
        handle = self._handles[run_id]
        projection = reduce_events(handle.log.events)
        handle = _RunHandle(
            directory=handle.directory,
            log=handle.log,
            projection_version=handle.projection_version + 1,
        )
        self._handles[run_id] = handle
        document = serialize_projection(
            projection, handle.projection_version, updated_at=utc_now()
        )
        _atomic_write(handle.directory / "run.json", json.dumps(document))


# ---------------------------------------------------------------------------
# Artifact document codec (root runtime_schema_version=1 + 11-field record)
# ---------------------------------------------------------------------------

_ARTIFACT_DOCUMENT_FIELDS = (
    "artifact_id",
    "run_id",
    "invocation_id",
    "artifact_schema_id",
    "artifact_schema_version",
    "created_at",
    "step_id",
    "attempt_id",
    "digest",
    "provenance",
    "payload",
)


def _jsonable(value: object) -> object:
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _encode_artifact_document(artifact: ArtifactEnvelope) -> dict[str, object]:
    return {
        "runtime_schema_version": RUNTIME_SCHEMA_VERSION,
        "artifact": {
            name: _jsonable(getattr(artifact, name))
            for name in _ARTIFACT_DOCUMENT_FIELDS
        },
    }


def _artifact_text(document: dict[str, object], name: str, label: str) -> str:
    value = document.get(name)
    if not isinstance(value, str) or not value:
        raise EvidenceIntegrityError(f"{label}.{name} must be a non-empty string.")
    return value


def _artifact_optional_text(
    document: dict[str, object], name: str, label: str
) -> str | None:
    value = document.get(name)
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise EvidenceIntegrityError(
            f"{label}.{name} must be a string or null."
        )
    return value


def _artifact_id_tuple(
    document: dict[str, object], name: str, label: str
) -> tuple[str, ...]:
    value = document.get(name, [])
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise EvidenceIntegrityError(
            f"{label}.{name} must be a list of non-empty strings."
        )
    return tuple(value)


def _decode_artifact_record(record: dict[str, object], label: str) -> ArtifactEnvelope:
    unknown = set(record) - set(_ARTIFACT_DOCUMENT_FIELDS)
    if unknown:
        raise EvidenceIntegrityError(
            f"artifact document {label} carries unknown fields "
            f"{sorted(unknown)}; only the v1 envelope shape is supported."
        )
    try:
        return ArtifactEnvelope(
            artifact_id=_artifact_text(record, "artifact_id", label),
            run_id=_artifact_text(record, "run_id", label),
            invocation_id=_artifact_text(record, "invocation_id", label),
            artifact_schema_id=_artifact_text(record, "artifact_schema_id", label),
            artifact_schema_version=_artifact_text(
                record, "artifact_schema_version", label
            ),
            created_at=_artifact_text(record, "created_at", label),
            step_id=_artifact_optional_text(record, "step_id", label),
            attempt_id=_artifact_optional_text(record, "attempt_id", label),
            digest=_artifact_optional_text(record, "digest", label),
            provenance=_artifact_id_tuple(record, "provenance", label),
            payload=record.get("payload"),
        )
    except RuntimeContractError as exc:
        raise EvidenceIntegrityError(
            f"artifact document {label} violates the envelope contract: {exc}"
        ) from exc
