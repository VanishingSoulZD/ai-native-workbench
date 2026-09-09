"""Runtime-local digest utilities (Task 3).

One digest format is used across the Runtime bindings layer::

    sha256:<64 lowercase hex characters>

computed over UTF-8 bytes with hashlib.sha256 (stdlib; the canonical core's
fingerprinting is intentionally NOT imported here — Runtime digesting is a
separate reproducibility concern, Spec section 19).

``payload_digest`` is the deterministic serialization used for Artifact
payloads and configuration items: canonical JSON (``sort_keys=True``,
compact separators, ``ensure_ascii=False``). Deterministic for identical
content; payloads must already be JSON-able (the store persists artifact
documents as JSON). ``sha256_digest`` over the raw file text/bytes is used
by the Case loader so digests cover the file content exactly as approved.
"""

import hashlib
import json

DIGEST_PREFIX = "sha256:"
"""Digest scheme marker used by every runtime binding digest."""

_CANONICAL_DUMPS = dict(sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_digest(value: str | bytes) -> str:
    """Return ``sha256:<hex>`` over the UTF-8 bytes of *value*."""
    data = value.encode("utf-8") if isinstance(value, str) else bytes(value)
    return f"{DIGEST_PREFIX}{hashlib.sha256(data).hexdigest()}"


def payload_digest(value: object) -> str:
    """Return ``sha256:<hex>`` over the canonical JSON of *value*.

    Raises the standard json.dumps TypeError/ValueError for payloads that
    are not JSON-able — such payloads could never be persisted as artifact
    evidence, so the failure is explicit, never silent.
    """
    text = json.dumps(value, **_CANONICAL_DUMPS)
    return sha256_digest(text)
