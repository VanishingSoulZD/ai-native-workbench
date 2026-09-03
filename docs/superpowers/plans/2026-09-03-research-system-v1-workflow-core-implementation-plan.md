# Research System v1 — Workflow Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the minimal reusable Workflow Core defined by Research System v1 so a new research case can be initialized and executed through stable WorkflowStep interfaces without reproducing Case 001's phase-specific prompt sequence.

**Architecture:** Build a small Python package with three responsibilities: immutable workflow contracts, dependency-aware workflow composition, and a lightweight executor boundary/runner. R0–R8 remain lifecycle metadata only. Prompts, models and tools remain behind the executor boundary. Synthetic research cases prove reuse without importing any Case 001 artifact.

**Tech Stack:** Python 3.11+, standard-library `dataclasses`, `enum`, `typing` and `heapq`; `pytest>=8,<9` for tests. No external workflow framework, database, queue, vector store, MCP server or agent runtime.

**Spec:** `docs/superpowers/specs/2026-09-03-research-system-contract-design.md`

**Methodology:** `docs/methodology/research-system-v1.md` (Roadmap Step 2 — Workflow Core)

**Repository guidance:** `CLAUDE.md`

## Global Constraints

- **Workflow is the execution contract; Prompt is only an execution detail.**
- The reusable execution unit is `WorkflowStep`, not a lifecycle phase.
- Lifecycle labels `R0`–`R8` are conceptual research stages, not reusable implementation interfaces.
- **Artifacts carry research work; canonical objects carry semantic authority.**
- The public WorkflowStep interface must not contain prompt, model, tool, agent or runtime fields.
- The Workflow Core MUST NOT depend on Case 001 phase names, filenames, prompts or domain entities.
- Human gates are declarative requirements in WorkflowStep during this plan; persistent `HumanGate` governance records belong to later governance/evaluation work.
- The runner may block on an unapproved required gate but must not fabricate an approval or create a governance record.
- The runner must not create or mutate canonical claims, evidence, sources, judgments, decisions, scores or snapshots.
- No database, vector database, graph database, MCP server, multi-agent runtime, distributed worker, event bus, autonomous browser infrastructure or universal connector framework is introduced.
- Do not migrate, adapt or rebuild `cases/001-ai-coding-agent-landscape/`.
- No changes to `docs/methodology/research-system-v1.md` or the approved System Contract are part of this plan.
- Every implementation task has a failing-test step, a focused verification command and a focused commit.

---

## 1. Implementation Boundary and File Structure

The first implementation slice is Roadmap **Step 2 — Workflow Core** only. Step 3–9 remain separate plans.

### Files to create

- `pyproject.toml` — package metadata and pytest configuration.
- `src/ai_native_workbench/__init__.py` — package marker.
- `src/ai_native_workbench/research/__init__.py` — research package marker.
- `src/ai_native_workbench/research/workflow/__init__.py` — public Workflow Core exports.
- `src/ai_native_workbench/research/workflow/contract.py` — immutable step contract types and validation.
- `src/ai_native_workbench/research/workflow/composition.py` — lifecycle metadata, graph nodes and deterministic topological ordering.
- `src/ai_native_workbench/research/workflow/execution.py` — executor protocol, execution context/results and lightweight runner.
- `tests/conftest.py` — reusable synthetic step/workflow factories for tests; no Case 001 data.
- `tests/unit/research/workflow/test_contract.py` — contract validation.
- `tests/unit/research/workflow/test_composition.py` — dependency graph and lifecycle metadata.
- `tests/unit/research/workflow/test_execution.py` — runner behavior, gate blocking and failure propagation.
- `tests/integration/research/workflow/test_new_case_execution.py` — case-independent new-case execution.

### Files explicitly not created by this plan

```text
canonical registry
canonical object persistence
reusable evaluator
human evaluation records
build system
renderers
Dataset / Note / HTML / PPT generators
skills
agents
Case 001 adapters
```

---

## 2. Task 1: Bootstrap the Minimal Python/Test Harness

**Files:**
- Create: `pyproject.toml`
- Create: `src/ai_native_workbench/__init__.py`
- Create: `src/ai_native_workbench/research/__init__.py`
- Create: `src/ai_native_workbench/research/workflow/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/unit/research/workflow/test_contract.py`

**Interfaces:**
- Consumes: repository guidance and the approved System Contract.
- Produces: importable package plus shared test factories used by later tasks.

- [ ] **Step 1: Write the failing import test**

```python
def test_workflow_package_imports():
    import ai_native_workbench.research.workflow as workflow
    assert workflow is not None
```

- [ ] **Step 2: Run the failing test**

Run: `pytest tests/unit/research/workflow/test_contract.py::test_workflow_package_imports -q`

Expected: FAIL because the package does not exist.

- [ ] **Step 3: Add the minimal package configuration and package markers**

Use this `pyproject.toml`:

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

The three package markers contain no runtime logic.

Add the following exact fixture helpers to `tests/conftest.py` after Task 2's contract types exist; during Task 1 they may initially be omitted and added as part of Task 2's fixture setup:

```python
import pytest

from ai_native_workbench.research.workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    WorkflowStep,
)
from ai_native_workbench.research.workflow.composition import (
    LifecycleStage,
    WorkflowDefinition,
    WorkflowNode,
)


def make_step(step_id: str, *, gate_required: bool = False, gate_type: str | None = None,
              depends_on: tuple[str, ...] = ()) -> WorkflowNode:
    step = WorkflowStep(
        id=step_id,
        name=step_id.replace("_", " ").title(),
        version="1.0.0",
        purpose=f"Execute {step_id}.",
        inputs=(StepInput("input", "value"),),
        outputs=(StepOutput("output", "value"),),
        preconditions=("preconditions are satisfied",),
        method=("perform the declared step method",),
        constraints=("do not change undeclared scope",),
        human_gate=GateRequirement(required=gate_required, gate_type=gate_type),
        validation=("declared output exists",),
        provenance=ProvenanceRequirement(required=False, rules=()),
    )
    return WorkflowNode(step=step, depends_on=depends_on)


@pytest.fixture
def workflow():
    return WorkflowDefinition(
        id="research-basic-v1",
        version="1.0.0",
        steps=(
            make_step("define"),
            make_step("collect", depends_on=("define",)),
            make_step("synthesize", depends_on=("collect",)),
        ),
        lifecycle_stage_map={
            "define": LifecycleStage.R0_DEFINE,
            "collect": LifecycleStage.R2_EVIDENCE,
            "synthesize": LifecycleStage.R5_SYNTHESIZE,
        },
    )


@pytest.fixture
def workflow_with_required_gate():
    return WorkflowDefinition(
        id="research-gated-v1",
        version="1.0.0",
        steps=(
            make_step("define"),
            make_step("select", gate_required=True, gate_type="H2_POPULATION_SELECTION",
                       depends_on=("define",)),
        ),
        lifecycle_stage_map={
            "define": LifecycleStage.R0_DEFINE,
            "select": LifecycleStage.R4_DECIDE,
        },
    )
```

The helper is the single source for synthetic WorkflowNode creation in tests. No fixture may load Case 001 content.

- [ ] **Step 4: Run the import test**

Run: `pytest tests/unit/research/workflow/test_contract.py::test_workflow_package_imports -q`

Expected: PASS.

- [ ] **Step 5: Run the complete suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/ai_native_workbench tests/unit/research/workflow/test_contract.py
git commit -m "feat: bootstrap research workflow package"
```

---

## 3. Task 2: Implement the WorkflowStep Contract

**Files:**
- Create: `src/ai_native_workbench/research/workflow/contract.py`
- Modify: `src/ai_native_workbench/research/workflow/__init__.py`
- Modify: `tests/unit/research/workflow/test_contract.py`
- Modify: `tests/conftest.py`

**Interfaces:**
- Consumes: package scaffold from Task 1.
- Produces: `StepInput`, `StepOutput`, `GateRequirement`, `ProvenanceRequirement`, `WorkflowStep`, `StepValidationError`, `validate_step_contract(step: WorkflowStep) -> None`.

- [ ] **Step 1: Write failing contract tests**

Test these cases:

```python
def test_valid_step_contract_is_accepted(): ...
def test_empty_identity_is_rejected(): ...
def test_empty_inputs_or_outputs_are_rejected(): ...
def test_duplicate_input_names_are_rejected(): ...
def test_duplicate_output_names_are_rejected(): ...
def test_required_gate_without_type_is_rejected(): ...
def test_required_provenance_without_rules_is_rejected(): ...
def test_workflow_step_exposes_no_prompt_model_or_runtime_field(): ...
```

The test fixture must instantiate a valid `WorkflowStep` using only the contract fields.

- [ ] **Step 2: Run the focused tests to verify failure**

Run: `pytest tests/unit/research/workflow/test_contract.py -q`

Expected: FAIL because the contract types do not exist.

- [ ] **Step 3: Implement the immutable contract types**

Implement:

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

`validate_step_contract` must raise `StepValidationError` for:

```text
empty id/name/version/purpose
missing inputs or outputs
duplicate input names
duplicate output names
empty method
empty constraints
required human gate without gate_type
required provenance without at least one rule
```

Do not validate Claim/Evidence/Source semantics here; those belong to Step 3/4.

- [ ] **Step 4: Run focused tests to verify pass**

Run: `pytest tests/unit/research/workflow/test_contract.py -q`

Expected: PASS.

- [ ] **Step 5: Run the complete suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/workflow/contract.py src/ai_native_workbench/research/workflow/__init__.py tests/unit/research/workflow/test_contract.py tests/conftest.py
git commit -m "feat: add workflow step contract"
```

---

## 4. Task 3: Implement Workflow Composition and R0–R8 Lifecycle Metadata

**Files:**
- Create: `src/ai_native_workbench/research/workflow/composition.py`
- Modify: `src/ai_native_workbench/research/workflow/__init__.py`
- Modify: `tests/unit/research/workflow/test_composition.py`
- Modify: `tests/conftest.py`

**Interfaces:**
- Consumes: `WorkflowStep` and `validate_step_contract` from Task 2.
- Produces:
  - `LifecycleStage`
  - `WorkflowNode`
  - `WorkflowDefinition`
  - `WorkflowValidationError`
  - `validate_workflow(workflow: WorkflowDefinition) -> None`
  - `execution_order(workflow: WorkflowDefinition) -> tuple[str, ...]`

- [ ] **Step 1: Write failing graph tests**

Cover:

```python
def test_explicit_dependencies_are_resolved(): ...
def test_missing_dependency_is_rejected(): ...
def test_duplicate_step_id_is_rejected(): ...
def test_cycle_is_rejected(): ...
def test_step_contracts_are_revalidated_inside_workflow_validation(): ...
def test_topological_order_is_deterministic(): ...
def test_lifecycle_stage_is_optional_metadata(): ...
def test_multiple_steps_may_share_one_lifecycle_stage(): ...
def test_workflow_does_not_require_all_r0_to_r8_nodes(): ...
```

- [ ] **Step 2: Run focused tests to verify failure**

Run: `pytest tests/unit/research/workflow/test_composition.py -q`

Expected: FAIL because composition types do not exist.

- [ ] **Step 3: Implement the composition model**

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

Validation rules:

```text
workflow id/version must be non-empty
step ids must be unique
every dependency must resolve
every step contract must validate
lifecycle_stage_map keys must reference existing step ids
lifecycle_stage_map may omit steps
multiple steps may share a lifecycle stage
all R0–R8 values do not have to appear
graph must be acyclic
```

`execution_order` must return a deterministic topological order. When several nodes are ready, choose lexicographically smallest step id. Use `heapq` or an equivalent deterministic priority structure rather than relying on input tuple order.

- [ ] **Step 4: Run focused tests to verify pass**

Run: `pytest tests/unit/research/workflow/test_composition.py -q`

Expected: PASS.

- [ ] **Step 5: Run the complete suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/workflow/composition.py src/ai_native_workbench/research/workflow/__init__.py tests/unit/research/workflow/test_composition.py tests/conftest.py
git commit -m "feat: add workflow composition"
```

---

## 5. Task 4: Implement the Lightweight Executor Boundary and Runner

**Files:**
- Create: `src/ai_native_workbench/research/workflow/execution.py`
- Modify: `src/ai_native_workbench/research/workflow/__init__.py`
- Modify: `tests/unit/research/workflow/test_execution.py`

**Interfaces:**
- Consumes: `WorkflowDefinition`, `WorkflowNode`, `WorkflowStep` and `execution_order` from Tasks 2–3.
- Produces:
  - `StepExecutor` protocol
  - `WorkflowExecutionContext`
  - `StepExecutionResult`
  - `WorkflowRunResult`
  - `WorkflowExecutionError`
  - `WorkflowRunner`

- [ ] **Step 1: Write failing execution tests**

Use a fake executor:

```python
class EchoExecutor:
    def __init__(self):
        self.calls: list[str] = []

    def execute(self, step, context):
        self.calls.append(step.id)
        return {output.name: f"{step.id}:{output.name}" for output in step.outputs}
```

Cover:

```python
def test_runner_executes_in_dependency_order(workflow): ...
def test_runner_passes_prior_outputs_in_context(workflow): ...
def test_required_gate_blocks_before_step_execution(workflow_with_required_gate): ...
def test_approved_gate_allows_execution(workflow_with_required_gate): ...
def test_executor_failure_returns_failed_result_and_stops_downstream(workflow): ...
def test_success_requires_every_step_to_succeed(workflow): ...
```

- [ ] **Step 2: Run focused tests to verify failure**

Run: `pytest tests/unit/research/workflow/test_execution.py -q`

Expected: FAIL because execution types do not exist.

- [ ] **Step 3: Implement the executor boundary**

Use these exact public shapes:

```python
class StepExecutor(Protocol):
    def execute(
        self,
        step: WorkflowStep,
        context: "WorkflowExecutionContext",
    ) -> Mapping[str, object]: ...

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

`WorkflowRunner.run(context: WorkflowExecutionContext) -> WorkflowRunResult` must:

1. validate the WorkflowDefinition before execution;
2. calculate `execution_order(workflow)`;
3. execute nodes in that order;
4. for each node, check `human_gate.required`; when required and the node id is not in `approved_gates`, return `blocked` and do not execute that node or any downstream node;
5. build the next context by preserving original `inputs` and adding the executed step's outputs under `step_outputs[node.step.id]`;
6. never fabricate values for undeclared inputs;
7. on executor exception, record `failed` for that step, preserve a human-readable error string, and stop execution;
8. return `succeeded` only after every step has succeeded.

The public WorkflowStep interface must not expose the executor implementation, prompt, model, tool or agent.

The runner does not create `HumanGate` objects and does not mutate canonical state.

- [ ] **Step 4: Run focused tests to verify pass**

Run: `pytest tests/unit/research/workflow/test_execution.py -q`

Expected: PASS.

- [ ] **Step 5: Run the complete suite**

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
- Create: `tests/integration/research/workflow/test_new_case_execution.py`
- Modify: `tests/conftest.py`

**Interfaces:**
- Consumes: public Workflow Core exports from Tasks 2–4.
- Produces: an executable synthetic research case proving the Roadmap Step 2 exit condition.

- [ ] **Step 1: Write the failing integration test**

Construct a synthetic case with the research topic:

```text
Should a small team adopt a new project-management tool?
```

Use exactly three steps:

```text
frame_question
collect_evidence
synthesize_answer
```

The test constructs all steps through `WorkflowStep`/`WorkflowNode` and `WorkflowDefinition`. It must not import or reference:

```text
cases/001-ai-coding-agent-landscape/
Phase 0 ... Phase 8
AI Coding Agent
```

The test must assert:

```text
case_id is supplied through WorkflowExecutionContext
same WorkflowDefinition interface is used for all steps
execution order follows dependencies
execution succeeds
no Case 001 artifact or prompt is required
```

- [ ] **Step 2: Run the integration test to verify failure**

Run: `pytest tests/integration/research/workflow/test_new_case_execution.py -q`

Expected: FAIL until the synthetic case and runner are wired together.

- [ ] **Step 3: Add only the synthetic fixture/helper required to pass**

Do not add a case template, CLI, YAML loader, registry, persistence layer or Case 001 adapter.

- [ ] **Step 4: Run the integration test to verify pass**

Run: `pytest tests/integration/research/workflow/test_new_case_execution.py -q`

Expected: PASS.

- [ ] **Step 5: Run the complete suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tests/conftest.py tests/integration/research/workflow/test_new_case_execution.py
git commit -m "test: prove case-independent workflow execution"
```

---

## 7. Task 6: Final Verification and Scope Audit

**Files:**
- Modify source/tests only if a verification failure requires a correction.
- Do not modify: `docs/methodology/research-system-v1.md`
- Do not modify: `docs/superpowers/specs/2026-09-03-research-system-contract-design.md`

**Interfaces:**
- Consumes: all Workflow Core code/tests from Tasks 1–5.
- Produces: verified Step 2 implementation ready for separate review.

- [ ] **Step 1: Run the full verification matrix**

Run:

```bash
pytest -q
python -m compileall -q src
```

Expected: both commands exit with status 0.

- [ ] **Step 2: Verify Step 2 roadmap coverage**

Confirm test/code coverage exists for:

```text
stable WorkflowStep interface
input/output contract validation
dependency validation
cycle rejection
deterministic topological ordering
optional R0–R8 lifecycle metadata
prompt-independent public API
required human-gate blocking
gate approval continuation
executor failure propagation
dependency-output context propagation
new-case initialization/execution without Case 001
```

- [ ] **Step 3: Audit forbidden legacy coupling**

Run:

```bash
grep -R "cases/001-ai-coding-agent-landscape\|Phase [0-8]\|AI Coding Agent" src tests || true
```

Expected: no matches in `src/` and no matches in the integration test. Any accidental match must be removed.

- [ ] **Step 4: Audit premature infrastructure dependencies**

Run:

```bash
grep -R "mcp\|redis\|postgres\|sqlalchemy\|langchain\|langgraph\|agent" src/ai_native_workbench/research/workflow || true
```

Expected: no matches introduced by Workflow Core implementation.

- [ ] **Step 5: Audit public exports**

Run a Python smoke check that the package exposes only the intended Workflow Core API:

```python
from ai_native_workbench.research.workflow import (
    GateRequirement,
    LifecycleStage,
    ProvenanceRequirement,
    StepExecutor,
    StepInput,
    StepOutput,
    WorkflowDefinition,
    WorkflowNode,
    WorkflowRunner,
    WorkflowStep,
    execution_order,
    validate_step_contract,
    validate_workflow,
)
```

Expected: all imports succeed.

- [ ] **Step 6: Inspect the final diff against the Contract**

Verify:

```text
WorkflowStep is the reusable unit.
Lifecycle phases are metadata only.
Prompt/model/tool/agent are behind the executor boundary.
No canonical registry or evaluator was implemented early.
No renderer/delivery code was implemented early.
No Case 001 migration/rebuild was introduced.
No infrastructure dependency was added.
```

- [ ] **Step 7: Commit verification-driven corrections only**

If corrections were needed:

```bash
git add src tests
 git commit -m "fix: align workflow core with system contract"
```

Do not create an empty verification commit.

---

## 8. Step 2 Exit Criteria

The Workflow Core implementation is ready for review only when all are demonstrably true:

1. A `WorkflowStep` has a stable contract containing `id`, `name`, `version`, `purpose`, `inputs`, `outputs`, `method`, `constraints`, `human_gate`, `validation` and `provenance`.
2. Workflow composition uses explicit dependencies and deterministic topological ordering.
3. R0–R8 are optional lifecycle metadata, not required workflow nodes.
4. Prompts/models/tools/agents are not part of the public WorkflowStep interface.
5. Required gates can block execution until explicitly approved.
6. Executor failure is visible and prevents silent downstream continuation.
7. Prior step outputs are propagated through a stable execution context.
8. A synthetic, meaningfully non-Case-001 research case executes successfully through the same workflow interfaces.
9. No Canonical Registry, Evaluator, Renderer, Agent runtime or infrastructure was introduced.
10. `pytest -q` and `python -m compileall -q src` both pass.

This establishes the roadmap exit condition: a new research case can be initialized and executed through stable workflow interfaces rather than manually recreating the Case 001 prompt sequence.

## 9. Explicitly Deferred to Later Plans

```text
Step 3 — Canonical Knowledge + Provenance
Step 4 — Evaluation
Step 5 — Reproducible Build + Delivery
Step 6 — End-to-End Validation Case
Step 7 — Generalization Case
Step 8 — System Revision
Step 9 — Automation / Skills / Agentization
```

The Workflow Core should be evaluated before any of these are expanded.
