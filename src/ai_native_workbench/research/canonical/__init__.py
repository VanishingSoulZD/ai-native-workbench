"""Public interfaces for canonical knowledge objects and identity."""

from .errors import (
    CanonicalError,
    CanonicalValidationError,
    IntegrityError,
    RegistryError,
    ResolutionError,
    SnapshotError,
)
from .model import CanonicalObject, Claim, Entity, Evidence, Relationship, Source, Unknown
from .registry import CanonicalRegistry

from .identity import (
    CanonicalObjectType,
    CanonicalRef,
    canonical_fingerprint,
    canonical_serialize,
)

__all__ = [
    "CanonicalError",
    "CanonicalObject",
    "CanonicalObjectType",
    "CanonicalRef",
    "CanonicalRegistry",
    "CanonicalValidationError",
    "Claim",
    "Entity",
    "Evidence",
    "IntegrityError",
    "RegistryError",
    "ResolutionError",
    "Relationship",
    "SnapshotError",
    "Source",
    "Unknown",
    "canonical_fingerprint",
    "canonical_serialize",
]
