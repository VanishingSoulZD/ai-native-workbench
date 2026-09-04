"""End-to-end validation for a self-contained synthetic canonical research case."""

import pytest

from ai_native_workbench.research.canonical import (
    CanonicalObjectType,
    CanonicalRef,
    CanonicalRegistry,
    Claim,
    Entity,
    Evidence,
    Relationship,
    ResearchSnapshot,
    SnapshotError,
    Source,
    Unknown,
    canonical_fingerprint,
)


def test_synthetic_research_case_preserves_provenance_and_historical_snapshot():
    """Validate the complete canonical research loop without Case 001 dependencies."""
    registry = CanonicalRegistry()
    source = Source(
        id="source-official-1",
        canonical_title="Product X Official Documentation",
        publisher="Example Vendor",
        canonical_url="https://example.com/product-x/docs",
        source_type="official-documentation",
        published_at="2026-08-20",
        accessed_at="2026-09-03",
        quality_tier="A",
    )
    entity = Entity(
        id="product-x",
        entity_type="product",
        name="Product X",
        status="active",
        attributes={"category": "developer-tool"},
    )
    claim_ref = CanonicalRef(CanonicalObjectType.CLAIM, "claim-indexing-1")
    evidence_ref = CanonicalRef(CanonicalObjectType.EVIDENCE, "evidence-indexing-1")
    evidence = Evidence(
        id="evidence-indexing-1",
        source_id=source.canonical_ref,
        observation="The official documentation describes repository indexing support.",
        date_or_period="2026-08-20",
        evidence_type="documentation",
        evidence_grade="A",
        supports_claim_ids=(claim_ref,),
        contradicts_claim_ids=(),
        note="Direct product documentation observation.",
    )
    claim_v1 = Claim(
        id="claim-indexing-1",
        statement="Product X supports repository indexing.",
        subject_ref=entity.canonical_ref,
        claim_type="factual",
        status="active",
        confidence=0.95,
        evidence_ids=(evidence_ref,),
    )
    unknown = Unknown(
        id="unknown-region-support",
        question="Does Product X support region Y?",
        why_it_matters="Regional availability affects recommendation validity.",
        scope="Product X public availability information.",
        status="unresolved",
    )
    relationship = Relationship(
        id="relationship-product-indexing",
        subject_ref=entity.canonical_ref,
        predicate="has_capability",
        object_ref=claim_v1.canonical_ref,
        evidence_ids=(evidence_ref,),
        status="active",
    )

    for obj in (source, entity, evidence, claim_v1, unknown, relationship):
        assert registry.register(obj) == obj.canonical_ref
    registry.validate()

    for obj in (source, entity, evidence, claim_v1, unknown, relationship):
        assert registry.get(obj.canonical_ref) == obj
        assert registry.resolve(obj.canonical_ref) == registry.get(obj.canonical_ref)
    assert unknown.object_type is CanonicalObjectType.UNKNOWN

    claim_v1_fingerprint = canonical_fingerprint(claim_v1)
    snapshot_refs = (
        source.canonical_ref,
        entity.canonical_ref,
        evidence.canonical_ref,
        claim_v1.canonical_ref,
        unknown.canonical_ref,
        relationship.canonical_ref,
    )
    snapshot = registry.snapshot(
        "synthetic-snapshot-1",
        snapshot_refs,
        case_id="synthetic-step3-case",
        cutoff="2026-09-03",
        workflow_version="research-v1",
        schema_version="1",
        transformation_version="1",
        status="draft",
    )

    assert len(snapshot.refs()) == 6
    assert set(snapshot.members) == set(snapshot_refs)
    assert snapshot.fingerprint_for(claim_v1.canonical_ref) == claim_v1_fingerprint

    claim_v2 = Claim(
        id=claim_v1.id,
        statement=claim_v1.statement,
        subject_ref=entity.canonical_ref,
        claim_type="factual",
        status="deprecated",
        confidence=0.90,
        evidence_ids=(evidence_ref,),
    )
    claim_v2_fingerprint = registry.replace(claim_v1.canonical_ref, claim_v2)

    assert claim_v2_fingerprint != claim_v1_fingerprint
    assert registry.get(claim_v1.canonical_ref) == claim_v2
    assert registry.get_state(claim_v1.canonical_ref, claim_v1_fingerprint) == claim_v1
    assert snapshot.fingerprint_for(claim_v1.canonical_ref) == claim_v1_fingerprint
    assert snapshot.resolve(registry, claim_v1.canonical_ref) == claim_v1
    assert snapshot.resolve(registry, unknown.canonical_ref) == unknown
    registry.validate()

    invalid_snapshot = ResearchSnapshot(
        snapshot_id="synthetic-invalid-snapshot",
        case_id="synthetic-step3-case",
        cutoff="2026-09-03",
        workflow_version="research-v1",
        schema_version="1",
        transformation_version="1",
        configuration_hash=None,
        assumptions_hash=None,
        status="draft",
        members={claim_v1.canonical_ref: "sha256:" + "0" * 64},
    )
    with pytest.raises(SnapshotError, match="cannot be recovered"):
        invalid_snapshot.resolve(registry, claim_v1.canonical_ref)
