"""The isolated DeepSeek adapter boundary (Task 4, brief Steps 5-6).

The Runtime LLM boundary is provider-``deepseek`` / model-
``deepseek-v4-flash`` only (architecture spec 7.5): no fallback provider, no
multi-provider routing, no automatic provider selection. Everything
provider-specific stays inside this one thin client, and the HTTP transport
is injected behind a small protocol, so tests exercise the client with
fakes and never touch the network or a real secret (``DEEPSEEK_API_KEY`` is
read once, at construction).

``DeepSeekClient.complete`` is a pure producer: it returns a frozen result
record and never mutates Runtime state. Timeout, transport and API failures
map to the explicit ``DeepSeekError`` family; result records validate their
own shape with the Runtime contract error. Prompt/schema digest capture
pins the exact versioned content executed — the same digest scheme as the
Task 3 execution-binding identity digests — so the orchestrator can compare
executed digests against the frozen binding.
"""

import json
import os
import urllib.error
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from ..digests import payload_digest
from ..domain import RuntimeContractError

DEEPSEEK_PROVIDER = "deepseek"
"""The single provider this adapter talks to (spec 7.5)."""

DEEPSEEK_MODEL = "deepseek-v4-flash"
"""The single model every completion request uses (spec 7.5)."""

DEEPSEEK_API_KEY_ENV = "DEEPSEEK_API_KEY"
"""Environment variable holding the API key; read once at construction."""

DEEPSEEK_ENDPOINT = "https://api.deepseek.com/chat/completions"
"""Chat completions endpoint the client posts to."""

_DEFAULT_TIMEOUT_SECONDS = 60.0


def _require_text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeContractError(f"{name} must be a non-empty string.")


def _require_optional_text(value: object, name: str) -> None:
    if value is not None:
        _require_text(value, name)


@dataclass(frozen=True)
class CompletionRequest:
    """The versioned prompt/schema content sent to the model.

    ``schema_*`` describe the output schema the model is asked to conform
    to and must arrive as a full (identity, version, content) triple or not
    at all — a partial declaration would break digest pinning.
    """

    prompt_identity: str
    prompt_version: str
    prompt: str
    schema_identity: str | None = None
    schema_version: str | None = None
    schema_content: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.prompt_identity, "prompt_identity")
        _require_text(self.prompt_version, "prompt_version")
        _require_text(self.prompt, "prompt")
        triple = (self.schema_identity, self.schema_version, self.schema_content)
        if all(value is None for value in triple):
            return
        if any(value is None for value in triple):
            raise RuntimeContractError(
                "schema_identity, schema_version and schema_content must be "
                "given together or not at all."
            )
        for name in ("schema_identity", "schema_version", "schema_content"):
            _require_text(getattr(self, name), name)


@dataclass(frozen=True)
class CompletionResult:
    """The produced text plus digest pins of exactly what was executed."""

    provider: str
    model: str
    text: str
    prompt_digest: str
    schema_digest: str | None = None

    def __post_init__(self) -> None:
        for name in ("provider", "model", "text", "prompt_digest"):
            _require_text(getattr(self, name), name)
        _require_optional_text(self.schema_digest, "schema_digest")


class DeepSeekError(Exception):
    """Base class of every explicit DeepSeek adapter failure."""


class DeepSeekConfigurationError(DeepSeekError):
    """Missing API key or transport — the client refuses to start."""


class DeepSeekTransportError(DeepSeekError):
    """The transport could not reach the provider."""


class DeepSeekTimeoutError(DeepSeekTransportError):
    """The provider request timed out (mapped from TimeoutError)."""


class DeepSeekAPIError(DeepSeekError):
    """The provider answered with a non-success HTTP status."""

    def __init__(self, status_code: int, message: str | None = None) -> None:
        self.status_code = status_code
        if message:
            super().__init__(
                f"DeepSeek API error (HTTP {status_code}): {message}"
            )
        else:
            super().__init__(f"DeepSeek API error (HTTP {status_code}).")


class DeepSeekResponseError(DeepSeekError):
    """A success status carried a malformed completion response."""


class DeepSeekTransport(Protocol):
    """The injected HTTP transport contract.

    ``post`` returns ``(status_code, body bytes)`` and raises OSError/
    TimeoutError for transport-level failures; the client maps those into
    the typed DeepSeek error family.
    """

    def post(
        self,
        url: str,
        headers: dict[str, str],
        payload: Mapping[str, object],
        timeout: float,
    ) -> tuple[int, bytes]: ...


class UrllibTransport:
    """The real stdlib transport behind the injected-transport seam.

    HTTP error statuses are returned as ``(status, body)`` pairs rather
    than raised, so the client's API-error mapping sees provider bodies.
    Network behavior is a manual/smoke concern (spec 7.2) — automated
    suites inject fakes and never touch the network.
    """

    def post(
        self,
        url: str,
        headers: dict[str, str],
        payload: Mapping[str, object],
        timeout: float,
    ) -> tuple[int, bytes]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return int(response.status), response.read()
        except urllib.error.HTTPError as exc:
            return int(exc.code), exc.read()


def _content_digest(identity: str, version: str, content: str) -> str:
    """Digest pin over the {identity, version, content} triple (Runtime
    scheme, sha256:<hex> over canonical JSON)."""
    return payload_digest(
        {"identity": identity, "version": version, "content": content}
    )


def _api_error_message(body: bytes) -> str | None:
    """Best-effort extraction of the provider error message from the body."""
    try:
        document = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(document, dict):
        return None
    error = document.get("error")
    if not isinstance(error, dict):
        return None
    message = error.get("message")
    if isinstance(message, str) and message.strip():
        return message
    return None


def _completion_text(body: bytes) -> str:
    """Extract choices[0].message.content from a successful response."""
    try:
        document = json.loads(body.decode("utf-8"))
        content = document["choices"][0]["message"]["content"]
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        raise DeepSeekResponseError(
            "DeepSeek response is malformed: expected JSON with "
            f"choices[0].message.content ({exc})."
        ) from exc
    if not isinstance(content, str) or not content.strip():
        raise DeepSeekResponseError(
            "DeepSeek response carried an empty completion content."
        )
    return content


class DeepSeekClient:
    """Thin DeepSeek completion client: one provider, one model, no
    fallback. Reads the API key from the environment at construction only."""

    def __init__(
        self,
        transport: DeepSeekTransport | None,
        *,
        api_key: str | None = None,
    ) -> None:
        if transport is None:
            raise DeepSeekConfigurationError(
                "DeepSeekClient requires an injected transport."
            )
        if api_key is None:
            api_key = os.environ.get(DEEPSEEK_API_KEY_ENV)
        if not isinstance(api_key, str) or not api_key.strip():
            raise DeepSeekConfigurationError(
                f"No DeepSeek API key: set the {DEEPSEEK_API_KEY_ENV} "
                "environment variable or pass api_key."
            )
        self._transport = transport
        self._api_key = api_key

    def complete(self, request: CompletionRequest) -> CompletionResult:
        """Send *request* to the provider and return the frozen result.

        Never mutates Runtime state. Raises DeepSeekConfigurationError
        never (configuration is checked at construction); DeepSeekTimeout
        /Transport/API/Response errors cover every failure after that.
        """
        if not isinstance(request, CompletionRequest):
            raise RuntimeContractError("complete requires a CompletionRequest.")
        messages = []
        if request.schema_content is not None:
            messages.append({"role": "system", "content": request.schema_content})
        messages.append({"role": "user", "content": request.prompt})
        payload: dict[str, object] = {
            "model": DEEPSEEK_MODEL,
            "messages": messages,
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        try:
            status_code, body = self._transport.post(
                DEEPSEEK_ENDPOINT, headers, payload, _DEFAULT_TIMEOUT_SECONDS
            )
        except TimeoutError as exc:
            raise DeepSeekTimeoutError(
                f"DeepSeek request timed out: {exc}"
            ) from exc
        except OSError as exc:
            raise DeepSeekTransportError(
                f"DeepSeek transport failure: {exc}"
            ) from exc
        if not 200 <= status_code < 300:
            raise DeepSeekAPIError(status_code, _api_error_message(body))
        prompt_digest = _content_digest(
            request.prompt_identity, request.prompt_version, request.prompt
        )
        schema_digest = None
        if request.schema_content is not None:
            schema_digest = _content_digest(
                request.schema_identity or "",
                request.schema_version or "",
                request.schema_content,
            )
        return CompletionResult(
            provider=DEEPSEEK_PROVIDER,
            model=DEEPSEEK_MODEL,
            text=_completion_text(body),
            prompt_digest=prompt_digest,
            schema_digest=schema_digest,
        )
