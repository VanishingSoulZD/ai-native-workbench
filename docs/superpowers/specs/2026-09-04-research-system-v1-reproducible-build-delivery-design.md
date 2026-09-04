# Research System v1 — Reproducible Build + Delivery Design

> **Status:** Approved design · Step 5 — Reproducible Build + Delivery  
> **Date:** 2026-09-04  
> **Repository:** `VanishingSoulZD/ai-native-workbench`  
> **Baseline:** `main@7cbdc31ab4242cc220c92aa9bf85fd284c927462`

## 0. Executive Summary

Step 5 establishes the minimum reusable **Reproducible Build + Delivery Core** for Research System v1.

Its purpose is to make the semantic boundary between canonical research knowledge and audience-specific delivery explicit and executable:

```text
ResearchSnapshot
      ↓
Canonical State Resolution
      ↓
Canonical Validation
      ↓
Evaluation Gate
      ↓
Build
      ↓
Projection
      ↓
Renderer
      ↓
Delivery Artifact
      ↓
Build / Audit Manifest
```

The central invariant is:

> **One Canonical Research State → Many Deliveries.**

Delivery artifacts are projections of canonical research knowledge. They are not independently authored research sources and must never become the source of truth for a later build.

Step 5 deliberately does **not** redesign the Step 3 canonical model, introduce a delivery management platform, or repair the Case 001 legacy pipeline. It establishes only enough deterministic transformation and rendering capability to prove that one historical canonical state can produce at least two meaningfully different delivery forms and that the process can be explained and repeated from declared inputs.

The first delivery pair is:

```text
Dataset Export
Research Note
```

This pair demonstrates a machine-oriented structured delivery and a human-oriented narrative delivery without requiring the visual/layout complexity of PPT or HTML in the first slice.

---

# 1. Problem

Research System v1 already provides three critical foundations:

1. **Canonical Knowledge + Provenance** — immutable canonical object states, typed `CanonicalRef`, deterministic fingerprints, and recoverable `ResearchSnapshot` state.
2. **Evaluation Core** — versioned evaluation rules, immutable evaluation runs/results, explicit human reviews, and quality-gate outcomes.
3. **System-level contracts** — canonical knowledge is the semantic authority and delivery is a projection rather than an alternative source of truth.

What is missing is a reusable build boundary that turns a declared historical research state into one or more deliveries without re-authoring research content.

The legacy Case 001 Phase 8 implementation demonstrates the practical need for such a boundary, but it remains case-specific and is intentionally not the implementation target for Step 5.

The Step 5 problem is therefore:

> Given an explicitly identified and evaluated `ResearchSnapshot`, build delivery-specific projections and render them into reusable artifacts while capturing enough metadata to explain exactly which canonical state, versions, configuration, assumptions, and delivery logic were used.

---

# 2. Goals

Step 5 must:

1. Consume an explicit `ResearchSnapshot`, never an implicit current Registry state.
2. Reuse Step 3 canonical identity, snapshot recovery, and validation semantics rather than introducing parallel semantic identity.
3. Reuse Step 4 Quality Gate semantics so a build cannot silently bypass required evaluation eligibility.
4. Define a narrow boundary between canonical state, delivery projection, and renderer implementation.
5. Support at least two materially different delivery forms from the same canonical snapshot.
6. Capture declared build inputs, versions, configuration, assumptions, and output metadata in a build manifest.
7. Make rebuild semantics explicit without requiring false byte-for-byte determinism.
8. Keep delivery edits outside the canonical authority boundary.
9. Prove the complete flow with synthetic, legally constructed canonical research data independent of Case 001.
10. Remain in-memory and standard-library based unless implementation evidence proves otherwise.

---

# 3. Non-Goals

Step 5 does not implement:

- Case 001 migration or legacy Phase 8 repair;
- PPT generation;
- HTML application infrastructure;
- artifact storage services;
- persistent build databases;
- distributed or asynchronous build execution;
- build queues or workflow orchestration platforms;
- build caching;
- plugin marketplaces;
- universal renderer registries;
- automatic semantic reconciliation from delivery back into canonical state;
- automatic human judgment;
- a new canonical knowledge schema;
- a new provenance/reference system;
- a generalized artifact lifecycle service;
- byte-for-byte reproducibility as a universal contract;
- delivery-side authoring as a canonicalization mechanism.

The first implementation should not create an abstraction merely because a future delivery type may eventually need it.

---

# 4. Existing Contracts Reused

## 4.1 Step 3 Canonical Knowledge

Step 5 consumes existing public Step 3 APIs:

```text
CanonicalRef
CanonicalRegistry
ResearchSnapshot
canonical_fingerprint()
canonical_serialize()
```

`CanonicalRef` remains the only typed reference form for canonical objects. Logical identity and historical state identity remain separate.

A build that requires a particular historical state must resolve members through:

```python
snapshot.resolve(registry, ref)
```

rather than:

```python
registry.get(ref)
```

The latter is explicitly a current-state lookup and therefore cannot be the basis of historical reproducibility.

## 4.2 Step 3 Snapshot Semantics

`ResearchSnapshot` already records:

```text
snapshot_id
case_id
cutoff
workflow_version
schema_version
transformation_version
configuration_hash
assumptions_hash
status
members[CanonicalRef → fingerprint]
```

Step 5 reuses these fields as declared state/version inputs. It must not duplicate them into a second snapshot/version system.

## 4.3 Step 4 Evaluation

Step 5 consumes the existing evaluation boundary rather than redefining it.

The build may require an externally supplied completed evaluation/gate outcome, or the Step 5 orchestration may invoke the existing Quality Gate after evaluating the target. In either case:

```text
Evaluation = assessment authority
Build = transformation authority
```

A build MUST NOT reinterpret evaluation results as canonical facts and MUST NOT silently bypass a declared blocking gate.

## 4.4 System Contract

The System Contract establishes:

```text
Canonical Model = semantic authority
Delivery = projection
Reproducibility = declared-state reconstructability
```

Step 5 implements these principles; it does not amend them.

---

# 5. Architectural Boundary

The v1 architecture is intentionally narrow:

```text
                 ResearchSnapshot
                        │
                        ▼
              Canonical State Resolver
                        │
                        ▼
                   Validation
                        │
                        ▼
                 Evaluation Gate
                        │
                        ▼
                      Build
                        │
                 ┌──────┴──────┐
                 ▼             ▼
        Dataset Projection   Note Projection
                 │             │
                 ▼             ▼
        Dataset Renderer   Markdown Renderer
                 │             │
                 ▼             ▼
        Delivery Artifact  Delivery Artifact
                 │             │
                 └──────┬──────┘
                        ▼
                  Build Manifest
                        │
                        ▼
                   Audit Manifest
```

Each layer has one responsibility.

### Canonical State Resolver

Resolves the exact canonical object states named by the snapshot.

It may validate and assemble a read-only view of the historical canonical state. It must not change canonical data.

### Validation

Uses Step 3 validation authority. Step 5 may call existing validation but does not create a competing canonical validation model.

### Evaluation Gate

Uses Step 4 Quality Gate semantics. The build may proceed only when the declared build policy considers the target eligible.

### Build

Owns build-level coordination and captures the declared inputs used for the transformation.

Build does not invent research semantics.

### Projection

Selects and organizes canonical information for a particular delivery purpose.

Projection may:

- select fields;
- group canonical objects;
- reorder information;
- omit information not required by the target audience;
- derive presentation-local structure that is mechanically computable from canonical state.

Projection must not:

- invent facts;
- invent scores or rankings;
- silently resolve Unknown into a confirmed value;
- silently promote hypotheses into established facts;
- replace a historical snapshot member with current Registry state;
- introduce untracked consequential judgments.

### Renderer

Serializes a projection into a concrete delivery form.

A renderer is a presentation/serialization concern, not a research reasoning engine.

A renderer must not inspect unrelated current Registry state to fill missing delivery information.

### Delivery Artifact

Represents the produced output and its relationship to the build manifest.

It does not become canonical semantic authority.

### Build / Audit Manifest

Explains what state and logic produced the delivery.

---

# 6. Build Model

The first implementation should use one build operation rather than a persistent BuildRun lifecycle.

Conceptually:

```python
build(
    snapshot=..., 
    delivery_spec=...,
    registry=...,
    evaluation_gate=...,
) -> DeliveryArtifact
```

The operation is synchronous and in-memory.

A later persistent BuildRun abstraction may be introduced only if actual cases demonstrate a need for execution history, resume, retry, queueing, or distributed execution. Step 5 v1 does not justify that infrastructure.

## 6.1 Build Input

The build input is the explicit combination of:

```text
ResearchSnapshot
CanonicalRegistry
Delivery specification
Evaluation eligibility
Declared configuration
Declared assumptions
Build implementation/projection/renderer versions
```

The Registry is a state resolver for the snapshot; the build must never treat the Registry's current state as the build target by itself.

## 6.2 Build Preconditions

Before rendering a delivery, the build must verify:

1. the snapshot is structurally valid and recoverable;
2. every required snapshot member can be resolved at its captured fingerprint;
3. the declared evaluation gate permits delivery;
4. the requested delivery specification is known and versioned;
5. all required configuration and assumptions are declared.

A precondition failure is a build failure, not a successful delivery with warnings hidden in the output.

## 6.3 Build Identity

Build identity has two layers.

### Semantic input identity

The build's semantic input identity is derived from:

```text
exact snapshot member state
workflow version
schema version
transformation version
configuration
assumptions
projection version
renderer version
delivery type
```

The implementation may represent this as a deterministic digest over a canonical build-input manifest.

### Run/output metadata

The following are audit metadata and do not change canonical research identity:

```text
build_id
created_at
output path/name
environment metadata when recorded
```

This distinction prevents timestamps and output filenames from accidentally changing the semantic identity of a build.

## 6.4 Snapshot Identity versus Build Identity

`ResearchSnapshot.snapshot_id` identifies the named research snapshot. It is not sufficient by itself to identify exact build input state.

The exact canonical state used by a build is represented through the snapshot's member fingerprints.

Therefore a build must record both:

```text
snapshot identity
exact snapshot member states
```

A build must not reconstruct state solely from `snapshot_id` if that would permit ambiguity about the historical member states.

---

# 7. Reproducibility Semantics

## 7.1 v1 Definition

A build is **reproducible** when the same declared canonical snapshot state, transformation and projection versions, renderer version, configuration, assumptions, and build inputs are sufficient to reconstruct an equivalent delivery without manually re-authoring research content.

The contract is about declared state and transformation semantics, not accidental runtime identity.

## 7.2 Equivalent Delivery

Equivalent delivery means the rebuilt output preserves the same canonical research meaning required by that delivery type, including:

- the same source canonical objects and state versions;
- the same factual content selected by the projection;
- the same explicit Unknown states and qualification semantics;
- the same provenance references where the delivery type exposes provenance;
- the same ordering/grouping semantics when those are declared by the projection;
- no additional untracked research facts or judgments.

Equivalent delivery does not require identical byte representation.

## 7.3 Byte-for-byte Identity

Byte-for-byte identity is **not** a mandatory v1 contract for all delivery types.

Differences may arise from:

- timestamps intentionally treated as metadata;
- file-container metadata;
- platform serialization differences;
- non-semantic formatting differences.

Where a delivery renderer can be made deterministically byte-stable at low cost, tests may assert exact output. Such determinism is a renderer property, not a system-wide prerequisite.

## 7.4 Required Rebuild Proof

The integration test suite must prove that:

```text
same snapshot
+ same versions
+ same configuration
+ same assumptions
+ same delivery specification
        ↓
rebuild
        ↓
equivalent semantic delivery
```

It must also prove the negative case:

```text
snapshot state changes
        ↓
build input identity changes
        ↓
new build must not silently reuse the old canonical state
```

---

# 8. Delivery Abstraction

The v1 delivery abstraction is intentionally minimal.

## 8.1 Delivery Specification

A delivery specification identifies:

```text
delivery_type
projection_version
renderer_version
```

It may also carry delivery-local configuration that is explicitly declared as part of the build input.

No global registry of every future renderer is required.

## 8.2 Delivery Artifact

The first implementation needs only enough structure to identify:

```text
artifact_id
delivery_type
build_id
manifest / metadata
payload or output reference
content_digest when practical
```

The artifact does not embed a duplicate canonical knowledge graph.

## 8.3 Projection Boundary

Projection is the only layer allowed to adapt canonical semantics to delivery-specific information shape.

A projection should be deterministic given:

```text
snapshot-resolved canonical state
projection version
explicit projection configuration
```

Projection must not perform network retrieval, model inference, or hidden external lookups in v1.

---

# 9. First Delivery Forms

## 9.1 Dataset Export

The first dataset delivery is a machine-oriented projection.

Its purpose is to prove that canonical objects can be flattened into a structured reusable representation while preserving stable identifiers and provenance links.

The first implementation may use JSON or CSV depending on the simplest stable representation supported by the chosen synthetic case. The format must be declared in the Delivery Specification and included in the build manifest.

The dataset projection should preserve, at minimum where applicable:

```text
CanonicalRef
logical IDs
object type
selected semantic fields
provenance references
Unknown state markers
```

It must not invent fields that imply unsupported semantics.

## 9.2 Research Note

The first note delivery is a human-oriented narrative projection rendered as Markdown.

The first implementation should use a small deterministic structure such as:

```text
Research context
Key findings
Evidence-backed claims
Unknowns / limitations
Provenance references
```

The exact section layout belongs to the Note Projection, not the canonical model.

The Note Renderer must format already projected content. It must not independently decide what the research concludes.

## 9.3 Deferred Visual Deliveries

PPT and HTML remain important later delivery forms, but they are deliberately deferred from the first implementation slice so that Step 5 can first prove the semantic build boundary without coupling correctness to layout and browser/presentation infrastructure.

Their later implementation should consume the same canonical state and follow the same projection/renderer boundary.

---

# 10. Build Manifest

The build manifest is the minimum v1 audit record explaining how an artifact was generated.

It should contain:

```yaml
build_id
created_at

snapshot:
  snapshot_id
  case_id
  cutoff
  member_fingerprints

versions:
  workflow_version
  schema_version
  transformation_version
  projection_version
  renderer_version

delivery:
  delivery_type
  format
  artifact_id

configuration: ...
assumptions: ...

evaluation:
  gate_id
  gate_version
  outcome
  run_id

build_input_digest
artifact_digest?
```

### Required semantics

`member_fingerprints` must come from the actual snapshot used for the build.

`configuration` and `assumptions` must be explicit. If they are hashed for identity purposes, the raw values need not always be embedded in the artifact, but the manifest must make clear what was declared and how it is identified. A future privacy-sensitive implementation may store only references/digests; v1 need not introduce secret management.

The manifest is explanatory metadata. It is not canonical research content.

---

# 11. Audit / Validation Package

The first audit package is intentionally a manifest-oriented package rather than an artifact-management subsystem.

Conceptually it contains:

```text
Build Manifest
Snapshot Manifest
Evaluation Summary
Delivery Manifest
```

The v1 implementation may emit a single audit manifest if that is sufficient to explain the build. Splitting it into multiple files is a presentation/packaging choice, not a semantic requirement.

The audit boundary must allow a reviewer to answer:

1. Which research snapshot was used?
2. Which exact canonical states were used?
3. Which workflow/schema/transformation/projection/renderer versions were used?
4. Which configuration and assumptions were declared?
5. Which evaluation gate authorized delivery?
6. Which delivery artifact was produced?
7. Can the same declared state be rebuilt?

It does not need to provide a database, searchable registry, or long-term artifact storage service.

---

# 12. Human Editing Boundary

Human editing of a delivery is allowed as a communication activity but is outside the canonical build source of truth.

The relationship is:

```text
Canonical State
      ↓
Build
      ↓
Delivery Artifact
      ↓
Human Editing
      ↓
Edited Communication Artifact
```

A human edit to a delivery:

- does not mutate the canonical registry;
- does not modify the historical snapshot;
- does not become implicit input to a later build;
- does not retroactively change the build manifest;
- does not create a new canonical claim merely because text was added to a delivery.

A future process may support explicit correction back into research, but that would be a new versioned research action governed by the canonical/human-gate model. Step 5 does not implement automatic back-propagation.

This preserves the authority rule:

> **Delivery artifacts are write-only projections with respect to canonical knowledge.**

---

# 13. Error / Failure Semantics

Step 5 failures must remain explicit.

Minimum semantic failure categories are:

```text
Snapshot Resolution Failure
Validation Failure
Evaluation Gate Block
Projection Failure
Renderer Failure
Manifest / Identity Failure
Build Configuration Failure
```

The implementation may use one build-specific exception hierarchy with typed subclasses.

## 13.1 Validation Failure

The canonical validation authority rejected the snapshot or its recoverability.

No delivery should be emitted as successful output.

## 13.2 Evaluation Gate Block

The evaluation layer has determined that process eligibility is not satisfied.

The build must not convert `REVIEW` or `FAIL` into success merely because rendering is technically possible.

## 13.3 Projection Failure

The delivery-specific projection could not produce a valid delivery view from the declared canonical state.

This is a build failure, not a canonical knowledge failure.

## 13.4 Renderer Failure

The projection is valid but concrete serialization failed.

This is a delivery/build failure and must not mutate canonical or evaluation state.

## 13.5 Manifest / Identity Failure

The build cannot prove what inputs or versions were used.

The artifact must not be marked as a successful reproducible build.

## 13.6 Partial Outputs

The first implementation should prefer atomic success semantics for each delivery:

```text
success → artifact + manifest
failure → no successful artifact declaration
```

Intermediate files may exist in a local working directory but must not be reported as valid delivery artifacts.

---

# 14. Evaluation Gate Interaction

The build and evaluation layers remain distinct:

```text
Canonical State
      ↓
Validation
      ↓
Evaluation
      ↓
Quality Gate
      ↓
Build Eligibility
```

The build does not reinterpret a Quality Gate result.

The minimum rule is:

```text
PASS → eligible
REVIEW → blocked pending required action
FAIL → blocked
```

For delivery-specific evaluation, the build may consume a gate targeted at that delivery after projection. This does not change the underlying canonical authority model; it only means that delivery correctness can itself be assessed before release.

A future implementation may support:

```text
Snapshot Gate → Build
Delivery Evaluation → Final Delivery Gate
```

but Step 5 v1 should implement only the minimum gate interaction required by the selected delivery workflows.

---

# 15. Versioning Rules

The following version domains are distinct:

```text
Workflow Version
Schema Version
Transformation Version
Projection Version
Renderer Version
```

### Workflow Version

Inherited from `ResearchSnapshot` and identifies reusable workflow behavior that produced the state.

### Schema Version

Inherited from `ResearchSnapshot` and identifies canonical field semantics.

### Transformation Version

Inherited from `ResearchSnapshot` and identifies the canonical transformation state already captured by Step 3.

### Projection Version

Owned by the delivery-specific projection. Material semantic changes to the projection require a new version.

### Renderer Version

Owned by the concrete renderer. Formatting-only changes may require a new version when they can affect output semantics or reproducibility expectations; purely internal refactors that do not affect output may retain the same version when verified.

Step 5 must not create a second canonical schema/version namespace merely for delivery.

---

# 16. Deterministic Software Responsibilities

Step 5 follows the system division of responsibilities.

Deterministic software owns:

```text
Snapshot resolution
Validation invocation
Build orchestration
Projection transformation
Normalization
Identifier preservation
Rendering
Manifest generation
Digest calculation
```

Human remains responsible for:

```text
research scope
consequential judgment
decision
final communication approval
historical correction
```

AI assistance may be used around the system, but Step 5 core build behavior must remain deterministic and auditable in v1.

---

# 17. Test Strategy

Testing must prove boundaries, not merely successful file creation.

## 17.1 Contract Tests

Prove:

- build contracts reject missing required inputs;
- build metadata is immutable where required;
- delivery specifications require explicit versions;
- manifests preserve exact snapshot member fingerprints;
- content digests are deterministic where supported.

## 17.2 Snapshot Binding Tests

Prove:

```text
snapshot captures claim v1
registry current becomes claim v2
build resolves v1
```

and not v2.

## 17.3 Authority Boundary Tests

Prove that:

- renderers cannot mutate the canonical registry through normal interfaces;
- projection does not become a canonical writer;
- delivery artifacts do not feed the next build as canonical state;
- Unknown remains Unknown rather than becoming `No`, `False`, `0`, or another inferred value;
- historical state remains stable after later registry replacement.

## 17.4 Gate Tests

Prove that:

- an evaluation `PASS` permits build;
- `REVIEW` blocks build;
- `FAIL` blocks build;
- evaluator execution failure does not become a successful build gate.

## 17.5 Projection Tests

Prove that each projection:

- consumes only explicit canonical state;
- preserves stable identity where relevant;
- preserves required provenance references;
- is deterministic for the same input;
- does not introduce untracked research facts.

## 17.6 Renderer Tests

Prove that renderers:

- produce the declared format;
- fail explicitly on invalid projection input;
- do not perform hidden semantic lookups;
- preserve required delivery content and provenance references.

## 17.7 Reproducibility Integration Test

One synthetic snapshot must generate both:

```text
Dataset
Research Note
```

Then the same snapshot/configuration/version set must rebuild each delivery and produce semantically equivalent results.

The test must also demonstrate that changing canonical state changes the build input identity.

## 17.8 Global Verification

The final Step 5 implementation must pass:

```bash
pytest tests/unit/research/build -q
pytest tests/unit/research/canonical -q
pytest tests/unit/research/evaluation -q
pytest tests/integration/research/build -q
pytest -q
```

The exact command set may be adjusted if the final repository structure differs, but the global suite remains mandatory.

---

# 18. Proposed Implementation Boundary

The initial implementation is expected to add a focused `research.build` package. The exact file split should follow actual code complexity, but the conceptual responsibilities are:

```text
research/build/
├── model          # immutable build/delivery contracts
├── errors         # build-specific exceptions
├── engine         # build orchestration and input binding
├── projection     # delivery-specific transformations
└── renderers      # minimal concrete renderers
```

The implementation should resist creating a class for every conceptual noun. In particular, do **not** create all of the following merely because they are named in architectural discussion:

```text
BuildInput
BuildRun
DeliverySpec
ProjectionRegistry
RendererRegistry
ArtifactRegistry
```

Only abstractions that are required by the final tested boundary should be implemented.

The strongest v1 candidates are:

```text
BuildManifest
DeliverySpec
DeliveryArtifact
Projection boundary
Renderer boundary
```

`BuildRun` is intentionally deferred.

---

# 19. Synthetic Validation Scenario

Step 5 integration tests must use a small legal canonical research scenario constructed entirely from literals.

The scenario should include at minimum:

```text
Source
Entity
Evidence
supported factual Claim
Unknown
ResearchSnapshot
```

A second historical state should be introduced for at least one canonical object to prove that builds remain snapshot-bound.

The scenario must be independent of:

```text
cases/001-ai-coding-agent-landscape/
```

and must pass Step 3 validation before it is used for build tests.

The synthetic scenario should support both delivery projections without requiring Case 001-specific fields.

---

# 20. Exit Criteria

Step 5 is complete when all of the following are demonstrated:

### A. Canonical authority preserved

The build reads canonical knowledge from an explicit `ResearchSnapshot` and never makes a delivery artifact the semantic source of truth.

### B. Historical snapshot correctness

A later Registry replacement does not change the canonical state used by a build for an existing snapshot.

### C. Evaluation boundary respected

A declared Quality Gate controls build eligibility and the build cannot turn `REVIEW` or `FAIL` into successful delivery.

### D. Two delivery forms

The same canonical snapshot produces at least:

```text
Dataset
Research Note
```

through separate projections from the same state.

### E. No manual re-authoring

The deliveries can be reconstructed entirely from declared canonical/build inputs. No copying from one delivery into another is required.

### F. Reproducibility manifest

Each successful delivery is accompanied by enough metadata to identify:

```text
snapshot
member fingerprints
workflow/schema/transformation versions
projection/renderer versions
configuration
assumptions
evaluation gate
build identity
```

### G. Rebuild proof

The same declared state can regenerate semantically equivalent deliveries.

### H. Failure transparency

Snapshot, evaluation, projection, renderer, and manifest failures are distinguishable and do not masquerade as successful research output.

### I. No Step 1–4 semantic regression

Existing canonical and evaluation tests remain green, and Step 5 requires no change to Step 3 canonical semantics.

---

# 21. Explicit Architectural Constraints

The following constraints are part of the Step 5 design contract:

1. **Canonical Research Model is the authority.**
2. **`ResearchSnapshot` is the explicit build state boundary.**
3. **Snapshot members must be resolved by historical fingerprint, not current Registry state.**
4. **Evaluation remains assessment; Build remains transformation.**
5. **Projection is allowed to select and reorganize semantics but not invent research facts.**
6. **Renderer is serialization/presentation, not reasoning.**
7. **Delivery artifacts cannot become future canonical build inputs implicitly.**
8. **Human-edited delivery content remains outside canonical authority unless a separate explicit research correction/versioning process occurs.**
9. **Reproducibility means equivalent reconstruction from declared state, not universal byte identity.**
10. **Version fields already defined by Step 3 are reused rather than duplicated.**
11. **Build identity must distinguish logical snapshot identity from exact canonical member state.**
12. **No persistent/distributed build infrastructure is justified in v1.**
13. **No Case 001-specific field or phase name may become a shared build interface.**
14. **Audit packaging remains manifest-oriented and minimal.**
15. **No future renderer or artifact framework is created unless implementation evidence requires it.**

---

# 22. Open-but-Bounded Implementation Decisions

The following decisions are intentionally left to the implementation plan because they depend on the smallest tested representation:

1. Whether the first Dataset Renderer uses JSON or CSV.
2. Whether the build manifest is represented as one object or split into smaller manifest records.
3. Whether `DeliveryArtifact` stores an in-memory payload, a path, or both in the first slice.
4. The exact Python module split inside `research.build`.

These are implementation details. They must not change the architectural boundaries above.

---

# 23. Summary

The Step 5 foundation is deliberately small:

```text
ResearchSnapshot
      ↓
Validation
      ↓
Evaluation Gate
      ↓
Build
      ↓
Projection
      ↓
Renderer
      ↓
DeliveryArtifact
      ↓
Build Manifest / Audit
```

The system does not attempt to make delivery itself intelligent. It establishes a trustworthy projection boundary so that one canonical research state can be communicated in multiple forms without fragmenting semantic authority.

The intended result is not a general artifact platform. It is a small, testable capability that makes the following statement true:

> **One Canonical Research State can generate many explainable, reproducible delivery projections without manually re-authoring the research content.**
