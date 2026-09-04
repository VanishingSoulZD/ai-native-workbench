"""Snapshot-bound orchestration for reproducible delivery builds."""

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from types import MappingProxyType

from ..canonical import (
    CanonicalRef,
    CanonicalRegistry,
    ResearchSnapshot,
    canonical_fingerprint,
)
from ..evaluation import GateOutcome, QualityGateEvaluation
from .errors import BuildExecutionError, BuildPreconditionError, BuildValidationError
from .model import (
    AuditManifest,
    BuildManifest,
    BuildResult,
    BuildStatus,
    DeliveryArtifact,
    DeliverySpec,
    DeliveryType,
)


@dataclass(frozen=True)
class ResolvedSnapshot:
    snapshot: ResearchSnapshot
    states: Mapping[CanonicalRef, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "states", MappingProxyType(dict(self.states)))


@dataclass(frozen=True)
class BuildInput:
    snapshot_id: str
    case_id: str
    cutoff: str
    member_fingerprints: Mapping[CanonicalRef, str]
    workflow_version: str
    schema_version: str
    transformation_version: str
    delivery_type: DeliveryType
    format: str
    projection_version: str
    renderer_version: str
    configuration: Mapping[str, object]
    assumptions: Mapping[str, object]


def resolve_snapshot_state(snapshot: ResearchSnapshot, registry: CanonicalRegistry) -> ResolvedSnapshot:
    try:
        snapshot.validate(registry)
        states = {ref: snapshot.resolve(registry, ref) for ref in snapshot.refs()}
        return ResolvedSnapshot(snapshot, states)
    except Exception as error:
        raise BuildPreconditionError(f"Snapshot cannot be resolved: {error}") from error


def compute_build_input_digest(build_input: BuildInput) -> str:
    normalized = {
        "snapshot_id": build_input.snapshot_id,
        "case_id": build_input.case_id,
        "cutoff": build_input.cutoff,
        "member_fingerprints": {
            str(ref): fingerprint
            for ref, fingerprint in build_input.member_fingerprints.items()
        },
        "workflow_version": build_input.workflow_version,
        "schema_version": build_input.schema_version,
        "transformation_version": build_input.transformation_version,
        "delivery_type": build_input.delivery_type.value,
        "format": build_input.format,
        "projection_version": build_input.projection_version,
        "renderer_version": build_input.renderer_version,
        "configuration": build_input.configuration,
        "assumptions": build_input.assumptions,
    }
    return canonical_fingerprint(normalized)


def create_build_manifest(
    *,
    build_id: str,
    created_at: str,
    snapshot: ResearchSnapshot,
    delivery_spec: DeliverySpec,
    assumptions: Mapping[str, object],
    gate: QualityGateEvaluation,
    build_input_digest: str,
) -> BuildManifest:
    return BuildManifest(
        build_id, created_at, snapshot.snapshot_id, snapshot.case_id, snapshot.cutoff,
        snapshot.members, snapshot.workflow_version, snapshot.schema_version,
        snapshot.transformation_version, delivery_spec.projection_version,
        delivery_spec.renderer_version, delivery_spec.delivery_type, delivery_spec.format,
        delivery_spec.configuration, assumptions, gate.gate_id, gate.gate_version,
        gate.outcome.value, gate.run_id, build_input_digest,
    )


def build_audit_manifest(artifact: DeliveryArtifact) -> AuditManifest:
    return AuditManifest(artifact.manifest, artifact.artifact_id, artifact.content_digest)


def build_delivery(
    *,
    snapshot: ResearchSnapshot,
    registry: CanonicalRegistry,
    delivery_spec: DeliverySpec,
    assumptions: Mapping[str, object],
    gate: QualityGateEvaluation,
    build_id: str,
    created_at: str,
) -> BuildResult:
    resolved = resolve_snapshot_state(snapshot, registry)
    if gate.outcome is not GateOutcome.PASS:
        raise BuildPreconditionError(f"Quality gate is {gate.outcome.value}.")
    build_input = BuildInput(
        snapshot.snapshot_id, snapshot.case_id, snapshot.cutoff, snapshot.members,
        snapshot.workflow_version, snapshot.schema_version, snapshot.transformation_version,
        delivery_spec.delivery_type, delivery_spec.format, delivery_spec.projection_version,
        delivery_spec.renderer_version, delivery_spec.configuration, assumptions,
    )
    build_input_digest = compute_build_input_digest(build_input)
    try:
        from .projection import project_dataset, project_research_note
        from .renderers import (
            render_dataset_csv,
            render_dataset_json,
            render_research_note_markdown,
        )
        if delivery_spec.delivery_type is DeliveryType.DATASET:
            projection = project_dataset(resolved, delivery_spec.projection_version)
            if delivery_spec.format == "json":
                payload = render_dataset_json(projection)
            elif delivery_spec.format == "csv":
                payload = render_dataset_csv(projection)
            else:
                raise BuildValidationError("Unsupported dataset format.")
        elif (
            delivery_spec.delivery_type is DeliveryType.RESEARCH_NOTE
            and delivery_spec.format == "markdown"
        ):
            projection = project_research_note(resolved, delivery_spec.projection_version)
            payload = render_research_note_markdown(projection)
        else:
            raise BuildValidationError("Unsupported delivery format.")
    except BuildValidationError:
        raise
    except Exception as error:
        raise BuildExecutionError("Delivery rendering failed.") from error
    manifest = create_build_manifest(
        build_id=build_id, created_at=created_at, snapshot=snapshot,
        delivery_spec=delivery_spec, assumptions=assumptions, gate=gate,
        build_input_digest=build_input_digest,
    )
    artifact = DeliveryArtifact(
        f"{build_id}:{delivery_spec.delivery_type.value}",
        delivery_spec.delivery_type, delivery_spec.format, build_id, manifest, payload,
        sha256(payload.encode("utf-8")).hexdigest(),
    )
    return BuildResult(BuildStatus.COMPLETED, artifact)
