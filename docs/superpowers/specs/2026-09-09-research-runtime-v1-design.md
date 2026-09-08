# Research Runtime v1 Design

> Step 6 architectural design for `ai-native-workbench`
>
> Status: **Design approved in brainstorming · 2026-09-09**
>
> Repository baseline: `main` at the Step 5 regression baseline lineage. The current authoritative methodology and architecture documents are `docs/methodology/research-system-v1.md` and `docs/architecture/research-runtime-v1.md`. The older implementation plan remains historical inventory only.

---

## 1. Purpose

Step 6 implements the minimum executable Research Runtime required to turn an approved Research Case into a durable, auditable execution path.

The architectural completion criterion is **not** the existence of Runtime modules. A Step 6 implementation is complete only when the Runtime can execute a real synthetic research path end-to-end, cross the R5 knowledge-plane boundary, survive a process boundary, and expose explicit recovery/control semantics without becoming an autonomous research agent.

The minimum meaningful execution boundary is:

```text
Approved Case
    ↓
Case Validation
    ↓
Run
    ↓
Invocation
    ↓
Source Acquisition
    ↓
Standard Research Workflow
    ↓
R1 → R2 → R3 → H2 → R4 → H3 → R5
    ↓
Candidate → Validation → Acceptance
    ↓
Canonical Registry
    ↓
ResearchSnapshot
    ↓
Bounded completion
```

Step 6 does not require the synthetic fixture to complete R6, R7, or R8. Those remain Step 7 validation and generalization scope. Evaluation/Build/Archive integration contracts may be established and tested where useful, but they are not the Step 6 synthetic completion boundary.

---

## 2. Architectural Context

The repository separates:

```text
Workflow Core
Canonical Core
Evaluation Core
Build Core
Research Runtime
```

Workflow Core defines reusable workflow structure and step contracts. Canonical Core owns semantic authority and historical canonical state. Evaluation Core owns evaluation semantics. Build Core consumes explicit Research Snapshots and owns delivery construction. Research Runtime is the Control Plane that coordinates these capabilities and persists execution history.

The Runtime must not absorb the responsibilities of those cores.

The two-plane model is:

```text
CONTROL PLANE
Run
Invocation
Attempt
Gate
Checkpoint
Artifact lineage
Execution History
Runtime manifests

KNOWLEDGE PLANE
Canonical Registry
ResearchSnapshot
```

Runtime is the authority for execution state and execution lineage. Canonical Core remains the authority for research meaning.

This design follows the Methodology v1 boundary in which H1 remains outside the Build System Runtime, while the Runtime begins from an approved Case and coordinates the shared Research Lifecycle. fileciteturn18file0

The existing Architecture v1 already establishes the filesystem Runtime Store, Run/Step/Attempt concepts, explicit control actions, Source Acquisition, candidate validation/acceptance, and LLM/Workflow/Core boundaries. Step 6 turns those architecture contracts into one coherent executable spine. fileciteturn19file0

---

## 3. Step 6 Completion Criteria

Step 6 is considered architecturally complete when all of the following are true:

1. A synthetic Case can create a durable Run.
2. A Run creates an immutable Execution Invocation with a frozen requested scope.
3. The Runtime resolves the formal `StandardResearchWorkflow` through Workflow Core rather than hardcoding lifecycle order.
4. Source Acquisition consumes only declared URLs and produces immutable Source Artifacts.
5. A minimum semantically real synthetic path crosses R1, R2, R3, H2, R4, H3, and R5.
6. Step execution is mediated by an Executor Registry/Strategy rather than `step_id`-specific orchestration branches.
7. Attempt inputs are explicitly persisted before the Attempt becomes `RUNNING`.
8. Candidates are validated and accepted before Step completion.
9. Accepted R5 output crosses the Canonical Core boundary and enters the Canonical Registry without Runtime access to Canonical internals.
10. A ResearchSnapshot is created/frozen immediately after successful R5 canonical registration, outside the Workflow graph as a Runtime-managed knowledge-plane freeze operation.
11. The Snapshot binding is durable and the Run can complete with `completion_reason=BOUNDED_SCOPE` and an explicit `execution_scope`.
12. `execution.jsonl` is authoritative execution history and `run.json` is a rebuildable projection.
13. Process restart can reconcile incomplete execution without silently rerunning work.
14. Explicit `retry`, `rerun`, `resume`, `--from`, `--until`, and Human Gate decisions have the semantics defined in this document.
15. Artifact, Attempt, Gate, Checkpoint, Invocation, and Event lineage is inspectable.
16. The synthetic integration suite runs without external internet or real LLM dependencies.
17. The repository regression baseline remains `191 passed` for the full pytest suite.

These criteria are intentionally stricter than “all classes exist” and narrower than “all Research Lifecycle stages are production-complete.”

---

## 4. Scope and Non-Goals

### 4.1 In scope

- Durable single-machine Runtime execution.
- Filesystem persistence using JSON/JSONL and immutable artifact storage.
- Run, Invocation, Attempt, Artifact, Gate, Checkpoint, Event models.
- Standard Research Workflow execution.
- Source Acquisition for declared URLs.
- Deterministic fake Executors for integration tests.
- Thin DeepSeek adapter boundary for future/optional real-model execution.
- Human Gate CLI adapter and durable Gate transitions.
- Crash reconciliation.
- Explicit recovery/control actions.
- Candidate validation and acceptance orchestration.
- R5 Canonical registration boundary.
- Runtime binding to ResearchSnapshot.
- Synthetic semantic integration fixture.
- TDD-based implementation and regression protection.

### 4.2 Explicit non-goals

Step 6 does not introduce:

- autonomous research chatbot behavior;
- autonomous source discovery;
- browser agents or MCP retrieval;
- multi-agent orchestration;
- provider fallback;
- distributed workers or queue infrastructure;
- database persistence;
- automatic retry/rerun/correction loops;
- exactly-once execution semantics;
- a general revision-impact analysis engine;
- a general event-sourcing platform;
- Runtime-owned Canonical domain rules;
- Snapshot as a Workflow Step.

---

## 5. Core Execution Model

### 5.1 Run

A Run is the long-lived execution identity for one concrete execution of one Case.

```text
Case
 ├── Run 001
 ├── Run 002
 └── Run 003
```

Run creation freezes the Case Definition inputs required for the execution, including the approved Charter/source declarations and relevant digests/identities.

Run-level Case binding and Invocation-level execution configuration are distinct:

```text
Run
├── Case Binding
│   ├── case_id
│   ├── charter identity/digest
│   ├── source declaration identity/digest
│   └── other approved Case inputs
│
└── Invocation(s)
    └── Execution Binding
        ├── workflow identity/version
        ├── prompt identities/digests
        ├── schema identities/digests
        └── runtime configuration identity
```

A Case change therefore affects new Runs. Continuing an existing Run is permitted only when the new Invocation passes the defined compatibility checks.

### 5.2 Invocation

An Invocation is an immutable execution request boundary.

An Invocation records at minimum:

```text
invocation_id
run_id
requested_scope
entry_mode
from_step?
until_step?
execution configuration identities
status
completion_reason?
timestamps
```

The following rules are fixed:

- Invocation scope is frozen at creation.
- Invocation configuration identity is frozen at creation.
- An Invocation is never rewritten to describe a later execution request.
- `start`, `resume`, `--from`, and `--until` create a new Invocation when they represent a new execution request.
- `rerun` remains within the current Invocation and creates a new Attempt.
- `retry` remains within the current Invocation and Attempt.

Invocation status is intentionally small:

```text
RUNNING
FAILED
SUCCEEDED
```

A Human Gate waiting period does not create another Invocation state; the Run may be `WAITING_FOR_HUMAN` while the active Invocation remains `RUNNING`. The Invocation succeeds only after its requested scope completes. A rejected Human Gate makes the Invocation fail with a human-rejection disposition and moves the Run to `NEEDS_REVISION`.

### 5.3 Cumulative Execution Scope

The Run keeps a cumulative execution scope. Each Invocation also records its own immutable requested scope.

Example:

```text
Run #001
cumulative scope = R1..R5 + SNAPSHOT

Invocation #001
requested scope = R1..R5 + SNAPSHOT

resume

Invocation #002
requested scope = R6..R8

Run #001
cumulative scope = R1..R8
```

The cumulative scope must not erase prior invocation history.

### 5.4 Attempt

An Attempt is one concrete execution instance of one logical Workflow Step.

Attempt status remains:

```text
PENDING
RUNNING
FAILED
SUCCEEDED
```

Candidate/Validation/Acceptance are not folded into Attempt status. They are separate result/disposition evidence.

For example:

```text
Attempt = SUCCEEDED
Gate = REJECTED
Run = NEEDS_REVISION
```

This preserves the fact that execution itself succeeded even though the research result was not accepted for progression.

### 5.5 Attempt Input Binding

Before an Attempt enters `RUNNING`, the Runtime must:

1. create the Attempt;
2. resolve its concrete inputs;
3. persist the Input Binding;
4. then mark the Attempt `RUNNING`;
5. then invoke the Executor.

The Executor never receives an implicitly resolved “latest accepted” input.

An Input Binding records the concrete Artifact Set and upstream Attempt lineage used by the execution. The binding is immutable for that Attempt.

### 5.6 Output Ports and Artifact Sets

A named Workflow Output Port maps to a logical output collection containing one or more Artifact references. Step 6 does not create a separate cardinality type system.

Artifacts are independently identified from Workflow Steps and Attempts, but carry explicit lineage:

```text
artifact_id
run_id
invocation_id
step_id
attempt_id
```

---

## 6. Runtime State Semantics

### 6.1 Run States

The Runtime retains exactly six primary Run states:

```text
CREATED
RUNNING
WAITING_FOR_HUMAN
NEEDS_REVISION
FAILED
COMPLETED
```

Important transitions include:

```text
CREATED → RUNNING
RUNNING → WAITING_FOR_HUMAN
WAITING_FOR_HUMAN → RUNNING
RUNNING → NEEDS_REVISION
RUNNING → FAILED
RUNNING → COMPLETED
COMPLETED → RUNNING     (explicit resume only)
NEEDS_REVISION → RUNNING (explicit resume only)
FAILED → RUNNING        (explicit recovery action only)
```

`COMPLETED` is not permanently terminal when it represents a bounded scope. A completed bounded Run may be explicitly resumed as the same Run with a new Invocation.

### 6.2 Completion Scope

A bounded completion is represented as:

```text
state = COMPLETED
completion_reason = BOUNDED_SCOPE
execution_scope = <completed requested scope>
```

`COMPLETED` never by itself means “R0–R8 completed”. Consumers must inspect scope/completion metadata.

### 6.3 Failure Semantics

`FAILED` is used for execution/contract failures, including validation failures that prevent progression.

`NEEDS_REVISION` is reserved for an explicit Human Gate rejection/requested revision.

There is no automatic correction loop.

### 6.4 Control Actions

```text
start
resume
retry
rerun
--from Rn
--until Rn
Gate decision
```

Semantics:

- `retry`: retry within the same Attempt. It is explicit and never automatically scheduled.
- `rerun`: create a new Attempt for the same logical Step inside the current Invocation.
- `resume`: create a new Invocation for the same Run and continue from the Run's current durable state.
- `--from Rn`: create a new Invocation beginning at Rn using an exact-compatible checkpoint; rebuild the downstream execution path from Rn onward.
- `--until Rn`: create an invocation with a bounded target scope and complete when that scope is reached.

### 6.5 Revision Semantics

A rejected Gate persists:

```text
revision_target
├── entry_step
└── reason
```

`entry_step` is the minimum re-execution boundary. It is not a fixed list of steps.

The Runtime validates that the boundary is compatible with the Gate/Workflow dependency graph and then uses Workflow semantics to determine the downstream path.

A revision does not mutate old Attempt, Artifact, or Gate history.

---

## 7. Workflow and Executor Architecture

### 7.1 Standard Research Workflow

The Runtime consumes the formal, versioned Standard Research Workflow represented by Workflow Core.

It must not embed:

```python
if step_id == "R1": ...
elif step_id == "R2": ...
```

as the primary execution mechanism.

The workflow remains DAG-capable. Runtime v1 uses a single-process sequential scheduler, selecting executable nodes according to Workflow Core dependency semantics.

H2/H3/H4 remain Gate Barriers rather than ordinary Workflow Steps.

### 7.2 Executor Registry / Strategy

A Workflow Step declares an execution specification. The Runtime resolves that specification through an Executor Registry/Strategy.

Conceptually:

```text
WorkflowStep
     ↓ execution spec
Executor Registry
     ↓
Executor implementation
     ↓
Candidate / Artifact output
```

The Orchestrator is not allowed to become a table of step-specific executor logic.

Executor modes required for the Step 6 architecture are:

```text
deterministic
llm
source
human
composite
```

The synthetic E2E path uses deterministic fake Executors. Real DeepSeek execution is a separate adapter/smoke concern and is not part of the main regression suite.

### 7.3 Candidate Pipeline

A reusable execution path may follow:

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

Step completion requires both execution success and all required validation/acceptance conditions.

---

## 8. Source Acquisition

Source Acquisition happens before R1 and is a Runtime capability, not a new research lifecycle number.

Input is the Case's declared `inputs/urls.yaml`.

The service must:

1. validate declarations;
2. fetch declared URL(s);
3. preserve raw content where supported;
4. record retrieval metadata;
5. compute digest;
6. create a committed Source Artifact / acquisition record.

Rules:

- no autonomous source discovery;
- no undeclared URL fetches;
- required-source failure blocks research execution;
- optional-source failure is durable but non-blocking;
- unsupported or oversized acquisition is an explicit failure.

Source acquisition is Run-scoped immutable input. A successful Source Artifact is reused during `resume`, `retry`, and `rerun` in the same Run. A future new Run or explicit source-refresh capability may refetch; Step 6 does not invent source refresh semantics beyond this boundary.

The synthetic E2E uses a local HTTP test server so that source acquisition is semantically real but has no external internet dependency. Unit tests may mock the transport boundary.

---

## 9. Artifact Envelope and Persistence Contract

Every Runtime-managed Artifact uses a uniform envelope around a typed payload.

Conceptually:

```text
Artifact Envelope
├── artifact_id
├── run_id
├── invocation_id
├── step_id
├── attempt_id
├── created_at
├── artifact schema identity/version
├── digest
├── provenance metadata
└── typed payload reference
```

Runtime owns envelope identity, lineage, digest, persistence metadata, and artifact lifecycle. Payload semantics remain owned by the Executor or corresponding Core.

Artifact Envelope is not a Canonical domain schema.

### 9.1 Artifact Commit

Only a fully persisted Artifact is eligible for downstream Input Binding.

Commit ordering is:

```text
1. produce payload
2. write payload/envelope
3. complete digest and metadata
4. persist committed evidence
5. append ARTIFACT_COMMITTED event
6. append downstream success/disposition event
7. refresh run projection
```

A file left behind by a crashed process is not automatically a valid Artifact.

### 9.2 Uncommitted Residue

Uncommitted temporary output is execution residue. It must not be used as a downstream input and must not be treated as successful execution evidence.

---

## 10. Control Plane Event Model

`execution.jsonl` is the authoritative execution history.

Each event uses one lightweight common envelope:

```text
event_id
event_type
schema_version
timestamp
run_id
invocation_id?
step_id?
attempt_id?
artifact_id?
gate_id?
payload
```

Events record facts that have happened, not command intent.

Representative event types include:

```text
RUN_CREATED
INVOCATION_STARTED
ATTEMPT_CREATED
INPUT_BOUND
ATTEMPT_STARTED
ARTIFACT_COMMITTED
VALIDATION_COMPLETED
ACCEPTANCE_RECORDED
GATE_CREATED
GATE_DECIDED
GATE_SUPERSEDED
ATTEMPT_SUCCEEDED
ATTEMPT_FAILED
CHECKPOINT_CREATED
CHECKPOINT_INVALIDATED
CANONICAL_BINDING_PENDING
CANONICAL_BINDING_COMMITTED
SNAPSHOT_BOUND
INVOCATION_COMPLETED
RUN_STATE_CHANGED
```

The final implementation may combine some low-value transition records where a single authoritative event is sufficient, but it must preserve the logical facts needed to reconstruct Control Plane state.

Canonical Core's internal domain history is not copied wholesale into `execution.jsonl`. Runtime records only its execution binding/result facts.

### 10.1 Event Identity and Idempotency

Each Event has a unique immutable `event_id`.

Step 6 does not introduce a second `idempotency_key`.

Crash reconciliation must reuse the same `event_id` when reconstructing a single fact whose write outcome is uncertain. A previously persisted `event_id` is never appended again as a second logical fact.

### 10.2 Event Schema Versioning

Every Event has `schema_version`.

Step 6 supports the current version only. Unknown Event Schema versions fail fast during load/reconciliation. No migration framework is introduced in v1.

---

## 11. Run Projection and Crash Consistency

`run.json` is a current-state projection derived from `execution.jsonl` plus referenced durable evidence.

Core Run/Invocation/Attempt/Gate/Checkpoint/Snapshot-binding state must be reconstructible from authoritative history and evidence.

Purely derived/cache fields may exist, but they are not independent truth.

On Runtime startup:

```text
load execution.jsonl
      ↓
validate Event identities/schemas
      ↓
replay/reduce history
      ↓
verify referenced durable evidence
      ↓
reconcile incomplete facts
      ↓
rebuild/repair run.json projection
```

### 11.1 Crash Protocol

The core ordering is:

```text
Durable evidence
      ↓
Execution event
      ↓
State projection
```

A state transition must not claim success before the durable evidence supporting that success exists.

### 11.2 At-Least-Once Semantics

Step 6 provides:

```text
at-least-once execution
+
durable reconciliation
+
immutable artifacts/events
```

It does not claim exactly-once execution.

### 11.3 Stranded RUNNING Attempt

If startup finds an Attempt that was `RUNNING` but lacks verifiable durable completion evidence:

```text
Attempt → FAILED
failure disposition = EXECUTION_INTERRUPTED
```

The Runtime must not automatically rerun it.

If complete durable success evidence exists but an expected success event/projection update is missing, reconciliation may append the missing fact deterministically instead of re-executing the Executor.

---

## 12. Checkpoint and Compatibility Model

A Checkpoint is a durable set of Artifact references and metadata sufficient to establish a later Step's input context.

A Checkpoint never serializes Python process state.

A reusable checkpoint must satisfy exact compatibility of the relevant execution identities:

```text
Workflow identity/version
Step identity/version
Prompt identity/version (when applicable)
Schema identity/version
Runtime configuration identity
```

Compatibility is deliberately conservative and exact in Step 6. No fuzzy compatibility or semantic similarity checks are introduced.

When a logical Step is rerun, downstream checkpoints depending on its previous output are invalidated by default.

### 12.1 `--from`

`--from Rn` means:

```text
select exact-compatible checkpoint at Rn's input boundary
→ create new Invocation
→ execute Rn as a new Attempt
→ rebuild downstream path
→ create new derived Gates/Artifacts/Snapshot as required
```

It does not mean “skip prerequisites”.

The new path must not reuse dependent downstream checkpoints or the old Snapshot merely because they exist.

Checkpoint reuse is local; lineage is rebuilt downstream.

---

## 13. Human Gate Runtime

Human Gate records are immutable review facts.

Minimum semantics:

```text
gate_id
gate_type
run_id
logical gate identity
review target Artifact Set / Candidate Set
reviewer
created_at
decision
decided_at
comment/reason
revision_target? 
supersedes?
superseded_by?
```

### 13.1 Review Target

A Gate binds to the concrete Artifact/Candidate Set being reviewed, not merely to a Step or Attempt.

Step 6 Human Gate decision is whole-set:

```text
APPROVE
or
REJECT
```

Partial approval is out of scope.

### 13.2 Gate Supersession

Gate supersession is a lightweight generic Control Plane mechanism, not a separate subsystem.

When a new execution path creates a replacement Gate for a logical review point, Runtime records an immutable relationship:

```text
Gate #001
superseded_by → Gate #002

Gate #002
supersedes → Gate #001
```

Gate decision states remain simple:

```text
PENDING
APPROVED
REJECTED
```

Supersession is a relationship, not a new Gate state.

A Gate's approval is valid for progression only when its review target binding matches the current execution lineage and the Gate is not superseded by a newer path.

### 13.3 Revision Target

A rejected Gate may contain:

```text
revision_target
├── entry_step
└── reason
```

`entry_step` is the minimum re-execution boundary. Runtime validates it against Workflow dependency semantics but does not infer research impact from prose.

---

## 14. R4 / H3 / R5 and Snapshot Boundary

The semantic flow through the key knowledge boundary is:

```text
R4 working research artifacts
        ↓
H3 human judgment gate
        ↓
R5 synthesis / canonicalization
        ↓
Schema Validation
        ↓
Provenance Validation
        ↓
Canonical Domain Validation
        ↓
Acceptance
        ↓
Canonical Registry
        ↓
ResearchSnapshot
```

R4 does not directly emit authoritative Canonical objects.

### 14.1 R5 Acceptance / Canonical Registration Boundary

Runtime uses a lightweight two-phase boundary protocol:

```text
1. persist Canonical Binding Pending
2. call Canonical Core registration
3. persist Canonical Binding Committed
```

If the process crashes between these points, startup reconciliation must determine whether Canonical Core already registered the accepted candidate using the durable binding/evidence available through the public Core API.

Runtime must not inspect `_current`, `_states`, or other Canonical Registry internals.

### 14.2 ResearchSnapshot

ResearchSnapshot is created immediately after successful R5 acceptance and canonical registration.

Snapshot creation is:

```text
Runtime-managed
Knowledge-plane freeze operation
Not a Workflow Step
```

The Snapshot becomes the immutable freeze point for the accepted canonical state at that execution boundary.

Runtime stores only the snapshot reference/binding. Snapshot semantic ownership and persistence belong to Canonical Core. If the current Canonical Core lacks the necessary persistence API, implementation should record the API gap rather than bypassing Core encapsulation.

### 14.3 Snapshot Failure

If Canonical registration succeeds but Snapshot creation/binding fails:

```text
R5 Attempt = SUCCEEDED
Invocation = FAILED
Run = FAILED
```

The Runtime must retry/reconcile the Snapshot operation without rerunning R5 or registering the same canonical candidate a second time.

Old Snapshots are immutable and are never overwritten by a new execution path.

---

## 15. Invocation and Recovery Semantics

### 15.1 `retry`

`retry` is an explicit retry within the same Attempt and same Invocation.

The Attempt identity remains unchanged.

No automatic retry policy is run by the Runtime. The control action must be explicit.

### 15.2 `rerun`

`rerun` creates a new Attempt inside the current Invocation.

```text
Invocation #001
 ├── R3 Attempt #001
 └── R3 Attempt #002  ← rerun
```

The new Attempt receives a new explicit Input Binding. By default it inherits the prior logical input selection only when those concrete inputs remain valid; it never resolves an implicit “latest” artifact.

Downstream dependent checkpoints are invalidated and downstream Gates must be recreated for new review targets.

### 15.3 `resume`

`resume` creates a new Invocation for the same Run and continues from the current durable state.

Historical Invocation records are immutable.

A `COMPLETED` Run with bounded scope may be resumed explicitly to extend its scope. A `NEEDS_REVISION` Run may be resumed only after the revision target is explicit and validated.

### 15.4 `--from`

As specified in Section 12, `--from Rn` creates a new Invocation and rebuilds the downstream path from an exact-compatible checkpoint.

### 15.5 `--until`

`--until Rn` defines a bounded requested scope. When reached successfully:

```text
Invocation = SUCCEEDED
Run = COMPLETED
completion_reason = BOUNDED_SCOPE
```

No later lifecycle stages are implied by that state.

---

## 16. Case and Configuration Immutability

### 16.1 Run Case Binding

At Run creation, the Runtime binds the relevant Case Definition identities/digests. Later modifications to the Case do not mutate that Run.

### 16.2 Invocation Execution Binding

Each Invocation freezes:

```text
requested scope
entry mode
from/until boundary
Workflow identity/version
Prompt identities/digests
Schema identities/digests
Runtime configuration identity
```

A new Invocation can continue the same Run only if its execution configuration is compatible with the existing Run lineage.

A new Run is required when the requested change alters the Case Definition itself or creates an incompatible research/execution lineage that cannot be safely connected.

### 16.3 Compatibility Boundary

Compatibility is a deterministic validation operation. Runtime never silently “best effort” connects two incompatible execution contexts.

---

## 17. CLI Boundary

The CLI is a thin formal Runtime control surface.

It may expose:

```text
create/start
resume
retry
rerun
run-from / --from
run-until / --until
Gate decision
```

The CLI must delegate semantics to Runtime APIs. It must not contain the orchestration logic itself.

No administrative schema-migration CLI, autonomous repair CLI, browser-control CLI, or general research chat command is introduced in Step 6.

---

## 18. Persistence Versioning

### 18.1 Runtime Persistence Schema

Every independent Runtime persistence document carries:

```text
runtime_schema_version = 1
```

Nested objects do not repeat the same version field.

Unknown Runtime Persistence Schema versions fail fast.

Step 6 does not provide migration tooling or automatic persistence upgrades.

### 18.2 Event Schema

Each Event independently carries:

```text
schema_version = 1
```

Unknown Event schema versions fail fast.

### 18.3 Artifact / Domain Schema

Artifact payloads and domain objects retain their own schema/version contracts and are not conflated with Runtime Persistence Schema.

---

## 19. Synthetic Integration Fixture

The Step 6 E2E fixture must be small but semantically real.

It must not be a plumbing-only fixture in which R1–R5 merely echo strings.

Minimum semantic chain:

```text
Synthetic Source
    ↓
Evidence
    ↓
Claim / Relationship
    ↓
Analysis
    ↓
Human Judgment
    ↓
Canonicalization
    ↓
ResearchSnapshot
```

The fixture should use only the existing first-slice Canonical vocabulary:

```text
Entity
Claim
Evidence
Source
Unknown
Relationship
```

No new Canonical object type is introduced merely to make the synthetic fixture convenient. The purpose of the fixture is partly to probe whether existing vocabulary is sufficient for a genuinely end-to-end runtime execution.

R4 may produce working judgment-oriented research artifacts, but H3 is the boundary that permits R5 canonical entry. If the existing Canonical model exposes an architectural gap during implementation, the gap must be recorded explicitly rather than papered over with ad hoc Runtime-owned concepts.

---

## 20. Testing Strategy

The implementation plan must use TDD for each implementation task:

```text
write failing test
    ↓
verify failure
    ↓
implement minimum behavior
    ↓
run focused tests
    ↓
run relevant integration tests
    ↓
run regression suite
    ↓
commit
```

### 20.1 Unit Tests

Minimum unit coverage should include:

- domain model validation;
- Event schema parsing/version checks;
- Event idempotency;
- Run projection/reducer;
- Invocation immutability;
- Attempt transitions;
- explicit Input Binding persistence;
- Artifact commit rules;
- checkpoint compatibility;
- Gate target binding/supersession;
- revision target validation;
- Run state transitions;
- control action semantics.

### 20.2 Integration Tests

At minimum:

1. create a synthetic Case;
2. execute Source Acquisition using a local HTTP server;
3. execute the standard workflow through R5;
4. perform H2/H3 Gate decisions;
5. validate/accept R5 output;
6. register Canonical state through public APIs;
7. create and bind ResearchSnapshot;
8. complete bounded Run.

### 20.3 Recovery Tests

The test suite must exercise crash windows such as:

```text
before Artifact commit
Artifact committed before success event
success event before run projection
Canonical binding pending
Snapshot binding pending
RUNNING Attempt without completion evidence
```

Expected behavior is deterministic reconciliation without automatic business retry.

### 20.4 Control Action Tests

Explicitly test:

```text
retry
rerun
resume
--from
--until
NEEDS_REVISION → resume
COMPLETED bounded scope → resume
```

### 20.5 Regression Gate

The current repository regression baseline is:

```text
pytest --collect-only -q  → 191 tests
pytest -q                 → 191 passed
```

The final Step 6 implementation must preserve this baseline unless a reviewed test-count change is intentionally introduced by the implementation itself.

---

## 21. Package Boundary and Responsibility Proposal

The Runtime should be organized around stable responsibilities rather than one large orchestrator module. A likely logical layout is:

```text
src/ai_native_workbench/research/runtime/
├── domain/
│   ├── run.py
│   ├── invocation.py
│   ├── attempt.py
│   ├── artifact.py
│   ├── gate.py
│   ├── checkpoint.py
│   └── events.py
├── store/
│   ├── filesystem.py
│   ├── event_log.py
│   ├── projection.py
│   └── artifacts.py
├── execution/
│   ├── orchestrator.py
│   ├── executors.py
│   ├── registry.py
│   └── binding.py
├── source/
│   └── acquisition.py
├── gates/
│   └── runtime.py
├── snapshot/
│   └── binding.py
├── cli/
│   └── ...
└── reconciliation/
    └── ...
```

This is a responsibility guide, not a requirement that every filename must be implemented exactly this way. The implementation plan should follow existing repository conventions and split further only when a unit has a clear independent responsibility.

The critical boundary is that Runtime modules depend on Workflow/Canonical/Evaluation/Build public APIs rather than internal implementation details.

---

## 22. Key Architectural Invariants

The following invariants are non-negotiable for Step 6:

1. **Case is definition; Run is execution.**
2. **Run identity is stable across bounded continuation.**
3. **Invocation is an immutable execution request.**
4. **Attempt is a concrete Step execution and has only simple execution states.**
5. **Candidate/Validation/Acceptance are separate from Attempt state.**
6. **Artifact lineage is explicit and artifacts are immutable after commit.**
7. **Attempt Input Binding is durable before Attempt RUNNING.**
8. **No implicit “latest artifact” resolution.**
9. **Workflow Core owns graph semantics; Runtime owns execution state.**
10. **Executor resolution is registry/strategy based, not Step-ID hardcoded.**
11. **Human Gate is Control Plane state and binds to concrete reviewed targets.**
12. **Gate approvals apply only to their bound execution lineage.**
13. **Gate supersession is relational, not another Gate state.**
14. **Human rejection is the only source of `NEEDS_REVISION`.**
15. **No automatic retry/rerun/correction loop.**
16. **`execution.jsonl` is authoritative; `run.json` is rebuildable projection.**
17. **Success requires durable evidence before success state.**
18. **Crash reconciliation never silently re-executes business work.**
19. **Checkpoint reuse is exact and local; downstream lineage is rebuilt.**
20. **R5 canonical registration is the Knowledge Plane entry boundary.**
21. **ResearchSnapshot is an immutable freeze operation, not a Workflow Step.**
22. **Runtime does not access Canonical internals.**
23. **Bounded `COMPLETED` means completed requested scope, not necessarily complete lifecycle.**
24. **A new execution request creates a new Invocation.**
25. **New execution paths create new Gates/Artifacts rather than mutating historical records.**
26. **Step 6 optimizes for minimal sufficient engineering, not generic platform completeness.**

---

## 23. Risks and Mitigations

### Risk 1: Runtime becomes a second Workflow engine

**Mitigation:** consume Workflow Core definitions/dependencies; keep Runtime-specific concerns limited to execution, persistence, gates, lineage, and recovery.

### Risk 2: Control Plane becomes a hidden knowledge authority

**Mitigation:** Artifact payload semantics remain in Executors/Cores; Canonical Registry remains semantic authority; Snapshot ownership remains with Canonical Core.

### Risk 3: Crash recovery creates phantom success

**Mitigation:** durable evidence precedes success events and projections; incomplete residue is not an Artifact; reconciliation requires explicit evidence.

### Risk 4: New paths accidentally reuse old review decisions

**Mitigation:** Gate review target binding plus explicit supersession; new lineage creates new Gate Records.

### Risk 5: New paths accidentally reuse old downstream knowledge

**Mitigation:** exact checkpoint compatibility and downstream invalidation; `--from` rebuilds derived lineage and creates a new Snapshot.

### Risk 6: Invocation/Run state semantics become too complicated

**Mitigation:** keep Run states at six, Invocation states at three, and represent scope/disposition as explicit metadata instead of proliferating states.

### Risk 7: Synthetic E2E is too artificial to validate architecture

**Mitigation:** use semantically real Source → Evidence → Claim/Relationship → Analysis → human judgment → Canonicalization fixture while keeping transport and LLM deterministic/local.

### Risk 8: Step 6 expands into Step 7

**Mitigation:** stop the synthetic completion boundary at ResearchSnapshot; defer full Evaluation/Delivery/Archive validation and Case generalization to Step 7.

---

## 24. Deferred Questions for Later Versions

These are intentionally not solved in Step 6:

- runtime persistence migration framework;
- source refresh workflows;
- concurrent DAG scheduling;
- distributed execution;
- autonomous agent planning;
- generalized revision impact analysis;
- multi-provider failover;
- browser/MCP source acquisition;
- richer Gate workflows such as partial approval or multi-reviewer quorum;
- generalized Event Store infrastructure.

The absence of these features is a deliberate architectural choice, not an unresolved blocker.

---

## 25. Implementation Planning Boundary

The implementation plan created after this Spec is approved must decompose the Runtime into vertical, testable increments rather than attempting one giant implementation task.

The implementation plan should prioritize:

1. Runtime persistence/domain spine;
2. Event history and projection/reconciliation;
3. Executor/Input/Artifact protocol;
4. Workflow orchestration;
5. Source Acquisition;
6. Human Gate Runtime and revision/supersession semantics;
7. R5 Canonical boundary and Snapshot binding;
8. synthetic E2E completion and CLI control surface;
9. regression and recovery verification.

Each implementation task must preserve the invariants in Section 22 and follow the repository's TDD workflow.

---

## 26. Final Design Decision

The Step 6 Runtime is a **durable single-process Research Control Plane** around the existing Workflow, Canonical, Evaluation, and Build cores.

Its core execution identity is:

```text
Case
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
Gate Barrier when required
  ↓
Canonical Binding
  ↓
ResearchSnapshot
```

Its core audit identity is:

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

The architectural boundary is intentionally small:

> **The Runtime makes research execution durable and auditable; it does not become the research itself.**

Step 6 stops at a trustworthy ResearchSnapshot boundary. Step 7 validates the resulting Runtime against broader research cases and the remaining Evaluation/Delivery/Archive lifecycle.
