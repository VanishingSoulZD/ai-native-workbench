"""Stable canonical references and deterministic state fingerprints."""

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import hashlib
import json
from collections.abc import Mapping, Sequence

from .errors import CanonicalValidationError


class CanonicalObjectType(str, Enum):
    """The six canonical object types in the first implementation slice."""

    ENTITY = "entity"
    CLAIM = "claim"
    EVIDENCE = "evidence"
    SOURCE = "source"
    UNKNOWN = "unknown"
    RELATIONSHIP = "relationship"


@dataclass(frozen=True)
class CanonicalRef:
    """A typed, stable logical identity for a canonical object."""

    object_type: CanonicalObjectType
    logical_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.object_type, CanonicalObjectType):
            raise CanonicalValidationError("CanonicalRef object_type must be a CanonicalObjectType.")
        if not isinstance(self.logical_id, str) or not self.logical_id.strip():
            raise CanonicalValidationError("CanonicalRef logical_id must not be empty.")
        if ":" in self.logical_id:
            raise CanonicalValidationError("CanonicalRef logical_id must not contain ':'.")

    def __str__(self) -> str:
        return f"{self.object_type.value}:{self.logical_id}"

    @classmethod
    def parse(cls, value: str) -> "CanonicalRef":
        """Parse the sole canonical reference wire representation."""
        if not isinstance(value, str) or value.count(":") != 1:
            raise CanonicalValidationError(f"Invalid CanonicalRef: {value!r}.")
        object_type_value, logical_id = value.split(":", 1)
        try:
            object_type = CanonicalObjectType(object_type_value)
        except ValueError as error:
            raise CanonicalValidationError(
                f"Unknown canonical object type: {object_type_value!r}."
            ) from error
        return cls(object_type, logical_id)


def canonical_serialize(value: object) -> str:
    """Return a compact, deterministic JSON representation of supported values."""
    try:
        return json.dumps(
            _normalize(value),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise CanonicalValidationError("Value cannot be canonically serialized.") from error


def canonical_fingerprint(value: object) -> str:
    """Return the SHA-256 fingerprint of a canonical serialization."""
    payload = canonical_serialize(value).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _normalize(value: object) -> object:
    if isinstance(value, Enum):
        return _normalize(value.value)
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _normalize(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        normalized: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalValidationError("Canonical mapping keys must be strings.")
            normalized[key] = _normalize(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise CanonicalValidationError(
        f"Unsupported value for canonical serialization: {type(value).__name__}."
    )
