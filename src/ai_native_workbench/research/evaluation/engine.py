"""In-memory execution of versioned evaluation rules."""
from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Protocol
from ..canonical import CanonicalError, CanonicalRegistry, Claim, ResearchSnapshot
from .errors import EvaluationExecutionError, EvaluationResolutionError
from .model import EvaluationResult, EvaluationResultStatus, EvaluationRule, EvaluationRun, EvaluationRunStatus

@dataclass(frozen=True)
class EvaluationContext:
    run: EvaluationRun
    target: object
    canonical_registry: CanonicalRegistry | None = None
class EvaluationExecutor(Protocol):
    def evaluate(self, rule: EvaluationRule, context: EvaluationContext) -> EvaluationResult: ...

class EvaluationEngine:
    def __init__(self, rules: Mapping[str, EvaluationRule], executors: Mapping[str, EvaluationExecutor]) -> None:
        self._rules=dict(rules); self._executors=dict(executors)
    def run(self, run: EvaluationRun, *, target: object, canonical_registry: CanonicalRegistry|None=None) -> EvaluationRun:
        if run.status is not EvaluationRunStatus.CREATED: raise EvaluationExecutionError("Evaluation run must be created.")
        resolved=[]
        for key in sorted(run.evaluation_rule_versions):
            rule_id, version=key.split("@")
            rule=self._rules.get(rule_id)
            if rule is None or rule.version != version: raise EvaluationResolutionError(f"Unable to resolve evaluation rule: {key}.")
            executor=self._executors.get(rule_id)
            if executor is None: raise EvaluationResolutionError(f"No executor for evaluation rule: {key}.")
            resolved.append((rule,executor))
        running=replace(run,status=EvaluationRunStatus.RUNNING)
        context=EvaluationContext(running,target,canonical_registry); results=[]
        try:
            for rule, executor in resolved:
                result=executor.evaluate(rule,context)
                if not isinstance(result,EvaluationResult) or (result.run_id,result.rule_id,result.target_type,result.target_id)!=(run.run_id,rule.rule_id,run.target_type,run.target_id): raise EvaluationExecutionError("Executor returned a result that does not match the run.")
                results.append(result)
        except Exception:
            return replace(run,status=EvaluationRunStatus.FAILED,results=tuple(results))
        return replace(run,status=EvaluationRunStatus.COMPLETED,results=tuple(results))

def _mechanical_result(rule: EvaluationRule, context: EvaluationContext, status: EvaluationResultStatus, finding: str, subject_refs=()):
    return EvaluationResult(f"{context.run.run_id}:{rule.rule_id}",context.run.run_id,rule.rule_id,context.run.target_type,context.run.target_id,status,finding,rule.severity,tuple(subject_refs))
def _snapshot_context(context: EvaluationContext) -> ResearchSnapshot:
    if not isinstance(context.target,ResearchSnapshot) or context.canonical_registry is None: raise EvaluationExecutionError("Mechanical snapshot evaluation requires a snapshot and registry.")
    return context.target

def evaluate_snapshot_integrity(rule: EvaluationRule, context: EvaluationContext) -> EvaluationResult:
    _snapshot_context(context)
    try: context.canonical_registry.validate()  # type: ignore[union-attr]
    except CanonicalError as error: return _mechanical_result(rule,context,EvaluationResultStatus.FAIL,f"Canonical integrity validation failed: {error}")
    return _mechanical_result(rule,context,EvaluationResultStatus.PASS,"Canonical integrity validation passed.")
def evaluate_factual_claim_support(rule: EvaluationRule, context: EvaluationContext) -> EvaluationResult:
    snapshot=_snapshot_context(context); registry=context.canonical_registry
    unsupported=[]
    for ref in snapshot.refs():
        obj=snapshot.resolve(registry,ref)  # type: ignore[arg-type]
        if isinstance(obj,Claim) and obj.claim_type == "factual" and not obj.evidence_ids: unsupported.append(ref)
    if unsupported: return _mechanical_result(rule,context,EvaluationResultStatus.FAIL,f"{len(unsupported)} factual claims have no supporting evidence.",unsupported)
    return _mechanical_result(rule,context,EvaluationResultStatus.PASS,"All factual claims have supporting evidence.")
