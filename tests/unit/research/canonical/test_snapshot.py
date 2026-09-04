from dataclasses import FrozenInstanceError

import pytest

from ai_native_workbench.research.canonical import (
    CanonicalObjectType,
    CanonicalRef,
    CanonicalRegistry,
    CanonicalValidationError,
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


def entity(status: str = "active") -> Entity:
    return Entity("product-x", "product", "Product X", status, {})


def test_snapshot_captures_exact_current_fingerprints_and_metadata():
    registry = CanonicalRegistry()
    value = entity()
    registry.register(value)

    snapshot = registry.snapshot(
        "snapshot-1",
        (value.canonical_ref,),
        case_id="case-1",
        cutoff="2026-09-03",
        workflow_version="research-v1",
        schema_version="1",
        transformation_version="1",
        configuration_hash="config-v1",
        assumptions_hash="assumptions-v1",
        status="draft",
    )

    assert snapshot.snapshot_id == "snapshot-1"
    assert snapshot.case_id == "case-1"
    assert snapshot.cutoff == "2026-09-03"
    assert snapshot.workflow_version == "research-v1"
    assert snapshot.schema_version == "1"
    assert snapshot.transformation_version == "1"
    assert snapshot.configuration_hash == "config-v1"
    assert snapshot.assumptions_hash == "assumptions-v1"
    assert snapshot.status == "draft"
    assert snapshot.members[value.canonical_ref] == canonical_fingerprint(value)
    assert snapshot.fingerprint_for(value.canonical_ref) == canonical_fingerprint(value)
    assert snapshot.refs() == (value.canonical_ref,)


def test_snapshot_members_and_fields_cannot_be_mutated():
    registry = CanonicalRegistry()
    value = entity()
    registry.register(value)
    snapshot = registry.snapshot("snapshot-1", (value.canonical_ref,))

    with pytest.raises(TypeError):
        snapshot.members[value.canonical_ref] = "sha256:" + "0" * 64
    with pytest.raises(FrozenInstanceError):
        snapshot.snapshot_id = "snapshot-2"


def test_snapshot_missing_ref_is_rejected():
    registry = CanonicalRegistry()
    missing = CanonicalRef(CanonicalObjectType.ENTITY, "missing")

    with pytest.raises(SnapshotError, match="cannot be resolved"):
        registry.snapshot("snapshot-1", (missing,))


def test_snapshot_invalid_membership_is_rejected_and_missing_state_fails_validation():
    ref = CanonicalRef(CanonicalObjectType.ENTITY, "product-x")
    fake_fingerprint = "sha256:" + "0" * 64
    registry = CanonicalRegistry()
    registry.register(entity())

    with pytest.raises(SnapshotError, match="fingerprint"):
        ResearchSnapshot("snapshot-1", "case-1", "", "", "1", "1", None, None, "draft", {ref: "fake"})

    snapshot = ResearchSnapshot(
        "snapshot-1", "case-1", "", "", "1", "1", None, None, "draft", {ref: fake_fingerprint}
    )
    with pytest.raises(SnapshotError, match="cannot be recovered"):
        snapshot.validate(registry)


def test_snapshot_recovers_old_state_after_registry_replace():
    registry = CanonicalRegistry()
    original = entity("active")
    changed = entity("deprecated")
    registry.register(original)
    snapshot = registry.snapshot("snapshot-1", (original.canonical_ref,))
    old_fingerprint = snapshot.fingerprint_for(original.canonical_ref)

    registry.replace(original.canonical_ref, changed)

    assert old_fingerprint != canonical_fingerprint(changed)
    assert registry.get(original.canonical_ref) == changed
    assert snapshot.resolve(registry, original.canonical_ref) == original
    assert registry.get_state(original.canonical_ref, old_fingerprint) == original


def test_current_registry_changes_do_not_change_snapshot_membership():
    registry = CanonicalRegistry()
    original = entity("active")
    registry.register(original)
    snapshot = registry.snapshot("snapshot-1", (original.canonical_ref,))

    registry.replace(original.canonical_ref, entity("deprecated"))

    assert snapshot.members == {original.canonical_ref: canonical_fingerprint(original)}


def test_empty_snapshot_is_valid_and_preserves_empty_input_semantics():
    snapshot = CanonicalRegistry().snapshot("empty", ())

    assert snapshot.members == {}
    assert snapshot.refs() == ()


def test_snapshot_rejects_duplicate_refs_without_implicit_deduplication():
    registry = CanonicalRegistry()
    value = entity()
    registry.register(value)

    with pytest.raises(SnapshotError, match="duplicate"):
        registry.snapshot("snapshot-1", (value.canonical_ref, value.canonical_ref))


def test_snapshot_accepts_all_canonical_types_including_unknown():
    registry = CanonicalRegistry()
    source = Source("source-1", "Docs", "Vendor", "https://example.com", "docs", "", "", "A")
    subject = entity()
    claim_ref = CanonicalRef(CanonicalObjectType.CLAIM, "claim-1")
    evidence = Evidence("evidence-1", source.canonical_ref, "Observation", "", "documentation", "A", (claim_ref,), (), "")
    claim = Claim("claim-1", "Product X supports indexing.", subject.canonical_ref, "factual", "active", 0.9, (evidence.canonical_ref,))
    unknown = Unknown("unknown-1", "Does X support Y?", "It affects selection.", "Product X.", "open")
    relationship = Relationship("relationship-1", subject.canonical_ref, "has_capability", claim.canonical_ref, (evidence.canonical_ref,), "active")
    values = (source, subject, claim, evidence, unknown, relationship)
    for value in values:
        registry.register(value)

    snapshot = registry.snapshot("snapshot-1", tuple(value.canonical_ref for value in values))

    assert snapshot.resolve(registry, unknown.canonical_ref) == unknown
    assert snapshot.refs() == tuple(value.canonical_ref for value in values)
    assert set(snapshot.members) == {value.canonical_ref for value in values}


@pytest.mark.parametrize(
    "field,value",
    [
        ("snapshot_id", ""),
        ("case_id", ""),
        ("cutoff", None),
        ("workflow_version", None),
        ("schema_version", ""),
        ("transformation_version", ""),
        ("status", ""),
        ("configuration_hash", 1),
        ("assumptions_hash", 1),
    ],
)
def test_snapshot_metadata_is_validated(field, value):
    kwargs = dict(
        snapshot_id="snapshot-1", case_id="case-1", cutoff="", workflow_version="",
        schema_version="1", transformation_version="1", configuration_hash=None,
        assumptions_hash=None, status="draft", members={},
    )
    kwargs[field] = value

    with pytest.raises(SnapshotError):
        ResearchSnapshot(**kwargs)


def test_snapshot_rejects_non_canonical_ref_member_keys():
    with pytest.raises(SnapshotError, match="CanonicalRef"):
        ResearchSnapshot("snapshot-1", "case-1", "", "", "1", "1", None, None, "draft", {"entity:x": "sha256:" + "0" * 64})
