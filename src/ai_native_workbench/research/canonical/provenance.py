"""Mechanical cross-object reference and provenance integrity validation."""

from .errors import IntegrityError, ResolutionError
from .identity import CanonicalObjectType, CanonicalRef
from .model import (
    CanonicalObject,
    Claim,
    Entity,
    Evidence,
    Relationship,
    Source,
)


def validate_object_references(obj: CanonicalObject, registry: object) -> None:
    """Validate the typed references declared by one canonical object.

    The registry is read only: this function reports invalid provenance and never
    repairs or synchronizes reverse links.
    """
    if isinstance(obj, Claim):
        _resolve_expected(obj, "subject_ref", obj.subject_ref, Entity, registry)
        for reference in obj.evidence_ids:
            _resolve_expected(obj, "evidence_ids", reference, Evidence, registry)
    elif isinstance(obj, Evidence):
        _resolve_expected(obj, "source_id", obj.source_id, Source, registry)
        for reference in obj.supports_claim_ids:
            _resolve_expected(obj, "supports_claim_ids", reference, Claim, registry)
        for reference in obj.contradicts_claim_ids:
            _resolve_expected(obj, "contradicts_claim_ids", reference, Claim, registry)
    elif isinstance(obj, Relationship):
        _resolve_supported_endpoint(obj, "subject_ref", obj.subject_ref, registry)
        _resolve_supported_endpoint(obj, "object_ref", obj.object_ref, registry)
        for reference in obj.evidence_ids:
            _resolve_expected(obj, "evidence_ids", reference, Evidence, registry)


def validate_registry_integrity(registry: object) -> None:
    """Validate reference integrity for every current and historical object state."""
    states = getattr(registry, "_states", None)
    if not isinstance(states, dict):
        raise IntegrityError("Registry states are unavailable for integrity validation.")

    objects = tuple(
        state for historical_states in states.values() for state in historical_states.values()
    )
    for obj in objects:
        validate_object_references(obj, registry)

    _validate_reverse_provenance_links(registry)


def _validate_reverse_provenance_links(registry: object) -> None:
    """Validate reverse links against the authoritative current provenance graph."""
    current = getattr(registry, "_current", None)
    if not isinstance(current, dict):
        raise IntegrityError("Registry current states are unavailable for integrity validation.")
    current_objects = tuple(registry.resolve(reference) for reference in current)
    evidence_states = {
        obj.canonical_ref: obj for obj in current_objects if isinstance(obj, Evidence)
    }
    claim_states = {
        obj.canonical_ref: obj for obj in current_objects if isinstance(obj, Claim)
    }

    for evidence in evidence_states.values():
        for field_name, claim_refs in (
            ("supports_claim_ids", evidence.supports_claim_ids),
            ("contradicts_claim_ids", evidence.contradicts_claim_ids),
        ):
            for claim_ref in claim_refs:
                claim = claim_states.get(claim_ref)
                if claim is not None and evidence.canonical_ref not in claim.evidence_ids:
                    raise IntegrityError(
                        f"{evidence.canonical_ref}.{field_name} references {claim_ref} "
                        "without matching forward evidence_ids."
                    )


def _resolve_expected(
    obj: CanonicalObject,
    field_name: str,
    reference: object,
    expected_class: type[CanonicalObject],
    registry: object,
) -> None:
    expected_type = _object_type_for(expected_class)
    if not isinstance(reference, CanonicalRef):
        raise IntegrityError(f"{obj.canonical_ref}.{field_name} must be a CanonicalRef.")
    if reference.object_type is not expected_type:
        raise IntegrityError(
            f"{obj.canonical_ref}.{field_name} must reference {expected_type.value}, "
            f"not {reference}."
        )
    resolved = _resolve(obj, field_name, reference, registry)
    if not isinstance(resolved, expected_class):
        raise IntegrityError(
            f"{obj.canonical_ref}.{field_name} resolved {reference} to "
            f"{type(resolved).__name__}, not {expected_type.value}."
        )


def _resolve_supported_endpoint(
    obj: Relationship,
    field_name: str,
    reference: object,
    registry: object,
) -> None:
    if not isinstance(reference, CanonicalRef):
        raise IntegrityError(f"{obj.canonical_ref}.{field_name} must be a CanonicalRef.")
    if not isinstance(reference.object_type, CanonicalObjectType):
        raise IntegrityError(
            f"{obj.canonical_ref}.{field_name} must reference a supported canonical object."
        )
    _resolve(obj, field_name, reference, registry)


def _resolve(
    obj: CanonicalObject, field_name: str, reference: CanonicalRef, registry: object
) -> CanonicalObject:
    try:
        return registry.resolve(reference)
    except (ResolutionError, KeyError) as error:
        raise IntegrityError(
            f"{obj.canonical_ref}.{field_name} references missing {reference}."
        ) from error


def _object_type_for(model_class: type[CanonicalObject]) -> CanonicalObjectType:
    return {
        Entity: CanonicalObjectType.ENTITY,
        Claim: CanonicalObjectType.CLAIM,
        Evidence: CanonicalObjectType.EVIDENCE,
        Source: CanonicalObjectType.SOURCE,
    }[model_class]
