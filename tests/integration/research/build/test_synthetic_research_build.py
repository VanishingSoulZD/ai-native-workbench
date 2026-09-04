from ai_native_workbench.research.build import *
from ai_native_workbench.research.canonical import *
from ai_native_workbench.research.evaluation import GateOutcome, QualityGateEvaluation

def state():
 r=CanonicalRegistry(); s=Source('s','Title','Pub','https://x','report','','','high'); e=Entity('e','company','Name','active',{}); sr=r.register(s); er=r.register(e); ev=Evidence('v',sr,'Observed','','report','high',(),(),''); vr=r.register(ev); c=Claim('c','Version one',er,'factual','active',.8,(vr,)); cr=r.register(c); r.replace(vr,Evidence('v',sr,'Observed','','report','high',(cr,),(),'')); u=Unknown('u','Unknown?','Matters','scope','open'); ur=r.register(u); snap=r.snapshot('snap',(sr,er,vr,cr,ur),case_id='case',cutoff='2026',workflow_version='w'); return r,snap,cr
def gate(outcome=GateOutcome.PASS): return QualityGateEvaluation('gate','1','run',outcome,(),(),'ok')
def test_resolution_is_snapshot_bound_and_digest_normalized():
 r,s,cr=state(); old=s.resolve(r,cr); r.replace(cr,Claim('c','Version two',old.subject_ref,'factual','active',.8,old.evidence_ids)); assert resolve_snapshot_state(s,r).states[cr]==old
 spec=DeliverySpec(DeliveryType.DATASET,'json','p','r',{'x':1}); a=BuildInput(s.snapshot_id,s.case_id,s.cutoff,s.members,s.workflow_version,s.schema_version,s.transformation_version,spec.delivery_type,spec.format,spec.projection_version,spec.renderer_version,spec.configuration,{})
 assert compute_build_input_digest(a).startswith('sha256:')
def test_build_enforces_gate_and_builds_snapshot_state():
 r,s,cr=state(); r.replace(cr,Claim('c','Version two',r.get(cr).subject_ref,'factual','active',.8,r.get(cr).evidence_ids)); spec=DeliverySpec(DeliveryType.DATASET,'json','p','r',{})
 result=build_delivery(snapshot=s,registry=r,delivery_spec=spec,assumptions={},gate=gate(),build_id='b',created_at='now'); assert 'Version one' in result.artifact.payload; assert build_audit_manifest(result.artifact).content_digest==result.artifact.content_digest
 import pytest
 with pytest.raises(BuildPreconditionError): build_delivery(snapshot=s,registry=r,delivery_spec=spec,assumptions={},gate=gate(GateOutcome.REVIEW),build_id='b2',created_at='now')
