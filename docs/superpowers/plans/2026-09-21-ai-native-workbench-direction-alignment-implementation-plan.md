# AI Native Workbench Direction Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize the active repository guidance layer with the approved AI-native Workbench direction and install the four reusable AI-work-guidance document artifacts without changing application code.

**Architecture:** Keep the existing Research System and Research Runtime implementations intact, while moving AI Work Advisor and case-specific Work Planning above the Research subsystem. The execution consists entirely of focused Markdown document creation/update tasks, followed by cross-document consistency verification.

**Tech Stack:** Markdown; existing GitHub repository documentation; no new runtime dependency; no source-code behavior change.

**Spec:** `docs/superpowers/specs/2026-09-21-ai-native-workbench-direction-alignment-design.md`

## Global Constraints

- The project mission is: **通过真实任务，学习、实践和沉淀 AI 原生工作能力。**
- The canonical work chain is: Real Task → Problem Framing → AI Work Planning → AI Capability Selection → AI Product / Model Selection → AI Tool Configuration → AI Orchestration → Artifacts / Evidence → Human Judgment → Final Delivery → Evaluation.
- The authoritative planning relationship is: Research Charter → AI Work Advisor Prompt → AI Work Plan → Actual Execution.
- Current AI Ecosystem Knowledge is dynamically acquired by the Advisor when planning requires it; it is not a mandatory standalone reusable input artifact.
- No Global Playbook is required.
- No permanent product-to-task mapping is introduced.
- AI Work Advisor does not own Research Workflow Core, Research System semantics, or Research Runtime execution mechanics.
- Research Runtime v1 is retained as research execution infrastructure and is not the top-level project roadmap.
- Existing historical Research System / Runtime specs, plans, and Case 001 artifacts are preserved rather than cosmetically rewritten.
- Only documentation is changed; no application source code, tests, runtime dependencies, or architecture implementation are changed in this alignment pass.
- Case 002 may start through Research Charter Discussion → Work Plan Generation → Human Review → Execution without first completing future Runtime expansion.

## Review Focus

- **Stale staged-roadmap language:** Active guidance must no longer imply that building a Research Agent is the required project progression; verify with repository-wide searches for the old staged roadmap terms after updates.
- **Planning-boundary drift:** Research Charter, Advisor Prompt, Work Plan, Research System, and Runtime must each retain distinct authority; verify the canonical relationship and boundary statements appear consistently in all active guidance documents.
- **Dynamic-ecosystem regression:** No active document may turn illustrative AI product examples into fixed recommendations; verify that product lists are explicitly illustrative and that Advisor research is need-driven.
- **Research-Runtime overreach:** Runtime documentation must not assign current AI product discovery, model selection, or user-level orchestration to Runtime; verify the boundary language in methodology and architecture docs.
- **Missing execution artifacts:** The four canonical reusable artifacts and the Case 002 entry contract must exist and be referenced consistently; verify by fetching each file and searching for the canonical paths.

---

### Task 1: Install the Four AI-Work-Guidance Artifacts

**Files:**
- Create: `docs/methodology/ai-work-advisor-v1.md`
- Create: `docs/methodology/templates/research-charter-discussion-session.md`
- Create: `docs/methodology/templates/ai-work-plan-generation-session.md`
- Create: `docs/methodology/templates/ai-work-plan.md`

**Interfaces:**
- Consumes: The locked Step 3 Advisor Prompt design, locked Step 4 Session Opening Template designs, and approved AI Work Plan schema from the direction-alignment spec.
- Produces: Four canonical reusable document artifacts referenced by active project guidance and consumed by Case-specific planning sessions.

- [ ] **Step 1: Create the AI Work Advisor Prompt document**

Write `docs/methodology/ai-work-advisor-v1.md` with:
1. title, status, purpose, and scope;
2. the reusable **AI Work Orchestration Advisor** prompt itself;
3. the full decision protocol from task understanding through self-review;
4. the six decision layers and all approved decision dimensions;
5. dynamic current-ecosystem research rules;
6. official / independent / community source priority;
7. product/model/session/context/files/connector/skill selection rules;
8. one-AI-is-enough and minimal-effective-tool-set rules;
9. artifact / handoff / verification rules;
10. uncertainty levels and human responsibility;
11. failure / edge-case handling;
12. exact AI Work Plan output contract.

Keep product examples, if any, explicitly illustrative rather than permanent mappings.

- [ ] **Step 2: Create the Research Charter Discussion Session template**

Write `docs/methodology/templates/research-charter-discussion-session.md` with:
1. session purpose;
2. What / Why boundary;
3. one-important-question-at-a-time discussion rule;
4. separation of Observation / Interpretation / Research Requirement / Human Decision;
5. discussion checklist covering objective, questions, scope, population, definitions, inclusion/exclusion, dimensions, comparison/ranking, evidence, cutoff, deliverables, success criteria, assumptions, and approvals;
6. final `00-research-charter.md` structure;
7. explicit end condition;
8. explicit prohibition on premature tool/model/agent selection and research execution.

- [ ] **Step 3: Create the AI Work Plan Generation Session template**

Write `docs/methodology/templates/ai-work-plan-generation-session.md` with:
1. session purpose;
2. required inputs: approved Research Charter and Advisor Prompt;
3. optional context / constraints;
4. input validation and Charter-preservation rules;
5. need-driven current AI ecosystem research;
6. decomposition and AI selection workflow;
7. configuration and orchestration rules;
8. artifact / handoff / verification rules;
9. human review boundary;
10. explicit planning-only output boundary;
11. final output path `01-ai-work-plan.md`.

- [ ] **Step 4: Create the reusable AI Work Plan template**

Write `docs/methodology/templates/ai-work-plan.md` with the locked schema:
`0. Plan Metadata`, `1. Executive Work Strategy`, `2. AI Ecosystem Selection Summary`, `3. Global Execution Rules`, `4. Detailed Work Plan`, `5. Artifact & Handoff Map`, `6. Verification & Human Review`, and `7. Plan Assumptions / Uncertainties`.

Under each meaningful Task include the exact fixed fields:
`Purpose`, `Required Capability`, `Recommended Product`, `Model`, `Mode`, `Thinking`, `Session`, `Context`, `Files`, `Connectors`, `Skills`, `Input`, `Instruction`, `Expected Output`, `Artifact`, `Execution Boundary`, `Handoff`, `Verification`, `Rationale`, `Alternatives Considered`.

The template must be structural rather than a filled product recommendation.

- [ ] **Step 5: Verify the four artifacts**

Fetch all four new files and verify:
- every file exists at the canonical path;
- no file contains `TBD` or `TODO`;
- the Advisor document contains the approved decision workflow and dynamic ecosystem policy;
- both session templates have their explicit execution boundaries;
- the Work Plan template contains every required section and Task field.

Commit:

```text
docs: 建立 AI-native 工作规划核心文档
```

---

### Task 2: Realign Active Project Guidance

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`
- Modify: `docs/foundation/ai-native-work-capability.md`

**Interfaces:**
- Consumes: Task 1 artifact paths and the approved direction-alignment spec.
- Produces: A consistent active project guidance layer that describes AI Workbench as the top-level system and Research as a capability subsystem.

- [ ] **Step 1: Update README canonical language**

Preserve the already-updated mission and work chain, then correct any remaining ambiguity so that:
- Current AI Ecosystem Knowledge is described as information dynamically acquired by the Advisor, not a required third artifact input;
- the four canonical reusable artifacts are discoverable;
- Case-specific instances are `00-research-charter.md` and `01-ai-work-plan.md`;
- Research System / Runtime are explicitly subsystem / infrastructure layers;
- Case 002 is the current next execution point;
- the Runtime expansion is retained but deferred.

- [ ] **Step 2: Replace stale CLAUDE staged roadmap**

Rewrite the active operating guidance so it starts from:
`Real Task → Problem Framing → Research Charter → AI Work Planning → AI Selection / Configuration → AI Orchestration → Artifacts / Evidence → Human Judgment → Delivery → Evaluation`.

Preserve repository maintenance rules that are still valid.

Remove the old required six-stage Research roadmap and its claim that Agentization is a later mandatory phase.

Add explicit instructions for:
- Charter-first Research Cases;
- AI Work Advisor use for complex AI-assisted work;
- dynamic ecosystem knowledge;
- minimal effective tool set;
- no premature Agentization / Automation;
- Research System / Runtime boundary;
- no Runtime expansion without demonstrated need.

- [ ] **Step 3: Align the foundation document**

Preserve the document's original personal motivation and capability rationale, but replace the obsolete project-level roadmap conclusions with the approved AI-native Workbench model.

Make Agentization optional and downstream of demonstrated workflow value.

Keep Research, Reasoning, Communication, Delivery, and Engineering as capability areas rather than redefining the whole repository as a Research Agent project.

- [ ] **Step 4: Verify active guidance consistency**

Fetch all three documents and confirm:
- mission is consistent;
- canonical work chain is consistent;
- Charter → Advisor → Work Plan → Execution is consistent;
- no stale mandatory Research-Agent stage language remains in active guidance;
- no document defines a permanent product mapping.

Commit:

```text
docs: 对齐 AI-native workbench 项目指导
```

---

### Task 3: Align Research System and Research Runtime Boundaries

**Files:**
- Modify: `docs/methodology/research-system-v1.md`
- Modify: `docs/architecture/research-runtime-v1.md`

**Interfaces:**
- Consumes: Task 1 canonical artifact definitions and Task 2 active guidance.
- Produces: Explicit boundaries between Workbench-level planning, Research methodology, and Research execution infrastructure.

- [ ] **Step 1: Update Research System positioning**

Add a concise top-level statement that Research System v1 is a reusable research capability subsystem inside AI Native Workbench.

Add boundary language stating:
- Research Charter defines task intent;
- AI Work Advisor is outside Research Workflow Core;
- Research System owns research semantics, evidence, canonical knowledge, evaluation, and reproducible delivery;
- AI product/model/tool selection is not Research Runtime responsibility.

Do not rewrite the historical Research lifecycle, evidence model, canonical model, evaluation model, or Case 001 semantics except where this boundary requires a small wording correction.

- [ ] **Step 2: Update Research Runtime positioning**

Add a clear architecture boundary near the Runtime entry point:
- Runtime starts after an approved research execution context / plan exists;
- Runtime owns research execution state, workflow coordination, artifacts, gates, and control;
- Runtime does not discover the current AI ecosystem or choose user-level AI products/models/tools;
- Runtime does not become the AI Work Advisor.

Keep all existing Runtime interfaces and implementation descriptions unchanged.

- [ ] **Step 3: Verify boundary language**

Fetch both documents and confirm there is no statement assigning AI ecosystem selection to Runtime and no duplication of Advisor methodology inside Workflow Core.

Commit:

```text
docs: 明确 Research System 与 Runtime 边界
```

---

### Task 4: Final Repository Consistency Check and Case 002 Readiness

**Files:**
- Verify: all documents changed or created in Tasks 1–3
- Verify: `cases/001-ai-coding-agent-landscape/00-research-charter.md`
- Verify: `cases/002-ai-work-agent-landscape/` references where available

**Interfaces:**
- Consumes: the complete synchronized guidance layer.
- Produces: verified readiness for Case 002; no code implementation.

- [ ] **Step 1: Repository-wide stale-language search**

Search the repository for the obsolete active-roadmap phrases and inspect matches. The search must specifically check for:
`核心工作链：`, `第一阶段：先不做复杂 Agent`, `第二阶段：研究 OpenAI / Anthropic`, `第三阶段：Human + AI`, `第四阶段：Research Agent`, `第五阶段：把 Research 能力扩展`, `第六阶段：形成 Evaluation`.

Expected result: these phrases may remain only in historical records when they document past decisions; they must not remain as the current active project roadmap.

- [ ] **Step 2: Verify canonical artifact references**

Search active documents for:
- `docs/methodology/ai-work-advisor-v1.md`
- `docs/methodology/templates/research-charter-discussion-session.md`
- `docs/methodology/templates/ai-work-plan-generation-session.md`
- `docs/methodology/templates/ai-work-plan.md`
- `cases/<case>/01-ai-work-plan.md`

Expected result: active guidance points to the canonical artifacts and does not introduce a Global Playbook.

- [ ] **Step 3: Verify Case 002 entry contract**

Confirm the repository contains the Case 002 directory or clearly record its absence without inventing files. Confirm the active guidance still specifies:
`Research Charter Discussion → 00-research-charter.md → AI Work Plan Generation → 01-ai-work-plan.md → Human Review → Actual AI Execution`.

- [ ] **Step 4: Verify no source-code changes**

Inspect repository changes for this alignment pass and confirm only Markdown documentation files were touched.

- [ ] **Step 5: Commit final consistency corrections, if any**

If verification exposes a documentation-only inconsistency, correct it before the final report and use:

```text
docs: 完成 AI-native workbench 方向同步校验
```

If no correction is required, do not create an empty commit.

---

## Verification Commands / Checks

The alignment is documentation-only, so verification is primarily repository-content verification rather than unit testing.

Use the repository search / fetch facilities to confirm the exact document contents. When a local clone is available, additionally run:

```bash
git status --short
git diff --check
git diff --name-only
```

Expected:
- `git diff --check` exits successfully with no whitespace errors;
- `git diff --name-only` contains only the files listed in Tasks 1–4;
- no application source code or test file is changed by this alignment.

No new test suite is required because this plan changes documentation only.
