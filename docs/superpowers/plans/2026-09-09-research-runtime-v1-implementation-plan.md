# Research Runtime v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved Research Runtime v1 architecture so an approved Research Case executes durably from declared sources through R5 Canonicalization and an immutable ResearchSnapshot, with explicit recovery and Human-in-the-loop control.

**Architecture:** Add a research-specific Runtime above the existing Workflow, Canonical, Evaluation, and Build cores. The Runtime owns Run/Invocation/Attempt/Gate/Checkpoint/Artifact lineage, filesystem persistence, orchestration, reconciliation, and control actions; existing cores retain workflow structure, semantic authority, evaluation, and delivery authority. Step 6 ends at the ResearchSnapshot boundary.

**Tech Stack:** Python 3.11+, standard-library-first implementation, `pytest>=8,<9`, filesystem JSON/JSONL, local HTTP server for source tests, deterministic fake Executors for the main integration path, and an isolated DeepSeek adapter for optional live-model smoke coverage.

**Spec:** `docs/superpowers/specs/2026-09-09-research-runtime-v1-design.md`

## Global Constraints

- Runtime begins only from an approved Research Case; R0/H1 framing remains outside the Runtime.
- Run binds immutable Case Definition identities/digests; Invocation binds immutable requested scope and execution configuration identities.
- Run identity remains stable across bounded continuation; a new execution request creates a new Invocation.
- `retry` stays within the same Attempt and Invocation; `rerun` creates a new Attempt in the current Invocation; `resume` and `--from` create new Invocations.
- `--from Rn` reuses only an exact-compatible checkpoint at Rn's input boundary and rebuilds all dependent downstream lineage.
- `--until Rn` yields `COMPLETED + completion_reason=BOUNDED_SCOPE + execution_scope` when requested scope completes.
- Run states remain exactly `CREATED`, `RUNNING`, `WAITING_FOR_HUMAN`, `NEEDS_REVISION`, `FAILED`, `COMPLETED`.
- Attempt states remain exactly `PENDING`, `RUNNING`, `FAILED`, `SUCCEEDED`; Candidate/Validation/Acceptance are separate evidence/disposition.
- Attempt Input Binding is durable before Attempt `RUNNING`; no implicit “latest artifact” resolution.
- Artifacts are independently identified, explicitly lineage-bound, and immutable after commit.
- Durable Artifact evidence precedes success events and state projection.
- `execution.jsonl` is authoritative history; `run.json` is a rebuildable projection.
- Every Event has unique `event_id` and `schema_version=1`; no second `idempotency_key`; unknown versions fail fast.
- Every independent Runtime persistence document has `runtime_schema_version=1`; no migration tooling in Step 6.
- Crash handling provides at-least-once execution plus deterministic reconciliation; it never silently reruns business work.
- Human Gates bind to concrete Artifact/Candidate Sets and use whole-set `APPROVE` or `REJECT` decisions.
- Gate supersession is an immutable relation, not a new Gate state.
- `NEEDS_REVISION` comes only from explicit Human Gate rejection/requested revision; no automatic correction loop.
- `revision_target.entry_step` is the human-specified minimum re-execution boundary; Runtime validates it against Workflow dependencies.
- Source Acquisition fetches only declared URLs; required-source failures block research execution and optional-source failures are recorded but non-blocking.
- Main tests use no external internet and no live LLM dependency.
- Real LLM support is DeepSeek-only, without provider fallback; secrets come from the environment.
- Workflow Core remains domain-agnostic; Runtime v1 uses a single-process sequential scheduler and does not hardcode R-step behavior by `step_id`.
- H2/H3/H4 are Runtime Gate Barriers, not ordinary Workflow Steps.
- Runtime never accesses Canonical Registry private internals.
- R6/R7/R8, Case 001 replay, Case 002 generalization, concurrent scheduling, autonomous research, and production browser/MCP acquisition remain Step 7 scope.
- Every task follows TDD: failing test → verify failure → minimal implementation → focused tests → relevant integration tests → regression → commit.
- Existing repository regression baseline is `pytest --collect-only -q` → 191 tests and `pytest -q` → 191 passed before new Runtime tests are added.

## Existing Repository Contracts Used by the Plan

The repository already provides immutable `WorkflowStep`, `WorkflowDefinition`, dependency validation, and deterministic topological ordering. fileciteturn19file0 fileciteturn20file0

Canonical Core already exposes the first-slice object vocabulary `Entity`, `Claim`, `Evidence`, `Source`, `Unknown`, and `Relationship`, plus `CanonicalRegistry.register()`, `get_state()`, `snapshot()`, and immutable `ResearchSnapshot`. Runtime must use those public APIs. fileciteturn21file0 fileciteturn26file0 fileciteturn31file0 fileciteturn43file0

Evaluation Core evaluates explicit targets and Build Core consumes explicit Research Snapshots; neither should be replicated inside Runtime. fileciteturn32file0 fileciteturn33file0

The previous `docs/superpowers/plans/2026-09-08-research-runtime-v1-implementation-plan.md` remains historical inventory. This plan replaces its ordering and does not pull full R6–R8 delivery into Step 6. fileciteturn29file0

---

### Task 1: Runtime Domain Contracts and Public Package Boundary

**Files:**
- Create: `src/ai_native_workbench/research/runtime/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/domain/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/domain/models.py`
- Create: `src/ai_native_workbench/research/runtime/domain/events.py`
- Test: `tests/unit/research/runtime/domain/test_models.py`
- Test: `tests/unit/research/runtime/domain/test_events.py`

**Interfaces:**
- Consumes: approved Step 6 Spec.
- Produces: immutable `RunRecord`, `InvocationRecord`, `AttemptRecord`, `InputBinding`, `ArtifactEnvelope`, `GateRecord`, `CheckpointRecord`, `EventEnvelope`, and enums used by all later Runtime layers.

**Required model fields:**

```python
RunRecord(
    run_id: str,
    case_id: str,
    case_binding: CaseBinding,
    state: RunState,
    cumulative_execution_scope: tuple[str, ...],
    current_invocation_id: str | None,
    completion_reason: str | None,
    runtime_schema_version: int = 1,
)

InvocationRecord(
    invocation_id: str,
    run_id: str,
    requested_scope: ExecutionScope,
    entry_mode: EntryMode,
    from_step: str | None,
    until_step: str | None,
    execution_binding: ExecutionBinding,
    status: InvocationStatus,
    completion_reason: str | None,
    runtime_schema_version: int = 1,
)

AttemptRecord(
    attempt_id: str,
    run_id: str,
    invocation_id: str,
    step_id: str,
    status: AttemptStatus,
    input_binding_id: str | None,
    runtime_schema_version: int = 1,
)
```

- [ ] **Step 1: Write failing tests for Run, Invocation, and Attempt invariants.**

```python
def test_completed_bounded_run_records_scope():
    run = make_created_run()
    completed = run.complete(
        completion_reason="BOUNDED_SCOPE",
        execution_scope=("R1", "R2", "R3", "R4", "R5", "SNAPSHOT"),
    )
    assert completed.state is RunState.COMPLETED
    assert completed.completion_reason == "BOUNDED_SCOPE"
    assert completed.cumulative_execution_scope == (
        "R1", "R2", "R3", "R4", "R5", "SNAPSHOT"
    )
```

Assert direct `CREATED -> COMPLETED` is rejected; `COMPLETED -> RUNNING` is legal only through an explicit resume operation; Invocation scope/configuration are immutable.

- [ ] **Step 2: Run the failing domain tests.**

```bash
pytest tests/unit/research/runtime/domain/test_models.py -v
```

Expected: FAIL because Runtime domain models do not exist.

- [ ] **Step 3: Implement immutable domain records and transition guards.**

Keep Run, Invocation, Attempt semantics distinct. Attempt states remain `PENDING/RUNNING/FAILED/SUCCEEDED`; do not add validation or acceptance to the Attempt state enum.

- [ ] **Step 4: Write failing tests for Artifact Envelope and Input Binding.**

```python
def test_attempt_cannot_become_running_without_durable_input_binding():
    attempt = make_attempt()
    with pytest.raises(RuntimeContractError):
        attempt.mark_running()


def test_artifact_lineage_is_explicit():
    artifact = make_artifact()
    assert artifact.run_id == "run-1"
    assert artifact.invocation_id == "inv-1"
    assert artifact.attempt_id == "att-1"
```

- [ ] **Step 5: Implement Artifact/Input Binding records and lifecycle methods.**

Input Binding stores concrete Artifact IDs plus upstream Attempt lineage. It never stores the phrase “latest artifact” or an unresolved selector.

- [ ] **Step 6: Write failing tests for Gate, Checkpoint, and Event schemas.**

```python
def test_event_rejects_unknown_schema_version():
    event = make_event(schema_version=2)
    with pytest.raises(EventSchemaError):
        validate_event(event)
```

Also assert Gate decisions are only `PENDING/APPROVED/REJECTED` and Checkpoints contain compatibility identity rather than process state.

- [ ] **Step 7: Implement GateRecord, CheckpointRecord, and EventEnvelope.**

EventEnvelope fields are `event_id`, `event_type`, `schema_version`, `timestamp`, `run_id`, optional lineage IDs, and payload. Events describe facts, never command intent.

- [ ] **Step 8: Run the complete Task 1 tests and commit.**

```bash
pytest tests/unit/research/runtime/domain -v

git add src/ai_native_workbench/research/runtime tests/unit/research/runtime/domain
git commit -m "feat: add research runtime domain contracts"
```

---

### Task 2: Filesystem Store, Event Log, Projection, and Crash Reconciliation

**Files:**
- Create: `src/ai_native_workbench/research/runtime/store/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/store/filesystem.py`
- Create: `src/ai_native_workbench/research/runtime/store/events.py`
- Create: `src/ai_native_workbench/research/runtime/store/projection.py`
- Create: `src/ai_native_workbench/research/runtime/reconciliation.py`
- Test: `tests/unit/research/runtime/store/test_filesystem.py`
- Test: `tests/unit/research/runtime/store/test_events.py`
- Test: `tests/unit/research/runtime/store/test_projection.py`
- Test: `tests/unit/research/runtime/test_reconciliation.py`

**Interfaces:**
- Consumes: Task 1 domain contracts.
- Produces: one filesystem-backed source of runtime truth with durable event history and a rebuildable `run.json` projection.

**Key APIs:**

```python
class RuntimeStore(Protocol):
    def create_run(self, run: RunRecord) -> None: ...
    def load_run(self, run_id: str) -> RunRecord: ...
    def save_projection(self, run: RunRecord) -> None: ...
    def append_event(self, event: EventEnvelope) -> None: ...
    def events(self, run_id: str) -> tuple[EventEnvelope, ...]: ...
    def save_artifact(self, artifact: ArtifactEnvelope) -> None: ...
    def load_artifact(self, artifact_id: str) -> ArtifactEnvelope: ...
```

- [ ] **Step 1: Write failing tests for durable layout and `runtime_schema_version=1`.**

```python
def test_run_layout_is_created(tmp_path):
    store = FileSystemRuntimeStore(tmp_path)
    store.create_run(make_created_run())
    assert (tmp_path / "cases" / "case-1" / "runs" / "run-1" / "run.json").exists()
    assert (tmp_path / "cases" / "case-1" / "runs" / "run-1" / "execution.jsonl").exists()
```

- [ ] **Step 2: Verify failure.**

```bash
pytest tests/unit/research/runtime/store/test_filesystem.py -v
```

Expected: FAIL because the filesystem store does not exist.

- [ ] **Step 3: Implement atomic-ish JSON document writes and immutable event append.**

Use temp-file-then-replace for `run.json`. `execution.jsonl` is append-only and is never rewritten. Each independent JSON document declares `runtime_schema_version=1`.

- [ ] **Step 4: Write failing Event idempotency tests.**

```python
def test_duplicate_event_id_is_idempotent(store):
    store.append_event(event)
    store.append_event(event)
    assert store.events("run-1").count(event) == 1


def test_same_event_id_with_different_payload_is_rejected(store):
    store.append_event(event)
    with pytest.raises(EventConflictError):
        store.append_event(replace_event(event, payload={"changed": True}))
```

- [ ] **Step 5: Implement Event Log validation and EventReducer.**

Reducer must reconstruct current Run/Invocation/Attempt/Gate/checkpoint/Snapshot binding state from event facts plus durable evidence. It must reject unknown Event schema versions and duplicate/conflicting Event IDs.

- [ ] **Step 6: Write failing projection/reconciliation tests for all required crash windows.**

Test:

```text
Attempt RUNNING + no committed Artifact
Artifact committed + missing success event
success event + stale run.json
Canonical binding pending
Snapshot binding pending
```

- [ ] **Step 7: Implement startup reconciliation.**

Rules:

```text
no durable success evidence → FAILED / EXECUTION_INTERRUPTED
complete durable success evidence + missing event → append missing fact
stale run.json → rebuild projection
unknown schema → fail fast
```

Never call an Executor during reconciliation.

- [ ] **Step 8: Run Task 2 tests and commit.**

```bash
pytest tests/unit/research/runtime/store -v
pytest tests/unit/research/runtime/test_reconciliation.py -v

git add src/ai_native_workbench/research/runtime/store src/ai_native_workbench/research/runtime/reconciliation.py tests/unit/research/runtime/store tests/unit/research/runtime/test_reconciliation.py
git commit -m "feat: add durable runtime event store and reconciliation"
```

---

### Task 3: Case Binding, Checkpoints, Artifact Commit, and Exact Compatibility

**Files:**
- Create: `src/ai_native_workbench/research/runtime/binding.py`
- Create: `src/ai_native_workbench/research/runtime/artifacts.py`
- Create: `src/ai_native_workbench/research/runtime/checkpoints.py`
- Create: `tests/unit/research/runtime/test_binding.py`
- Create: `tests/unit/research/runtime/test_artifacts.py`
- Create: `tests/unit/research/runtime/test_checkpoints.py`

**Interfaces:**
- Consumes: Task 1 models and Task 2 Store.
- Produces: frozen Case/Execution bindings, committed Artifacts, explicit Input Bindings, exact Checkpoint compatibility.

**Key APIs:**

```python
def freeze_case_binding(case: ResearchCase) -> CaseBinding: ...
def freeze_execution_binding(config: ExecutionConfiguration) -> ExecutionBinding: ...
def assert_compatible(expected: CompatibilityIdentity, actual: CompatibilityIdentity) -> None: ...
def persist_input_binding(store: RuntimeStore, binding: InputBinding) -> None: ...
def commit_artifact(store: RuntimeStore, artifact: ArtifactEnvelope, payload: object) -> ArtifactEnvelope: ...
def validate_checkpoint(store: RuntimeStore, checkpoint: CheckpointRecord, expected: CompatibilityIdentity) -> None: ...
def invalidate_downstream(store: RuntimeStore, run_id: str, step_id: str) -> tuple[str, ...]: ...
```

- [ ] **Step 1: Write failing tests for Run-level Case binding and Invocation-level execution binding.**

Assert Case changes affect new Runs only, while compatible later Invocations may continue the same Run. Assert incompatible Workflow/Prompt/Schema/Runtime configuration fails deterministically.

- [ ] **Step 2: Verify failure.**

```bash
pytest tests/unit/research/runtime/test_binding.py -v
```

Expected: FAIL because binding APIs do not exist.

- [ ] **Step 3: Implement bindings and exact compatibility checks.**

Compatibility identity includes exactly:

```text
Workflow identity/version
Step identity/version
Prompt identity/version when applicable
Schema identity/version
Runtime configuration identity
```

No fuzzy or semantic similarity check is allowed.

- [ ] **Step 4: Write failing Artifact commit tests.**

```python
def test_uncommitted_residue_cannot_be_used_as_step_input(store):
    residue = make_uncommitted_residue()
    store.write_residue(residue)
    with pytest.raises(ArtifactNotCommittedError):
        store.resolve_input(residue.artifact_id)
```

- [ ] **Step 5: Implement the commit protocol.**

Perform in order:

```text
payload/envelope
→ digest + metadata
→ committed evidence
→ ARTIFACT_COMMITTED event
```

Only committed Artifacts are eligible for Input Binding.

- [ ] **Step 6: Write failing Checkpoint tests.**

Verify exact compatibility, missing Artifact failure, digest mismatch, and downstream invalidation after upstream rerun.

- [ ] **Step 7: Implement Checkpoint persistence and invalidation.**

Checkpoint stores Artifact references plus compatibility metadata; it never stores serialized process state. Invalidation is historical and does not delete prior records.

- [ ] **Step 8: Run Task 3 tests and commit.**

```bash
pytest tests/unit/research/runtime/test_binding.py tests/unit/research/runtime/test_artifacts.py tests/unit/research/runtime/test_checkpoints.py -v

git add src/ai_native_workbench/research/runtime/binding.py src/ai_native_workbench/research/runtime/artifacts.py src/ai_native_workbench/research/runtime/checkpoints.py tests/unit/research/runtime/test_binding.py tests/unit/research/runtime/test_artifacts.py tests/unit/research/runtime/test_checkpoints.py
git commit -m "feat: add runtime bindings artifacts and checkpoints"
```

---

### Task 4: Executor Registry and Candidate/Validation/Acceptance Pipeline

**Files:**
- Create: `src/ai_native_workbench/research/runtime/execution/__init__.py`
- Create: `src/ai_native_workbench/research/runtime/execution/registry.py`
- Create: `src/ai_native_workbench/research/runtime/execution/candidate.py`
- Create: `src/ai_native_workbench/research/runtime/execution/acceptance.py`
- Create: `src/ai_native_workbench/research/runtime/execution/llm.py`
- Test: `tests/unit/research/runtime/execution/test_registry.py`
- Test: `tests/unit/research/runtime/execution/test_candidate.py`
- Test: `tests/unit/research/runtime/execution/test_llm.py`

**Interfaces:**
- Consumes: WorkflowStep execution metadata and explicit Attempt Input Bindings.
- Produces: registry-based execution, deterministic fake Executors, Candidate results, validation/acceptance dispositions, and isolated DeepSeek adapter.

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

- [ ] **Step 1: Write failing registry tests.**

```python
def test_registry_resolves_executor_by_mode():
    registry = ExecutorRegistry()
    fake = DeterministicExecutor()
    registry.register("deterministic", fake)
    assert registry.resolve("deterministic") is fake
```

Assert unknown mode fails explicitly and no registry lookup uses `step_id` as the dispatch key.

- [ ] **Step 2: Implement Registry and deterministic executor.**

The deterministic executor returns semantically meaningful structured Candidates for the synthetic fixture.

- [ ] **Step 3: Write failing Candidate validation/acceptance tests.**

Schema, provenance, and domain failures must prevent Step completion. Rejected candidates remain durable history. Candidate/Validation/Acceptance never modify Attempt state semantics.

- [ ] **Step 4: Implement AcceptancePipeline.**

Acceptance policies must be explicit:

```text
automatic
human
canonical/domain
```

- [ ] **Step 5: Write failing DeepSeek adapter tests with mocked transport.**

```python
def test_deepseek_adapter_records_provider_and_model(fake_transport, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-only")
    result = DeepSeekClient(fake_transport).complete(make_request())
    assert result.provider == "deepseek"
    assert result.model == "deepseek-v4-flash"
```

Test timeout/API failure mapping and prompt/schema digest capture; never use a real secret.

- [ ] **Step 6: Implement the thin DeepSeek adapter.**

Keep provider-specific HTTP details isolated. No provider fallback or Runtime state mutation.

- [ ] **Step 7: Run execution tests and commit.**

```bash
pytest tests/unit/research/runtime/execution -v

git add src/ai_native_workbench/research/runtime/execution tests/unit/research/runtime/execution
git commit -m "feat: add runtime executor and acceptance pipeline"
```

---

### Task 5: Standard Research Workflow Adapter and Source Acquisition

**Files:**
- Create: `src/ai_native_workbench/research/runtime/workflow.py`
- Create: `src/ai_native_workbench/research/runtime/source/acquisition.py`
- Create: `tests/unit/research/runtime/test_workflow.py`
- Create: `tests/unit/research/runtime/source/test_acquisition.py`
- Create: `tests/integration/research/runtime/source/test_declared_urls.py`
- Reference only: `src/ai_native_workbench/research/workflow/contract.py`
- Reference only: `src/ai_native_workbench/research/workflow/composition.py`

**Interfaces:**
- Consumes: existing public Workflow Core contracts and approved Case source declarations.
- Produces: versioned `StandardResearchWorkflow` adapter and durable Source Acquisition capability.

**Key APIs:**

```python
@dataclass(frozen=True)
class StandardResearchWorkflow:
    definition: WorkflowDefinition
    gate_barriers: Mapping[str, GateBarrier]

def scope_nodes(workflow: StandardResearchWorkflow, scope: ExecutionScope) -> tuple[str, ...]: ...
def validate_entry_boundary(workflow: StandardResearchWorkflow, step_id: str) -> None: ...

class SourceAcquisitionService:
    def acquire(self, case: ResearchCase, run: RunRecord) -> AcquisitionResult: ...
```

- [ ] **Step 1: Write failing tests for the Standard Workflow adapter.**

Verify the adapter uses `WorkflowDefinition`, dependency validation, lifecycle mapping, and topological order from Workflow Core. H2/H3/H4 are barrier metadata, not artificial Step nodes.

- [ ] **Step 2: Verify failure.**

```bash
pytest tests/unit/research/runtime/test_workflow.py -v
```

Expected: FAIL before Runtime workflow adapter exists.

- [ ] **Step 3: Implement the Standard Workflow adapter.**

Do not turn the existing `WorkflowRunner` into a Research Runtime. The Runtime scheduler will consume this adapter later.

- [ ] **Step 4: Write failing source declaration tests.**

Cover malformed URL, duplicate source ID, unsupported scheme, required/optional flags, and frozen source declaration digest.

- [ ] **Step 5: Implement declaration validation.**

Only the Case's frozen `inputs/urls.yaml` declarations may be acquired.

- [ ] **Step 6: Write failing local HTTP acquisition tests.**

Use a local server to cover success, redirect, oversized/unsupported content, required failure, optional failure, metadata capture, digesting, and reuse of a committed Source Artifact in the same Run.

- [ ] **Step 7: Implement SourceAcquisitionService.**

Use standard-library HTTP primitives unless an existing dependency is strictly necessary. Preserve raw content and retrieval metadata where supported.

- [ ] **Step 8: Run focused tests and commit.**

```bash
pytest tests/unit/research/runtime/test_workflow.py tests/unit/research/runtime/source/test_acquisition.py -v
pytest tests/integration/research/runtime/source/test_declared_urls.py -v
pytest tests/unit/research/workflow -q

git add src/ai_native_workbench/research/runtime/workflow.py src/ai_native_workbench/research/runtime/source/acquisition.py tests/unit/research/runtime/test_workflow.py tests/unit/research/runtime/source tests/integration/research/runtime/source
git commit -m "feat: add standard research workflow and source acquisition"
```

---

### Task 6: Gate Runtime and Research Orchestrator Control Plane

**Files:**
- Create: `src/ai_native_workbench/research/runtime/gates/runtime.py`
- Create: `src/ai_native_workbench/research/runtime/orchestrator.py`
- Create: `src/ai_native_workbench/research/runtime/control.py`
- Create: `tests/unit/research/runtime/gates/test_runtime.py`
- Create: `tests/unit/research/runtime/test_orchestrator.py`
- Create: `tests/unit/research/runtime/test_control.py`
- Create: `tests/integration/research/runtime/test_revision_and_controls.py`

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: durable Gate Barriers, Attempt execution protocol, Run lifecycle orchestration, and explicit control actions.

**Key APIs:**

```python
class GateRuntime:
    def create(self, run_id: str, logical_gate_id: str, target: ReviewTarget) -> GateRecord: ...
    def decide(self, gate_id: str, decision: GateDecision, reviewer: str, comment: str, revision_target: RevisionTarget | None) -> GateRecord: ...
    def replace(self, prior_gate_id: str, target: ReviewTarget, gate_id: str) -> GateRecord: ...

class ResearchRuntime:
    def create_run(self, case: ResearchCase) -> RunRecord: ...
    def start(self, run_id: str, *, until_step: str | None = None) -> RunRecord: ...
    def resume(self, run_id: str, *, until_step: str | None = None) -> RunRecord: ...
    def retry(self, run_id: str, step_id: str) -> RunRecord: ...
    def rerun(self, run_id: str, step_id: str) -> RunRecord: ...
    def run_from(self, run_id: str, step_id: str, *, until_step: str | None = None) -> RunRecord: ...
    def decide_gate(self, run_id: str, gate_id: str, decision: GateDecision, reviewer: str, comment: str, revision_target: RevisionTarget | None = None) -> RunRecord: ...
```

- [ ] **Step 1: Write failing Gate tests.**

Assert creation binds a concrete Artifact/Candidate Set; `APPROVE` permits progression; `REJECT` moves Run to `NEEDS_REVISION` and does not auto-rerun.

- [ ] **Step 2: Implement GateRuntime and generic supersession.**

When a new execution path creates a replacement Gate, persist `supersedes/superseded_by` relationship facts. Do not add an `INVALIDATED` Gate state.

- [ ] **Step 3: Write failing revision tests.**

```python
def test_rejected_gate_requires_revision_target():
    with pytest.raises(RuntimeContractError):
        gate_runtime.decide("gate-1", GateDecision.REJECTED, "human", "revise", None)
```

Accept only a validated `RevisionTarget(entry_step, reason)`. Runtime must reject an entry boundary that is downstream of the barrier's required revision boundary.

- [ ] **Step 4: Implement revision semantics.**

`NEEDS_REVISION -> resume` creates a new Invocation using the explicit revision target. Historical Attempts, Artifacts, and Gates are never mutated.

- [ ] **Step 5: Write failing orchestrator tests for the Attempt start protocol.**

Assert exact order:

```text
ATTEMPT_CREATED
→ INPUT_BOUND
→ ATTEMPT_STARTED
→ Executor invoked
```

- [ ] **Step 6: Implement single-process sequential orchestration.**

Resolve Workflow nodes through the Standard Workflow adapter, resolve Executors through `ExecutorRegistry`, persist lifecycle facts, and stop at Gate Barriers or failures. Do not add R1/R2/R3/R4/R5 condition chains as the main dispatch mechanism.

- [ ] **Step 7: Write failing control-action tests.**

Verify:

```text
retry → same Attempt + same Invocation
rerun → new Attempt + same Invocation
resume → new Invocation + same Run
--from R3 → new Invocation + new R3 Attempt + rebuilt downstream path
--until R5 → bounded completion
```

- [ ] **Step 8: Implement control actions and completion rules.**

Invocation succeeds only when its requested scope has complete durable evidence. Run state is projected from Invocation outcome plus Gate/failure disposition. Bounded completion stores `completion_reason=BOUNDED_SCOPE`.

- [ ] **Step 9: Run focused control tests and commit.**

```bash
pytest tests/unit/research/runtime/gates -v
pytest tests/unit/research/runtime/test_orchestrator.py tests/unit/research/runtime/test_control.py -v
pytest tests/integration/research/runtime/test_revision_and_controls.py -v

git add src/ai_native_workbench/research/runtime/gates src/ai_native_workbench/research/runtime/orchestrator.py src/ai_native_workbench/research/runtime/control.py tests/unit/research/runtime/gates tests/unit/research/runtime/test_orchestrator.py tests/unit/research/runtime/test_control.py tests/integration/research/runtime/test_revision_and_controls.py
git commit -m "feat: add research runtime control plane"
```

---

### Task 7: R5 Canonical Boundary, ResearchSnapshot, Synthetic E2E, and Final Regression

**Files:**
- Create: `src/ai_native_workbench/research/runtime/canonical.py`
- Create: `src/ai_native_workbench/research/runtime/snapshot.py`
- Create: `cases/runtime-synthetic/00-research-charter.md`
- Create: `cases/runtime-synthetic/inputs/urls.yaml`
- Create: `tests/unit/research/runtime/test_canonical_boundary.py`
- Create: `tests/unit/research/runtime/test_snapshot_boundary.py`
- Create: `tests/integration/research/runtime/test_synthetic_e2e.py`
- Create: `tests/integration/research/runtime/test_crash_windows.py`
- Create: `tests/integration/research/runtime/test_lineage.py`
- Create: `scripts/run_research.py`

**Interfaces:**
- Consumes: Tasks 1–6, public Canonical Registry/Snapshot APIs, and the semantically real synthetic case.
- Produces: trustworthy R5 → Canonical Registry → ResearchSnapshot execution boundary plus final Step 6 validation.

**Key APIs:**

```python
class CanonicalBoundary:
    def register_accepted(self, artifact: ArtifactEnvelope, registry: CanonicalRegistry) -> CanonicalBinding: ...

class SnapshotBoundary:
    def freeze(self, binding: CanonicalBinding, registry: CanonicalRegistry, snapshot_id: str) -> SnapshotBinding: ...
    def reconcile(self, binding: SnapshotBinding, registry: CanonicalRegistry) -> SnapshotBinding: ...
```

- [ ] **Step 1: Write failing Canonical two-phase boundary tests.**

Assert:

```text
CANONICAL_BINDING_PENDING
→ public CanonicalRegistry registration
→ CANONICAL_BINDING_COMMITTED
```

A crash between pending and committed must not cause duplicate semantic registration or require Runtime access to private Registry dictionaries.

- [ ] **Step 2: Implement `CanonicalBoundary`.**

Use `register()` and other public APIs only. If the current Canonical Core lacks a necessary public persistence/reconciliation API, add the smallest domain-owned API there and test it in Canonical Core; never read `_current` or `_states` from Runtime.

- [ ] **Step 3: Write failing Snapshot-boundary tests.**

Assert Snapshot creation immediately follows successful R5 canonical registration, Snapshot is not a Workflow Step, and Snapshot resolves exact historical fingerprints.

- [ ] **Step 4: Implement `SnapshotBoundary`.**

Use existing `CanonicalRegistry.snapshot()` semantics and persist only the Runtime Snapshot Binding. Runtime does not become the semantic owner of Snapshot membership.

- [ ] **Step 5: Write failing Snapshot failure reconciliation tests.**

Simulate successful R5 canonical registration followed by Snapshot failure and assert:

```text
R5 Attempt = SUCCEEDED
Invocation = FAILED
Run = FAILED
```

Recovery must retry/reconcile only Snapshot creation.

- [ ] **Step 6: Write the failing synthetic happy-path E2E test.**

```python
def test_synthetic_runtime_reaches_snapshot(tmp_path):
    case = make_runtime_synthetic_case(tmp_path)
    runtime = build_test_runtime(tmp_path)
    run = runtime.start(runtime.create_run(case).run_id)
    assert run.state is RunState.WAITING_FOR_HUMAN

    run = runtime.decide_gate(run.run_id, "H2", GateDecision.APPROVED, "human", "ok")
    run = runtime.decide_gate(run.run_id, "H3", GateDecision.APPROVED, "human", "ok")
    assert run.state is RunState.COMPLETED
    assert run.completion_reason == "BOUNDED_SCOPE"
    assert runtime.snapshot_for_run(run.run_id).snapshot_id
```

- [ ] **Step 7: Verify failure and then implement the semantically real synthetic fixture.**

```bash
pytest tests/integration/research/runtime/test_synthetic_e2e.py -v
```

Expected before implementation: FAIL.

The fixture must model:

```text
Synthetic Source
→ Evidence
→ Claim / Relationship
→ Analysis working artifact
→ Human Judgment artifact
→ Canonicalization
→ ResearchSnapshot
```

Use only `Entity`, `Claim`, `Evidence`, `Source`, `Unknown`, and `Relationship` for Canonical meaning; do not invent a Runtime-owned Canonical object.

- [ ] **Step 8: Implement the complete R1–R5 synthetic path.**

Wire source acquisition, deterministic Executors, validation/acceptance, H2/H3 Gates, R5 Canonicalization, Snapshot freeze, and bounded completion through the public Runtime API.

- [ ] **Step 9: Add lineage and crash-window integration tests.**

Cover:

```text
upstream rerun → downstream checkpoint invalidation
new path → new Gate review target
--from → new Invocation + rebuilt downstream lineage + new Snapshot
bounded COMPLETED → resume → new Invocation
NEEDS_REVISION → explicit revision_target → resume
Artifact/success/projection crash windows
```

Run:

```bash
pytest tests/integration/research/runtime/test_lineage.py -v
pytest tests/integration/research/runtime/test_crash_windows.py -v
```

- [ ] **Step 10: Implement the thin CLI entry point and test delegation.**

`scripts/run_research.py` must delegate to `ResearchRuntime` and expose only `create/start`, `resume`, `retry`, `rerun`, `--from`, `--until`, and Gate decisions. It must not contain workflow orchestration.

- [ ] **Step 11: Run the complete Runtime suite and existing subsystem suites.**

```bash
pytest tests/unit/research/runtime -v
pytest tests/integration/research/runtime -v
pytest tests/unit/research/workflow -q
pytest tests/unit/research/canonical -q
pytest tests/unit/research/evaluation -q
pytest tests/unit/research/build -q
pytest tests/integration/research/canonical -q
```

Expected: PASS.

- [ ] **Step 12: Run the repository regression gate.**

```bash
pytest --collect-only -q
pytest -q
```

Expected: all tests pass; the pre-existing 191-test baseline remains green and the count increases only by the intentionally added Runtime tests.

- [ ] **Step 13: Perform the final architecture check.**

Run:

```bash
grep -R "_current\|_states\|_logical_id_types" -n src/ai_native_workbench/research/runtime || true
grep -R 'step_id == "R[1-5]' -n src/ai_native_workbench/research/runtime || true
git diff --check
```

Expected: no Runtime access to Canonical private internals, no hardcoded primary Step-ID dispatch, and no whitespace errors.

- [ ] **Step 14: Commit final Step 6 validation evidence.**

```bash
git add src/ai_native_workbench/research/runtime cases/runtime-synthetic tests/integration/research/runtime scripts/run_research.py
git commit -m "test: validate research runtime v1 end to end"
```

---

## Final Verification Checklist

- [ ] Approved Case is the only Runtime entry point.
- [ ] Run/Invocation/Attempt lineage is inspectable and immutable as specified.
- [ ] Attempt Input Binding is durable before Attempt execution starts.
- [ ] `execution.jsonl` can rebuild `run.json`.
- [ ] Crash reconciliation never silently reruns business work.
- [ ] `retry`, `rerun`, `resume`, `--from`, and `--until` semantics match the Spec.
- [ ] Gate approval is target-bound; superseded Gates never authorize a new lineage.
- [ ] Human rejection produces `NEEDS_REVISION` and requires explicit revision execution.
- [ ] R5 acceptance crosses the Canonical Core boundary through public APIs.
- [ ] ResearchSnapshot is a Runtime-managed freeze operation, not a Workflow Step.
- [ ] Synthetic E2E reaches ResearchSnapshot without external network or live LLM dependency.
- [ ] Existing Workflow/Canonical/Evaluation/Build tests remain green.
- [ ] Step 6 does not absorb Step 7 scope.

## Execution Handoff

This plan is intentionally divided into independently reviewable vertical slices. Use `superpowers:subagent-driven-development` for fresh-worker execution per task, or `superpowers:executing-plans` for inline execution. Do not collapse the seven tasks into a single implementation pass.
