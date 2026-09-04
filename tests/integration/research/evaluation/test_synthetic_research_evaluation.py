"""Independent synthetic proof of snapshot-bound evaluation semantics."""
from dataclasses import FrozenInstanceError, replace

import pytest

from ai_native_workbench.research.canonical import CanonicalRegistry, Claim, Entity, Evidence, Source
from ai_native_workbench.research.evaluation import *


def _rule(rule_id, mode):
    return EvaluationRule(rule_id, rule_id, "Synthetic criterion", EvaluationTargetType.SNAPSHOT, mode, "critical", "1")


def _case(*, explicitly_supporting):
    registry = CanonicalRegistry()
    source_ref = registry.register(Source("source", "Source", "Publisher", "https://example.test", "report", "", "", "primary"))
    entity_ref = registry.register(Entity("entity", "company", "Example", "active", {}))
    evidence_ref = Evidence("evidence", source_ref, "Observation", "", "quote", "A", (), (), "").canonical_ref
    claim_v1 = Claim("claim", "Example is supported.", entity_ref, "factual", "active", .9, (evidence_ref,))
    claim_ref = registry.register(claim_v1)
    registry.register(Evidence("evidence", source_ref, "Observation", "", "quote", "A", (claim_ref,) if explicitly_supporting else (), (), ""))
    snapshot = registry.snapshot("snapshot", (source_ref, entity_ref, claim_ref, evidence_ref))
    return registry, snapshot, claim_v1, claim_ref, evidence_ref


class Reasoning:
    def evaluate(self, rule, context):
        return EvaluationResult("reasoning-result", context.run.run_id, rule.rule_id, context.run.target_type, context.run.target_id, EvaluationResultStatus.INCONCLUSIVE, "Human assessment required")


def _run(snapshot, rule_keys):
    return EvaluationRun("run", EvaluationTargetType.SNAPSHOT, snapshot.snapshot_id, rule_keys, "1", {}, "2026-09-04T00:00:00Z", EvaluationRunStatus.CREATED)


def _engine(rules):
    return EvaluationEngine({rule.rule_id: rule for rule in rules}, {
        "canonical_integrity": type("Integrity", (), {"evaluate": staticmethod(evaluate_snapshot_integrity)})(),
        "factual_claim_support": type("Support", (), {"evaluate": staticmethod(evaluate_factual_claim_support)})(),
        "reasoning_quality": Reasoning(),
    })


def test_scenario_a_legal_canonical_snapshot_has_evaluation_quality_failure():
    registry, snapshot, *_ = _case(explicitly_supporting=False)
    integrity = _rule("canonical_integrity", EvaluationMode.MECHANICAL)
    support = _rule("factual_claim_support", EvaluationMode.MECHANICAL)
    run = _run(snapshot, ("factual_claim_support@1", "canonical_integrity@1"))
    completed = _engine((integrity, support)).run(run, target=snapshot, canonical_registry=registry)
    assert registry.validate() is None
    assert [result.status for result in completed.results] == [EvaluationResultStatus.PASS, EvaluationResultStatus.FAIL]
    gate = evaluate_quality_gate(QualityGatePolicy("gate", "1", ("canonical_integrity", "factual_claim_support")), completed, rules={rule.rule_id: rule for rule in (integrity, support)})
    assert gate.outcome is GateOutcome.FAIL


def test_scenario_b_human_review_and_historical_immutability():
    registry, snapshot, claim_v1, claim_ref, _ = _case(explicitly_supporting=True)
    claim_v2 = replace(claim_v1, statement="Current registry wording.")
    registry.replace(claim_ref, claim_v2)
    assert registry.get(claim_ref) == claim_v2
    assert snapshot.resolve(registry, claim_ref) == claim_v1
    integrity = _rule("canonical_integrity", EvaluationMode.MECHANICAL)
    support = _rule("factual_claim_support", EvaluationMode.MECHANICAL)
    reasoning = _rule("reasoning_quality", EvaluationMode.HUMAN_REQUIRED)
    rules = (integrity, support, reasoning)
    run = _run(snapshot, ("reasoning_quality@1", "factual_claim_support@1", "canonical_integrity@1"))
    members_before = dict(snapshot.members)
    current_before = dict(registry._current)
    states_before = {ref: dict(states) for ref, states in registry._states.items()}
    completed = _engine(rules).run(run, target=snapshot, canonical_registry=registry)
    assert run.status is EvaluationRunStatus.CREATED and run.results == ()
    assert completed.status is EvaluationRunStatus.COMPLETED
    assert [result.status for result in completed.results] == [EvaluationResultStatus.PASS, EvaluationResultStatus.PASS, EvaluationResultStatus.INCONCLUSIVE]
    assert dict(snapshot.members) == members_before and dict(registry._current) == current_before
    assert {ref: dict(states) for ref, states in registry._states.items()} == states_before
    assert snapshot.resolve(registry, claim_ref) == claim_v1
    policy = QualityGatePolicy("gate", "1", ("canonical_integrity", "factual_claim_support", "reasoning_quality"))
    rules_by_id = {rule.rule_id: rule for rule in rules}
    assert evaluate_quality_gate(policy, completed, rules=rules_by_id).outcome is GateOutcome.REVIEW
    for decision, expected in ((HumanReviewDecision.ACCEPTED, GateOutcome.PASS), (HumanReviewDecision.REJECTED, GateOutcome.FAIL), (HumanReviewDecision.NEEDS_REVISION, GateOutcome.REVIEW)):
        review = HumanReviewRecord(f"review-{decision.value}", completed.run_id, completed.target_type, completed.target_id, "researcher", decision, "2026-09-04T00:00:00Z", "Reviewed the entire evaluation run.")
        assert evaluate_quality_gate(policy, completed, rules=rules_by_id, human_reviews=(review,)).outcome is expected
    with pytest.raises(FrozenInstanceError):
        completed.results[0].finding = "changed"
