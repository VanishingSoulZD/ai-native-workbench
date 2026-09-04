from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from ..canonical import Claim, Entity, Evidence, Source, Unknown, Relationship
@dataclass(frozen=True)
class DatasetRow:
 ref:object; object_type:str; logical_id:str; fields:Mapping[str,object]
 def __post_init__(self): object.__setattr__(self,'fields',MappingProxyType(dict(self.fields)))
@dataclass(frozen=True)
class DatasetProjection: version:str; rows:tuple[DatasetRow,...]
@dataclass(frozen=True)
class ResearchNoteSection: heading:str; paragraphs:tuple[str,...]; refs:tuple[object,...]
@dataclass(frozen=True)
class ResearchNoteProjection: version:str; sections:tuple[ResearchNoteSection,...]
def _refs(v): return tuple(str(x) for x in v)
def _fields(o):
 if isinstance(o,Entity): return {'id':o.id,'name':o.name,'entity_type':o.entity_type,'status':o.status,'attributes':o.attributes}
 if isinstance(o,Claim): return {'id':o.id,'statement':o.statement,'claim_type':o.claim_type,'status':o.status,'confidence':o.confidence,'evidence_refs':_refs(o.evidence_ids),'subject_ref':str(o.subject_ref)}
 if isinstance(o,Evidence): return {'id':o.id,'observation':o.observation,'date_or_period':o.date_or_period,'evidence_type':o.evidence_type,'evidence_grade':o.evidence_grade,'source_ref':str(o.source_id),'claim_refs':_refs(o.supports_claim_ids+o.contradicts_claim_ids)}
 if isinstance(o,Source): return {'id':o.id,'canonical_title':o.canonical_title,'publisher':o.publisher,'canonical_url':o.canonical_url,'source_type':o.source_type,'published_at':o.published_at,'accessed_at':o.accessed_at,'quality_tier':o.quality_tier}
 if isinstance(o,Unknown): return {'id':o.id,'question':o.question,'why_it_matters':o.why_it_matters,'scope':o.scope,'status':o.status}
 if isinstance(o,Relationship): return {'id':o.id,'subject_ref':str(o.subject_ref),'predicate':o.predicate,'object_ref':str(o.object_ref),'evidence_refs':_refs(o.evidence_ids),'status':o.status}
 raise TypeError('unsupported canonical object')
def project_dataset(resolved,version='1'):
 return DatasetProjection(version,tuple(DatasetRow(r,r.object_type.value,r.logical_id,_fields(o)) for r,o in sorted(resolved.states.items(),key=lambda x:str(x[0]))))
def project_research_note(resolved,version='1'):
 s=resolved.snapshot; items=sorted(resolved.states.items(),key=lambda x:str(x[0])); claims=[(r,o) for r,o in items if isinstance(o,Claim) and o.claim_type=='factual']; unknowns=[(r,o) for r,o in items if isinstance(o,Unknown)]; sources=[(r,o) for r,o in items if isinstance(o,Source)]
 return ResearchNoteProjection(version,(ResearchNoteSection('Research Context',(f'Case: {s.case_id}',f'Cutoff: {s.cutoff}',f'Snapshot: {s.snapshot_id}'),()),ResearchNoteSection('Key Findings',tuple(f'{o.statement} (evidence: {", ".join(_refs(o.evidence_ids))})' for r,o in claims),tuple(r for r,o in claims)),ResearchNoteSection('Unknowns / Limitations',tuple(f'{o.question} — {o.why_it_matters}' for r,o in unknowns),tuple(r for r,o in unknowns)),ResearchNoteSection('Provenance',tuple(f'{o.canonical_title} — {o.canonical_url}' for r,o in sources),tuple(r for r,o in sources))))
