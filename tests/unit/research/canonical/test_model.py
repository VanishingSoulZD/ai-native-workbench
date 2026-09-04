from dataclasses import FrozenInstanceError

import pytest

from ai_native_workbench.research.canonical import (
    CanonicalObjectType,
    CanonicalRef,
    CanonicalValidationError,
    Claim,
    Entity,
    Evidence,
    Relationship,
    Source,
    Unknown,
)


def entity() -> Entity:
    return Entity("product-x", "product", "Product X", "active", {"tier": "pro"})


def evidence_ref() -> CanonicalRef:
    return CanonicalRef(CanonicalObjectType.EVIDENCE, "evidence-1")


def test_entity_requires_id_and_name():
    with pytest.raises(CanonicalValidationError):
        Entity(id="", entity_type="product", name="", status="active", attributes={})


def test_valid_entity_is_accepted_and_copies_attributes():
    attributes = {"tier": "pro"}
    result = Entity("product-x", "product", "Product X", "active", attributes)
    attributes["tier"] = "basic"

    assert result.id == "product-x"
    assert result.attributes["tier"] == "pro"
    assert result.canonical_ref == CanonicalRef(CanonicalObjectType.ENTITY, "product-x")


def test_factual_claim_requires_evidence():
    with pytest.raises(CanonicalValidationError):
        Claim("claim-1", "Product X supports feature Y.", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "factual", "supported", 0.9, ())


def test_derived_claim_can_be_created():
    claim = Claim("claim-2", "Product X is likely easier to deploy.", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "derived", "proposed", 0.7, (evidence_ref(),))

    assert claim.claim_type == "derived"


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_claim_confidence_must_be_between_zero_and_one(confidence):
    with pytest.raises(CanonicalValidationError):
        Claim("claim-1", "Statement", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "factual", "supported", confidence, (evidence_ref(),))


def test_claim_type_is_restricted_to_factual_or_derived():
    with pytest.raises(CanonicalValidationError):
        Claim("claim-1", "Statement", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "hypothesis", "proposed", 0.5, ())


def test_claim_subject_and_evidence_must_be_canonical_refs_in_a_tuple():
    with pytest.raises(CanonicalValidationError):
        Claim("claim-1", "Statement", "entity:product-x", "factual", "supported", 0.9, (evidence_ref(),))
    with pytest.raises(CanonicalValidationError):
        Claim("claim-1", "Statement", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "factual", "supported", 0.9, [evidence_ref()])


def test_unknown_is_first_class_and_meaningful():
    unknown = Unknown("unknown-1", "Does Product X support feature Y?", "This affects product selection.", "official vendor documentation", "unresolved")

    assert unknown.question
    assert unknown.status == "unresolved"


@pytest.mark.parametrize(
    "question, why_it_matters, scope, status",
    [
        ("", "This affects product selection.", "Product X public capabilities.", "open"),
        ("Does Product X support feature Y?", "", "Product X public capabilities.", "open"),
        ("Does Product X support feature Y?", "This affects product selection.", "", "open"),
        ("Does Product X support feature Y?", "This affects product selection.", "Product X public capabilities.", ""),
    ],
)
def test_unknown_requires_meaningful_fields(question, why_it_matters, scope, status):
    with pytest.raises(CanonicalValidationError):
        Unknown("unknown-1", question, why_it_matters, scope, status)


def test_valid_evidence_uses_source_reference():
    evidence = Evidence("evidence-1", CanonicalRef(CanonicalObjectType.SOURCE, "source-1"), "Official documentation states feature Y is supported.", "2026-09", "official_documentation", "A", (), (), "")

    assert evidence.source_id == CanonicalRef(CanonicalObjectType.SOURCE, "source-1")


def test_evidence_and_source_validate_intrinsic_fields_only():
    source = Source("source-1", "Product documentation", "Vendor", "https://example.test/docs", "documentation", "", "", "A")
    assert source.object_type is CanonicalObjectType.SOURCE
    with pytest.raises(CanonicalValidationError):
        Evidence("evidence-1", "source:source-1", "Observation", "", "documentation", "A", (), (), "")


def test_valid_relationship_is_constructible():
    relationship = Relationship("relationship-1", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "supports", CanonicalRef(CanonicalObjectType.ENTITY, "feature-y"), (), "asserted")

    assert relationship.predicate == "supports"


def test_relationship_requires_canonical_refs_and_tuple_evidence():
    with pytest.raises(CanonicalValidationError):
        Relationship("relationship-1", "entity:product-x", "supports", CanonicalRef(CanonicalObjectType.ENTITY, "feature-y"), (), "asserted")
    with pytest.raises(CanonicalValidationError):
        Relationship("relationship-1", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "supports", CanonicalRef(CanonicalObjectType.ENTITY, "feature-y"), [], "asserted")


def test_models_do_not_require_registry_existence():
    claim = Claim("claim-1", "Statement", CanonicalRef(CanonicalObjectType.ENTITY, "entity-that-is-not-registered"), "derived", "proposed", 0.5, ())

    assert claim.subject_ref.logical_id == "entity-that-is-not-registered"


@pytest.mark.parametrize(
    "model, attribute, replacement",
    [
        (entity(), "name", "Changed"),
        (Claim("claim-1", "Statement", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "derived", "proposed", 0.5, ()), "status", "changed"),
        (Evidence("evidence-1", CanonicalRef(CanonicalObjectType.SOURCE, "source-1"), "Observation", "", "documentation", "A", (), (), ""), "note", "changed"),
        (Source("source-1", "Title", "Publisher", "https://example.test", "documentation", "", "", "A"), "publisher", "Changed"),
        (Unknown("unknown-1", "Question?", "It matters.", "scope", "unresolved"), "status", "resolved"),
        (Relationship("relationship-1", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "supports", CanonicalRef(CanonicalObjectType.ENTITY, "feature-y"), (), "asserted"), "predicate", "changed"),
    ],
)
def test_models_are_frozen(model, attribute, replacement):
    with pytest.raises(FrozenInstanceError):
        setattr(model, attribute, replacement)


def test_reference_collections_require_their_declared_reference_types():
    with pytest.raises(CanonicalValidationError):
        Evidence("evidence-1", CanonicalRef(CanonicalObjectType.ENTITY, "not-a-source"), "Observation", "", "documentation", "A", (), (), "")
    with pytest.raises(CanonicalValidationError):
        Evidence("evidence-1", CanonicalRef(CanonicalObjectType.SOURCE, "source-1"), "Observation", "", "documentation", "A", (CanonicalRef(CanonicalObjectType.ENTITY, "not-a-claim"),), (), "")
    with pytest.raises(CanonicalValidationError):
        Relationship("relationship-1", CanonicalRef(CanonicalObjectType.ENTITY, "product-x"), "supports", CanonicalRef(CanonicalObjectType.ENTITY, "feature-y"), (CanonicalRef(CanonicalObjectType.CLAIM, "not-evidence"),), "asserted")


def test_entity_attributes_are_immune_to_nested_caller_mutation():
    attributes = {
        "metadata": {"tier": "pro"},
        "regions": ["global"],
    }
    result = Entity("product-x", "product", "Product X", "active", attributes)

    attributes["metadata"]["tier"] = "basic"
    attributes["regions"].append("regional")

    assert result.attributes["metadata"]["tier"] == "pro"
    assert result.attributes["regions"] == ("global",)
    with pytest.raises(TypeError):
        result.attributes["metadata"]["tier"] = "enterprise"
    with pytest.raises(AttributeError):
        result.attributes["regions"].append("enterprise")
