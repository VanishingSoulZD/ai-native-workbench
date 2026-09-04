"""Synthetic, snapshot-bound evaluation proof without Case 001 fixtures."""
from dataclasses import FrozenInstanceError
import pytest
from ai_native_workbench.research.canonical import CanonicalRegistry, Claim, Entity, Evidence, Relationship, Source, Unknown
from ai_native_workbench.research.evaluation import *

def _rule(i, mode): return EvaluationRule(i,i,"Synthetic criterion",EvaluationTargetType.SNAPSHOT,mode,"critical","1")
def _case():
 registry=CanonicalRegistry(); source=Source("source","Source","Publisher","https://example.test","report","","","primary"); entity=Entity("entity","company","Example","active",{})
 source_ref=registry.register(source); entity_ref=registry.register(entity)
 claim=Claim("claim","Example is supported.",entity_ref,"factual","active",.9,(Evidence("placeholder",source_ref,"x","","quote","A",(),(),"").canonical_ref,))
 claim_ref=registry.register(claim); evidence=Evidence("placeholder",source_ref,"Observation","","quote","A",(claim_ref,),(),"")
 registry.register(evidence); unknown=Unknown("unknown","What remains?","Scope","snapshot","open"); registry.register(unknown)
 relationship=Relationship("relationship",entity_ref,"has_claim",claim_ref,(evidence.canonical_ref,),"active"); registry.register(relationship)
 snapshot=registry.snapshot("snapshot",(source_ref,entity_ref,claim_ref,evidence.canonical_ref,unknown.canonical_ref,relationship.canonical_ref))
 return registry,snapshot,claim_ref
class Reasoning:
 def evaluate(self,rule,context): return EvaluationResult("reasoning-result",context.run.run_id,rule.rule_id,context.run.target_type,context.run.target_id,EvaluationResultStatus.INCONCLUSIVE,"Human assessment required")
def test_synthetic_clean_snapshot_human_review_and_non_mutation():
 registry,snapshot,claim_ref=_case(); members_before=dict(snapshot.members); claim_before=snapshot.resolve(registry,claim_ref)
 integrity=_rule("canonical_integrity",EvaluationMode.MECHANICAL); support=_rule("factual_claim_support",EvaluationMode.MECHANICAL); reasoning=_rule("reasoning_quality",EvaluationMode.HUMAN_REQUIRED)
 run=EvaluationRun("run",EvaluationTargetType.SNAPSHOT,snapshot.snapshot_id,("reasoning_quality@1","factual_claim_support@1","canonical_integrity@1"),"1",{},"2026-09-04T00:00:00Z",EvaluationRunStatus.CREATED)
 engine=EvaluationEngine({r.rule_id:r for r in (integrity,support,reasoning)},{"canonical_integrity":type("Integrity",(),{"evaluate":staticmethod(evaluate_snapshot_integrity)})(),"factual_claim_support":type("Support",(),{"evaluate":staticmethod(evaluate_factual_claim_support)})(),"reasoning_quality":Reasoning()})
 completed=engine.run(run,target=snapshot,canonical_registry=registry)
 assert run.status is EvaluationRunStatus.CREATED and completed.status is EvaluationRunStatus.COMPLETED
 assert [r.status for r in completed.results] == [EvaluationResultStatus.PASS,EvaluationResultStatus.PASS,EvaluationResultStatus.INCONCLUSIVE]
 policy=QualityGatePolicy("gate","1",("canonical_integrity","factual_claim_support","reasoning_quality")); rules={r.rule_id:r for r in (integrity,support,reasoning)}
 assert evaluate_quality_gate(policy,completed,rules=rules).outcome is GateOutcome.REVIEW
 accepted=HumanReviewRecord("review",completed.run_id,completed.target_type,completed.target_id,"researcher",HumanReviewDecision.ACCEPTED,"2026-09-04T00:00:00Z","Reviewed reasoning quality.")
 assert evaluate_quality_gate(policy,completed,rules=rules,human_reviews=(accepted,)).outcome is GateOutcome.PASS
 assert evaluate_quality_gate(policy,completed,rules=rules,human_reviews=(HumanReviewRecord("reject",completed.run_id,completed.target_type,completed.target_id,"researcher",HumanReviewDecision.REJECTED,"now","No."),)).outcome is GateOutcome.FAIL
 assert dict(snapshot.members) == members_before and snapshot.resolve(registry,claim_ref) == claim_before
 with pytest.raises(FrozenInstanceError): completed.results[0].finding="changed"
