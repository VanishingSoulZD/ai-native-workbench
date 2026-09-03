# Research System v1

> Repository-level design specification for `ai-native-workbench`
>
> Status: **Design baseline**
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

The first Research Case exposed three structural limitations in a prompt-driven workflow:

1. Each research phase could be completed successfully, while the overall method remained dependent on repeated natural-language prompting.
2. Phase 8 produced structured datasets and presentation assets, but the transformation from earlier research artifacts into those datasets was not fully reproducible.
3. Research, canonical knowledge, evaluation, and delivery were mixed across phase-oriented files, making it difficult to know which artifacts should be reused, audited, updated, or presented externally.

Case 001 therefore serves two purposes:

- **Research output:** understand the 2026 AI Coding Agent landscape.
- **System experiment:** discover which parts of high-quality research can be standardized and engineered.

The system-level objective is therefore not “make Case 001 better”. It is:

> **Extract a reusable research operating model from real work, validate it against new cases, and only then automate stable portions of it.**

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

Evidence should retain enough provenance to understand:

- where it came from;
- when it was observed;
- what exactly was observed;
- what kind of evidence it is;
- what claim(s) it supports or contradicts.

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

R5 is where phase-oriented working papers become a reusable knowledge asset.

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

A future implementation may use:

- a prompt template;
- a Python function;
- a CLI command;
- an LLM call;
- a browser/search tool;
- a human form;
- a combination of these.

The workflow contract remains stable even when execution technology changes.

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

Examples:

- Research Charter;
- Research Plan;
- taxonomy;
- scope rules;
- success criteria.

Purpose: define the research.

## 6.2 Working Artifacts

Examples:

- candidate universe;
- market evidence;
- product research;
- benchmark research;
- cross-product analysis;
- decision working paper.

Purpose: support research execution and preserve reasoning trace.

These are important, but they are not automatically the final knowledge source of truth.

## 6.3 Canonical Knowledge Artifacts

Examples:

- canonical registry;
- claims;
- evidence;
- sources;
- judgments;
- recommendations;
- hypotheses;
- unknowns;
- relationships;
- scores / metrics;
- research snapshot.

Purpose: preserve what the research actually knows and how it knows it.

## 6.4 Evaluation Artifacts

Examples:

- validation report;
- citation audit;
- consistency report;
- coverage assessment;
- human review record;
- final quality report.

Purpose: evaluate research quality.

## 6.5 Delivery Artifacts

Examples:

- executive PPT;
- research report / note;
- HTML explorer;
- dataset export;
- source / audit package.

Purpose: communicate or reuse canonical knowledge.

---

# 7. Canonical Research Model

The Canonical Research Model is the semantic center of the system.

It follows:

> **One Canonical Model, Many Renderings.**

The canonical model must not be derived by reading one already-rendered output and copying it into another. Instead, delivery artifacts project from the same canonical data and provenance layer.

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

And the reasoning chain:

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

Unknown must not be represented as:

- blank;
- zero;
- “No”;
- “—”;
- an inferred negative.

The state must remain semantically distinct from confirmed absence.

## 7.5 Historical Decisions

Historical rankings, scores, or decisions are immutable within a research snapshot unless a new human-approved research action explicitly creates a new version.

Phase 8 should not silently “fix” earlier phases merely because a discrepancy is discovered.

---

# 8. Provenance and Citation Model

Every important claim that appears in canonical knowledge or delivery assets should have a provenance path.

Required conceptual chain:

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

A Source identifies the citable document or artifact.

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

Evidence records what was observed from a source.

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

Claims are atomic enough to audit individually.

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

Not every sentence in a delivery artifact requires identical citation granularity. At minimum:

- externally verifiable factual claims → provenance required;
- quantitative claims → provenance + qualifier required;
- major analytical judgments → supporting claim/evidence chain required;
- hypotheses → explicitly labeled as hypotheses and not represented as established facts;
- unknowns → explicitly represented and preserved.

---

# 9. Human Judgment Gates

The system is intentionally Human-in-the-loop.

## H1 — Research Scope Gate

Human approves:

- research question;
- boundaries;
- research unit;
- key definitions;
- cutoff / snapshot definition.

## H2 — Research Population / Selection Gate

Human reviews consequential inclusion, exclusion, ranking, and exception decisions.

## H3 — Judgment Gate

Human reviews important strategic conclusions, recommendations, major inference, and unresolved ambiguity.

## H4 — Final Delivery Gate

Human reviews the final delivered artifact for:

- factual correctness;
- citation integrity;
- wording;
- uncertainty representation;
- audience appropriateness;
- compression distortion.

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
- rank / score invariant checks;
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

Evaluation results should themselves be archived because they reveal:

- where the workflow fails;
- where automation is unsafe;
- which steps deserve stronger validation;
- what should change in the next workflow version.

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
- configuration / assumptions;
- model-generated inputs when relevant.

## 11.2 Build Outputs

The build should generate, rather than manually maintain where feasible:

- canonical datasets;
- source ledger;
- research note;
- HTML explorer;
- executive presentation;
- validation report.

## 11.3 Build Boundaries

A renderer must not silently introduce new research.

A renderer may:

- transform;
- format;
- compress;
- visualize;
- reorder for presentation;

but should not invent new facts or judgments.

## 11.4 Case 001 Implication

Case 001 currently has `08-dataset/candidates.csv` and `08-dataset/products.csv` plus a `08-presentation/build_assets.py` generator. The missing reproducible transformation from Phase 1–7 research artifacts into those datasets is therefore a real system gap.

For Case 001, the target chain is:

```text
Phase 0–7 working artifacts
        ↓
build_dataset
        ↓
Canonical / normalized dataset
        ↓
validate
        ↓
build_assets
        ↓
Research Note / HTML / PPT / exports
```

The existing `build_assets.py` should ultimately consume canonical data rather than carrying duplicate hand-authored research content.

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

It intentionally compresses information and therefore has the highest compression-distortion risk.

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

Optimized for:

- query;
- filtering / exploration;
- comparison;
- matrix inspection;
- evidence lookup;
- uncertainty / unknown inspection.

## 12.4 Dataset

Optimized for:

- rebuilding visualizations;
- analysis;
- downstream automation;
- update workflows;
- future agent consumption.

## 12.5 Source / Audit Package

Optimized for:

- source verification;
- citation review;
- discrepancy investigation;
- research handoff.

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

When a standard case template is mature enough, it should support initialization of a new case without requiring the researcher to manually recreate the workflow from old prompts.

Conceptually:

```text
research init
      ↓
Case Skeleton
      ↓
Research Charter
      ↓
Reusable Workflow
      ↓
Case-specific configuration
```

---

# 14. Case 001 Mapping to Research System v1

Case 001 is the reference implementation and retrospective source for this model.

The current phase structure can be mapped approximately as follows:

| Case 001 artifact / phase | Research System v1 role |
|---|---|
| `00-research-charter.md` | R0 Definition |
| `01-candidate-universe.md` | R1 Discovery / Working |
| `02-market-evidence.md` | R2 Evidence / Working |
| `03-ranking-methodology.md` | R3 Analysis / Method definition |
| `03-top10-selection.md` | R4 Decision |
| `04-products/` | R2 Evidence + R3 Analysis / Working |
| `05-benchmarks.md` | R2 Evidence + R3 Analysis / Working |
| `06-cross-product-analysis.md` | R3 Analysis |
| `07-decision.md` | R4 Decision |
| `08-canonical-research-model.md` | Canonical model specification |
| `08-dataset/` | Canonical / normalized export |
| `08-sources.md` | Provenance / source ledger |
| `08-research-note.md` | Canonical narrative delivery |
| `08-presentation/landscape.html` | Interactive delivery |
| `08-presentation/executive-summary.pptx` | Executive delivery |

This mapping is deliberately not a one-to-one replacement of the existing case files. The Phase files remain useful as historical working papers and research trace.

The key architectural change is that **future cases should not treat the phase numbering itself as the reusable interface**.

---

# 15. Research Case vs Research System

A Case answers:

> “What did we learn about this particular problem?”

The Research System answers:

> “How do we repeatedly produce trustworthy research for different problems?”

Therefore:

```text
Case 001
   ↓
Workflow Prototype
   ↓
Research System v1
   ↓
Case 002
   ↓
Generalization Test
   ↓
Research System v2
```

Case 002 is not just the next research topic. It is also a test of whether the abstractions extracted from Case 001 actually generalize.

---

# 16. Promotion Rules: Case-specific → Reusable System Capability

A capability should move from a Case directory into `workflows/`, `skills/`, or `evaluations/` only when its reuse boundary is understood.

## Promote to Workflow when:

- the procedure recurs;
- inputs / outputs are stable;
- the purpose is clear;
- quality can be evaluated.

## Promote to Skill when:

- the workflow step benefits from reusable specialized instructions or tooling;
- the behavior can be invoked independently;
- its interface is narrower than the whole Research Workflow.

## Promote to Agent when:

- the workflow has already been validated;
- the task contains sufficient repeatable work;
- automation has measurable benefit;
- failure modes and human gates are understood.

## Promote to Evaluation Capability when:

- the quality check is reusable across multiple cases;
- the check is sufficiently deterministic or has a defined human-review protocol.

---

# 17. Versioning Model

The Research System has at least three independent version axes:

```text
Workflow Version
Schema / Canonical Model Version
Research Snapshot Version
```

Example:

```text
workflow: 1.2
schema: 1.1
case snapshot: 2026-09-15
```

A new workflow version does not retroactively rewrite an old research snapshot.

A new research snapshot may use a newer workflow and therefore must record the relevant versions.

---

# 18. Failure and Exception Model

The system should explicitly represent common research failure states.

## 18.1 Insufficient Evidence

Represent the claim as low-confidence, provisional, or unknown rather than filling the gap with speculation.

## 18.2 Contradictory Evidence

Preserve competing evidence and record the contradiction. Do not silently choose one source unless the methodology explicitly defines the adjudication rule.

## 18.3 Ambiguous Entity

Create an explicit unresolved entity state or ambiguity record rather than silently merging distinct products or companies.

## 18.4 Historical Discrepancy

Preserve the historical value in the relevant snapshot and record the discrepancy separately. Corrections require a human-approved versioned action.

## 18.5 Rendering Failure

Delivery failure must never corrupt canonical research data. Rendering should be repeatable from the same canonical inputs.

---

# 19. Operational Division of Labor

The system is designed around capability allocation rather than “AI does everything”.

## Human responsibilities

```text
Problem Framing
Research Scope
Key Definitions
Important Judgment
Decision
Final Review
```

## AI / automation responsibilities

```text
Search assistance
Extraction
Normalization
Summarization
Candidate analysis
Structured transformation
Validation assistance
Draft generation
Rendering
Repetitive updates
```

The actual allocation may evolve after evaluation. No role is permanently automated merely because it is technically automatable.

---

# 20. Target Architecture

The conceptual architecture is:

```text
                         RESEARCH REQUEST
                                │
                                ▼
                         ┌──────────────┐
                         │ R0 DEFINE    │
                         │ Charter      │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R1 DISCOVER   │
                         │ Population   │
                         │ Source Map   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R2 EVIDENCE   │
                         │ Claims       │
                         │ Evidence     │
                         │ Sources      │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R3 ANALYZE    │
                         │ Models       │
                         │ Comparisons  │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ R4 DECIDE     │
                         │ Judgments    │
                         │ Decisions    │
                         └──────┬───────┘
                                │
                           HUMAN GATE
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
                         │ Mechanical   │
                         │ + Human      │
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

A future Research Agent should execute selected workflow steps inside this architecture. It should not replace the architecture.

---

# 21. Repository Boundary

The repository should gradually align its existing top-level responsibilities with the system model:

```text
cases/
    Real research cases and case-specific artifacts

workflows/
    Validated reusable research workflows

skills/
    Reusable specialized capabilities used by workflows

agents/
    Automated execution of sufficiently validated workflows

evaluations/
    Reusable research-quality evaluation logic and protocols

docs/
    System methodology, design decisions, and long-term principles
```

This does **not** authorize premature implementation of empty future layers.

A directory becomes “real” when a concrete workflow or case has demonstrated the need for the shared capability.

---

# 22. Implementation Roadmap

Research System v1 should be built in the following order.

## Step 1 — Case 001 Retrospective

Map every existing Case 001 phase and artifact into:

- lifecycle step;
- artifact class;
- canonical authority;
- human gate;
- validation;
- delivery role.

## Step 2 — Reproducible Phase 8 Build

For Case 001:

- implement dataset extraction / normalization;
- remove duplicated hard-coded research data from renderers;
- validate canonical data;
- regenerate outputs from canonical inputs.

## Step 3 — Research Workflow v1

Extract the recurring workflow steps from Case 001 and give them explicit interfaces.

## Step 4 — Evaluation v1

Implement reusable mechanical checks and a human review protocol.

## Step 5 — Case Template v1

Create the smallest practical scaffold that allows a new research case to instantiate the workflow without recreating it from old prompts.

## Step 6 — Case 002 Generalization Test

Use a meaningfully different research problem to test whether the abstraction is genuinely reusable.

## Step 7 — Automation / Skills

Automate only the stable, repeated, evaluated steps.

## Step 8 — Research Agent

Only after the workflow and evaluation boundaries are demonstrated should an Agent become the execution layer.

---

# 23. Non-Goals for v1

Research System v1 will not attempt to:

- solve every research domain;
- guarantee factual correctness automatically;
- eliminate human judgment;
- create a fully autonomous multi-agent system;
- build a general-purpose database platform before the data model proves stable;
- force all cases into identical files;
- optimize for code volume;
- optimize for maximum automation at the expense of auditability.

---

# 24. Success Criteria

Research System v1 is considered validated when a new case can satisfy all of the following without recreating the entire process from ad-hoc prompts:

1. A researcher can define a Research Charter using a reusable interface.
2. A reusable workflow can execute the recurring research lifecycle.
3. Important claims can be traced to evidence and sources.
4. Canonical knowledge can be validated independently from presentation rendering.
5. At least two different delivery formats can be generated from the same canonical source.
6. Mechanical quality checks can detect at least the main classes of structural inconsistency.
7. Human judgment gates are explicit rather than implicit.
8. A research snapshot can be rebuilt or substantially reproduced from declared inputs and workflow versions.
9. A second research case can reuse the workflow without inheriting Case 001's topic-specific assumptions.

The decisive success criterion is:

> **The researcher should spend less time reconstructing the research process and more time thinking about the actual research problem.**

---

# 25. Final Design Position

The intended evolution is:

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

The repository should therefore resist the temptation to jump directly from “AI can do research” to “build a Research Agent”.

The strategic sequence is:

```text
Real Task
   ↓
Human Work
   ↓
AI Collaboration
   ↓
Reusable Workflow
   ↓
Canonical Knowledge
   ↓
Evaluation
   ↓
Automation
   ↓
Agent / Skills / System
```

> **The ultimate product of `ai-native-workbench` is not a Research Agent. It is a reusable way of doing high-quality knowledge work with AI, with Research as the first proving ground.**
