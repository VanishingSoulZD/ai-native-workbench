"""Integration tests for declared-URL source acquisition over a local HTTP
server (Task 5 brief Step 6, Spec section 8, architecture 11.2/11.3).

The tests are semantically real but never touch the internet: a local
stdlib HTTP server serves the declared routes. Coverage: acquisition
success over text and JSON media, redirect following with final-URL
metadata, oversized and unsupported content as explicit failures, required
failure blocking with optional failure continuing, retrieval metadata and
raw-content digesting, and same-Run reuse of committed Source Artifacts
(Spec 8) — including across a resume-style new Invocation — while a new Run
refetches.
"""

import hashlib
import http.server
import json
import threading
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    EntryMode,
    EventEnvelope,
    EventType,
    RunRecord,
    RunState,
    RuntimeContractError,
    utc_now,
)
from ai_native_workbench.research.runtime.binding import (
    freeze_case_binding,
    load_research_case,
)
from ai_native_workbench.research.runtime.source.acquisition import (
    SourceAcquisitionService,
    SourceDeclarationError,
    SourceState,
)
from ai_native_workbench.research.runtime.store import FileSystemRuntimeStore

CASE_ID = "case-1"
RUN_ID = "run-1"
RUN_ID_2 = "run-2"
INVOCATION_ID = "inv-1"
INVOCATION_ID_2 = "inv-2"
ALPHA_BODY = "The quick brown fox — 敏捷的棕色狐狸."
BETA_BODY = '{"items": [{"id": "s-1"}]}'

SMALL_MAX_BYTES = 1024


# ---------------------------------------------------------------------------
# Local HTTP server helpers (no external network dependency)
# ---------------------------------------------------------------------------


class DeclaredUrlHandler(http.server.BaseHTTPRequestHandler):
    """Serves the routes declared for one test; counts hits per path."""

    routes: dict = {}
    hits: list = []

    def do_GET(self):  # noqa: N802 (stdlib hook name)
        type(self).hits.append(self.path)
        route = type(self).routes.get(self.path)
        if route is None:
            self._respond(404, {"Content-Type": "text/plain"}, b"not found")
            return
        status, headers, body = route
        self._respond(status, headers, body)

    def _respond(self, status: int, headers: dict, body: bytes) -> None:
        self.send_response(status)
        for name, value in headers.items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass  # the client may stop reading early (oversized responses)

    def log_message(self, *args) -> None:  # keep test output clean
        pass


@pytest.fixture
def http_origin():
    """A running local server with a fresh, per-test route table."""
    DeclaredUrlHandler.routes = {}
    DeclaredUrlHandler.hits = []
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), DeclaredUrlHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{httpd.server_address[1]}"
    yield origin
    httpd.shutdown()
    httpd.server_close()
    thread.join(timeout=5)


def route_text(body: str = ALPHA_BODY, content_type: str = "text/plain; charset=utf-8"):
    return (200, {"Content-Type": content_type}, body.encode("utf-8"))


def sha256_digest(raw: bytes) -> str:
    """Independent reference digest pinning the documented digest scheme."""
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def payload_digest(payload: object) -> str:
    text = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return sha256_digest(text.encode("utf-8"))


def make_case_dir(tmp_path, urls_text: str):
    case_dir = tmp_path / "cases" / CASE_ID
    inputs = case_dir / "inputs"
    inputs.mkdir(parents=True)
    (case_dir / "00-research-charter.md").write_text("# charter\n", encoding="utf-8")
    (case_dir / "inputs" / "urls.yaml").write_text(urls_text, encoding="utf-8")
    return case_dir


def declared_urls(*entries) -> str:
    """Render list entries of (source_id, url, required) as urls.yaml text."""
    lines = []
    for source_id, url, required in entries:
        lines.append(f"- id: {source_id}\n  url: {url}\n")
        if required is not None:
            lines.append(f"  required: {str(required).lower()}\n")
    return "".join(lines)


def make_run(
    case, run_id: str = RUN_ID, invocation_id: str = INVOCATION_ID
) -> RunRecord:
    return RunRecord(
        run_id=run_id,
        case_id=CASE_ID,
        case_binding=freeze_case_binding(case),
        state=RunState.RUNNING,
        cumulative_execution_scope=(),
        current_invocation_id=invocation_id,
        completion_reason=None,
    )


def evt(run_id: str, event_id: str, invocation_id: str, kind: EventType, payload: dict):
    return EventEnvelope(
        event_id=event_id,
        event_type=kind,
        timestamp=utc_now(),
        run_id=run_id,
        invocation_id=invocation_id,
        payload=payload,
    )


def execution_binding_payload(entry_mode: str) -> dict:
    return {
        "requested_scope": ["R1", "R2", "R3", "R4", "R5", "SNAPSHOT"],
        "entry_mode": entry_mode,
        "execution_binding": {
            "workflow_identity": "research-standard",
            "workflow_version": "1.0.0",
            "runtime_configuration_identity": "runtime-config-001",
            "prompts": {},
            "schemas": {},
        },
    }


def build_running_run(store, run: RunRecord) -> None:
    """create_run + INVOCATION_STARTED, mirroring the Task 3 conventions.

    store.create_run requires a CREATED record (the Task 3 contract), while
    acquire() needs the RUNNING projection with a current Invocation, so the
    CREATED record is derived from the RUNNING one.
    """
    store.create_run(
        replace(
            run,
            state=RunState.CREATED,
            current_invocation_id=None,
            completion_reason=None,
        )
    )
    store.append_event(
        evt(
            run.run_id,
            f"evt-{run.run_id}-started",
            run.current_invocation_id,
            EventType.INVOCATION_STARTED,
            execution_binding_payload(EntryMode.START.value),
        )
    )


def commit_events(store, run_id: str = RUN_ID) -> tuple:
    return tuple(
        event
        for event in store.events(run_id)
        if event.event_type is EventType.ARTIFACT_COMMITTED
    )


# ---------------------------------------------------------------------------
# Declared-URL acquisition over local HTTP (brief Step 6 coverage)
# ---------------------------------------------------------------------------


def test_acquires_declared_sources_over_local_http(tmp_path, http_origin):
    DeclaredUrlHandler.routes = {
        "/source-a": route_text(ALPHA_BODY),
        "/source-b": route_text(BETA_BODY, content_type="application/json"),
    }
    urls = declared_urls(
        ("src-1", f"{http_origin}/source-a", True),
        ("src-2", f"{http_origin}/source-b", None),
    )
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    result = SourceAcquisitionService(store).acquire(case, make_run(case))

    assert result.blocked is False
    assert [(s.source_id, s.state) for s in result.sources] == [
        ("src-1", SourceState.ACQUIRED),
        ("src-2", SourceState.ACQUIRED),
    ]
    assert sorted(DeclaredUrlHandler.hits) == ["/source-a", "/source-b"]

    envelope = store.load_artifact(result.sources[0].artifact_id)
    assert envelope.digest
    assert envelope.provenance[0] == "declared:inputs/urls.yaml"
    assert envelope.provenance[1] == f"url:{http_origin}/source-a"
    content = envelope.payload["content"]
    assert content["text"] == ALPHA_BODY
    assert content["encoding"] == "utf-8"
    assert content["bytes"] == len(ALPHA_BODY.encode("utf-8"))
    assert content["raw_digest"] == sha256_digest(ALPHA_BODY.encode("utf-8"))
    retrieval = envelope.payload["retrieval"]
    assert retrieval["http_status"] == 200
    assert retrieval["final_url"] == f"{http_origin}/source-a"
    assert retrieval["content_type"].startswith("text/plain")
    assert retrieval["retrieved_at"]
    assert envelope.digest == payload_digest(envelope.payload)


def test_redirect_is_followed_and_final_url_recorded(tmp_path, http_origin):
    DeclaredUrlHandler.routes = {
        "/doc": (302, {"Location": "/final"}, b""),
        "/final": route_text("redirected body"),
    }
    urls = declared_urls(("src-1", f"{http_origin}/doc", True))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    result = SourceAcquisitionService(store).acquire(case, make_run(case))

    assert result.sources[0].state is SourceState.ACQUIRED
    assert DeclaredUrlHandler.hits == ["/doc", "/final"]
    payload = store.load_artifact(result.sources[0].artifact_id).payload
    assert payload["content"]["text"] == "redirected body"
    assert payload["retrieval"]["final_url"] == f"{http_origin}/final"
    assert payload["retrieval"]["http_status"] == 200


def test_oversized_response_is_an_explicit_failure(tmp_path, http_origin):
    DeclaredUrlHandler.routes = {
        "/big": (200, {"Content-Type": "text/plain"}, b"x" * (4 * SMALL_MAX_BYTES)),
    }
    urls = declared_urls(("src-1", f"{http_origin}/big", True))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    result = SourceAcquisitionService(
        store, max_bytes=SMALL_MAX_BYTES
    ).acquire(case, make_run(case))

    assert result.blocked is True
    (status,) = result.sources
    assert status.state is SourceState.FAILED
    assert status.disposition == "OVERSIZED"
    assert commit_events(store) == ()


def test_unsupported_content_is_an_explicit_failure(tmp_path, http_origin):
    DeclaredUrlHandler.routes = {
        "/paper.pdf": (200, {"Content-Type": "application/pdf"}, b"%PDF-1.4"),
    }
    urls = declared_urls(("src-1", f"{http_origin}/paper.pdf", True))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    result = SourceAcquisitionService(store).acquire(case, make_run(case))

    assert result.blocked is True
    (status,) = result.sources
    assert status.state is SourceState.FAILED
    assert status.disposition == "UNSUPPORTED_CONTENT"
    assert "application/pdf" in status.detail
    assert commit_events(store) == ()


def test_required_failure_blocks_and_optional_failure_continues(tmp_path, http_origin):
    DeclaredUrlHandler.routes = {"/ok": route_text("fine")}
    urls = declared_urls(
        ("required-src", f"{http_origin}/missing", True),
        ("optional-src", f"{http_origin}/also-missing", None),
        ("ok-src", f"{http_origin}/ok", None),
    )
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    result = SourceAcquisitionService(store).acquire(case, make_run(case))

    # The required failure blocks the result while every declaration is still
    # processed and recorded (the orchestrator decides how to dispose of the
    # blocked run).
    assert result.blocked is True
    assert [s.source_id for s in result.sources] == [
        "required-src",
        "optional-src",
        "ok-src",
    ]
    assert [s.state for s in result.sources] == [
        SourceState.FAILED,
        SourceState.FAILED,
        SourceState.ACQUIRED,
    ]
    required, optional, ok = result.sources
    assert required.disposition == "HTTP_ERROR"
    assert "404" in required.detail
    assert optional.disposition == "HTTP_ERROR"
    assert ok.artifact_id
    # Only the successful source is committed.
    assert len(commit_events(store)) == 1


def test_same_run_reuse_never_refetches(tmp_path, http_origin):
    """Spec 8: a successful Source Artifact is reused during retry/rerun in
    the same Run — the local server sees exactly one request."""
    DeclaredUrlHandler.routes = {"/source-a": route_text(ALPHA_BODY)}
    urls = declared_urls(("src-1", f"{http_origin}/source-a", True))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))
    service = SourceAcquisitionService(store)

    first = service.acquire(case, make_run(case))
    second = service.acquire(case, make_run(case))

    assert DeclaredUrlHandler.hits == ["/source-a"]
    assert len(commit_events(store)) == 1
    assert second.sources[0].state is SourceState.REUSED
    assert second.sources[0].artifact_id == first.sources[0].artifact_id


def test_resume_in_the_same_run_reuses_committed_sources(tmp_path, http_origin):
    """Spec 15.3: a resume-style new Invocation stays in the same Run and
    reuses its committed Source Artifacts — no second fetch happens."""
    DeclaredUrlHandler.routes = {"/source-a": route_text(ALPHA_BODY)}
    urls = declared_urls(("src-1", f"{http_origin}/source-a", True))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))
    service = SourceAcquisitionService(store)
    service.acquire(case, make_run(case))

    store.append_event(
        evt(
            RUN_ID,
            "evt-inv1-completed",
            INVOCATION_ID,
            EventType.INVOCATION_COMPLETED,
            {"status": "SUCCEEDED", "completion_reason": "BOUNDED_SCOPE"},
        )
    )
    store.append_event(
        evt(
            RUN_ID,
            "evt-inv2-started",
            INVOCATION_ID_2,
            EventType.INVOCATION_STARTED,
            execution_binding_payload(EntryMode.RESUME.value),
        )
    )
    resumed_result = service.acquire(case, make_run(case, invocation_id=INVOCATION_ID_2))

    assert DeclaredUrlHandler.hits == ["/source-a"]
    assert len(commit_events(store)) == 1
    assert resumed_result.sources[0].state is SourceState.REUSED


def test_new_run_refetches_declared_sources(tmp_path, http_origin):
    """Reuse is Run-scoped: a future new Run re-acquires (Spec 8)."""
    DeclaredUrlHandler.routes = {"/source-a": route_text(ALPHA_BODY)}
    urls = declared_urls(("src-1", f"{http_origin}/source-a", True))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))
    service = SourceAcquisitionService(store)
    first = service.acquire(case, make_run(case))

    second_run = make_run(case, run_id=RUN_ID_2, invocation_id="inv-run-2")
    build_running_run(store, second_run)
    second = service.acquire(case, second_run)

    assert DeclaredUrlHandler.hits == ["/source-a", "/source-a"]
    assert second.sources[0].state is SourceState.ACQUIRED
    assert second.sources[0].artifact_id != first.sources[0].artifact_id
    assert len(commit_events(store, run_id=RUN_ID_2)) == 1


def test_declared_urls_only_no_other_paths_are_fetched(tmp_path, http_origin):
    """Spec 8: no autonomous discovery — an undeclared path is never hit."""
    DeclaredUrlHandler.routes = {"/source-a": route_text(ALPHA_BODY)}
    urls = declared_urls(("src-1", f"{http_origin}/source-a", False))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    SourceAcquisitionService(store).acquire(case, make_run(case))

    assert DeclaredUrlHandler.hits == ["/source-a"]


def test_charset_parameter_is_honoured_in_content_text(tmp_path, http_origin):
    body = "Grüße aus der Forschung — 研究问候"
    DeclaredUrlHandler.routes = {
        "/source-a": (200, {"Content-Type": "text/plain; charset=utf-8"}, body.encode("utf-8"))
    }
    urls = declared_urls(("src-1", f"{http_origin}/source-a", False))
    case = load_research_case(make_case_dir(tmp_path, urls))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    result = SourceAcquisitionService(store).acquire(case, make_run(case))

    payload = store.load_artifact(result.sources[0].artifact_id).payload
    assert payload["content"]["text"] == body
    assert payload["content"]["encoding"] == "utf-8"
    assert payload["content"]["bytes"] == len(body.encode("utf-8"))
    assert payload["content"]["raw_digest"] == sha256_digest(body.encode("utf-8"))
    # The artifact digest is the canonical-JSON digest of the whole payload.
    assert store.load_artifact(result.sources[0].artifact_id).digest == payload_digest(
        payload
    )


def test_invalid_declaration_never_fetches(tmp_path, http_origin):
    """An invalid frozen declaration aborts acquisition before any fetch."""
    DeclaredUrlHandler.routes = {"/source-a": route_text(ALPHA_BODY)}
    urls = declared_urls(("src-1", f"{http_origin}/source-a", None))
    case = load_research_case(make_case_dir(tmp_path, urls + "  extra: key\n"))
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")
    build_running_run(store, make_run(case))

    with pytest.raises(SourceDeclarationError) as excinfo:
        SourceAcquisitionService(store).acquire(case, make_run(case))
    assert "extra" in str(excinfo.value)
    assert isinstance(excinfo.value, RuntimeContractError)
    assert DeclaredUrlHandler.hits == []
