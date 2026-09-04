"""Immutable point-in-time membership for canonical research states."""

from collections.abc import Mapping
from dataclasses import dataclass
import re
from types import MappingProxyType
from typing import TYPE_CHECKING

from .errors import CanonicalError, SnapshotError
from .identity import CanonicalRef
from .model import CanonicalObject

if TYPE_CHECKING:
    from .registry import CanonicalRegistry


_FINGERPRINT_PATTERN = re.compile(r"sha256:[0-9a-f]{64}\Z")


def _require_non_empty_string(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SnapshotError(f"{field_name} must be a non-empty string.")


def _require_string(value: object, field_name: str) -> None:
    if not isinstance(value, str):
        raise SnapshotError(f"{field_name} must be a string.")


def _require_optional_string(value: object, field_name: str) -> None:
    if value is not None and not isinstance(value, str):
        raise SnapshotError(f"{field_name} must be a string or None.")


def _require_fingerprint(value: object) -> None:
    if not isinstance(value, str) or not _FINGERPRINT_PATTERN.fullmatch(value):
        raise SnapshotError("Snapshot member fingerprint must be a sha256 fingerprint.")


@dataclass(frozen=True)
class ResearchSnapshot:
    """An immutable mapping of canonical refs to their exact state fingerprints."""

    snapshot_id: str
    case_id: str
    cutoff: str
    workflow_version: str
    schema_version: str
    transformation_version: str
    configuration_hash: str | None
    assumptions_hash: str | None
    status: str
    members: Mapping[CanonicalRef, str]

    def __post_init__(self) -> None:
        _require_non_empty_string(self.snapshot_id, "snapshot_id")
        _require_non_empty_string(self.case_id, "case_id")
        _require_string(self.cutoff, "cutoff")
        _require_string(self.workflow_version, "workflow_version")
        _require_non_empty_string(self.schema_version, "schema_version")
        _require_non_empty_string(self.transformation_version, "transformation_version")
        _require_optional_string(self.configuration_hash, "configuration_hash")
        _require_optional_string(self.assumptions_hash, "assumptions_hash")
        _require_non_empty_string(self.status, "status")
        if not isinstance(self.members, Mapping):
            raise SnapshotError("members must be a mapping of CanonicalRef to fingerprint.")

        members: dict[CanonicalRef, str] = {}
        for ref, fingerprint in self.members.items():
            if not isinstance(ref, CanonicalRef):
                raise SnapshotError("Snapshot member keys must be CanonicalRef values.")
            _require_fingerprint(fingerprint)
            if ref in members:
                raise SnapshotError(f"Snapshot contains duplicate member ref: {ref}.")
            members[ref] = fingerprint
        object.__setattr__(self, "members", MappingProxyType(members))

    def fingerprint_for(self, ref: CanonicalRef) -> str:
        """Return the captured fingerprint for *ref*."""
        if not isinstance(ref, CanonicalRef):
            raise SnapshotError("ref must be a CanonicalRef.")
        try:
            return self.members[ref]
        except KeyError as error:
            raise SnapshotError(f"Snapshot does not contain member ref: {ref}.") from error

    def refs(self) -> tuple[CanonicalRef, ...]:
        """Return member refs in their input insertion order."""
        return tuple(self.members)

    def resolve(self, registry: "CanonicalRegistry", ref: CanonicalRef) -> CanonicalObject:
        """Recover *ref* through its captured historical fingerprint, not current state."""
        fingerprint = self.fingerprint_for(ref)
        try:
            return registry.get_state(ref, fingerprint)
        except (AttributeError, CanonicalError) as error:
            raise SnapshotError(
                f"Snapshot member cannot be recovered: {ref} at {fingerprint}."
            ) from error

    def validate(self, registry: "CanonicalRegistry") -> None:
        """Verify that every recorded historical member remains recoverable."""
        for ref in self.refs():
            self.resolve(registry, ref)
