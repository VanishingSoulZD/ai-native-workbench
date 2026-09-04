from dataclasses import replace
import pytest
from ai_native_workbench.research.evaluation import *
from ai_native_workbench.research.evaluation.engine import EvaluationContext, EvaluationEngine

def rule(rule_id, version="1"):
 return EvaluationRule(rule_id,rule_id,"desc",EvaluationTargetType.SNAPSHOT,EvaluationMode.MECHANICAL,"critical",version)
def run(keys=("b@1","a@1")):
 return EvaluationRun("run",EvaluationTargetType.SNAPSHOT,"snap",keys,"1",{},"now",EvaluationRunStatus.CREATED)
class Executor:
 def __init__(self, calls): self.calls=calls
 def evaluate(self, rule, context):
  self.calls.append(rule.rule_id); return EvaluationResult("r-"+rule.rule_id,context.run.run_id,rule.rule_id,context.run.target_type,context.run.target_id,EvaluationResultStatus.PASS,"ok")
def test_engine_executes_rules_in_deterministic_rule_key_order():
 calls=[]; completed=EvaluationEngine({"a":rule("a"),"b":rule("b")},{"a":Executor(calls),"b":Executor(calls)}).run(run(),target=object())
 assert calls == ["a","b"] and completed.status is EvaluationRunStatus.COMPLETED
def test_engine_rejects_non_created_run():
 with pytest.raises(EvaluationExecutionError): EvaluationEngine({},{}).run(replace(run(),status=EvaluationRunStatus.COMPLETED),target=object())
def test_engine_marks_run_failed_when_executor_raises():
 class Bad:
  def evaluate(self, rule, context): raise RuntimeError("crash")
 completed=EvaluationEngine({"a":rule("a")},{"a":Bad()}).run(run(("a@1",)),target=object())
 assert completed.status is EvaluationRunStatus.FAILED and not completed.results
def test_result_metadata_must_match_run():
 class Bad:
  def evaluate(self, rule, context): return EvaluationResult("r","other",rule.rule_id,context.run.target_type,context.run.target_id,EvaluationResultStatus.PASS,"x")
 assert EvaluationEngine({"a":rule("a")},{"a":Bad()}).run(run(("a@1",)),target=object()).status is EvaluationRunStatus.FAILED
def test_unknown_rule_raises_resolution_error():
 with pytest.raises(EvaluationResolutionError): EvaluationEngine({},{}).run(run(("a@1",)),target=object())

from ai_native_workbench.research.canonical import CanonicalRegistry, Claim, Entity, Evidence, Source


def _snapshot_with_claim(*, reverse_support=False):
 registry = CanonicalRegistry()
 source_ref = registry.register(Source("source", "Source", "Publisher", "https://example.test", "report", "", "", "primary"))
 entity_ref = registry.register(Entity("entity", "company", "Example", "active", {}))
 evidence_ref = Evidence("evidence", source_ref, "Observation", "", "quote", "A", (), (), "").canonical_ref
 claim = Claim("claim", "Example is supported.", entity_ref, "factual", "active", .9, (evidence_ref,))
 claim_ref = registry.register(claim)
 registry.register(Evidence("evidence", source_ref, "Observation", "", "quote", "A", (claim_ref,) if reverse_support else (), (), ""))
 return registry, registry.snapshot("snapshot", (source_ref, entity_ref, claim_ref, evidence_ref)), claim, claim_ref, evidence_ref


def _context(registry, snapshot):
 return EvaluationContext(run(("support@1",)), snapshot, registry)


def test_executor_failure_does_not_fabricate_quality_result():
 class Bad:
  def evaluate(self, rule, context): raise RuntimeError("crash")
 completed = EvaluationEngine({"a": rule("a")}, {"a": Bad()}).run(run(("a@1",)), target=object())
 assert completed.status is EvaluationRunStatus.FAILED
 assert completed.results == ()


def test_engine_does_not_mutate_registry_or_snapshot():
 registry, snapshot, *_ = _snapshot_with_claim(reverse_support=True)
 current_before = dict(registry._current); states_before = {ref: dict(states) for ref, states in registry._states.items()}; members_before = dict(snapshot.members)
 completed = EvaluationEngine({"support": rule("support")}, {"support": type("Support", (), {"evaluate": staticmethod(evaluate_factual_claim_support)})()}).run(run(("support@1",)), target=snapshot, canonical_registry=registry)
 assert completed.status is EvaluationRunStatus.COMPLETED
 assert dict(registry._current) == current_before and {ref: dict(states) for ref, states in registry._states.items()} == states_before and dict(snapshot.members) == members_before


def test_snapshot_integrity_rule_delegates_to_registry_validate(monkeypatch):
 registry, snapshot, *_ = _snapshot_with_claim(reverse_support=True)
 calls = []
 monkeypatch.setattr(registry, "validate", lambda: calls.append("validate"))
 result = evaluate_snapshot_integrity(rule("integrity"), EvaluationContext(run(("integrity@1",)), snapshot, registry))
 assert calls == ["validate"] and result.status is EvaluationResultStatus.PASS


def test_factual_support_rule_finds_evaluation_level_failure():
 registry, snapshot, *_ = _snapshot_with_claim(reverse_support=False)
 registry.validate()
 result = evaluate_factual_claim_support(rule("support"), _context(registry, snapshot))
 assert result.status is EvaluationResultStatus.FAIL and len(result.subject_refs) == 1


def test_factual_support_rule_uses_historical_snapshot_states():
 registry, snapshot, claim_v1, claim_ref, evidence_ref = _snapshot_with_claim(reverse_support=False)
 claim_v2 = replace(claim_v1, statement="Current claim text.")
 registry.replace(claim_ref, claim_v2)
 source_ref = snapshot.resolve(registry, next(ref for ref in snapshot.refs() if ref.logical_id == "source")).canonical_ref
 registry.replace(evidence_ref, Evidence("evidence", source_ref, "Observation", "", "quote", "A", (claim_ref,), (), ""))
 assert registry.get(claim_ref) == claim_v2
 assert snapshot.resolve(registry, claim_ref) == claim_v1
 result = evaluate_factual_claim_support(rule("support"), _context(registry, snapshot))
 assert result.status is EvaluationResultStatus.FAIL


def test_factual_support_resolution_failure_becomes_run_failure():
 registry, _, _, claim_ref, _ = _snapshot_with_claim(reverse_support=False)
 snapshot = registry.snapshot("missing-evidence", tuple(ref for ref in registry._current if ref.logical_id != "evidence"))
 assert claim_ref in snapshot.refs()
 completed = EvaluationEngine({"support": rule("support")}, {"support": type("Support", (), {"evaluate": staticmethod(evaluate_factual_claim_support)})()}).run(run(("support@1",)), target=snapshot, canonical_registry=registry)
 assert completed.status is EvaluationRunStatus.FAILED
 assert completed.results == ()
 assert not any(result.rule_id == "support" and result.status is EvaluationResultStatus.FAIL for result in completed.results)
