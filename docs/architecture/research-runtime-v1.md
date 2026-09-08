# Research Runtime v1

> Architecture specification for the executable Research Build System in `ai-native-workbench`.
>
> Status: **Architecture baseline · 2026-09-08**
>
> This document defines how an approved Research Case is executed end-to-end. It is intentionally separate from `docs/methodology/research-system-v1.md`, which defines the Research System's higher-level methodology, lifecycle, and principles.

---

## 1. Purpose

Research Runtime v1 turns an **approved Research Case** into a durable, auditable research execution:

```text
Approved Research Case
        ↓
Research Run
        ↓
Source Acquisition
        ↓
Standard Research Workflow
        ↓
Canonical Knowledge
        ↓
Evaluation
        ↓
Research Snapshot
        ↓
Build / Delivery
        ↓
Archive
```

The Runtime is not a chatbot and does not own the external research-framing conversation. Human + general-purpose AI tools may be used outside the system to turn a research idea into an approved Research Charter and source list. The Runtime begins after those inputs have been approved.

The design goal is **minimal sufficient engineering**: durable single-machine execution, human-in-the-loop control, explicit provenance, resumability, and reuse of the existing Workflow, Canonical, Evaluation, and Build cores without prematurely introducing databases, queues, distributed workers, browser agents, or multi-agent orchestration.

---

## 2. System Boundary

### 2.1 Outside the Research Build System

```text
Human
  +
ChatGPT / Claude / Gemini / other general AI
        ↓
Research Idea
        ↓
Research Framing
        ↓
Research Charter
        ↓
Source Selection
        ↓
Human Approval (H1)
```

The external process produces, at minimum:

```text
cases/<case-id>/
├── 00-research-charter.md
└── inputs/
    └── urls.yaml
```

### 2.2 Inside the Research Build System

```text
Approved Case
    ↓
Case Validation
    ↓
Research Run
    ↓
Source Acquisition
    ↓
R1 → R2 → R3 → H2 → R4 → H3 → R5 → R6 → H4
    ↓
Research Snapshot
    ↓
R7 Build / Delivery
    ↓
R8 Archive
```

The Runtime does not perform autonomous web search in v1. It fetches sources explicitly declared by the Case.

---

## 3. Architectural Principles

### 3.1 Case Is Definition

A Research Case is an executable research package containing approved research definition and declared source inputs. It is not one execution and does not contain mutable execution state.

### 3.2 Run Is Execution State

A Research Run represents one concrete execution of one Case. Multiple Runs may exist for the same Case.

```text
Case
 ├── Run 001
 ├── Run 002
 └── Run 003
```

### 3.3 Control Plane Is Separate from Knowledge Plane

```text
Execution / Control Plane
    Research Run
    Step Attempts
    Human Gates
    Artifacts
    Checkpoints
    Execution History

Knowledge Plane
    Canonical Registry
    Research Snapshot
```

The Runtime controls execution but does not become the authority for research meaning.

### 3.4 Workflow Core Is Separate from Research Runtime

Workflow Core provides generic workflow definitions, dependency validation, ordering, and Step contracts. Research Runtime provides research-specific lifecycle orchestration, durable state, gates, artifacts, and recovery.

The Runtime is built **on top of** Workflow Core; Workflow Core does not grow into a Research Runner.

### 3.5 Step / Executor / Artifact Separation

```text
Workflow Step = WHAT work must be done
Executor      = HOW the work is performed
Artifact      = WHAT durable result was produced
```

### 3.6 LLM Output Is Never Automatically Authoritative

Important outputs follow:

```text
Candidate
   ↓
Validation
   ↓
Acceptance
   ↓
Accepted Artifact / Knowledge
```

An LLM may produce candidates but does not directly own authoritative research knowledge.

### 3.7 Human Judgment Remains Explicit

Consequential selection and judgment gates remain durable Runtime state. Rejection does not cause an automatic corrective loop.

### 3.8 Reproducibility Is Layered

- **Execution reproducibility:** the execution can be reconstructed and audited from recorded inputs, versions, configuration, artifacts, and events; LLM output is not assumed deterministic.
- **Canonical reproducibility:** a Research Snapshot resolves to the exact historical canonical state from which it was created.
- **Delivery reproducibility:** a snapshot and declared build inputs can deterministically reproduce delivery artifacts.

---

## 4. Research Case

### 4.1 MVP Structure

```text
cases/<case-id>/
├── 00-research-charter.md
├── inputs/
│   └── urls.yaml
└── runs/
```

A separate `case.yaml` is not required in the MVP. Conventional filenames are sufficient until a real need for additional machine configuration is demonstrated.

### 4.2 Case Responsibilities

The Case provides:

- approved Research Charter;
- declared source URLs;
- research-specific constraints present in the approved definition;
- durable identity for the research problem.

The Case does **not** define an arbitrary custom workflow in v1. Cases use the shared Standard Research Workflow unless a future version explicitly introduces workflow selection as a validated capability.

### 4.3 `urls.yaml`

`urls.yaml` is a source-selection input, not an evidence or claim store. Its entries identify sources the Runtime should attempt to acquire.

Each source may declare whether it is required. Required-source acquisition failure blocks the Run before research execution. Optional-source failure is recorded but does not by itself block the Run.

---

## 5. Research Run

A Run answers:

> What is the current state of this concrete research execution, and what has happened so far?

Minimum concepts:

```text
run_id
case_id
workflow identity
input digests
runtime configuration
current status
current stage
execution scope
step executions
human gates
artifacts
execution history
completion / stop information
```

A Run is durable on disk and must be restartable without relying on in-memory Python state.

`execution_scope` records the requested lifecycle boundary for the Run. A normal build has full lifecycle scope; a bounded run such as `--until R3` has a partial scope.

---

## 6. Runtime State Model

### 6.1 Run Status

v1 uses six primary Run states:

```text
CREATED
RUNNING
WAITING_FOR_HUMAN
NEEDS_REVISION
FAILED
COMPLETED
```

Meaning:

- `CREATED` — Run exists but execution has not started.
- `RUNNING` — Runtime is actively executing the workflow.
- `WAITING_FOR_HUMAN` — execution is intentionally paused at a required human decision.
- `NEEDS_REVISION` — a human has rejected or requested revision of consequential research output.
- `FAILED` — system or execution failure prevents normal continuation.
- `COMPLETED` — the requested execution scope completed successfully.

`NEEDS_REVISION` is not an execution error, and `FAILED` is not a research-quality judgment.

A Run may therefore be `COMPLETED` for a bounded execution scope without claiming that the entire Research Lifecycle completed. `completion_reason` and `execution_scope` make that distinction explicit.

### 6.2 Step State

A logical Step may be:

```text
PENDING
RUNNING
WAITING_FOR_HUMAN
FAILED
COMPLETED
```

`NEEDS_REVISION` is primarily a Run / Gate semantic, not an ordinary Step execution state.

### 6.3 Step Attempt

Each concrete execution of a logical Step is a separate Attempt:

```text
R2
 ├── attempt-001 → FAILED
 ├── attempt-002 → FAILED
 └── attempt-003 → SUCCEEDED
```

Historical Attempts are never silently overwritten.

### 6.4 Control Actions

State and control action are distinct concepts:

```text
State  = where the system is
Action = what an operator asks it to do next
```

- `retry` — retry within the same Attempt according to its retry policy.
- `rerun` — create a new Attempt for the logical Step.
- `resume` — continue an existing Run from its durable state.
- `--from Rn` — start from an existing, validated checkpoint for `Rn`; it does not mean “ignore missing prerequisites”.
- `--until Rn` — execute through `Rn`, then mark the requested scope as completed at that boundary; this is not a claim that later lifecycle stages were completed.

### 6.5 Revision Semantics

Human rejection does not automatically trigger a loop. The Run becomes `NEEDS_REVISION`, and a human must explicitly choose a recovery action such as rerunning an upstream Step, changing the Case, or starting a new Run.

---

## 7. Runtime Components

### 7.1 Research Orchestrator

The Orchestrator is the Runtime coordination center. It owns:

- loading current Run state;
- resolving the next Workflow node;
- checking prerequisites;
- invoking Execution Capabilities;
- recording step results;
- creating and resolving Human Gates;
- updating Run state;
- coordinating checkpoint and recovery behavior.

It does not own HTTP retrieval, LLM API details, canonical business rules, evaluation rules, or delivery rendering.

### 7.2 Case / Run Management

Responsible for validating Cases, creating and loading Runs, reconstructing execution context from durable artifacts, and enforcing Run identity boundaries.

### 7.3 Workflow Core

Responsible for:

- `WorkflowDefinition`;
- `WorkflowStep`;
- dependency graph validation;
- deterministic execution order;
- reusable Step contract validation.

Research Runtime-specific state and persistence do not belong in Workflow Core.

### 7.4 Runtime Store

The v1 Runtime Store uses the filesystem. It stores:

- Run state;
- execution events;
- Step Attempts;
- Human Gate records;
- Artifacts;
- manifests and checkpoint metadata.

No database is required for v1.

### 7.5 LLM Execution Service

Provides the LLM execution boundary used by LLM-backed Steps.

v1 implements only one provider/model configuration:

```text
provider: deepseek
model: deepseek-v4-flash
```

A thin internal client boundary is retained so Workflow Steps do not depend directly on provider-specific HTTP details.

There is no automatic multi-provider fallback in v1.

### 7.6 Source Acquisition Service

Consumes declared URLs from `urls.yaml` and produces durable Source Artifacts.

Responsibilities include:

- URL validation;
- HTTP retrieval;
- redirect handling;
- bounded content capture;
- retrieval metadata;
- content digest;
- fetch status / error recording.

The v1 boundary excludes autonomous web search, browser agents, MCP retrieval, and dynamic source discovery.

### 7.7 Human Gate Runtime

Maintains durable Gate Records, including:

```text
gate_id
run_id
stage
status
required_decision
reviewer
decision
comment
created_at
decided_at
```

Human interaction may later be exposed through different interfaces; the Runtime contract is the state transition, not a chat UI.

### 7.8 Canonical / Evaluation / Build Cores

These remain independent domain capabilities. Runtime coordinates them but does not duplicate their semantics.

---

## 8. Persistence and Runtime Store

### 8.1 Recommended Run Layout

```text
cases/<case-id>/
└── runs/<run-id>/
    ├── run.json
    ├── execution.jsonl
    ├── steps/
    │   ├── R1/
    │   │   ├── state.json
    │   │   └── attempt-001/
    │   │       ├── execution.json
    │   │       └── output.json
    │   └── ...
    ├── gates/
    │   ├── H2.json
    │   ├── H3.json
    │   └── H4.json
    ├── artifacts/
    │   └── ...
    └── manifests/
        └── execution.json
```

The exact filesystem filenames may evolve during implementation, but the logical boundaries must remain.

### 8.2 Current State vs History

```text
run.json
    = materialized current state

execution.jsonl
    = append-only execution history
```

Historical Attempt records and Artifacts are immutable once committed.

### 8.3 Checkpoint

A checkpoint is a set of durable Artifacts and metadata sufficient to reconstruct the input context for a later Step. It is not a serialized Python process.

A valid checkpoint requires:

- required input Artifacts exist;
- referenced digests still match;
- Workflow compatibility is satisfied;
- relevant configuration / schema / prompt identity is compatible.

### 8.4 Downstream Invalidation

When a logical Step is rerun, downstream checkpoints that depended on its previous output are invalid by default unless the Workflow explicitly defines them as compatible with the new result.

---

## 9. Workflow Step and Execution Model

A `WorkflowStep` defines the research work and its contract. Its execution specification identifies the means by which the work is realized.

Conceptually:

```yaml
id: R2
name: Evidence
version: "1"
purpose: Extract and normalize evidence from declared sources.
inputs:
  - source_artifacts
  - research_questions
outputs:
  - evidence_candidates
constraints:
  - preserve provenance
  - do not invent sources
validation:
  - schema valid
  - provenance valid
provenance:
  required: true
execution:
  mode: llm
  prompt: r2-evidence-v1
  output_schema: evidence-candidates-v1
```

The `execution` section is implementation metadata, not the semantic identity of the Step.

### 9.1 Execution Modes

v1 permits these execution patterns:

```text
deterministic
llm
source
human
composite
```

Composite execution is declarative. A Step may combine deterministic processing, source acquisition, LLM transformation, validation, and artifact persistence without allowing the LLM to redefine the Workflow itself.

### 9.2 Prompt / Schema / Template / Configuration

They are distinct:

```text
Workflow = process structure
Prompt   = model instructions
Schema   = machine-readable result contract
Template = human presentation form
Config   = execution parameters
Secret   = sensitive credentials
```

Prompts and schemas are versioned and hashed. Run manifests record the referenced versions and digests.

Secrets are supplied through the runtime environment and are never stored in repository configuration.

---

## 10. Candidate → Validation → Acceptance

Important Step results follow a common pattern:

```text
Executor
   ↓
Candidate Output
   ↓
Schema Validation
   ↓
Provenance Validation
   ↓
Domain Validation
   ↓
Acceptance Policy
   ↓
Accepted Artifact / Knowledge
```

Validation and acceptance are distinct:

- **Validation** asks whether the result satisfies structural, provenance, and domain rules.
- **Acceptance** asks whether the result is authoritative enough to advance.

Acceptance modes may be:

```text
automatic
human
domain
```

Examples:

- R1 Candidate Universe → validated / automatically accepted as working artifact;
- R2 Evidence → validated working artifact with provenance;
- R4 Judgment Candidates → H3 human acceptance;
- R5 Canonical Candidates → Canonical Core acceptance;
- final Delivery → H4 human acceptance.

Rejected candidates and failed Attempts remain durable history.

---

## 11. Source Acquisition

### 11.1 Input

```text
inputs/urls.yaml
```

### 11.2 Acquisition Flow

```text
urls.yaml
    ↓
validate source declarations
    ↓
fetch declared URL
    ↓
preserve content + metadata
    ↓
compute content digest
    ↓
Source Artifact
    ↓
Source Record
```

### 11.3 Failure Policy

- Required source failure → block transition into research execution and record the failure explicitly.
- Optional source failure → record failure and continue.
- Unsupported content / oversized content / unavailable resource → explicit fetch failure, not silent omission.

The v1 implementation should support ordinary direct HTTP retrieval. Complex JavaScript-only pages or browser-dependent acquisition are outside the initial Runtime boundary.

---

## 12. LLM Execution

The LLM is a semantic transformation capability, not a lifecycle controller.

```text
Workflow Step
    ↓
LLM Execution Adapter
    ↓
DeepSeek
    ↓
Structured Candidate
```

The LLM should not directly:

- change Run state;
- approve its own Human Gate;
- register authoritative Canonical objects;
- choose a new Workflow graph;
- silently acquire undeclared external sources.

### 12.1 Audit Metadata

LLM execution should record, where available:

```text
provider
model
prompt_id
prompt_version
prompt_digest
input_artifact_digests
output_digest
timestamp
token_usage
retry_count
status
error
```

This supports execution auditability without claiming deterministic model behavior.

---

## 13. Human Gate Runtime

The standard in-run gates are:

```text
H2 — Population / Selection
H3 — Judgment
H4 — Final Delivery
```

H1 is completed before the Runtime starts under the current operating model.

### 13.1 H2

```text
R3
 ↓
H2
 ↓
Selection Decision
 ↓
R4
```

### 13.2 H3

```text
R4
 ↓
Judgment Candidates
 ↓
H3
 ↓
Accepted Judgments
 ↓
R5
```

### 13.3 H4

```text
R6 PASS
 ↓
H4
 ↓
Research Snapshot
 ↓
R7 Delivery
```

A Gate creates a durable wait state. A rejection creates `NEEDS_REVISION` and does not automatically mutate earlier research.

---

## 14. Standard Research Workflow v1

The default Research Workflow is:

```text
Approved Case
      ↓
Source Acquisition
      ↓
R1 Discover
      ↓
R2 Evidence
      ↓
R3 Analyze
      ↓
H2 Selection Gate
      ↓
R4 Decide
      ↓
H3 Judgment Gate
      ↓
R5 Synthesize / Canonicalize
      ↓
R6 Evaluate
      ↓
H4 Final Delivery Gate
      ↓
Research Snapshot
      ↓
R7 Build / Delivery
      ↓
R8 Archive
```

### 14.1 R1 Discover

Inputs:

- approved Charter;
- acquired Source Artifacts;
- research questions.

Outputs:

- candidate universe;
- taxonomy / categories;
- source map;
- research hypotheses / plan.

R1 creates a working map of the research space, not final selection decisions.

### 14.2 R2 Evidence

Inputs:

- candidate universe;
- Source Artifacts;
- research questions;
- source map.

Outputs:

- Source Records;
- Evidence Candidates;
- Claim Candidates.

### 14.3 R3 Analyze

Inputs:

- evidence;
- claims;
- candidate universe;
- research framework.

Outputs may include:

- comparisons;
- metrics;
- scores;
- relationships;
- analytical findings.

Observation and inference must remain distinguishable.

### 14.4 R4 Decide

Inputs:

- evidence / claims;
- analysis;
- H2 selection decision;
- research questions.

Outputs:

- judgment candidates;
- decision candidates;
- recommendation candidates;
- hypotheses;
- unknowns.

R4 does not silently turn unknowns into negative findings.

### 14.5 R5 Synthesize / Canonicalize

```text
Working Research Artifacts
        ↓
Synthesis
        ↓
Canonical Candidates
        ↓
Schema Validation
        ↓
Provenance Validation
        ↓
Canonical Domain Validation
        ↓
Canonical Registry
```

R5 remains one lifecycle Step even though its internal execution contains multiple validation and acceptance operations.

### 14.6 R6 Evaluate

R6 invokes Evaluation Core rather than reimplementing evaluation logic.

```text
Canonical / research state
        ↓
Evaluation Core
        ↓
EvaluationRun
        ↓
Quality Gate
```

Evaluation failure blocks final Snapshot / Delivery according to the established Evaluation Core semantics.

---

## 15. Canonical Integration

The Runtime must never bypass Canonical Core rules.

The expected boundary is:

```text
R5
 ↓
Canonical Candidates
 ↓
Canonical Core
 ↓
Registry
 ↓
Snapshot
```

The Runtime may request registry operations or snapshot creation, but canonical identity, provenance, historical state, and snapshot resolution remain owned by Canonical Core.

---

## 16. Evaluation Integration

The Runtime delegates evaluation to Evaluation Core.

Runtime responsibilities:

- provide the research state to be evaluated;
- persist the EvaluationRun reference;
- interpret the resulting Quality Gate;
- block or continue lifecycle accordingly.

Evaluation responsibilities remain in Evaluation Core:

- evaluation rules;
- execution of those rules;
- evaluation result semantics;
- quality gate semantics.

---

## 17. Snapshot / Build / Delivery Integration

The Runtime does not implement a second delivery system.

```text
Canonical Registry
      ↓
Research Snapshot
      ↓
Existing Build Core
      ↓
Delivery Artifacts
```

Existing snapshot-bound Build behavior remains the delivery capability. The Runtime calls it only after required evaluation and Human Gate conditions have passed.

Delivery artifacts are projections of canonical knowledge and are never the source of truth.

---

## 18. Failure and Recovery

### 18.1 System Failure

Examples:

```text
network failure
LLM API failure
timeout
invalid response
artifact write failure
validation exception
```

These result in `FAILED` at the appropriate execution level and preserve error metadata.

### 18.2 Research Revision

Examples:

```text
insufficient evidence
human rejects selection
human rejects strategic conclusion
unresolved ambiguity
```

These result in `NEEDS_REVISION` and require explicit human-directed recovery.

### 18.3 No Silent Repair

The Runtime must not silently mutate prior accepted research to make an execution appear successful. New Attempts and new snapshots must remain distinguishable from their predecessors.

---

## 19. Reproducibility and Run Identity

A Run should record enough identity information to answer:

> What exact declared inputs and execution configuration produced these artifacts?

At minimum:

```text
Charter digest
URLs digest
Workflow id / version
Prompt id / version / digest
Schema id / version / digest
Runtime configuration digest
Source artifact digests
Transformation / implementation identity where relevant
```

Execution identity is distinct from Snapshot identity.

```text
Execution identity
    = how the research was run

Snapshot identity
    = what canonical research state was accepted
```

---

## 20. Repository Boundaries

The Runtime should reuse existing repository capabilities rather than creating parallel implementations.

```text
src/ai_native_workbench/research/
├── workflow/      → reusable workflow primitives
├── canonical/     → canonical knowledge authority
├── evaluation/    → evaluation authority
├── build/         → snapshot-bound delivery
└── runtime/       → Research Runtime / orchestration
```

The exact runtime submodules should be chosen during implementation from the architectural responsibilities in this document. Architecture does not require every conceptual component to become a separate Python package.

---

## 21. Validation Strategy

Research Runtime v1 is not validated by unit tests alone. It must be exercised through progressively more realistic executions.

### 21.1 Synthetic Validation

First validate runtime mechanics with a minimal deterministic Case:

- Case loading;
- Run lifecycle;
- Step execution;
- Artifact persistence;
- Human wait / resume;
- retry / rerun semantics;
- checkpoint validation;
- failure handling.

### 21.2 Case 001 Replay

Run the new Runtime against Case 001 as a reference problem. The objective is to test the generic system against a known complex research shape, not to repair the legacy pipeline.

### 21.3 Case 002 Generalization

Run a meaningfully different research problem using the same shared Runtime and Workflow contracts.

The case should not require Case-001-specific step names, data assumptions, or implementation hacks.

### 21.4 Validation Claim

A successful synthetic run demonstrates Runtime mechanics. A successful Case 001 replay demonstrates realistic integration. A successful Case 002 execution demonstrates reusable abstraction.

All three are needed before making a strong reusability claim.

---

## 22. Non-Goals for v1

The following are explicitly outside the first implementation:

- embedded research-framing chatbot;
- autonomous web search;
- browser-agent retrieval;
- MCP-based retrieval orchestration;
- multi-agent coordination;
- dynamic Agent-generated workflow graphs;
- automatic model fallback;
- distributed workers;
- message queues;
- production database infrastructure;
- universal plugin registry;
- vector database as a required Runtime dependency;
- arbitrary local-document ingestion as a required Case input;
- formal CLI as a prerequisite for Runtime semantics.

A thin Python entry point may be used during early validation. A polished `research build <case>` CLI is a downstream interface decision after Runtime semantics stabilize.

---

## 23. Architecture Decision Summary

The v1 architecture freezes the following decisions:

```text
D1  Research Case = Executable Research Package.
D2  Research Run = concrete execution state.
D3  Execution / Control Plane ≠ Knowledge Plane.
D4  Workflow Core ≠ Research Runtime.
D5  Workflow Step = WHAT; Executor = HOW; Artifact = WHAT HAPPENED.
D6  R0 / H1 are outside the current Runtime boundary.
D7  Standard Workflow is DAG-capable; the default research path is linear.
D8  H2 / H3 / H4 are gate barriers, not independent research tasks.
D9  R5 is one lifecycle Step with an internal canonicalization pipeline.
D10 R6 is an Evaluation barrier using Evaluation Core.
D11 R7 reuses Build Core and does not duplicate delivery logic.
D12 Run state is distinct from control actions.
D13 Step Attempts and Artifacts are immutable history.
D14 Source Acquisition fetches declared URLs only.
D15 LLM is an Executor, not the lifecycle controller.
D16 Deterministic code owns mechanical integrity; LLM handles semantic transformation.
D17 Important results follow Candidate → Validate → Accept.
D18 Prompt / Schema / Config / Secret are distinct concerns.
D19 v1 implements DeepSeek only and has no automatic fallback.
D20 Filesystem is the v1 durable Runtime Store.
D21 Checkpoints are validated durable artifacts, not serialized process state.
D22 Existing Canonical / Evaluation / Build cores remain authoritative for their domains.
D23 `--until` is a bounded execution scope, not a new Run state.
```

---

## 24. Relationship to `research-system-v1.md`

`docs/methodology/research-system-v1.md` remains the higher-level methodology and Research System contract. This document is the Runtime architecture that operationalizes those principles.

The Methodology document should be updated only where required to reflect the new system boundary and roadmap. Runtime-specific implementation details should remain here.

The intended documentation hierarchy is:

```text
Research Methodology
    ↓
docs/methodology/research-system-v1.md
    ↓
Research Runtime Architecture
    ↓
docs/architecture/research-runtime-v1.md
    ↓
Implementation Design / Plan
    ↓
Code + Tests
```

---

## 25. Exit Condition for This Architecture

The architecture is considered ready for implementation planning when:

1. the component boundaries in this document are accepted;
2. the Methodology / Architecture boundary is consistent;
3. the Standard Research Workflow can be expressed without Case-001-specific assumptions;
4. Case / Run / Attempt / Artifact / Gate / Snapshot semantics are stable;
5. the existing Workflow, Canonical, Evaluation, and Build cores can be reused without duplicating their domain authority.
