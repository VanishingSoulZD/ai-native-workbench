"""First-slice canonical research domain objects and intrinsic validation."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from .errors import CanonicalValidationError
from .identity import CanonicalObjectType, CanonicalRef


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CanonicalValidationError(f"{field_name} must be a non-empty string.")


def _require_ref(
    value: object,
    field_name: str,
    expected_type: CanonicalObjectType | None = None,
) -> None:
    if not isinstance(value, CanonicalRef):
        raise CanonicalValidationError(f"{field_name} must be a CanonicalRef.")
    if expected_type is not None and value.object_type is not expected_type:
        raise CanonicalValidationError(
            f"{field_name} must reference a {expected_type.value} object."
        )


def _require_ref_tuple(
    value: object,
    field_name: str,
    expected_type: CanonicalObjectType | None = None,
) -> None:
    if not isinstance(value, tuple):
        raise CanonicalValidationError(f"{field_name} must be a tuple of CanonicalRef values.")
    for reference in value:
        _require_ref(reference, field_name, expected_type)


@dataclass(frozen=True)
class Entity:
    id: str
    entity_type: str
    name: str
    status: str
    attributes: Mapping[str, object]

    def __post_init__(self) -> None:
        for field_name in ("id", "entity_type", "name", "status"):
            _require_non_empty(getattr(self, field_name), field_name)
        if not isinstance(self.attributes, Mapping):
            raise CanonicalValidationError("attributes must be a mapping.")
        object.__setattr__(self, "attributes", MappingProxyType(dict(self.attributes)))

    @property
    def object_type(self) -> CanonicalObjectType:
        return CanonicalObjectType.ENTITY

    @property
    def canonical_ref(self) -> CanonicalRef:
        return CanonicalRef(self.object_type, self.id)


@dataclass(frozen=True)
class Claim:
    id: str
    statement: str
    subject_ref: CanonicalRef
    claim_type: str
    status: str
    confidence: float
    evidence_ids: tuple[CanonicalRef, ...]

    def __post_init__(self) -> None:
        for field_name in ("id", "statement", "status"):
            _require_non_empty(getattr(self, field_name), field_name)
        _require_ref(self.subject_ref, "subject_ref")
        if self.claim_type not in {"factual", "derived"}:
            raise CanonicalValidationError("claim_type must be 'factual' or 'derived'.")
        if (
            not isinstance(self.confidence, (int, float))
            or isinstance(self.confidence, bool)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise CanonicalValidationError("confidence must be between 0.0 and 1.0.")
        _require_ref_tuple(
            self.evidence_ids, "evidence_ids", CanonicalObjectType.EVIDENCE
        )
        if self.claim_type == "factual" and not self.evidence_ids:
            raise CanonicalValidationError("factual claims require at least one evidence reference.")

    @property
    def object_type(self) -> CanonicalObjectType:
        return CanonicalObjectType.CLAIM

    @property
    def canonical_ref(self) -> CanonicalRef:
        return CanonicalRef(self.object_type, self.id)


@dataclass(frozen=True)
class Evidence:
    id: str
    source_id: CanonicalRef
    observation: str
    date_or_period: str
    evidence_type: str
    evidence_grade: str
    supports_claim_ids: tuple[CanonicalRef, ...]
    contradicts_claim_ids: tuple[CanonicalRef, ...]
    note: str

    def __post_init__(self) -> None:
        for field_name in ("id", "observation", "evidence_type", "evidence_grade"):
            _require_non_empty(getattr(self, field_name), field_name)
        _require_ref(self.source_id, "source_id", CanonicalObjectType.SOURCE)
        _require_ref_tuple(
            self.supports_claim_ids,
            "supports_claim_ids",
            CanonicalObjectType.CLAIM,
        )
        _require_ref_tuple(
            self.contradicts_claim_ids,
            "contradicts_claim_ids",
            CanonicalObjectType.CLAIM,
        )
        if not isinstance(self.date_or_period, str):
            raise CanonicalValidationError("date_or_period must be a string.")
        if not isinstance(self.note, str):
            raise CanonicalValidationError("note must be a string.")

    @property
    def object_type(self) -> CanonicalObjectType:
        return CanonicalObjectType.EVIDENCE

    @property
    def canonical_ref(self) -> CanonicalRef:
        return CanonicalRef(self.object_type, self.id)


@dataclass(frozen=True)
class Source:
    id: str
    canonical_title: str
    publisher: str
    canonical_url: str
    source_type: str
    published_at: str
    accessed_at: str
    quality_tier: str

    def __post_init__(self) -> None:
        for field_name in ("id", "canonical_title", "publisher", "canonical_url", "source_type", "quality_tier"):
            _require_non_empty(getattr(self, field_name), field_name)
        for field_name in ("published_at", "accessed_at"):
            if not isinstance(getattr(self, field_name), str):
                raise CanonicalValidationError(f"{field_name} must be a string.")

    @property
    def object_type(self) -> CanonicalObjectType:
        return CanonicalObjectType.SOURCE

    @property
    def canonical_ref(self) -> CanonicalRef:
        return CanonicalRef(self.object_type, self.id)


@dataclass(frozen=True)
class Unknown:
    id: str
    question: str
    why_it_matters: str
    scope: str
    status: str

    def __post_init__(self) -> None:
        for field_name in ("id", "question", "why_it_matters", "scope", "status"):
            _require_non_empty(getattr(self, field_name), field_name)

    @property
    def object_type(self) -> CanonicalObjectType:
        return CanonicalObjectType.UNKNOWN

    @property
    def canonical_ref(self) -> CanonicalRef:
        return CanonicalRef(self.object_type, self.id)


@dataclass(frozen=True)
class Relationship:
    id: str
    subject_ref: CanonicalRef
    predicate: str
    object_ref: CanonicalRef
    evidence_ids: tuple[CanonicalRef, ...]
    status: str

    def __post_init__(self) -> None:
        for field_name in ("id", "predicate", "status"):
            _require_non_empty(getattr(self, field_name), field_name)
        _require_ref(self.subject_ref, "subject_ref")
        _require_ref(self.object_ref, "object_ref")
        _require_ref_tuple(
            self.evidence_ids, "evidence_ids", CanonicalObjectType.EVIDENCE
        )

    @property
    def object_type(self) -> CanonicalObjectType:
        return CanonicalObjectType.RELATIONSHIP

    @property
    def canonical_ref(self) -> CanonicalRef:
        return CanonicalRef(self.object_type, self.id)


CanonicalObject = Entity | Claim | Evidence | Source | Unknown | Relationship
