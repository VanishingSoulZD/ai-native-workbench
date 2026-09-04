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
from .provenance import validate_object_references, validate_registry_integrity
from .registry import CanonicalRegistry
from .snapshot import ResearchSnapshot

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
    "ResearchSnapshot",
    "Relationship",
    "SnapshotError",
    "Source",
    "Unknown",
    "canonical_fingerprint",
    "validate_object_references",
    "validate_registry_integrity",
    "canonical_serialize",
]
