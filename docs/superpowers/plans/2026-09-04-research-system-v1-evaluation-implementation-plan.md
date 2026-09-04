# Research System v1 — Evaluation Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the minimum reusable Evaluation Core defined by the approved Step 4 design so a research snapshot or delivery artifact can be evaluated through versioned rules, immutable results, explicit human review, and a simple quality gate.

**Architecture:** Add an isolated `research.evaluation` package that treats Evaluation as a read-only assessment layer over Step 3 canonical state. The core contains versioned rules, immutable run/result records, explicit human review records, and rule-based quality gates; mechanical rules reuse Step 3 validation rather than duplicating it. The implementation remains in-memory and standard-library based, with small synthetic integration coverage and no benchmark, LLM-judge, database, agent, or delivery infrastructure.

**Tech Stack:** Python 3.11+, standard-library `dataclasses`, `enum`, `typing`, `collections.abc`; existing `pytest>=8,<9` test setup. No new runtime dependencies.

**Spec:** `docs/superpowers/specs/2026-09-04-research-system-v1-evaluation-design.md`

## Global Constraints

- **Evaluation assesses canonical research state; it does not become the authority for canonical research knowledge.**
- Existing Step 3 validation remains the authority for canonical structural integrity; Step 4 may consume validation outcomes but MUST NOT duplicate the same validation authority.
- Evaluation MUST NOT silently mutate canonical objects.
- Every EvaluationRun MUST identify an explicit immutable evaluation target.
- A completed EvaluationRun MUST NOT be mutated in place; later evaluation uses a new run.
- EvaluationResult status is only `pass`, `fail`, `inconclusive`, or `not_applicable`.
- `review` is a Quality Gate outcome, not an EvaluationResult status.
- Quality Gate outcome is only `PASS`, `REVIEW`, or `FAIL`.
- Human review is an explicit record, not an undocumented override mechanism.
- Evaluation execution failure MUST remain distinct from research-quality failure.
- Canonical object references in evaluation results MUST reuse Step 3 `CanonicalRef`.
- Step 4 MUST NOT introduce a second provenance/reference system for canonical knowledge.
- Step 4 MUST NOT introduce independent `EvaluationMetric` or `Score` core objects.
- Optional numeric `EvaluationResult.value` remains contextual to its rule/run/result.
- Step 4 MUST NOT introduce a weighted aggregate research-quality score.
- EvaluationRule MUST describe evaluation semantics, not prompt/model/agent/runtime implementation details.
- The first implementation does not require a separate `EvaluationTarget` class.
- The first implementation does not introduce `EvaluationFinding`, `GateRun`, reviewer identity infrastructure, governance platform, persistence layer, LLM judge framework, benchmark framework, vector database, MCP server, or agent runtime.
- All implementation tasks follow TDD: failing test, focused implementation, focused verification, full-suite verification, focused commit.
- Synthetic tests must not import or depend on `cases/001-ai-coding-agent-landscape/`.

---

## 1. Implementation Boundary and File Structure

Create the evaluation subsystem under:

```text
src/ai_native_workbench/research/evaluation/
├── __init__.py
├── errors.py
├── model.py
├── gate.py
└── engine.py
```

Responsibilities:

- `errors.py` — Evaluation-specific exception categories only.
- `model.py` — immutable domain records and enums for rules, runs, results, and human review; no execution logic.
- `gate.py` — pure Quality Gate policy evaluation over existing results and review records; no canonical-state inspection.
- `engine.py` — evaluator protocol, in-memory run execution, result collection, and built-in mechanical rules that delegate to Step 3 capabilities.
- `__init__.py` — stable public exports only.

Test structure:

```text
tests/unit/research/evaluation/
├── test_model.py
├── test_engine.py
└── test_gate.py

tests/integration/research/evaluation/
└── test_synthetic_research_evaluation.py
```

No existing Step 3 file should be modified by the core implementation unless a minimal public export adjustment is required; the preferred integration path is importing existing public Step 3 APIs.

---

## 2. Task 1: Bootstrap Evaluation Package and Immutable Core Records

**Files:**
- Create: `src/ai_native_workbench/research/evaluation/__init__.py`
- Create: `src/ai_native_workbench/research/evaluation/errors.py`
- Create: `src/ai_native_workbench/research/evaluation/model.py`
- Create: `tests/unit/research/evaluation/test_model.py`

**Interfaces:**
- Consumes: existing Python package layout and Step 3 `CanonicalRef` type.
- Produces:
  - `EvaluationTargetType`
  - `EvaluationMode`
  - `EvaluationResultStatus`
  - `EvaluationRunStatus`
  - `GateOutcome`
  - `HumanReviewDecision`
  - `EvaluationRule`
  - `EvaluationRun`
  - `EvaluationResult`
  - `HumanReviewRecord`
  - `EvaluationValidationError`
  - `EvaluationExecutionError`
  - `EvaluationResolutionError`

- [ ] **Step 1: Write the failing model tests**

Create tests covering valid construction, required fields, enum values, and immutability.

```python
from dataclasses import FrozenInstanceError
import pytest

from ai_native_workbench.research.canonical import CanonicalRef
from ai_native_workbench.research.evaluation import (
    EvaluationMode,
    EvaluationResult,
    EvaluationResultStatus,
    EvaluationRule,
    EvaluationRun,
    EvaluationRunStatus,
    EvaluationTargetType,
    HumanReviewDecision,
    HumanReviewRecord,
)


def make_rule() -> EvaluationRule:
    return EvaluationRule(
        rule_id="citation_accuracy",
        name="Citation Accuracy",
        description="Assess whether cited sources support the represented claims.",
        target_scope="delivery",
        mode=EvaluationMode.HUMAN_ASSISTED,
        severity="critical",
        version="1.0.0",
    )


def test_evaluation_rule_is_immutable():
    rule = make_rule()
    with pytest.raises(FrozenInstanceError):
        rule.name = "changed"  # type: ignore[misc]


def test_evaluation_rule_requires_non_empty_identity_fields():
    with pytest.raises(ValueError):
        EvaluationRule(
            rule_id="",
            name="Name",
            description="Description",
            target_scope="snapshot",
            mode=EvaluationMode.MECHANICAL,
            severity="warning",
            version="1.0.0",
        )


def test_evaluation_result_uses_only_declared_statuses():
    assert {member.value for member in EvaluationResultStatus} == {
        "pass",
        "fail",
        "inconclusive",
        "not_applicable",
    }


def test_quality_gate_review_is_not_an_evaluation_result_status():
    assert "review" not in {member.value for member in EvaluationResultStatus}


def test_run_lifecycle_is_minimal():
    assert {member.value for member in EvaluationRunStatus} == {
        "created",
        "running",
        "completed",
        "failed",
    }


def test_human_review_decisions_are_explicit():
    assert {member.value for member in HumanReviewDecision} == {
        "accepted",
        "rejected",
        "needs_revision",
    }
```

Also test `EvaluationRun` fields and `EvaluationResult` with `subject_refs` using actual `CanonicalRef` values; test `value` and `notes` are optional; test `HumanReviewRecord` references an existing run identifier by string and records reviewer/decision/time/comment.

- [ ] **Step 2: Run the focused test file to verify failure**

Run:

```bash
pytest tests/unit/research/evaluation/test_model.py -q
```

Expected: FAIL because the evaluation package and model types do not exist.

- [ ] **Step 3: Implement the exception categories and immutable records**

Implement the following exact enum values:

```python
class EvaluationTargetType(str, Enum):
    OBJECT = "object"
    SNAPSHOT = "snapshot"
    DELIVERY = "delivery"

class EvaluationMode(str, Enum):
    MECHANICAL = "mechanical"
    HUMAN_ASSISTED = "human_assisted"
    HUMAN_REQUIRED = "human_required"

class EvaluationResultStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    NOT_APPLICABLE = "not_applicable"

class EvaluationRunStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class GateOutcome(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    FAIL = "FAIL"

class HumanReviewDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
```

Implement frozen dataclasses with these fields:

```python
@dataclass(frozen=True)
class EvaluationRule:
    rule_id: str
    name: str
    description: str
    target_scope: EvaluationTargetType | str
    mode: EvaluationMode
    severity: str
    version: str

@dataclass(frozen=True)
class EvaluationRun:
    run_id: str
    target_type: EvaluationTargetType
    target_id: str
    evaluation_rule_versions: tuple[str, ...]
    evaluation_protocol_version: str
    configuration: Mapping[str, object]
    created_at: str
    status: EvaluationRunStatus

@dataclass(frozen=True)
class EvaluationResult:
    result_id: str
    run_id: str
    rule_id: str
    target_type: EvaluationTargetType
    target_id: str
    status: EvaluationResultStatus
    finding: str
    severity: str | None = None
    subject_refs: tuple[CanonicalRef, ...] = ()
    value: int | float | str | None = None
    notes: str | None = None

@dataclass(frozen=True)
class HumanReviewRecord:
    review_id: str
    run_id: str
    target_type: EvaluationTargetType
    target_id: str
    reviewer: str
    decision: HumanReviewDecision
    reviewed_at: str
    comment: str
```

Use `MappingProxyType` in `EvaluationRun.__post_init__` so configuration is immutable from callers. Validate required strings as non-empty, require `finding` to be non-empty, validate `subject_refs` contain only `CanonicalRef`, and reject booleans as numeric `value` because `bool` is an `int` subclass. `target_scope` must normalize to `EvaluationTargetType`; do not accept arbitrary scope values.

For `EvaluationRun.evaluation_rule_versions`, store version keys in the format `"<rule_id>@<version>"`. Validate each key is non-empty and unique.

- [ ] **Step 4: Export the public evaluation model**

`src/ai_native_workbench/research/evaluation/__init__.py` must export the enums, records, and three error classes; do not export private helpers.

- [ ] **Step 5: Run focused tests to verify pass**

Run:

```bash
pytest tests/unit/research/evaluation/test_model.py -q
```

Expected: PASS.

- [ ] **Step 6: Run the full suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/ai_native_workbench/research/evaluation tests/unit/research/evaluation/test_model.py
git commit -m "feat: add evaluation core records"
```

---

## 3. Task 2: Implement Evaluation Execution and Rule Interface

**Files:**
- Create: `src/ai_native_workbench/research/evaluation/engine.py`
- Modify: `src/ai_native_workbench/research/evaluation/__init__.py`
- Create: `tests/unit/research/evaluation/test_engine.py`

**Interfaces:**
- Consumes: `EvaluationRule`, `EvaluationRun`, `EvaluationResult`, `EvaluationRunStatus`, `EvaluationExecutionError`, and existing Step 3 canonical public APIs.
- Produces:
  - `EvaluationContext`
  - `EvaluationExecutor`
  - `EvaluationEngine`
  - `evaluate_snapshot_integrity`
  - `evaluate_factual_claim_support`
  - `EvaluationEngine.run(...) -> EvaluationRun`

- [ ] **Step 1: Write failing execution tests**

Cover these behaviors:

```python
def test_engine_executes_declared_rules(): ...
def test_engine_records_one_result_per_rule(): ...
def test_completed_run_is_immutable(): ...
def test_executor_failure_marks_run_failed_not_quality_failed(): ...
def test_unknown_rule_is_resolution_error(): ...
def test_result_subject_refs_use_canonical_refs(): ...
def test_engine_does_not_mutate_registry(): ...
def test_snapshot_integrity_rule_reuses_registry_validation(): ...
def test_factual_claim_support_rule_finds_missing_evidence(): ...
```

Use a tiny fake executor in tests:

```python
class FakeEvaluator:
    def __init__(self, result: EvaluationResult | None = None, error: Exception | None = None):
        self.result = result
        self.error = error

    def evaluate(self, rule: EvaluationRule, context: EvaluationContext) -> EvaluationResult:
        if self.error is not None:
            raise self.error
        assert self.result is not None
        return self.result
```

Test that the engine passes a rule-scoped context and that evaluator exceptions produce an `EvaluationRun` with `status=FAILED` without fabricating a `FAIL` result.

- [ ] **Step 2: Run focused tests to verify failure**

Run:

```bash
pytest tests/unit/research/evaluation/test_engine.py -q
```

Expected: FAIL because execution types do not exist.

- [ ] **Step 3: Implement the engine boundary**

Implement:

```python
@dataclass(frozen=True)
class EvaluationContext:
    run: EvaluationRun
    target: object
    canonical_registry: CanonicalRegistry | None = None

class EvaluationExecutor(Protocol):
    def evaluate(
        self,
        rule: EvaluationRule,
        context: EvaluationContext,
    ) -> EvaluationResult: ...
```

Implement:

```python
class EvaluationEngine:
    def __init__(self, executors: Mapping[str, EvaluationExecutor]) -> None: ...

    def run(
        self,
        run: EvaluationRun,
        *,
        target: object,
        canonical_registry: CanonicalRegistry | None = None,
    ) -> EvaluationRun: ...
```

The engine must:

1. validate that the Run status is `CREATED` before starting;
2. return a new `RUNNING` record internally rather than mutating the input Run;
3. parse every `rule_id@version` entry in `evaluation_rule_versions`;
4. resolve an executor by `rule_id` only, because the rule version is already recorded in the Run;
5. execute each rule in deterministic lexicographic order of `rule_id@version`;
6. create a single `EvaluationContext` per rule invocation containing the exact Run and target;
7. validate returned result `run_id`, `rule_id`, target type/id against the current Run before accepting the result;
8. on evaluator exception, return a new `EvaluationRun` with `FAILED` status and no fabricated quality result;
9. on successful completion, return a new `COMPLETED` Run while leaving all supplied records unchanged.

The engine itself does not persist a result store. It may maintain results in a private local tuple only for the duration of the run; add a read-only `results` tuple to `EvaluationRun` only if needed for gate evaluation. Prefer adding the field now so a completed Run is self-contained:

```python
results: tuple[EvaluationResult, ...] = ()
```

If this field is added, validate that every result belongs to this run and that result IDs are unique.

Do not introduce an evaluator registry abstraction beyond the `Mapping[str, EvaluationExecutor]` constructor argument.

- [ ] **Step 4: Implement mechanical Step 3-backed evaluators**

Implement:

```python
def evaluate_snapshot_integrity(
    rule: EvaluationRule,
    context: EvaluationContext,
) -> EvaluationResult: ...
```

For snapshot targets this function must call the existing `CanonicalRegistry.validate()` and convert outcomes as follows:

```text
validate() succeeds → PASS
CanonicalError/IntegrityError from the validation boundary → FAIL
unexpected evaluator exception → propagate to engine as execution failure
```

The finding must identify the integrity condition at a high level; do not copy exception internals into the canonical model.

Implement:

```python
def evaluate_factual_claim_support(
    rule: EvaluationRule,
    context: EvaluationContext,
) -> tuple[EvaluationResult, ...]: ...
```

This rule must inspect the exact `ResearchSnapshot` members, recover each historical object with `snapshot.resolve(...)`, and identify factual `Claim` objects whose `evidence_ids` are empty. It must report `FAIL` for each violating Claim using its `CanonicalRef` in `subject_refs`; Claims with required evidence are not individually emitted as failures. Do not mutate Claims, Evidence, or the Registry.

The engine should support only one-result-per-rule for the first implementation. Therefore the factual support evaluator should return one aggregated `EvaluationResult` whose `finding` reports the number of unsupported factual claims and whose `subject_refs` lists all violating Claim refs. This keeps the engine/result contract simple.

- [ ] **Step 5: Run focused tests to verify pass**

Run:

```bash
pytest tests/unit/research/evaluation/test_engine.py -q
```

Expected: PASS.

- [ ] **Step 6: Run related Step 3 tests and the full suite**

Run:

```bash
pytest tests/unit/research/canonical -q
pytest -q
```

Expected: PASS with no Step 3 regressions.

- [ ] **Step 7: Commit**

```bash
git add src/ai_native_workbench/research/evaluation/engine.py src/ai_native_workbench/research/evaluation/__init__.py tests/unit/research/evaluation/test_engine.py
git commit -m "feat: add evaluation execution core"
```

---

## 4. Task 3: Implement Quality Gate Policy

**Files:**
- Create: `src/ai_native_workbench/research/evaluation/gate.py`
- Modify: `src/ai_native_workbench/research/evaluation/__init__.py`
- Create: `tests/unit/research/evaluation/test_gate.py`

**Interfaces:**
- Consumes: completed `EvaluationRun.results`, `EvaluationRule` metadata, and `HumanReviewRecord` values.
- Produces:
  - `QualityGatePolicy`
  - `QualityGateEvaluation`
  - `evaluate_quality_gate(...) -> QualityGateEvaluation`

- [ ] **Step 1: Write failing gate tests**

Cover:

```python
def test_all_mandatory_pass_results_produce_pass(): ...
def test_mandatory_fail_produces_fail(): ...
def test_mandatory_inconclusive_produces_review(): ...
def test_human_required_without_accepted_review_produces_review(): ...
def test_accepted_human_review_allows_pass_when_result_is_inconclusive(): ...
def test_rejected_human_review_produces_fail_when_policy_blocks(): ...
def test_gate_does_not_reinspect_canonical_registry(): ...
def test_gate_result_is_immutable(): ...
```

Use a minimal policy representation:

```python
policy = QualityGatePolicy(
    gate_id="research-complete-v1",
    version="1.0.0",
    mandatory_rule_ids=(
        "canonical_integrity",
        "factual_claim_support",
        "reasoning_quality",
    ),
)
```

- [ ] **Step 2: Run focused tests to verify failure**

Run:

```bash
pytest tests/unit/research/evaluation/test_gate.py -q
```

Expected: FAIL because gate types do not exist.

- [ ] **Step 3: Implement the minimal gate policy**

Implement:

```python
@dataclass(frozen=True)
class QualityGatePolicy:
    gate_id: str
    version: str
    mandatory_rule_ids: tuple[str, ...]
```

Implement:

```python
@dataclass(frozen=True)
class QualityGateEvaluation:
    gate_id: str
    gate_version: str
    run_id: str
    outcome: GateOutcome
    result_ids: tuple[str, ...]
    human_review_ids: tuple[str, ...]
    finding: str
```

Implement:

```python
def evaluate_quality_gate(
    policy: QualityGatePolicy,
    run: EvaluationRun,
    *,
    rules: Mapping[str, EvaluationRule],
    human_reviews: tuple[HumanReviewRecord, ...] = (),
) -> QualityGateEvaluation: ...
```

Gate algorithm:

1. Select results whose `rule_id` is listed in `mandatory_rule_ids`.
2. If a mandatory result has `status=FAIL`, outcome is `FAIL` unless the result's rule is `HUMAN_ASSISTED` and an accepted human review explicitly records the result as accepted; in that case continue evaluation.
3. If a mandatory result has `status=INCONCLUSIVE` and there is no `accepted` HumanReviewRecord for that run/rule target, outcome is `REVIEW`.
4. If a mandatory rule has no result, outcome is `REVIEW` because required evaluation has not completed.
5. If every mandatory rule is satisfied and all `HUMAN_REQUIRED` rules have accepted human reviews, outcome is `PASS`.
6. `NOT_APPLICABLE` satisfies the gate only when that rule is present in the policy with explicit applicability recorded in its result; do not invent applicability from missing data.

The implementation must not inspect a `CanonicalRegistry`, resolve canonical refs, or perform any validation. It consumes only Run/Result/Rule/Review records.

Do not implement rule weighting, numeric aggregation, automatic thresholding, or a secondary gate state machine.

- [ ] **Step 4: Run focused tests to verify pass**

Run:

```bash
pytest tests/unit/research/evaluation/test_gate.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the full suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/evaluation/gate.py src/ai_native_workbench/research/evaluation/__init__.py tests/unit/research/evaluation/test_gate.py
git commit -m "feat: add evaluation quality gate"
```

---

## 5. Task 4: Add Explicit Human Review Records and Human-Required Flow Coverage

**Files:**
- Modify: `src/ai_native_workbench/research/evaluation/model.py`
- Modify: `src/ai_native_workbench/research/evaluation/gate.py`
- Modify: `tests/unit/research/evaluation/test_model.py`
- Modify: `tests/unit/research/evaluation/test_gate.py`

**Interfaces:**
- Consumes: `HumanReviewRecord`, `EvaluationRun`, `EvaluationResult`, and `QualityGatePolicy` from previous tasks.
- Produces: validated human-review semantics in the existing model; no new public object type.

- [ ] **Step 1: Write failing human-review tests**

Add tests that ensure:

```python
def test_review_requires_non_empty_reviewer_and_comment(): ...
def test_review_target_must_match_run_target(): ...
def test_accepted_review_is_only_valid_for_a_completed_or_failed_run(): ...
def test_needs_revision_review_keeps_gate_at_review(): ...
def test_human_review_does_not_mutate_evaluation_result(): ...
```

Use `dataclasses.replace` in the test to prove the original result remains unchanged when deriving any subsequent record.

- [ ] **Step 2: Run focused tests to verify failure**

Run:

```bash
pytest tests/unit/research/evaluation/test_model.py tests/unit/research/evaluation/test_gate.py -q
```

Expected: FAIL for newly asserted validation behavior.

- [ ] **Step 3: Implement the smallest validation additions**

Add `EvaluationRunStatus.COMPLETED` and `FAILED` target restrictions for review records: a HumanReviewRecord may only reference a run whose final status is known by the caller; since the immutable record only stores `run_id`, expose a validation helper in `gate.py`:

```python
def validate_human_review_for_run(
    review: HumanReviewRecord,
    run: EvaluationRun,
) -> None: ...
```

It must raise `EvaluationValidationError` if:

```text
review.run_id != run.run_id
review.target_type != run.target_type
review.target_id != run.target_id
run.status not in {COMPLETED, FAILED}
reviewer is empty
comment is empty
```

Use this helper from `evaluate_quality_gate` before consuming a review. Do not make HumanReviewRecord mutable or add a back-reference object.

- [ ] **Step 4: Run focused tests to verify pass**

Run:

```bash
pytest tests/unit/research/evaluation/test_model.py tests/unit/research/evaluation/test_gate.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the full suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/evaluation/model.py src/ai_native_workbench/research/evaluation/gate.py tests/unit/research/evaluation/test_model.py tests/unit/research/evaluation/test_gate.py
git commit -m "feat: enforce human review semantics"
```

---

## 6. Task 5: Add Synthetic End-to-End Evaluation Case

**Files:**
- Create: `tests/integration/research/evaluation/test_synthetic_research_evaluation.py`
- Modify: `src/ai_native_workbench/research/evaluation/__init__.py` only if a public import is missing

**Interfaces:**
- Consumes: complete Evaluation Core and Step 3 Canonical Registry/Snapshot APIs.
- Produces: integration proof that canonical state can be evaluated without mutation and can move through mechanical evaluation, human review, and Quality Gate.

- [ ] **Step 1: Write the failing synthetic end-to-end test**

Build a small registry entirely from literals using the existing Step 3 models:

```text
Source
Entity
Evidence
factual Claim
Unknown
Relationship
ResearchSnapshot
```

Construct a first snapshot with a supported factual Claim, then construct a second valid snapshot containing one additional factual Claim with no Evidence. Do not modify the first snapshot.

Create Rules:

```python
canonical_integrity = EvaluationRule(
    rule_id="canonical_integrity",
    name="Canonical Integrity",
    description="Canonical snapshot must satisfy Step 3 integrity validation.",
    target_scope="snapshot",
    mode=EvaluationMode.MECHANICAL,
    severity="critical",
    version="1.0.0",
)

factual_support = EvaluationRule(
    rule_id="factual_claim_support",
    name="Factual Claim Support",
    description="Every factual Claim must have supporting Evidence.",
    target_scope="snapshot",
    mode=EvaluationMode.MECHANICAL,
    severity="critical",
    version="1.0.0",
)

reasoning_quality = EvaluationRule(
    rule_id="reasoning_quality",
    name="Reasoning Quality",
    description="Research reasoning is acceptable for intended use.",
    target_scope="snapshot",
    mode=EvaluationMode.HUMAN_REQUIRED,
    severity="critical",
    version="1.0.0",
)
```

Run the engine against the second snapshot and assert:

```text
canonical_integrity = PASS
factual_claim_support = FAIL
reasoning_quality = no automated result until human review requirement is represented
```

Then run a gate and assert `FAIL` because factual support is a blocking failure.

Create a separate synthetic Run for a clean snapshot where mechanical results pass and the reasoning-quality result is `INCONCLUSIVE`. Assert Gate is `REVIEW`. Add an accepted HumanReviewRecord and assert Gate becomes `PASS` without mutating the original EvaluationResult or canonical snapshot.

Also assert the original snapshot remains recoverable after every evaluation operation, including exact historical claim state via `snapshot.resolve(...)`.

- [ ] **Step 2: Run the integration test to verify failure**

Run:

```bash
pytest tests/integration/research/evaluation/test_synthetic_research_evaluation.py -q
```

Expected: FAIL because the complete evaluation flow is not yet wired together.

- [ ] **Step 3: Fix only integration wiring and public exports needed for the test**

Do not add new architecture. The implementation must use the already-created model, engine, gate, and Step 3 public APIs.

The synthetic case must remain independent of Case 001 files and domain content.

- [ ] **Step 4: Run the integration test to verify pass**

Run:

```bash
pytest tests/integration/research/evaluation/test_synthetic_research_evaluation.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the complete validation suite**

Run:

```bash
pytest tests/unit/research/evaluation -q
pytest tests/unit/research/canonical -q
pytest tests/integration/research/evaluation -q
pytest tests/integration/research/canonical -q
pytest -q
python -m compileall src
```

Expected: all tests pass and compileall exits successfully.

- [ ] **Step 6: Check repository hygiene**

Run:

```bash
git diff --check
```

Expected: no output and exit code 0.

- [ ] **Step 7: Commit**

```bash
git add tests/integration/research/evaluation/test_synthetic_research_evaluation.py src/ai_native_workbench/research/evaluation/__init__.py
git commit -m "test: validate evaluation core end to end"
```

---

## 7. Task 6: Global Evaluation Core Exit Review and Documentation Alignment

**Files:**
- Modify: `docs/superpowers/specs/2026-09-04-research-system-v1-evaluation-design.md` only if an implementation-discovered contradiction requires a design correction approved before merging
- Modify: `docs/methodology/research-system-v1.md` only if an implementation-discovered roadmap mismatch is demonstrated and the change is explicitly within Step 4 scope
- No implementation files should be changed by this task unless a verified defect is found

**Interfaces:**
- Consumes: full Step 4 implementation, tests, approved Design Spec, System Contract, and methodology.
- Produces: verified Step 4 exit status and, only when necessary, a minimal corrective documentation change.

- [ ] **Step 1: Verify Design Spec coverage**

Check that implementation and tests cover:

```text
Evaluation vs Validation
Object / Snapshot / Delivery scope vocabulary
EvaluationRule
EvaluationRun
EvaluationResult
Metric/Score deferral
Mechanical / Human-assisted / Human-required modes
QualityGate PASS/REVIEW/FAIL
HumanReviewRecord
Snapshot-bound evaluation
immutability
execution failure vs quality failure
reproducibility context
Step 3 validation reuse
no canonical mutation
```

- [ ] **Step 2: Run targeted anti-regression searches**

Run:

```bash
grep -R "LLM\|OpenCompass\|MT-Bench\|MCP\|vector\|database\|agent runtime\|EvaluationMetric\|Score" src/ai_native_workbench/research/evaluation tests/unit/research/evaluation tests/integration/research/evaluation
```

Expected: no newly introduced implementation dependency on heavyweight evaluation infrastructure and no independent Metric/Score object.

- [ ] **Step 3: Run the final suite and hygiene checks**

Run:

```bash
pytest -q
python -m compileall src
git diff --check
git status --short
```

Expected:

```text
all tests pass
compileall succeeds
git diff --check is clean
working tree is clean after commit
```

- [ ] **Step 4: Record the Step 4 exit decision**

The Step 4 implementation is eligible for merge only if all of the following are true:

```text
Evaluation Core tests pass.
Existing Step 3 tests still pass.
Synthetic E2E evaluation passes.
No canonical object is mutated by evaluation.
No duplicate Step 3 provenance/validation authority was introduced.
No heavyweight infrastructure was introduced.
Historical evaluation records remain immutable.
Human review is explicit.
Gate semantics remain PASS/REVIEW/FAIL.
No weighted aggregate research-quality score exists.
```

If any item fails, stop at a clearly classified `BLOCKER`, `NON-BLOCKING`, or `NOTE` and do not claim Step 4 exit PASS.

- [ ] **Step 5: Commit only documentation corrections if required**

Use a focused commit such as:

```bash
git add docs/superpowers/specs/2026-09-04-research-system-v1-evaluation-design.md docs/methodology/research-system-v1.md
git commit -m "docs: align evaluation design after implementation review"
```

Do not create a speculative documentation change merely to produce a final commit.

---

## 8. Task-to-Requirement Coverage Matrix

| Design requirement | Primary task | Verification |
|---|---|---|
| Separate Evaluation from Validation | Tasks 2, 6 | Step 3 regression + engine/gate tests |
| Three evaluation scopes | Task 1 | model validation tests |
| EvaluationRule | Task 1 | model tests |
| EvaluationRun and rule-version context | Tasks 1–2 | engine tests |
| EvaluationResult statuses | Task 1 | model tests |
| Optional result value without Score object | Task 1 | model tests + anti-regression search |
| CanonicalRef subject refs | Tasks 1–2 | engine tests |
| Mechanical / human-assisted / human-required | Tasks 1–4 | engine/gate tests |
| QualityGate | Task 3 | gate tests |
| HumanReviewRecord | Task 4 | review/gate tests |
| Snapshot target immutability | Tasks 2, 5 | synthetic integration |
| No canonical mutation | Tasks 2, 5 | engine + E2E assertions |
| Execution failure distinct from quality failure | Task 2 | failure-path test |
| No weighted aggregate score | Tasks 3, 6 | gate design tests + search |
| No duplicated Step 3 validation | Task 2 | registry validation reuse + Step 3 regression |
| Historical evaluation immutability | Tasks 1–2 | frozen model + Run/result tests |
| Minimal standard-library implementation | All | dependency and anti-scope review |

---

## 9. Implementation Sequence

Execute tasks strictly in order because each task produces interfaces consumed by the next:

```text
Task 1
  ↓
Task 2
  ↓
Task 3
  ↓
Task 4
  ↓
Task 5
  ↓
Task 6 / Global Exit Review
```

Each Task is intended to be one independent implementation/review unit with its own focused tests and commit. Do not ask one Codex session to implement the entire plan. After each task:

```text
Codex implementation
    ↓
PR
    ↓
ChatGPT code review
    ↓
fix if necessary
    ↓
merge
    ↓
next task
```

The final Global Exit Review happens only after all task PRs are merged and the full suite passes.