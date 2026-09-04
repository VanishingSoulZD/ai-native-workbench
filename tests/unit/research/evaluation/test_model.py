from dataclasses import FrozenInstanceError

import pytest

from ai_native_workbench.research.canonical import CanonicalObjectType, CanonicalRef
from ai_native_workbench.research.evaluation import (
    EvaluationMode, EvaluationResult, EvaluationResultStatus, EvaluationRule,
    EvaluationRun, EvaluationRunStatus, EvaluationTargetType, EvaluationValidationError,
    HumanReviewDecision, HumanReviewRecord,
)


def rule(**changes):
    values = dict(rule_id="factual_support", name="Factual support", description="Checks support.", target_scope=EvaluationTargetType.SNAPSHOT, mode=EvaluationMode.MECHANICAL, severity="critical", version="1")
    values.update(changes); return EvaluationRule(**values)


def test_rule_is_immutable():
    with pytest.raises(FrozenInstanceError): rule().name = "changed"


def test_rule_rejects_empty_fields():
    with pytest.raises(EvaluationValidationError): rule(name="")


def test_rule_rejects_invalid_scope_mode_and_severity():
    with pytest.raises(EvaluationValidationError): rule(target_scope="snapshot")
    with pytest.raises(EvaluationValidationError): rule(mode="mechanical")
    with pytest.raises(EvaluationValidationError): rule(severity="high")


def test_result_rejects_invalid_status():
    with pytest.raises(EvaluationValidationError): result(status="review")


def result(**changes):
    values = dict(result_id="result-1", run_id="run-1", rule_id="factual_support", target_type=EvaluationTargetType.SNAPSHOT, target_id="snapshot-1", status=EvaluationResultStatus.PASS, finding="Supported")
    values.update(changes); return EvaluationResult(**values)


def test_result_accepts_optional_value_and_notes():
    assert result(value=.5, notes="note").value == .5
    with pytest.raises(EvaluationValidationError): result(value=True)


def test_result_subject_refs_require_canonical_refs():
    ref = CanonicalRef(CanonicalObjectType.CLAIM, "claim-1")
    assert result(subject_refs=(ref,)).subject_refs == (ref,)
    with pytest.raises(EvaluationValidationError): result(subject_refs=("claim:claim-1",))


def test_run_has_only_declared_lifecycle_statuses():
    with pytest.raises(EvaluationValidationError): run(status="done")


def run(**changes):
    values = dict(run_id="run-1", target_type=EvaluationTargetType.SNAPSHOT, target_id="snapshot-1", evaluation_rule_versions=("factual_support@1",), evaluation_protocol_version="1", configuration={"x": [1]}, created_at="2026-09-04T00:00:00Z", status=EvaluationRunStatus.CREATED)
    values.update(changes); return EvaluationRun(**values)


def test_run_configuration_is_immutable():
    value = run()
    with pytest.raises(TypeError): value.configuration["y"] = 2
    assert value.configuration["x"] == (1,)


def test_run_rule_versions_are_unique():
    with pytest.raises(EvaluationValidationError): run(evaluation_rule_versions=("factual_support@1", "factual_support@1"))


def test_review_decisions_are_explicit():
    assert HumanReviewDecision.ACCEPTED.value == "accepted"


def test_review_record_is_immutable():
    review = HumanReviewRecord("review-1", "run-1", EvaluationTargetType.SNAPSHOT, "snapshot-1", "reviewer", HumanReviewDecision.ACCEPTED, "2026-09-04T00:00:00Z", "OK")
    with pytest.raises(FrozenInstanceError): review.comment = "changed"
