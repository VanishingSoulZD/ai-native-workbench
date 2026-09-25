# AI Work Plan

> Case-specific execution plan generated from Research Charter v1.0 and AI Work Advisor Prompt v1.
> Planning boundary: this document defines how the research should be executed. It does not execute research or produce the final Research Note / PPT / HTML.

## 0. Plan Metadata

- Case: 002 — AI for Knowledge Work / Work AI Landscape
- Work Plan Version: v1.0
- Generated At: 2026-09-24
- Planning Cutoff: 2026-09-24
- Research Snapshot Cutoff: 2026-09-24
- Source Charter: `cases/002-ai-work-agent-landscape/00-research-charter.md` — Charter v1.0 — SHA `5830a11529c5050e539fb7232cb0fbf9b15710a5`
- AI Work Advisor Prompt: `docs/methodology/ai-work-advisor-v1.md` — SHA `a76d98fbc0ad01607f3cdc71553f2ef2116e941e`
- Session Template: `docs/methodology/templates/ai-work-plan-generation-session.md` — SHA `6f1977f5abac0a1520d03c64324e97ebb5f220e2`
- Repository Context: `VanishingSoulZD/ai-native-workbench`, default branch `main`
- Planner Notes:
  - The Charter is explicitly marked **Approved for execution**.
  - The Charter defines What / Why; this Work Plan defines the subsequent How.
  - The plan deliberately does not preselect the Global Top 10 or China Top 5. Those are outputs of the research, not planning assumptions.
  - Current product facts used for tool selection were checked against official sources on 2026-09-24.
  - The tool set is intentionally small: ChatGPT Deep Research + ChatGPT synthesis/QA + Kimi Deep Research for the China-specific independent research track, with the existing GitHub connector as the repository system of record.
- Overall Uncertainty: **Likely**
  - Research architecture and selected capability classes are sufficiently clear.
  - Exact product availability, plan quotas, model exposure, and connector availability can vary by account, region, workspace, and date and must be checked again at execution time.
  - The research itself must determine the representative product populations; this plan does not claim those products in advance.

## 1. Executive Work Strategy

### Objective

Execute Case 002 exactly against the approved Charter:

> When facing a concrete Knowledge Work task, determine what class of AI to use, which product is appropriate, and how the work should be allocated between AI and humans.

The research must therefore move beyond feature inventory toward an operational model:

\`\`\`
Knowledge Work Task
→ Required Capability
→ Work AI Category / Role
→ Candidate Product
→ Actual Work Position
→ Usage Pattern
→ Human / AI Allocation
→ Potential Multi-AI Handoff
\`\`\`

The Global Representative Top 10 and China Representative Top 5 are representative research sets, not universal quality rankings.

### Overall Strategy

Use a **two-research-engine, one-synthesis-system architecture**:

1. **ChatGPT Deep Research** is the primary global research engine.
   - It is appropriate for multi-step, multi-source research.
   - It can create an editable research plan, track progress, use public web sources, use uploaded files, and use enabled connected apps.
   - Official OpenAI documentation states that Deep Research can use connected apps and that GitHub is among supported connectors; exact availability remains account-dependent.
   - Use it to build the broad candidate universe, global representative set, product work-positioning cards, task-fit evidence, and orchestration analysis.

2. **Kimi Deep Research** is the independent China-market research engine.
   - It is selected for a concrete gap: China-specific source discovery, product availability/context, and regional market/product interpretation.
   - Kimi's official documentation describes Deep Research as a dedicated research agent powered by Kimi-Researcher, with multi-step search/reasoning and Markdown/HTML research outputs.
   - Use it primarily for China Top 5 candidate discovery, China-specific evidence, borderline cases, and regional context.
   - It is not used as a permanent product mapping and is not used to determine the Global Top 10 by itself.

3. **ChatGPT synthesis / QA** is the final integration layer.
   - Use a fresh ChatGPT session with the durable research artifacts as authoritative context.
   - Prefer GPT-5.6 Sol with high reasoning effort when available; use the highest effort only for final synthesis / consistency audit.
   - If Sol or the required reasoning level is unavailable, use the currently available GPT-5.6 Luna + Think configuration.
   - Do not rely on conversational memory from research sessions as authoritative state.

4. **GitHub connector** is the durable repository interface.
   - The repository, not a chat transcript, is the system of record.
   - Durable research packets, evidence ledgers, product cards, and final deliverable source material should be stored in the case directory.
   - The Work Plan itself is the first durable artifact; no research should begin until the human reviews and approves this plan.

### Core Orchestration Decision

A one-AI workflow was explicitly considered.

**Why one AI is not used alone:** Case 002 includes a dedicated China market view and has a high risk of source / coverage blind spots caused by language, region, market-access differences, and vendor framing. A second research engine fills this specific independent evidence gap.

**Why a third external research engine is not added:** ChatGPT Deep Research already provides broad current web research and source control, while Kimi Deep Research provides an independent China lens. Adding Gemini, Perplexity, Claude, or another general research system would mostly duplicate web research / synthesis capability and increase coordination, cost, and evidence reconciliation.

The resulting minimum effective architecture is:

\`\`\`
Human
  ↓ approves Charter + Work Plan
ChatGPT Deep Research
  ↓ global research packets
Kimi Deep Research
  ↓ China research packet
ChatGPT synthesis / QA
  ↓ canonical evidence model
Human
  ↓ final judgment / delivery approval
Research Note / PPT / HTML
\`\`\`

## 2. AI Ecosystem Selection Summary

| Capability | Candidates Considered | Recommended Product | Model | Key Configuration | Evidence / Freshness | Why Selected | Rejected Alternatives / Trade-off |
|---|---|---|---|---|---|---|---|
| Multi-source global research | ChatGPT Deep Research, Gemini Deep Research, Perplexity Research, Claude research/web workflows | ChatGPT Deep Research | Product-managed current Deep Research runtime; use current GPT-5.6-family runtime when exposed | Deep Research; edit research plan before run; source allowlist for authoritative sites; GitHub app only for repo context where permitted | Official OpenAI Deep Research Help / release notes checked 2026-09-24 | Best fit for current multi-step research plus existing GitHub connector and durable repository workflow | Gemini has strong Google-source integration but adds a second global research stack; Perplexity overlaps heavily; Claude is useful but would add another research/synthesis system without filling a unique gap |
| China-market independent research | Kimi Deep Research, Gemini Deep Research, ChatGPT Deep Research | Kimi Deep Research | Kimi-Researcher | Deep Research; Chinese-source discovery; output Markdown + HTML; export as durable packet | Official Kimi Deep Research docs checked 2026-09-24 | Fills the concrete regional independence gap; strong Chinese-language research workflow; dedicated Deep Research product | Using ChatGPT alone creates more correlated coverage risk; using Gemini here adds an access/integration dependency without a uniquely necessary capability |
| Final synthesis / evidence integration | ChatGPT, Claude, Gemini, Perplexity | ChatGPT | GPT-5.6 Sol high reasoning when available; fallback GPT-5.6 Luna + Think | Fresh session; authoritative files only; high reasoning for synthesis; highest effort reserved for QA | OpenAI GPT-5.6 and ChatGPT docs checked 2026-09-24 | Existing repository connector, strong structured synthesis, and no additional transfer layer | Claude / Gemini could provide an independent review, but this is not necessary unless the first QA pass identifies a material uncertainty that cannot be resolved from evidence |
| Repository I/O | ChatGPT GitHub connector; manual file transfer; other external connectors | ChatGPT GitHub connector | N/A | Read approved case files; write durable artifacts; no hidden conversational state as authoritative state | Existing connected tool availability + OpenAI connector documentation checked 2026-09-24 | Already available in this environment and directly supports durable handoffs | Manual file transfer retained only for importing Kimi outputs when no direct connector exists |
| Lightweight matrix / formatting work | ChatGPT standard chat / data tools, local scripts | ChatGPT standard chat / data tools | GPT-5.6 Luna or equivalent available model | Low-to-medium reasoning; deterministic formats; do not use premium deep research for simple transformations | Stable capability; exact plan limits checked at execution time | Avoids spending deep-research quota on mechanical work | Coding a bespoke pipeline is unnecessary unless execution reveals repeated formatting / validation pain |

### Current Ecosystem Notes

1. **ChatGPT Deep Research**
   - OpenAI's current Deep Research documentation describes a workflow in which the system plans, researches, synthesizes, and returns a cited report.
   - The user can review or modify the proposed research plan before research begins.
   - Deep Research can use public web sources, uploaded files, and eligible connected apps; current OpenAI release notes also document use of connectors and MCP with Deep Research.
   - Research can be constrained to trusted websites when a source allowlist is useful.
   - The exact quota and feature availability vary by plan and account and must be checked in-product at execution time.

2. **GPT-5.6 family**
   - OpenAI's 2026-07-09 release describes GPT-5.6 as a current model family spanning Sol, Terra, and Luna; model availability varies by product and plan.
   - For this case, model selection is about matching work quality and cost rather than assuming the largest model is always required.
   - Final synthesis / contradiction resolution should use the highest accessible reasoning level; routine transformations should use a lower-cost current model.

3. **Kimi Deep Research**
   - Kimi documents Deep Research as a dedicated research agent powered by Kimi-Researcher.
   - Its documented workflow includes research-plan construction, large-scale web search, iterative retrieval, and structured report production.
   - Kimi documents Markdown and HTML report output, which is useful for durable handoff.
   - Kimi's quota is shared across certain agent/product functions and is usage-dependent; exact remaining quota must be checked at execution time.

4. **Gemini Deep Research**
   - Google documents Deep Research as a multi-step research workflow using Google Search by default, with optional connected Google sources and file / NotebookLM inputs.
   - It is a meaningful alternative, especially where Google Workspace context is central.
   - It is not selected because this case does not require a third global research stack and does not rely on Google Workspace as an authoritative source boundary.

5. **Perplexity Research**
   - Perplexity documents Research mode as a multi-step research capability and Pro Search as a source-rich research/search mode with model selection.
   - It is a meaningful alternative for research breadth, but it overlaps too strongly with ChatGPT Deep Research for the specific execution gap in this case.

### Access / Cost Constraints

- No subscription upgrade is assumed as a prerequisite.
- At execution start, verify:
  - ChatGPT Deep Research availability and remaining quota.
  - ChatGPT model / reasoning availability.
  - GitHub connector availability in the active ChatGPT account/workspace.
  - Kimi Deep Research remaining quota and export capability.
- Do not consume premium deep-research quota for mechanical transformations.
- Use one Deep Research run per major research package where possible, rather than spawning many overlapping runs.
- If a quota or access limit blocks a selected product:
  1. use the documented fallback in Section 3;
  2. preserve the access limitation as an uncertainty;
  3. do not silently substitute a different product while retaining the original plan's claim.
- No paid product should be added solely for convenience when the same capability can be obtained from the selected tools and targeted web verification.

### Product-Selection Source References

- OpenAI — Deep Research Help: https://help.openai.com/en/articles/10500283-deep-research-faq
- OpenAI — Introducing Deep Research: https://openai.com/index/introducing-deep-research/
- OpenAI — ChatGPT Release Notes / Deep Research connector updates: https://help.openai.com/en/articles/6825453-chatgpt-release-notes
- OpenAI — GPT-5.6: https://openai.com/index/gpt-5-6/
- Google — Gemini Deep Research: https://support.google.com/gemini/answer/15719111
- Perplexity — Pro Search: https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search
- Perplexity — Pro / Research: https://www.perplexity.ai/help-center/en/articles/10352901-what-is-perplexity-pro
- Kimi — Deep Research overview: https://www.kimi.com/help/deep-research/deep-research-overview
- Kimi — Agent quota / billing: https://www.kimi.com/help/agent/agent-quota-and-billing

## 3. Global Execution Rules

- Context policy:
  - The approved Charter is immutable during execution unless a Charter revision is formally approved.
  - Every research task receives only the context needed for that task.
  - Durable files, not chat history, are the authoritative state.
  - Do not pass the complete repository to every research task; pass the relevant charter excerpts plus the task brief and authoritative artifacts.
  - Preserve the research cutoff of 2026-09-24. Later product changes may be documented only as explicit post-cutoff notes when necessary.
- File policy:
  - Repository files are authoritative.
  - Intermediate AI reports are evidence-bearing working artifacts, not final truth.
  - Store evidence and decisions in durable Markdown / CSV artifacts.
  - Do not overwrite authoritative artifacts with a new synthesis without explicit versioning.
  - Recommended case asset layout:
    - `cases/002-ai-work-agent-landscape/00-research-charter.md`
    - `cases/002-ai-work-agent-landscape/01-ai-work-plan.md`
    - `cases/002-ai-work-agent-landscape/research-packets/global-candidate-universe.md`
    - `cases/002-ai-work-agent-landscape/research-packets/global-landscape.md`
    - `cases/002-ai-work-agent-landscape/research-packets/china-landscape.md`
    - `cases/002-ai-work-agent-landscape/research-packets/product-cards.md`
    - `cases/002-ai-work-agent-landscape/research-packets/orchestration-patterns.md`
    - `cases/002-ai-work-agent-landscape/evidence/claim-evidence-ledger.csv`
    - `cases/002-ai-work-agent-landscape/evidence/source-register.csv`
    - `cases/002-ai-work-agent-landscape/analysis/canonical-research-model.md`
    - final delivery artifacts in the case directory as defined later.
- Session policy:
  - Use dedicated sessions for Global Research, China Research, Synthesis, and Verification.
  - Do not continue a giant research conversation indefinitely.
  - Start a fresh synthesis session after the major evidence packets are frozen.
  - Start a fresh verification session when checking the canonical model against evidence.
- Connector / MCP policy:
  - Use the GitHub connector for repository reads/writes and durable artifact persistence.
  - Use Deep Research connected apps only when the connector materially helps access authoritative work context.
  - Do not use the repository connector as a substitute for current external-source research.
  - Never use a hidden connector state as evidence unless it can be represented in a durable artifact with a source/date trail.
- Skill / Instruction policy:
  - Reuse the approved AI Work Advisor methodology for planning.
  - Do not create a giant permanent prompt.
  - Each execution task should use a short task-specific brief derived from the Work Plan plus the global evidence rules.
  - Skills may be added only when execution reveals a stable repeated capability gap; no new Skill is required by this Work Plan.
- Evidence policy:
  - Apply the Charter's tiered source hierarchy.
  - Match source type to claim type.
  - Date all time-sensitive claims.
  - Separate Fact, Evidence, Analysis, Judgment, and Unknown.
  - Do not treat a vendor capability statement as independent proof of actual effectiveness.
  - Do not use model benchmarks as direct evidence of end-to-end product work capability.
- Verification policy:
  - Mechanical checks for schema / completeness / counts.
  - Source verification for factual product claims.
  - Independent AI review for synthesis coherence.
  - Human review for representative-set selection, borderline cases, consequential interpretations, and final delivery.
- Human approval checkpoints:
  - Approve this Work Plan before execution.
  - Approve the evidence-backed candidate / representative-set decision before final synthesis.
  - Review unresolved conflicts and material uncertainties.
  - Approve the final practical implications and all final deliverables.
- Cost / time constraints:
  - Use deep research for tasks that actually require multi-source investigation.
  - Use standard chat for extraction, transformation, formatting, and mechanical QA.
  - Avoid redundant research of the same claim across multiple AI systems.
  - The second AI is used only for the China-specific independent lens.
- Fallback rule:
  - Global Deep Research unavailable → use ChatGPT standard web search in a dedicated research session, with explicit query batches and manual source ledger maintenance.
  - ChatGPT high reasoning unavailable → use the highest current reasoning setting available; document the access mismatch.
  - Kimi unavailable → use ChatGPT Deep Research with a dedicated China-source allowlist and explicitly mark the loss of independent regional verification.
  - GitHub connector write unavailable → retain artifacts locally until repository write access is restored; do not pretend the repo is synchronized.
  - If any major handoff becomes infeasible, trigger replanning before continuing.

## 4. Detailed Work Plan

### Stage 1 — Execution Frame and Research Workspace

#### Step 1.1 — Freeze execution context

##### Task 1.1.1 — Establish authoritative research workspace and execution briefs

- Purpose:
  - Turn the approved Charter into an executable research workspace without changing its intent.
  - Establish the durable artifact structure and task-specific briefs before actual research begins.
- Required Capability:
  - Task decomposition, information architecture, repository management, research-method translation.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Luna / current efficient model; GPT-5.6 Sol is unnecessary unless material ambiguity appears.
- Mode:
  - Standard chat / analysis.
- Thinking:
  - Medium / Think.
- Session:
  - Dedicated execution-preparation session; terminate after artifacts are created.
- Context:
  - Full approved Charter, Advisor Prompt, Work Plan, case directory structure.
- Files:
  - Input: `00-research-charter.md`, `ai-work-advisor-v1.md`, `01-ai-work-plan.md`.
  - Output: task briefs and directory placeholders only where useful.
- Connectors:
  - GitHub connector for repository inspection and writes.
- Skills:
  - AI Work Advisor methodology; no additional Skill.
- Input:
  - Approved Charter v1.0 and this Work Plan.
- Instruction:
  - Preserve every Charter requirement.
  - Create short case-specific briefs for the planned research packages.
  - Define required artifact schemas before research.
  - Do not populate research findings.
- Expected Output:
  - Stable research-workspace structure and brief templates for Global, China, Product Cards, Orchestration, Evidence QA, and Delivery.
- Artifact:
  - `research-packets/task-briefs.md` or equivalent durable brief set.
- Execution Boundary:
  - Planning / workspace setup only. No external research and no product selection.
- Handoff:
  - Producer = Task 1.1.1; Artifact = task briefs; Consumer = Tasks 2.1.1–6.3.1; Purpose = enforce consistent execution contracts; Verification = human or mechanical schema review before research.
- Verification:
  - Mechanical + Human.
- Rationale:
  - Durable schemas prevent drift and reduce the need to repeat large prompts.
- Alternatives Considered:
  - Sending the Charter directly into every AI session was rejected because it increases context cost and encourages inconsistent interpretation.
  - Building a custom Research Runtime now was rejected because the Charter is a research case, not a runtime-engineering project.

### Stage 2 — Global Work AI Landscape

#### Step 2.1 — Candidate universe

##### Task 2.1.1 — Build the broad Global candidate universe and boundary map

- Purpose:
  - Establish a broad candidate universe before selecting the representative Global Top 10.
  - Make Work AI boundaries explicit, including adjacent categories.
- Required Capability:
  - Current market research, taxonomy discovery, product-family identification, inclusion/exclusion analysis, current-state verification.
- Recommended Product:
  - ChatGPT Deep Research
- Model:
  - Product-managed current Deep Research model; use the strongest current research runtime available within quota.
- Mode:
  - Deep Research.
- Thinking:
  - Deep Research default / product-managed; edit the research plan before launch.
- Session:
  - Dedicated Global Candidate Universe research session.
- Context:
  - Charter Sections 1–8, especially scope, research population, definitions, inclusion/exclusion, and representative-set rules.
- Files:
  - Input: Charter + Task 2.1 brief.
  - Output: research packet in Markdown; source links embedded in the report and later normalized into the source register.
- Connectors:
  - GitHub connector for reading the Charter / task brief.
  - Optional connected apps only if they materially provide authoritative work context; not required for market research.
- Skills:
  - AI Work Advisor instruction set; evidence-first research instructions.
- Input:
  - Task brief asking for a deliberately broad 2026 candidate universe across global general-purpose AI, office AI, work agents, enterprise work AI, knowledge-work-native products, and important adjacent products.
- Instruction:
  - Start from category buckets rather than a preselected Top 10.
  - Use official sources first.
  - Record candidate, product family, work surface, work role, evidence of relevance, access/geography, and possible boundary status.
  - Explicitly record candidates that appear borderline.
  - Do not rank candidates as “best”.
  - Date material product facts to the 2026-09-24 snapshot.
- Expected Output:
  - Candidate universe containing materially relevant products and product families, category/boundary notes, initial evidence references, and a shortlist of candidates requiring deeper product-level research.
- Artifact:
  - `research-packets/global-candidate-universe.md`.
- Execution Boundary:
  - Discovery and candidate-universe construction only. No final Global Top 10 and no delivery claims.
- Handoff:
  - Producer = Task 2.1.1; Artifact = global candidate universe; Consumer = Task 2.2.1 and Task 5.1.1; Purpose = establish the selection universe and prevent premature product anchoring; Verification = evidence/source-register checks.
- Verification:
  - Source + Mechanical.
- Rationale:
  - The Charter explicitly requires a broad candidate universe before representative-set selection.
- Alternatives Considered:
  - Starting from a memorized list of famous AI products was rejected because it may miss important Work AI product families and creates selection bias.
  - Using multiple global research engines here was rejected because one strong Deep Research run plus later evidence verification is sufficient.

#### Step 2.2 — Representative landscape selection

##### Task 2.2.1 — Select the Global Representative Top 10 and record inclusion/exclusion logic

- Execution Status: **Completed — 2026-09-25**
- Completed Artifact: `research-packets/global-landscape.md`
- Selection Note:
  - The task was executed as a representative-set selection, not a universal quality ranking.
  - No fixed numeric scoring formula was used.
  - Product-family normalization was preserved, so Deep Research / Researcher / Computer Use / Cowork-style modes were not double-counted as independent product families.
  - The completed packet records the selected Global Representative Top 10, meaningful exclusions, borderline cases, evidence anchors, confidence, and downstream verification items.
  - Final selection packet status: **REVIEW** pending Task 5.1.1 evidence audit and human review.

- Purpose:
  - Convert the broad candidate universe into an evidence-traceable representative Global Top 10.
- Required Capability:
  - Comparative market analysis, evidence weighting without fixed numeric scoring, category coverage reasoning, inclusion/exclusion decisions.
- Recommended Product:
  - ChatGPT Deep Research
- Model:
  - Current strongest available Deep Research runtime; prefer quality over speed for this task.
- Mode:
  - Deep Research.
- Thinking:
  - Deep Research default; allow plan iteration before execution.
- Session:
  - Dedicated Global Selection session, separate from the candidate-universe run.
- Context:
  - `global-candidate-universe.md`, Charter Sections 6–10, current evidence/source register.
- Files:
  - Input: candidate universe + source register.
  - Output: selection packet and provisional Global Top 10 rationale table.
- Connectors:
  - GitHub connector for authoritative candidate-universe artifact and source-register access.
- Skills:
  - Evidence-first selection instructions; no fixed numeric scoring rubric.
- Input:
  - Broad candidate universe, product significance evidence, Knowledge Work relevance, workflow significance, category coverage evidence.
- Instruction:
  - Select a representative set, not a universal ranking.
  - Explain inclusion and meaningful exclusion.
  - Ensure category coverage is intentional.
  - Preserve borderline candidates and unresolved cases.
  - Never output “#1 is best” or an equivalent normative ranking.
- Expected Output:
  - Global Representative Top 10, selection rationale, meaningful exclusions, borderline cases, confidence status, and evidence gaps.
- Artifact:
  - `research-packets/global-landscape.md`.
- Execution Boundary:
  - Selection analysis only; no final report prose and no PPT/HTML production.
- Handoff:
  - Producer = Task 2.2.1; Artifact = Global landscape selection packet; Consumer = Tasks 2.3.1, 4.1.1, 5.1.1; Purpose = establish the representative product set for downstream analysis; Verification = human selection review plus evidence audit.
- Verification:
  - Source + Human.
- Rationale:
  - The Charter explicitly prohibits a universal “best AI” ranking and requires an evidence-traceable representative set.
- Alternatives Considered:
  - Numeric scoring was rejected because the Charter approves no fixed weighting and because a single score would obscure different work roles.
  - Human selection without an AI-generated evidence packet was rejected because traceability and breadth would be weaker.

#### Step 2.3 — Product-level work models

##### Task 2.3.1 — Produce representative product work-positioning and capability cards

- Purpose:
  - For every Global Top 10 product, characterize actual Work AI positioning and workflow contribution.
- Required Capability:
  - Product research, capability decomposition, task-fit analysis, work-surface mapping, context / execution / artifact analysis, uncertainty handling.
- Recommended Product:
  - ChatGPT Deep Research
- Model:
  - Current strongest Deep Research runtime available.
- Mode:
  - Deep Research.
- Thinking:
  - Product-managed deep research; use explicit source restrictions for official documentation where needed.
- Session:
  - One dedicated Product Cards research session, or two logically separated runs if context / quota limits make batching unsafe.
- Context:
  - Global Top 10 selection packet + Charter Research Dimensions + source register.
- Files:
  - Input: `global-landscape.md`, product URLs / evidence notes, Charter Section 7.
  - Output: structured product cards.
- Connectors:
  - GitHub connector for durable product-set and schema access.
- Skills:
  - Evidence-first product analysis instructions.
- Input:
  - Approved representative product list and required dimensions:
    - work positioning;
    - task fit;
    - interaction model;
    - persistent context;
    - agentic execution;
    - artifact model;
    - integrations/context;
    - usage model;
    - orchestration role;
    - constraints/economics;
    - evidence/uncertainty.
- Instruction:
  - Separate product facts from model facts.
  - Describe what the product actually enables, not merely what the vendor calls it.
  - Distinguish stated capabilities from independently observed / documented workflows.
  - Record access and plan constraints where material.
  - Date change-sensitive facts.
- Expected Output:
  - One structured card per representative product, each with factual evidence, analysis, uncertainty, and a concise “what this AI is for” statement.
- Artifact:
  - `research-packets/product-cards.md`.
- Execution Boundary:
  - Product characterization only. Do not yet synthesize the final Work AI taxonomy or make overall recommendations.
- Handoff:
  - Producer = Task 2.3.1; Artifact = product cards; Consumer = Tasks 4.1.1, 4.2.1, 5.1.1; Purpose = common analytical substrate across products; Verification = source audit and cross-product consistency check.
- Verification:
  - Source + Mechanical.
- Rationale:
  - The Charter makes work positioning, task fit, usage patterns, and orchestration roles core research goals.
- Alternatives Considered:
  - Relying on product homepages only was rejected because homepage claims are insufficient for execution, context, integration, and human-control analysis.
  - Researching every candidate at full depth was rejected because deep product analysis belongs only to the representative set.

### Stage 3 — China Work AI Landscape

#### Step 3.1 — Regional candidate universe and representative set

##### Task 3.1.1 — Build and select the China Representative Top 5

- Purpose:
  - Produce an independent China-market view using Chinese-language and region-specific research, while allowing overlap with the Global Top 10.
- Required Capability:
  - China market research, Chinese product research, regional availability/context verification, product-family identification, representative-set reasoning.
- Recommended Product:
  - Kimi Deep Research
- Model:
  - Kimi-Researcher.
- Mode:
  - Deep Research.
- Thinking:
  - Product-managed autonomous research; review/approve the proposed research direction before the run where the interface allows it.
- Session:
  - Dedicated China Landscape research session.
- Context:
  - Charter Sections 3–10 + a short China-specific task brief. Do not pass the Global Top 10 as an answer key.
- Files:
  - Input: Charter + China task brief + optional exported global candidate categories for coverage comparison only.
  - Output: Markdown/HTML China research report.
- Connectors:
  - No external repository connector is required; export the resulting report and import it as a durable repository artifact.
- Skills:
  - Evidence-first Chinese research instructions.
- Input:
  - China candidate universe covering domestic general-purpose AI, office/productivity AI, knowledge-work agents, enterprise work AI, and materially relevant cross-border products available/relevant in China.
- Instruction:
  - Establish the candidate universe before selecting Top 5.
  - Use official Chinese product documentation, pricing/help pages, product announcements, credible market evidence, and practitioner evidence according to the Charter hierarchy.
  - Separate mainland availability, overseas availability, enterprise access, and language support when relevant.
  - Explicitly record overlap with global products and borderline exclusions.
  - Do not assume that Chinese popularity automatically establishes global significance, or vice versa.
- Expected Output:
  - China candidate universe, China Representative Top 5, inclusion/exclusion rationale, regional differences, borderline candidates, evidence gaps, and cited sources.
- Artifact:
  - `research-packets/china-landscape.md` plus optional `china-landscape.html` as an intermediate visual research packet.
- Execution Boundary:
  - China regional research only. No final cross-global synthesis.
- Handoff:
  - Producer = Task 3.1.1; Artifact = China landscape packet; Consumer = Task 3.2.1 and Task 5.1.1; Purpose = independent regional evidence and comparison substrate; Verification = ChatGPT source verification and human review of the Top 5 set.
- Verification:
  - Source + Independent AI + Human.
- Rationale:
  - Kimi is selected because China-specific evidence discovery is the only material gap not already covered by the primary global research engine.
- Alternatives Considered:
  - ChatGPT Deep Research alone was considered sufficient for many China questions but rejected as the sole China path because an independent regional research engine reduces correlated coverage risk.
  - Gemini Deep Research was considered but not selected because it primarily fills a Google-source / Workspace integration role rather than a China-specific gap.

#### Step 3.2 — Normalize China product evidence

##### Task 3.2.1 — Normalize China Top 5 product cards against the common Work AI schema

- Purpose:
  - Make China products comparable to Global products without forcing them into a global-product template that hides regional differences.
- Required Capability:
  - Evidence normalization, comparative product analysis, schema alignment, regional-context preservation.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Sol high reasoning when available; fallback GPT-5.6 Luna + Think.
- Mode:
  - Standard chat / analysis using durable research artifacts.
- Thinking:
  - High / Think.
- Session:
  - Fresh China-normalization session after the Kimi artifact has been imported.
- Context:
  - `china-landscape.md`, Charter Section 7, common product-card schema, source register.
- Files:
  - Input: Kimi China packet + source URLs + common schema.
  - Output: normalized China product cards and explicit regional-difference notes.
- Connectors:
  - GitHub connector for source artifact access and durable output.
- Skills:
  - Evidence normalization instructions; no additional Skill.
- Input:
  - China Top 5 candidate records and evidence.
- Instruction:
  - Preserve region-specific facts.
  - Do not “upgrade” vendor claims into verified product capability.
  - Use the same work-positioning dimensions as Global cards.
  - Mark missing or conflicting evidence rather than filling gaps by inference.
- Expected Output:
  - China Top 5 cards compatible with the Global product-card schema, including regional-access and evidence caveats.
- Artifact:
  - Append/merge into `research-packets/product-cards.md` with explicit Global / China labels.
- Execution Boundary:
  - Evidence normalization only. Do not modify the approved Global Top 10 or invent additional products.
- Handoff:
  - Producer = Task 3.2.1; Artifact = normalized China cards; Consumer = Tasks 4.1.1, 4.2.1, 5.1.1; Purpose = common substrate for global-vs-China analysis; Verification = schema completeness + source checks.
- Verification:
  - Mechanical + Source.
- Rationale:
  - A shared schema is necessary for comparison, while explicit regional labels prevent false equivalence.
- Alternatives Considered:
  - Maintaining a separate incompatible China schema was rejected because it would make cross-region capability comparison unnecessarily difficult.
  - Merging China and global evidence without region labels was rejected because availability and product positioning can differ materially by market.

### Stage 4 — Capability, Task Fit, and Orchestration Model

#### Step 4.1 — Build the decision model

##### Task 4.1.1 — Synthesize Work AI taxonomy, task-to-capability map, and work-role map

- Purpose:
  - Convert product-level observations into the reusable conceptual model that supports the Charter's real-world objective.
- Required Capability:
  - Cross-product synthesis, taxonomy design, task/capability mapping, role modeling, abstraction without overgeneralization.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Sol high reasoning; use Extra High / max only for difficult contradictions.
- Mode:
  - Standard chat / analysis.
- Thinking:
  - High; highest setting only for final abstraction QA.
- Session:
  - Fresh synthesis session with only frozen research packets.
- Context:
  - Charter + Global landscape + China landscape + Product Cards + evidence/source register.
- Files:
  - Input: `global-landscape.md`, `china-landscape.md`, `product-cards.md`.
  - Output: canonical model.
- Connectors:
  - GitHub connector.
- Skills:
  - AI Work Advisor reasoning rules; evidence-first synthesis.
- Input:
  - Evidence-backed product/work-role observations.
- Instruction:
  - Derive categories from evidence rather than beginning from a fixed taxonomy.
  - Explain relationships among Knowledge Work, Work AI, Work Agent, Office AI, and adjacent categories.
  - Map tasks to required capabilities, then to Work AI categories/roles and product candidates.
  - Preserve uncertainty and avoid timeless product-to-task mappings.
- Expected Output:
  - Work AI taxonomy, capability map, work-role map, task-fit matrix, terminology/boundary explanation, and reusable decision chain.
- Artifact:
  - `analysis/canonical-research-model.md`.
- Execution Boundary:
  - Analytical synthesis only. No final delivery formatting.
- Handoff:
  - Producer = Task 4.1.1; Artifact = canonical research model; Consumer = Tasks 4.2.1, 6.1.1, 6.2.1, 6.3.1; Purpose = single source for all final deliverables; Verification = independent AI review + human review.
- Verification:
  - Independent AI + Human.
- Rationale:
  - The Charter's real value is the reusable decision model, not a static product catalog.
- Alternatives Considered:
  - A permanent hard-coded product→task table was rejected because the Charter explicitly rejects timeless mapping.
  - An overall product score was rejected because it would collapse role and task differences.

#### Step 4.2 — Derive orchestration patterns

##### Task 4.2.1 — Identify recurring AI orchestration patterns and one-AI sufficiency conditions

- Purpose:
  - Determine when one AI is enough and when specialist, sequential, parallel, or review-oriented multi-AI workflows materially help.
- Required Capability:
  - Workflow pattern analysis, orchestration design, reliability analysis, human-in-the-loop modeling.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Sol high reasoning; fallback GPT-5.6 Luna + Think.
- Mode:
  - Standard chat / analysis.
- Thinking:
  - High.
- Session:
  - Fresh orchestration-analysis session.
- Context:
  - Product cards + canonical research model + Charter Sections 7.8–7.9 and 12.5.
- Files:
  - Input: product and workflow evidence.
  - Output: orchestration-pattern artifact.
- Connectors:
  - GitHub connector.
- Skills:
  - Evidence-to-workflow reasoning instructions.
- Input:
  - Evidence about one-shot, iterative, artifact-centric, delegated, long-running, specialist, reviewer, and human-in-loop workflows.
- Instruction:
  - Identify repeatable patterns rather than anecdotes.
  - For every multi-AI pattern, state the concrete capability/reliability gap that justifies the second AI.
  - Explicitly document cases where one capable AI should remain the default.
  - Record human approval boundaries.
- Expected Output:
  - Named workflow archetypes, trigger conditions, handoff conditions, verification boundaries, and one-AI sufficiency criteria.
- Artifact:
  - `research-packets/orchestration-patterns.md`.
- Execution Boundary:
  - Orchestration analysis only. No implementation / automation.
- Handoff:
  - Producer = Task 4.2.1; Artifact = orchestration patterns; Consumer = Tasks 5.1.1, 6.1.1, 6.2.1, 6.3.1; Purpose = make human/AI and AI/AI allocation explicit; Verification = evidence trace + human review.
- Verification:
  - Source + Independent AI + Human.
- Rationale:
  - The Charter explicitly requires both multi-AI orchestration understanding and an explanation of when additional AI does not materially improve the workflow.
- Alternatives Considered:
  - Assuming multi-AI is always better was rejected.
  - Designing an executable agent workflow at this stage was rejected because the Charter asks for research understanding, not an implementation project.

### Stage 5 — Evidence Quality and Final Research-Model QA

#### Step 5.1 — Evidence ledger

##### Task 5.1.1 — Build and audit the claim-evidence ledger

- Purpose:
  - Make important claims traceable from claim → evidence → source → date → confidence/limitation.
- Required Capability:
  - Source normalization, evidence matching, contradiction detection, freshness validation, provenance management.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Luna for mechanical normalization; GPT-5.6 Sol high reasoning for conflict review.
- Mode:
  - Standard chat / analysis with targeted web search for unresolved freshness gaps.
- Thinking:
  - Medium for normalization; High for unresolved conflicts.
- Session:
  - Dedicated Evidence QA session, separate from synthesis.
- Context:
  - All research packets + Charter Section 9 + source register schema.
- Files:
  - Input: research packets and source URLs.
  - Output: claim-evidence ledger + source register.
- Connectors:
  - GitHub connector; targeted web search for current-source verification only.
- Skills:
  - Evidence QA instructions.
- Input:
  - Factual and comparative claims intended for final delivery.
- Instruction:
  - Verify claim/source/date alignment.
  - Mark claim status as Confirmed, Likely, Unverified, Conflicting, or Unknown.
  - Keep vendor claims separate from independent evidence.
  - Flag post-cutoff sources and determine whether they legitimately describe a pre-cutoff state.
  - Never use absence of evidence as evidence of absence.
- Expected Output:
  - Audited claim-evidence ledger and source register with explicit unresolved items.
- Artifact:
  - `evidence/claim-evidence-ledger.csv` and `evidence/source-register.csv`.
- Execution Boundary:
  - Evidence audit only. No new market-selection decision except where an evidence failure makes an existing selection untenable; such a case triggers explicit replanning.
- Handoff:
  - Producer = Task 5.1.1; Artifact = audited evidence ledger; Consumer = Tasks 5.1.2, 6.1.1, 6.2.1, 6.3.1; Purpose = prevent unsupported factual claims from entering final deliverables; Verification = source checks + mechanical completeness.
- Verification:
  - Mechanical + Source + Human for unresolved material conflicts.
- Rationale:
  - Evidence traceability is an explicit Charter success criterion.
- Alternatives Considered:
  - Manual citation checking only at the end was rejected because late-stage provenance repair is expensive and error-prone.
  - Treating AI-generated citations as automatically trustworthy was rejected.

#### Step 5.2 — Human gate

##### Task 5.2.1 — Human review gate for representative sets, model, and unresolved uncertainty

- Purpose:
  - Give the human explicit control over the key judgment points before the research model becomes the basis for final delivery.
- Required Capability:
  - Judgment, scope control, consequential decision review, uncertainty review.
- Recommended Product:
  - Human + ChatGPT review support
- Model:
  - GPT-5.6 Sol high reasoning for discrepancy explanation; human remains decision maker.
- Mode:
  - Standard chat / review.
- Thinking:
  - High for discrepancy analysis.
- Session:
  - Fresh verification session with no authority to silently modify approved judgments.
- Context:
  - Global Top 10, China Top 5, canonical research model, claim-evidence ledger, unresolved-question list.
- Files:
  - Input: all authoritative intermediate artifacts.
  - Output: explicit human approval record or revision instructions.
- Connectors:
  - GitHub connector for read/write of approval record.
- Skills:
  - Verification instructions; no new Skill.
- Input:
  - Evidence-backed selection and analytical model.
- Instruction:
  - Surface only material decisions, conflicts, or uncertainty requiring human judgment.
  - Do not present an AI-generated ranking as a recommendation.
  - Record any approved change as a specific decision.
  - If a material Charter conflict is discovered, stop and revise the Charter rather than silently changing the Work Plan.
- Expected Output:
  - Human approval / revision record for representative sets, taxonomy, practical implications, and unresolved material uncertainties.
- Artifact:
  - `analysis/human-review-gate.md`.
- Execution Boundary:
  - Review and approval only. No new broad research unless a material evidence gap is identified.
- Handoff:
  - Producer = Task 5.2.1; Artifact = human review gate; Consumer = Tasks 6.1.1, 6.2.1, 6.3.1; Purpose = authorize downstream delivery synthesis; Verification = explicit human sign-off.
- Verification:
  - Human.
- Rationale:
  - The Charter and Advisor Prompt both place human scope approval, consequential trade-offs, material uncertainty review, final judgment, and delivery approval with the human.
- Alternatives Considered:
  - Full AI autonomy was rejected because it would hide consequential interpretive choices inside synthesis.

### Stage 6 — Final Delivery Derivation

#### Step 6.1 — Research Note

##### Task 6.1.1 — Produce the canonical Research Note from the frozen evidence model

- Purpose:
  - Turn the approved research model and evidence base into the durable Markdown research note.
- Required Capability:
  - Long-form research synthesis, information architecture, evidence-linked writing, consistency control.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Sol high reasoning; fallback GPT-5.6 Luna + Think.
- Mode:
  - Standard chat / analysis using frozen artifacts.
- Thinking:
  - High; no need for maximum effort unless a material contradiction remains.
- Session:
  - Fresh final-writing session after human gate approval.
- Context:
  - Canonical model + evidence ledger + human review record + Charter deliverable requirements.
- Files:
  - Input: authoritative analysis/evidence artifacts.
  - Output: Markdown Research Note.
- Connectors:
  - GitHub connector.
- Skills:
  - Reusable research-writing instructions; no product-specific prompt hard-coding.
- Input:
  - Approved canonical research model.
- Instruction:
  - Derive all substantive conclusions from the canonical model and evidence ledger.
  - Include category framing, candidate universe, Global Top 10, China Top 5, product work positioning, task fit, taxonomy, orchestration, cross-product comparison, evidence/uncertainty, and practical implications.
  - Preserve snapshot integrity.
  - Avoid universal “best” claims.
- Expected Output:
  - Complete, navigable, evidence-backed Research Note.
- Artifact:
  - Final Research Note, e.g. `research-note.md`.
- Execution Boundary:
  - Research Note production only. No new research except targeted correction of a verified factual error.
- Handoff:
  - Producer = Task 6.1.1; Artifact = canonical Research Note; Consumer = Tasks 6.2.1 and 6.3.1; Purpose = authoritative narrative source for PPT and HTML; Verification = content/evidence consistency audit.
- Verification:
  - Source + Independent AI + Human.
- Rationale:
  - The Charter requires all three final deliverables to derive from a consistent evidence base.
- Alternatives Considered:
  - Writing PPT and HTML independently was rejected because it risks divergent conclusions and inconsistent product facts.

#### Step 6.2 — PPT

##### Task 6.2.1 — Derive the PPT from the approved Research Note / canonical model

- Purpose:
  - Communicate the same research model efficiently in presentation form.
- Required Capability:
  - Executive communication, information compression, visual hierarchy, consistency preservation.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Sol high reasoning for narrative structure; use slide-generation tooling only when available and appropriate.
- Mode:
  - Standard chat / document or presentation workflow.
- Thinking:
  - High.
- Session:
  - Fresh presentation-design session after Research Note approval.
- Context:
  - Final Research Note + canonical research model + Charter PPT requirements.
- Files:
  - Input: Research Note and canonical model.
  - Output: slide outline and presentation artifact.
- Connectors:
  - GitHub connector for source material; presentation-generation capability may vary by account.
- Skills:
  - Presentation-generation capability only if already available; do not install a new Skill solely for this case.
- Input:
  - Approved Research Note.
- Instruction:
  - Present category definition, 2026 landscape, representative products, product archetypes, task/capability map, work-role map, orchestration patterns, and implications.
  - Do not create new conclusions not supported by the Research Note.
- Expected Output:
  - PPT that is a compressed presentation of the same research model, not an independent conclusion set.
- Artifact:
  - Final PPT, e.g. `research-note.pptx`.
- Execution Boundary:
  - Presentation production only.
- Handoff:
  - Producer = Task 6.2.1; Artifact = PPT; Consumer = final human delivery review; Purpose = presentation layer of the canonical research; Verification = slide-to-source consistency check.
- Verification:
  - Mechanical + Human.
- Rationale:
  - The Charter explicitly requires the PPT to derive from the same research model.
- Alternatives Considered:
  - Authoring slides independently from raw research packets was rejected because it invites conclusion drift.

#### Step 6.3 — HTML

##### Task 6.3.1 — Derive an interactive/navigable HTML research representation

- Purpose:
  - Provide an explorable representation of the same evidence-backed research model.
- Required Capability:
  - Information architecture, interactive document generation, cross-linking, evidence navigation.
- Recommended Product:
  - ChatGPT
- Model:
  - GPT-5.6 Sol high reasoning for information architecture; current coding/tool-capable mode for implementation if available.
- Mode:
  - Standard chat with coding / artifact-generation capability when available.
- Thinking:
  - High.
- Session:
  - Fresh HTML-production session after Research Note approval.
- Context:
  - Final Research Note + canonical model + evidence ledger + Charter HTML requirements.
- Files:
  - Input: Research Note + evidence IDs/source links.
  - Output: navigable HTML artifact.
- Connectors:
  - GitHub connector for source and output persistence.
- Skills:
  - Existing coding / document skills only; no new permanent Skill required.
- Input:
  - Approved Research Note and canonical research model.
- Instruction:
  - Support landscape exploration, product comparison, task-fit navigation, work-role/orchestration views, and evidence traceability.
  - Keep displayed claims synchronized with the Research Note and ledger.
- Expected Output:
  - Interactive/navigable HTML representation with consistent conclusions and evidence links.
- Artifact:
  - Final HTML, e.g. `research-note.html` plus supporting assets if needed.
- Execution Boundary:
  - HTML production only. Do not expand scope into a general application.
- Handoff:
  - Producer = Task 6.3.1; Artifact = HTML research representation; Consumer = final human delivery review; Purpose = interactive delivery layer; Verification = link/navigation + consistency check.
- Verification:
  - Mechanical + Human.
- Rationale:
  - The Charter explicitly requests an interactive/navigable HTML representation where useful.
- Alternatives Considered:
  - Building a full permanent web application was rejected because the Charter requires a research representation, not a product.
  - A static HTML page without evidence navigation was rejected because evidence traceability is a success criterion.

## 5. Artifact & Handoff Map

| Producer Task | Artifact | Artifact Role | Consumer Task | Handoff Method | Verification Before Handoff |
|---|---|---|---|---|---|
| 1.1.1 | `research-packets/task-briefs.md` | Execution contract | 2.1.1–6.3.1 | GitHub durable file | Schema/completeness check |
| 2.1.1 | `research-packets/global-candidate-universe.md` | Candidate-universe authority | 2.2.1, 5.1.1 | GitHub file | Source/date presence; no premature ranking |
| 2.2.1 | `research-packets/global-landscape.md` | Global representative-set authority | 2.3.1, 4.1.1, 5.1.1 | GitHub file | Inclusion/exclusion rationale + human review |
| 2.3.1 | `research-packets/product-cards.md` (Global section) | Product capability evidence layer | 4.1.1, 4.2.1, 5.1.1 | GitHub file | Required-dimension completeness |
| 3.1.1 | `research-packets/china-landscape.md` | China representative-set authority | 3.2.1, 4.1.1, 5.1.1 | Kimi export → GitHub durable file | Source/date + China-context review |
| 3.2.1 | `research-packets/product-cards.md` (China section) | Normalized regional product evidence | 4.1.1, 4.2.1, 5.1.1 | GitHub file | Schema alignment + regional labels |
| 4.1.1 | `analysis/canonical-research-model.md` | Authoritative analytical model | 4.2.1, 5.1.1, 6.1.1–6.3.1 | GitHub file | Independent AI review + human gate |
| 4.2.1 | `research-packets/orchestration-patterns.md` | Workflow / handoff model | 5.1.1, 6.1.1–6.3.1 | GitHub file | Evidence linkage + one-AI sufficiency check |
| 5.1.1 | `evidence/claim-evidence-ledger.csv` + `source-register.csv` | Evidence authority | 5.2.1, 6.1.1–6.3.1 | GitHub files | Mechanical completeness + source checks |
| 5.2.1 | `analysis/human-review-gate.md` | Human approval authority | 6.1.1–6.3.1 | GitHub file | Explicit human approval |
| 6.1.1 | Research Note | Authoritative narrative delivery | 6.2.1, 6.3.1 | GitHub file | Full source/evidence consistency review |
| 6.2.1 | PPT | Presentation delivery | Human final review | GitHub/file artifact | Slide-to-note consistency |
| 6.3.1 | HTML | Interactive delivery | Human final review | GitHub/file artifact | Navigation/link/claim consistency |

### Artifact Authority

Authoritative artifacts, in descending semantic authority:

1. Approved Research Charter — defines What / Why.
2. Human Review Gate — defines approved consequential interpretations and decisions.
3. Claim-Evidence Ledger / Source Register — defines evidence provenance and currentness.
4. Canonical Research Model — defines the analytical synthesis used by deliverables.
5. Research Note — authoritative narrative representation of the model.
6. PPT / HTML — presentation and interaction layers derived from the Research Note / canonical model.
7. AI research packets — important but intermediate evidence-bearing inputs; they do not override the evidence ledger or human review record.

No chat transcript is authoritative.

## 6. Verification & Human Review

### Verification Matrix

| Artifact / Claim / Decision | Verification Level | Verification Method | Responsible Party | Exit Condition |
|---|---|---|---|---|
| Charter intent preservation | Human | Compare Work Plan against Charter requirements | Human | No material Charter requirement omitted or changed |
| Candidate universe coverage | Source + Mechanical | Check category coverage, inclusion/exclusion fields, dated evidence | ChatGPT + Human | Broad candidate universe is explainable and traceable |
| Global Top 10 set | Source + Human | Evidence-backed inclusion/exclusion review; no universal ranking | ChatGPT + Human | Human approves representative set |
| China Top 5 set | Source + Independent AI + Human | Kimi packet + ChatGPT normalization + human review | Kimi + ChatGPT + Human | Human approves representative set and regional context |
| Product capability claims | Source | Official product/help/pricing docs first; independent evidence as needed | ChatGPT | Material claims have source/date/status |
| Vendor agent claims | Source + Independent AI | Compare vendor statement with observed / independent evidence | ChatGPT | Claims labeled Fact/Vendor claim/Observed/Unknown |
| Task-fit conclusions | Source + Analysis + Human | Trace product evidence → task capability → workflow role | ChatGPT + Human | No task-fit claim lacks a reasoning path |
| Taxonomy / Work AI definitions | Analysis + Human | Cross-product consistency review against Charter definitions | ChatGPT + Human | Terms are coherent and boundaries documented |
| Orchestration patterns | Source + Independent AI + Human | Pattern recurrence check; explicit capability gap per extra AI | ChatGPT + Human | Only repeatable / supported patterns retained |
| Claim-evidence ledger | Mechanical + Source | Required fields, URL/date/status/confidence checks | ChatGPT | No material claim is provenance-orphaned |
| Research Note | Source + Independent AI + Human | Trace to canonical model and evidence ledger | ChatGPT + Human | No material unsupported or conflicting claims |
| PPT | Mechanical + Human | Slide-to-note consistency and evidence traceability | ChatGPT + Human | No material content drift |
| HTML | Mechanical + Human | Navigation, evidence links, content consistency | ChatGPT + Human | Functional and consistent |
| Snapshot integrity | Source | Confirm product facts are valid for 2026-09-24 | ChatGPT | Later changes are excluded or explicitly labeled |

### Human Responsibility

- Problem / scope approval:
  - Human approves Charter and this Work Plan before execution.
- Consequential decisions:
  - Human approves representative Global Top 10 / China Top 5, borderline product treatment, and material interpretive choices.
- Material uncertainty review:
  - Human reviews unresolved or conflicting evidence that could change the research model.
- Final judgment:
  - Human decides whether the canonical research model adequately supports the real-world objective.
- Final delivery approval:
  - Human approves Research Note, PPT, and HTML before publication / external use.

### AI Verification Responsibilities

- Research AIs:
  - Gather and synthesize evidence, but do not own final judgment.
- ChatGPT evidence QA:
  - Validate claim/source/date alignment and preserve uncertainty.
- Independent review session:
  - Challenge contradictions, missing evidence, taxonomy drift, and unsupported generalization.
- Mechanical checks:
  - Verify required dimensions, source fields, count requirements, internal links, artifact consistency, and file presence.
- Human:
  - Resolve consequential ambiguity and approve final interpretations.

## 7. Plan Assumptions / Uncertainties

### Assumptions

- The Charter v1.0 remains the governing intent and is not materially revised during execution.
- The research cutoff remains 2026-09-24.
- Work AI remains the preferred umbrella term.
- Global Top 10 / China Top 5 remain representative research sets rather than universal quality rankings.
- General-purpose AI products may enter the population when their Knowledge Work capability is materially relevant.
- The current repository structure remains available for durable artifact persistence.
- ChatGPT GitHub connector access remains available during execution.
- No new Skill is necessary before actual work begins.
- The user will review and approve the Work Plan before research execution.

### Confirmed

- The Research Charter is marked **Approved for execution**.
- The Charter explicitly defines the Global Representative Top 10 and China Representative Top 5 as research sets, not “best product” rankings.
- The Charter explicitly requires evidence traceability, snapshot integrity, and human review.
- The current OpenAI Deep Research documentation describes multi-step research, editable research planning, public web/file sources, and connected-app use.
- OpenAI's 2026 connector/release documentation includes GitHub among supported ChatGPT connectors for relevant workflows.
- OpenAI's current model documentation describes the GPT-5.6 family and plan-dependent model availability.
- Kimi's official Deep Research documentation describes Kimi-Researcher-powered research, structured research plans, multi-step search/reasoning, and Markdown/HTML report outputs.
- Google and Perplexity both have current research-capable alternatives, but neither fills a unique capability gap required by this case.

### Likely

- The two-research-engine architecture will provide materially better coverage than a single global research engine because the China market has distinct language, access, and product-context considerations.
- ChatGPT will be sufficient as the primary synthesis / QA system once durable evidence packets are available.
- Most final insights can be derived from a small number of canonical artifacts rather than maintaining many independent AI transcripts.

### Unverified

- Exact ChatGPT Deep Research quota available to the executing account on the day research starts.
- Exact model selector / reasoning settings exposed to the executing account and workspace.
- Exact availability of GitHub inside the Deep Research entry point for the executing account.
- Exact Kimi quota remaining at execution start.
- Whether any selected product or product mode changes materially between plan generation and research start.

### Conflicting

- None material to Work Plan generation at the 2026-09-24 snapshot.
- During actual research, conflicting vendor vs independent claims must be preserved explicitly rather than flattened.

### Unknown

- Which specific products will become the final Global Top 10.
- Which specific products will become the final China Top 5.
- Which product archetypes will emerge as the strongest explanatory categories.
- Which orchestration patterns will prove repeatable rather than anecdotal.
- Which adoption metrics will be sufficiently comparable to support market-significance claims.
- Where vendor-described agent behavior will differ materially from independently observed behavior.
- Whether any product's access, pricing, connector, or agent capabilities will change before the execution session.

### Replanning Triggers

- ChatGPT Deep Research becomes unavailable or materially changes the required research workflow.
- Kimi Deep Research becomes unavailable or loses the capability needed for the China track.
- GitHub connector read/write becomes unavailable.
- A material product/model/plan/availability change alters the selected execution architecture.
- A research handoff cannot be represented by a durable artifact.
- Evidence quality is insufficient to support the planned Global Top 10 / China Top 5 selection.
- A material Charter ambiguity or requirement conflict is discovered.
- The scope, deliverables, or success criteria change materially; in that case revise the Charter and generate Work Plan v2 rather than silently modifying this plan.
- Execution constraints change without changing Charter intent; update only the affected planning segment and increment to Work Plan v1.1.
