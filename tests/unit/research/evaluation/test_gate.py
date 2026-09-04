from dataclasses import FrozenInstanceError
import pytest
from ai_native_workbench.research.evaluation import *
from ai_native_workbench.research.evaluation.gate import *
def rule(): return EvaluationRule("r","Rule","desc",EvaluationTargetType.SNAPSHOT,EvaluationMode.HUMAN_REQUIRED,"critical","1")
def run(status=EvaluationRunStatus.COMPLETED, result_status=EvaluationResultStatus.PASS):
 r=EvaluationResult("result","run","r",EvaluationTargetType.SNAPSHOT,"target",result_status,"finding")
 return EvaluationRun("run",EvaluationTargetType.SNAPSHOT,"target",("r@1",),"1",{},"now",status,(r,))
def review(decision): return HumanReviewRecord("review","run",EvaluationTargetType.SNAPSHOT,"target","person",decision,"now","comment")
def gate(current, reviews=()): return evaluate_quality_gate(QualityGatePolicy("gate","1",("r",)),current,rules={"r":rule()},human_reviews=reviews)
def test_all_mandatory_pass_results_produce_pass(): assert gate(run()).outcome is GateOutcome.PASS
def test_mandatory_fail_produces_fail(): assert gate(run(result_status=EvaluationResultStatus.FAIL), (review(HumanReviewDecision.ACCEPTED),)).outcome is GateOutcome.FAIL
def test_missing_mandatory_result_produces_review(): assert gate(EvaluationRun("run",EvaluationTargetType.SNAPSHOT,"target",("r@1",),"1",{},"now",EvaluationRunStatus.COMPLETED)).outcome is GateOutcome.REVIEW
def test_mandatory_inconclusive_produces_review_without_human_review(): assert gate(run(result_status=EvaluationResultStatus.INCONCLUSIVE)).outcome is GateOutcome.REVIEW
def test_accepted_review_resolves_inconclusive_result(): assert gate(run(result_status=EvaluationResultStatus.INCONCLUSIVE),(review(HumanReviewDecision.ACCEPTED),)).outcome is GateOutcome.PASS
def test_rejected_review_turns_inconclusive_result_into_fail(): assert gate(run(result_status=EvaluationResultStatus.INCONCLUSIVE),(review(HumanReviewDecision.REJECTED),)).outcome is GateOutcome.FAIL
def test_needs_revision_review_keeps_gate_at_review(): assert gate(run(result_status=EvaluationResultStatus.INCONCLUSIVE),(review(HumanReviewDecision.NEEDS_REVISION),)).outcome is GateOutcome.REVIEW
def test_gate_evaluation_is_immutable():
 with pytest.raises(FrozenInstanceError): gate(run()).finding="x"
