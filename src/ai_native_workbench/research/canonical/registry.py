"""In-memory lifecycle management for canonical object states."""

from dataclasses import fields

from .errors import (
    CanonicalError,
    CanonicalValidationError,
    IntegrityError,
    RegistryError,
    ResolutionError,
    SnapshotError,
)
from .identity import CanonicalObjectType, CanonicalRef, canonical_fingerprint
from .model import CanonicalObject, Claim, Entity, Evidence, Relationship, Source, Unknown
from .snapshot import ResearchSnapshot


_CANONICAL_OBJECT_CLASSES = (Entity, Claim, Evidence, Source, Unknown, Relationship)


class CanonicalRegistry:
    """Store current canonical states while retaining immutable historical states."""

    def __init__(self) -> None:
        self._current: dict[CanonicalRef, str] = {}
        self._states: dict[CanonicalRef, dict[str, CanonicalObject]] = {}
        self._logical_id_types: dict[str, CanonicalObjectType] = {}

    def register(self, obj: CanonicalObject) -> CanonicalRef:
        """Store *obj* and make its fingerprint the current state for its ref."""
        ref = self._canonical_ref_for(obj)
        self._ensure_logical_id_type(ref)
        fingerprint = canonical_fingerprint(obj)
        states = self._states.setdefault(ref, {})
        states.setdefault(fingerprint, obj)
        self._current[ref] = fingerprint
        return ref

    def get(self, ref: CanonicalRef) -> CanonicalObject:
        """Return the current state for *ref*."""
        self._require_ref(ref)
        try:
            fingerprint = self._current[ref]
        except KeyError as error:
            raise ResolutionError(f"Canonical ref is not registered: {ref}.") from error
        return self.get_state(ref, fingerprint)

    def get_state(self, ref: CanonicalRef, fingerprint: str) -> CanonicalObject:
        """Return the exact historical state identified by *ref* and *fingerprint*."""
        self._require_ref(ref)
        if not isinstance(fingerprint, str) or not fingerprint:
            raise CanonicalValidationError("fingerprint must be a non-empty string.")
        try:
            return self._states[ref][fingerprint]
        except KeyError as error:
            raise ResolutionError(
                f"Canonical state cannot be resolved: {ref} at {fingerprint}."
            ) from error

    def replace(self, ref: CanonicalRef, obj: CanonicalObject) -> str:
        """Store a new immutable state for an existing logical object."""
        self._require_ref(ref)
        if ref not in self._current:
            raise RegistryError(f"Cannot replace unregistered canonical ref: {ref}.")
        object_ref = self._canonical_ref_for(obj)
        if object_ref != ref:
            raise RegistryError(
                "Replacement object canonical_ref must match the supplied ref."
            )
        self._ensure_logical_id_type(ref)
        fingerprint = canonical_fingerprint(obj)
        self._states[ref].setdefault(fingerprint, obj)
        self._current[ref] = fingerprint
        return fingerprint

    def resolve(self, ref: CanonicalRef) -> CanonicalObject:
        """Resolve *ref* to its current canonical object without mutation."""
        return self.get(ref)

    def validate(self) -> None:
        """Check structural and cross-object provenance integrity."""
        self._validate_registry_structure()
        from .provenance import validate_registry_integrity

        validate_registry_integrity(self)

    def snapshot(
        self,
        snapshot_id: str,
        refs: tuple[CanonicalRef, ...],
        *,
        case_id: str = "synthetic-case",
        cutoff: str = "",
        workflow_version: str = "",
        schema_version: str = "1",
        transformation_version: str = "1",
        configuration_hash: str | None = None,
        assumptions_hash: str | None = None,
        status: str = "draft",
    ) -> ResearchSnapshot:
        """Freeze current fingerprints for *refs* into an immutable snapshot."""
        if not isinstance(refs, tuple):
            raise SnapshotError("refs must be a tuple of CanonicalRef values.")

        members: dict[CanonicalRef, str] = {}
        for ref in refs:
            if not isinstance(ref, CanonicalRef):
                raise SnapshotError("Snapshot refs must be CanonicalRef values.")
            if ref in members:
                raise SnapshotError(f"Snapshot contains duplicate member ref: {ref}.")
            try:
                current_state = self.get(ref)
                fingerprint = self._current[ref]
                self._validate_intrinsic_state(ref, current_state)
                self.get_state(ref, fingerprint)
            except (CanonicalError, KeyError) as error:
                raise SnapshotError(f"Snapshot ref cannot be resolved: {ref}.") from error
            members[ref] = fingerprint

        snapshot = ResearchSnapshot(
            snapshot_id,
            case_id,
            cutoff,
            workflow_version,
            schema_version,
            transformation_version,
            configuration_hash,
            assumptions_hash,
            status,
            members,
        )
        snapshot.validate(self)
        return snapshot

    def _validate_registry_structure(self) -> None:
        """Check consistency of current and historical state mappings."""
        for ref, fingerprint in self._current.items():
            self._require_ref(ref)
            if not isinstance(fingerprint, str) or not fingerprint:
                raise IntegrityError(f"Current fingerprint is invalid for {ref}.")
            states = self._states.get(ref)
            if states is None or fingerprint not in states:
                raise IntegrityError(f"Current state is missing from history for {ref}.")

        for ref, states in self._states.items():
            self._require_ref(ref)
            if not states:
                raise IntegrityError(f"Historical states must not be empty for {ref}.")
            if ref not in self._current:
                raise IntegrityError(f"Historical states have no current state for {ref}.")
            known_type = self._logical_id_types.get(ref.logical_id)
            if known_type is not ref.object_type:
                raise IntegrityError(f"Logical ID type mapping is invalid for {ref}.")
            for fingerprint, obj in states.items():
                self._validate_intrinsic_state(ref, obj)
                if canonical_fingerprint(obj) != fingerprint:
                    raise IntegrityError(f"Historical fingerprint does not match object state for {ref}.")
                if self._canonical_ref_for(obj) != ref:
                    raise IntegrityError(f"Historical object identity does not match its state ref: {ref}.")

        for logical_id, object_type in self._logical_id_types.items():
            if not isinstance(logical_id, str) or not logical_id:
                raise IntegrityError("Logical ID type mapping contains an invalid logical ID.")
            if not isinstance(object_type, CanonicalObjectType):
                raise IntegrityError("Logical ID type mapping contains an invalid object type.")
            ref = CanonicalRef(object_type, logical_id)
            if ref not in self._states:
                raise IntegrityError(f"Logical ID type mapping has no states for {ref}.")

    @staticmethod
    def _require_ref(ref: object) -> None:
        if not isinstance(ref, CanonicalRef):
            raise CanonicalValidationError("ref must be a CanonicalRef.")

    @staticmethod
    def _canonical_ref_for(obj: CanonicalObject) -> CanonicalRef:
        ref = getattr(obj, "canonical_ref", None)
        if not isinstance(ref, CanonicalRef):
            raise CanonicalValidationError("obj must be a canonical object.")
        return ref

    @staticmethod
    def _validate_intrinsic_state(ref: CanonicalRef, obj: object) -> None:
        """Revalidate every stored state without mutating registry history."""
        if type(obj) not in _CANONICAL_OBJECT_CLASSES:
            raise IntegrityError(f"Historical state for {ref} is not a canonical object.")
        try:
            type(obj)(
                **{field.name: getattr(obj, field.name) for field in fields(obj)}
            )
        except (AttributeError, CanonicalValidationError, TypeError) as error:
            raise IntegrityError(
                f"Historical object fails intrinsic validation for {ref}."
            ) from error

    def _ensure_logical_id_type(self, ref: CanonicalRef) -> None:
        known_type = self._logical_id_types.get(ref.logical_id)
        if known_type is not None and known_type is not ref.object_type:
            raise RegistryError("logical ID is already bound to a different object type")
        self._logical_id_types[ref.logical_id] = ref.object_type
