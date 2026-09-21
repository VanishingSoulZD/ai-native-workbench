# AI Native Workbench Direction Alignment Design

> Status: Draft for review
>
> Date: 2026-09-21
>
> Repository: `VanishingSoulZD/ai-native-workbench`
>
> Scope: Final alignment after Step 1–4 direction, relationship, Advisor, and Session Template design approval.

---

## 0. Purpose

This spec records the final architectural alignment of `ai-native-workbench` after the approved Step 1–4 design.

The repository is no longer organized around a staged roadmap whose primary objective is to build a Research System and eventually a Research Agent.

The repository is instead a long-lived personal laboratory for developing **AI-native work capability through real tasks**.

Research remains a first-class capability area and an important execution substrate, but it is no longer the top-level project identity.

This document defines:

1. the canonical project positioning and work chain;
2. the relationship among Research Charter, AI Work Advisor Prompt, AI Work Plan, and execution;
3. the four formal reusable work-guidance artifacts;
4. the boundary between the Workbench, Research System, Research Runtime, and AI Work Advisor;
5. the required documentation alignment;
6. the treatment of the existing Research Runtime v1 work;
7. the transition point into Case 002.

Historical Research System / Runtime design documents remain historical records unless explicitly updated by a future decision.

---

# 1. Canonical Project Position

## 1.1 Mission

> **通过真实任务，学习、实践和沉淀 AI 原生工作能力。**

English:

> Build a personal laboratory for developing AI-native work capabilities by applying the current AI ecosystem to real-world tasks.

The project is not primarily:

- an AI Agent product;
- a Research Agent;
- a Research Runtime;
- an AI tool catalog;
- an automation platform.

These can be implementation or experimentation surfaces when real work requires them, but they are not the repository's top-level purpose.

## 1.2 Core capability goals

The two highest-level capability goals are:

### Goal A — AI Task → AI Selection

Given a real task, determine:

- what capabilities are required;
- what AI capability is appropriate;
- which current AI product / model / mode is fit for the task;
- how it should be configured.

### Goal B — AI Selection → AI Orchestration

Given the selected AI capabilities, determine:

- whether one AI is sufficient;
- which tasks should be split;
- how multiple AIs should hand off work;
- what artifacts should be persisted between stages;
- where verification occurs;
- where human judgment remains mandatory.

The project therefore trains **selection and orchestration methodology**, not permanent product mappings.

---

# 2. Canonical Work Chain

The canonical project-wide chain is:

```text
Real Task
    ↓
Problem Framing
    ↓
AI Work Planning
    ↓
AI Capability Selection
    ↓
AI Product / Model Selection
    ↓
AI Tool Configuration
    ↓
AI Orchestration
    ↓
Artifacts / Evidence
    ↓
Human Judgment
    ↓
Final Delivery
    ↓
Evaluation
```

This chain is the top-level Workbench model.

Research is one important specialization of this chain:

```text
Problem Framing
→ Research
→ Evidence
→ Analysis
→ Judgment
→ Writing
→ Delivery
→ Evaluation
```

The Research System must therefore be treated as a **capability subsystem** within the broader Workbench rather than as the definition of the entire project.

---

# 3. Canonical Planning Relationship

The authoritative planning relationship is:

```text
Research Charter
       ↓
AI Work Advisor Prompt
       ↓
AI Work Plan
       ↓
Actual Execution
```

The Advisor may dynamically acquire current ecosystem knowledge during planning.

For avoidance of ambiguity, the canonical data flow is:

```text
Research Charter
+
AI Work Advisor Prompt
+
Optional user / environment constraints
       ↓
Advisor need-driven ecosystem discovery
       ↓
AI Work Plan
       ↓
Human review
       ↓
Execution
```

**Current AI Ecosystem Knowledge is not a mandatory third reusable input artifact.**

It is information the Advisor obtains when planning requires it.

---

# 4. Responsibility of Each Artifact

## 4.1 Research Charter

**Question answered:** What problem are we solving and why?

The Charter is case-specific and defines:

- objective;
- research questions;
- scope and boundaries;
- research population;
- definitions;
- inclusion / exclusion;
- research dimensions;
- comparison or ranking requirements;
- evidence requirements;
- research cutoff / snapshot;
- expected deliverables;
- success criteria;
- assumptions / open questions;
- explicit human decisions and approvals.

The Charter is the authority for task intent.

It must not silently absorb AI tool-selection decisions.

## 4.2 AI Work Advisor Prompt v1

**Question answered:** How should the current AI ecosystem be used to solve this problem?

The Advisor Prompt is reusable methodology.

It defines decision protocol, not permanent tool mappings.

It must:

1. understand the task before selecting tools;
2. decompose work;
3. identify required AI capabilities;
4. identify current-ecosystem knowledge requirements;
5. acquire and verify relevant current ecosystem knowledge;
6. generate candidate AI options;
7. select products and models by task fit;
8. configure reasoning / thinking;
9. choose session, context, file, connector, skill, and instruction strategies;
10. decide whether one AI is enough;
11. design AI handoffs and orchestration;
12. define artifacts;
13. define verification;
14. preserve human judgment boundaries;
15. self-review the resulting plan.

The Advisor must not:

- expose hidden chain-of-thought;
- silently modify the Charter;
- select tools before understanding the task;
- select by popularity alone;
- maximize tool count;
- recommend rebuilding capabilities that suitable existing AI already provides;
- treat unverified claims as confirmed;
- perform the actual research merely because it is capable of doing so.

## 4.3 AI Work Plan

**Question answered:** For this case, what exactly should each meaningful task use, and how?

The Work Plan is case-specific and acts as an execution manual.

Each meaningful task should be expressible with the following structured fields:

- Purpose
- Required Capability
- Recommended Product
- Model
- Mode
- Thinking
- Session
- Context
- Files
- Connectors
- Skills
- Input
- Instruction
- Expected Output
- Artifact
- Execution Boundary
- Handoff
- Verification
- Rationale
- Alternatives Considered

The Work Plan also contains:

1. plan metadata;
2. executive work strategy;
3. ecosystem selection summary;
4. global execution rules;
5. detailed Stage / Step / Task plan;
6. artifact and handoff map;
7. verification and human review;
8. assumptions and uncertainties.

The Work Plan should record why meaningful alternatives were rejected.

It must not become a global playbook or a permanent product map.

## 4.4 Session Opening Templates

There are two distinct session templates:

### A — Research Charter Discussion Session

Purpose:

> Turn an initial real-world objective into an approved `00-research-charter.md`.

Rules:

- define What / Why only;
- do not prematurely choose products, models, or agents;
- ask one important question at a time;
- distinguish Observation / Interpretation / Research Requirement / Human Decision;
- preserve uncertainty;
- stop when the Charter is sufficiently explicit and approved.

Output boundary:

- approved Research Charter;
- assumptions / open questions;
- recorded human approvals.

Do not output an AI Work Plan or perform research in this session.

### B — AI Work Plan Generation Session

Purpose:

> Load an approved Charter and Advisor Prompt, then generate `01-ai-work-plan.md`.

Rules:

- validate required inputs;
- preserve Charter intent;
- dynamically obtain current ecosystem knowledge relevant to planning;
- prefer primary / official sources for current product facts;
- compare candidates by task fit and constraints;
- configure execution details;
- design handoffs and verification;
- self-review the plan.

Output boundary:

- the Work Plan and its assumptions / uncertainties;
- no actual research or delivery execution unless explicitly requested in a separate execution context.

---

# 5. Advisor Decision Dimensions

The Advisor must reason across these six layers.

## Layer 1 — Task understanding

- Task Type
- Required Capability
- Work Structure

## Layer 2 — Current ecosystem discovery

- Current Knowledge Requirements
- Current AI Ecosystem Research
- Candidate Tool Universe

## Layer 3 — AI selection

- AI Product Selection
- Model Selection
- Reasoning / Thinking Configuration

## Layer 4 — Usage configuration

- Session Strategy
- Context Strategy
- File Strategy
- Connector / MCP Strategy
- Skill / Instruction Strategy

## Layer 5 — Multi-AI collaboration

- AI Handoff / Orchestration

## Layer 6 — Results / verification

- Artifact Strategy
- Verification Strategy

Cross-cutting rules:

- Current over Memorized
- Capability over Brand
- Evidence over Assertion
- Minimal Effective Tool Set
- Existing AI over Rebuilding
- Human Judgment remains central

A single AI may be the correct orchestration result.

---

# 6. Current AI Ecosystem Knowledge Policy

The repository must not encode a permanent mapping such as:

```text
Research → Product A
Coding → Product B
PPT → Product C
```

Such mappings become stale and defeat the purpose of the Advisor.

Instead:

1. the Advisor classifies the freshness sensitivity of the required knowledge;
2. it performs need-driven ecosystem research;
3. official product sources are preferred;
4. independent sources are used for cross-checking;
5. community evidence may be used for experience signals;
6. conflicts are explicitly recorded;
7. planning stops when the information is sufficient for candidate generation, comparison, selection, and configuration.

The Advisor's output should distinguish:

- Confirmed
- Likely
- Unverified
- Conflicting
- Unknown

and should record access / subscription / cost constraints where relevant.

---

# 7. Boundary Model

The final architecture should be understood as four layers.

```text
┌──────────────────────────────────────────────────────────┐
│ AI Native Workbench                                     │
│                                                          │
│ Real Task → Problem Framing → AI Work Planning          │
│             → Selection → Configuration → Orchestration │
│             → Artifacts → Human Judgment → Delivery     │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ↓
              ┌─────────────────────┐
              │ AI Work Advisor     │
              │ decision methodology│
              └──────────┬──────────┘
                         │
                         ↓
              ┌─────────────────────┐
              │ AI Work Plan        │
              │ case-specific       │
              └──────────┬──────────┘
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
      General Work Execution   Research Execution
                                    │
                                    ↓
                         Research System v1
                                    │
                                    ↓
                         Research Runtime v1
```

## 7.1 AI Work Advisor boundary

The Advisor sits **above** Research System and Research Runtime.

It decides how the AI ecosystem should be used for a particular case.

It is not implemented as part of Workflow Core.

## 7.2 Research System boundary

Research System v1 owns reusable research semantics, including:

- research lifecycle;
- evidence-first methodology;
- canonical research knowledge;
- evaluation;
- reproducible research delivery.

It does not define the entire Workbench.

## 7.3 Research Runtime boundary

Research Runtime v1 is execution infrastructure for an approved Research case.

It is responsible for execution state, workflow coordination, artifacts, gates, and runtime control.

It is **not** responsible for:

- discovering the current AI ecosystem;
- selecting the best AI product for a task;
- deciding whether ChatGPT / Claude / Gemini / Coding Agent / Work Agent / Deep Research should be used;
- maintaining a permanent product playbook;
- serving as the top-level AI Work Advisor.

Runtime execution details remain implementation-specific to the Research subsystem.

## 7.4 Workflow Core boundary

Workflow Core defines domain-agnostic workflow semantics.

It must not absorb:

- model selection;
- product selection;
- session policy;
- tool-selection policy;
- AI brand mappings;
- user-level AI orchestration methodology.

This preserves the previously established rule that Workflow Step means **WHAT**, while the execution layer determines **HOW**.

---

# 8. Existing Research Runtime v1 Work

The existing Research Runtime v1 implementation and historical specifications remain valuable engineering assets.

They are **not deleted or rewritten as if they never existed**.

Their new status is:

> **Research capability engineering baseline / retained experimental infrastructure, not the current top-level project roadmap.**

Therefore:

- existing Runtime code remains available for future research execution needs;
- existing Step 6 work remains valid as an engineering milestone;
- planned Runtime expansion beyond the current baseline is deferred;
- R6 / R7 / R8 expansion, Case 001 replay, Case 002 generalization, concurrent scheduling, autonomous research, and production browser / MCP acquisition are not the current project mainline;
- future Runtime work resumes only when a real Research Case or repeated workflow creates a demonstrated need.

Historical `docs/superpowers/specs/` and `docs/superpowers/plans/` documents are treated as historical decision records and implementation records. They do not need cosmetic rewriting.

---

# 9. Repository Artifact Set

The final reusable AI-work-guidance surface consists of exactly four formal artifacts:

### Artifact 1 — AI Work Advisor Prompt

Path:

```text
docs/methodology/ai-work-advisor-v1.md
```

Contains the reusable Advisor Prompt v1 and its decision protocol.

### Artifact 2 — Research Charter Discussion Session

Path:

```text
docs/methodology/templates/research-charter-discussion-session.md
```

Contains the session opening instructions and Charter completion boundary.

### Artifact 3 — AI Work Plan Generation Session

Path:

```text
docs/methodology/templates/ai-work-plan-generation-session.md
```

Contains the session opening instructions and planning-only boundary.

### Artifact 4 — AI Work Plan Template

Path:

```text
docs/methodology/templates/ai-work-plan.md
```

Contains the reusable Markdown structure for case-specific Work Plans.

Case-specific Charter and Work Plan instances remain inside each Case directory:

```text
cases/<case>/
├── 00-research-charter.md
└── 01-ai-work-plan.md
```

No Global Playbook is required.

No permanent product-to-task mapping document is required.

No generic Prompt Library is introduced as a prerequisite.

---

# 10. Documentation Alignment

The final synchronization should cover these active documents:

## 10.1 `README.md`

Align with:

- project mission;
- canonical work chain;
- Charter → Advisor → Work Plan → Execution;
- dynamic ecosystem knowledge policy;
- Research as capability area;
- current Case 002 next step;
- Runtime retained but not top-level.

A wording correction is required so that Current AI Ecosystem Knowledge is not presented as a mandatory standalone input artifact.

The current AI-ecosystem product lists remain illustrative examples only.

## 10.2 `CLAUDE.md`

Replace the stale staged roadmap with operating rules centered on:

```text
Real Task
→ Problem Framing
→ Research Charter
→ AI Work Planning
→ AI Selection / Configuration
→ AI Orchestration
→ Artifacts / Evidence
→ Human Judgment
→ Delivery
→ Evaluation
```

The file should instruct future coding sessions to:

- use the Charter-first workflow for Research Cases;
- use the AI Work Advisor when planning complex AI-assisted work;
- treat current ecosystem knowledge as dynamic;
- prefer minimal effective tool sets;
- keep human judgment central;
- avoid premature Agentization / Automation;
- preserve the Research System / Runtime boundary;
- avoid extending Runtime without demonstrated task need;
- update repository structure documentation when actual structure changes.

The old fixed six-stage Research roadmap must be removed.

## 10.3 `docs/foundation/ai-native-work-capability.md`

Preserve the document's personal motivation and long-term capability rationale, but update its canonical conclusions to the new project direction.

The document should no longer imply that the project is primarily a staged Research-Agent construction effort.

Its central capability model should become:

```text
Real Task
→ Problem Framing
→ AI Work Planning
→ AI Capability / Product / Model Selection
→ AI Configuration
→ AI Orchestration
→ Evidence / Artifacts
→ Human Judgment
→ Delivery
→ Evaluation
→ Optional Engineering / Automation
```

Research, Reasoning, Communication, and Delivery remain human-plus-AI capability areas.

Agentization becomes an optional downstream engineering result, not a required current-stage milestone.

## 10.4 `docs/methodology/research-system-v1.md`

Keep the Research System's valid evidence-first / canonical / evaluation architecture.

Update its top-level positioning to explicitly state:

> Research System v1 is a reusable research capability subsystem inside AI Native Workbench.

Add the Workbench / Advisor / Research System / Runtime boundary.

Clarify:

- Research Charter is task intent;
- AI Work Advisor is outside Research Workflow Core;
- Research System owns research semantics;
- Runtime owns research execution mechanics;
- AI product/model/tool selection is not Research Runtime responsibility.

## 10.5 `docs/architecture/research-runtime-v1.md`

Add a clear boundary statement:

> Research Runtime v1 begins after task-specific planning has produced an approved Research execution context; it does not own current AI ecosystem discovery or user-level AI tool selection.

Keep the existing runtime architecture intact.

Do not duplicate AI Work Advisor logic inside Runtime.

---

# 11. What Is Deliberately Not Changed

The following are not rewritten merely for stylistic consistency:

- historical Research System superpowers specs;
- historical Research Runtime design specs;
- completed engineering task plans;
- Case 001 historical research artifacts;
- working source / evaluation / canonical / build implementations.

The repository should preserve historical evidence of how the project evolved.

The synchronization target is the **active project guidance layer**, not retrospective erasure.

---

# 12. Case 002 Entry Contract

After this alignment is approved and implemented, the project enters:

> **Case 002 — AI Work Agent / AI Office Agent Landscape**

The Case 002 opening sequence is fixed:

```text
Real Objective
    ↓
Research Charter Discussion Session
    ↓
00-research-charter.md
    ↓
AI Work Plan Generation Session
    ↓
01-ai-work-plan.md
    ↓
Human Review
    ↓
Actual AI Execution
```

The new workflow starts immediately with Case 002.

There is no prerequisite requirement to:

- finish every future Runtime task;
- build a Research Agent;
- create a Global Playbook;
- memorize the current AI ecosystem;
- complete a generic AI tooling curriculum.

---

# 13. Success Criteria for the Alignment

The alignment is considered complete only when:

- [ ] README describes the new project identity without stale phase language.
- [ ] CLAUDE provides operational guidance consistent with the new direction.
- [ ] Foundation document no longer makes Research Agent construction the implied main roadmap.
- [ ] Research System is explicitly positioned as a subsystem / capability area.
- [ ] Research Runtime is explicitly bounded as execution infrastructure, not an AI selection layer.
- [ ] The four formal AI-work-guidance artifacts exist at their canonical paths.
- [ ] Charter → Advisor → Work Plan → Execution semantics are consistent across active docs.
- [ ] Current ecosystem knowledge is treated as dynamic Advisor-acquired knowledge, not a hardcoded repository input.
- [ ] No Global Playbook or permanent product mapping is introduced.
- [ ] Research Runtime work is retained but no longer drives the top-level roadmap.
- [ ] Case 002 can start from the new session sequence without additional architectural prerequisites.

---

# 14. Final Architectural Principle

The project should now be understood as:

> **A real-work laboratory for learning how to decide what AI should do, how AI should be configured, and how multiple AI capabilities should be orchestrated to produce verifiable work.**

The most important reusable method is therefore:

```text
What is the real problem?
        ↓
What capabilities are required?
        ↓
What does the current AI ecosystem offer for those capabilities?
        ↓
Which AI should do which part?
        ↓
How should each AI be configured?
        ↓
How should outputs move between AIs?
        ↓
What evidence / artifacts prove the work?
        ↓
Where must a human judge?
        ↓
What should be delivered?
```

The repository's long-term engineering question remains:

> **Which parts of a proven AI-native way of working are worth turning into reusable Workflow, Skill, Agent, or System capabilities?**

But engineering follows demonstrated work.

> **先成为一个优秀的 AI-native Worker，再把优秀的工作方式变成 Agent。**
