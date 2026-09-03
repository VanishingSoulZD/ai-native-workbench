# Research System v1 — System Contract Design

> Status: **Approved design / Step 1 — System Contract**
>
> Date: 2026-09-03
>
> Repository: `VanishingSoulZD/ai-native-workbench`
>
> Scope: Freeze the minimum reusable system contract for Research System v1 before implementation. This document is intentionally independent of Case 001's historical phase/file layout and does not define runtime infrastructure or agent architecture.

---

## 0. Executive Summary

Research System v1 is a Human-in-the-loop, Evidence-first, Evaluation-driven research system.

Its core architecture is:

```text
Research Definition
        ↓
Workflow Execution
        ↓
Research Artifacts
        ↓
Canonical Semantic Model
        ↓
Evaluation + Human Gates
        ↓
Research Snapshot
        ↓
Delivery Projections
```

The system freezes three boundaries:

1. **Workflow is the execution contract; Prompt is only an execution detail.**
2. **Canonical objects are semantic authority; artifacts are research work carriers.**
3. **Deliveries are projections; they cannot silently become sources of truth.**

Case 001 remains a Reference / Legacy Research Case. Its phase-based files and its Phase 8 canonical model are historical instantiated artifacts, not system-level interfaces.

---

# 1. Contract Philosophy

## 1.1 System principles

### Workflow before Agent

The reusable execution unit is a `WorkflowStep`, not a prompt and not a lifecycle phase. A step must expose stable inputs, outputs, constraints, validation and human-gate requirements independently of whether it is executed by a prompt, code, CLI, tool call, human interaction or future agent.

### Canonical Knowledge before Rendering

The semantic center is the Canonical Research Model. Research Notes, HTML, PPT and Dataset outputs are projections of canonical knowledge. They must not introduce untracked facts, scores, rankings or judgments.

### Evaluation before Automation

A workflow capability should be evaluated before its automation is expanded. Automation is not considered successful merely because it reduces human effort; reliability, failure modes and validation must be understood.

### Evidence before Assertion

Externally verifiable claims require explicit provenance. Unsupported certainty is a quality defect.

### Human authority around automation

AI may assist discovery, extraction, comparison, drafting, scoring proposals and recommendations. It does not silently acquire authority over consequential scope, selection, judgment, decision, final delivery or historical correction.

### Reproducibility without false determinism

Reproducibility means the research state can be reconstructed and explained from declared versions, inputs, assumptions, configuration and provenance. It does not require identical byte-for-byte model output.

### Minimal sufficient engineering

Research System v1 freezes semantic and process contracts, not future infrastructure. Databases, vector stores, MCP servers, distributed workers, event buses, autonomous browsers and multi-agent runtimes are outside this contract unless later evidence establishes a need.

---

# 2. Core Objects

## 2.1 Definition objects

### ResearchRequest

**Definition**: The incoming statement of why research is needed.

**Problem solved**: Preserves decision context and the original intent before scope is narrowed.

**Created by**: Human requester, stakeholder, or upstream system.

**Content authority**: Owns request intent and context only; it does not own final research scope.

**Who may modify**: Human authority. Superseding a request creates a new request/version rather than rewriting history.

**Consumers**: Research Charter.

**Minimum fields**:

```yaml
id
request
title
decision_context
requester
created_at
status
```

**Valid states**:

```text
draft
accepted
superseded
```

**Invalid states**:

- accepted request without requester or creation timestamp;
- using the request as authority for scope after a Charter has been approved.

**Relationships**:

```text
ResearchRequest 1 → 1..n ResearchCharter
```

---

### ResearchCharter

**Definition**: The approved formal definition of a research case's scope and success conditions.

**Problem solved**: Makes scope, research unit, exclusions, cutoff and success criteria explicit.

**Created by**: Human researcher with AI assistance permitted.

**Content authority**: Scope, exclusions, research unit, cutoff/snapshot definition, assumptions and success criteria.

**Who may modify**: Human authority. Material scope changes require a new version and may require a new snapshot.

**Consumers**: ResearchCase, ResearchQuestion, workflow planning and evaluation.

**Minimum fields**:

```yaml
charter_id
request_id
objective
scope
exclusions
research_unit
cutoff
success_criteria
assumptions
version
status
```

**Valid states**:

```text
draft
under_review
approved
superseded
```

**Invalid states**:

- approved Charter with undefined scope or research unit;
- approved Charter whose success criteria cannot be evaluated in principle;
- silently changing an approved scope without a versioned action.

---

### ResearchCase

**Definition**: A named research instance governed by a Charter.

**Problem solved**: Gives one research effort a stable identity and lifecycle independent of individual artifacts.

**Created by**: Human researcher or controlled workflow.

**Content authority**: Case identity, ownership and lifecycle status.

**Who may modify**: Human/system according to lifecycle permissions; historical identity is immutable.

**Consumers**: Questions, Snapshots, Workflow execution and Deliveries.

**Minimum fields**:

```yaml
case_id
title
charter_id
owner
status
created_at
```

**Valid states**:

```text
draft
active
evaluating
completed
archived
```

**Invalid states**:

- case without a valid Charter reference;
- duplicate case identifier;
- completed case with no valid completed snapshot.

**Relationships**:

```text
ResearchCase 1 → 1 Charter
ResearchCase 1 → n ResearchQuestion
ResearchCase 1 → n ResearchSnapshot
```

---

### ResearchQuestion

**Definition**: An answerable research question belonging to a Case.

**Problem solved**: Decomposes broad research intent into explicit units of inquiry.

**Created by**: Human researcher, with AI assistance permitted.

**Content authority**: Question wording, priority, acceptance criteria and status.

**Who may modify**: Human authority while the case is active; approved historical questions require versioning.

**Consumers**: Workflow, Claims, Analysis, Evaluation and Delivery.

**Minimum fields**:

```yaml
question_id
case_id
question
type
priority
acceptance_criteria
status
```

**Valid states**:

```text
draft
active
answered
unresolved
superseded
```

**Invalid states**:

- question without a case reference;
- answered question with no traceable supporting knowledge or explicit unresolved status.

---

### ResearchSnapshot

**Definition**: A versioned, point-in-time research state for a Case.

**Problem solved**: Provides the historical boundary for what the research knew, assumed and produced at a specific cutoff and version context.

**Created by**: Workflow execution under the ResearchCase; publication requires human authority.

**Content authority**: Snapshot membership, version boundary and historical state.

**Who may modify**: Draft snapshots may be edited under workflow rules. Validated/published/superseded/archived snapshots are immutable by default; corrections create a new versioned action and normally a new snapshot.

**Consumers**: Canonical Model, Evaluation, Delivery, Update workflows and Audit.

**Minimum fields**:

```yaml
snapshot_id
case_id
parent_snapshot_id?
cutoff
created_at
workflow_version
schema_version
transformation_version
configuration_hash
assumptions_hash
status
```

**Valid states**:

```text
draft
under_review
validated
published
superseded
archived
```

**Invalid states**:

- published snapshot whose version context is unknown;
- silent mutation of historical snapshot content;
- snapshot referencing artifacts outside its declared version context without explanation.

**Relationships**:

```text
ResearchSnapshot 1 → n ResearchArtifact
ResearchSnapshot 1 → n Canonical Objects
ResearchSnapshot n → 1 ResearchCase
```

---

## 2.2 Execution object

### WorkflowStep

**Definition**: A reusable unit of research work with a stable interface and explicit constraints.

**Problem solved**: Replaces prompt-dependent procedures with composable, evaluable execution contracts.

**Created by**: Research system maintainer / capability owner.

**Content authority**: Owns its contract, method, constraints, validation and declared gate/provenance rules.

**Who may modify**: Capability owner/version maintainer. Material changes require a new WorkflowStep version.

**Consumers**: Workflow composition, execution runtime, evaluation and capability registry.

**Minimum fields**:

```yaml
id
name
version
purpose
inputs[]
outputs[]
preconditions[]
method[]
constraints[]
human_gate
validation[]
provenance
```

**Valid states**:

```text
draft
validated
active
deprecated
retired
```

**Invalid states**:

- step with ambiguous or unnamed inputs/outputs;
- step whose mandatory constraints cannot be evaluated;
- active step with materially changed semantics but no new version.

**Composition**:

Workflow is a directed composition of steps. A step may consume outputs from upstream steps and produce one or more artifacts/canonical changes. The core contract does not require a specific runtime or orchestration technology.

**Prompt position**:

```text
WorkflowStep Contract
        ↓
Execution Method
        ↓
Prompt / Code / Tool / Human Interaction
```

A prompt is never the public workflow interface.

**Promotion to reusable Workflow Capability**:

A Case-specific procedure may be promoted when all of the following hold:

1. it solves a recurring problem across cases or is demonstrably domain-independent;
2. its inputs and outputs can be named;
3. its quality can be evaluated;
4. its important failure modes are sufficiently understood for reuse.

As an additional default safeguard, promotion should be supported by two independent research cases or by a clear proof of domain-independence.

---

## 2.3 Artifact object

### ResearchArtifact

**Definition**: A durable research work product carrying definitions, working material, canonical representations, evaluation results or delivery output.

**Problem solved**: Preserves research work without confusing file/artifact identity with semantic authority.

**Created by**: Human or workflow execution.

**Content authority**: The artifact owns its representation and version metadata. It does not automatically own the semantics of canonical objects it contains.

**Who may modify**: According to artifact lifecycle and owner. Historical published artifacts are versioned rather than silently overwritten.

**Consumers**: Workflow steps, evaluators, canonical loaders, reviewers and delivery renderers.

**Minimum fields**:

```yaml
artifact_id
case_id
snapshot_id
artifact_type
title
content_uri
created_by
created_at
workflow_step_id?
version
status
```

**Artifact classes**:

```text
definition
working
canonical
evaluation
delivery
```

**Valid states**:

```text
draft
active
superseded
archived
```

**Invalid states**:

- artifact without a declared class;
- delivery artifact used as semantic authority when canonical objects exist;
- historical artifact silently replaced without a new version.

**Core authority rule**:

> Artifacts carry research work; canonical objects carry semantic authority.

A Markdown document may contain a Claim, Evidence or Judgment, but the document filename/path is not the semantic identifier of that object.

---

## 2.4 Canonical semantic objects

### Entity

Represents a research subject.

**Created by**: Workflow or researcher during research execution.

**Authority**: Canonical semantic state of the represented subject within a Snapshot.

**Consumers**: Claims, Relationships, Metrics, Scores, Analysis and Delivery.

**Minimum fields**:

```yaml
entity_id
entity_type
name
status
attributes
```

`entity_type` remains extensible. Domain-specific taxonomies are not frozen globally in v1.

---

### Claim

Represents an atomic assertion carried by the canonical model.

**Created by**: Evidence/analysis workflow with researcher oversight as required.

**Authority**: Statement, status, confidence and evidence bindings.

**Consumers**: Analysis, Judgment, Evaluation and Delivery.

**Minimum fields**:

```yaml
claim_id
statement
subject_ref
claim_type
status
confidence
evidence_ids[]
```

A factual claim without required provenance is invalid.

---

### Evidence

Represents an observed or extracted piece of support/challenge.

**Created by**: Evidence collection/normalization workflow or researcher.

**Authority**: Observation and its provenance binding; not the truth of the resulting claim.

**Consumers**: Claims, Analysis, Evaluation and Audit.

**Minimum fields**:

```yaml
evidence_id
source_id
observation
date_or_period
evidence_type
evidence_grade
supports_claim_ids[]
contradicts_claim_ids[]
note
```

Evidence is not itself a conclusion.

---

### Source

Represents a citable information source.

**Created by**: Researcher or evidence workflow.

**Authority**: Source identity and citation metadata.

**Consumers**: Evidence, Claims, Audit and Delivery.

**Minimum fields**:

```yaml
source_id
canonical_title
publisher
canonical_url
source_type
published_at
accessed_at
quality_tier
```

A Source may point to an original document, official page, dataset, study, vendor publication or other citable source type.

---

### Analysis

Represents an explicit transformation of evidence/claims into comparison, model, inference or structured reasoning.

**Created by**: Researcher or workflow.

**Authority**: The declared analytical method and resulting analysis statement/model.

**Consumers**: Judgment, Recommendation, Decision and Delivery.

**Minimum fields**:

```yaml
analysis_id
statement_or_model
input_refs[]
method
assumptions[]
limitations[]
status
```

Analysis must remain distinguishable from externally verified fact.

---

### Relationship

Represents a typed relation between canonical objects.

**Created by**: Researcher or workflow.

**Authority**: Relationship predicate and endpoint references.

**Minimum fields**:

```yaml
relationship_id
subject_ref
predicate
object_ref
evidence_ids[]
status
```

---

### Metric

Defines a quantitative measure.

**Created by**: Researcher / methodology owner.

**Authority**: Definition, unit, method and qualifier semantics.

**Minimum fields**:

```yaml
metric_id
name
definition
unit
method
source_refs[]
qualifiers[]
```

---

### Score

Represents a value assigned to an object under a specific Metric in a Snapshot.

**Created by**: Scoring workflow / researcher.

**Authority**: Historical scored value within its Snapshot and declared Metric.

**Minimum fields**:

```yaml
score_id
subject_ref
metric_id
value
qualifier
method
evidence_ids[]
snapshot_id
```

Historical scores are read-only records within a Snapshot unless a versioned human-approved correction creates a new state.

---

## 2.5 Judgment and decision objects

### Judgment

Represents a synthesized research judgment.

**Created by**: Researcher with AI assistance permitted.

**Authority**: The research judgment and its declared basis, not the underlying factual sources.

**Consumers**: Decision, Recommendation, Delivery and Evaluation.

**Minimum fields**:

```yaml
judgment_id
statement
basis_refs[]
confidence
author
authority
status
```

Judgment requires an explicit basis chain to supporting analysis/claims/evidence where applicable.

---

### Recommendation

Represents a proposed action or preference.

**Created by**: Human or AI-assisted workflow.

**Authority**: Recommendation text and basis; not final action authority.

**Consumers**: Decision, Delivery and Human Gate review.

**Minimum fields**:

```yaml
recommendation_id
statement
basis_refs[]
confidence
status
```

Recommendation may be AI-generated. It is not a decision.

---

### Decision

Represents an authoritative choice with consequences.

**Created by**: Human decision authority, possibly assisted by AI-generated analysis/recommendations.

**Authority**: Designated human authority.

**Consumers**: Delivery, downstream case execution and audit.

**Minimum fields**:

```yaml
decision_id
statement
options[]
selected_option
rationale_refs[]
authority
status
```

Decision authority belongs to the designated human authority unless a future system explicitly establishes a different approved authority model.

---

### Hypothesis

Represents an unconfirmed explanatory proposition.

**Created by**: Human or AI-assisted analysis workflow.

**Authority**: Hypothesis state only; it is not factual authority.

**Consumers**: Future research questions, Analysis, Delivery and Evaluation.

**Minimum fields**:

```yaml
hypothesis_id
statement
basis_refs[]
confidence
testability
status
```

A hypothesis must not be rendered as an established fact.

---

### Unknown

Represents a material unresolved research state.

**Created by**: Human or workflow when evidence is insufficient, ambiguous or unavailable.

**Authority**: The unresolved state of the specified question/scope.

**Consumers**: Evaluation, Decision, Delivery and Update workflows.

**Minimum fields**:

```yaml
unknown_id
question
why_it_matters
scope
status
```

**Semantic rule**:

```text
Unknown ≠ No
Unknown ≠ False
Unknown ≠ 0
Unknown ≠ Empty
Unknown ≠ Not Applicable
```

Unknown is not a null formatting convention. It is a first-class knowledge state that must survive canonicalization and delivery.

---

## 2.6 Operational / governance objects

### Evaluation

**Definition**: A structured assessment of a research artifact, canonical snapshot, workflow or delivery against declared quality criteria.

**Problem solved**: Makes research quality itself inspectable and reusable.

**Created by**: Evaluator workflow and/or human reviewer.

**Content authority**: The recorded evaluation result and its evaluation context; it does not alter the evaluated research state.

**Who may modify**: Evaluator/reviewer through a versioned evaluation record.

**Consumers**: ResearchCase lifecycle, workflow promotion, delivery gating and audit.

**Minimum fields**:

```yaml
evaluation_id
target_ref
evaluation_type
criteria
results
status
evaluator
created_at
```

**Valid states**:

```text
draft
in_progress
passed
failed
superseded
```

**Invalid states**:

- passed evaluation without results against declared criteria;
- evaluation whose target cannot be resolved;
- modifying a historical passed evaluation without a new version.

---

### HumanGate

**Definition**: A governance checkpoint at which a designated human must make or approve a consequential research decision.

**Problem solved**: Prevents AI assistance from becoming implicit authority.

**Created by**: Workflow system when a gate is required; completed by the designated human authority.

**Content authority**: The human decision recorded at that gate.

**Who may modify**: Designated human authority; system may append audit metadata but cannot substitute a human decision.

**Consumers**: Workflow execution, Snapshot publication, Evaluation and Audit.

**Minimum fields**:

```yaml
gate_id
type
subject_refs[]
reviewer
decision
timestamp
rationale
status
```

**Valid types**:

```text
H1_SCOPE
H2_POPULATION_SELECTION
H3_JUDGMENT_DECISION
H4_FINAL_DELIVERY
H5_UPDATE_CORRECTION
```

**Valid states**:

```text
pending
passed
rejected
superseded
```

**Invalid states**:

- required gate marked passed without a human reviewer and decision;
- system-generated approval that bypasses the designated human authority;
- historical gate decision silently replaced.

---

### Delivery

**Definition**: A projection of a validated canonical snapshot into an audience- or machine-specific representation.

**Problem solved**: Separates communication/reuse formats from semantic authority.

**Created by**: Rendering workflow.

**Content authority**: None over canonical semantics. Delivery owns representation metadata only.

**Who may modify**: Renderer/build process; final acceptance requires H4 human review where applicable.

**Consumers**: Intended audience, downstream analysis, systems and audit.

**Minimum fields**:

```yaml
delivery_id
snapshot_id
delivery_type
renderer_version
created_at
content_uri
status
```

**Valid states**:

```text
draft
built
validated
published
superseded
archived
```

**Invalid states**:

- delivery with no source Snapshot;
- delivery introducing untracked semantic content;
- published delivery whose rendering/version context cannot be identified.

---

### Build

**Definition**: A recorded transformation execution that turns declared inputs and canonical state into one or more artifacts/deliveries.

**Problem solved**: Makes reproducible transformation context explicit without prescribing infrastructure.

**Created by**: Build/transformation workflow.

**Content authority**: Build metadata and execution provenance, not the semantic truth of the resulting research objects.

**Who may modify**: Build system may create records; historical build records are append-only/versioned.

**Consumers**: Evaluation, Audit, Reproducibility and Delivery.

**Minimum fields**:

```yaml
build_id
snapshot_id
workflow_version
schema_version
transformation_version
input_refs[]
configuration_hash
assumptions_hash
outputs[]
status
created_at
```

**Valid states**:

```text
started
succeeded
failed
superseded
```

**Invalid states**:

- successful build without declared input/version context;
- build record that claims reproducibility while omitting required context;
- historical build metadata silently overwritten.

---

# 3. Object Relationships

The definition-to-execution spine is:

```text
ResearchRequest
      ↓
ResearchCharter
      ↓
ResearchCase
      ↓
ResearchQuestion
      ↓
ResearchSnapshot
      ↓
WorkflowStep
      ↓
ResearchArtifact
      ↓
Canonical Semantic Objects
```

Evidence/provenance chain:

```text
Entity
  ↓
Claim
  ↓
Evidence
  ↓
Source
```

The graph must be navigable in both directions so that the system can answer both:

```text
Which Evidence supports this Claim?
Which Claims does this Evidence support or contradict?
```

Reasoning chain:

```text
Claim / Evidence
        ↓
     Analysis
        ↓
     Judgment
        ↓
 Recommendation
        ↓
     Decision
```

Governance chain:

```text
WorkflowStep
      ↓
 HumanGate
      ↓
 Evaluation
      ↓
 ResearchSnapshot status
      ↓
 Delivery / Build
```

`Hypothesis` and `Unknown` are first-class side branches and must not be silently promoted into established facts or resolved negatives.

---

# 4. Workflow Contract

## 4.1 Formal interface

Every reusable WorkflowStep MUST expose:

```yaml
id: <stable identifier>
name: <human-readable name>
version: <semantic contract version>
purpose: <problem being solved>

inputs:
  - <named artifact/object/input>

outputs:
  - <named artifact/object/output>

preconditions:
  - <conditions that must hold before execution>

method:
  - <operational actions/rules>

constraints:
  - <non-negotiable prohibitions/limits>

human_gate:
  required: true | false
  gate_type: <H1-H5 or declared gate>

validation:
  - <machine-checkable and/or reviewable criteria>

provenance:
  required: true | false
  rules:
    - <provenance requirements>
```

## 4.2 Composition

The system may compose WorkflowSteps into larger workflows. A workflow is a logical graph of steps with explicit dependencies.

Lifecycle labels such as `R0 Define`, `R1 Discover` and `R2 Evidence` are conceptual research stages, not reusable implementation interfaces.

A case need not create one file per lifecycle stage and must not be required to do so.

## 4.3 Constraints on step behavior

A step MUST NOT:

- invent facts outside its declared method and inputs;
- silently change the scope or research unit established by the Charter;
- silently mutate historical canonical state;
- erase uncertainty or contradictions merely to simplify output;
- treat a delivery file as authoritative source when canonical data exists.

## 4.4 Prompt role

Prompt templates may be versioned implementation inputs to a step, but changes to a prompt only require a WorkflowStep version increment when they can materially change contract semantics or output behavior relevant to reproducibility/evaluation.

---

# 5. Canonical Model Contract

## 5.1 Canonical semantic center

The Canonical Research Model contains at minimum:

```text
ResearchCase
ResearchQuestion
ResearchSnapshot

Entity
Claim
Evidence
Source

Analysis
Relationship
Metric
Score

Judgment
Decision
Recommendation
Hypothesis
Unknown
```

Evaluation, HumanGate, Delivery and Build are governance/operational objects around the canonical semantic core rather than research facts themselves.

The exact serialization is intentionally not frozen. Markdown, YAML, JSON, CSV or a database representation may be used by an implementation.

## 5.2 Content authority

Authority belongs to semantic objects and their declared owners, not to delivery format.

Examples:

```text
Scope                  → ResearchCharter
Snapshot boundary      → ResearchSnapshot
Canonical fact claim   → Claim + Evidence + Source
Historical score       → Score within Snapshot
Recommendation         → Recommendation
Human decision         → Decision
Unknown state          → Unknown
Evaluation result      → Evaluation
Gate decision          → HumanGate
Build provenance       → Build
```

A rendering layer may format, filter, select or compress. It must not silently become authority for these values.

## 5.3 Delivery independence

The canonical model MUST be usable without requiring PPT, HTML, Dataset or Research Note to exist.

Conversely, a Delivery MUST be rebuildable from the canonical model plus declared rendering configuration/code.

## 5.4 Historical snapshots

A validated/published Snapshot is an immutable historical state by default. Corrections happen through explicit versioned actions and must preserve an audit trail.

---

# 6. Provenance Contract

## 6.1 Provenance chain

The minimum provenance graph is:

```text
Delivery Element
      ↓
Claim / Judgment
      ↓
Evidence
      ↓
Source
      ↓
Original Source / Document
```

A direct delivery-to-claim path is acceptable for simple factual material only when the underlying Evidence/Source chain remains inspectable.

## 6.2 Identifier rules

At minimum, the following identifiers are required where the object class exists:

```text
source_id
evidence_id
claim_id
```

Identifiers MUST be unique within their declared namespace and MUST NOT be reused for semantically different objects.

## 6.3 Factual claims

An externally verifiable factual Claim MUST have:

```text
Claim
  → at least one supporting Evidence
  → Source
```

If the Claim is itself a conclusion based on multiple conflicting sources, the conflict must remain visible in the evidence graph.

## 6.4 Quantitative claims

A quantitative Claim MUST additionally preserve:

```text
metric definition
value
unit
qualifier
source/evidence
relevant date or period
```

Qualifiers such as survey signal, vendor-reported number, estimate or benchmark result must not be silently removed when they materially affect interpretation.

## 6.5 Analytical judgments

A major Judgment MUST link to the claims, analysis and/or evidence supporting it.

It may synthesize and infer, but must remain distinguishable from a direct external fact.

## 6.6 Hypotheses

A Hypothesis must be explicitly typed/labeled as a hypothesis and may carry supporting evidence. It cannot inherit factual status merely because it appears in a polished delivery.

## 6.7 Unknowns

Unknowns do not require artificial evidence proving their unknown status. They MUST preserve their scope, significance and unresolved state.

## 6.8 Contradictory evidence

Evidence MUST be able to support one Claim and contradict another, or otherwise expose incompatible observations. Contradictions MUST NOT be resolved silently by overwriting one side.

A future implementation may materialize a dedicated Contradiction object, but v1 does not require one if the evidence graph can express the same semantics.

---

# 7. Human Judgment Gate Contract

The mandatory human gate vocabulary is:

```text
H1 Scope
H2 Population / Selection
H3 Judgment / Decision
H4 Final Delivery
H5 Update / Correction
```

## H1 — Scope

Human approval of research objective, questions, boundaries, research unit, exclusions, cutoff and success conditions.

AI may draft these. AI cannot silently approve them on behalf of the human authority.

## H2 — Population / Selection

Human review of consequential inclusion, exclusion, ranking, selection and exception decisions.

AI may propose a population or ranking, but approval remains human unless a separately approved rule establishes otherwise.

## H3 — Judgment / Decision

Human review of major strategic conclusions, recommendations, interpretations, unresolved ambiguity and consequential decisions.

AI assistance is permitted; human authority remains explicit.

## H4 — Final Delivery

Human review of factual accuracy, citation integrity, uncertainty, wording, audience fit and compression/distortion risk.

## H5 — Update / Correction

Corrections affecting a historical snapshot require explicit, versioned human action. Automated rebuilds cannot silently rewrite history.

## Gate record

The `HumanGate` object defined in §2.6 records the subject references, human reviewer, decision, timestamp, rationale and state.

A required gate without a recorded human decision is not passed.

---

# 8. Evaluation Contract

## 8.1 Mechanical Evaluation

The v1 evaluator must be conceptually capable of checking at least:

```text
schema validation
identifier uniqueness
referential integrity
required-field completeness
provenance completeness
cross-artifact consistency
Unknown-state preservation
historical snapshot immutability
build validation
render smoke test
invariant checks
```

These checks are contract requirements, not a requirement to implement the evaluator during Step 1.

## 8.2 Human Evaluation

Minimum v1 dimensions:

```text
Coverage
Source Quality
Citation Accuracy
Factual Accuracy
Contradiction Handling
Reasoning Quality
Final Answer Usefulness
```

Human evaluation records should preserve both assessment and review context where material.

## 8.3 Research Run completion

A Research Run is complete only when all of the following are true:

```text
Canonical Snapshot is structurally valid
        AND
Mandatory mechanical validation = PASS
        AND
Required Human Gates = explicitly passed
        AND
Delivery projection is consistent with the validated snapshot
```

An attractive delivery with unknown evaluation status is not a completed research run.

Evaluation results are themselves durable research-system knowledge because they indicate workflow weaknesses, automation risks and areas requiring future improvement.

---

# 9. Reproducibility Contract

## 9.1 Reproducibility context

A Research Snapshot is rebuildable only when its reproducibility context is declared:

```text
Research Case
+
Snapshot Definition / Cutoff
+
Workflow Version
+
Schema Version
+
Transformation Code Version
+
Input Artifact Versions
+
Configuration
+
Assumptions
+
Relevant Model-Generated Inputs
```

A Build records this context for an actual transformation execution.

A compact conceptual identity is:

```text
ReproducibilityContext =
(
  case,
  snapshot,
  workflow_version,
  schema_version,
  transformation_version,
  configuration,
  assumptions,
  input_versions
)
```

## 9.2 Reproducible does not mean deterministic

The same context may yield non-identical model output because external sources, models, search results or stochastic execution can change.

v1 therefore defines reproducibility as:

> Given the declared versions, inputs, assumptions, configuration and provenance context, the system can re-execute the research transformation and explain how the snapshot and deliveries were produced.

Byte-for-byte identical output is not a v1 requirement unless a particular transformation explicitly declares deterministic behavior.

## 9.3 Historical protection

Rebuilding from old inputs MUST NOT silently rewrite a published historical snapshot. A rebuild produces a comparable result or a new versioned snapshot/action according to explicit update rules.

---

# 10. Delivery Contract

The delivery pipeline is:

```text
Canonical Model
      ↓
Projection / Rendering
      ↓
Delivery
```

## 10.1 Dataset

Purpose: machine-readable reuse, analysis and downstream automation.

May perform formatting, normalization and structural projection.

Must not introduce new facts, scores, rankings or judgments not present in canonical sources.

## 10.2 Research Note / Report

Purpose: durable human reading and reasoning narrative.

May organize and compress canonical knowledge and explain relationships. It must preserve material uncertainty, qualifiers and provenance.

## 10.3 HTML / Explorer

Purpose: interactive exploration and comparison.

May support filters, sorting, navigation and view transformations. Such interaction changes presentation, not canonical semantics.

## 10.4 PPT / Executive Brief

Purpose: decision support and executive communication.

It carries the highest semantic-compression risk. Numbers, qualifiers, uncertainty and ranking semantics must survive compression. Human H4 review is mandatory.

## 10.5 Audit Package

Purpose: inspection, provenance verification, evaluation review and reproducibility.

It should make it possible to answer:

```text
Where did this statement come from?
What evidence supports it?
What source was used?
What was the snapshot/version?
What assumptions applied?
Who approved the consequential judgment?
```

## 10.6 Non-negotiable projection rule

A Delivery MUST NOT silently introduce:

```text
new factual claims
new metrics
new scores
new rankings
new decisions
resolved Unknowns
removed contradictions
```

Any genuinely new research content must return to the canonical research process rather than being hidden in rendering.

---

# 11. Version Contract

The v1 system distinguishes these version dimensions:

```text
ResearchCase Version
ResearchSnapshot Version
WorkflowStep Version
Schema Version
Transformation Version
ResearchArtifact Version
Delivery Version
Evaluation Version
HumanGate Version
Build Record Version
```

## Versioning rules

1. Stable identifiers identify semantic objects; versions identify historical changes to their state or contract.
2. Material WorkflowStep contract changes require a new step version.
3. Schema changes require a new schema version.
4. Transformation changes that can alter canonicalization or delivery require a new transformation version.
5. Material assumptions, scope, or consequential historical judgments require versioned research state.
6. A historical published Snapshot is not silently rewritten.
7. Supersession is explicit; old states remain recoverable.
8. Evaluation and HumanGate records are historical governance records; corrections append/version rather than silently overwrite.

No v1 contract requires a general-purpose schema migration engine.

---

# 12. Invariants

The following invariants are normative.

## 12.1 MUST

```text
MUST-001
Identifiers are unique within their declared namespace.

MUST-002
Every reference resolves to an existing canonical object or explicitly declared external reference.

MUST-003
Every externally verifiable factual Claim has required provenance.

MUST-004
Every quantitative Claim preserves its metric context, qualifier, period and provenance.

MUST-005
Unknown remains semantically distinct from No, False, 0, Empty and Not Applicable.

MUST-006
A validated/published historical Snapshot cannot be silently mutated.

MUST-007
Delivery artifacts are not semantic authority when canonical sources exist.

MUST-008
Delivery cannot introduce untracked facts, scores, rankings, judgments or decisions.

MUST-009
Required Human Gates have an explicit recorded human decision before Research Run completion.

MUST-010
Contradictory evidence can be represented without silently deleting one side.

MUST-011
Canonical references and required provenance references are valid.

MUST-012
Mandatory mechanical validation must pass before a Research Run is complete.

MUST-013
A Hypothesis cannot be represented as an established factual Claim without an explicit state transition supported by the research process.

MUST-014
A Recommendation is not equivalent to a Decision unless a human-authorized transition records that decision.

MUST-015
A successful Build records the reproducibility context needed to explain its transformation.

MUST-016
A Delivery must reference the Snapshot it projects from.
```

## 12.2 SHOULD

```text
SHOULD-001
Important Judgments expose their supporting basis chain.

SHOULD-002
Delivery elements expose traceability to canonical objects where practical.

SHOULD-003
Reusable Workflow promotion is supported by evidence from multiple cases or clear domain-independence.

SHOULD-004
Version-bound artifacts record their Snapshot context.

SHOULD-005
Qualifiers and uncertainty survive delivery projection whenever they affect interpretation.
```

## 12.3 MAY

```text
MAY-001
Artifacts may be Markdown, YAML, JSON, CSV, database records or other representations.

MAY-002
Workflow execution may use prompts, code, tools, human forms or future agents.

MAY-003
A Case may define domain-specific entity types.

MAY-004
A future implementation may store the Canonical Model in a database.

MAY-005
A future implementation may materialize additional specialized relationship/evaluation objects when real cases demonstrate need.
```

---

# 13. System Boundary

## Included in v1 contract

```text
Research Definition
Research Case / Question / Snapshot
Workflow Step
Research Artifact
Canonical Semantic Objects
Provenance
Human Gates
Mechanical Evaluation
Human Evaluation
Reproducibility Context
Versioning
Delivery Projection Rules
System Invariants
```

## Explicitly excluded from Step 1

```text
Workflow Runtime implementation
Canonical Registry implementation
Evaluator implementation
Renderer implementation
Agent implementation
Database deployment
Vector Database
Graph Database
MCP server
Multi-agent runtime
Distributed workers
Event bus / queue
Autonomous browser infrastructure
Universal connector framework
```

These may become later implementation concerns only when justified by demonstrated workflow needs.

---

# 14. Case 001 Compatibility / Legacy Boundary

Case 001 is a Reference / Legacy Research Case, not the schema authority for Research System v1.

Its historical artifacts, including phase-based files and its `08-canonical-research-model.md`, remain valid as historical research artifacts and reference material. Its domain-specific entities such as ProductFamily, Candidate, ProductCapability, Category and Phase are not mandatory system-level object types.

The case's canonical model can be understood as an instantiated semantic model that records historical decisions from the old process. It does not redefine the reusable Workflow, Canonical Model, Provenance, Human Gate or Evaluation contracts.

The system MUST NOT require:

```text
Phase 0
Phase 1
...
Phase 8
```

as system interfaces.

The existing `research-system-v1.md` remains the methodology baseline. This design adds the formal contract layer without modifying it because the current baseline already establishes the system-first direction, the Research Lifecycle, the WorkflowStep abstraction, canonical knowledge principles, human gates, evaluation and reproducibility requirements. Any future edits to the methodology document should preserve this separation rather than promote Case 001's legacy schema into a universal interface.

---

# 15. Step 1 Exit Criteria

Step 1 is complete when all criteria below are satisfied:

```text
E1
All required core objects have stable definitions.

E2
Core object relationships are explicit.

E3
WorkflowStep has a stable reusable interface.

E4
Canonical Model is independent of delivery format.

E5
The minimum provenance chain is explicit and machine-checkable in principle.

E6
Human Judgment authority is explicit at H1-H5.

E7
Research Run completion is explicitly defined.

E8
Reproducibility context is explicit and does not imply deterministic output.

E9
Historical Snapshot mutation rules are explicit.

E10
MUST invariants are objectively testable in principle.

E11
No core system interface depends on Case 001 phase numbering.

E12
No future infrastructure is required by the contract.

E13
Case 001 can be treated as an instance/legacy case without changing the system contract.
```

---

# 16. Design Decision Record

## Decision

Adopt **Contractual Semantic Core + Artifact Boundary** for Research System v1.

## Rejected alternatives

### Artifact-Centric Contract

Rejected because it leaves too much semantic authority attached to files and makes cross-delivery consistency harder to guarantee.

### Fully Typed Research Registry

Rejected for v1 because it risks prematurely turning the system contract into a database/infrastructure design. The semantic object model is frozen now; storage/runtime implementation remains open.

## Why the selected design wins

It preserves the repository's practical artifact-first workflow while separating semantic authority from file layout. It is therefore compatible with the existing Markdown-based research practice, independent of Case 001's phase structure, and open to future storage/runtime changes without changing the conceptual contract.

---

# 17. Non-Goals

This document does not:

- implement any runtime;
- create a canonical registry;
- implement validators/evaluators;
- build renderers;
- build agents or skills;
- migrate Case 001 into the new model;
- rebuild Case 001 Phase 8;
- require a database;
- define every future domain-specific entity;
- specify a universal research automation engine.

The purpose of Step 1 is contract stability, not implementation completeness.
