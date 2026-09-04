# Research System v1 — Evaluation Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the minimum reusable Evaluation Core defined by the approved Step 4 Design Spec so a stable research snapshot or delivery target can be evaluated through versioned rules, immutable results, explicit human review, and a simple quality gate.

**Architecture:** Add an isolated `research.evaluation` package that treats Evaluation as a read-only assessment layer over Step 3 canonical state. The core contains versioned rules, immutable run/result records, explicit human review records, and rule-based quality gates; mechanical rules reuse Step 3 validation instead of duplicating it. The implementation remains in-memory and standard-library based and proves the complete loop with synthetic tests, without benchmark infrastructure, LLM judges, persistence, agents, or Case 001 migration.

**Tech Stack:** Python 3.11+, standard-library `dataclasses`, `enum`, `typing`, `collections.abc`; existing `pytest>=8,<9` test setup. No new runtime dependencies.

**Spec:** `docs/superpowers/specs/2026-09-04-research-system-v1-evaluation-design.md`

## Global Constraints

- **Evaluation assesses canonical research state; it does not become the authority for canonical research knowledge.**
- Step 3 validation remains the authority for canonical structural/intrinsic integrity; Step 4 may consume validation outcomes but MUST NOT duplicate it or manufacture canonical-invalid state for an evaluation scenario.
- Evaluation MUST NOT silently mutate canonical objects.
- Every `EvaluationRun` MUST identify an explicit immutable evaluation target.
- A completed `EvaluationRun` MUST NOT be mutated in place; later evaluation creates a new run.
- `EvaluationResult` status is only `pass`, `fail`, `inconclusive`, or `not_applicable`.
- `REVIEW` is a Quality Gate outcome, not an `EvaluationResult` status.
- Quality Gate outcome is only `PASS`, `REVIEW`, or `FAIL`.
- Human review is an explicit record, not an undocumented override mechanism.
- Evaluator execution failure MUST remain distinct from research-quality failure.
- Canonical object references in evaluation results MUST reuse Step 3 `CanonicalRef`.
- Step 4 MUST NOT introduce a second provenance/reference system for canonical knowledge.
- Step 4 MUST NOT introduce independent `EvaluationMetric` or `Score` core objects.
- Optional `EvaluationResult.value` remains contextual to its rule/run/result.
- Step 4 MUST NOT introduce a weighted aggregate research-quality score.
- `EvaluationRule` MUST describe evaluation semantics, not prompt/model/agent/runtime implementation details.
- The first implementation does not require a separate `EvaluationTarget` class.
- The first implementation does not introduce `EvaluationFinding`, `GateRun`, reviewer identity infrastructure, governance platform, persistence layer, LLM judge framework, benchmark framework, vector database, MCP server, or agent runtime.
- All implementation tasks follow TDD: failing test, focused implementation, focused verification, full-suite verification, focused commit.
- Synthetic tests must not import or depend on `cases/001-ai-coding-agent-landscape/`.

---

## 1. Implementation Boundary and File Structure

Create:

```text
src/ai_native_workbench/research/evaluation/
├── __init__.py
├── errors.py
├── model.py
├── engine.py
└── gate.py
```

Responsibilities:

- `errors.py` — evaluation-specific exception hierarchy.
- `model.py` — immutable enums and records only; no execution logic.
- `engine.py` — evaluator protocol, in-memory execution, Step 3-backed mechanical rules, and result collection.
- `gate.py` — pure gate policy evaluation over results, rules, and human reviews; no canonical-state inspection.
- `__init__.py` — stable public exports only.

Create tests:

```text
tests/unit/research/evaluation/
├── test_model.py
├── test_engine.py
└── test_gate.py

tests/integration/research/evaluation/
└── test_synthetic_research_evaluation.py
```

Do not modify Step 3 implementation files unless a missing public export makes integration impossible; prefer existing public Step 3 APIs.

---

## 2. Task 1: Build Immutable Evaluation Contracts

**Files:**
- Create: `src/ai_native_workbench/research/evaluation/__init__.py`
- Create: `src/ai_native_workbench/research/evaluation/errors.py`
- Create: `src/ai_native_workbench/research/evaluation/model.py`
- Create: `tests/unit/research/evaluation/test_model.py`

**Interfaces:**
- Consumes: Step 3 `CanonicalRef` and existing package/test conventions.
- Produces:
  - `EvaluationTargetType`
  - `EvaluationMode`
  - `EvaluationResultStatus`
  - `EvaluationRunStatus`
  - `GateOutcome`
  - `HumanReviewDecision`
  - `EvaluationRule`
  - `EvaluationResult`
  - `EvaluationRun`
  - `HumanReviewRecord`
  - `EvaluationValidationError`
  - `EvaluationExecutionError`
  - `EvaluationResolutionError`

- [ ] **Step 1: Write the failing tests**

Cover:

```python
def test_rule_is_immutable(): ...
def test_rule_rejects_empty_fields(): ...
def test_rule_rejects_invalid_scope_mode_and_severity(): ...
def test_result_rejects_invalid_status(): ...
def test_result_accepts_optional_value_and_notes(): ...
def test_result_subject_refs_require_canonical_refs(): ...
def test_run_has_only_declared_lifecycle_statuses(): ...
def test_run_configuration_is_immutable(): ...
def test_run_rule_versions_are_unique(): ...
def test_review_decisions_are_explicit(): ...
def test_review_record_is_immutable(): ...
```

Use actual `CanonicalRef` instances in `subject_refs`; do not use strings for canonical object references.

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/evaluation/test_model.py -q
```

Expected: FAIL because the evaluation package does not yet exist.

- [ ] **Step 3: Implement exact enum vocabularies**

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

Implement frozen dataclasses:

```python
@dataclass(frozen=True)
class EvaluationRule:
    rule_id: str
    name: str
    description: str
    target_scope: EvaluationTargetType
    mode: EvaluationMode
    severity: str
    version: str

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
class EvaluationRun:
    run_id: str
    target_type: EvaluationTargetType
    target_id: str
    evaluation_rule_versions: tuple[str, ...]
    evaluation_protocol_version: str
    configuration: Mapping[str, object]
    created_at: str
    status: EvaluationRunStatus
    results: tuple[EvaluationResult, ...] = ()

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

Validation requirements:

```text
all identity/name/description/version/timestamp fields required by the spec are non-empty
severity ∈ {informational, warning, critical}
subject_refs contains only CanonicalRef
value rejects bool and accepts int/float/str/None
EvaluationRun.evaluation_rule_versions uses unique '<rule_id>@<version>' keys
EvaluationRun.results contains only results with matching run_id and unique result_id
HumanReviewRecord reviewer/comment are non-empty
```

Use `MappingProxyType` for `EvaluationRun.configuration`. Validate `target_scope` and `target_type` through `EvaluationTargetType`; do not accept arbitrary strings.

Implement the three errors as siblings under a common `EvaluationError` base:

```python
class EvaluationError(RuntimeError): ...
class EvaluationValidationError(EvaluationError): ...
class EvaluationExecutionError(EvaluationError): ...
class EvaluationResolutionError(EvaluationError): ...
```

- [ ] **Step 4: Export only the public contracts and errors**

`__init__.py` exports the enums, dataclasses, and errors defined above. Keep private helpers private.

- [ ] **Step 5: Run focused and full tests**

```bash
pytest tests/unit/research/evaluation/test_model.py -q
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/evaluation tests/unit/research/evaluation/test_model.py
git commit -m "feat: add evaluation core contracts"
```

---

## 3. Task 2: Implement Rule Execution and Step 3-Backed Mechanical Evaluation

**Files:**
- Create: `src/ai_native_workbench/research/evaluation/engine.py`
- Modify: `src/ai_native_workbench/research/evaluation/__init__.py`
- Create: `tests/unit/research/evaluation/test_engine.py`

**Interfaces:**
- Consumes: Task 1 contracts plus existing Step 3 `CanonicalRegistry`, `ResearchSnapshot`, `Claim`, `CanonicalRef`, and canonical errors.
- Produces:
  - `EvaluationContext`
  - `EvaluationExecutor`
  - `EvaluationEngine`
  - `evaluate_snapshot_integrity`
  - `evaluate_factual_claim_support`

- [ ] **Step 1: Write failing tests**

Cover:

```python
def test_engine_executes_rules_in_deterministic_rule_key_order(): ...
def test_engine_rejects_non_created_run(): ...
def test_engine_marks_run_failed_when_executor_raises(): ...
def test_executor_failure_does_not_fabricate_quality_result(): ...
def test_result_metadata_must_match_run(): ...
def test_unknown_rule_raises_resolution_error(): ...
def test_engine_does_not_mutate_registry_or_snapshot(): ...
def test_snapshot_integrity_rule_delegates_to_registry_validate(): ...
def test_factual_support_rule_finds_evaluation_level_failure(): ...
def test_factual_support_rule_uses_historical_snapshot_states(): ...
```

Use a fake evaluator that records invocation order and returns a valid `EvaluationResult`. Use a fake evaluator that raises `RuntimeError` to prove execution failure is not converted to a quality `FAIL` result.

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/evaluation/test_engine.py -q
```

Expected: FAIL because engine types do not exist.

- [ ] **Step 3: Implement `EvaluationContext` and executor protocol**

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

`EvaluationContext` is read-only and is the only context an executor receives. It must not expose the evaluator implementation, prompt, model, agent, or runtime internals.

- [ ] **Step 4: Implement `EvaluationEngine`**

```python
class EvaluationEngine:
    def __init__(
        self,
        rules: Mapping[str, EvaluationRule],
        executors: Mapping[str, EvaluationExecutor],
    ) -> None: ...

    def run(
        self,
        run: EvaluationRun,
        *,
        target: object,
        canonical_registry: CanonicalRegistry | None = None,
    ) -> EvaluationRun: ...
```

Requirements:

1. Require input `run.status == CREATED`.
2. Resolve every `rule_id@version` against `rules` using the exact rule id and version; a mismatched or missing version raises `EvaluationResolutionError`.
3. Execute rule keys in deterministic lexicographic order.
4. Create a `RUNNING` value with `dataclasses.replace`; never mutate the input `run`.
5. Pass a read-only `EvaluationContext` containing the exact target object.
6. Validate returned result `run_id`, `rule_id`, `target_type`, and `target_id` against the run/rule before accepting it.
7. Require exactly one `EvaluationResult` per declared rule in the first implementation.
8. On evaluator exception, return a new `EvaluationRun(status=FAILED, results=partial_results)` and do not fabricate a `FAIL` result.
9. On success, return a new `EvaluationRun(status=COMPLETED, results=all_results)`.
10. Never mutate `CanonicalRegistry`, `ResearchSnapshot`, or any canonical object.

The engine is an in-memory execution boundary only. It does not persist runs or results.

- [ ] **Step 5: Implement `evaluate_snapshot_integrity`**

```python
def evaluate_snapshot_integrity(
    rule: EvaluationRule,
    context: EvaluationContext,
) -> EvaluationResult: ...
```

Requirements:

- target must be a `ResearchSnapshot` and a `CanonicalRegistry` must be supplied;
- call `canonical_registry.validate()` exactly as the Step 3 authority;
- successful validation produces `PASS`;
- `CanonicalError`/`IntegrityError` from the validation boundary produces `FAIL` with a concise finding;
- unexpected exceptions propagate to the engine as execution failure;
- do not copy canonical validation exception internals into canonical state.

- [ ] **Step 6: Implement `evaluate_factual_claim_support`**

```python
def evaluate_factual_claim_support(
    rule: EvaluationRule,
    context: EvaluationContext,
) -> EvaluationResult: ...
```

Requirements:

- target must be a `ResearchSnapshot` and the Registry must be supplied;
- iterate exact snapshot members and recover historical state through `snapshot.resolve(registry, ref)` rather than `registry.get(ref)`;
- for every factual `Claim`, resolve its declared `evidence_ids` through the same snapshot and require at least one resolved `Evidence.supports_claim_ids` to contain the Claim ref; this is an evaluation-level support-quality criterion, not Step 3’s non-empty-forward-reference invariant;
- return one aggregated `EvaluationResult`:
  - `PASS` when no unsupported factual claims exist;
  - `FAIL` when one or more exist;
  - `subject_refs` lists the violating Claim refs;
  - `finding` reports the count;
- derived Claims are not subject to the factual-claim rule;
- do not mutate any canonical object.

- [ ] **Step 7: Run focused, Step 3, and full tests**

```bash
pytest tests/unit/research/evaluation/test_engine.py -q
pytest tests/unit/research/canonical -q
pytest -q
```

Expected: PASS with no Step 3 regressions.

- [ ] **Step 8: Commit**

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
- Consumes: `EvaluationRule`, `EvaluationRun`, `EvaluationResult`, `HumanReviewRecord`, and gate enums.
- Produces:
  - `QualityGatePolicy`
  - `QualityGateEvaluation`
  - `evaluate_quality_gate(...)`
  - `validate_human_review_for_run(...)`

- [ ] **Step 1: Write failing gate tests**

Cover:

```python
def test_all_mandatory_pass_results_produce_pass(): ...
def test_mandatory_fail_produces_fail(): ...
def test_missing_mandatory_result_produces_review(): ...
def test_mandatory_inconclusive_produces_review_without_human_review(): ...
def test_accepted_review_resolves_inconclusive_result(): ...
def test_rejected_review_turns_inconclusive_result_into_fail(): ...
def test_needs_revision_review_keeps_gate_at_review(): ...
def test_human_review_does_not_override_explicit_fail(): ...
def test_gate_does_not_inspect_registry_or_canonical_objects(): ...
def test_gate_evaluation_is_immutable(): ...
```

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/evaluation/test_gate.py -q
```

Expected: FAIL because gate types do not exist.

- [ ] **Step 3: Implement the gate records**

```python
@dataclass(frozen=True)
class QualityGatePolicy:
    gate_id: str
    version: str
    mandatory_rule_ids: tuple[str, ...]

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

Validate non-empty ids/version and unique mandatory rule ids.

- [ ] **Step 4: Implement human review/run compatibility validation**

```python
def validate_human_review_for_run(
    review: HumanReviewRecord,
    run: EvaluationRun,
) -> None: ...
```

Reject when:

```text
review.run_id != run.run_id
review.target_type != run.target_type
review.target_id != run.target_id
run.status not in {COMPLETED, FAILED}
reviewer is empty
comment is empty
```

This helper must not modify either record.

- [ ] **Step 5: Implement `evaluate_quality_gate`**

```python
def evaluate_quality_gate(
    policy: QualityGatePolicy,
    run: EvaluationRun,
    *,
    rules: Mapping[str, EvaluationRule],
    human_reviews: tuple[HumanReviewRecord, ...] = (),
) -> QualityGateEvaluation: ...
```

Apply these exact rules in order:

1. A `FAILED` run returns `REVIEW` with “Evaluation run failed before all evaluation criteria were completed.” A `CREATED` or `RUNNING` run also returns `REVIEW`; none can receive `PASS`. This is execution-state handling, not a fabricated quality `FAIL`.
2. A mandatory rule with no corresponding result causes `REVIEW`.
3. A mandatory result with `FAIL` causes `FAIL`. Human review MUST NOT silently override an explicit failure.
4. A mandatory result with `PASS` satisfies the rule.
5. A mandatory result with `NOT_APPLICABLE` satisfies the rule only when the rule itself declares applicability is optional through the policy/configuration used by that rule; do not infer N/A from missing evidence.
6. A mandatory `INCONCLUSIVE` result with no accepted human review causes `REVIEW`.
7. In v1 a matching `HumanReviewRecord` explicitly reviews the entire run, so an accepted decision may resolve its human-required `INCONCLUSIVE` results; a future per-rule model must add explicit association.
8. A rejected review for an `INCONCLUSIVE` result causes `FAIL`.
9. A `NEEDS_REVISION` review keeps the gate at `REVIEW`.
10. If every mandatory condition is satisfied, outcome is `PASS`.
11. The gate implementation does not inspect `CanonicalRegistry`, `ResearchSnapshot`, or canonical objects.

The gate uses explicit policy. It does not use numeric weighting, averages, thresholds across heterogeneous dimensions, or a secondary state machine.

- [ ] **Step 6: Run focused and full tests**

```bash
pytest tests/unit/research/evaluation/test_gate.py -q
pytest -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/ai_native_workbench/research/evaluation/gate.py src/ai_native_workbench/research/evaluation/__init__.py tests/unit/research/evaluation/test_gate.py
git commit -m "feat: add evaluation quality gate"
```

---

## 5. Task 4: Prove Human Review and Historical Immutability End to End

**Files:**
- Modify: `tests/unit/research/evaluation/test_model.py`
- Modify: `tests/unit/research/evaluation/test_gate.py`
- Create: `tests/integration/research/evaluation/test_synthetic_research_evaluation.py`

**Interfaces:**
- Consumes: complete Task 1–3 Evaluation Core and existing Step 3 canonical APIs.
- Produces: integration proof of snapshot-bound evaluation, human review, gate outcomes, and non-mutation.

- [ ] **Step 1: Write independent failing synthetic scenarios**

Construct legal canonical snapshots entirely from literals; do not use Case 001 or bypass Step 3 validation.

**Scenario A** contains a factual Claim with non-empty `evidence_ids` but Evidence whose `supports_claim_ids` does not name the Claim. It must prove:

```text
canonical_integrity = PASS
factual_claim_support = FAIL
Gate = FAIL
```

This is a valid canonical snapshot with an evaluation-specific quality failure.

**Scenario B** contains explicitly supporting Evidence and a human-required `reasoning_quality` result of `INCONCLUSIVE`. It must prove:

```text
canonical_integrity = PASS
factual_claim_support = PASS
Gate without review = REVIEW
accepted review = PASS
rejected review = FAIL
needs_revision review = REVIEW
```

- [ ] **Step 2: Prove immutability and historical state recovery**

Capture the snapshot’s Claim v1, then `registry.replace(claim_ref, claim_v2)` and assert current registry state is v2 while `snapshot.resolve(registry, claim_ref)` remains v1. Also prove the input run, completed run/result records, snapshot membership, registry current state, and registry historical states remain unchanged by evaluation.

- [ ] **Step 3: Add gate and engine regressions**

Include `test_failed_run_cannot_produce_pass`, executor-crash/no-fabricated-result, non-mutation, validation delegation, evaluation-level factual-support failure, and historical snapshot-state tests.

- [ ] **Step 4: Add HumanReviewRecord and prove Gate PASS**

Create:

```python
HumanReviewRecord(
    review_id="review-reasoning-1",
    run_id=completed_run.run_id,
    target_type=completed_run.target_type,
    target_id=completed_run.target_id,
    reviewer="researcher-1",
    decision=HumanReviewDecision.ACCEPTED,
    reviewed_at="2026-09-04T00:00:00Z",
    comment="Reviewed reasoning quality against the declared research purpose.",
)
```

Re-run gate evaluation and assert `PASS`.

Also create `REJECTED` and `NEEDS_REVISION` variants in focused tests and assert `FAIL` and `REVIEW` respectively for an `INCONCLUSIVE` human-required result.

- [ ] **Step 5: Prove immutability and non-mutation**

Assert:

```text
input EvaluationRun is unchanged
completed EvaluationRun is unchanged after gate evaluation
EvaluationResult is unchanged after HumanReviewRecord creation
ResearchSnapshot membership is unchanged
historical Claim state is still recoverable with snapshot.resolve(...)
current Registry state is not rewritten by evaluation
```

Use equality assertions plus `FrozenInstanceError` checks where appropriate.

- [ ] **Step 6: Run the integration and regression suite**

```bash
pytest tests/integration/research/evaluation/test_synthetic_research_evaluation.py -q
pytest tests/unit/research/evaluation -q
pytest tests/unit/research/canonical -q
pytest tests/integration/research/canonical -q
pytest -q
```

Expected: PASS.

- [ ] **Step 7: Run compile and hygiene checks**

```bash
python -m compileall src
git diff --check
```

Expected: both commands succeed with no reported issues.

- [ ] **Step 8: Commit**

```bash
git add tests/integration/research/evaluation/test_synthetic_research_evaluation.py tests/unit/research/evaluation/test_model.py tests/unit/research/evaluation/test_gate.py
git commit -m "test: validate evaluation core end to end"
```

---

## 6. Task 5: Final Evaluation Core Exit Review

**Files:**
- Review only by default.
- Modify: `docs/superpowers/specs/2026-09-04-research-system-v1-evaluation-design.md` only if implementation exposes a genuine contradiction that requires an approved design correction.
- Modify: `docs/methodology/research-system-v1.md` only if a concrete Step 4 roadmap mismatch is discovered.

**Interfaces:**
- Consumes: all implementation tasks, tests, approved Design Spec, System Contract, and methodology.
- Produces: a verified Step 4 exit decision; no new architecture.

- [ ] **Step 1: Verify implementation against the Design Spec**

Confirm each requirement is implemented and tested:

```text
Evaluation vs Validation boundary
Object / Snapshot / Delivery scope vocabulary
EvaluationRule
EvaluationRun
EvaluationResult
Metric/Score deferral
Mechanical / Human-assisted / Human-required modes
QualityGate PASS/REVIEW/FAIL
HumanReviewRecord
Snapshot-bound target semantics
immutability
execution failure vs quality failure
reproducibility context
Step 3 validation reuse
no canonical mutation
```

- [ ] **Step 2: Check for scope creep**

Run:

```bash
grep -R -E "OpenCompass|MT-Bench|LLM[ -]?Judge|EvaluationMetric|Score|MCP|vector database|database persistence|agent runtime|benchmark framework" src/ai_native_workbench/research/evaluation tests/unit/research/evaluation tests/integration/research/evaluation
```

Expected: no heavyweight infrastructure or independent Metric/Score implementation is introduced. References inside tests/docs describing excluded scope are acceptable; implementation imports/dependencies are not.

- [ ] **Step 3: Run the final verification set**

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
git diff --check succeeds
working tree is clean after the final task commit
```

- [ ] **Step 4: Classify any findings before merge**

Use only:

```text
BLOCKER
NON-BLOCKING
NOTE
```

Do not claim Step 4 PASS while any blocker remains unresolved.

- [ ] **Step 5: Commit documentation corrections only when justified**

If implementation reveals a real documentation contradiction and the correction is approved, use a focused commit:

```bash
git add docs/superpowers/specs/2026-09-04-research-system-v1-evaluation-design.md docs/methodology/research-system-v1.md
git commit -m "docs: align evaluation design after implementation review"
```

Do not make speculative documentation edits.

---

## 7. Task-to-Requirement Coverage

| Requirement | Task | Primary verification |
|---|---|---|
| Evaluation separate from Validation | 2, 3, 5 | engine/gate tests + Step 3 regression |
| Three evaluation scopes | 1 | model validation |
| EvaluationRule | 1 | model tests |
| Snapshot-bound EvaluationRun | 2, 4 | engine + synthetic E2E |
| Immutable run/result records | 1, 2, 4 | frozen models + non-mutation tests |
| EvaluationResult status vocabulary | 1 | model tests |
| CanonicalRef subject references | 1, 2 | model/engine tests |
| Optional numeric value without Score object | 1, 5 | model tests + scope check |
| Metric/Score deferral | 1, 5 | architecture/scope review |
| Mechanical reuse of Step 3 validation | 2 | delegation test + Step 3 suite |
| Human-assisted / human-required modes | 1, 4 | model/gate tests |
| HumanReviewRecord | 1, 3, 4 | review/gate/E2E tests |
| QualityGate policy | 3 | gate tests |
| PASS/REVIEW/FAIL semantics | 3, 4 | gate tests |
| Explicit execution failure | 2 | failure-path tests |
| No canonical mutation | 2, 4 | registry/snapshot assertions |
| Historical reproducibility | 2, 4 | snapshot historical recovery |
| No weighted aggregate score | 3, 5 | gate tests + scope review |
| No heavyweight evaluation infrastructure | all, 5 | dependency/scope check |

---

## 8. Execution Order and Review Protocol

Execute in strict order:

```text
Task 1
  ↓
Task 2
  ↓
Task 3
  ↓
Task 4
  ↓
Task 5 / Global Exit Review
```

Each implementation task is an independent implementation/review unit:

```text
Codex session
    ↓
Task implementation
    ↓
Task PR
    ↓
ChatGPT independent code review
    ↓
fix / follow-up review if needed
    ↓
merge
    ↓
next task
```

Do not ask a single Codex session to implement Tasks 1–4 together. The purpose of the decomposition is to preserve independent review gates and make boundary violations easy to isolate.

The final Step 4 Exit Review occurs only after Tasks 1–4 have been implemented, reviewed, fixed, and merged, and the complete repository suite passes.