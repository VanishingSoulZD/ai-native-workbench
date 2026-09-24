# Case 002 — Research Workspace & Execution Briefs

> Purpose: Establish the durable execution contract for Case 002 after approval of the Research Charter and AI Work Plan.
>
> Status: **Execution workspace established**
>
> Created: 2026-09-24
>
> Governing Charter: `00-research-charter.md` — v1.0 — approved for execution
>
> Governing Work Plan: `01-ai-work-plan.md` — v1.0
>
> This file is an execution aid. It does **not** contain research findings, product selections, rankings, or final conclusions.

---

## 1. Workspace Contract

### 1.1 Authority

The following files are authoritative in descending semantic order:

1. `00-research-charter.md` — defines **What / Why**, scope, population, definitions, evidence rules, cutoff, deliverables, and human decisions.
2. `01-ai-work-plan.md` — defines the approved **How**, including products, modes, sessions, inputs, outputs, handoffs, and verification.
3. `research-packets/task-briefs.md` — defines short execution contracts derived from the Charter + Work Plan.
4. Downstream research packets and evidence artifacts — record the work actually produced under those contracts.
5. Chat transcripts — **not authoritative state**.

No downstream artifact may silently override the Charter. If execution reveals a material Charter conflict, stop and trigger replanning rather than changing scope inside a research packet.

### 1.2 Snapshot

- Research cutoff: **2026-09-24**
- Primary population: **Product / Product Family**
- Umbrella term: **Work AI**
- China view: **China Representative Top 5**
- Global view: **Global Representative Top 10**
- Top 10 / Top 5 interpretation: **representative research sets, not universal quality rankings**
- No fixed numeric scoring formula is authorized by the Charter.

Time-sensitive product claims must be anchored to the 2026-09-24 snapshot. Later evidence may be used only when it is explicitly justified as describing a pre-cutoff state.

### 1.3 Workspace layout

The case workspace is logically organized as:

```
cases/002-ai-work-agent-landscape/
├── 00-research-charter.md
├── 01-ai-work-plan.md
├── research-packets/
│   ├── task-briefs.md
│   ├── global-candidate-universe.md
│   ├── global-landscape.md
│   ├── product-cards.md
│   ├── china-landscape.md
│   └── orchestration-patterns.md
├── evidence/
│   ├── claim-evidence-ledger.csv
│   └── source-register.csv
├── analysis/
│   ├── canonical-research-model.md
│   └── human-review-gate.md
└── final/
    ├── research-note.md
    ├── research-note.pptx
    └── research-note.html
```

Git does not persist empty directories. Producer tasks should create the listed artifacts when the relevant work begins; no empty placeholder files are required.

### 1.4 Artifact lifecycle

Each durable artifact should be treated as:

```
DRAFT → REVIEW → FROZEN → CONSUMED
```

Rules:

- **DRAFT** — producer is still working.
- **REVIEW** — producer believes the artifact satisfies its brief and it is ready for verification / human review.
- **FROZEN** — downstream consumers may rely on it as the current authority.
- **CONSUMED** — downstream work has used it; the artifact remains immutable unless a new version is explicitly produced.
- Do not overwrite a frozen artifact to repair an unrelated downstream issue.
- Material corrections require an explicit version increment or a new corrective artifact, with downstream consumers notified.

---

## 2. Common Execution Rules

### 2.1 Preserve the Charter

Every execution session must preserve:

- Knowledge Work / Work AI as the umbrella framing;
- product / product family as the research unit;
- global + China regional scope;
- representative-set interpretation of Top 10 / Top 5;
- evidence-first source hierarchy;
- 2026-09-24 snapshot integrity;
- Fact / Evidence / Analysis / Judgment / Unknown separation;
- explicit treatment of borderline cases;
- human ownership of consequential decisions and final approval.

### 2.2 Research only the required layer

Do not perform broad research in a task that only needs transformation, normalization, QA, or delivery formatting.

Use the smallest effective AI/tool set described in the Work Plan.

Before adding another AI or research engine, identify the concrete capability or reliability gap that the additional system fills.

### 2.3 Evidence discipline

For material claims, preserve:

```
Claim
↓
Evidence
↓
Source
↓
Date
↓
Confidence / Limitation
```

Use the Charter source hierarchy:

1. Tier 1 — official product/documentation/pricing/release/announcement/repository/company sources.
2. Tier 2 — strong independent evidence.
3. Tier 3 — credible practitioner/community evidence.
4. Tier 4 — individual reviews/blogs, primarily for workflow experience or issue discovery.

Do not treat:

- a vendor capability statement as independent proof of effectiveness;
- a model benchmark as proof of end-to-end product capability;
- absence of evidence as evidence of absence.

### 2.4 Product vs model

Every product brief must distinguish:

```
Underlying Model
→ Product / Agent Runtime
→ Context / Memory / Tools / Execution
→ Product Experience
→ Work Capability
→ Workflow Outcome
```

Do not attribute a model-level benchmark or capability directly to the complete Work AI product without supporting product evidence.

### 2.5 Handoff discipline

All task handoffs must use durable repository artifacts.

Every handoff must specify:

- producer;
- artifact;
- consumer;
- purpose / transformation;
- verification boundary.

Chat history may help an operator continue work but is never the sole handoff state.

---

# 3. Execution Brief A — Global Landscape

## 3.1 Consumer tasks

- Task 2.1.1 — Build broad Global candidate universe and boundary map.
- Task 2.2.1 — Select Global Representative Top 10 and record inclusion/exclusion logic.

## 3.2 Objective

Establish a broad and evidence-traceable view of the global Work AI population before narrowing to the representative Global Top 10.

The work must explain **what kinds of products exist and why particular products are materially relevant**, rather than starting from a memorized list of famous AI brands.

## 3.3 Scope to cover

At minimum consider:

- general-purpose AI with substantial Knowledge Work capability;
- Office / productivity-suite AI;
- work-oriented assistants and agents;
- agentic Knowledge Work products;
- enterprise-first Work AI;
- AI-native Knowledge Work products;
- emerging products with meaningful workflow or ecosystem significance;
- adjacent products when needed to explain the boundary.

Explicitly account for out-of-scope areas from the Charter, including pure models, pure coding agents, pure creative-generation products, pure search, pure transcription, pure RPA/workflow infrastructure, and developer/model infrastructure.

## 3.4 Required output

### Phase A — Candidate universe

Produce a broad candidate set with:

| Field | Required meaning |
|---|---|
| candidate_id | Stable local identifier |
| company | Owning / operating company |
| product_family | Research unit |
| category_bucket | Relevant Work AI category or multiple categories |
| work_surfaces | Main knowledge-work surfaces |
| work_roles | Observable or stated work roles |
| relevant_capability | Why it materially supports Knowledge Work |
| significance_evidence | Adoption, enterprise relevance, innovation, ecosystem, or other relevant evidence |
| geography_access | Global / regional availability and access notes where material |
| inclusion_status | Candidate / Borderline / Exclude |
| boundary_reason | Explicit reason for inclusion, exclusion, or ambiguity |
| source_refs | Source IDs or URLs |
| as_of | Date for change-sensitive facts |
| confidence | Confirmed / Likely / Unverified / Conflicting / Unknown |

Do not rank candidates.

### Phase B — Representative set

For each selected representative product, record:

| Field | Required meaning |
|---|---|
| representative_id | Stable identifier |
| product_family | Selected research unit |
| category_coverage | Which important category / direction it represents |
| work_significance | Evidence of material Work AI significance |
| inclusion_rationale | Evidence-backed reason it belongs in the representative set |
| meaningful_exclusions | Important candidates considered but not selected, where useful |
| borderline_status | Relevant unresolved boundary issue, if any |
| confidence | Confidence in selection rationale |
| source_refs | Supporting evidence |
| snapshot_date | 2026-09-24 or justified evidence date |

No overall quality score and no universal “best” ordering.

## 3.5 Core instructions

- Start from category buckets, not a preselected Top 10.
- Use primary sources first.
- Preserve meaningful exclusions and borderline candidates.
- Separate observed / independently evidenced behavior from vendor positioning.
- Use representative-set reasoning rather than popularity-only reasoning.
- Do not allow the selected set to become the hidden ranking rubric for later work.
- Do not begin detailed product cards before the representative set is sufficiently stable.

## 3.6 Boundary

This brief may discover and select the Global Representative Top 10, but it must not:

- write the final Research Note;
- generate PPT / HTML;
- create a permanent product→task mapping;
- turn the representative set into a universal quality ranking;
- silently change the Charter.

## 3.7 Handoff

Producer:
- Task 2.1.1 → `global-candidate-universe.md`
- Task 2.2.1 → `global-landscape.md`

Consumers:
- Task 2.3.1
- Task 4.1.1
- Task 4.2.1
- Task 5.1.1
- final synthesis tasks

Verification:
- source/date checks for material claims;
- mechanical completeness;
- human review of the representative set before final synthesis.

---

# 4. Execution Brief B — China Landscape

## 4.1 Consumer task

- Task 3.1.1 — Build and select the China Representative Top 5.

## 4.2 Objective

Produce an independent China-market view that can identify region-specific Work AI products, evidence, constraints, and workflow context without assuming that the global landscape is the answer key.

## 4.3 Scope to cover

Consider:

- mainland China general-purpose AI with material Knowledge Work capability;
- China office/productivity AI;
- China knowledge-work agents;
- China enterprise Work AI;
- AI-native Chinese products;
- relevant cross-border products that are actually available / meaningful in the China context.

## 4.4 Required output

Each candidate / representative record should include:

| Field | Required meaning |
|---|---|
| candidate_id / representative_id | Stable local identifier |
| company | Company / provider |
| product_family | Research unit |
| category | Work AI category |
| work_positioning | What knowledge work it is for |
| task_fit | Supported task classes |
| work_surfaces | Main user/work surfaces |
| agentic_capability | Relevant multi-step execution |
| context / integrations | Enterprise, workspace, web, files, etc. |
| mainland_availability | Availability in mainland China |
| access_mode | Consumer / enterprise / plan / invite / other relevant mode |
| language_support | Chinese-language support where material |
| regional_constraints | Important geography / access / feature differences |
| significance_evidence | Market/product/workflow relevance |
| top5_status | Candidate / Top 5 / Borderline / Exclude |
| inclusion_exclusion_reason | Evidence-backed rationale |
| global_overlap | Overlap with Global Representative Top 10, if applicable |
| source_refs | Source IDs / URLs |
| as_of | Evidence date |
| confidence | Evidence status |

## 4.5 Core instructions

- Establish the China candidate universe before selecting Top 5.
- Use Chinese-language and region-specific primary sources wherever available.
- Separate mainland availability, overseas availability, enterprise access, and language support when they materially differ.
- Preserve regional differences instead of forcing false equivalence with global products.
- Record overlap with global products.
- Record important borderline candidates and exclusions.
- Do not infer market significance from a single popularity signal.

## 4.6 Boundary

No final global-vs-China synthesis is produced here.

Do not silently modify the Global Top 10.

## 4.7 Handoff

Producer:
- Task 3.1.1 → `china-landscape.md`

Consumers:
- Task 3.2.1
- Task 4.1.1
- Task 4.2.1
- Task 5.1.1
- final synthesis tasks

Verification:
- source/date checks;
- ChatGPT normalization and contradiction review;
- human review of the China Top 5.

---

# 5. Execution Brief C — Product Cards

## 5.1 Consumer tasks

- Task 2.3.1 — Global representative product cards.
- Task 3.2.1 — Normalize China Top 5 against the common schema.

## 5.2 Objective

Describe what each representative Work AI product **actually is for in a knowledge worker workflow**, using a common schema that supports task-fit, role, interaction, execution, and orchestration analysis.

## 5.3 Required card schema

Every product card must contain:

### Identity
- product family;
- company;
- region label: Global / China / Both;
- source / snapshot date.

### Work positioning
- one concise statement answering: “What is this AI for?”
- primary work roles;
- important secondary roles;
- product type / archetype as an analytical label, not a permanent category.

### Task fit
Assess, with evidence:

- research;
- synthesis;
- writing;
- editing;
- document transformation;
- presentation;
- communication;
- meeting work;
- analysis;
- planning;
- structured knowledge work;
- multi-step execution.

Do not mark a task as supported solely because the vendor mentions the keyword.

### Work interaction model
Record:

- prompt-driven vs workflow-driven;
- one-shot vs iterative;
- chat vs workspace vs artifact-centric;
- persistent context;
- project / memory mechanisms;
- delegation / review patterns;
- human-in-the-loop checkpoints.

### Agentic execution
Where applicable:

- planning;
- context gathering;
- tool use;
- browser / external-system interaction;
- file manipulation;
- artifact creation;
- long-running execution;
- verification;
- retry / repair;
- approval boundaries.

### Artifact model
Record durable outputs such as:

- documents;
- spreadsheets;
- presentations;
- reports;
- research packages;
- structured data;
- task results;
- other durable work artifacts.

### Integration / context
Record material support for:

- email;
- calendar;
- cloud storage;
- office suites;
- enterprise knowledge;
- web;
- third-party applications;
- connected workspaces;
- identity / permissions / enterprise context.

### Usage model
Classify observed / supported patterns such as:

- direct Q&A;
- iterative co-working;
- delegation;
- long-running / background work;
- artifact review;
- continuous project context;
- specialist invocation;
- verification.

### Orchestration role
Describe the plausible role(s):

- primary worker;
- researcher;
- analyst;
- specialist;
- synthesizer;
- operator;
- creator / transformer;
- reviewer;
- coordinator.

State only roles supported by evidence or clearly labeled analysis.

### Constraints / economics
Where material to task fit:

- pricing model;
- usage limits;
- access / geography;
- plan tier;
- enterprise restrictions;
- setup / switching friction;
- important workflow constraints.

### Evidence / uncertainty
Separate:

- Product fact;
- Vendor claim;
- Independent evidence;
- Analysis;
- Unknown / unresolved.

Every material change-sensitive claim must carry an evidence date.

## 5.4 Core instructions

- Separate product capability from underlying model capability.
- Prefer official product documentation for product facts.
- Use independent evidence where it is needed to validate observed workflow behavior, adoption, or comparative claims.
- Record uncertainty rather than filling gaps through inference.
- Keep Global and China regional differences explicitly labeled.
- Do not synthesize the final Work AI taxonomy here.
- Do not generate a permanent product-to-task mapping.

## 5.5 Boundary

Product Cards are an evidence-bearing characterization layer.

They are **not**:

- a final report;
- a universal recommendation;
- a quality score;
- a permanent product catalog;
- a substitute for the evidence ledger.

## 5.6 Handoff

Producer:
- Task 2.3.1 → Global section of `product-cards.md`
- Task 3.2.1 → China section / normalized China cards in `product-cards.md`

Consumers:
- Task 4.1.1
- Task 4.2.1
- Task 5.1.1
- final synthesis tasks

Verification:
- required-field completeness;
- source audit;
- cross-product schema consistency;
- region labels preserved.

---

# 6. Execution Brief D — Work AI Taxonomy / Orchestration

## 6.1 Consumer tasks

- Task 4.1.1 — Canonical Work AI taxonomy, task-to-capability map, and work-role map.
- Task 4.2.1 — Recurring orchestration patterns and one-AI sufficiency analysis.

## 6.2 Objective

Translate evidence-backed product observations into a reusable decision model:

```
Knowledge Work Task
→ Required Capability
→ Work AI Category / Role
→ Candidate Product
→ Usage Pattern
→ Human / AI Allocation
→ Potential Multi-AI Handoff
```

The model must remain reusable without becoming a hard-coded timeless product map.

## 6.3 Required analytical layers

### Layer A — Terminology / category model

Explain the relationships among:

- Knowledge Work;
- AI for Knowledge Work;
- Work AI;
- Work Agent;
- Office AI;
- adjacent categories.

Derive boundaries from evidence and Charter definitions.

### Layer B — Task → capability

Identify the capabilities a task actually requires, e.g.:

- retrieval;
- source discovery;
- synthesis;
- reasoning;
- drafting;
- transformation;
- structured analysis;
- tool execution;
- artifact production;
- verification;
- coordination.

### Layer C — Capability → Work AI role

Map capabilities to analytical work roles such as:

- researcher;
- analyst;
- writer;
- editor;
- planner;
- coordinator;
- document worker;
- meeting assistant;
- knowledge interface;
- operator;
- execution agent;
- reviewer.

These labels are explanatory, not permanent market categories.

### Layer D — Orchestration patterns

For each recurring pattern define:

| Field | Required meaning |
|---|---|
| pattern_id | Stable local identifier |
| name | Short pattern name |
| task_shape | Work situation that triggers the pattern |
| one_ai_baseline | What one capable AI can already do |
| added_ai_role | What additional AI contributes |
| capability_gap | Concrete capability/reliability gap |
| producer | Producer of the handoff artifact |
| artifact | Durable handoff object |
| consumer | Receiving AI / human |
| purpose | Why the handoff exists |
| verification_boundary | Where correctness is checked |
| human_boundary | Human approval / judgment point |
| recurrence_evidence | Why this appears repeatable rather than anecdotal |
| limitations | When the pattern should not be used |

### Layer E — One-AI sufficiency

Explicitly state when:

- one capable AI is sufficient;
- adding another AI only duplicates web research or synthesis;
- an extra AI creates unnecessary coordination / transfer cost;
- a second AI materially adds independent evidence, a distinct context domain, a specialist capability, or a meaningful verification function.

## 6.4 Core instructions

- Derive abstractions from repeated evidence.
- Do not start from a fixed taxonomy and force products into it.
- Every multi-AI pattern must identify the concrete reason the second AI exists.
- Preserve human review boundaries.
- Do not assume multi-AI orchestration is inherently better.
- Prefer repeatable patterns over anecdotal workflows.
- Keep product facts, evidence, analysis, judgment, and unknowns separate.

## 6.5 Boundary

This brief covers analysis and conceptual synthesis only.

It must not produce:

- executable agent automation;
- a permanent orchestration runtime;
- a fixed product-routing table;
- final presentation / report formatting.

## 6.6 Handoff

Producer:
- Task 4.1.1 → `analysis/canonical-research-model.md`
- Task 4.2.1 → `research-packets/orchestration-patterns.md`

Consumers:
- Task 5.1.1
- Task 5.2.1
- Tasks 6.1.1–6.3.1

Verification:
- independent AI review;
- evidence trace;
- human review for consequential interpretation.

---

# 7. Execution Brief E — Evidence QA

## 7.1 Consumer task

- Task 5.1.1 — Build and audit the claim-evidence ledger and source register.

## 7.2 Objective

Create the provenance layer that makes important final claims traceable and keeps the 2026-09-24 snapshot internally consistent.

## 7.3 Claim ledger schema

`evidence/claim-evidence-ledger.csv` must use, at minimum:

| Field | Required meaning |
|---|---|
| claim_id | Stable claim identifier |
| artifact | Downstream artifact(s) using the claim |
| section | Relevant section / location |
| claim | Atomic factual / comparative claim |
| claim_type | Fact / Evidence / Analysis / Judgment |
| status | Confirmed / Likely / Unverified / Conflicting / Unknown |
| evidence_summary | What the evidence actually supports |
| source_id | Primary source-register key |
| source_tier | Tier 1–4 |
| source_kind | Official / Independent / Community / Individual |
| source_date | Publication / update date when known |
| accessed_date | Date checked |
| snapshot_relevance | Why the source supports the 2026-09-24 state |
| confidence | Confidence in claim support |
| limitation | Material limitation or missing evidence |
| conflict_note | Conflicting evidence, if any |
| vendor_claim | Vendor-stated language, when relevant |
| independent_support | Independent validation, when available |

Each row should represent an atomic or tightly scoped claim. Avoid one row containing multiple unrelated propositions.

## 7.4 Source register schema

`evidence/source-register.csv` must use, at minimum:

| Field | Required meaning |
|---|---|
| source_id | Stable source identifier |
| publisher | Publisher / organization |
| title | Source title |
| url | Canonical URL |
| source_tier | Tier 1–4 |
| source_kind | Official / Independent / Community / Individual |
| published_date | Publication date when known |
| updated_date | Update date when known |
| accessed_date | Verification date |
| snapshot_scope | Whether it describes the 2026-09-24 state |
| supports_claims | Claim IDs supported |
| notes | Important context / limitations |

## 7.5 Core instructions

- Verify claim/source/date alignment.
- Prefer official sources for product facts and capabilities.
- Use independent evidence for adoption, market significance, and observed workflow claims where available.
- Keep vendor statements distinct from independent support.
- Flag post-cutoff sources.
- When a post-cutoff source describes a pre-cutoff state, record the justification.
- Preserve conflicting evidence.
- Never infer that a feature does not exist merely because a source did not mention it.
- Use targeted fresh web verification only for unresolved current-state gaps; do not reopen the entire landscape.

## 7.6 Boundary

Evidence QA may identify that an existing conclusion is no longer supportable. It may not silently change a representative-set decision or Charter requirement. A material failure that changes a selection or scope triggers explicit replanning.

## 7.7 Handoff

Producer:
- Task 5.1.1 → `claim-evidence-ledger.csv` + `source-register.csv`

Consumers:
- Task 5.2.1
- Tasks 6.1.1–6.3.1

Verification:
- mechanical schema / completeness checks;
- source checks;
- human resolution of material conflicts.

---

# 8. Execution Brief F — Final Delivery

## 8.1 Consumer tasks

- Task 6.1.1 — Research Note.
- Task 6.2.1 — PPT.
- Task 6.3.1 — HTML.

## 8.2 Objective

Produce three mutually consistent representations of the **same frozen research model and evidence base**.

```
Frozen Evidence
→ Canonical Research Model
→ Research Note
→ PPT / HTML
```

The delivery layer must not become an independent conclusion engine.

## 8.3 Required inputs

Final delivery may rely only on:

- approved Charter;
- frozen Global landscape packet;
- frozen China landscape packet;
- frozen Product Cards;
- frozen canonical research model;
- frozen orchestration patterns;
- audited claim-evidence ledger;
- source register;
- human review gate.

Unresolved material items must be surfaced, not silently resolved through prose.

## 8.4 Research Note contract

`final/research-note.md` must cover, at minimum:

- research framing and terminology;
- candidate universe and inclusion / exclusion logic;
- Global Representative Top 10;
- China Representative Top 5;
- product-level work positioning;
- task-fit and capability analysis;
- Work AI taxonomy;
- usage patterns;
- orchestration roles and recurring workflow patterns;
- cross-product comparison;
- evidence and uncertainty;
- research-backed practical implications.

The note must support the real-world decision objective:

> Given a concrete Knowledge Work task, identify a relevant AI capability class, candidate products, appropriate usage pattern, and human / AI allocation.

## 8.5 PPT contract

The PPT must communicate the same model efficiently, including:

- Work AI category definition;
- 2026 landscape;
- representative products;
- major product archetypes;
- task / capability map;
- work-role map;
- orchestration patterns;
- key implications.

No slide may introduce a material conclusion unsupported by the frozen research note / canonical model.

## 8.6 HTML contract

The HTML representation should support:

- landscape exploration;
- product comparison;
- task-fit navigation;
- work-role / orchestration views;
- evidence traceability.

Navigation and displayed claims must remain synchronized with the Research Note and evidence ledger.

## 8.7 Boundary

Final delivery tasks must not:

- perform broad new market research;
- reselect the Global Top 10 / China Top 5;
- invent unsupported product capabilities;
- silently change taxonomy;
- create a new permanent product-to-task mapping.

Targeted factual correction is allowed only when a verified error is found and the correction can be traced to the evidence layer; material model changes return to the appropriate upstream task.

## 8.8 Handoff

Producer:
- Task 6.1.1 → `final/research-note.md`
- Task 6.2.1 → `final/research-note.pptx`
- Task 6.3.1 → `final/research-note.html`

Consumer:
- final human delivery review.

Verification:
- source / claim consistency;
- slide-to-note consistency;
- HTML navigation and evidence-link checks;
- human final approval.

---

# 9. Cross-Task Handoff Matrix

| Producer | Durable artifact | Primary consumer | Purpose |
|---|---|---|---|
| 1.1.1 | `research-packets/task-briefs.md` | 2.1.1–6.3.1 | Common execution contracts, schemas, and boundaries |
| 2.1.1 | `research-packets/global-candidate-universe.md` | 2.2.1, 5.1.1 | Broad global selection universe |
| 2.2.1 | `research-packets/global-landscape.md` | 2.3.1, 4.1.1, 5.1.1 | Evidence-backed Global Representative Top 10 |
| 2.3.1 | `research-packets/product-cards.md` (Global) | 4.1.1, 4.2.1, 5.1.1 | Common product-level evidence substrate |
| 3.1.1 | `research-packets/china-landscape.md` | 3.2.1, 4.1.1, 5.1.1 | Independent China-market evidence |
| 3.2.1 | `research-packets/product-cards.md` (China) | 4.1.1, 4.2.1, 5.1.1 | Region-normalized product evidence |
| 4.1.1 | `analysis/canonical-research-model.md` | 4.2.1, 5.2.1, 6.1.1–6.3.1 | Canonical analytical model |
| 4.2.1 | `research-packets/orchestration-patterns.md` | 5.1.1, 6.1.1–6.3.1 | Workflow / orchestration model |
| 5.1.1 | `evidence/claim-evidence-ledger.csv` + `source-register.csv` | 5.2.1, 6.1.1–6.3.1 | Evidence authority |
| 5.2.1 | `analysis/human-review-gate.md` | 6.1.1–6.3.1 | Human approval authority |
| 6.1.1 | `final/research-note.md` | 6.2.1, 6.3.1 | Canonical narrative delivery |
| 6.2.1 | `final/research-note.pptx` | Human | Presentation delivery |
| 6.3.1 | `final/research-note.html` | Human | Interactive delivery |

---

# 10. Execution Gate for Task 1.1.1

Task 1.1.1 is complete when all of the following are true:

- [x] The authoritative case context is identified.
- [x] The 2026-09-24 snapshot is explicit.
- [x] The durable case workspace layout is defined.
- [x] The repository is declared the system of record.
- [x] Durable artifact lifecycle rules are defined.
- [x] Short execution briefs exist for Global, China, Product Cards, Orchestration, Evidence QA, and Delivery.
- [x] Required schemas are defined before research begins.
- [x] Each brief states its scope and execution boundary.
- [x] Each planned handoff identifies producer, artifact, consumer, purpose, and verification.
- [x] Evidence and uncertainty rules are repeated at the execution-contract layer.
- [x] No research findings or product rankings have been populated.
- [x] No Charter requirement has been intentionally changed.

Next execution gate:

> Human / mechanical review of this workspace contract before Task 2.1.1 begins.
