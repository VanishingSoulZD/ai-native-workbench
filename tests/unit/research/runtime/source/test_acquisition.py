"""Unit tests for source declaration parsing and SourceAcquisitionService
(Task 5 brief Steps 4-7, Spec section 8, architecture sections 11.2/11.3).

Declaration parsing covers the constrained urls.yaml subset (list items of
``- id: <source id>`` with two-space-indented ``url:`` and optional
``required:`` keys): malformed URLs, duplicate source ids, unsupported
schemes, required/optional flags and the frozen declaration digest guard.
Acquisition covers fetch success, redirect/transport handling through the
injectable fetcher seam, oversized and unsupported content, required-failure
blocking, optional-failure continuation, metadata capture, digesting and
same-Run reuse of committed Source Artifacts (Spec 8). Tests never touch the
network; the integration suite exercises a local HTTP server.
"""

import hashlib
import json
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    ArtifactEnvelope,
    CaseBinding,
    EntryMode,
    EventEnvelope,
    EventType,
    RunRecord,
    RunState,
    RuntimeContractError,
    utc_now,
)
from ai_native_workbench.research.runtime.binding import ResearchCase
from ai_native_workbench.research.runtime.source.acquisition import (
    FetchError,
    FetchResult,
    SourceAcquisitionService,
    SourceDeclarationError,
    SourceState,
    parse_source_declarations,
)
from ai_native_workbench.research.runtime.store import (
    FileSystemRuntimeStore,
    reduce_events,
)

CASE_ID = "case-1"
RUN_ID = "run-1"
INVOCATION_ID = "inv-1"
INVOCATION_ID_2 = "inv-2"
URLS_IDENTITY = "inputs/urls.yaml"
TS = "2026-09-09T08:00:00+00:00"

URLS_TEXT = (
    "- id: src-1\n"
    "  url: https://example.com/source-a\n"
    "  required: true\n"
    "- id: src-2\n"
    "  url: http://example.org/source-b\n"
)


# ---------------------------------------------------------------------------
# Shared helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def sha256_digest(text: str) -> str:
    """Independent reference digest pinning the documented digest scheme."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def raw_digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def reference_payload_digest(payload: object) -> str:
    text = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_case(**overrides) -> ResearchCase:
    defaults = dict(
        case_id=CASE_ID,
        charter_identity="00-research-charter.md",
        charter_digest=sha256_digest("# charter\n"),
        charter_text="# charter\n",
        source_declaration_identity=URLS_IDENTITY,
        source_declaration_digest=sha256_digest(URLS_TEXT),
        source_declaration_text=URLS_TEXT,
    )
    defaults.update(overrides)
    return ResearchCase(**defaults)


def case_binding(case_id: str = CASE_ID) -> CaseBinding:
    return CaseBinding(
        case_id=case_id,
        charter_identity="00-research-charter.md",
        charter_digest=sha256_digest("# charter\n"),
        source_declaration_identity=URLS_IDENTITY,
        source_declaration_digest=sha256_digest(URLS_TEXT),
    )


def make_run_record(run_id: str = RUN_ID, case_id: str = CASE_ID, **overrides) -> RunRecord:
    """A CREATED record for store.create_run (the Task 3 convention)."""
    defaults = dict(
        run_id=run_id,
        case_id=case_id,
        case_binding=case_binding(case_id),
        state=RunState.CREATED,
        cumulative_execution_scope=(),
        current_invocation_id=None,
        completion_reason=None,
    )
    defaults.update(overrides)
    return RunRecord(**defaults)


def running_record(run_id: str = RUN_ID, **overrides) -> RunRecord:
    """The RUNNING record (with a current Invocation) an acquire call needs."""
    defaults = dict(
        state=RunState.RUNNING,
        current_invocation_id=INVOCATION_ID,
    )
    defaults.update(overrides)
    return make_run_record(run_id=run_id, **defaults)


def one_source_case(**overrides) -> ResearchCase:
    """A Case whose frozen declaration is a single required source (src-1)."""
    text = (
        "- id: src-1\n"
        "  url: https://example.com/source-a\n"
        "  required: true\n"
    )
    defaults = dict(
        source_declaration_text=text,
        source_declaration_digest=sha256_digest(text),
    )
    defaults.update(overrides)
    return make_case(**defaults)


def evt(kind: EventType, event_id: str, **overrides) -> EventEnvelope:
    return replace(
        EventEnvelope(
            event_id=event_id,
            event_type=kind,
            timestamp=TS,
            run_id=RUN_ID,
            payload={},
        ),
        **overrides,
    )


def invocation_started_event(invocation_id: str = INVOCATION_ID, **kw) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_STARTED,
        f"evt-{invocation_id}-started",
        invocation_id=invocation_id,
        payload={
            "requested_scope": ["R1", "R2", "R3", "R4", "R5", "SNAPSHOT"],
            "entry_mode": EntryMode.START.value,
            "execution_binding": {
                "workflow_identity": "research-standard",
                "workflow_version": "1.0.0",
                "runtime_configuration_identity": "runtime-config-001",
                "prompts": {},
                "schemas": {},
            },
        },
        **kw,
    )


def invocation_completed_event(invocation_id: str = INVOCATION_ID, **kw) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_COMPLETED,
        f"evt-{invocation_id}-completed",
        invocation_id=invocation_id,
        payload={"status": "SUCCEEDED", "completion_reason": "BOUNDED_SCOPE"},
        **kw,
    )


def build_running_invocation(
    store,
    *,
    run_id: str = RUN_ID,
    case_id: str = CASE_ID,
    invocation_id: str = INVOCATION_ID,
) -> None:
    """create_run + INVOCATION_STARTED: the Run a service may acquire for."""
    store.create_run(make_run_record(run_id=run_id, case_id=case_id))
    store.append_event(
        invocation_started_event(run_id=run_id, invocation_id=invocation_id)
    )


def commit_events(store, run_id: str = RUN_ID) -> tuple:
    return tuple(
        event
        for event in store.events(run_id)
        if event.event_type is EventType.ARTIFACT_COMMITTED
    )


class FakeFetcher:
    """Recorded-response fetcher: returns queued results, raises on empty."""

    def __init__(self, *results):
        self.responses = list(results)
        self.calls: list[str] = []

    def fetch(self, url: str) -> FetchResult:
        self.calls.append(url)
        if not self.responses:
            raise AssertionError(f"fetch({url!r}) called with no queued response")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def ok_result(
    url: str,
    raw: bytes = b"plain text body",
    content_type: str = "text/plain",
    status: int = 200,
    final_url: str | None = None,
) -> FetchResult:
    return FetchResult(
        status=status,
        final_url=final_url or url,
        content_type=content_type,
        raw=raw,
    )


# ---------------------------------------------------------------------------
# Declaration parsing and validation (brief Step 4/5 coverage)
# ---------------------------------------------------------------------------


def test_parse_declares_sources_in_order_with_defaults():
    declarations = parse_source_declarations(URLS_TEXT)
    assert len(declarations) == 2
    first, second = declarations
    assert first.source_id == "src-1"
    assert first.url == "https://example.com/source-a"
    assert first.required is True
    assert second.source_id == "src-2"
    assert second.url == "http://example.org/source-b"
    assert second.required is False  # optional when not declared


def test_parse_allows_blank_lines_and_boolean_variants():
    text = (
        "\n"
        "- id: src-a\n"
        "  url: https://example.com/a\n"
        "\n"
        "- id: src-b\n"
        "  url: https://example.com/b\n"
        "  required: FALSE\n"
        "- id: src-c\n"
        "  url: https://example.com/c\n"
        "  required: True\n"
    )
    declarations = parse_source_declarations(text)
    assert [d.source_id for d in declarations] == ["src-a", "src-b", "src-c"]
    assert [d.required for d in declarations] == [False, False, True]


def test_parse_is_deterministic_over_the_frozen_text():
    assert parse_source_declarations(URLS_TEXT) == parse_source_declarations(URLS_TEXT)


def test_parse_rejects_a_missing_url():
    with pytest.raises(SourceDeclarationError) as excinfo:
        parse_source_declarations("- id: src-1\n")
    assert "url" in str(excinfo.value)


def test_parse_rejects_a_blank_url():
    text = "- id: src-1\n  url:   \n"
    with pytest.raises(SourceDeclarationError) as excinfo:
        parse_source_declarations(text)
    assert "2" in str(excinfo.value)  # the line number is reported


def test_parse_rejects_duplicate_source_ids():
    text = (
        "- id: src-1\n  url: https://example.com/a\n"
        "- id: src-1\n  url: https://example.com/b\n"
    )
    with pytest.raises(SourceDeclarationError) as excinfo:
        parse_source_declarations(text)
    message = str(excinfo.value)
    assert "src-1" in message
    assert "3" in message  # the duplicate is reported at its own line


def test_parse_rejects_unsupported_url_schemes():
    for url in ("ftp://example.com/file", "file:///etc/passwd", "gopher://x"):
        with pytest.raises(SourceDeclarationError, match="scheme"):
            parse_source_declarations(f"- id: src-1\n  url: {url}\n")


def test_parse_rejects_malformed_urls():
    for url in ("example.com/no-scheme", "https:///missing-host", "https://"):
        with pytest.raises(SourceDeclarationError, match="url"):
            parse_source_declarations(f"- id: src-1\n  url: {url}\n")


def test_parse_rejects_non_boolean_required():
    with pytest.raises(SourceDeclarationError) as excinfo:
        parse_source_declarations(
            "- id: src-1\n  url: https://example.com/a\n  required: maybe\n"
        )
    assert "maybe" in str(excinfo.value)
    assert "3" in str(excinfo.value)


def test_parse_rejects_unknown_keys():
    with pytest.raises(SourceDeclarationError) as excinfo:
        parse_source_declarations(
            "- id: src-1\n  url: https://example.com/a\n  title: Home\n"
        )
    message = str(excinfo.value)
    assert "title" in message
    assert "3" in message


def test_parse_rejects_duplicate_keys_within_one_entry():
    with pytest.raises(SourceDeclarationError) as excinfo:
        parse_source_declarations(
            "- id: src-1\n"
            "  url: https://example.com/a\n"
            "  url: https://example.com/b\n"
        )
    assert "url" in str(excinfo.value)


def test_parse_rejects_content_outside_the_subset():
    # Anything that is not a list item or a continuation line is refused
    # explicitly with its line number (the subset is constrained on purpose).
    for line in ("urls:", "  - id: src-1", "  id: src-1", "# comment", "---"):
        with pytest.raises(SourceDeclarationError) as excinfo:
            parse_source_declarations(line)
        assert "1" in str(excinfo.value)


def test_parse_rejects_invalid_source_ids():
    for source_id in ("", "src 1", "src:1", "s\nrc", ".hidden"):
        with pytest.raises(SourceDeclarationError) as excinfo:
            parse_source_declarations(f"- id: {source_id}\n  url: https://e.com/a\n")
        assert str(excinfo.value)


def test_parse_rejects_declarations_without_sources():
    with pytest.raises(SourceDeclarationError) as excinfo:
        parse_source_declarations("   \n\n")
    assert "no sources" in str(excinfo.value)


def test_parse_rejects_non_text_declarations():
    with pytest.raises(SourceDeclarationError):
        parse_source_declarations(123)  # type: ignore[arg-type]


def test_source_declaration_error_is_a_contract_error():
    with pytest.raises(RuntimeContractError):
        parse_source_declarations("not a declaration\n")


# ---------------------------------------------------------------------------
# SourceAcquisitionService (brief Step 6/7, Spec section 8, 11.2/11.3)
# ---------------------------------------------------------------------------


def test_acquire_commits_source_artifacts_with_metadata_and_digest(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(
        store, fetcher=FakeFetcher(
            ok_result("https://example.com/source-a", raw=b"alpha body"),
            ok_result("http://example.org/source-b", raw=b"beta body"),
        )
    )

    result = service.acquire(make_case(), running_record())

    assert result.run_id == RUN_ID
    assert result.case_id == CASE_ID
    assert result.blocked is False
    assert [(s.source_id, s.state) for s in result.sources] == [
        ("src-1", SourceState.ACQUIRED),
        ("src-2", SourceState.ACQUIRED),
    ]
    first = result.sources[0]
    assert first.artifact_id.startswith("src-src-1-")
    assert first.digest and first.digest.startswith("sha256:")
    assert first.retrieved_at

    events = commit_events(store)
    assert len(events) == 2
    assert {event.artifact_id for event in events} == {
        s.artifact_id for s in result.sources
    }
    assert all(event.step_id is None and event.attempt_id is None for event in events)

    envelope = store.load_artifact(first.artifact_id)
    assert envelope.run_id == RUN_ID
    assert envelope.invocation_id == INVOCATION_ID
    assert envelope.step_id is None
    assert envelope.attempt_id is None
    assert envelope.artifact_schema_id == "source-artifact"
    assert envelope.artifact_schema_version == "1"
    assert envelope.digest == reference_payload_digest(envelope.payload)

    payload = envelope.payload
    assert payload["source_id"] == "src-1"
    assert payload["url"] == "https://example.com/source-a"
    assert payload["required"] is True
    assert payload["content"] == {
        "text": "alpha body",
        "encoding": "utf-8",
        "bytes": 10,
        "raw_digest": raw_digest(b"alpha body"),
    }
    retrieval = payload["retrieval"]
    assert retrieval["http_status"] == 200
    assert retrieval["final_url"] == "https://example.com/source-a"
    assert retrieval["content_type"] == "text/plain"
    assert retrieval["retrieved_at"]
    assert envelope.digest == reference_payload_digest(payload)
    assert envelope.provenance[0] == "declared:inputs/urls.yaml"
    assert envelope.provenance[1] == "url:https://example.com/source-a"
    # The committed artifact is a projection fact of the run (Ruling 4).
    projection = reduce_events(store.events(RUN_ID))
    assert set(projection.artifacts) == {s.artifact_id for s in result.sources}


def test_acquire_required_failure_blocks_with_explicit_disposition(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(
        store,
        fetcher=FakeFetcher(FetchError("HTTP_ERROR", "HTTP 404 Not Found", status=404)),
    )

    result = service.acquire(one_source_case(), running_record())

    assert result.blocked is True
    (status,) = result.sources
    assert status.source_id == "src-1"
    assert status.required is True
    assert status.state is SourceState.FAILED
    assert status.disposition == "HTTP_ERROR"
    assert "404" in status.detail
    assert status.artifact_id is None
    assert commit_events(store) == ()


def test_acquire_optional_failure_is_non_blocking_and_continues(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(
        store,
        fetcher=FakeFetcher(
            FetchError("UNREACHABLE", "connection refused"),
            ok_result("http://example.org/source-b", raw=b"beta body"),
        ),
    )

    urls = (
        "- id: src-1\n"
        "  url: https://example.com/a\n"
        "- id: src-2\n"
        "  url: http://example.org/source-b\n"
    )
    case = make_case(
        source_declaration_text=urls, source_declaration_digest=sha256_digest(urls)
    )
    result = service.acquire(case, running_record())

    # src-1 is optional (no required flag): its failure is recorded but the
    # acquisition result is not blocked and src-2 is still acquired.
    assert result.blocked is False
    first, second = result.sources
    assert first.source_id == "src-1"
    assert first.state is SourceState.FAILED
    assert first.disposition == "UNREACHABLE"
    assert second.source_id == "src-2"
    assert second.state is SourceState.ACQUIRED
    assert len(commit_events(store)) == 1


def test_acquire_all_optional_failures_still_return_a_result(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    urls = "- id: src-1\n  url: https://example.com/a\n"
    case = make_case(
        source_declaration_text=urls,
        source_declaration_digest=sha256_digest(urls),
    )
    service = SourceAcquisitionService(
        store, fetcher=FakeFetcher(FetchError("UNREACHABLE", "timed out"))
    )
    result = service.acquire(case, running_record())
    assert result.blocked is False
    assert len(result.sources) == 1
    assert commit_events(store) == ()


def test_acquire_oversized_content_is_an_explicit_failure(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    # A bounded fetch contract limits raw bodies; the service re-checks so
    # every transport honors the same explicit OVERSIZED disposition.
    service = SourceAcquisitionService(
        store, fetcher=FakeFetcher(ok_result("https://e.com/a", raw=b"x" * 3000)),
        max_bytes=1024,
    )
    result = service.acquire(one_source_case(), running_record())
    assert result.blocked is True
    (status,) = result.sources
    assert status.state is SourceState.FAILED
    assert status.disposition == "OVERSIZED"
    assert commit_events(store) == ()


def test_acquire_unsupported_content_is_an_explicit_failure(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(
        store,
        fetcher=FakeFetcher(
            ok_result("https://e.com/a", raw=b"%PDF", content_type="application/pdf"),
            ok_result("https://e.com/b", raw=b"", content_type=""),
        ),
    )
    case = make_case(
        source_declaration_text=(
            "- id: src-1\n  url: https://e.com/a\n"
            "- id: src-2\n  url: https://e.com/b\n"
        ),
        source_declaration_digest=sha256_digest(
            "- id: src-1\n  url: https://e.com/a\n"
            "- id: src-2\n  url: https://e.com/b\n"
        ),
    )
    result = service.acquire(case, running_record())
    assert result.blocked is False  # both sources are optional
    assert [s.disposition for s in result.sources] == [
        "UNSUPPORTED_CONTENT",
        "UNSUPPORTED_CONTENT",
    ]
    assert commit_events(store) == ()


def test_acquire_reuses_committed_source_artifacts_in_the_same_run(tmp_path):
    """A successful Source Artifact is reused during retry/rerun in the same
    Run: the fetcher is not called again and no new commit facts are made."""
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    fetcher = FakeFetcher(ok_result("https://example.com/source-a", raw=b"alpha"))
    service = SourceAcquisitionService(store, fetcher=fetcher)

    first = service.acquire(one_source_case(), running_record())
    second = service.acquire(one_source_case(), running_record())

    assert len(fetcher.calls) == 1
    assert len(commit_events(store)) == 1
    first_status = first.sources[0]
    second_status = second.sources[0]
    assert second_status.state is SourceState.REUSED
    assert second_status.artifact_id == first_status.artifact_id
    assert second_status.digest == first_status.digest
    assert second_status.required is True


def test_acquire_reuse_spans_invocations_within_a_run(tmp_path):
    """Resume opens a new Invocation in the same Run (Spec 15.3); acquisition
    on the resumed Invocation reuses the Run's committed Source Artifacts."""
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    fetcher = FakeFetcher(ok_result("https://example.com/source-a", raw=b"alpha"))
    service = SourceAcquisitionService(store, fetcher=fetcher)
    first = service.acquire(one_source_case(), running_record())

    store.append_event(invocation_completed_event())
    store.append_event(invocation_started_event(invocation_id=INVOCATION_ID_2))
    resumed = running_record(current_invocation_id=INVOCATION_ID_2)
    second = service.acquire(one_source_case(), resumed)

    assert len(fetcher.calls) == 1
    assert len(commit_events(store)) == 1
    assert second.sources[0].state is SourceState.REUSED
    assert second.sources[0].artifact_id == first.sources[0].artifact_id
    # The reused artifact keeps its original Invocation lineage.
    envelope = store.load_artifact(first.sources[0].artifact_id)
    assert envelope.invocation_id == INVOCATION_ID


def test_acquire_a_new_run_refetches_declared_sources(tmp_path):
    """Reuse is Run-scoped (Spec 8): a new Run re-acquires, never silently
    borrowing another Run's committed Source Artifacts."""
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    fetcher = FakeFetcher(
        ok_result("https://example.com/source-a", raw=b"alpha"),
        ok_result("https://example.com/source-a", raw=b"alpha"),
    )
    service = SourceAcquisitionService(store, fetcher=fetcher)
    first = service.acquire(one_source_case(), running_record())

    build_running_invocation(
        store, run_id="run-2", invocation_id="inv-run-2"
    )
    second = service.acquire(
        one_source_case(),
        running_record(run_id="run-2", current_invocation_id="inv-run-2"),
    )

    assert len(fetcher.calls) == 2
    second_status = second.sources[0]
    assert second_status.state is SourceState.ACQUIRED
    assert second_status.artifact_id != first.sources[0].artifact_id
    assert len(commit_events(store, run_id=RUN_ID)) == 1
    assert len(commit_events(store, run_id="run-2")) == 1


def test_acquire_commits_under_the_runs_current_invocation(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(
        store, fetcher=FakeFetcher(ok_result("https://example.com/source-a"))
    )
    service.acquire(one_source_case(), running_record())
    commit = commit_events(store)[0]
    assert commit.invocation_id == INVOCATION_ID


def test_acquire_requires_a_running_run(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    store.create_run(make_run_record(state=RunState.CREATED, current_invocation_id=None))
    service = SourceAcquisitionService(store, fetcher=FakeFetcher())
    with pytest.raises(RuntimeContractError) as excinfo:
        service.acquire(make_case(), make_run_record(state=RunState.CREATED))
    assert "RUNNING" in str(excinfo.value)


def test_acquire_rejects_case_run_mismatch(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(store, fetcher=FakeFetcher())
    other_case = make_case(case_id="case-other")
    with pytest.raises(RuntimeContractError) as excinfo:
        service.acquire(other_case, running_record())
    assert "case-other" in str(excinfo.value)


def test_acquire_verifies_the_frozen_declaration_digest(tmp_path):
    """Ruling 3: only the Case's frozen inputs/urls.yaml may be acquired; a
    digest mismatch means the frozen declaration is not the text being
    parsed, which is never acquired silently."""
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(store, fetcher=FakeFetcher())
    case = make_case(source_declaration_digest="sha256:" + "0" * 64)
    with pytest.raises(RuntimeContractError) as excinfo:
        service.acquire(case, running_record())
    assert "digest" in str(excinfo.value)


def test_acquire_rejects_unknown_run_in_the_store(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    service = SourceAcquisitionService(store, fetcher=FakeFetcher())
    with pytest.raises(RuntimeContractError) as excinfo:
        service.acquire(make_case(), running_record())
    assert "run-1" in str(excinfo.value)


def test_acquire_requires_case_and_run_records(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    service = SourceAcquisitionService(store, fetcher=FakeFetcher())
    with pytest.raises(RuntimeContractError):
        service.acquire(object(), running_record())  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        service.acquire(make_case(), object())  # type: ignore[arg-type]


def test_acquire_surfaces_declaration_errors(tmp_path):
    """Invalid frozen declarations (here: an unsupported scheme) abort the
    whole acquisition explicitly before anything is fetched."""
    store = FileSystemRuntimeStore(tmp_path)
    build_running_invocation(store)
    urls = "- id: src-1\n  url: ftp://example.com/file\n"
    case = make_case(
        source_declaration_text=urls, source_declaration_digest=sha256_digest(urls)
    )
    service = SourceAcquisitionService(store, fetcher=FakeFetcher())
    with pytest.raises(SourceDeclarationError, match="scheme"):
        service.acquire(case, running_record())
    assert commit_events(store) == ()
