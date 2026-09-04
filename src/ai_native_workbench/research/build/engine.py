from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from types import MappingProxyType
from ..canonical import CanonicalRegistry, CanonicalRef, ResearchSnapshot, canonical_fingerprint, canonical_serialize
from ..evaluation import GateOutcome, QualityGateEvaluation
from .errors import BuildExecutionError, BuildPreconditionError, BuildValidationError
from .model import BuildManifest, BuildResult, BuildStatus, DeliveryArtifact, DeliverySpec, DeliveryType
@dataclass(frozen=True)
class ResolvedSnapshot:
    snapshot: ResearchSnapshot
    states: Mapping[CanonicalRef, object]
    def __post_init__(self): object.__setattr__(self,'states',MappingProxyType(dict(self.states)))
@dataclass(frozen=True)
class BuildInput:
    snapshot_id:str; case_id:str; cutoff:str; member_fingerprints:Mapping[CanonicalRef,str]; workflow_version:str; schema_version:str; transformation_version:str; delivery_type:DeliveryType; format:str; projection_version:str; renderer_version:str; configuration:Mapping[str,object]; assumptions:Mapping[str,object]

def resolve_snapshot_state(snapshot,registry):
    try:
        snapshot.validate(registry)
        return ResolvedSnapshot(snapshot,{ref:snapshot.resolve(registry,ref) for ref in snapshot.refs()})
    except Exception as e: raise BuildPreconditionError(f'Snapshot cannot be resolved: {e}') from e
def compute_build_input_digest(i):
    normalized={'snapshot_id':i.snapshot_id,'case_id':i.case_id,'cutoff':i.cutoff,'member_fingerprints':{str(k):v for k,v in i.member_fingerprints.items()},'workflow_version':i.workflow_version,'schema_version':i.schema_version,'transformation_version':i.transformation_version,'delivery_type':i.delivery_type.value,'format':i.format,'projection_version':i.projection_version,'renderer_version':i.renderer_version,'configuration':i.configuration,'assumptions':i.assumptions}
    return canonical_fingerprint(normalized)
def create_build_manifest(*,build_id,created_at,snapshot,delivery_spec,assumptions,gate,build_input_digest):
    return BuildManifest(build_id,created_at,snapshot.snapshot_id,snapshot.case_id,snapshot.cutoff,snapshot.members, snapshot.workflow_version,snapshot.schema_version,snapshot.transformation_version,delivery_spec.projection_version,delivery_spec.renderer_version,delivery_spec.delivery_type,delivery_spec.format,delivery_spec.configuration,assumptions,gate.gate_id,gate.gate_version,gate.outcome.value,gate.run_id,build_input_digest)
def build_audit_manifest(artifact):
    from .model import AuditManifest
    return AuditManifest(artifact.manifest,artifact.artifact_id,artifact.content_digest)
def build_delivery(*,snapshot,registry,delivery_spec,assumptions,gate,build_id,created_at):
    resolved=resolve_snapshot_state(snapshot,registry)
    if gate.outcome is not GateOutcome.PASS: raise BuildPreconditionError(f'Quality gate is {gate.outcome.value}.')
    input=BuildInput(snapshot.snapshot_id,snapshot.case_id,snapshot.cutoff,snapshot.members,snapshot.workflow_version,snapshot.schema_version,snapshot.transformation_version,delivery_spec.delivery_type,delivery_spec.format,delivery_spec.projection_version,delivery_spec.renderer_version,delivery_spec.configuration,assumptions)
    digest=compute_build_input_digest(input)
    try:
        from .projection import project_dataset,project_research_note
        from .renderers import render_dataset_json,render_dataset_csv,render_research_note_markdown
        if delivery_spec.delivery_type is DeliveryType.DATASET:
            projection=project_dataset(resolved,delivery_spec.projection_version); payload=render_dataset_json(projection) if delivery_spec.format=='json' else render_dataset_csv(projection) if delivery_spec.format=='csv' else None
        elif delivery_spec.delivery_type is DeliveryType.RESEARCH_NOTE and delivery_spec.format=='markdown': projection=project_research_note(resolved,delivery_spec.projection_version); payload=render_research_note_markdown(projection)
        else: payload=None
        if payload is None: raise BuildValidationError('Unsupported delivery format.')
    except BuildValidationError: raise
    except Exception as e: raise BuildExecutionError('Delivery rendering failed.') from e
    manifest=create_build_manifest(build_id=build_id,created_at=created_at,snapshot=snapshot,delivery_spec=delivery_spec,assumptions=assumptions,gate=gate,build_input_digest=digest)
    content=sha256(payload.encode()).hexdigest(); artifact=DeliveryArtifact(f'{build_id}:{delivery_spec.delivery_type.value}',delivery_spec.delivery_type,delivery_spec.format,build_id,manifest,payload,content)
    return BuildResult(BuildStatus.COMPLETED,artifact)
