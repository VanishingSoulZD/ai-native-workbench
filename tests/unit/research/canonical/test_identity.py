from dataclasses import dataclass
from enum import Enum

import pytest

from ai_native_workbench.research.canonical.errors import CanonicalValidationError
from ai_native_workbench.research.canonical.identity import (
    CanonicalObjectType,
    CanonicalRef,
    canonical_fingerprint,
    canonical_serialize,
)


def test_canonical_ref_round_trips():
    ref = CanonicalRef(CanonicalObjectType.CLAIM, "product-x-support")
    assert str(ref) == "claim:product-x-support"
    assert CanonicalRef.parse(str(ref)) == ref


def test_canonical_ref_is_hashable():
    ref = CanonicalRef(CanonicalObjectType.ENTITY, "product-x")
    assert {ref: "state"}[ref] == "state"


def test_invalid_canonical_ref_is_rejected():
    with pytest.raises(CanonicalValidationError):
        CanonicalRef.parse("not-a-valid-ref")


def test_empty_logical_id_is_rejected():
    with pytest.raises(CanonicalValidationError):
        CanonicalRef(CanonicalObjectType.ENTITY, "")


def test_logical_id_with_colon_is_rejected():
    with pytest.raises(CanonicalValidationError):
        CanonicalRef(CanonicalObjectType.ENTITY, "product:x")


def test_invalid_object_type_is_rejected():
    with pytest.raises(CanonicalValidationError):
        CanonicalRef("invalid", "product-x")


def test_all_supported_object_types_round_trip():
    for object_type in CanonicalObjectType:
        ref = CanonicalRef(object_type, "sample-id")
        assert CanonicalRef.parse(str(ref)) == ref


def test_fingerprint_is_independent_of_mapping_order():
    first = {
        "name": "Product X",
        "attributes": {"tier": "pro", "region": "global"},
    }
    second = {
        "attributes": {"region": "global", "tier": "pro"},
        "name": "Product X",
    }

    assert canonical_fingerprint(first) == canonical_fingerprint(second)


def test_fingerprint_changes_when_state_changes():
    first = {"id": "product-x", "status": "active"}
    second = {"id": "product-x", "status": "deprecated"}

    assert canonical_fingerprint(first) != canonical_fingerprint(second)


def test_fingerprint_uses_sha256_format():
    fingerprint = canonical_fingerprint({"id": "product-x"})
    assert fingerprint.startswith("sha256:")
    digest = fingerprint.removeprefix("sha256:")
    assert len(digest) == 64
    assert digest == digest.lower()


def test_canonical_serialize_is_deterministic_for_nested_mappings():
    first = {"outer": {"b": 2, "a": 1}, "items": [1, 2, 3]}
    second = {"items": [1, 2, 3], "outer": {"a": 1, "b": 2}}

    assert canonical_serialize(first) == canonical_serialize(second)


def test_canonical_serialize_supports_dataclasses_and_enums():
    class Status(str, Enum):
        ACTIVE = "active"

    @dataclass(frozen=True)
    class State:
        identifier: str
        status: Status

    assert canonical_serialize(State("product-x", Status.ACTIVE)) == (
        '{"identifier":"product-x","status":"active"}'
    )
