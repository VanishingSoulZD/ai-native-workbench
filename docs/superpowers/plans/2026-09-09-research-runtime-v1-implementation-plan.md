# Research Runtime v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved Research Runtime v1 architecture so an approved Research Case can execute a durable, auditable synthetic research path from declared sources through R5 Canonicalization and an immutable ResearchSnapshot, with explicit recovery/control semantics.

**Architecture:** Add a research-specific Runtime above the existing Workflow, Canonical, Evaluation, and Build cores. Runtime owns Run/Invocation/Attempt/Gate/Checkpoint/Artifact lineage, filesystem persistence, orchestration, reconciliation, and control actions; existing cores retain workflow structure, semantic knowledge, evaluation, and delivery authority. Step 6 stops its synthetic completion boundary at ResearchSnapshot.

**Tech Stack:** Python 3.11+, standard-library-first implementation, `pytest>=8,<9`, filesystem JSON/JSONL, local HTTP server for source integration tests, deterministic fake Executors for regression tests, and an isolated DeepSeek adapter boundary for optional live-model smoke coverage.

**Spec:** `docs/superpowers/specs/2026-09-09-research-runtime-v1-design.md`

## Global Constraints

- Runtime begins only from an approved Research Case; R0/H1 research framing remains outside the system.
- Run creation freezes relevant Case Definition identities/digests; Invocation creation freezes requested scope and execution configuration identities.
- Run identity remains stable across bounded continuation; a new execution request creates a new Invocation.
- `retry` stays within the same Attempt; `rerun` creates a new Attempt in the current Invocation; `resume` and `--from` create new Invocations.
- `--from Rn` reuses only an exact-compatible checkpoint at the specified boundary and rebuilds downstream lineage; old downstream checkpoints and Snapshots are not reused.
- `--until Rn` produces `COMPLETED + completion_reason=BOUNDED_SCOPE + execution_scope` when the requested scope succeeds.
- Run states remain exactly `CREATED`, `RUNNING`, `WAITING_FOR_HUMAN`, `NEEDS_REVISION`, `FAILED`, and `COMPLETED`.
- Attempt states remain exactly `PENDING`, `RUNNING`, `FAILED`, and `SUCCEEDED`; Candidate/Validation/Acceptance are separate evidence/disposition.
- Attempt Input Binding is durable before Attempt `RUNNING`; no implicit “latest artifact” resolution is permitted.
- Artifact lineage is explicit (`run_id`, `invocation_id`, `step_id`, `attempt_id`) and committed Artifacts are immutable.
- Artifact durable evidence must precede success events and state projection.
- `execution.jsonl` is authoritative history; `run.json` is a rebuildable projection.
- Every Event has `event_id` and `schema_version`; Step 6 uses `schema_version=1`, no second `idempotency_key`, and unknown versions fail fast.
- Every independent Runtime persistence document has `runtime_schema_version=1`; unknown versions fail fast and no migration command is added.
- Crash recovery is at-least-once plus durable reconciliation; it never silently reruns business work.
- Gate records bind to concrete review target Artifact/Candidate Sets; whole-set decision is `APPROVE` or `REJECT`.
- Gate supersession is an immutable relationship, not an additional Gate state; old Gates remain historical.
- `NEEDS_REVISION` is produced only by explicit human rejection/requested revision; no automatic correction loop exists.
- `revision_target.entry_step` is the minimum re-execution boundary and is human-specified; Runtime validates but does not infer research impact from prose.
- Source Acquisition fetches only declared URLs from `inputs/urls.yaml`; required-source failure blocks research execution and optional-source failure is durable and non-blocking.
- Synthetic integration uses a local HTTP server and deterministic fake Executors; the main regression suite has no external network or live LLM dependency.
- Real LLM support is DeepSeek-only, behind a thin adapter, without automatic provider fallback.
- Workflow Core owns DAG structure/dependency semantics; Runtime v1 schedules single-process sequential execution and must not hardcode R-step behavior by `step_id`.
- H2/H3/H4 are Runtime Gate Barriers, not ordinary Workflow Steps.
- R5 Canonical registration and ResearchSnapshot creation use public Canonical Core APIs only; Runtime must not inspect Canonical Registry internals.
- Evaluation/Build/Archive are not part of the Step 6 synthetic completion boundary; integrate only where required to establish public contracts without pulling Step 7 into the implementation.
- No database, queue, distributed workers, browser agent, MCP retrieval, multi-agent orchestration, autonomous source discovery, generalized revision engine, or generalized event-store platform.
- Every task follows TDD: failing test, verify failure, minimal implementation, focused tests, relevant integration tests, regression suite, then commit.
- The repository regression baseline to preserve is `pytest --collect-only -q` → 191 tests and `pytest -q` → 191 passed, allowing only reviewed test-count changes caused by new Runtime tests.

## Repository Map Before Implementation

The current repository already has a domain-agnostic Workflow Core with immutable `WorkflowStep`, dependency-aware `WorkflowDefinition`, and deterministic topological ordering; it also exposes Canonical Registry and immutable `ResearchSnapshot` public APIs, plus Evaluation and Build cores that operate on explicit research state. fileciteturn19file0 fileciteturn20file0 fileciteturn21file0 fileciteturn26file0 fileciteturn32file0 fileciteturn33file0

The older `docs/superpowers/plans/2026-09-08-research-runtime-v1-implementation-plan.md` is retained as historical inventory only. This plan supersedes its ordering because the approved Step 6 Spec deliberately stops the executable synthetic path at ResearchSnapshot rather than requiring full R6–R8 delivery in this stage. fileciteturn55file0

---

### Task 1: Establish the Runtime Domain Model and Public Package Boundary

**Files:**
- Create: `src/ai_native_workbench/research/runtime/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/domain/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/domain/run.py`
- Create: `src/ai_native_workbench/research/runtime/domain/invocation.py`
- Create: `src/ai_native_workbench/research/runtime/domain/attempt.py`
- Create: `src/ai_native_workbench/research/runtime/domain/artifact.py`
- Create: `src/ai_native_workbench/research/runtime/domain/gate.py`
- Create: `src/ai_native_workbench/research/runtime/domain/checkpoint.py`
- Create: `src/ai_native_workbench/research/runtime/domain/events.py`
- Test: `tests/unit/research/runtime/domain/test_run.py`
- Test: `tests/unit/research/runtime/domain/test_invocation.py`
- Test: `tests/unit/research/runtime/domain/test_attempt.py`
- Test: `tests/unit/research/runtime/domain/test_artifact.py`
- Test: `tests/unit/research/runtime/domain/test_gate.py`
- Test: `tests/unit/research/runtime/domain/test_checkpoint.py`
- Test: `tests/unit/research/runtime/domain/test_events.py`

**Interfaces:**
- Consumes: approved Step 6 Spec and existing immutable Workflow/Canonical domain style.
- Produces: immutable Runtime records and validation methods used by Store, Orchestrator, Gate Runtime, and reconciliation.

**Key APIs:**

```python
class RunState(str, Enum): ...
class AttemptStatus(str, Enum): ...
class InvocationStatus(str, Enum): ...
class GateDecision(str, Enum): ...

@dataclass(frozen=True)
class RunRecord: ...
def create_run(case_binding: CaseBinding, *, run_id: str, created_at: str) -> RunRecord: ...

def create_invocation(
    run_id: str,
    requested_scope: ExecutionScope,
    *,
    entry_mode: EntryMode,
    execution_binding: ExecutionBinding,
    invocation_id: str,
    created_at: str,
) -> InvocationRecord: ...

def create_attempt(run_id: str, invocation_id: str, step_id: str, *, attempt_id: str) -> AttemptRecord: ...

def bind_attempt_inputs(attempt: AttemptRecord, binding: InputBinding) -> AttemptRecord: ...
```

- [ ] **Step 1: Write failing tests for the six Run states and bounded completion metadata.**

```python
def test_bounded_completion_is_not_full_lifecycle_completion():
    run = RunRecord.created(...)
    completed = run.complete(
        completion_reason="BOUNDED_SCOPE",
        execution_scope=("R1", "R2", "R3", "R4", "R5", "SNAPSHOT"),
    )
    assert completed.state is RunState.COMPLETED
    assert completed.completion_reason == "BOUNDED_SCOPE"
```

Also assert invalid transitions such as direct `CREATED -> COMPLETED` and that `NEEDS_REVISION` is not an ordinary execution error.

- [ ] **Step 2: Run the focused Run tests and verify failure.**

```bash
pytest tests/unit/research/runtime/domain/test_run.py -v
```

Expected: FAIL because the Runtime domain package does not yet exist.

- [ ] **Step 3: Implement immutable Run/Invocation domain records.**

`RunRecord` must hold case binding, cumulative scope, current state, current Invocation reference, and completion metadata. `InvocationRecord` must freeze requested scope, entry mode, from/until boundaries, workflow/config identities, status, and completion disposition. `COMPLETED -> RUNNING` and `NEEDS_REVISION -> RUNNING` must be exposed only through explicit resume constructors/methods.

- [ ] **Step 4: Write and run failing Attempt/Artifact/Input Binding tests.**

```python
def test_input_binding_is_required_before_running():
    attempt = create_attempt("run-1", "inv-1", "R3", attempt_id="att-1")
    with pytest.raises(RuntimeError):
        attempt.mark_running()


def test_attempt_keeps_execution_status_separate_from_acceptance():
    attempt = bound_attempt(...).mark_running().mark_succeeded()
    assert attempt.status is AttemptStatus.SUCCEEDED
    assert attempt.acceptance_status is None
```

- [ ] **Step 5: Implement Attempt, InputBinding, ArtifactEnvelope, and OutputPort records.**

ArtifactEnvelope must include independent artifact identity, lineage, digest, schema identity/version, provenance metadata, and committed/uncommitted disposition. `mark_running()` must refuse to transition until an immutable InputBinding exists.

- [ ] **Step 6: Write and run failing Gate/Checkpoint/Event tests.**

```python
def test_gate_supersession_is_relation_not_state():
    approved = GateRecord(..., decision=GateDecision.APPROVED)
    replacement = GateRecord(..., decision=GateDecision.PENDING, supersedes=approved.gate_id)
    assert approved.decision is GateDecision.APPROVED
    assert replacement.supersedes == approved.gate_id
```

For events, assert `event_id`, `schema_version=1`, and rejection of an unknown schema version.

- [ ] **Step 7: Implement GateRecord, CheckpointRecord, EventEnvelope and exports.**

Keep `GateDecision` limited to `PENDING/APPROVED/REJECTED`; keep Event facts separate from commands.

- [ ] **Step 8: Run all Task 1 tests.**

```bash
pytest tests/unit/research/runtime/domain -v
```

Expected: PASS.

- [ ] **Step 9: Commit.**

```bash
git add src/ai_native_workbench/research/runtime tests/unit/research/runtime/domain
git commit -m "feat: add research runtime domain contracts"
```

---

### Task 2: Build Filesystem Persistence, Event Log, and Rebuildable Run Projection

**Files:**
- Create: `src/ai_native_workbench/research/runtime/store/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/store/filesystem.py`
- Create: `src/ai_native_workbench/research/runtime/store/event_log.py`
- Create: `src/ai_native_workbench/research/runtime/store/projection.py`
- Create: `src/ai_native_workbench/research/runtime/store/artifacts.py`
- Create: `src/ai_native_workbench/research/runtime/reconciliation.py`
- Test: `tests/unit/research/runtime/store/test_filesystem.py`
- Test: `tests/unit/research/runtime/store/test_event_log.py`
- Test: `tests/unit/research/runtime/store/test_projection.py`
- Test: `tests/unit/research/runtime/test_reconciliation.py`

**Interfaces:**
- Consumes: Task 1 domain records.
- Produces: filesystem store and event reducer used by every later Runtime service.

**Key APIs:**

```python
class RuntimeStore:
    def create_run(self, run: RunRecord) -> None: ...
    def load_run_projection(self, run_id: str) -> RunRecord: ...
    def append_event(self, event: EventEnvelope) -> None: ...
    def list_events(self, run_id: str) -> tuple[EventEnvelope, ...]: ...
    def save_artifact(self, artifact: ArtifactEnvelope) -> None: ...
    def load_artifact(self, artifact_id: str) -> ArtifactEnvelope: ...
    def save_gate(self, gate: GateRecord) -> None: ...
    def save_checkpoint(self, checkpoint: CheckpointRecord) -> None: ...

class EventReducer:
    def reduce(self, events: tuple[EventEnvelope, ...], evidence: EvidenceIndex) -> RunRecord: ...
```

- [ ] **Step 1: Write failing tests for the prescribed layout and root schema version.**

Assert creation of:

```text
cases/<case-id>/runs/<run-id>/
  run.json
  execution.jsonl
  steps/
  gates/
  artifacts/
  manifests/
```

and `run.json` root `runtime_schema_version == 1`.

- [ ] **Step 2: Run focused persistence tests and verify failure.**

```bash
pytest tests/unit/research/runtime/store -v
```

Expected: FAIL because the Store does not exist.

- [ ] **Step 3: Implement atomic-ish JSON document persistence.**

Write JSON through a temporary file in the same directory and replace the destination, so an interrupted projection update does not leave a partially written `run.json`. Store must never rewrite `execution.jsonl`.

- [ ] **Step 4: Write failing Event Log tests for append-only history and Event idempotency.**

```python
def test_same_event_id_is_not_appended_twice(store):
    store.append_event(event)
    store.append_event(event)
    assert len(store.list_events("run-1")) == 1
```

Also reject a second Event with an existing `event_id` but different payload.

- [ ] **Step 5: Implement `EventLog` with `event_id` index and schema-version validation.**

Use one JSON object per line. Event facts must be append-only and include `event_id`, `event_type`, `schema_version`, timestamps, lineage refs, and payload.

- [ ] **Step 6: Write failing projection/reducer tests.**

Cover rebuilding Run state, Invocation history, latest logical Step Attempt, Gate decisions, completion scope, and Snapshot binding entirely from history/evidence.

- [ ] **Step 7: Implement EventReducer and projection refresh.**

`run.json` is only a current-state projection. The reducer must not depend on mutable in-memory state from a prior process.

- [ ] **Step 8: Write failing crash-reconciliation tests.**

Cover these exact windows:

```text
Attempt RUNNING with no committed Artifact
Artifact committed but success event missing
success event present but run.json stale
unknown event schema version
```

Expected: stranded RUNNING Attempt becomes `FAILED/EXECUTION_INTERRUPTED`; complete durable success evidence allows deterministic event repair; unknown schema fails fast.

- [ ] **Step 9: Implement startup reconciliation and evidence verification.**

Reconcile durable evidence before business re-execution. Never automatically invoke an Executor as part of reconciliation.

- [ ] **Step 10: Run focused tests.**

```bash
pytest tests/unit/research/runtime/store -v
pytest tests/unit/research/runtime/test_reconciliation.py -v
```

Expected: PASS.

- [ ] **Step 11: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/store src/ai_native_workbench/research/runtime/reconciliation.py tests/unit/research/runtime/store tests/unit/research/runtime/test_reconciliation.py
git commit -m "feat: add durable runtime event store and reconciliation"
```

---

### Task 3: Implement Case Binding, Execution Binding, Checkpoints, and Artifact Commit Protocol

**Files:**
- Create: `src/ai_native_workbench/research/runtime/binding.py`
- Create: `src/ai_native_workbench/research/runtime/artifacts.py`
- Create: `src/ai_native_workbench/research/runtime/checkpoints.py`
- Modify: `src/ai_native_workbench/research/runtime/store/artifacts.py`
- Test: `tests/unit/research/runtime/test_binding.py`
- Test: `tests/unit/research/runtime/test_artifacts.py`
- Test: `tests/unit/research/runtime/test_checkpoints.py`

**Interfaces:**
- Consumes: Task 1 models and Task 2 persistence.
- Produces: immutable Case/Invocation bindings, artifact commit API, exact checkpoint compatibility.

**Key APIs:**

```python
def freeze_case_binding(case: ResearchCase) -> CaseBinding: ...
def freeze_execution_binding(config: ExecutionConfiguration) -> ExecutionBinding: ...
def assert_execution_compatible(existing: ExecutionBinding, proposed: ExecutionBinding) -> None: ...

def persist_input_binding(attempt_id: str, binding: InputBinding, store: RuntimeStore) -> None: ...
def commit_artifact(envelope: ArtifactEnvelope, payload: object, store: RuntimeStore) -> ArtifactEnvelope: ...

def validate_checkpoint(checkpoint: CheckpointRecord, expected: CompatibilityIdentity, store: RuntimeStore) -> None: ...
def invalidate_downstream(run_id: str, upstream_step_id: str, store: RuntimeStore) -> tuple[str, ...]: ...
```

- [ ] **Step 1: Write failing binding-freeze tests.**

```python
def test_case_binding_does_not_change_when_case_files_change(tmp_path):
    binding = freeze_case_binding(case)
    case.charter.write_text("changed")
    assert binding.charter_digest == original_digest
```

Test that incompatible Workflow/Prompt/Schema/Runtime configuration cannot continue the same Run.

- [ ] **Step 2: Implement Case Binding and Invocation Execution Binding.**

Case Binding captures `case_id`, Charter identity/digest, source declaration identity/digest, and other approved execution inputs. Invocation Binding captures requested scope, entry mode, Workflow/Prompt/Schema/Runtime identities.

- [ ] **Step 3: Write failing Artifact Commit tests for ordering.**

```python
def test_uncommitted_output_is_not_bindable(store):
    residue = create_uncommitted_artifact(...)
    with pytest.raises(ArtifactNotCommittedError):
        store.resolve_for_input(residue.artifact_id)
```

Also assert committed artifact digest correctness and immutable re-save behavior.

- [ ] **Step 4: Implement Artifact Commit Protocol.**

Perform:

```text
payload
→ envelope
→ digest/metadata
→ committed evidence
→ ARTIFACT_COMMITTED event
```

Only after commit evidence exists may later code create Input Bindings against the artifact.

- [ ] **Step 5: Write failing checkpoint compatibility tests.**

Test exact equality for Workflow identity/version, Step identity/version, Prompt identity/version, Schema identity/version, and Runtime configuration identity. Test missing artifact and digest mismatch as invalid.

- [ ] **Step 6: Implement Checkpoint validation and downstream invalidation.**

A Checkpoint stores Artifact references and compatibility metadata only. When an upstream Step is rerun, dependent checkpoints are invalidated by default and remain historical records.

- [ ] **Step 7: Run focused tests.**

```bash
pytest tests/unit/research/runtime/test_binding.py tests/unit/research/runtime/test_artifacts.py tests/unit/research/runtime/test_checkpoints.py -v
```

Expected: PASS.

- [ ] **Step 8: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/binding.py src/ai_native_workbench/research/runtime/artifacts.py src/ai_native_workbench/research/runtime/checkpoints.py src/ai_native_workbench/research/runtime/store/artifacts.py tests/unit/research/runtime/test_binding.py tests/unit/research/runtime/test_artifacts.py tests/unit/research/runtime/test_checkpoints.py
git commit -m "feat: add runtime bindings artifacts and checkpoints"
```

---

### Task 4: Add Executor Registry and Candidate/Validation/Acceptance Pipeline

**Files:**
- Create: `src/ai_native_workbench/research/runtime/execution/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/execution/registry.py`
- Create: `src/ai_native_workbench/research/runtime/execution/executors.py`
- Create: `src/ai_native_workbench/research/runtime/execution/acceptance.py`
- Create: `src/ai_native_workbench/research/runtime/execution/llm.py`
- Test: `tests/unit/research/runtime/execution/test_registry.py`
- Test: `tests/unit/research/runtime/execution/test_acceptance.py`
- Test: `tests/unit/research/runtime/execution/test_llm.py`

**Interfaces:**
- Consumes: Workflow `WorkflowStep.execution` metadata, bound input Artifacts, Runtime Store.
- Produces: Executor strategy resolution, deterministic fake execution, and optional DeepSeek adapter output without lifecycle authority.

**Key APIs:**

```python
class Executor(Protocol):
    def execute(self, step: WorkflowStep, inputs: InputBinding) -> CandidateOutput: ...

class ExecutorRegistry:
    def register(self, mode: str, executor: Executor) -> None: ...
    def resolve(self, mode: str) -> Executor: ...

class AcceptancePipeline:
    def validate_schema(self, candidate: CandidateOutput) -> ValidationResult: ...
    def validate_provenance(self, candidate: CandidateOutput) -> ValidationResult: ...
    def validate_domain(self, candidate: CandidateOutput) -> ValidationResult: ...
    def accept(self, candidate: CandidateOutput, policy: AcceptancePolicy) -> AcceptanceResult: ...
```

- [ ] **Step 1: Write failing registry tests proving the Orchestrator need not switch on `step_id`.**

```python
def test_registry_resolves_executor_by_declared_mode():
    registry = ExecutorRegistry()
    executor = FakeExecutor()
    registry.register("deterministic", executor)
    assert registry.resolve("deterministic") is executor
```

Unknown execution mode must fail explicitly.

- [ ] **Step 2: Implement Registry and deterministic Executor.**

The deterministic fake must return structured candidate payloads and stable metadata suitable for all Runtime integration tests.

- [ ] **Step 3: Write failing acceptance tests.**

Cover schema failure, provenance failure, domain failure, automatic acceptance, human acceptance requirement, and canonical acceptance requirement. Rejected candidates must remain durable and must not mark the Step completed.

- [ ] **Step 4: Implement AcceptancePipeline.**

Keep validation mechanics outside the Orchestrator. Step completion depends on acceptance policy satisfaction, not merely Executor success.

- [ ] **Step 5: Write failing DeepSeek boundary tests.**

Use a mocked transport to verify request metadata, provider/model identity, prompt/schema digests, timeout/error mapping, and absence of API key handling. Never put a live key in tests.

```python
def test_deepseek_client_never_changes_runtime_state(fake_transport, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-only")
    result = DeepSeekClient(fake_transport).complete(...)
    assert result.provider == "deepseek"
```

- [ ] **Step 6: Implement `DeepSeekClient` as an isolated adapter.**

Keep provider details out of Workflow and Orchestrator. Real live execution is optional smoke coverage, not a regression dependency.

- [ ] **Step 7: Run focused tests.**

```bash
pytest tests/unit/research/runtime/execution -v
```

Expected: PASS.

- [ ] **Step 8: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/execution tests/unit/research/runtime/execution
git commit -m "feat: add runtime executor and acceptance boundaries"
```

---

### Task 5: Define the Versioned Standard Research Workflow Adapter

**Files:**
- Create: `src/ai_native_workbench/research/runtime/workflow.py`
- Create: `tests/unit/research/runtime/test_workflow.py`
- Test: `tests/unit/research/runtime/test_workflow_compatibility.py`
- Reference only: `src/ai_native_workbench/research/workflow/contract.py`
- Reference only: `src/ai_native_workbench/research/workflow/composition.py`

**Interfaces:**
- Consumes: existing `WorkflowStep`, `WorkflowNode`, `WorkflowDefinition`, validation, and topological ordering.
- Produces: a versioned `StandardResearchWorkflow` object plus helpers for Gate Barriers and bounded scope calculations without turning Workflow Core into Runtime.

**Key APIs:**

```python
@dataclass(frozen=True)
class StandardResearchWorkflow:
    definition: WorkflowDefinition
    gate_barriers: Mapping[str, GateBarrier]

STANDARD_RESEARCH_WORKFLOW_V1: StandardResearchWorkflow

def workflow_nodes_for_scope(workflow: StandardResearchWorkflow, scope: ExecutionScope) -> tuple[str, ...]: ...
def validate_entry_boundary(workflow: StandardResearchWorkflow, step_id: str) -> None: ...
```

- [ ] **Step 1: Write failing tests for workflow version identity and canonical lifecycle mapping.**

Assert the shared workflow exposes R1/R2/R3/R4/R5 and gate barriers H2/H3 in the Step 6 execution slice, plus later lifecycle definitions needed for future continuation, without making Gate Barriers standalone Workflow Steps.

- [ ] **Step 2: Run the focused workflow tests and verify failure.**

```bash
pytest tests/unit/research/runtime/test_workflow.py -v
```

Expected: FAIL before the Runtime workflow adapter exists.

- [ ] **Step 3: Implement the Standard Research Workflow adapter.**

Use existing Workflow Core graph validation and execution ordering. Do not modify `WorkflowRunner` to own Runtime state. Keep Case-specific research content out of the shared graph.

- [ ] **Step 4: Add compatibility tests against the existing Workflow suite.**

```bash
pytest tests/unit/research/workflow -v
pytest tests/unit/research/runtime/test_workflow_compatibility.py -v
```

Expected: all existing Workflow tests remain green and the Runtime adapter only consumes public contracts.

- [ ] **Step 5: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/workflow.py tests/unit/research/runtime/test_workflow.py tests/unit/research/runtime/test_workflow_compatibility.py
git commit -m "feat: define standard research workflow adapter"
```

---

### Task 6: Implement Source Acquisition as a Durable Runtime Capability

**Files:**
- Create: `src/ai_native_workbench/research/runtime/source/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/source/acquisition.py`
- Test: `tests/unit/research/runtime/source/test_acquisition.py`
- Test: `tests/integration/research/runtime/source/test_declared_urls.py`

**Interfaces:**
- Consumes: Task 2 Store and approved Case `inputs/urls.yaml`.
- Produces: immutable Source Artifacts and Source Acquisition Records.

**Key APIs:**

```python
class SourceAcquisitionService:
    def acquire(self, case_binding: CaseBinding, *, run_id: str) -> AcquisitionResult: ...
```

- [ ] **Step 1: Write failing unit tests for URL declaration validation.**

Cover malformed URL, duplicate source ID, unsupported scheme, and required/optional classification.

- [ ] **Step 2: Verify failure.**

```bash
pytest tests/unit/research/runtime/source/test_acquisition.py -v
```

Expected: FAIL before the acquisition service exists.

- [ ] **Step 3: Implement declaration validation and source binding.**

Only declared URLs are eligible. Source acquisition uses the Run's frozen declaration digest.

- [ ] **Step 4: Write failing integration tests using `http.server` or equivalent local test server.**

Cover 200 response, redirect, oversized/unsupported body, required failure, optional failure, retrieval timestamp, content digest, and reuse of a committed Source Artifact within the same Run.

- [ ] **Step 5: Implement HTTP retrieval and durable source artifacts.**

Use standard library HTTP primitives unless a current repository dependency proves necessary. Preserve raw content where supported and write an explicit acquisition record for every declaration.

- [ ] **Step 6: Run source tests.**

```bash
pytest tests/unit/research/runtime/source/test_acquisition.py tests/integration/research/runtime/source/test_declared_urls.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/source tests/unit/research/runtime/source tests/integration/research/runtime/source
git commit -m "feat: add declared source acquisition"
```

---

### Task 7: Implement Human Gate Runtime, Revision Targets, and Gate Supersession

**Files:**
- Create: `src/ai_native_workbench/research/runtime/gates/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/gates/runtime.py`
- Test: `tests/unit/research/runtime/gates/test_runtime.py`
- Test: `tests/unit/research/runtime/gates/test_supersession.py`
- Test: `tests/integration/research/runtime/test_revision_flow.py`

**Interfaces:**
- Consumes: Task 1 Gate models, Task 2 Event Store, Task 5 workflow boundaries, Task 3 artifact lineage.
- Produces: durable H2/H3 gate barriers, whole-set decision handling, revision targets, and generic supersession.

**Key APIs:**

```python
class GateRuntime:
    def create_gate(self, target: ReviewTarget, requirement: GateRequirement, *, gate_id: str) -> GateRecord: ...
    def decide(self, gate_id: str, decision: GateDecision, *, reviewer: str, comment: str, revision_target: RevisionTarget | None = None) -> GateRecord: ...
    def create_replacement_gate(self, prior_gate_id: str, target: ReviewTarget, *, gate_id: str) -> GateRecord: ...
```

- [ ] **Step 1: Write failing gate lifecycle tests.**

Assert:

```text
create → WAITING_FOR_HUMAN
APPROVE → progression allowed
REJECT → Run.NEEDS_REVISION
```

A Gate must bind the concrete Artifact/Candidate Set under review.

- [ ] **Step 2: Implement GateRuntime persistence and decisions.**

Use only `PENDING/APPROVED/REJECTED` decisions. Whole-set approval/rejection is mandatory in v1.

- [ ] **Step 3: Write failing supersession tests.**

```python
def test_new_review_target_supersedes_old_gate():
    old = approved_gate(target="artifact-set-a")
    new = runtime.create_replacement_gate(old.gate_id, target="artifact-set-b", gate_id="gate-2")
    assert new.supersedes == old.gate_id
    assert old.decision is GateDecision.APPROVED
```

Also assert the old approval cannot satisfy a new lineage.

- [ ] **Step 4: Implement generic supersession by logical gate identity + target lineage.**

Do not add `INVALIDATED` or `SUPERSEDED` to the Gate enum. Persist relationship facts instead.

- [ ] **Step 5: Write failing revision-target validation tests.**

Cover valid `entry_step`, invalid downstream entry, missing revision target on rejection, and a `NEEDS_REVISION -> resume` path that creates a new Invocation.

- [ ] **Step 6: Implement minimal `RevisionTarget(entry_step, reason)`.**

Runtime validates the entry boundary against Workflow dependencies but does not infer business impact from prose.

- [ ] **Step 7: Run focused and revision integration tests.**

```bash
pytest tests/unit/research/runtime/gates -v
pytest tests/integration/research/runtime/test_revision_flow.py -v
```

Expected: PASS.

- [ ] **Step 8: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/gates tests/unit/research/runtime/gates tests/integration/research/runtime/test_revision_flow.py
git commit -m "feat: add durable human gate runtime"
```

---

### Task 8: Implement the Research Orchestrator and Explicit Control Actions

**Files:**
- Create: `src/ai_native_workbench/research/runtime/orchestrator.py`
- Create: `src/ai_native_workbench/research/runtime/control.py`
- Create: `src/ai_native_workbench/research/runtime/recovery.py`
- Test: `tests/unit/research/runtime/test_orchestrator.py`
- Test: `tests/unit/research/runtime/test_control.py`
- Test: `tests/integration/research/runtime/test_recovery_controls.py`

**Interfaces:**
- Consumes: Tasks 1–7.
- Produces: the single Runtime coordination point and explicit `start/resume/retry/rerun/--from/--until` semantics.

**Key APIs:**

```python
class ResearchRuntime:
    def create_run(self, case_path: Path) -> RunRecord: ...
    def start(self, run_id: str, *, until: str | None = None) -> RunRecord: ...
    def resume(self, run_id: str, *, until: str | None = None) -> RunRecord: ...
    def retry(self, run_id: str, step_id: str) -> RunRecord: ...
    def rerun(self, run_id: str, step_id: str) -> RunRecord: ...
    def run_from(self, run_id: str, step_id: str, *, until: str | None = None) -> RunRecord: ...
    def decide_gate(self, run_id: str, gate_id: str, decision: GateDecision, **kwargs) -> RunRecord: ...
```

- [ ] **Step 1: Write failing orchestration tests for the Attempt start protocol.**

Assert the exact ordering:

```text
Attempt Created
→ Input Binding persisted
→ Attempt RUNNING
→ Executor invoked
```

The Executor must never see inputs before durable binding.

- [ ] **Step 2: Implement one-step orchestration through Executor Registry.**

The Orchestrator must resolve Workflow nodes and prerequisites through Workflow Core, not by switching on R1/R2/R3/R4/R5 IDs.

- [ ] **Step 3: Write failing tests for `retry`, `rerun`, `resume`, and `--from`.**

Cover:

```text
retry → same Invocation + same Attempt
rerun → same Invocation + new Attempt
resume → new Invocation + same Run
--from R3 → new Invocation + R3 new Attempt + rebuilt downstream lineage
```

- [ ] **Step 4: Implement explicit control actions.**

Do not schedule automatic retry/rerun. `FAILED -> RUNNING` only through explicit recovery. `COMPLETED` bounded scope may resume as the same Run. `NEEDS_REVISION` resumes only with a validated revision target.

- [ ] **Step 5: Write failing `--until` tests.**

Assert that a bounded Invocation succeeds when its requested scope is satisfied and that the Run records:

```python
assert run.state is RunState.COMPLETED
assert run.completion_reason == "BOUNDED_SCOPE"
```

- [ ] **Step 6: Implement scope tracking and Invocation completion.**

Invocation success means the requested scope has complete durable evidence; Run projection derives its state from Invocation outcome plus failure disposition/Gate facts.

- [ ] **Step 7: Write failing `--from` and rerun invalidation tests.**

Assert that old downstream Checkpoints/Gates remain historical but do not permit progression on the new lineage, and that a new Snapshot is required after a new R5 path.

- [ ] **Step 8: Implement downstream lineage rebuild and checkpoint invalidation hooks.**

Do not mutate prior Attempts, Artifacts, or Gates.

- [ ] **Step 9: Run focused orchestration/recovery tests.**

```bash
pytest tests/unit/research/runtime/test_orchestrator.py tests/unit/research/runtime/test_control.py -v
pytest tests/integration/research/runtime/test_recovery_controls.py -v
```

Expected: PASS.

- [ ] **Step 10: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/orchestrator.py src/ai_native_workbench/research/runtime/control.py src/ai_native_workbench/research/runtime/recovery.py tests/unit/research/runtime/test_orchestrator.py tests/unit/research/runtime/test_control.py tests/integration/research/runtime/test_recovery_controls.py
git commit -m "feat: add research runtime orchestration controls"
```

---

### Task 9: Implement the R5 Canonical Boundary and ResearchSnapshot Freeze

**Files:**
- Create: `src/ai_native_workbench/research/runtime/canonical.py`
- Create: `src/ai_native_workbench/research/runtime/snapshot.py`
- Test: `tests/unit/research/runtime/test_canonical_boundary.py`
- Test: `tests/unit/research/runtime/test_snapshot_binding.py`
- Test: `tests/integration/research/runtime/test_r5_snapshot_boundary.py`
- Modify: `src/ai_native_workbench/research/canonical/*` only if a genuinely missing public API is required

**Interfaces:**
- Consumes: accepted R5 Artifact, public `CanonicalRegistry.register()`, `CanonicalRegistry.snapshot()` and public resolution APIs.
- Produces: durable Canonical Binding and Snapshot Binding without accessing `_current` / `_states` internals.

**Key APIs:**

```python
class CanonicalBoundary:
    def register_accepted(self, artifact: ArtifactEnvelope, registry: CanonicalRegistry) -> CanonicalBinding: ...

class SnapshotBoundary:
    def freeze(self, binding: CanonicalBinding, *, snapshot_id: str) -> SnapshotBinding: ...
    def reconcile(self, binding: SnapshotBinding, registry: CanonicalRegistry) -> SnapshotBinding: ...
```

- [ ] **Step 1: Write failing two-phase Canonical binding tests.**

Verify:

```text
CANONICAL_BINDING_PENDING
→ public Registry registration
→ CANONICAL_BINDING_COMMITTED
```

A crash between pending and committed must be recoverable without duplicate semantic registration.

- [ ] **Step 2: Implement CanonicalBoundary using only public APIs.**

Do not inspect `_current`, `_states`, or other Registry internals. If reconciliation cannot be implemented with the current public API, add the smallest public API to Canonical Core rather than breaking encapsulation.

- [ ] **Step 3: Write failing Snapshot boundary tests.**

Assert Snapshot creation happens immediately after successful canonical registration, is not represented as a Workflow Step, and binds exact historical membership.

```python
def test_snapshot_is_knowledge_freeze_not_workflow_step(runtime):
    result = runtime.complete_r5(...)
    assert result.snapshot_binding.snapshot_id
    assert "SNAPSHOT" not in runtime.workflow.definition_step_ids()
```

- [ ] **Step 4: Implement SnapshotBoundary through public Canonical APIs.**

Use `CanonicalRegistry.snapshot()` and persist only Runtime binding/reference information. Preserve immutable Snapshot semantics already provided by Canonical Core. The existing Snapshot model resolves historical state by exact fingerprint rather than current Registry state. fileciteturn26file0

- [ ] **Step 5: Add Snapshot failure recovery tests.**

Simulate:

```text
Canonical registration succeeds
Snapshot creation/binding fails
```

Assert:

```text
R5 Attempt = SUCCEEDED
Invocation = FAILED
Run = FAILED
```

and a later reconciliation retries only Snapshot creation, not R5 execution or canonical registration.

- [ ] **Step 6: Run focused Snapshot tests.**

```bash
pytest tests/unit/research/runtime/test_canonical_boundary.py tests/unit/research/runtime/test_snapshot_binding.py -v
pytest tests/integration/research/runtime/test_r5_snapshot_boundary.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit.**

```bash
git add src/ai_native_workbench/research/runtime/canonical.py src/ai_native_workbench/research/runtime/snapshot.py tests/unit/research/runtime/test_canonical_boundary.py tests/unit/research/runtime/test_snapshot_binding.py tests/integration/research/runtime/test_r5_snapshot_boundary.py src/ai_native_workbench/research/canonical
git commit -m "feat: add r5 canonical and snapshot boundary"
```

---

### Task 10: Build the Semantically Real Synthetic Case and Step 6 End-to-End Validation

**Files:**
- Create: `cases/runtime-synthetic/00-research-charter.md`
- Create: `cases/runtime-synthetic/inputs/urls.yaml`
- Create: `tests/integration/research/runtime/test_synthetic_runtime.py`
- Create: `tests/integration/research/runtime/test_crash_windows.py`
- Create: `tests/integration/research/runtime/test_lineage_controls.py`
- Create: `tests/integration/research/runtime/test_runtime_cli.py`
- Create: `scripts/run_research.py`

**Interfaces:**
- Consumes: complete Runtime from Tasks 1–9.
- Produces: the architecture-level evidence required by Step 6 completion criteria.

**Synthetic semantic chain:**

```text
Local HTTP Source
    ↓
Source Artifact
    ↓
Evidence
    ↓
Claim / Relationship
    ↓
Analysis working Artifact
    ↓
Human judgment Artifact
    ↓
H2 / H3 Gates
    ↓
R5 Canonicalization
    ↓
Canonical Registry
    ↓
ResearchSnapshot
    ↓
COMPLETED / BOUNDED_SCOPE
```

- [ ] **Step 1: Write the failing happy-path E2E test before creating the fixture.**

```python
def test_synthetic_case_reaches_snapshot_and_bounded_completion(tmp_path):
    case = make_runtime_synthetic_case(tmp_path)
    run = ResearchRuntime(...).start(case)
    assert run.state is RunState.WAITING_FOR_HUMAN
```

The test should then approve H2/H3 through the Runtime API and assert the final Snapshot binding and bounded completion.

- [ ] **Step 2: Run the E2E test and verify failure.**

```bash
pytest tests/integration/research/runtime/test_synthetic_runtime.py -v
```

Expected: FAIL because the synthetic fixture and complete orchestration path are not yet wired.

- [ ] **Step 3: Create the semantically real synthetic Case and deterministic fixtures.**

Use a tiny source document whose facts can support one factual Claim and one Relationship, include one unresolved `Unknown`, and derive an Analysis artifact from those observations. Use only the existing first-slice Canonical vocabulary (`Entity`, `Claim`, `Evidence`, `Source`, `Unknown`, `Relationship`). The existing Canonical Core already exposes these types and their typed references. fileciteturn31file0 fileciteturn43file0

- [ ] **Step 4: Implement end-to-end happy path through R5.**

Verify all of:

```text
Case validation
Run binding
Invocation creation
Source acquisition
R1/R2/R3 execution
H2 decision
R4 execution
H3 decision
R5 candidate validation/acceptance
Canonical registration
Snapshot freeze/binding
Run completion
```

- [ ] **Step 5: Add failing lineage-control tests.**

Cover:

```text
rerun upstream → new Attempt + downstream invalidation
old approved Gate → cannot satisfy new target
--from R3 → new Invocation + new downstream Gate/Snapshot
completed bounded Run → resume → new Invocation
NEEDS_REVISION → explicit revision_target → new Invocation
```

- [ ] **Step 6: Implement and run lineage-control tests.**

```bash
pytest tests/integration/research/runtime/test_lineage_controls.py -v
```

Expected: PASS.

- [ ] **Step 7: Add failing crash-window integration tests.**

Exercise:

```text
before Artifact commit
Artifact committed before success event
success event before projection update
Canonical binding pending
Snapshot binding pending
stranded RUNNING Attempt
```

- [ ] **Step 8: Implement fault injection hooks only for tests and run the crash suite.**

```bash
pytest tests/integration/research/runtime/test_crash_windows.py -v
```

Expected: PASS with deterministic reconciliation and no silent business re-execution.

- [ ] **Step 9: Add the thin CLI control surface.**

`python scripts/run_research.py` must delegate directly to `ResearchRuntime` APIs. Support only the formal operations already in the Spec:

```text
create/start
resume
retry
rerun
--from
--until
gate decision
```

Do not introduce a CLI framework unless the existing repository later requires one.

- [ ] **Step 10: Write and run CLI delegation tests.**

```bash
pytest tests/integration/research/runtime/test_runtime_cli.py -v
```

Expected: PASS and no orchestration logic duplicated in the script.

- [ ] **Step 11: Run the complete Runtime integration suite.**

```bash
pytest tests/integration/research/runtime -v
```

Expected: PASS.

- [ ] **Step 12: Commit the synthetic validation slice.**

```bash
git add cases/runtime-synthetic scripts/run_research.py tests/integration/research/runtime
git commit -m "test: validate research runtime end to end"
```

---

### Task 11: Final Regression, Contract Verification, and Step 6 Exit Gate

**Files:**
- Modify: none unless a prior task exposed a real contract inconsistency
- Test: repository-wide existing tests plus Runtime suites

**Interfaces:**
- Consumes: complete Step 6 implementation.
- Produces: verified evidence that the Runtime satisfies the approved Spec without expanding into Step 7.

- [ ] **Step 1: Verify collection baseline.**

```bash
pytest --collect-only -q
```

Record the resulting test count and confirm that the prior Step 5 baseline of 191 tests is preserved as the existing suite portion; any increase must correspond to the intentionally added Runtime tests.

- [ ] **Step 2: Run the complete regression suite.**

```bash
pytest -q
```

Expected: all tests pass; the pre-existing baseline remains green.

- [ ] **Step 3: Run the focused core suite to guard subsystem boundaries.**

```bash
pytest tests/unit/research/workflow -q
pytest tests/unit/research/canonical -q
pytest tests/unit/research/evaluation -q
pytest tests/unit/research/build -q
pytest tests/integration/research/canonical -q
```

Expected: PASS.

- [ ] **Step 4: Perform a static architecture check.**

Search the Runtime package for forbidden coupling patterns:

```bash
grep -R "_current\|_states\|_logical_id_types" -n src/ai_native_workbench/research/runtime || true
grep -R "step_id == \"R[1-5]" -n src/ai_native_workbench/research/runtime || true
grep -R "DEEPSEEK_API_KEY" -n src tests | grep -v test || true
```

Expected: no Runtime access to Canonical private internals, no Step-ID hardcoded orchestration branches, and no committed secret values.

- [ ] **Step 5: Verify the Step 6 completion matrix.**

Check each Spec completion criterion: durable Run, immutable Invocation, formal Standard Workflow consumption, declared source acquisition, R1–R5 semantic path, Executor Registry, durable Input Binding, validation/acceptance, Canonical boundary, Snapshot freeze, bounded completion, authoritative Event Log, crash reconciliation, explicit controls, inspectable lineage, offline deterministic integration, and regression preservation.

- [ ] **Step 6: Verify Step 7 has not been pulled forward.**

Confirm the implementation does not make Case 001 replay, Case 002 generalization, full R6/R7/R8 delivery, concurrent DAG scheduling, or production autonomous research part of the Step 6 acceptance criterion.

- [ ] **Step 7: Commit only if the final verification introduces an intentional documentation/test correction.**

```bash
git status --short
git diff --check
```

If no changes remain, do not create a meaningless empty commit. If a reviewed correction is required, commit it with a specific message describing the correction.

---

## Final Implementation Handoff

When execution begins, use `superpowers:subagent-driven-development` or `superpowers:executing-plans` as required by the header. Each task is intentionally sized so a reviewer can accept/reject one vertical slice at a time. Do not collapse Tasks 1–11 into a single implementation pass.

The architectural end state is:

```text
Approved Case
    ↓
Run
    ↓
Invocation
    ↓
Workflow Step
    ↓
Attempt
    ↓
Input Binding
    ↓
Executor
    ↓
Artifact
    ↓
Validation / Acceptance
    ↓
Gate Barrier
    ↓
Canonical Binding
    ↓
ResearchSnapshot
    ↓
COMPLETED / BOUNDED_SCOPE
```

The control-plane audit chain is:

```text
Run
  ↓
Invocation
  ↓
Attempt
  ↓
Artifact / Gate / Checkpoint
  ↓
execution.jsonl
  ↓
run.json projection
```

The implementation must preserve the approved invariant:

> **The Runtime makes research execution durable and auditable; it does not become the research itself.**
