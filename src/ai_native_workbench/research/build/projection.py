"""Pure, deterministic projections from resolved canonical state."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from ..canonical import CanonicalRef, Claim, Entity, Evidence, Relationship, Source, Unknown
from .engine import ResolvedSnapshot
from .errors import BuildValidationError


def _freeze_mapping(value: Mapping[str, object]) -> Mapping[str, object]:
    return MappingProxyType(dict(value))


def _reference_strings(references: tuple[CanonicalRef, ...]) -> tuple[str, ...]:
    return tuple(str(reference) for reference in references)


@dataclass(frozen=True)
class DatasetRow:
    ref: CanonicalRef
    object_type: str
    logical_id: str
    fields: Mapping[str, object]

    def __post_init__(self) -> None:
        if not isinstance(self.ref, CanonicalRef):
            raise BuildValidationError("DatasetRow.ref must be a CanonicalRef.")
        object.__setattr__(self, "fields", _freeze_mapping(self.fields))


@dataclass(frozen=True)
class DatasetProjection:
    version: str
    rows: tuple[DatasetRow, ...]


@dataclass(frozen=True)
class ResearchNoteSection:
    heading: str
    paragraphs: tuple[str, ...]
    refs: tuple[CanonicalRef, ...]


@dataclass(frozen=True)
class ResearchNoteProjection:
    version: str
    sections: tuple[ResearchNoteSection, ...]


def _dataset_fields(obj: object) -> Mapping[str, object]:
    if isinstance(obj, Entity):
        return {"id": obj.id, "name": obj.name, "entity_type": obj.entity_type, "status": obj.status, "attributes": obj.attributes}
    if isinstance(obj, Claim):
        return {"id": obj.id, "statement": obj.statement, "claim_type": obj.claim_type, "status": obj.status, "confidence": obj.confidence, "evidence_refs": _reference_strings(obj.evidence_ids), "subject_ref": str(obj.subject_ref)}
    if isinstance(obj, Evidence):
        return {"id": obj.id, "observation": obj.observation, "date_or_period": obj.date_or_period, "evidence_type": obj.evidence_type, "evidence_grade": obj.evidence_grade, "source_ref": str(obj.source_id), "supports_claim_refs": _reference_strings(obj.supports_claim_ids), "contradicts_claim_refs": _reference_strings(obj.contradicts_claim_ids), "note": obj.note}
    if isinstance(obj, Source):
        return {"id": obj.id, "canonical_title": obj.canonical_title, "publisher": obj.publisher, "canonical_url": obj.canonical_url, "source_type": obj.source_type, "published_at": obj.published_at, "accessed_at": obj.accessed_at, "quality_tier": obj.quality_tier}
    if isinstance(obj, Unknown):
        return {"id": obj.id, "question": obj.question, "why_it_matters": obj.why_it_matters, "scope": obj.scope, "status": obj.status}
    if isinstance(obj, Relationship):
        return {"id": obj.id, "subject_ref": str(obj.subject_ref), "predicate": obj.predicate, "object_ref": str(obj.object_ref), "evidence_refs": _reference_strings(obj.evidence_ids), "status": obj.status}
    raise BuildValidationError("Unsupported canonical object for dataset projection.")


def project_dataset(resolved: ResolvedSnapshot, version: str = "1") -> DatasetProjection:
    rows = tuple(DatasetRow(ref, ref.object_type.value, ref.logical_id, _dataset_fields(obj)) for ref, obj in sorted(resolved.states.items(), key=lambda item: str(item[0])))
    return DatasetProjection(version, rows)


def project_research_note(resolved: ResolvedSnapshot, version: str = "1") -> ResearchNoteProjection:
    snapshot = resolved.snapshot
    items = sorted(resolved.states.items(), key=lambda item: str(item[0]))
    claims = [(ref, obj) for ref, obj in items if isinstance(obj, Claim) and obj.claim_type == "factual"]
    unknowns = [(ref, obj) for ref, obj in items if isinstance(obj, Unknown)]
    sources = [(ref, obj) for ref, obj in items if isinstance(obj, Source)]
    findings = tuple(f"{claim.statement} (claim type: {claim.claim_type}; status: {claim.status}; confidence: {claim.confidence}; evidence: {', '.join(_reference_strings(claim.evidence_ids))})" for _, claim in claims)
    return ResearchNoteProjection(version, (
        ResearchNoteSection("Research Context", (f"Case: {snapshot.case_id}", f"Cutoff: {snapshot.cutoff}", f"Snapshot: {snapshot.snapshot_id}"), ()),
        ResearchNoteSection("Key Findings", findings, tuple(ref for ref, _ in claims)),
        ResearchNoteSection("Unknowns / Limitations", tuple(f"{unknown.question} — {unknown.why_it_matters}" for _, unknown in unknowns), tuple(ref for ref, _ in unknowns)),
        ResearchNoteSection("Provenance", tuple(f"{source.canonical_title} — {source.canonical_url}" for _, source in sources), tuple(ref for ref, _ in sources)),
    ))
