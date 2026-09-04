"""Pure policy evaluation for evaluation results and human reviews."""
from collections.abc import Mapping
from dataclasses import dataclass
from .errors import EvaluationValidationError
from .model import EvaluationResultStatus, EvaluationRule, EvaluationRun, EvaluationRunStatus, GateOutcome, HumanReviewDecision, HumanReviewRecord

def _text(value: object, name: str):
    if not isinstance(value,str) or not value.strip(): raise EvaluationValidationError(f"{name} must be a non-empty string.")
@dataclass(frozen=True)
class QualityGatePolicy:
    gate_id: str; version: str; mandatory_rule_ids: tuple[str,...]
    def __post_init__(self):
        _text(self.gate_id,"gate_id"); _text(self.version,"version")
        if not isinstance(self.mandatory_rule_ids,tuple) or not self.mandatory_rule_ids or len(set(self.mandatory_rule_ids)) != len(self.mandatory_rule_ids) or any(not isinstance(x,str) or not x.strip() for x in self.mandatory_rule_ids): raise EvaluationValidationError("mandatory_rule_ids must be unique non-empty values.")
@dataclass(frozen=True)
class QualityGateEvaluation:
    gate_id: str; gate_version: str; run_id: str; outcome: GateOutcome; result_ids: tuple[str,...]; human_review_ids: tuple[str,...]; finding: str
    def __post_init__(self):
        for n in ("gate_id","gate_version","run_id","finding"): _text(getattr(self,n),n)
        if not isinstance(self.outcome,GateOutcome): raise EvaluationValidationError("outcome must be a GateOutcome.")

def validate_human_review_for_run(review: HumanReviewRecord, run: EvaluationRun) -> None:
    if (review.run_id,review.target_type,review.target_id) != (run.run_id,run.target_type,run.target_id): raise EvaluationValidationError("Human review does not match evaluation run.")
    if run.status not in {EvaluationRunStatus.COMPLETED,EvaluationRunStatus.FAILED}: raise EvaluationValidationError("Human review requires a completed or failed run.")
    _text(review.reviewer,"reviewer"); _text(review.comment,"comment")
def evaluate_quality_gate(policy: QualityGatePolicy, run: EvaluationRun, *, rules: Mapping[str,EvaluationRule], human_reviews: tuple[HumanReviewRecord,...]=()) -> QualityGateEvaluation:
    for review in human_reviews: validate_human_review_for_run(review,run)
    by_rule={r.rule_id:r for r in run.results}; review_ids=tuple(r.review_id for r in human_reviews)
    result_ids=tuple(r.result_id for r in run.results if r.rule_id in policy.mandatory_rule_ids)
    outcome=GateOutcome.PASS; finding="All mandatory evaluation conditions are satisfied."
    for rule_id in policy.mandatory_rule_ids:
        if rule_id not in rules: raise EvaluationValidationError(f"Mandatory rule is unknown: {rule_id}.")
        result=by_rule.get(rule_id)
        if result is None: outcome=GateOutcome.REVIEW; finding=f"Mandatory rule {rule_id} has no result."; break
        if result.status is EvaluationResultStatus.FAIL: outcome=GateOutcome.FAIL; finding=f"Mandatory rule {rule_id} failed."; break
        if result.status is EvaluationResultStatus.NOT_APPLICABLE: outcome=GateOutcome.REVIEW; finding=f"Mandatory rule {rule_id} is not applicable without declared optionality."; break
        if result.status is EvaluationResultStatus.INCONCLUSIVE:
            decisions={r.decision for r in human_reviews}
            if HumanReviewDecision.REJECTED in decisions: outcome=GateOutcome.FAIL; finding=f"Human review rejected mandatory rule {rule_id}."; break
            if HumanReviewDecision.ACCEPTED not in decisions: outcome=GateOutcome.REVIEW; finding=f"Mandatory rule {rule_id} requires human review."; break
    return QualityGateEvaluation(policy.gate_id,policy.version,run.run_id,outcome,result_ids,review_ids,finding)
