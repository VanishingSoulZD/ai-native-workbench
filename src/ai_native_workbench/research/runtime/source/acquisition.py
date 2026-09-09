"""Source Acquisition for the Research Runtime v1 (Task 5, Spec section 8).

Source Acquisition happens before R1 and is a Runtime capability, never a
research lifecycle number. The input is the Case's frozen ``inputs/urls.yaml``
(Ruling 3): only those declared URLs may ever be fetched — there is no
autonomous source discovery. Because a Run freezes its Case identity and
declaration digests at creation (Spec 16.1), acquisition entry re-verifies the
loaded Case's declaration identity/digest against the Run's ``case_binding``
before anything is parsed, fetched, reused or written: a urls.yaml edited on
disk after Run creation is refused under that Run — Case changes affect new
Runs only. The module is layered so each concern stays separable and
testable:

* :mod:`declaration layer <parse_source_declarations>` — parses and validates
  the constrained urls.yaml subset (list items ``- id: <source id>`` with
  two-space-indented ``url:`` and optional ``required:`` keys) with explicit,
  line-numbered :class:`SourceDeclarationError` failures. The parser is a
  documented subset, not a general YAML engine: anything outside the subset
  (unknown keys, unsupported schemes, malformed URLs, duplicate ids) is an
  explicit error naming its line, never a silent skip.
* :mod:`transport layer <HttpFetcher>` — standard-library HTTP retrieval
  (urllib) with bounded reads (:class:`FetchError` ``OVERSIZED``), redirect
  following and final-URL reporting. Tests inject fakes behind the
  :class:`Fetcher` protocol; the integration suite runs a real local HTTP
  server, so acquisition is semantically real with no internet dependency.
* :mod:`persistence layer <SourceAcquisitionService.acquire>` — commits each
  successfully acquired source as a Run-scoped immutable Source Artifact
  (Spec 8) through the Task 3 commit protocol with no Workflow Attempt
  (``step_id``/``attempt_id`` both ``None``, Spec 9), preserving raw content
  and retrieval metadata, and reuses committed Source Artifacts during
  retry/rerun/resume within the same Run.

Failure policy (architecture 11.3) is delivered as a result, not an
exception: a required-source failure returns a blocked
:class:`AcquisitionResult` naming the disposition, an optional-source
failure is recorded in the result and processing continues, and unsupported
or oversized acquisition is an explicit per-source failure. Durable
persistence of the dispositions themselves is the orchestrator's concern —
v1 owns no event type for them, so the service never invents one. Fetched
content is preserved as raw bytes (digested with the runtime ``sha256:``
scheme) plus a decoded ``text`` form where the media type is supported.
"""

import socket
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable

from ..artifacts import commit_artifact
from ..binding import ResearchCase
from ..digests import sha256_digest
from ..domain import (
    ArtifactEnvelope,
    EventType,
    RunRecord,
    RunState,
    RuntimeContractError,
    utc_now,
)
from ..store import RunNotFoundError, RuntimeStore
# Documented bound of the constrained urls.yaml subset.
SOURCE_ID_PATTERN = "letters, digits, '.', '_' and '-' only"
SUPPORTED_SCHEMES = ("http", "https")

DEFAULT_MAX_BYTES = 5 * 1024 * 1024
"""Default per-source content bound (architecture: oversized is explicit)."""

DEFAULT_TIMEOUT_SECONDS = 15.0
"""Default socket timeout for declared-URL retrieval."""

_FETCH_CHUNK_BYTES = 64 * 1024
_SOURCE_SCHEMA_ID = "source-artifact"
_SOURCE_SCHEMA_VERSION = "1"
_TEXT_MEDIA_PREFIX = "text/"
_JSONISH_MEDIA_TYPES = frozenset(
    {
        "application/json",
        "application/xml",
        "application/xhtml+xml",
        "application/javascript",
        "application/x-javascript",
    }
)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class SourceDeclarationError(RuntimeContractError):
    """Raised when the Case's frozen declarations violate the subset.

    Declaration validation happens once, before anything is fetched, and a
    violation aborts the whole acquisition: an invalid declaration can never
    be treated as a per-source retrieval failure.
    """


class AcquisitionError(RuntimeContractError):
    """Raised when an acquisition request violates the Runtime contract.

    Covers non-record arguments, a Run that is not RUNNING, a Case/Run
    mismatch, a Case whose source declaration identity/digest drifted from
    the declaration frozen into the Run's CaseBinding at creation (Spec
    16.1), a frozen-declaration digest inconsistency and an unknown Run.
    Per-source *retrieval* failures are never raised: they are recorded in
    the AcquisitionResult with their disposition (architecture 11.3).
    """


# ---------------------------------------------------------------------------
# Declaration layer: constrained urls.yaml parsing and validation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceDeclaration:
    """One validated source-selection entry of the Case's urls.yaml."""

    source_id: str
    url: str
    required: bool


def parse_source_declarations(text: str) -> tuple[SourceDeclaration, ...]:
    """Parse and validate the constrained urls.yaml subset.

    Accepted shape (blank lines allowed between entries)::

        - id: <source id>
          url: <http(s) url>
          required: true   # optional; default false

    Every violation raises SourceDeclarationError with the offending line
    number and the reason — malformed URLs, duplicate source ids,
    unsupported schemes, non-boolean ``required`` values, unknown keys and
    out-of-subset content are all explicit. The declaration order of the
    frozen text is preserved.
    """
    if not isinstance(text, str):
        raise SourceDeclarationError(
            f"source declarations must be text, got {text!r}."
        )
    declarations: list[SourceDeclaration] = []
    start_lines: list[int] = []
    seen_ids: dict[str, int] = {}
    current: dict = {}
    current_keys: set[str] = set()

    def fail(line: int, message: str) -> None:
        raise SourceDeclarationError(f"urls.yaml line {line}: {message}")

    def finish_item(line: int) -> None:
        nonlocal current, current_keys
        if current["url"] is None:
            fail(line, f"source {current['source_id']!r} declares no 'url'.")
        source_id = current["source_id"]
        if source_id in seen_ids:
            fail(
                start_lines[-1],
                f"duplicate source id {source_id!r} (first declared on "
                f"line {seen_ids[source_id]}); source ids must be unique.",
            )
        seen_ids[source_id] = start_lines[-1]
        declarations.append(
            SourceDeclaration(
                source_id=source_id,
                url=current["url"],
                required=current["required"],
            )
        )
        current = {}
        current_keys = set()

    for index, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip():
            continue
        if raw_line.startswith("- id:"):
            if current:
                finish_item(index)
            source_id = raw_line[len("- id:"):].strip()
            if not source_id:
                fail(index, "source id must not be empty.")
            if not _is_valid_source_id(source_id):
                fail(
                    index,
                    f"invalid source id {source_id!r}: ids allow {SOURCE_ID_PATTERN}.",
                )
            current = {
                "source_id": source_id,
                "url": None,
                "required": False,
            }
            current_keys = set()
            start_lines.append(index)
            continue
        if raw_line.startswith("  url:"):
            if not current:
                fail(index, f"'url:' outside a source entry: {raw_line!r}")
            if "url" in current_keys:
                fail(index, "duplicate 'url' key for one source entry.")
            value = raw_line[len("  url:"):].strip()
            if not value:
                fail(index, "the declared url must not be empty.")
            url = _validate_url(value, index)
            current["url"] = url
            current_keys.add("url")
            continue
        if raw_line.startswith("  required:"):
            if not current:
                fail(index, f"'required:' outside a source entry: {raw_line!r}")
            if "required" in current_keys:
                fail(index, "duplicate 'required' key for one source entry.")
            value = raw_line[len("  required:"):].strip()
            if value.lower() not in ("true", "false"):
                fail(
                    index,
                    f"required must be a boolean (true/false), got {value!r}.",
                )
            current["required"] = value.lower() == "true"
            current_keys.add("required")
            continue
        fail(
            index,
            "expected '- id: <source id>' or a two-space-indented "
            f"'url:'/'required:' entry, got {raw_line!r}.",
        )
    if current:
        finish_item(len(text.splitlines()) + 1)
    if not declarations:
        raise SourceDeclarationError(
            "urls.yaml declares no sources; a Case's source selection must "
            "name at least one declared URL."
        )
    return tuple(declarations)


def _is_valid_source_id(source_id: str) -> bool:
    return all(
        character.isalnum() or character in "._-" for character in source_id
    ) and not source_id.startswith(".")


def _validate_url(value: str, line: int) -> str:
    if any(character.isspace() for character in value):
        raise SourceDeclarationError(
            f"urls.yaml line {line}: malformed url {value!r}: urls must not "
            "contain whitespace."
        )
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in SUPPORTED_SCHEMES:
        raise SourceDeclarationError(
            f"urls.yaml line {line}: source declares unsupported url scheme "
            f"{parsed.scheme!r}: only http and https are fetchable in v1 "
            "(Spec 8: unsupported acquisition is an explicit failure)."
        )
    if not parsed.netloc or not parsed.hostname:
        raise SourceDeclarationError(
            f"urls.yaml line {line}: malformed url {value!r}: missing host."
        )
    return value


# ---------------------------------------------------------------------------
# Transport layer: stdlib HTTP retrieval behind a testable seam
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FetchResult:
    """A successful bounded retrieval: final response facts plus raw bytes."""

    status: int
    final_url: str
    content_type: str
    raw: bytes = b""


class FetchError(Exception):
    """A transport-level failure with an explicit disposition.

    Dispositions are the documented tokens of the failure policy: OVERSIZED
    (bounded read exceeded), HTTP_ERROR (non-success status, carries the
    status code) and UNREACHABLE (connection/DNS/timeout/protocol failure).
    """

    def __init__(
        self, disposition: str, detail: str, *, status: int | None = None
    ) -> None:
        super().__init__(detail)
        self.disposition = disposition
        self.detail = detail
        self.status = status


@runtime_checkable
class Fetcher(Protocol):
    """Transport seam: fetch one declared URL with bounded reads.

    Implementations follow redirects, enforce the byte bound themselves and
    raise FetchError for transport failures — a 2xx-or-raise contract.
    """

    def fetch(self, url: str) -> FetchResult: ...


class HttpFetcher:
    """Standard-library urllib retrieval with bounded, chunked reads.

    Redirects are followed by urllib's default handler (final URL reported
    in the result); the body is read in bounded chunks so an oversized
    response aborts with FetchError(OVERSIZED) instead of buffering it, and
    non-2xx or unreachable responses become explicit FetchError outcomes.
    """

    def __init__(
        self, *, max_bytes: int = DEFAULT_MAX_BYTES, timeout: float = DEFAULT_TIMEOUT_SECONDS
    ) -> None:
        if max_bytes <= 0:
            raise RuntimeContractError(
                f"max_bytes must be positive (got {max_bytes})."
            )
        self._max_bytes = max_bytes
        self._timeout = timeout

    def fetch(self, url: str) -> FetchResult:
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme not in SUPPORTED_SCHEMES:
            raise FetchError(
                "UNREACHABLE",
                f"refusing to fetch url with unsupported scheme "
                f"{parsed.scheme!r}.",
            )
        request = urllib.request.Request(
            url, headers={"User-Agent": "ai-native-workbench research-runtime v1"}
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                status = response.getcode()
                if status is None or not (200 <= status < 300):
                    raise FetchError(
                        "HTTP_ERROR",
                        f"HTTP {status} while fetching {url!r}.",
                        status=status,
                    )
                raw = self._read_bounded(response)
                content_type = response.headers.get("Content-Type", "")
                return FetchResult(
                    status=status,
                    final_url=response.geturl(),
                    content_type=content_type,
                    raw=raw,
                )
        except FetchError:
            raise
        except urllib.error.HTTPError as error:
            raise FetchError(
                "HTTP_ERROR",
                f"HTTP {error.code} {error.reason} while fetching {url!r}.",
                status=error.code,
            ) from error
        except urllib.error.URLError as error:
            raise FetchError(
                "UNREACHABLE", f"{error.reason} while fetching {url!r}."
            ) from error
        except (socket.timeout, TimeoutError) as error:
            raise FetchError(
                "UNREACHABLE", f"timed out after {self._timeout}s fetching {url!r}."
            ) from error
        except OSError as error:
            raise FetchError(
                "UNREACHABLE", f"connection failed ({error}) fetching {url!r}."
            ) from error

    def _read_bounded(self, response) -> bytes:
        chunks: list[bytes] = []
        remaining = self._max_bytes + 1
        while remaining > 0:
            chunk = response.read(min(_FETCH_CHUNK_BYTES, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        if len(raw) > self._max_bytes:
            raise FetchError(
                "OVERSIZED",
                f"response body exceeds the {self._max_bytes}-byte bound.",
            )
        return raw


# ---------------------------------------------------------------------------
# Persistence layer: acquisition records and the service
# ---------------------------------------------------------------------------


class SourceState(str, Enum):
    """Per-source acquisition outcome tokens (Spec 8, architecture 11.3)."""

    ACQUIRED = "ACQUIRED"
    REUSED = "REUSED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class SourceStatus:
    """The per-source outcome of one acquisition pass."""

    source_id: str
    url: str
    required: bool
    state: SourceState
    artifact_id: str | None = None
    digest: str | None = None
    disposition: str | None = None
    detail: str | None = None
    retrieved_at: str | None = None


@dataclass(frozen=True)
class AcquisitionResult:
    """The acquisition outcome for one Run, one declared source each status.

    ``blocked`` is derived: it is True exactly when a required source failed
    (Spec 8: required-source failure blocks research execution). All
    declarations are always processed, so optional failures never block and
    never stop later sources from being acquired. The orchestrator owns
    persisting the dispositions of FAILED statuses (v1 has no event type for
    them) and disposing of a blocked Run.
    """

    run_id: str
    case_id: str
    sources: tuple[SourceStatus, ...]

    @property
    def blocked(self) -> bool:
        return any(
            status.required and status.state is SourceState.FAILED
            for status in self.sources
        )


class SourceAcquisitionService:
    """Acquires the Case's frozen declared URLs into the Run (Spec 8).

    The constructor carries the store (durable facts land through the Task 2
    store and Task 3 commit protocol only) and the transport seam: an
    injectable Fetcher for unit tests, with the default HttpFetcher built
    from the service's ``max_bytes``/``timeout`` bounds. ``acquire`` expects
    a RUNNING Run whose current Invocation was already durably started by
    the control layer; the commit path independently re-verifies the
    RUNNING invocation from the event history, so a stale RunRecord fails
    the commit, never a silent write.
    """

    def __init__(
        self,
        store: RuntimeStore,
        *,
        fetcher: Fetcher | None = None,
        max_bytes: int = DEFAULT_MAX_BYTES,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._store = store
        self._max_bytes = max_bytes
        self._fetcher = fetcher or HttpFetcher(max_bytes=max_bytes, timeout=timeout)

    def acquire(self, case: ResearchCase, run: RunRecord) -> AcquisitionResult:
        """Acquire every declared source of *case* for *run*.

        Raises SourceDeclarationError when the frozen declarations violate
        the subset and AcquisitionError when the request violates the
        Runtime contract (including a Case whose declaration identity/digest
        drifted from the Run's frozen CaseBinding, Spec 16.1); per-source
        retrieval failures are returned in the AcquisitionResult with
        explicit dispositions and a ``blocked`` flag.
        """
        if not isinstance(case, ResearchCase):
            raise AcquisitionError(
                f"acquire requires a ResearchCase (got {case!r})."
            )
        if not isinstance(run, RunRecord):
            raise AcquisitionError(f"acquire requires a RunRecord (got {run!r}).")
        if run.state is not RunState.RUNNING:
            raise AcquisitionError(
                f"Run {run.run_id} is {run.state.value}; source acquisition "
                "requires a RUNNING Run (Spec 8 runs before R1 within an "
                "Invocation)."
            )
        if not run.current_invocation_id:
            raise AcquisitionError(
                f"Run {run.run_id} is RUNNING without a current invocation; "
                "the control layer must durably start the Invocation before "
                "acquisition."
            )
        if case.case_id != run.case_id or case.case_id != run.case_binding.case_id:
            raise AcquisitionError(
                f"case {case.case_id!r} does not match Run {run.run_id} "
                f"(bound to case {run.case_binding.case_id!r}); a Run only "
                "acquires its own frozen Case declarations."
            )
        # Spec 16.1 entry guard: the Run froze its Case declaration
        # identity/digest at creation, so a loaded Case (a resumed Run has no
        # choice but to re-load from disk) must still be that same frozen
        # declaration. The check sits here — before any fetch, any reuse
        # lookup decision and any artifact write — and names the drifted
        # dimension; Case changes affect new Runs only.
        binding = run.case_binding
        if case.source_declaration_identity != binding.source_declaration_identity:
            raise AcquisitionError(
                f"case {case.case_id!r} source declaration identity "
                f"{case.source_declaration_identity!r} does not match the "
                f"identity frozen into Run {run.run_id!r} at creation "
                f"({binding.source_declaration_identity!r}); case changes "
                "affect new Runs only (Spec 16.1)."
            )
        if case.source_declaration_digest != binding.source_declaration_digest:
            raise AcquisitionError(
                f"case {case.case_id!r} source declaration digest "
                f"{case.source_declaration_digest!r} does not match the digest "
                f"frozen into Run {run.run_id!r} at creation "
                f"({binding.source_declaration_digest!r}); case changes "
                "affect new Runs only (Spec 16.1)."
            )
        # Ruling 3 consistency guard: only the frozen text may be parsed.
        if sha256_digest(case.source_declaration_text) != case.source_declaration_digest:
            raise AcquisitionError(
                f"case {case.case_id!r} frozen declaration digest mismatch: "
                "the declaration text is not the text its binding digest was "
                "frozen over; nothing is acquired from unfrozen text."
            )
        try:
            self._store.events(run.run_id)
        except RunNotFoundError as error:
            raise AcquisitionError(
                f"Run {run.run_id!r} does not exist in the store: {error}"
            ) from error
        declarations = parse_source_declarations(case.source_declaration_text)
        committed = _committed_sources_by_id(self._store, run.run_id)

        statuses: list[SourceStatus] = []
        for declaration in declarations:
            statuses.append(
                self._acquire_one(case, run, declaration, committed.get(declaration.source_id))
            )
        return AcquisitionResult(
            run_id=run.run_id, case_id=case.case_id, sources=tuple(statuses)
        )

    # ------------------------------------------------------------------
    # internal acquisition flow (per source)
    # ------------------------------------------------------------------

    def _acquire_one(
        self,
        case: ResearchCase,
        run: RunRecord,
        declaration: SourceDeclaration,
        prior: ArtifactEnvelope | None,
    ) -> SourceStatus:
        if prior is not None:
            # Spec 8: a successful Source Artifact is reused during resume,
            # retry and rerun in the same Run; the fetcher is not called.
            return SourceStatus(
                source_id=declaration.source_id,
                url=declaration.url,
                required=declaration.required,
                state=SourceState.REUSED,
                artifact_id=prior.artifact_id,
                digest=prior.digest,
                retrieved_at=prior.created_at,
            )
        try:
            result = self._fetcher.fetch(declaration.url)
        except FetchError as error:
            return SourceStatus(
                source_id=declaration.source_id,
                url=declaration.url,
                required=declaration.required,
                state=SourceState.FAILED,
                disposition=error.disposition,
                detail=error.detail,
            )
        if not (200 <= result.status < 300):
            return SourceStatus(
                source_id=declaration.source_id,
                url=declaration.url,
                required=declaration.required,
                state=SourceState.FAILED,
                disposition="HTTP_ERROR",
                detail=f"HTTP {result.status} while fetching {declaration.url!r}.",
            )
        if len(result.raw) > self._max_bytes:
            return SourceStatus(
                source_id=declaration.source_id,
                url=declaration.url,
                required=declaration.required,
                state=SourceState.FAILED,
                disposition="OVERSIZED",
                detail=f"response body exceeds the {self._max_bytes}-byte bound.",
            )
        if not _is_supported_content(result.content_type):
            return SourceStatus(
                source_id=declaration.source_id,
                url=declaration.url,
                required=declaration.required,
                state=SourceState.FAILED,
                disposition="UNSUPPORTED_CONTENT",
                detail=(
                    f"content type {result.content_type or '(missing)'!r} is not "
                    "a supported textual media type; raw content is not "
                    "preserved for unsupported media."
                ),
            )
        retrieved_at = utc_now()
        text, encoding = _decode_text(result.raw, result.content_type)
        payload = {
            "source_id": declaration.source_id,
            "url": declaration.url,
            "required": declaration.required,
            "content": {
                "text": text,
                "encoding": encoding,
                "bytes": len(result.raw),
                "raw_digest": sha256_digest(result.raw),
            },
            "retrieval": {
                "http_status": result.status,
                "final_url": result.final_url,
                "content_type": result.content_type,
                "retrieved_at": retrieved_at,
            },
        }
        envelope = ArtifactEnvelope(
            artifact_id=f"src-{declaration.source_id}-{uuid.uuid4().hex}",
            run_id=run.run_id,
            invocation_id=run.current_invocation_id,
            artifact_schema_id=_SOURCE_SCHEMA_ID,
            artifact_schema_version=_SOURCE_SCHEMA_VERSION,
            created_at=retrieved_at,
            step_id=None,
            attempt_id=None,
            provenance=(
                f"declared:{case.source_declaration_identity}",
                f"url:{declaration.url}",
                f"http:{result.status}",
            ),
        )
        committed = commit_artifact(self._store, envelope, payload)
        return SourceStatus(
            source_id=declaration.source_id,
            url=declaration.url,
            required=declaration.required,
            state=SourceState.ACQUIRED,
            artifact_id=committed.artifact_id,
            digest=committed.digest,
            retrieved_at=retrieved_at,
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _committed_sources_by_id(store: RuntimeStore, run_id: str) -> dict[str, ArtifactEnvelope]:
    """Map each source_id to its committed attempt-less artifact of the Run.

    Only ARTIFACT_COMMITTED facts of *run_id* with no step/attempt lineage
    (Spec 9: Source Artifacts bind to the Invocation only) are eligible;
    later commits win, matching event order. The scan reads the run's own
    history, so reuse is strictly Run-scoped (Spec 8) and cross-Run commits
    never surface here.
    """
    sources: dict[str, ArtifactEnvelope] = {}
    for event in store.events(run_id):
        if event.event_type is not EventType.ARTIFACT_COMMITTED:
            continue
        if event.step_id is not None or event.attempt_id is not None:
            continue
        envelope = store.load_artifact(event.artifact_id)
        payload = envelope.payload
        if not isinstance(payload, Mapping):
            continue
        source_id = payload.get("source_id")
        if isinstance(source_id, str) and source_id:
            sources[source_id] = envelope
    return sources


def _is_supported_content(content_type: str) -> bool:
    """Textual media only: text/* plus the common JSON/XML family.

    A missing Content-Type is unsupported: the service never guesses whether
    raw bytes are preservable text.
    """
    media = content_type.split(";", 1)[0].strip().lower()
    if not media:
        return False
    if media.startswith(_TEXT_MEDIA_PREFIX):
        return True
    return media in _JSONISH_MEDIA_TYPES


def _decode_text(raw: bytes, content_type: str) -> tuple[str, str]:
    """Decode raw bytes to text with the declared charset when present.

    The charset parameter wins when it names a codec Python knows; otherwise
    UTF-8 is tried and Latin-1 is the final fallback (it decodes every byte
    sequence). Raw fidelity is preserved independently via ``raw_digest``.
    """
    charset = _charset_of(content_type)
    if charset is not None:
        try:
            return raw.decode(charset), charset
        except (LookupError, UnicodeDecodeError):
            pass  # fall through to the deterministic fallbacks below
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("latin-1"), "latin-1"


def _charset_of(content_type: str) -> str | None:
    for parameter in content_type.split(";")[1:]:
        name, separator, value = parameter.strip().partition("=")
        if separator and name.lower() == "charset":
            charset = value.strip().strip('"').strip("'")
            return charset or None
    return None


__all__ = [
    "AcquisitionError",
    "AcquisitionResult",
    "DEFAULT_MAX_BYTES",
    "DEFAULT_TIMEOUT_SECONDS",
    "FetchError",
    "FetchResult",
    "Fetcher",
    "HttpFetcher",
    "SourceAcquisitionService",
    "SourceDeclaration",
    "SourceDeclarationError",
    "SourceState",
    "SourceStatus",
    "parse_source_declarations",
]
