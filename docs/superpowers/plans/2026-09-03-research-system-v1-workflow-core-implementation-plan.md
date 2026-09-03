# Research System v1 — Workflow Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the minimal reusable Workflow Core defined by Research System v1 so a new research case can be initialized and executed through stable WorkflowStep interfaces without reproducing Case 001's phase-specific prompt sequence.

**Architecture:** Build a small Python package with three responsibilities: typed workflow contracts, dependency-aware workflow composition, and a lightweight execution runner. Keep lifecycle labels (R0–R8) as metadata rather than hard-coded interfaces, keep prompts as execution details behind an executor boundary, and use synthetic test cases to prove case-independence. Do not implement the Canonical Registry, Evaluator, Renderer, Agent runtime, or infrastructure in this plan.

**Tech Stack:** Python 3.11+, standard-library `dataclasses` / `enum` / `typing`, `pytest` for tests. No external workflow framework, database, queue, vector store, MCP server, or agent runtime.

**Spec:** `docs/superpowers/specs/2026-09-03-research-system-contract-design.md`; methodology baseline: `docs/methodology/research-system-v1.md`; repository guidance: `CLAUDE.md`.

## Global Constraints

- **Workflow is the execution contract; Prompt is only an execution detail.**
- The reusable execution unit is `WorkflowStep`, not a lifecycle phase.
- Lifecycle labels `R0`–`R8` are conceptual research stages, not reusable implementation interfaces.
- **Artifacts carry research work; canonical objects carry semantic authority.**
- The Workflow Core MUST NOT depend on Case 001 phase names, filenames, or prompt text.
- Required human gates are declarative requirements in WorkflowStep; full `HumanGate` governance records belong to later evaluation/governance implementation.
- Workflow execution MUST expose stable inputs, outputs, constraints, validation and provenance requirements independently of the executor technology.
- Prompts MAY be used by an executor, but prompts are not part of the public workflow interface.
- A step MUST NOT silently mutate historical research state, silently change scope, or erase uncertainty/contradictions.
- No database, vector database, graph database, MCP server, multi-agent runtime, distributed worker, event bus, autonomous browser infrastructure, or universal connector framework is introduced by this plan.
- Do not migrate or rebuild `cases/001-ai-coding-agent-landscape/`; use synthetic fixtures for Workflow Core tests.
- No changes to `docs/methodology/research-system-v1.md` are required by this plan.
- Every implementation task ends with an independently runnable test command and a focused commit.

---

## 1. Implementation Boundary and File Structure

This plan creates only the smallest code surface required by Roadmap Step 2.

### Files to create

- `pyproject.toml` — minimal package/test configuration and Python version requirement.
- `src/ai_native_workbench/__init__.py` — package marker; no business logic.
- `src/ai_native_workbench/research/__init__.py` — research package exports.
- `src/ai_native_workbench/research/workflow/__init__.py` — public Workflow Core exports.
- `src/ai_native_workbench/research/workflow/contract.py` — immutable WorkflowStep contract types and contract validation.
- `src/ai_native_workbench/research/workflow/composition.py` — workflow graph, dependency validation, deterministic topological execution order.
- `src/ai_native_workbench/research/workflow/execution.py` — executor protocol, execution context/results, lightweight runner and gate blocking behavior.
- `tests/conftest.py` — shared synthetic research fixtures only.
- `tests/unit/research/workflow/test_contract.py` — WorkflowStep contract validation tests.
- `tests/unit/research/workflow/test_composition.py` — graph/composition tests.
- `tests/unit/research/workflow/test_execution.py` — runner/executor/gate behavior tests.
- `tests/integration/research/workflow/test_new_case_execution.py` — case-independent end-to-end Workflow Core test using a synthetic research case.

No other source or top-level directories should be added by this plan.

---

## 2. Task 1: Bootstrap the Minimal Python Package and Test Harness

**Files:**
- Create: `pyproject.toml`
- Create: `src/ai_native_workbench/__init__.py`
- Create: `src/ai_native_workbench/research/__init__.py`
- Create: `src/ai_native_workbench/research/workflow/__init__.py`
- Create: `tests/conftest.py`
- Test: `tests/unit/research/workflow/test_contract.py`

**Interfaces:**
- Consumes: repository-level guidance from `CLAUDE.md` and the approved System Contract.
- Produces: an importable `ai_native_workbench.research.workflow` package and a working `pytest` command for later tasks.

- [ ] **Step 1: Write the failing package smoke test**

```python
def test_research_workflow_package_imports():
    import ai_native_workbench.research.workflow as workflow

    assert workflow is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/research/workflow/test_contract.py::test_research_workflow_package_imports -q`

Expected: FAIL because the package does not yet exist.

- [ ] **Step 3: Write minimal package configuration and package markers**

`pyproject.toml` must:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-native-workbench"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
test = ["pytest>=8,<9"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

Create the three package `__init__.py` files with no runtime behavior.

- [ ] **Step 4: Run the smoke test to verify it passes**

Run: `pytest tests/unit/research/workflow/test_contract.py::test_research_workflow_package_imports -q`

Expected: PASS.

- [ ] **Step 5: Run the complete test suite**

Run: `pytest -q`

Expected: PASS with 1 test passed.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/ai_native_workbench tests/conftest.py tests/unit/research/workflow/test_contract.py
git commit -m "feat: bootstrap research workflow package"
```

---

## 3. Task 2: Implement the WorkflowStep Contract

**Files:**
- Create: `src/ai_native_workbench/research/workflow/contract.py`
- Modify: `src/ai_native_workbench/research/workflow/__init__.py`
- Modify: `tests/unit/research/workflow/test_contract.py`

**Interfaces:**
- Consumes: package bootstrap from Task 1.
- Produces:
  - `WorkflowStep`
  - `StepInput`
  - `StepOutput`
  - `GateRequirement`
  - `ProvenanceRequirement`
  - `StepValidationError`
  - `validate_step_contract(step: WorkflowStep) -> None`

Use immutable dataclasses (`frozen=True`) for contract values. Do not include executor/model/prompt/tool/runtime fields in `WorkflowStep`.

- [ ] **Step 1: Write failing tests for required contract fields and invalid contracts**

```python
import pytest

from ai_native_workbench.research.workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    StepValidationError,
    WorkflowStep,
    validate_step_contract,
)


def make_valid_step() -> WorkflowStep:
    return WorkflowStep(
        id="discover.sources",
        name="Discover Sources",
        version="1.0.0",
        purpose="Build an initial source map.",
        inputs=(StepInput("research_question", "question"),),
        outputs=(StepOutput("source_map", "artifact"),),
        preconditions=("research scope is approved",),
        method=("identify relevant source classes",),
        constraints=("do not expand the approved scope",),
        human_gate=GateRequirement(required=False, gate_type=None),
        validation=("source_map contains at least one source",),
        provenance=ProvenanceRequirement(required=True, rules=("record source identity",)),
    )


def test_valid_step_contract_is_accepted():
    step = make_valid_step()
    validate_step_contract(step)


def test_step_requires_stable_id_name_and_io():
    step = make_valid_step().__class__(
        id="",
        name="Discover Sources",
        version="1.0.0",
        purpose="Build an initial source map.",
        inputs=(),
        outputs=(),
        preconditions=(),
        method=(),
        constraints=(),
        human_gate=GateRequirement(required=False, gate_type=None),
        validation=(),
        provenance=ProvenanceRequirement(required=False, rules=()),
    )

    with pytest.raises(StepValidationError):
        validate_step_contract(step)


def test_required_human_gate_needs_gate_type():
    step = make_valid_step().__class__(
        **{**make_valid_step().__dict__, "human_gate": GateRequirement(required=True, gate_type=None)}
    )

    with pytest.raises(StepValidationError):
        validate_step_contract(step)
```

The test should also assert that the public `WorkflowStep` object has no prompt/model/runtime field.

- [ ] **Step 2: Run the focused tests to verify they fail**

Run: `pytest tests/unit/research/workflow/test_contract.py -q`

Expected: FAIL because the contract classes are not implemented.

- [ ] **Step 3: Implement the minimal contract types**

Implement these exact shapes:

```python
@dataclass(frozen=True)
class StepInput:
    name: str
    kind: str

@dataclass(frozen=True)
class StepOutput:
    name: str
    kind: str

@dataclass(frozen=True)
class GateRequirement:
    required: bool
    gate_type: str | None

@dataclass(frozen=True)
class ProvenanceRequirement:
    required: bool
    rules: tuple[str, ...]

@dataclass(frozen=True)
class WorkflowStep:
    id: str
    name: str
    version: str
    purpose: str
    inputs: tuple[StepInput, ...]
    outputs: tuple[StepOutput, ...]
    preconditions: tuple[str, ...]
    method: tuple[str, ...]
    constraints: tuple[str, ...]
    human_gate: GateRequirement
    validation: tuple[str, ...]
    provenance: ProvenanceRequirement
```

`validate_step_contract` must reject:

- empty `id`, `name`, `version`, or `purpose`;
- duplicate input names;
- duplicate output names;
- missing inputs or outputs;
- required human gate without a declared gate type;
- empty method or constraints;
- a provenance requirement marked `required=True` without at least one rule.

Do not validate canonical-object semantics here; that belongs to later steps.

- [ ] **Step 4: Run the focused tests to verify they pass**

Run: `pytest tests/unit/research/workflow/test_contract.py -q`

Expected: PASS for all contract tests.

- [ ] **Step 5: Run the complete test suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/workflow/contract.py src/ai_native_workbench/research/workflow/__init__.py tests/unit/research/workflow/test_contract.py
git commit -m "feat: add workflow step contract"
```

---

## 4. Task 3: Implement Workflow Composition and Lifecycle Metadata

**Files:**
- Create: `src/ai_native_workbench/research/workflow/composition.py`
- Modify: `src/ai_native_workbench/research/workflow/__init__.py`
- Modify: `tests/unit/research/workflow/test_composition.py`

**Interfaces:**
- Consumes: `WorkflowStep` and `validate_step_contract` from Task 2.
- Produces:
  - `LifecycleStage`
  - `WorkflowDefinition`
  - `WorkflowValidationError`
  - `validate_workflow(workflow: WorkflowDefinition) -> None`
  - `execution_order(workflow: WorkflowDefinition) -> tuple[str, ...]`

`LifecycleStage` must represent metadata such as `R0_DEFINE` through `R8_ARCHIVE_UPDATE`, but those labels MUST NOT change step identity or become required workflow nodes.

- [ ] **Step 1: Write failing tests for dependency validation and lifecycle independence**

```python
import pytest

from ai_native_workbench.research.workflow.composition import (
    LifecycleStage,
    WorkflowDefinition,
    WorkflowValidationError,
    execution_order,
    validate_workflow,
)


def test_workflow_can_use_multiple_steps_with_explicit_dependencies():
    workflow = WorkflowDefinition(
        id="research-basic-v1",
        version="1.0.0",
        steps=(step("define"), step("collect", depends_on=("define",)), step("synthesize", depends_on=("collect",))),
        lifecycle_stage_map={
            "define": LifecycleStage.R0_DEFINE,
            "collect": LifecycleStage.R2_EVIDENCE,
            "synthesize": LifecycleStage.R5_SYNTHESIZE,
        },
    )

    validate_workflow(workflow)
    assert execution_order(workflow) == ("define", "collect", "synthesize")


def test_missing_dependency_is_invalid():
    workflow = WorkflowDefinition(
        id="invalid",
        version="1.0.0",
        steps=(step("collect", depends_on=("missing",)),),
        lifecycle_stage_map={},
    )

    with pytest.raises(WorkflowValidationError):
        validate_workflow(workflow)


def test_cycle_is_invalid():
    workflow = WorkflowDefinition(
        id="invalid-cycle",
        version="1.0.0",
        steps=(step("a", depends_on=("b",)), step("b", depends_on=("a",))),
        lifecycle_stage_map={},
    )

    with pytest.raises(WorkflowValidationError):
        validate_workflow(workflow)


def test_lifecycle_stage_is_metadata_not_interface():
    workflow = WorkflowDefinition(
        id="non-phase-workflow",
        version="1.0.0",
        steps=(step("research"),),
        lifecycle_stage_map={"research": LifecycleStage.R1_DISCOVER},
    )

    validate_workflow(workflow)
    assert execution_order(workflow) == ("research",)
```

- [ ] **Step 2: Run the focused tests to verify they fail**

Run: `pytest tests/unit/research/workflow/test_composition.py -q`

Expected: FAIL because composition types are not implemented.

- [ ] **Step 3: Implement the minimal composition model**

Use:

```python
class LifecycleStage(str, Enum):
    R0_DEFINE = "R0_DEFINE"
    R1_DISCOVER = "R1_DISCOVER"
    R2_EVIDENCE = "R2_EVIDENCE"
    R3_ANALYZE = "R3_ANALYZE"
    R4_DECIDE = "R4_DECIDE"
    R5_SYNTHESIZE = "R5_SYNTHESIZE"
    R6_EVALUATE = "R6_EVALUATE"
    R7_DELIVER = "R7_DELIVER"
    R8_ARCHIVE_UPDATE = "R8_ARCHIVE_UPDATE"

@dataclass(frozen=True)
class WorkflowNode:
    step: WorkflowStep
    depends_on: tuple[str, ...] = ()

@dataclass(frozen=True)
class WorkflowDefinition:
    id: str
    version: str
    steps: tuple[WorkflowNode, ...]
    lifecycle_stage_map: Mapping[str, LifecycleStage]
```

`validate_workflow` must check:

- workflow id/version are non-empty;
- step ids are unique;
- every dependency resolves;
- every step contract validates;
- the dependency graph is acyclic;
- `lifecycle_stage_map` may omit steps and may map multiple steps to one stage;
- no code path requires one node for every R0–R8 value.

`execution_order` must return a deterministic topological order. For nodes that become simultaneously eligible, sort by step id. This makes workflow execution reproducible at the graph level without asserting deterministic model output.

- [ ] **Step 4: Run focused tests to verify they pass**

Run: `pytest tests/unit/research/workflow/test_composition.py -q`

Expected: PASS.

- [ ] **Step 5: Run the complete test suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/workflow/composition.py src/ai_native_workbench/research/workflow/__init__.py tests/unit/research/workflow/test_composition.py
git commit -m "feat: add workflow composition"
```

---

## 5. Task 4: Implement the Lightweight Execution Boundary

**Files:**
- Create: `src/ai_native_workbench/research/workflow/execution.py`
- Modify: `src/ai_native_workbench/research/workflow/__init__.py`
- Modify: `tests/unit/research/workflow/test_execution.py`

**Interfaces:**
- Consumes: `WorkflowDefinition`, `WorkflowStep`, and contract validation from Tasks 2–3.
- Produces:
  - `WorkflowExecutionContext`
  - `StepExecutionResult`
  - `WorkflowRunResult`
  - `StepExecutor` protocol
  - `WorkflowRunner`
  - `WorkflowExecutionError`

The executor boundary is deliberately technology-neutral. A concrete executor may later call a prompt, Python function, CLI, browser/search tool or agent, but those details are not part of the workflow contract.

- [ ] **Step 1: Write failing tests for execution, dependency propagation, and required human gates**

```python
import pytest

from ai_native_workbench.research.workflow.execution import (
    StepExecutor,
    WorkflowExecutionContext,
    WorkflowExecutionError,
    WorkflowRunner,
)


class EchoExecutor:
    def __init__(self):
        self.calls = []

    def execute(self, step, context):
        self.calls.append(step.id)
        return {name: f"output:{name}" for name in (item.name for item in step.outputs)}


def test_runner_executes_steps_in_dependency_order(workflow):
    executor = EchoExecutor()
    runner = WorkflowRunner(workflow=workflow, executor=executor)

    result = runner.run(WorkflowExecutionContext(case_id="case-synthetic", inputs={"question": "q"}))

    assert result.status == "succeeded"
    assert executor.calls == ["define", "collect", "synthesize"]


def test_runner_blocks_on_required_human_gate(workflow_with_required_gate):
    executor = EchoExecutor()
    runner = WorkflowRunner(workflow=workflow_with_required_gate, executor=executor)

    result = runner.run(WorkflowExecutionContext(case_id="case-synthetic", inputs={"question": "q"}))

    assert result.status == "blocked"
    assert result.blocked_step_id == "select"
    assert executor.calls == ["define"]


def test_runner_can_continue_after_explicit_gate_approval(workflow_with_required_gate):
    executor = EchoExecutor()
    runner = WorkflowRunner(workflow=workflow_with_required_gate, executor=executor)

    context = WorkflowExecutionContext(
        case_id="case-synthetic",
        inputs={"question": "q"},
        approved_gates={"select"},
    )
    result = runner.run(context)

    assert result.status == "succeeded"
    assert executor.calls == ["define", "select"]
```

Also test that an executor exception produces a failed run result with the step id and error preserved.

- [ ] **Step 2: Run focused tests to verify they fail**

Run: `pytest tests/unit/research/workflow/test_execution.py -q`

Expected: FAIL because the execution boundary is not implemented.

- [ ] **Step 3: Implement the minimal execution boundary**

Use:

```python
class StepExecutor(Protocol):
    def execute(self, step: WorkflowStep, context: WorkflowExecutionContext) -> Mapping[str, object]: ...

@dataclass(frozen=True)
class WorkflowExecutionContext:
    case_id: str
    inputs: Mapping[str, object]
    step_outputs: Mapping[str, Mapping[str, object]] = field(default_factory=dict)
    approved_gates: frozenset[str] = frozenset()

@dataclass(frozen=True)
class StepExecutionResult:
    step_id: str
    status: str
    outputs: Mapping[str, object]
    error: str | None = None

@dataclass(frozen=True)
class WorkflowRunResult:
    status: str
    steps: tuple[StepExecutionResult, ...]
    blocked_step_id: str | None = None
```

`WorkflowRunner.run` must:

1. validate the workflow before execution;
2. process steps in `execution_order(workflow)`;
3. before a step runs, check `step.human_gate.required` and `step.id not in context.approved_gates`; if so, return `blocked` without executing that step or its downstream nodes;
4. pass prior step outputs through the context; do not invent input values;
5. capture executor failures as `failed` results with a stable step id;
6. return `succeeded` only when every step executed successfully.

The runner MUST NOT create or mutate `HumanGate` records, canonical objects, claims, evidence, snapshots, scores or deliveries. Those belong to later system stages.

- [ ] **Step 4: Run focused tests to verify they pass**

Run: `pytest tests/unit/research/workflow/test_execution.py -q`

Expected: PASS.

- [ ] **Step 5: Run the complete test suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/workflow/execution.py src/ai_native_workbench/research/workflow/__init__.py tests/unit/research/workflow/test_execution.py
git commit -m "feat: add workflow execution boundary"
```

---

## 6. Task 5: Prove Case-Independent New-Case Initialization and Execution

**Files:**
- Modify: `tests/conftest.py`
- Create: `tests/integration/research/workflow/test_new_case_execution.py`

**Interfaces:**
- Consumes: public exports from `ai_native_workbench.research.workflow` produced by Tasks 2–4.
- Produces: a synthetic, Case-001-independent proof that a new research case can be initialized and executed through stable workflow interfaces.

- [ ] **Step 1: Write the integration test using a topic unrelated to Case 001**

Use a synthetic case such as “Should a small team adopt a new project-management tool?” with three generic steps:

```text
frame_question
collect_evidence
synthesize_answer
```

The fixture must not import or mention:

```text
Case 001
Phase 0 ... Phase 8
AI Coding Agent
```

The test should construct the workflow entirely from `WorkflowStep` objects and explicit dependencies, then run it through `WorkflowRunner`.

Assertions must prove:

```text
1. the case has a stable case_id;
2. no Case 001-specific path or prompt is needed;
3. the same WorkflowDefinition interface is used for all three steps;
4. the runner executes in dependency order;
5. the run ends in succeeded state.
```

- [ ] **Step 2: Run the integration test**

Run: `pytest tests/integration/research/workflow/test_new_case_execution.py -q`

Expected: FAIL until fixtures and the end-to-end workflow are wired together.

- [ ] **Step 3: Add only the synthetic fixtures required to make the test pass**

Do not introduce a case template, CLI, registry, YAML loader, or Case 001 adapter. A helper factory for tests is acceptable, but it must remain under `tests/`.

- [ ] **Step 4: Run the integration test to verify it passes**

Run: `pytest tests/integration/research/workflow/test_new_case_execution.py -q`

Expected: PASS.

- [ ] **Step 5: Run the complete test suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tests/conftest.py tests/integration/research/workflow/test_new_case_execution.py
git commit -m "test: prove case-independent workflow execution"
```

---

## 7. Task 6: Final Workflow Core Verification and Documentation Check

**Files:**
- Modify only if required by test/documentation findings: `src/ai_native_workbench/research/workflow/*`, `tests/*`
- Do not modify: `docs/methodology/research-system-v1.md`
- Do not modify: `docs/superpowers/specs/2026-09-03-research-system-contract-design.md`

**Interfaces:**
- Consumes: all Workflow Core implementation and tests from Tasks 1–5.
- Produces: a verified Step 2 implementation satisfying the roadmap exit condition.

- [ ] **Step 1: Run the full verification matrix**

Run:

```bash
pytest -q
python -m compileall -q src
```

Expected: both commands exit with status 0.

- [ ] **Step 2: Verify the required Step 2 behaviors by test inspection**

Confirm tests explicitly cover:

```text
WorkflowStep stable contract
input/output validation
workflow dependency validation
cycle rejection
deterministic graph ordering
R0-R8 lifecycle metadata without phase coupling
prompt-independent public API
required human-gate blocking
executor error propagation
new-case initialization/execution without Case 001
```

- [ ] **Step 3: Search the implementation for prohibited coupling**

Run:

```bash
grep -R "Phase [0-8]\|cases/001-ai-coding-agent-landscape\|AI Coding Agent" src tests || true
```

Expected: no matches under `src/` or the new Workflow Core integration tests. Any match must be removed unless it is part of a test comment explicitly asserting absence; prefer no matches.

- [ ] **Step 4: Search for premature infrastructure dependencies**

Run:

```bash
grep -R "mcp\|redis\|postgres\|sqlalchemy\|langgraph\|langchain\|agent" src/ai_native_workbench/research/workflow || true
```

Expected: no dependency-specific matches. The Workflow Core remains framework-neutral.

- [ ] **Step 5: Check the final diff against the approved Contract and Roadmap**

Review the diff and verify:

```text
- WorkflowStep is the reusable unit.
- lifecycle stages are metadata, not interfaces.
- prompts remain behind the executor boundary.
- no canonical/evaluation/delivery system is implemented early.
- no Case 001 migration/rebuild occurs.
```

- [ ] **Step 6: Commit any verification-driven corrections**

If corrections were required:

```bash
git add src tests
 git commit -m "fix: align workflow core with system contract"
```

If no corrections were required, do not create an empty commit.

---

## 8. Plan Exit Criteria

The plan is complete only when all of the following are demonstrated by tests and code inspection:

1. A reusable `WorkflowStep` contract exists with stable inputs, outputs, purpose, method, constraints, human-gate and provenance declarations.
2. Workflow composition uses explicit dependencies and deterministic topological ordering.
3. R0–R8 are represented only as lifecycle metadata; no workflow interface requires Phase 0–8 files or names.
4. Prompts/models/tools are behind an executor boundary rather than the WorkflowStep interface.
5. Required human gates can block execution until explicitly approved.
6. Executor failure is surfaced without silently continuing past the failed step.
7. A new synthetic research case can be initialized and executed without any Case 001-specific artifact or prompt sequence.
8. The implementation introduces no Canonical Registry, Evaluator, Renderer, Agent runtime, or infrastructure beyond the minimal Python/test harness.
9. Full verification passes: `pytest -q` and `python -m compileall -q src`.

## 9. Explicitly Deferred to Subsequent Plans

This Workflow Core plan intentionally does **not** implement:

```text
Step 3 — Canonical Knowledge + Provenance
    Canonical Registry
    Entity / Claim / Evidence / Source persistence
    Research Snapshot semantics beyond the workflow execution boundary

Step 4 — Evaluation
    reusable evaluator
    mechanical invariant evaluator
    human evaluation protocol/records

Step 5 — Reproducible Build + Delivery
    Build object persistence
    Dataset / Note / HTML / PPT / Audit rendering

Step 6 — End-to-End Validation Case
    real Case 001 or other production research case through the new system

Step 7 — Generalization Case
    second meaningfully different research case

Step 8 — System Revision
    evidence-driven v1.1 changes

Step 9 — Automation / Skills / Agentization
    Skills, stronger automation, or Agents
```

Those roadmap stages remain separate so that the Workflow Core can be evaluated before the system grows around it.
