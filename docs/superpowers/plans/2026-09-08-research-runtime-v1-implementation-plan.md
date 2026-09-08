# Research Runtime v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved Research Runtime v1 architecture so an approved Research Case can execute durably from declared sources through the standard research workflow, Human Gates, Canonical/Evaluation integration, Snapshot, Build/Delivery, and archive.

**Architecture:** Build a research-specific Runtime on top of the existing Workflow Core rather than expanding `WorkflowRunner` into a Research Runner. The Runtime owns Case/Run lifecycle, durable filesystem state, orchestration, attempts, checkpoints, gates, and boundary coordination; LLM, Source Acquisition, Canonical, Evaluation, and Build remain separate capabilities.

**Tech Stack:** Python 3.11+, existing standard-library-first codebase, `pytest`, filesystem JSON/JSONL artifacts, YAML parsing for `urls.yaml`, DeepSeek OpenAI-compatible HTTP API through a thin internal client boundary.

**Spec:** `docs/architecture/research-runtime-v1.md`

## Global Constraints

- Runtime begins only from an approved Research Case; R0/H1 research framing remains outside the system.
- MVP Case structure is `cases/<case-id>/00-research-charter.md`, `inputs/urls.yaml`, and `runs/`.
- Cases use the shared Standard Research Workflow; no arbitrary per-case workflow graphs in v1.
- Workflow Core remains domain-agnostic; do not grow the existing `WorkflowRunner` into the Research Runtime.
- Run / execution control state remains separate from Canonical Registry / Snapshot knowledge state.
- Workflow Step means WHAT; Executor means HOW; Artifact means WHAT HAPPENED.
- Important results use Candidate → Validate → Accept; LLM output is never directly authoritative.
- H2/H3/H4 are gate barriers, not standalone research tasks.
- R5 is one lifecycle step containing synthesis and canonicalization; R6 delegates to Evaluation Core; R7 reuses existing Build Core.
- v1 uses filesystem persistence and no database, queue, distributed workers, browser agent, MCP retrieval, or multi-agent orchestration.
- Source Acquisition fetches only URLs declared in `urls.yaml`; required-source failures block research execution and optional-source failures are recorded and non-blocking.
- v1 implements DeepSeek only with no automatic provider/model fallback; secrets come from the runtime environment.
- Step Attempts and produced Artifacts are immutable historical records; rerun creates a new Attempt and invalidates downstream checkpoints by default.
- `resume`, `retry`, `rerun`, `--from`, and `--until` retain the state/action semantics defined by the spec.
- Do not introduce a polished CLI before runtime semantics stabilize; a thin Python entry point is sufficient for validation.
- Preserve existing Canonical, Evaluation, and Build domain authority; do not duplicate their rules inside Runtime.
- Validate every implementation task with focused tests, then the full test suite before the task commit.

---

### Task 1: Align Methodology With the Approved Runtime Boundary

**Files:**
- Modify: `docs/methodology/research-system-v1.md`
- Reference: `docs/architecture/research-runtime-v1.md`
- Test: none (documentation consistency review)

**Interfaces:**
- Consumes: approved Runtime Architecture Spec.
- Produces: methodology text that agrees with the Runtime system boundary and roadmap without importing runtime implementation detail.

- [ ] **Step 1: Update the system scope and operating boundary**

State that R0 remains part of the Research Lifecycle, but under the current operating model Research Framing and H1 approval happen outside the Research Build System; the executable system begins with an approved Research Case containing the Charter and declared source URLs.

- [ ] **Step 2: Clarify Human Gate semantics**

Keep H1/H2/H3/H4/H5 as methodology-level gates, but state that H1 is pre-run definition approval while H2/H3/H4 are Runtime gate barriers. Avoid describing a Human Gate itself as a research work step.

- [ ] **Step 3: Clarify R5 canonicalization semantics**

State that R5 remains one lifecycle stage whose implementation may perform synthesis, candidate canonicalization, validation, and Registry acceptance. Canonical authority remains in Canonical Core.

- [ ] **Step 4: Replace the outdated Step 6/7 roadmap wording**

Change the roadmap so Step 7 is the Research Build System implementation/validation stage, with Synthetic validation, Case 001 replay, and Case 002 generalization as validation sequence elements rather than treating Generalization itself as the whole Step 7.

- [ ] **Step 5: Clarify Source and AI responsibilities**

Distinguish external AI research framing/source selection from internal declared-URL acquisition and clarify that v1 does not perform autonomous web search/browser/MCP retrieval.

- [ ] **Step 6: Review for unwanted Runtime detail**

Ensure implementation-specific filesystem layouts, Python interfaces, retry algorithms, and provider adapter internals remain only in `research-runtime-v1.md`.

- [ ] **Step 7: Commit**

```bash
git add docs/methodology/research-system-v1.md
git commit -m "docs: align methodology with research runtime architecture"
```

---

### Task 2: Add Runtime Domain State and Durable Store Primitives

**Files:**
- Create: `src/ai_native_workbench/research/runtime/models.py`
- Create: `src/ai_native_workbench/research/runtime/store.py`
- Create: `src/ai_native_workbench/research/runtime/__init__.py`
- Test: `tests/unit/research/runtime/test_models.py`
- Test: `tests/unit/research/runtime/test_store.py`

**Interfaces:**
- Consumes: Runtime state semantics from Sections 5–8 of the spec.
- Produces: typed Run/Attempt/Gate/Artifact records and a filesystem-backed store API used by all later Runtime components.

- [ ] **Step 1: Write failing tests for Run and Step Attempt state transitions**

Cover the six Run states, the logical Step states, separate Attempt records, `execution_scope`, `completion_reason`, and rejection → `NEEDS_REVISION` semantics.

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```bash
pytest tests/unit/research/runtime/test_models.py -v
```

Expected: FAIL because the Runtime models do not yet exist.

- [ ] **Step 3: Implement minimal immutable domain records**

Provide explicit enums/dataclasses for Run state, Step state, Attempt status, Gate status/decision, Artifact metadata, and durable run metadata. Do not create framework abstractions beyond fields required by the spec.

- [ ] **Step 4: Write failing tests for filesystem persistence**

Cover creation of a Run directory, atomic-ish materialization of `run.json`, append-only `execution.jsonl`, immutable Attempt/Artifact records, and loading state after a fresh process boundary.

- [ ] **Step 5: Run the focused store tests and verify failure**

Run:

```bash
pytest tests/unit/research/runtime/test_store.py -v
```

Expected: FAIL because the filesystem store is not implemented.

- [ ] **Step 6: Implement the filesystem Runtime Store**

Implement the logical boundaries from the spec: current Run state, append-only execution events, Step Attempt directories, Gate records, Artifact records, and execution manifest metadata. Use JSON/JSONL and deterministic digest helpers; do not serialize Python process state.

- [ ] **Step 7: Run both Runtime unit test modules**

```bash
pytest tests/unit/research/runtime/test_models.py tests/unit/research/runtime/test_store.py -v
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/ai_native_workbench/research/runtime tests/unit/research/runtime/test_models.py tests/unit/research/runtime/test_store.py
git commit -m "feat: add durable research runtime state store"
```

---

### Task 3: Implement Case Loading and Declared Source Acquisition

**Files:**
- Create: `src/ai_native_workbench/research/runtime/case.py`
- Create: `src/ai_native_workbench/research/runtime/source.py`
- Modify: `pyproject.toml`
- Test: `tests/unit/research/runtime/test_case.py`
- Test: `tests/unit/research/runtime/test_source.py`
- Test: `tests/integration/research/runtime/test_case_source.py`

**Interfaces:**
- Consumes: `cases/<case-id>/00-research-charter.md`, `inputs/urls.yaml`, Runtime Store.
- Produces: `ResearchCase` loader/validation result and durable Source Artifacts with source metadata and digest.

- [ ] **Step 1: Decide and document the minimal YAML parser dependency**

Add a small runtime YAML dependency only because the approved MVP input contract requires parsing `urls.yaml`. Keep all HTTP retrieval implementation standard-library-first; do not add a client framework solely for convenience.

- [ ] **Step 2: Write failing Case validation tests**

Cover missing Charter, missing `inputs/urls.yaml`, invalid `urls.yaml`, duplicate `source_id`, malformed URLs, and a valid approved Charter plus valid source list.

- [ ] **Step 3: Run the Case tests and verify failure**

```bash
pytest tests/unit/research/runtime/test_case.py -v
```

Expected: FAIL before `ResearchCase` exists.

- [ ] **Step 4: Implement `ResearchCase` loading and validation**

Load only the approved Charter and declared source inputs. Validate the Charter approval marker required by the architecture, parse the source list, and expose immutable case identity without introducing `case.yaml`.

- [ ] **Step 5: Write failing Source Acquisition tests**

Use a local HTTP test server or stub transport to cover successful retrieval, redirect handling, content digesting, optional-source failure, required-source failure, unsupported/oversized content, and metadata capture.

- [ ] **Step 6: Run the Source tests and verify failure**

```bash
pytest tests/unit/research/runtime/test_source.py -v
```

Expected: FAIL before the acquisition service exists.

- [ ] **Step 7: Implement Source Acquisition**

Fetch only declared HTTP(S) URLs, preserve response content and retrieval metadata as durable Artifacts, record errors explicitly, and distinguish required vs optional source failures. Do not implement autonomous search or browser retrieval.

- [ ] **Step 8: Add an integration test for Case → Source Artifacts**

Verify that a valid Case produces a Run-ready set of source artifacts and that a required-source failure prevents transition into R1.

- [ ] **Step 9: Run focused and integration tests**

```bash
pytest tests/unit/research/runtime/test_case.py tests/unit/research/runtime/test_source.py tests/integration/research/runtime/test_case_source.py -v
```

Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add pyproject.toml src/ai_native_workbench/research/runtime/case.py src/ai_native_workbench/research/runtime/source.py tests/unit/research/runtime/test_case.py tests/unit/research/runtime/test_source.py tests/integration/research/runtime/test_case_source.py
git commit -m "feat: add research case loading and source acquisition"
```

---

### Task 4: Add DeepSeek LLM Execution and Structured Candidate Boundary

**Files:**
- Create: `src/ai_native_workbench/research/runtime/llm.py`
- Create: `src/ai_native_workbench/research/runtime/execution.py`
- Create: `src/ai_native_workbench/research/runtime/prompts.py`
- Create: `src/ai_native_workbench/research/runtime/schemas.py`
- Test: `tests/unit/research/runtime/test_llm.py`
- Test: `tests/unit/research/runtime/test_execution.py`

**Interfaces:**
- Consumes: Step execution specification, prompt/schema identities, input Artifacts, runtime configuration.
- Produces: audited LLM execution records and structured Candidate outputs without direct Canonical mutation or Run-state ownership.

- [ ] **Step 1: Verify the current DeepSeek API contract before implementation**

At implementation time, check the current official DeepSeek API documentation for the OpenAI-compatible endpoint/model and structured-output behavior. Update the implementation only to match currently documented behavior; do not assume an earlier API contract is still valid.

- [ ] **Step 2: Write failing tests for provider-independent `LLMClient` behavior**

Cover successful structured output, API failure, timeout/error propagation, secret absence, request metadata capture, and prompt/schema digests.

- [ ] **Step 3: Run the focused LLM tests and verify failure**

```bash
pytest tests/unit/research/runtime/test_llm.py -v
```

Expected: FAIL before the client boundary exists.

- [ ] **Step 4: Implement the thin LLM client boundary**

Define a minimal `LLMClient` protocol and `DeepSeekClient`. Keep provider-specific HTTP details isolated. Read `DEEPSEEK_API_KEY` from the environment. Do not add provider routing or fallback logic.

- [ ] **Step 5: Write failing tests for Step Execution and Candidate handling**

Cover deterministic execution metadata, LLM execution, composite execution, prompt/schema identity capture, structured Candidate output, and rejection of malformed outputs before acceptance.

- [ ] **Step 6: Implement prompt/schema helpers and execution adapters**

Represent Prompt, Schema, Config, and Secret as distinct concerns. Hash/version prompts and schemas. Return Candidate outputs plus execution metadata and leave acceptance to the Runtime pipeline.

- [ ] **Step 7: Run focused execution tests**

```bash
pytest tests/unit/research/runtime/test_llm.py tests/unit/research/runtime/test_execution.py -v
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/ai_native_workbench/research/runtime/llm.py src/ai_native_workbench/research/runtime/execution.py src/ai_native_workbench/research/runtime/prompts.py src/ai_native_workbench/research/runtime/schemas.py tests/unit/research/runtime/test_llm.py tests/unit/research/runtime/test_execution.py

git commit -m "feat: add DeepSeek execution boundary"
```

---

### Task 5: Define the Standard Research Workflow and Acceptance Pipeline

**Files:**
- Create: `src/ai_native_workbench/research/runtime/workflow.py`
- Create: `src/ai_native_workbench/research/runtime/acceptance.py`
- Modify: `src/ai_native_workbench/research/workflow/contract.py`
- Modify: `src/ai_native_workbench/research/workflow/composition.py`
- Test: `tests/unit/research/runtime/test_workflow.py`
- Test: `tests/unit/research/runtime/test_acceptance.py`
- Test: `tests/unit/research/workflow/test_runtime_compatibility.py`

**Interfaces:**
- Consumes: existing Workflow Core contracts and the Standard Research Workflow v1 described in the spec.
- Produces: a declared Research Workflow plus generic Candidate validation/acceptance orchestration compatible with the existing Workflow Core.

- [ ] **Step 1: Write compatibility tests before changing Workflow Core**

Prove that existing `WorkflowDefinition` and `WorkflowStep` behavior continues to validate and execute independently of Research Runtime state.

- [ ] **Step 2: Run compatibility tests and verify the new cases fail**

```bash
pytest tests/unit/research/workflow/test_runtime_compatibility.py -v
```

Expected: FAIL for the new Research Runtime-specific contract expectations only; existing Workflow tests must remain green.

- [ ] **Step 3: Add the smallest execution metadata extension required by the spec**

Expose execution metadata without moving research-specific state into Workflow Core. Treat any existing `human_gate` metadata as a gate requirement on the transition, not as a Human Gate object.

- [ ] **Step 4: Define the shared Standard Research Workflow**

Represent the default path as a declared DAG with R1, R2, R3, R4, R5, R6 and gate barriers H2/H3/H4. Keep Case-specific research content out of the graph.

- [ ] **Step 5: Write failing Candidate acceptance tests**

Cover schema validation, provenance validation, domain validation, automatic acceptance for working artifacts, human acceptance for R4 judgments, Canonical acceptance for R5, and preservation of rejected candidates.

- [ ] **Step 6: Implement the generic acceptance pipeline**

Provide explicit validation and acceptance boundaries. Do not write special-case `if step_id == ...` logic into the generic pipeline when the acceptance policy can express the rule.

- [ ] **Step 7: Run all focused Workflow and acceptance tests plus the full existing Workflow suite**

```bash
pytest tests/unit/research/runtime/test_workflow.py tests/unit/research/runtime/test_acceptance.py tests/unit/research/workflow -v
```

Expected: PASS, including all pre-existing Workflow tests.

- [ ] **Step 8: Commit**

```bash
git add src/ai_native_workbench/research/runtime/workflow.py src/ai_native_workbench/research/runtime/acceptance.py src/ai_native_workbench/research/workflow/contract.py src/ai_native_workbench/research/workflow/composition.py tests/unit/research/runtime/test_workflow.py tests/unit/research/runtime/test_acceptance.py tests/unit/research/workflow/test_runtime_compatibility.py

git commit -m "feat: define standard research workflow and acceptance pipeline"
```

---

### Task 6: Implement Research Orchestrator, Human Gates, Resume, Retry, Rerun, and Checkpoints

**Files:**
- Create: `src/ai_native_workbench/research/runtime/orchestrator.py`
- Create: `src/ai_native_workbench/research/runtime/gates.py`
- Create: `src/ai_native_workbench/research/runtime/checkpoints.py`
- Modify: `src/ai_native_workbench/research/runtime/models.py`
- Modify: `src/ai_native_workbench/research/runtime/store.py`
- Test: `tests/unit/research/runtime/test_gates.py`
- Test: `tests/unit/research/runtime/test_checkpoints.py`
- Test: `tests/integration/research/runtime/test_orchestrator.py`

**Interfaces:**
- Consumes: Case loader, Runtime Store, Standard Workflow, execution capabilities, acceptance pipeline.
- Produces: end-to-end Run lifecycle control including durable Human Gate waits, resume, retry, rerun, `--from`, `--until`, downstream invalidation, and explicit revision semantics.

- [ ] **Step 1: Write failing Human Gate state tests**

Cover Gate creation, `WAITING_FOR_HUMAN`, approve → resume, reject → `NEEDS_REVISION`, reviewer/comment/timestamps, and the rule that rejection never auto-reruns a Step.

- [ ] **Step 2: Implement Gate Manager and state transitions**

Persist Gate Records independently from the Step artifacts, and materialize Run state consistently after each gate transition.

- [ ] **Step 3: Write failing checkpoint tests**

Cover valid checkpoint reconstruction, missing artifact detection, digest mismatch, incompatible workflow/config/schema/prompt identity, and downstream invalidation after rerun.

- [ ] **Step 4: Implement checkpoint validation and reconstruction**

Reconstruct future Step input context only from durable artifacts and compatible metadata; never serialize or depend on an in-memory Python process.

- [ ] **Step 5: Write failing orchestrator lifecycle tests**

Cover:

```text
Case → Run → Source Acquisition → R1 → R2 → R3 → H2
H2 approve → R4 → H3 → R5 → R6 → H4 → Snapshot → Build
```

Also cover failure → `FAILED`, human rejection → `NEEDS_REVISION`, process restart → `resume`, `retry`, `rerun`, `--from`, and `--until`.

- [ ] **Step 6: Implement the Orchestrator state machine**

Make the Orchestrator the sole Runtime coordination center. It should resolve Workflow nodes, invoke capabilities, persist state/events, and stop exactly at explicit gates or failure boundaries. Do not move domain business rules into the Orchestrator.

- [ ] **Step 7: Implement Attempt semantics**

Create a new Step Attempt for `rerun`; keep `retry` inside an Attempt; mark downstream checkpoints stale after an upstream rerun; preserve all historical records.

- [ ] **Step 8: Run focused integration tests**

```bash
pytest tests/unit/research/runtime/test_gates.py tests/unit/research/runtime/test_checkpoints.py tests/integration/research/runtime/test_orchestrator.py -v
```

Expected: PASS.

- [ ] **Step 9: Commit**

```bash
git add src/ai_native_workbench/research/runtime/orchestrator.py src/ai_native_workbench/research/runtime/gates.py src/ai_native_workbench/research/runtime/checkpoints.py src/ai_native_workbench/research/runtime/models.py src/ai_native_workbench/research/runtime/store.py tests/unit/research/runtime/test_gates.py tests/unit/research/runtime/test_checkpoints.py tests/integration/research/runtime/test_orchestrator.py

git commit -m "feat: add durable research orchestrator and recovery"
```

---

### Task 7: Integrate Canonical, Evaluation, Snapshot, Build, and Add the Thin Execution Entry Point

**Files:**
- Create: `src/ai_native_workbench/research/runtime/build.py`
- Create: `scripts/run_research.py`
- Modify: `src/ai_native_workbench/research/canonical/*` only where a public integration boundary is missing
- Modify: `src/ai_native_workbench/research/evaluation/*` only where a public integration boundary is missing
- Modify: `src/ai_native_workbench/research/build/*` only where a public integration boundary is missing
- Test: `tests/integration/research/runtime/test_end_to_end_runtime.py`
- Test: `tests/integration/research/runtime/test_core_integrations.py`

**Interfaces:**
- Consumes: completed Runtime execution, Canonical Core, Evaluation Core, Build Core.
- Produces: final Snapshot-bound delivery without duplicating Canonical/Evaluation/Build logic, plus a thin Python invocation path for validation.

- [ ] **Step 1: Write failing core integration tests**

Verify that R5 hands candidates to Canonical Core, R6 invokes Evaluation Core, only a passing evaluation can proceed to Snapshot/Delivery, and existing `build_delivery(...)` is reused for R7.

- [ ] **Step 2: Implement only missing public integration adapters**

Expose the smallest Runtime-facing calls needed to invoke existing Canonical, Evaluation, Snapshot, and Build capabilities. Do not copy internal rules into Runtime.

- [ ] **Step 3: Write failing end-to-end tests with a deterministic fake execution backend**

Run an approved synthetic case through source acquisition, R1–R6, Human Gates, Snapshot, Build, and Archive. Verify all durable files can be loaded by a fresh process and that delivery artifacts derive from Snapshot state.

- [ ] **Step 4: Implement the thin Python entry point**

Provide a minimal script equivalent to:

```bash
python scripts/run_research.py cases/002
```

Support only the invocation options justified by the Runtime contract; do not add a formal CLI framework.

- [ ] **Step 5: Run the core integration and end-to-end tests**

```bash
pytest tests/integration/research/runtime/test_core_integrations.py tests/integration/research/runtime/test_end_to_end_runtime.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/runtime/build.py scripts/run_research.py src/ai_native_workbench/research/canonical src/ai_native_workbench/research/evaluation src/ai_native_workbench/research/build tests/integration/research/runtime/test_core_integrations.py tests/integration/research/runtime/test_end_to_end_runtime.py

git commit -m "feat: integrate research runtime end to end"
```

---

### Task 8: Synthetic Runtime Validation and Full Regression

**Files:**
- Create: `cases/runtime-synthetic/00-research-charter.md`
- Create: `cases/runtime-synthetic/inputs/urls.yaml`
- Create: `tests/integration/research/runtime/test_synthetic_case.py`
- Modify: `docs/architecture/research-runtime-v1.md` only if validation exposes a genuine architectural correction
- Modify: `docs/methodology/research-system-v1.md` only if validation exposes a genuine methodology correction

**Interfaces:**
- Consumes: fully implemented Runtime.
- Produces: evidence that Runtime mechanics are operational and that checkpoint/gate/recovery semantics work across a full Run.

- [ ] **Step 1: Create a minimal deterministic synthetic Case**

Use local test-controlled source data and fake executors so the validation isolates Runtime mechanics from live model quality and external web variability.

- [ ] **Step 2: Exercise all critical lifecycle paths**

Verify normal completion, H2 wait/resume, H3 rejection → revision, R2 retry, R3 rerun and downstream invalidation, `--from`, `--until`, required/optional source failures, and process restart/resume.

- [ ] **Step 3: Run the complete repository test suite**

```bash
pytest -q
```

Expected: all existing Workflow/Canonical/Evaluation/Build tests plus new Runtime tests pass.

- [ ] **Step 4: Inspect the Run artifacts manually**

Confirm the durable layout contains current Run state, append-only events, immutable Attempts/Artifacts, Gate Records, and execution manifest entries with the required digests.

- [ ] **Step 5: Review implementation against the architecture spec**

Check that no code introduced an embedded chatbot, autonomous source search, Agent-generated workflow graphs, provider fallback, database, or duplicate Canonical/Evaluation/Build authority.

- [ ] **Step 6: Commit validation fixtures and any evidence-based documentation corrections**

```bash
git add cases/runtime-synthetic tests/integration/research/runtime/test_synthetic_case.py docs/architecture/research-runtime-v1.md docs/methodology/research-system-v1.md
git commit -m "test: validate research runtime synthetic end to end"
```

---

## Final Verification Gate

After all tasks:

- [ ] Run `pytest -q` and record the result.
- [ ] Verify `research-runtime-v1.md` remains consistent with the implementation.
- [ ] Verify `research-system-v1.md` contains only methodology-level Runtime changes.
- [ ] Verify no real secrets were committed.
- [ ] Verify no automatic provider fallback exists.
- [ ] Verify Run/Attempt/Artifact history is immutable in normal operation.
- [ ] Verify required source failure blocks entry into R1 while optional source failure is recorded and non-blocking.
- [ ] Verify a human gate can survive process restart and be resolved later.
- [ ] Verify an upstream rerun invalidates downstream checkpoints by default.
- [ ] Verify R6 cannot produce an accepted final delivery when the required Evaluation gate fails.
- [ ] Verify R7 uses the existing Build Core rather than a parallel renderer.

