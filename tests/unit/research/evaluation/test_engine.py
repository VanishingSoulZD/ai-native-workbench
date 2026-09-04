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
