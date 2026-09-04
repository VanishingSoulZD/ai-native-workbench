import pytest

from ai_native_workbench.research.canonical import (
    CanonicalObjectType,
    CanonicalRef,
    CanonicalRegistry,
    Claim,
    Entity,
    Evidence,
    IntegrityError,
    Relationship,
    Source,
    validate_object_references,
)


def build_valid_registry() -> tuple[CanonicalRegistry, Source, Entity, Claim, Evidence]:
    registry = CanonicalRegistry()
    source = Source("source-1", "Official Product Documentation", "Vendor", "https://example.com/docs", "official-docs", "2026-08-01", "2026-09-03", "A")
    entity = Entity("product-x", "product", "Product X", "active", {})
    evidence = Evidence("evidence-1", source.canonical_ref, "The documentation states that indexing is supported.", "2026-08-01", "documentation", "A", (CanonicalRef(CanonicalObjectType.CLAIM, "claim-1"),), (), "Direct statement in official documentation.")
    claim = Claim("claim-1", "Product X supports indexing.", entity.canonical_ref, "factual", "active", 0.95, (evidence.canonical_ref,))
    for obj in (source, entity, claim, evidence):
        registry.register(obj)
    return registry, source, entity, claim, evidence


def test_valid_claim_evidence_source_chain_passes():
    registry, _, _, claim, _ = build_valid_registry()

    validate_object_references(claim, registry)
    registry.validate()


def test_claim_missing_evidence_fails():
    registry, _, _, claim, _ = build_valid_registry()
    broken = Claim(claim.id, claim.statement, claim.subject_ref, claim.claim_type, claim.status, claim.confidence, (CanonicalRef(CanonicalObjectType.EVIDENCE, "missing"),))

    with pytest.raises(IntegrityError, match=r"claim:claim-1\.evidence_ids references missing evidence:missing"):
        validate_object_references(broken, registry)


@pytest.mark.parametrize("object_type", [CanonicalObjectType.SOURCE, CanonicalObjectType.ENTITY])
def test_claim_evidence_wrong_type_fails(object_type):
    registry, _, _, claim, _ = build_valid_registry()
    object.__setattr__(claim, "evidence_ids", (CanonicalRef(object_type, "wrong-target"),))

    with pytest.raises(IntegrityError, match=r"claim:claim-1\.evidence_ids must reference evidence"):
        validate_object_references(claim, registry)


def test_evidence_missing_source_fails():
    registry, _, _, _, evidence = build_valid_registry()
    broken = Evidence(evidence.id, CanonicalRef(CanonicalObjectType.SOURCE, "missing"), evidence.observation, evidence.date_or_period, evidence.evidence_type, evidence.evidence_grade, evidence.supports_claim_ids, evidence.contradicts_claim_ids, evidence.note)

    with pytest.raises(IntegrityError, match=r"evidence:evidence-1\.source_id references missing source:missing"):
        validate_object_references(broken, registry)


def test_evidence_source_wrong_type_fails():
    registry, _, _, _, evidence = build_valid_registry()
    object.__setattr__(evidence, "source_id", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"))

    with pytest.raises(IntegrityError, match=r"evidence:evidence-1\.source_id must reference source"):
        validate_object_references(evidence, registry)


@pytest.mark.parametrize(
    ("field", "reference", "message"),
    [
        ("supports_claim_ids", CanonicalRef(CanonicalObjectType.CLAIM, "missing"), r"supports_claim_ids references missing claim:missing"),
        ("supports_claim_ids", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), r"supports_claim_ids must reference claim"),
        ("contradicts_claim_ids", CanonicalRef(CanonicalObjectType.CLAIM, "missing"), r"contradicts_claim_ids references missing claim:missing"),
        ("contradicts_claim_ids", CanonicalRef(CanonicalObjectType.SOURCE, "source-1"), r"contradicts_claim_ids must reference claim"),
    ],
)
def test_evidence_reverse_claim_links_must_resolve_to_claim(field, reference, message):
    registry, _, _, _, evidence = build_valid_registry()
    object.__setattr__(evidence, field, (reference,))

    with pytest.raises(IntegrityError, match=message):
        validate_object_references(evidence, registry)


@pytest.mark.parametrize("field", ["subject_ref", "object_ref"])
def test_relationship_endpoints_must_resolve(field):
    registry, _, entity, _, _ = build_valid_registry()
    relationship = Relationship("relationship-1", entity.canonical_ref, "relates_to", entity.canonical_ref, (), "asserted")
    object.__setattr__(relationship, field, CanonicalRef(CanonicalObjectType.ENTITY, "missing"))

    with pytest.raises(IntegrityError, match=rf"relationship:relationship-1\.{field} references missing entity:missing"):
        validate_object_references(relationship, registry)


def test_relationship_evidence_must_resolve_to_evidence():
    registry, _, entity, _, _ = build_valid_registry()
    relationship = Relationship("relationship-1", entity.canonical_ref, "relates_to", entity.canonical_ref, (CanonicalRef(CanonicalObjectType.EVIDENCE, "missing"),), "asserted")

    with pytest.raises(IntegrityError, match=r"relationship:relationship-1\.evidence_ids references missing evidence:missing"):
        validate_object_references(relationship, registry)


def test_reverse_support_link_must_match_forward_claim_link():
    registry = CanonicalRegistry()
    source = Source("source-1", "Title", "Vendor", "https://example.com", "docs", "", "", "A")
    entity = Entity("product-x", "product", "Product X", "active", {})
    evidence = Evidence("evidence-1", source.canonical_ref, "Observation", "", "documentation", "A", (), (), "")
    claim = Claim("claim-1", "Product X supports indexing.", entity.canonical_ref, "factual", "active", 0.95, (evidence.canonical_ref,))
    for obj in (source, entity, claim, evidence):
        registry.register(obj)

    with pytest.raises(IntegrityError, match=r"claim:claim-1\.evidence_ids is missing reverse link from evidence:evidence-1"):
        registry.validate()


@pytest.mark.parametrize("field", ["supports_claim_ids", "contradicts_claim_ids"])
def test_reverse_claim_link_without_forward_claim_link_fails(field):
    registry = CanonicalRegistry()
    source = Source("source-1", "Title", "Vendor", "https://example.com", "docs", "", "", "A")
    entity = Entity("product-x", "product", "Product X", "active", {})
    claim_ref = CanonicalRef(CanonicalObjectType.CLAIM, "claim-1")
    evidence_1 = Evidence("evidence-1", source.canonical_ref, "Observation 1", "", "documentation", "A", (claim_ref,) if field == "supports_claim_ids" else (), (claim_ref,) if field == "contradicts_claim_ids" else (), "")
    evidence_2 = Evidence("evidence-2", source.canonical_ref, "Observation 2", "", "documentation", "A", (claim_ref,), (), "")
    claim = Claim("claim-1", "Product X supports indexing.", entity.canonical_ref, "factual", "active", 0.95, (evidence_2.canonical_ref,))
    for obj in (source, entity, claim, evidence_1, evidence_2):
        registry.register(obj)

    with pytest.raises(IntegrityError, match=rf"evidence:evidence-1\.{field} references claim:claim-1 without matching forward evidence_ids"):
        registry.validate()


def test_historical_state_references_are_validated():
    registry, _, _, claim, _ = build_valid_registry()
    broken = Claim(claim.id, claim.statement, claim.subject_ref, claim.claim_type, claim.status, claim.confidence, (CanonicalRef(CanonicalObjectType.EVIDENCE, "missing"),))
    registry.replace(claim.canonical_ref, broken)
    registry.replace(claim.canonical_ref, claim)

    with pytest.raises(IntegrityError, match=r"claim:claim-1\.evidence_ids references missing evidence:missing"):
        registry.validate()

@pytest.mark.parametrize("object_type", [CanonicalObjectType.ENTITY, CanonicalObjectType.SOURCE, CanonicalObjectType.CLAIM])
def test_relationship_evidence_wrong_type_fails(object_type):
    registry, _, entity, _, _ = build_valid_registry()
    relationship = Relationship("relationship-1", entity.canonical_ref, "relates_to", entity.canonical_ref, (), "asserted")
    object.__setattr__(relationship, "evidence_ids", (CanonicalRef(object_type, "wrong-target"),))

    with pytest.raises(IntegrityError, match=r"relationship:relationship-1\.evidence_ids must reference evidence"):
        validate_object_references(relationship, registry)


def test_historical_evidence_source_reference_is_validated():
    registry, _, _, _, evidence = build_valid_registry()
    broken = Evidence(evidence.id, CanonicalRef(CanonicalObjectType.SOURCE, "missing"), evidence.observation, evidence.date_or_period, evidence.evidence_type, evidence.evidence_grade, evidence.supports_claim_ids, evidence.contradicts_claim_ids, evidence.note)
    registry.replace(evidence.canonical_ref, broken)
    registry.replace(evidence.canonical_ref, evidence)

    with pytest.raises(IntegrityError, match=r"evidence:evidence-1\.source_id references missing source:missing"):
        registry.validate()
