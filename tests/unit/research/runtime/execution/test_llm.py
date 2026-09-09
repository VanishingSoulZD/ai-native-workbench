"""Tests for the isolated DeepSeek adapter boundary (Task 4, brief Step 5).

The LLM boundary is provider-``deepseek``/model-``deepseek-v4-flash`` only
(architecture doc 7.5): no fallback, no multi-provider routing, no automatic
provider selection. The adapter is thin — provider-specific HTTP details stay
inside one small client — and a transport is injected so tests never touch
the network and never use a real secret (``DEEPSEEK_API_KEY`` is always
monkeypatched to a test-only value or deleted).

Timeout and API failures map to explicit typed errors. The client is a
candidate *producer* only: ``complete`` returns a result record and never
mutates Runtime state. Prompt/schema digest capture pins the exact versioned
content executed (same digest scheme as the Task 3 execution-binding
identity digests), so the orchestrator can compare the executed digests
against the frozen binding.
"""

import hashlib
import json
from dataclasses import FrozenInstanceError

import pytest

from ai_native_workbench.research.runtime.execution.llm import (
    DEEPSEEK_API_KEY_ENV,
    DEEPSEEK_ENDPOINT,
    DEEPSEEK_MODEL,
    DEEPSEEK_PROVIDER,
    CompletionRequest,
    CompletionResult,
    DeepSeekAPIError,
    DeepSeekClient,
    DeepSeekConfigurationError,
    DeepSeekError,
    DeepSeekResponseError,
    DeepSeekTimeoutError,
    DeepSeekTransportError,
    UrllibTransport,
)
from ai_native_workbench.research.runtime.domain import RuntimeContractError

PROMPT_IDENTITY = "prompt-r1"
PROMPT_VERSION = "1"
PROMPT_TEXT = "Synthesize the evidence for the research question."
SCHEMA_IDENTITY = "evidence-set"
SCHEMA_VERSION = "1"
SCHEMA_TEXT = '{"kind": "evidence-set", "inputs": ["array"]}'
RESULT_TEXT = "Two landscape clusters emerged."

OK_BODY = json.dumps(
    {
        "id": "cmpl-test-1",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": RESULT_TEXT}}],
        "model": DEEPSEEK_MODEL,
    }
).encode("utf-8")


def _independent_digest(content: str, identity: str, version: str) -> str:
    """Re-pin the runtime digest scheme with stdlib only (canonical JSON of
    the {identity, version, content} triple, sha256:<hex>)."""
    text = json.dumps(
        {"identity": identity, "version": version, "content": content},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


class FakeTransport:
    """The brief-mandated fake transport: records the request, returns a
    canned response or raises a configured transport-level error."""

    def __init__(self):
        self.calls: list[tuple[str, dict, dict, float]] = []
        self.status_code = 200
        self.body = OK_BODY
        self.error: Exception | None = None

    def post(self, url, headers, payload, timeout):
        self.calls.append((url, dict(headers), dict(payload), timeout))
        if self.error is not None:
            raise self.error
        return self.status_code, self.body


@pytest.fixture
def fake_transport() -> FakeTransport:
    return FakeTransport()


def make_request(**overrides) -> CompletionRequest:
    defaults = dict(
        prompt_identity=PROMPT_IDENTITY,
        prompt_version=PROMPT_VERSION,
        prompt=PROMPT_TEXT,
        schema_identity=SCHEMA_IDENTITY,
        schema_version=SCHEMA_VERSION,
        schema_content=SCHEMA_TEXT,
    )
    defaults.update(overrides)
    return CompletionRequest(**defaults)


def make_client(fake_transport, monkeypatch, **overrides) -> DeepSeekClient:
    monkeypatch.setenv(DEEPSEEK_API_KEY_ENV, "test-only")
    return DeepSeekClient(fake_transport, **overrides)


# ---------------------------------------------------------------------------
# Provider/model boundary (brief Step 5 snippet verbatim shape)
# ---------------------------------------------------------------------------


def test_deepseek_adapter_records_provider_and_model(fake_transport, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-only")
    result = DeepSeekClient(fake_transport).complete(make_request())
    assert result.provider == "deepseek"
    assert result.model == "deepseek-v4-flash"


def test_provider_constants_are_deepseek_only():
    assert DEEPSEEK_PROVIDER == "deepseek"
    assert DEEPSEEK_MODEL == "deepseek-v4-flash"
    assert DEEPSEEK_API_KEY_ENV == "DEEPSEEK_API_KEY"


def test_client_sends_model_messages_and_auth_header(fake_transport, monkeypatch):
    client = make_client(fake_transport, monkeypatch)
    result = client.complete(make_request())
    assert result.text == RESULT_TEXT

    url, headers, payload, timeout = fake_transport.calls[0]
    assert url == DEEPSEEK_ENDPOINT
    assert headers["Authorization"] == "Bearer test-only"
    assert headers["Content-Type"] == "application/json"
    assert payload["model"] == "deepseek-v4-flash"
    roles = [message["role"] for message in payload["messages"]]
    assert roles == ["system", "user"]
    assert payload["messages"][0]["content"] == SCHEMA_TEXT
    assert payload["messages"][1]["content"] == PROMPT_TEXT


def test_client_sends_no_system_message_without_declared_schema(
    fake_transport, monkeypatch
):
    client = make_client(fake_transport, monkeypatch)
    request = make_request(schema_identity=None, schema_version=None, schema_content=None)
    client.complete(request)
    _, _, payload, _ = fake_transport.calls[0]
    assert [message["role"] for message in payload["messages"]] == ["user"]


def test_completion_result_records_prompt_and_schema_digests(
    fake_transport, monkeypatch
):
    result = make_client(fake_transport, monkeypatch).complete(make_request())
    assert result.prompt_digest == _independent_digest(
        PROMPT_TEXT, PROMPT_IDENTITY, PROMPT_VERSION
    )
    assert result.schema_digest == _independent_digest(
        SCHEMA_TEXT, SCHEMA_IDENTITY, SCHEMA_VERSION
    )
    # No schema in the request -> no schema digest in the result.
    request = make_request(schema_identity=None, schema_version=None, schema_content=None)
    result = make_client(fake_transport, monkeypatch).complete(request)
    assert result.schema_digest is None
    assert result.prompt_digest == _independent_digest(
        PROMPT_TEXT, PROMPT_IDENTITY, PROMPT_VERSION
    )


# ---------------------------------------------------------------------------
# Timeout / API / transport failure mapping (brief Step 5)
# ---------------------------------------------------------------------------


def test_client_maps_transport_timeout_to_explicit_error(fake_transport, monkeypatch):
    fake_transport.error = TimeoutError("timed out")
    client = make_client(fake_transport, monkeypatch)
    with pytest.raises(DeepSeekTimeoutError) as excinfo:
        client.complete(make_request())
    assert "timed out" in str(excinfo.value)


def test_client_maps_oserror_transport_failures(fake_transport, monkeypatch):
    fake_transport.error = OSError("connection refused")
    client = make_client(fake_transport, monkeypatch)
    with pytest.raises(DeepSeekTransportError) as excinfo:
        client.complete(make_request())
    assert "connection refused" in str(excinfo.value)


def test_client_maps_api_error_status_and_provider_message(fake_transport, monkeypatch):
    fake_transport.status_code = 401
    fake_transport.body = json.dumps(
        {"error": {"message": "rate limited", "type": "rate_limit", "code": "401"}}
    ).encode("utf-8")
    client = make_client(fake_transport, monkeypatch)
    with pytest.raises(DeepSeekAPIError) as excinfo:
        client.complete(make_request())
    assert excinfo.value.status_code == 401
    assert "rate limited" in str(excinfo.value)


def test_client_maps_api_error_without_parseable_body(fake_transport, monkeypatch):
    fake_transport.status_code = 500
    fake_transport.body = b"<html>gateway error</html>"
    client = make_client(fake_transport, monkeypatch)
    with pytest.raises(DeepSeekAPIError) as excinfo:
        client.complete(make_request())
    assert excinfo.value.status_code == 500


def test_client_maps_malformed_success_responses(fake_transport, monkeypatch):
    client = make_client(fake_transport, monkeypatch)
    fake_transport.body = b"not json at all"
    with pytest.raises(DeepSeekResponseError):
        client.complete(make_request())
    fake_transport.body = json.dumps({"id": "x"}).encode("utf-8")  # no choices
    with pytest.raises(DeepSeekResponseError):
        client.complete(make_request())
    fake_transport.body = json.dumps(
        {"choices": [{"index": 0, "message": {"role": "assistant"}}]}
    ).encode("utf-8")  # no content field
    with pytest.raises(DeepSeekResponseError):
        client.complete(make_request())


def test_error_family_is_catchable_as_deepseek_error(fake_transport, monkeypatch):
    fake_transport.status_code = 429
    client = make_client(fake_transport, monkeypatch)
    try:
        client.complete(make_request())
    except Exception as exc:  # noqa: BLE001 - the family base is asserted
        assert type(exc) is DeepSeekAPIError
        assert isinstance(exc, DeepSeekError)
    else:
        pytest.fail("expected an API error")


# ---------------------------------------------------------------------------
# Secret handling and configuration
# ---------------------------------------------------------------------------


def test_client_refuses_to_start_without_api_key(fake_transport, monkeypatch):
    monkeypatch.delenv(DEEPSEEK_API_KEY_ENV, raising=False)
    with pytest.raises(DeepSeekConfigurationError):
        DeepSeekClient(fake_transport)


def test_client_never_uses_a_real_secret(fake_transport, monkeypatch):
    """The only key the client ever sees is the monkeypatched test value;
    the real environment secret is deleted before construction."""
    monkeypatch.delenv(DEEPSEEK_API_KEY_ENV, raising=False)
    client = DeepSeekClient(fake_transport, api_key="test-only")
    client.complete(make_request())
    _, headers, _, _ = fake_transport.calls[0]
    assert headers["Authorization"] == "Bearer test-only"
    assert DEEPSEEK_API_KEY_ENV not in headers["Authorization"]


def test_client_explicit_api_key_wins_over_environment(fake_transport, monkeypatch):
    monkeypatch.setenv(DEEPSEEK_API_KEY_ENV, "env-secret")
    client = DeepSeekClient(fake_transport, api_key="explicit-test-key")
    client.complete(make_request())
    _, headers, _, _ = fake_transport.calls[0]
    assert headers["Authorization"] == "Bearer explicit-test-key"


def test_client_rejects_missing_transport():
    with pytest.raises(DeepSeekConfigurationError):
        DeepSeekClient(None, api_key="test-only")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Request / result records
# ---------------------------------------------------------------------------


def test_completion_request_validation():
    with pytest.raises(RuntimeContractError):
        CompletionRequest(prompt_identity="", prompt_version="1", prompt="x")
    with pytest.raises(RuntimeContractError):
        CompletionRequest(prompt_identity="p", prompt_version="1", prompt="")
    # The declared schema must arrive as a full (identity, version, content)
    # triple or not at all.
    with pytest.raises(RuntimeContractError):
        CompletionRequest(
            prompt_identity="p",
            prompt_version="1",
            prompt="x",
            schema_identity=SCHEMA_IDENTITY,
        )
    with pytest.raises(RuntimeContractError):
        CompletionRequest(
            prompt_identity="p",
            prompt_version="1",
            prompt="x",
            schema_content=SCHEMA_TEXT,
        )
    request = CompletionRequest(
        prompt_identity="p",
        prompt_version="1",
        prompt="x",
        schema_identity=None,
        schema_version=None,
        schema_content=None,
    )
    assert request.schema_content is None


def test_completion_result_is_frozen():
    result = CompletionResult(
        provider=DEEPSEEK_PROVIDER,
        model=DEEPSEEK_MODEL,
        text=RESULT_TEXT,
        prompt_digest="sha256:" + "a" * 64,
    )
    assert result.provider == "deepseek"
    assert result.model == "deepseek-v4-flash"
    assert result.schema_digest is None
    with pytest.raises(FrozenInstanceError):
        result.text = "tampered"


def test_completion_result_validation():
    with pytest.raises(RuntimeContractError):
        CompletionResult(
            provider="",
            model=DEEPSEEK_MODEL,
            text=RESULT_TEXT,
            prompt_digest="sha256:" + "a" * 64,
        )
    with pytest.raises(RuntimeContractError):
        CompletionResult(
            provider=DEEPSEEK_PROVIDER,
            model="",
            text=RESULT_TEXT,
            prompt_digest="",
        )


def test_client_requires_a_completion_request(fake_transport, monkeypatch):
    client = make_client(fake_transport, monkeypatch)
    with pytest.raises(RuntimeContractError):
        client.complete(object())  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Real transport shape (contract only: never touches the network here)
# ---------------------------------------------------------------------------


def test_urllib_transport_exists_as_the_real_transport_implementation():
    """The stdlib transport is the injected transport's real counterpart; its
    network behavior is a manual/smoke concern (spec 7.2), never exercised in
    this suite. The client accepts it through the same protocol."""
    client = DeepSeekClient(UrllibTransport(), api_key="test-only")
    assert client is not None
