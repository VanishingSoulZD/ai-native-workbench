# Research System v1

> Repository-level design specification for `ai-native-workbench`
>
> Status: **Design baseline · Roadmap revised 2026-09-03**
>
> Origin: Case 001 — 2026 AI Coding Agent Landscape retrospective
>
> Scope: Define the reusable Research Workbench architecture before implementing broader automation, Skills, or Agents.

---

## 0. Executive Definition

`ai-native-workbench` is intended to evolve from a collection of AI-assisted research cases into a reusable **Human-in-the-loop, Evidence-first, Evaluation-driven Research Workbench**.

The system does not aim to make research fully autonomous. Its purpose is to transform high-quality research from a prompt-dependent, person-dependent activity into a process that is:

- **Definable** — research questions, scope, units, constraints, and success criteria are explicit.
- **Executable** — recurring research work is represented as reusable workflow steps rather than ad-hoc prompts.
- **Traceable** — important judgments can be traced to claims, evidence, and sources.
- **Evaluable** — research quality is checked through mechanical validation and human review.
- **Reproducible** — structured research assets and deliveries can be rebuilt from declared inputs.
- **Deliverable** — the same research knowledge can be rendered for different audiences and use cases.
- **Updatable** — research exists as versioned snapshots that can be refreshed as evidence changes.

The central architectural principle is:

> **One Workflow, Many Cases. One Canonical Research Model, Many Deliveries. Human Judgment around Automation, not replaced by Automation.**

This document is a system-level design baseline. It is not an implementation specification for a Research Agent, and it does not require all future directories or components to be created immediately.

---

# 1. Why This System Exists

Case 001 demonstrated that a complex research task can be completed with AI assistance, but also exposed three structural limitations:

1. Each research phase could be completed successfully while the overall method remained dependent on repeated natural-language prompting.
2. Phase 8 produced structured datasets and presentation assets, but the transformation from earlier research artifacts into those datasets was not fully reproducible.
3. Research, canonical knowledge, evaluation, and delivery were mixed across phase-oriented files, making it difficult to know which artifacts should be reused, audited, updated, or presented externally.

Case 001 therefore serves two purposes:

- **Research output:** understand the 2026 AI Coding Agent landscape.
- **System experiment:** discover which parts of high-quality research can be standardized and engineered.

The system-level objective is not to perfect the legacy implementation of Case 001. It is:

> **Extract a reusable research operating model from real work, implement that model independently of the legacy case layout, and validate it against both a reference problem and a meaningfully different research problem.**

Case 001 is therefore treated as a **Reference / Legacy Research Case** during Research System v1 implementation. Its historical artifacts remain valuable evidence and examples, but fixing or rebuilding its old phase-to-dataset pipeline is not a prerequisite for the new system.

---

# 2. Design Principles

## 2.1 Real Work First

Capabilities are extracted from real tasks rather than invented as abstract framework features.

## 2.2 Workflow Before Agent

A Research Agent may only automate a research workflow after the workflow has been performed, reviewed, and evaluated as a human/AI collaboration pattern.

## 2.3 Canonical Knowledge Before Rendering

Reports, HTML explorers, presentations, and datasets are views of canonical research knowledge. They are not competing sources of truth.

## 2.4 Human Judgment Remains Central

Problem framing, scope, consequential judgment, decision, and final review remain human responsibilities unless explicitly validated otherwise.

## 2.5 Evidence Before Assertion

Important claims should have explicit provenance. Unsupported certainty is treated as a quality defect.

## 2.6 Evaluation Before Automation

A workflow should be measured before its automation is expanded. A fast workflow with unknown quality is not considered a successful automation.

## 2.7 Reproducibility Without False Determinism

Research is not always deterministic because sources, model outputs, and external information change. Reproducibility therefore means that the transformation logic, inputs, assumptions, versions, and provenance are explicit enough to rebuild and explain a research snapshot.

## 2.8 Minimal Sufficient Engineering

The repository must not create infrastructure merely because it is technically possible. Components are promoted into shared system capabilities only when a real case demonstrates repeated value.

---

# 3. System Scope

Research System v1 covers five layers:

```text
Research Definition
        ↓
Research Execution
        ↓
Canonical Knowledge
        ↓
Evaluation
        ↓
Delivery
```

Supporting lifecycle concerns span all five layers:

```text
Versioning / Provenance / Human Gates / Reproducible Build / Update
```

The system does **not** yet define:

- a fully autonomous research agent;
- multi-agent orchestration;
- a universal database deployment;
- autonomous final decision making;
- automatic browsing of every source type;
- domain-specific expert reasoning as a guaranteed capability.

Those are later-stage implementation questions and must be justified by real workflow evidence.

---

# 4. Standard Research Lifecycle

The canonical Research Lifecycle v1 is:

```text
R0 Define
  ↓
R1 Discover
  ↓
R2 Evidence
  ↓
R3 Analyze
  ↓
R4 Decide
  ↓
R5 Synthesize
  ↓
R6 Evaluate
  ↓
R7 Deliver
  ↓
R8 Archive / Update
```

The lifecycle is a **logical workflow**, not a requirement that every case must produce exactly one file per step.

## R0 — Define

Purpose: determine what should be researched and why.

Inputs:

- research request;
- decision context;
- stakeholder needs;
- known constraints.

Outputs:

- Research Charter;
- research questions;
- scope and exclusions;
- research unit;
- cutoff date / snapshot definition;
- success criteria.

Human gate: **required**.

## R1 — Discover

Purpose: establish the research population and information space.

Outputs may include:

- candidate universe;
- source map;
- taxonomy;
- research plan;
- initial research hypotheses.

The output is a map of the problem space, not yet a final conclusion.

## R2 — Evidence

Purpose: collect and normalize observations that can support or challenge claims.

Core objects:

```text
Source
Evidence
Claim
```

Evidence should retain enough provenance to understand where it came from, when it was observed, what exactly was observed, what kind of evidence it is, and what claims it supports or contradicts.

## R3 — Analyze

Purpose: transform evidence into structured comparisons, models, patterns, metrics, and relationships.

Examples:

- comparison matrices;
- scores;
- category models;
- market strata;
- architecture paradigms;
- workflow patterns;
- competition relationships.

Analysis must distinguish observation from inference.

## R4 — Decide

Purpose: form consequential judgments and decisions.

Core objects:

```text
Judgment
Recommendation
Hypothesis
Unknown
Decision
```

Important decisions should remain explicitly attributable to human judgment even when AI helped prepare the analysis.

## R5 — Synthesize

Purpose: produce the canonical knowledge representation and durable narrative.

Outputs:

- Canonical Research Model / Registry;
- Research Note;
- Source Ledger;
- normalized datasets.

R5 is where working research becomes reusable knowledge.

## R6 — Evaluate

Purpose: establish whether the research is sufficiently reliable and useful.

Two evaluation modes are required:

```text
Mechanical Validation
        +
Human Review
```

A research package should not be considered complete until mandatory evaluation gates pass.

## R7 — Deliver

Purpose: project canonical knowledge into audience-specific forms.

Standard delivery classes:

- Executive Brief / PPT;
- Research Note / report;
- Interactive Explorer / HTML;
- Dataset export;
- Source Ledger / audit package.

## R8 — Archive / Update

Purpose: preserve the research snapshot and support future updates.

An update should be modeled as:

```text
Previous Snapshot
      ↓
New Evidence / Changed Assumptions
      ↓
Impact Analysis
      ↓
Updated Canonical Model
      ↓
New Snapshot
```

Historical snapshots should remain recoverable rather than silently overwritten.

---

# 5. Workflow Model

The reusable unit is a **Workflow Step**, not a prompt.

A Workflow Step has the following conceptual interface:

```yaml
id: <stable identifier>
name: <human-readable name>
purpose: <what problem the step solves>

inputs:
  - <named input>

outputs:
  - <named output>

method:
  - <operational actions / rules>

constraints:
  - <non-negotiable constraints>

human_gate:
  required: true | false

validation:
  - <machine-checkable or reviewable criteria>

provenance:
  required: true | false
```

## 5.1 Step Contract

Every reusable step must make four things explicit:

1. **Consumes** — the structured artifacts it expects.
2. **Produces** — the structured artifacts later steps may consume.
3. **Constraints** — what it is prohibited from changing or inventing.
4. **Gate** — whether human approval is mandatory.

## 5.2 Prompt Role

Prompts are implementation details of a workflow step. They are not the workflow interface.

A future implementation may use a prompt template, Python function, CLI command, LLM call, browser/search tool, human form, or a combination of these. The workflow contract remains stable even when execution technology changes.

## 5.3 Reusability Criterion

A workflow step is promoted from Case-specific procedure to reusable Workflow capability only when:

- it solves a recurring problem across cases or is clearly domain-independent;
- its inputs and outputs can be named;
- its quality can be evaluated;
- its failure modes are understood sufficiently for reuse.

---

# 6. Research Artifact Model

Research artifacts are grouped by role rather than by phase number.

```text
Definition Artifacts
Working Artifacts
Canonical Knowledge Artifacts
Evaluation Artifacts
Delivery Artifacts
```

## 6.1 Definition Artifacts

Examples: Research Charter, Research Plan, taxonomy, scope rules, success criteria.

Purpose: define the research.

## 6.2 Working Artifacts

Examples: candidate universe, market evidence, product research, benchmark research, cross-product analysis, decision working paper.

Purpose: support research execution and preserve reasoning trace.

These are important, but they are not automatically the final knowledge source of truth.

## 6.3 Canonical Knowledge Artifacts

Examples: canonical registry, claims, evidence, sources, judgments, recommendations, hypotheses, unknowns, relationships, scores/metrics, research snapshot.

Purpose: preserve what the research actually knows and how it knows it.

## 6.4 Evaluation Artifacts

Examples: validation report, citation audit, consistency report, coverage assessment, human review record, final quality report.

Purpose: evaluate research quality.

## 6.5 Delivery Artifacts

Examples: executive PPT, research report/note, HTML explorer, dataset export, source/audit package.

Purpose: communicate or reuse canonical knowledge.

---

# 7. Canonical Research Model

The Canonical Research Model is the semantic center of the system.

It follows:

> **One Canonical Model, Many Renderings.**

The canonical model must not be derived by reading one already-rendered output and copying it into another. Delivery artifacts project from the same canonical data and provenance layer.

## 7.1 Core Entities

Minimum conceptual entities for v1:

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

## 7.2 Core Evidence Chain

```text
Entity
  ↓
Claim
  ↓
Evidence
  ↓
Source
```

Reasoning chain:

```text
Claim / Evidence
        ↓
     Analysis
        ↓
     Judgment
        ↓
Decision / Recommendation
```

The system should make these relationships inspectable.

## 7.3 Authority Principle

For each important field, the system should define its **content authority**: the artifact or stage that owns the value.

Examples:

- Research scope → Charter;
- historical score → scoring artifact;
- selected population → selection decision;
- capability cell → canonical capability record;
- claim provenance → Claim/Evidence/Source layer.

A rendering may transform formatting, but must not silently become the authority for the value it renders.

## 7.4 Unknown Is a First-Class State

Unknown must not be represented as blank, zero, “No”, “—”, or an inferred negative. The state must remain semantically distinct from confirmed absence.

## 7.5 Historical Decisions

Historical rankings, scores, or decisions are immutable within a research snapshot unless a new human-approved research action explicitly creates a new version.

A new system build must not silently “fix” an old snapshot.

---

# 8. Provenance and Citation Model

Every important claim that appears in canonical knowledge or delivery assets should have a provenance path.

```text
Delivery Element
      ↓
Judgment / Claim
      ↓
Evidence
      ↓
Source
      ↓
Original Document / URL
```

## 8.1 Source

Minimum fields:

```text
source_id
canonical_title
publisher / owner
canonical_url
source_type
date
accessed_at
tier / quality class
```

## 8.2 Evidence

Minimum fields:

```text
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

## 8.3 Claim

Minimum fields:

```text
claim_id
statement
claim_type
subject_ref
evidence_ids[]
confidence
status
```

## 8.4 Provenance Requirements by Content Class

At minimum:

- externally verifiable factual claims → provenance required;
- quantitative claims → provenance + qualifier required;
- major analytical judgments → supporting claim/evidence chain required;
- hypotheses → explicitly labeled as hypotheses and not represented as established facts;
- unknowns → explicitly represented and preserved.

---

# 9. Human Judgment Gates

The system is intentionally Human-in-the-loop.

## H1 — Research Scope Gate

Human approves research question, boundaries, research unit, key definitions, and cutoff/snapshot definition.

## H2 — Research Population / Selection Gate

Human reviews consequential inclusion, exclusion, ranking, and exception decisions.

## H3 — Judgment Gate

Human reviews important strategic conclusions, recommendations, major inference, and unresolved ambiguity.

## H4 — Final Delivery Gate

Human reviews factual correctness, citation integrity, wording, uncertainty representation, audience appropriateness, and compression distortion.

## H5 — Update / Correction Gate

A correction to a historical research snapshot requires an explicit, versioned action. It must not be silently rewritten by an automated build.

---

# 10. Evaluation Model

Research quality is evaluated through two complementary systems.

## 10.1 Mechanical Evaluation

Examples:

- schema validation;
- identifier uniqueness;
- referential integrity;
- required-field checks;
- source existence;
- citation mapping;
- CSV parseability;
- cross-artifact consistency;
- build success;
- invalid-state detection;
- Unknown-state preservation;
- invariant checks;
- generated asset smoke tests.

## 10.2 Human Evaluation

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

## 10.3 Evaluation Gate

A research case is complete only when mandatory mechanical checks pass and the required human review gates are explicitly recorded.

## 10.4 Evaluation Is Reusable Knowledge

Evaluation results should themselves be archived because they reveal where the workflow fails, where automation is unsafe, which steps deserve stronger validation, and what should change in the next workflow version.

---

# 11. Reproducible Build Model

The build system must separate **research creation** from **asset rendering**.

The intended build chain is:

```text
Research Working Artifacts
        ↓
Extraction / Normalization
        ↓
Canonical Registry
        ↓
Validation
        ↓
Evaluation Gates
        ↓
Delivery Rendering
        ↓
PPT / Note / HTML / Dataset / Audit Package
```

## 11.1 Build Inputs

A reproducible build must identify:

- research case;
- research snapshot / cutoff;
- source working artifacts;
- workflow version;
- schema version;
- transformation code version;
- configuration and assumptions;
- model-generated inputs when relevant.

## 11.2 Build Outputs

Where feasible, the build should generate:

- canonical datasets;
- source ledger;
- research note;
- HTML explorer;
- executive presentation;
- validation report.

## 11.3 Build Boundaries

A renderer may transform, format, compress, visualize, or reorder canonical knowledge for presentation. It must not silently introduce new facts, scores, rankings, or judgments.

## 11.4 Case 001 Legacy Gap — Deferred

Case 001 currently contains historical Phase 8 datasets and a presentation generator. The old transformation from Phase 1–7 artifacts into those datasets is known to be incomplete as a reproducible pipeline.

This gap is intentionally **deferred** during Research System v1 implementation.

The system should first establish a generic build model that does not depend on the Case 001 phase layout. After the new system is validated, Case 001 may be rerun through the new system and its legacy implementation may then be archived or retained as a historical reference.

---

# 12. Delivery Model

Delivery is audience-specific projection from canonical knowledge.

| Delivery | Primary audience | Primary use |
|---|---|---|
| Executive Brief / PPT | executives / decision makers | briefing and decision |
| Research Note / Report | researchers / owners | deep reading and durable knowledge |
| Interactive Explorer / HTML | practitioners / team | exploration and comparison |
| Dataset | analysts / software | further analysis and downstream automation |
| Source Ledger / Audit Package | reviewers / researchers | verification and traceability |

## 12.1 Executive Brief / PPT

Optimized for:

```text
What happened?
Why does it matter?
What do we believe?
What should we do?
```

It intentionally compresses information and therefore has high compression-distortion risk.

## 12.2 Research Note / Report

Optimized for:

```text
Question
→ Method
→ Evidence
→ Analysis
→ Judgment
→ Unknowns
→ Implications
```

This is the durable human-readable knowledge asset.

## 12.3 Interactive Explorer / HTML

Optimized for query, comparison, matrix inspection, evidence lookup, and uncertainty/unknown inspection.

## 12.4 Dataset

Optimized for analysis, rebuilding visualizations, downstream automation, update workflows, and future agent consumption.

## 12.5 Source / Audit Package

Optimized for source verification, citation review, discrepancy investigation, and research handoff.

---

# 13. Case Template Model

Future cases should progressively converge toward a common logical structure:

```text
Case
├── Definition
├── Working Research
├── Canonical Knowledge
├── Evaluation
└── Delivery
```

A concrete file layout is intentionally **not fully frozen in v1**. The repository should only create structures that have been justified by actual case needs.

A mature case template should support initializing a new research case without requiring the researcher to manually recreate the workflow from old prompts.

Conceptually:

```text
research init
      ↓
Case Skeleton
      ↓
Research Workflow
      ↓
Canonical Knowledge
      ↓
Evaluation
      ↓
Delivery
```

---

# 14. Case 001 Mapping — Reference Only

Case 001 remains useful as the empirical source from which the system design was derived.

Its historical phase structure can be interpreted approximately as:

```text
Phase 0 → R0 Define
Phase 1 → R1 Discover
Phase 2 → R2 Evidence
Phase 3 → R3 Analyze / Select
Phase 4 → R2/R3 Product Evidence + Analysis
Phase 5 → R2/R3 Benchmark Evidence + Analysis
Phase 6 → R3 Analyze
Phase 7 → R4 Decide
Phase 8 → R5/R7 Synthesize + Deliver
```

This mapping is **descriptive, not normative**.

The Phase 0–8 numbering and Case 001 file layout are historical implementation details. They are not the interface that future cases must reproduce.

Case 001 should therefore be treated as:

```text
Reference Research
        +
Legacy Artifact Set
        +
System Design Evidence
```

not as the implementation template that Research System v1 must mechanically rebuild.

---

# 15. Validation Strategy

Research System v1 must prove itself through execution, not through design claims alone.

The validation sequence is:

```text
Case 001 (Reference / Legacy)
        ↓
Research System v1
        ↓
End-to-End Validation Case
        ↓
Meaningfully Different Generalization Case
        ↓
System Revision
```

## 15.1 Reference Validation

Case 001 may be rerun using the new system after the system becomes executable. This checks whether the new workflow can represent a known complex research problem.

The legacy Case 001 implementation itself is not a prerequisite and should not be repaired merely to satisfy this test.

## 15.2 Generalization Validation

At least one **meaningfully different research problem** should be executed using the same core workflow.

The purpose is to distinguish:

```text
Reproducing one case
        from
Reusing a research system
```

A generalization case should differ materially in research object, evidence structure, decision pattern, or analytical method rather than merely changing the topic name.

## 15.3 Reusability Claim

Research System v1 should not be considered reusable based on a single successful run.

A credible v1 reusability claim requires evidence that:

- the same workflow contracts can be reused;
- no core step depends on Case 001-specific phase names;
- canonical knowledge can represent both cases;
- evaluation works across both cases;
- delivery can be regenerated from canonical knowledge;
- case-specific extensions are isolated from the shared core.

---

# 16. Versioning and Research Snapshots

The system distinguishes at least three versions:

```text
Workflow Version
Schema Version
Research Snapshot Version
```

## 16.1 Workflow Version

Defines the behavior and contracts of the reusable research workflow.

Examples:

```text
research-workflow-v1
research-workflow-v1.1
```

## 16.2 Schema Version

Defines canonical entity structures and field semantics.

A schema change must be explicit because downstream renderers and validators depend on it.

## 16.3 Research Snapshot

Represents a bounded state of research at a stated time/cutoff and under stated assumptions.

A new snapshot may be generated because of:

- new evidence;
- changed source data;
- changed research scope;
- approved correction;
- workflow/schema changes with semantic impact.

Historical snapshots should remain recoverable.

---

# 17. Failure and Exception Model

The system must represent research failure explicitly rather than forcing every case into a successful-looking output.

Minimum exception classes:

```text
Insufficient Evidence
Contradictory Evidence
Ambiguous Entity
Missing Provenance
Historical Discrepancy
Validation Failure
Evaluation Failure
Renderer Failure
Generalization Failure
```

An exception should record:

```text
What failed
Where it failed
Why it failed
Impact
Human disposition
Whether the workflow should change
```

A failure in one case should not automatically be hidden by manual patching. Where appropriate, it becomes evidence for workflow revision.

---

# 18. Promotion Rules

The repository contains multiple capability layers, but promotion must be earned.

## 18.1 Working Procedure → Workflow Capability

Promote when a procedure is repeated or clearly domain-independent, has explicit inputs/outputs, has evaluation criteria, and has understood failure modes.

## 18.2 Workflow Capability → Skill

Promote when the capability is stable, reusable, bounded, and useful as a callable unit.

## 18.3 Workflow / Skill → Automation

Promote when repetition justifies engineering and evaluation shows that automation does not reduce required quality.

## 18.4 Automation → Agent

Promote only when dynamic decision making, tool selection, iteration, or orchestration provides demonstrated value beyond deterministic workflow execution.

The project therefore follows:

```text
Real Work
↓
Working Procedure
↓
Workflow Capability
↓
Evaluation
↓
Skill / Automation
↓
Agent
```

---

# 19. Division of Responsibilities

Research System v1 should maintain clear boundaries between Human, AI, and deterministic software.

## Human

```text
Problem Framing
Scope
Key Definitions
Consequential Judgment
Decision
Final Review
```

## AI

```text
Search Assistance
Extraction
Summarization
Candidate Analysis
Drafting
Pattern Discovery
Reasoning Assistance
```

## Deterministic Software

```text
Schema Validation
Transformation
Normalization
Identifier Management
Referential Integrity
Build
Rendering
Mechanical Evaluation
```

These are default responsibilities, not absolute limits. Any boundary change should be justified by evaluation evidence.

---

# 20. Architectural Summary

The target architecture is:

```text
                         RESEARCH REQUEST
                                │
                                ▼
                         ┌──────────────┐
                         │   R0 DEFINE  │
                         │    Charter   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R1 DISCOVER   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R2 EVIDENCE   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R3 ANALYZE    │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R4 DECIDE     │
                         └──────┬───────┘
                                │
                         HUMAN JUDGMENT
                                │
                                ▼
                    ┌───────────────────────┐
                    │ CANONICAL RESEARCH   │
                    │ MODEL / REGISTRY     │
                    └───────────┬───────────┘
                                │
                         VALIDATION
                                │
                                ▼
                         ┌──────────────┐
                         │ R6 EVALUATE   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R7 DELIVER    │
                         └──────┬───────┘
                                │
                ┌───────────────┼────────────────┐
                ▼               ▼                ▼
              PPT           Research Note     HTML
                │               │                │
                └───────────────┼────────────────┘
                                │
                         Dataset / Sources
                                │
                                ▼
                         R8 ARCHIVE / UPDATE
```

The key invariant is:

> **Delivery artifacts are projections of canonical research knowledge; they are not independently authored research sources.**

---

# 21. Repository Boundary

Research System v1 is a system design boundary, not a mandate to create every possible directory immediately.

The repository currently has conceptual responsibilities for:

| Area | Responsibility |
|---|---|
| `cases/` | real research cases and case-specific artifacts |
| `workflows/` | validated reusable workflows |
| `skills/` | callable reusable capabilities extracted from workflows |
| `agents/` | agent implementations when the workflow maturity justifies them |
| `evaluations/` | reusable evaluation methods and results |
| `docs/` | methodology, design decisions, and project-level documentation |

New shared capabilities should appear only when the current roadmap reaches them.

The rule remains:

> **Do not create future architecture only to make the repository look complete.**

---

# 22. Implementation Roadmap — Revised 2026-09-03

The roadmap is intentionally **system-first**.

The former Case 001 Retrospective and Case 001 Reproducible Phase 8 Build are now **deferred legacy work**. They are not prerequisites for Research System v1.

## Step 1 — System Contract

Define and freeze the minimum contracts for:

- Research Request / Charter;
- Workflow Step;
- Research Artifact;
- Canonical Research Model;
- Provenance;
- Human Judgment Gate;
- Evaluation;
- Reproducible Build;
- Delivery.

Also define the minimum invariants, version declarations, and success criteria that make reusability and reproducibility testable.

**Exit condition:** the system can state its inputs, outputs, invariants, versions, and human gates without relying on Case 001-specific phase names or file layout.

## Step 2 — Workflow Core

Implement the minimal reusable workflow capability around the R0–R8 lifecycle and Workflow Step contract.

Prompts remain implementation details. The system interface is the workflow contract.

**Exit condition:** a new research case can be initialized and executed through stable workflow interfaces rather than manually recreating the Case 001 prompt sequence.

## Step 3 — Canonical Knowledge + Provenance

Implement the canonical registry and the Claim / Evidence / Source relationships, including stable identifiers, authority rules, Unknown state, and research snapshot semantics.

**Exit condition:** important research facts, judgments, and decisions can be represented independently of any delivery format and traced through their provenance.

## Step 4 — Evaluation

Implement reusable mechanical validators and the human evaluation protocol.

Minimum automated checks should cover schema integrity, referential integrity, provenance completeness, invariant preservation, cross-artifact consistency, and build/render smoke tests.

**Exit condition:** a research package cannot be treated as complete without explicit evaluation results and required human gates.

## Step 5 — Reproducible Build + Delivery

Implement the generic transformation and rendering chain:

```text
Canonical Research Model
        ↓
Dataset Export
        ↓
Research Note
        ↓
HTML Explorer
        ↓
Executive Presentation
        ↓
Audit / Validation Package
```

Builds must capture declared inputs, versions, snapshot identity, configuration, and assumptions.

**Exit condition:** the same canonical research state can generate at least two delivery forms, and those forms can be rebuilt from declared state without manually re-authoring research content.

## Step 6 — End-to-End Validation Case

Run one complete real research case through the **new** system.

Case 001 may be selected as the reference validation case after the system is runnable, but its historical implementation is not repaired as a prerequisite.

**Exit condition:** one real case completes the full lifecycle with deviations, failures, and human decisions explicitly recorded.

## Step 7 — Generalization Case

Run a **meaningfully different research problem** using the same core workflow.

The second case must differ materially enough to test whether the workflow abstractions are genuinely reusable.

**Exit condition:** the same core workflow contracts are reused without embedding assumptions specific to the first validation case.

## Step 8 — System Revision

Use the observed failures and adaptations from the validation and generalization cases to revise:

- workflow contracts;
- canonical schema;
- provenance rules;
- evaluation checks;
- delivery interfaces.

Version the result as v1.1 only when the observed evidence justifies a semantic change.

**Exit condition:** the next version is evidence-driven rather than feature-driven.

## Step 9 — Automation / Skills / Agentization

Only after the core system is validated should stable, repeated, evaluable workflow steps be promoted into Skills, stronger automation, or Agents.

The order remains:

```text
Workflow
↓
Evaluation
↓
Automation / Skill
↓
Agent
```

---

## 22.1 Deferred Legacy Work

| Work | Status | Reason |
|---|---|---|
| Case 001 Retrospective | **Deferred** | Useful for historical learning, but not a Research System v1 gate |
| Case 001 Phase 1–7 → Phase 8 extraction rebuild | **Deferred** | Avoid overfitting the new system to the legacy phase layout |
| Case 001 rerun through Research System v1 | **Validation option** | Use after the new system is executable |
| Archive Case 001 legacy outputs | **Later** | Preserve them until v1 validation/generalization is complete |

Deferred does not mean abandoned. It means the work is intentionally postponed until the new system provides a better target for it.

---

# 23. Non-Goals for v1

The following are explicitly outside the minimum v1 implementation unless later evidence changes the scope:

- fully autonomous Research Agent;
- multi-agent research orchestration;
- universal source ingestion;
- production-scale distributed infrastructure;
- automatic final strategic decision making;
- forcing all research into one domain-specific schema;
- preserving Case 001's exact phase layout as a compatibility requirement.

The goal is a **small, credible, reusable core**, not a complete research platform on the first implementation cycle.

---

# 24. Success Criteria

Research System v1 is successful only when evidence demonstrates all of the following:

1. **Workflow independence** — a new case can use the workflow without recreating Case 001's phase-specific prompts or file layout.
2. **Canonical authority** — important research content has one canonical source of truth.
3. **Provenance** — important factual and quantitative claims can be traced to evidence and sources.
4. **Human judgment visibility** — consequential decisions and final review are explicitly recorded.
5. **Evaluation gate** — mechanical checks and required human review are part of completion, not optional cleanup.
6. **Reproducible build** — a declared research snapshot can regenerate its structured outputs and delivery assets without manually re-authoring research content.
7. **Multi-delivery consistency** — at least two delivery forms are generated from the same canonical knowledge without semantic drift.
8. **Reference validation** — one real end-to-end case is completed through the new system.
9. **Generalization validation** — one meaningfully different research problem reuses the same core workflow.
10. **Controlled evolution** — failures from validation cases become explicit changes to workflow/schema/evaluation rather than ad-hoc patches.

A single successful Case 001 rerun is therefore **not sufficient** to claim that Research System v1 is reusable.

---

# 25. Final Design Position

The project should evolve through the following sequence:

```text
Prompt-driven Research
        ↓
Workflow-driven Research
        ↓
Canonical Research System
        ↓
Evaluated Research Automation
        ↓
Research Agent
```

Case 001 is the empirical foundation and reference implementation that exposed the need for this evolution. It is not the permanent architecture.

The intended end state is not:

> “a collection of better research prompts”

and not:

> “an autonomous agent that happens to do research”.

It is:

> **a reusable system that allows a human to define a research problem, execute a structured evidence-first workflow, preserve canonical knowledge and provenance, evaluate the result, generate audience-specific deliveries, and update the research over time — while progressively turning stable parts of that workflow into automation, Skills, and eventually Agents.**

The most important architectural test is therefore:

> **Can the same system solve two materially different research problems without being redesigned from scratch?**

That is the central definition of “reusable” for Research System v1.