import pytest

from ai_native_workbench.research.canonical import (
    CanonicalObjectType,
    CanonicalRef,
    CanonicalRegistry,
    Claim,
    Entity,
    IntegrityError,
    RegistryError,
    ResolutionError,
    canonical_fingerprint,
)


def entity(identifier: str = "product-x", status: str = "active") -> Entity:
    return Entity(identifier, "product", "Product X", status, {"tier": "pro"})


def test_get_missing_ref_raises_resolution_error():
    registry = CanonicalRegistry()
    ref = CanonicalRef(CanonicalObjectType.ENTITY, "missing")

    with pytest.raises(ResolutionError):
        registry.get(ref)


def test_register_returns_canonical_ref():
    registry = CanonicalRegistry()
    value = entity()

    assert registry.register(value) == value.canonical_ref


def test_register_then_get_returns_current_state():
    registry = CanonicalRegistry()
    value = entity()

    registry.register(value)

    assert registry.get(value.canonical_ref) == value


def test_repeated_identical_registration_is_idempotent():
    registry = CanonicalRegistry()
    value = entity()

    ref1 = registry.register(value)
    ref2 = registry.register(value)

    assert ref1 == ref2
    assert len(registry._states[ref1]) == 1


def test_changed_state_creates_new_historical_state():
    registry = CanonicalRegistry()
    v1 = entity(status="active")
    v2 = entity(status="deprecated")
    fingerprint_v1 = canonical_fingerprint(v1)

    registry.register(v1)
    registry.register(v2)

    assert registry.get(v1.canonical_ref) == v2
    assert registry.get_state(v1.canonical_ref, fingerprint_v1) == v1


def test_historical_state_remains_recoverable_after_registration():
    registry = CanonicalRegistry()
    v1 = entity(status="active")
    v2 = entity(status="deprecated")
    fingerprint_v1 = canonical_fingerprint(v1)
    fingerprint_v2 = canonical_fingerprint(v2)

    registry.register(v1)
    registry.register(v2)

    assert registry.get_state(v1.canonical_ref, fingerprint_v1) == v1
    assert registry.get_state(v1.canonical_ref, fingerprint_v2) == v2


def test_missing_historical_fingerprint_raises_resolution_error():
    registry = CanonicalRegistry()
    value = entity()
    registry.register(value)

    with pytest.raises(ResolutionError):
        registry.get_state(value.canonical_ref, "sha256:" + "0" * 64)


def test_replace_preserves_old_state():
    registry = CanonicalRegistry()
    v1 = entity(status="active")
    v2 = entity(status="deprecated")
    fingerprint_v1 = canonical_fingerprint(v1)
    fingerprint_v2 = canonical_fingerprint(v2)
    registry.register(v1)

    new_fingerprint = registry.replace(v1.canonical_ref, v2)

    assert registry.get(v1.canonical_ref) == v2
    assert registry.get_state(v1.canonical_ref, fingerprint_v1) == v1
    assert new_fingerprint == fingerprint_v2


def test_replace_rejects_wrong_ref():
    registry = CanonicalRegistry()
    registry.register(entity("a"))

    with pytest.raises(RegistryError):
        registry.replace(CanonicalRef(CanonicalObjectType.ENTITY, "a"), entity("b"))


def test_replace_rejects_wrong_object_type():
    registry = CanonicalRegistry()
    value = entity("foo")
    registry.register(value)
    claim = Claim(
        "foo",
        "Product X is available.",
        value.canonical_ref,
        "derived",
        "proposed",
        0.5,
        (),
    )

    with pytest.raises(RegistryError):
        registry.replace(value.canonical_ref, claim)


def test_same_logical_id_cannot_change_object_type():
    registry = CanonicalRegistry()
    value = entity("shared")
    registry.register(value)
    claim = Claim(
        "shared",
        "Product X is available.",
        value.canonical_ref,
        "derived",
        "proposed",
        0.5,
        (),
    )

    with pytest.raises(RegistryError):
        registry.register(claim)


def test_resolve_returns_current_object():
    registry = CanonicalRegistry()
    value = entity()
    ref = registry.register(value)

    assert registry.resolve(ref) == registry.get(ref)


def test_validate_passes_for_a_healthy_registry():
    registry = CanonicalRegistry()
    registry.register(entity(status="active"))
    registry.register(entity(status="deprecated"))

    registry.validate()


def test_validate_detects_corrupt_current_state_mapping():
    registry = CanonicalRegistry()
    value = entity()
    ref = registry.register(value)
    registry._current[ref] = "sha256:" + "0" * 64

    with pytest.raises(IntegrityError):
        registry.validate()


def test_different_logical_ids_with_identical_content_remain_distinct():
    registry = CanonicalRegistry()
    first = Entity("a", "product", "Same", "active", {})
    second = Entity("b", "product", "Same", "active", {})

    assert first.canonical_ref != second.canonical_ref
    registry.register(first)
    registry.register(second)

    assert registry.get(first.canonical_ref) == first
    assert registry.get(second.canonical_ref) == second


def test_validate_includes_provenance_integrity():
    registry = CanonicalRegistry()
    subject = entity()
    claim = Claim(
        "claim-1",
        "Product X supports indexing.",
        subject.canonical_ref,
        "factual",
        "active",
        0.9,
        (CanonicalRef(CanonicalObjectType.EVIDENCE, "missing"),),
    )
    registry.register(subject)
    registry.register(claim)

    with pytest.raises(IntegrityError, match=r"claim:claim-1\.evidence_ids references missing evidence:missing"):
        registry.validate()


def test_validate_preserves_structural_integrity_checks_before_provenance():
    registry = CanonicalRegistry()
    value = entity()
    ref = registry.register(value)
    registry._current[ref] = "sha256:" + "0" * 64

    with pytest.raises(IntegrityError, match="Current state is missing from history"):
        registry.validate()
