from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from ..canonical import CanonicalRef
from ..evaluation import GateOutcome
from .errors import BuildValidationError

def _freeze(v):
    if isinstance(v, Mapping): return MappingProxyType({k:_freeze(x) for k,x in v.items()})
    if isinstance(v, (list,tuple)): return tuple(_freeze(x) for x in v)
    return v
def _text(v,n):
    if not isinstance(v,str) or not v.strip(): raise BuildValidationError(f'{n} must be non-empty.')
def _digest(v,n):
    _text(v,n)
    if not v.startswith('sha256:') or len(v)!=71: raise BuildValidationError(f'{n} must be a sha256 digest.')
class DeliveryType(str,Enum): DATASET='dataset'; RESEARCH_NOTE='research_note'
class BuildStatus(str,Enum): COMPLETED='completed'
@dataclass(frozen=True)
class DeliverySpec:
    delivery_type: DeliveryType; format: str; projection_version: str; renderer_version: str; configuration: Mapping[str,object]
    def __post_init__(self):
        if not isinstance(self.delivery_type,DeliveryType): raise BuildValidationError('delivery_type must be DeliveryType.')
        for n in ('format','projection_version','renderer_version'): _text(getattr(self,n),n)
        if not isinstance(self.configuration,Mapping): raise BuildValidationError('configuration must be a mapping.')
        object.__setattr__(self,'configuration',_freeze(self.configuration))
@dataclass(frozen=True)
class BuildManifest:
    build_id:str; created_at:str; snapshot_id:str; case_id:str; cutoff:str; member_fingerprints:Mapping[CanonicalRef,str]; workflow_version:str; schema_version:str; transformation_version:str; projection_version:str; renderer_version:str; delivery_type:DeliveryType; format:str; configuration:Mapping[str,object]; assumptions:Mapping[str,object]; evaluation_gate_id:str; evaluation_gate_version:str; evaluation_outcome:str; evaluation_run_id:str; build_input_digest:str
    def __post_init__(self):
        for n in ('build_id','created_at','snapshot_id','case_id','cutoff','workflow_version','schema_version','transformation_version','projection_version','renderer_version','format','evaluation_gate_id','evaluation_gate_version','evaluation_outcome','evaluation_run_id'): _text(getattr(self,n),n)
        if not isinstance(self.delivery_type,DeliveryType): raise BuildValidationError('delivery_type must be DeliveryType.')
        if self.evaluation_outcome not in {x.value for x in GateOutcome}: raise BuildValidationError('invalid gate outcome.')
        if not isinstance(self.member_fingerprints,Mapping) or any(not isinstance(k,CanonicalRef) or not isinstance(v,str) or not v for k,v in self.member_fingerprints.items()): raise BuildValidationError('invalid member fingerprints.')
        for n in ('member_fingerprints','configuration','assumptions'):
            v=getattr(self,n)
            if not isinstance(v,Mapping): raise BuildValidationError(f'{n} must be a mapping.')
            object.__setattr__(self,n,_freeze(v))
        _digest(self.build_input_digest,'build_input_digest')
@dataclass(frozen=True)
class DeliveryArtifact:
    artifact_id:str; delivery_type:DeliveryType; format:str; build_id:str; manifest:BuildManifest; payload:str; content_digest:str
    def __post_init__(self):
        for n in ('artifact_id','format','build_id','payload','content_digest'): _text(getattr(self,n),n)
        if not isinstance(self.delivery_type,DeliveryType) or not isinstance(self.manifest,BuildManifest): raise BuildValidationError('invalid artifact contract.')
        if self.manifest.build_id != self.build_id or self.manifest.delivery_type is not self.delivery_type or self.manifest.format != self.format: raise BuildValidationError('artifact does not match manifest.')
@dataclass(frozen=True)
class BuildResult: status:BuildStatus; artifact:DeliveryArtifact
@dataclass(frozen=True)
class AuditManifest: build_manifest:BuildManifest; artifact_id:str; content_digest:str
