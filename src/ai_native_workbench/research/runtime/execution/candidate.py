"""CandidateOutput — the frozen structured result of an executor run (Task 4).

A Candidate is the unit the acceptance pipeline evaluates and the
orchestrator may commit: content must be a JSON object (deep-frozen and
immutable, but JSON-serializable exactly as stored — the artifact-commit
digest path canonicalizes candidate content), it declares the schema
identity/version its content conforms to (the v1 schema seam: identity +
version, no schema framework), and it carries provenance facts (a tuple of
non-empty strings such as ``input:<artifact id>`` and ``mode:<executor
mode>``).

Content immutability is enforced by a private frozen ``dict`` subclass, not
by ``MappingProxyType``: ``runtime.digests.payload_digest`` serializes with
``json.dumps``, which rejects mapping proxies, so the frozen object keeps
plain-dict serialization while every mutator raises ``TypeError``.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass

from ..domain import RuntimeContractError


class _FrozenJSONObject(dict):
    """A deep-frozen JSON object: reads and digests behave like a dict;
    every mutation raises TypeError."""

    _MUTATION_MESSAGE = "candidate content is immutable."

    def __setitem__(self, key: object, value: object) -> None:
        raise TypeError(self._MUTATION_MESSAGE)

    def __delitem__(self, key: object) -> None:
        raise TypeError(self._MUTATION_MESSAGE)

    def clear(self) -> None:  # type: ignore[override]
        raise TypeError(self._MUTATION_MESSAGE)

    def pop(self, *args: object):  # type: ignore[override]
        raise TypeError(self._MUTATION_MESSAGE)

    def popitem(self):  # type: ignore[override]
        raise TypeError(self._MUTATION_MESSAGE)

    def setdefault(self, *args: object):  # type: ignore[override]
        raise TypeError(self._MUTATION_MESSAGE)

    def update(self, *args: object, **kwargs: object) -> None:  # type: ignore[override]
        raise TypeError(self._MUTATION_MESSAGE)


def _freeze_json_object(value: object, path: str) -> object:
    """Recursively freeze one JSON-able structure, validating JSON-ability.

    Mappings become ``_FrozenJSONObject`` instances (string keys only),
    arrays become tuples, scalars pass through; non-JSON values (objects,
    non-finite floats, non-string keys) raise ``RuntimeContractError``.
    The frozen structure serializes to the identical canonical JSON as the
    original, so digests are unaffected by the freeze.
    """
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RuntimeContractError(
                f"{path} contains a non-finite number; candidate content "
                "must be JSON-serializable."
            )
        return value
    if isinstance(value, Mapping):
        items: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise RuntimeContractError(
                    f"{path} keys must be strings; candidate content must be "
                    "JSON-serializable."
                )
            items[key] = _freeze_json_object(item, f"{path}[{key!r}]")
        # dict.__init__ on the subclass bypasses the frozen __setitem__.
        return _FrozenJSONObject(items)
    if isinstance(value, (list, tuple)):
        return tuple(
            _freeze_json_object(item, f"{path}[{index}]")
            for index, item in enumerate(value)
        )
    raise RuntimeContractError(
        f"{path} contains a value that is not JSON-serializable "
        f"({type(value).__name__})."
    )


@dataclass(frozen=True)
class CandidateOutput:
    """One executor-produced candidate: frozen content, declared schema,
    provenance facts. Keyword-constructed; records never mutate."""

    content: Mapping[str, object]
    schema_identity: str
    schema_version: str
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.content, Mapping):
            raise RuntimeContractError(
                "candidate content must be a JSON object mapping."
            )
        object.__setattr__(
            self, "content", _freeze_json_object(self.content, "content")
        )
        for name in ("schema_identity", "schema_version"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeContractError(f"{name} must be a non-empty string.")
        if not isinstance(self.provenance, tuple):
            raise RuntimeContractError(
                "provenance must be a tuple of non-empty strings."
            )
        seen: set[str] = set()
        for fact in self.provenance:
            if not isinstance(fact, str) or not fact.strip():
                raise RuntimeContractError(
                    "provenance entries must be non-empty strings."
                )
            if fact in seen:
                raise RuntimeContractError(
                    "provenance must not contain duplicates."
                )
            seen.add(fact)
