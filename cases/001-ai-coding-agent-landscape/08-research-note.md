# Case 001 — 2026 AI Coding Agent Landscape

> Research note — long-term knowledge asset
> Research snapshot: **2026-08-31** · Research cutoff: **August 2026** · Verification date: **2026-08-31**
> Research unit: **AI Coding Agent Product / Product Family**
> Governing document: `00-research-charter.md` (v1.1)
> Source hierarchy: Charter → Phase 3 locked selection → Phase 4 product evidence → Phase 5 benchmark evidence → Phase 6 cross-product analysis → Phase 7 strategic judgment → `08-sources.md`
> Phase 8 status: **rendering only — no new research, no new ranking, no new judgment**

This note is written so a future reader can understand the entire Case without reading every Phase file. It is **not** a copy of Phase 7, not a chronological Phase 1–7 summary, not a feature checklist, and not a new ranking report. Every load-bearing claim traces to a Phase and, where registered, to a claim ID (`C###`) and source ID (`S###`) in `08-sources.md`.

**Label conventions (applied selectively, not mechanically):** `[FACT]` publicly stated/observable · `[EVIDENCE]` benchmark/survey/study/documentation · `[ANALYSIS]` interpretation across evidence · `[JUDGMENT]` this Case's evidence-backed conclusion · `[HYPOTHESIS]` plausible future direction, not proven · `[UNKNOWN]` not established by the reviewed evidence.

---

## 1. Research Snapshot

| Field | Value |
|---|---|
| Case | 001 — 2026 AI Coding Agent Landscape |
| Research question | As of Aug 2026, which Market / Representative Leaders constitute the AI Coding Agent market, what product/agent/workflow forms do they represent, which are defining the next direction? |
| Population | 10 Product Families — Market Significance × Technology/Product Significance (Charter §3.2), **not** user-count Top 10, **not** capability ranking |
| Evidence base | 50-candidate universe (Phase 1) → broad evidence (Phase 2) → locked Top 10 (Phase 3) → 10 deep dossiers (Phase 4) → public benchmarks (Phase 5) → cross-product matrices (Phase 6) → strategic judgments (Phase 7) |
| Central conclusion | AI Coding Agent is an **umbrella market** of agentic software-engineering systems; the technical substrate is converging while the product boundary is diverging. Competition is moving **Model → Agent System → Workflow**. |
| Standing limits | No defensible single global market-share table for Aug 2026; end-to-end autonomous engineering not proven; real-world productivity uplift incompletely measured. |

---

## 2. Executive Summary

[JUDGMENT] The 2026 AI Coding Agent market is best understood as **an umbrella market of agentic software-engineering systems, not a single homogeneous product category** (C006). The ten studied products share one technical substrate — intent, context, reasoning, tool use, execution, verification, repair — but they manage **different primary work objects** (a task, a repository, an issue/PR, an agent workstream, a product, an enterprise job). That is why a feature-by-feature comparison obscures more than it explains.

[JUDGMENT] The decisive competitive question is shifting:

> **"How good is the model at writing code?" → "What part of Software Engineering can this agent system reliably own, in which environment, under which control model, and as part of which workflow?"**

The strategic direction is therefore **Model → Agent System → Workflow** (C007): durable differentiation increasingly lives in harness, runtime, context/memory, tools, orchestration, verification and workflow integration — not in model identity alone. Model quality still sets much of the capability ceiling, so this is **not** a "model no longer matters" claim.

[EVIDENCE] The most comparable independent market signal is the JetBrains May–Jul 2026 professional-developer survey: work-adoption signals of Claude Code 39%, GitHub Copilot 21%, Codex 16%, Cursor 12%, OpenCode 7%, Google Antigravity 6% (multi-select; sums to 110%; **not** market shares — C001, C002, S001). Vendor-reported scale (Codex >5M weekly active users; Copilot 4.7M paid subscribers / 77K+ orgs; Devin 1M+ users / 4K+ enterprises; Qoder 6M+ users / 100K+ businesses; Replit 50M+ *platform* users; Factory hundreds of thousands of developers + $1.5B valuation) is retained as **Vendor claim**, never upgraded to independent evidence (C030, C031, LOCK-16).

This note answers seven questions: (1) what the market is; (2) why these ten products matter; (3) what product paradigms are emerging; (4) what parts of the stack are commoditizing; (5) where durable differentiation may emerge; (6) how the engineering workflow is changing; (7) what remains uncertain.

---

## 3. Research Scope & Method

### 3.1 What counts as an AI Coding Agent (Charter §2.1)

[FACT] An AI Coding Agent is defined as a product that accepts a relatively high-level software goal and completes parts of a software-engineering task through semi/autonomous multi-step reasoning, code modification, tool calling, execution and verification. The distinguishing criterion is **Agentic Software Engineering Capability**, not chat or code generation alone.

### 3.2 Research unit and exclusions (Charter §2.3–2.5)

- **Unit of analysis:** Product / Product Family, not company, model, client or single feature. Families expand across CLI/IDE/Desktop/Cloud surfaces; counting a family once prevents the same product from occupying multiple slots.
- **Explicitly excluded as core subjects:** pure models (GPT/Claude/Gemini/Qwen/DeepSeek) studied only as the model layer; pure completion tools without a mature agent loop; general-purpose (non-coding) agents; CI/CD, Git hosting, issue-trackers as standalone subjects.
- **Plugin-only rule:** plugin-only products do not enter the main population.

### 3.3 Method constraints carried into this note

- Separate Fact / Evidence / Analysis / Judgment (Charter §16.4; Phase 7 §1).
- Benchmark = supporting evidence, never the sole ranking authority (Charter §8.2; LOCK-15).
- No model-benchmark ↔ agent-product-benchmark conflation (Charter §8.3; LOCK-15).
- No feature-count ranking (Charter §16.9).
- Vendor claims kept distinct from independent evidence (LOCK-16).
- Unknowns preserved, never resolved (LOCK-13).

---

## 4. Market Structure

### 4.1 What the market is

[JUDGMENT] Three labels describe different layers of the same phenomenon (Phase 7 §4.1):

| Label | What it captures | 2026 status |
|---|---|---|
| AI Coding Tool | Coding assistance, editing, generation | Still widespread, insufficient to explain the leaders |
| AI Coding Agent | Multi-step task execution with tools, execution, verification | **Current core category** |
| Agentic Software Engineering Platform | Agent + runtime + workflow + orchestration + enterprise controls | **Emerging strategic layer** |

The market is best read as the **middle label expanding into the third**: agents are becoming engineering-execution systems, not just code writers.

### 4.2 Market strata (LOCK-05)

[EVIDENCE/Phase 7 §4.2] Three strata are visible; they are **not** quality tiers and must not be intra-ranked:

- **Stratum A — Independently observable mainstream adoption:** Claude Code, GitHub Copilot, Codex, Cursor — strongest comparable independent survey signals (C001, S001).
- **Stratum B — Strategic-scale agent platforms:** Devin, Qoder, Replit, Factory — meaningful platform/enterprise/workflow significance, but their scale metrics are **not** directly comparable with the JetBrains survey (C031, LOCK-16).
- **Stratum C — Open / architecture-significant challengers:** OpenCode — an open, provider-agnostic harness that itself became a significant product/ecosystem position (S069).

### 4.3 Market denominator limitation (LOCK-03)

[JUDGMENT — C005] **There is no defensible single global AI Coding Agent market-share table for August 2026 using the evidence reviewed here.** Survey adoption, paid seats, weekly active users, platform users, enterprise customers and OSS/community signals measure different objects and must not be collapsed into false precision. The JetBrains figures are multi-select survey responses that sum to 110% and are explicitly **not** shares of a single denominator (C002). China-market products (Qoder, TRAE, CodeBuddy, Kimi Code, Qwen Code) lack a unified independent denominator, so vendor scale must not mechanically push them to a global front rank (Phase 3 §7.3).

---

## 5. The Top 10

### 5.1 Locked selection (LOCK-01)

> **2026 AI Coding Agent Market Leaders / Representative Leaders — Top 10.** This is a research ranking of Market Significance × Technology/Product Significance, **not** a user-count Top 10 and **not** a capability ranking. Order is locked from Phase 3 and must not be re-sorted.

| # | Product Family | Product surface(s) | Workflow paradigm | Category / leadership role |
|---:|---|---|---|---|
| 1 | Claude Code | CLI, IDE, desktop, cloud | Terminal-first repository task execution | Market Adoption Leader · Terminal SWE Agent Leader (C019, S004/Phase 3 §9) |
| 2 | Codex | App, CLI, IDE, cloud | Delegated multi-surface / cloud SWE | Delegated Multi-agent Leader |
| 3 | Cursor | AI-native IDE, cloud agent workspace | AI-native IDE → cloud/background engineering | AI-native IDE / Distributed Workspace Leader |
| 4 | GitHub Copilot | GitHub lifecycle, IDE, CLI, cloud | Issue → Code → PR / GitHub-native workflow | GitHub Lifecycle Leader |
| 5 | Devin | Desktop, local/cloud agents | Human-managed autonomous SWE / agent fleet | Agent-Fleet / Autonomous SWE Leader |
| 6 | Google Antigravity | Standalone desktop, CLI | Agent command center + parallel async work | Agent Command Center Leader |
| 7 | Replit Agent | Cloud product-building workspace | Idea → Production application | Idea-to-Production Leader |
| 8 | OpenCode | OSS terminal/TUI, desktop client-server | Open, provider-agnostic terminal agent harness | Open-source Agent Harness Leader |
| 9 | Qoder | IDE, CLI, Cloud Agent | IDE → cloud agent platform / persistent task | Persistent Task-centric Leader |
| 10 | Factory | Control plane + deployable Droids | Enterprise autonomous SWE / Droids | Enterprise Deploy-anywhere Runtime Leader |

[UNKNOWN] The Phase 3 composite scores are a historical research record (`03-top10-selection.md` §3.1) and are **not** recomputed here. One recorded discrepancy (Jules printed 3.70 vs formula 3.75) is preserved, not corrected (H-02).

### 5.2 Product paradigm map

The Top 10 is **not** "ten similar AI IDEs." It is a set of related systems converging on a shared execution loop while differing on the object the product manages (Phase 6 §5.1):

| Product | Primary work object | Dominant paradigm | Secondary overlap |
|---|---|---|---|
| Claude Code / OpenCode | engineering task in executable terminal | Terminal-first SWE Agent | open-ish extensibility / agent-harness |
| Cursor | developer workspace + agent execution env | AI-native IDE → distributed workspace | enterprise runtime / cloud agents |
| GitHub Copilot | GitHub delivery object / lifecycle state | GitHub-native lifecycle agent | multi-agent cloud workflow |
| Codex / Devin / Antigravity | delegated agent workstream | Delegated multi-agent SWE system | cloud execution / agent fleet |
| Qoder | persistent task/spec + execution state | Persistent task-centric workspace | spec-driven + cloud/background |
| Replit Agent | product/application outcome | Idea-to-production agent | cloud product-building |
| Factory | repeatable enterprise agent operation | Enterprise autonomous SWE control plane | deploy-anywhere runtime |

[EVIDENCE — Phase 6 §5.2] The market is converging on a shared **agent loop** while diverging on **the object the product manages**. This single observation explains more than any feature matrix.

### 5.3 Why each product matters

> Per-product sections intentionally avoid copying Phase 4 dossiers. Each focuses on: why it matters, workflow paradigm, architecture significance, category role, strategic relevance, major evidence limitation. Facts draw on `products.csv` and `08-sources.md`.

**1 · Claude Code (Anthropic)** — [ANALYSIS] The clearest current market-adoption leader in the available independent survey (39% work adoption; C001) and the defining reference for the terminal as a *persistent agent operating environment* rather than a shell (C026, S023). **Workflow:** terminal-first repository task execution. **Architecture significance:** it made the harness (planning/control loop, permissions, tool use, iterative execution, compaction, extensions) a first-class strategic layer. **Category role:** Market Adoption + Terminal SWE Agent leader. **Strategic relevance:** the baseline against which "agentic execution" is measured. **Evidence limitation:** Anthropic's own usage research is a proprietary sample, not a market census (S003); internal planner/orchestrator topology and any hidden success classifier are **not public** (PF-01 `unknowns`).

**2 · Codex (OpenAI)** — [ANALYSIS] Combines >5M weekly active users (*vendor claim*, C030) with the fastest-growing major-survey signal (16%, up roughly 5× Jan→Jul 2026) and a cross-surface agent system (app/CLI/IDE/cloud) (S027–S032). **Workflow:** delegated multi-surface / cloud software engineering; the human supervises a review queue of parallel/background workstreams. **Architecture significance:** Codex treats *agent orchestration*, not code generation, as the product (PF-02 `unique_insight`). **Category role:** Delegated Multi-agent Leader. **Strategic relevance:** the strongest expression of "model-family + agent system + distribution." **Evidence limitation:** different Codex surfaces use different usage denominators; the >5M WAU figure is a vendor metric, not an independent market share (C030, LOCK-16).

**3 · Cursor (Anthropic-independent vendor; Anysphere → SpaceX)** — [ANALYSIS] The AI-native IDE reference, now extending into Cloud Agents, parallel/background execution, isolated VMs, browser/desktop control and self-hosted workers (S035–S040). **Workflow:** AI-native IDE → cloud/background engineering. **Architecture significance:** pushes runtime provisioning, isolation and parallel execution into the core product; self-hosting moves network/environment ownership inside the customer boundary (S037). **Category role:** AI-native IDE / Distributed Workspace Leader. **Strategic relevance:** defines IDE-to-runtime convergence. **Evidence limitation:** the Aug-2026 corporate transition — acquisition by SpaceX (completed 2026-08-14) and OpenAI's announced model-supply wind-down (proposed 2026-11-12 cutoff; Reuters 2026-08-29) — is **strategic/model-supply context, not a capability regression** (C032, LOCK-20). It raises ecosystem risk without invalidating the product classification.

**4 · GitHub Copilot (Microsoft/GitHub)** — [ANALYSIS] The clearest example of **platform-native agentification**: the agent enters through the existing software-delivery graph — repository, issue, PR, review, CI, enterprise policy (S043–S049). **Workflow:** Issue → Code → PR / GitHub-native workflow. **Architecture significance:** workflow integration as a moat candidate — the agent owns the lifecycle object rather than forcing work into a new environment. **Category role:** GitHub Lifecycle Leader. **Strategic relevance:** distribution through the existing collaboration graph lowers adoption friction. **Evidence limitation:** Copilot is a large family where traditional completion and agentic surfaces are hard to separate; its 4.7M paid subscribers / 77K+ orgs is vendor-reported (C031, S050). A distribution fact worth noting (not a ranking input): Copilot Pro also makes the third-party agents Claude Code and Codex available (C029, H-28).

**5 · Devin (Cognition)** — [ANALYSIS] The clearest product expression of the "agent as engineer / workforce" abstraction: session/fleet management, human supervision of many asynchronous agents (S052–S056). **Workflow:** human-managed autonomous SWE / agent fleet. **Architecture significance:** organizational knowledge, playbooks and session history as persistent agent context. **Category role:** Agent-Fleet / Autonomous SWE Leader. **Strategic relevance:** defines the "manage a portfolio of agent workstreams" operating model. **Evidence limitation:** 1M+ users / 4K+ enterprise customers are **vendor claims**; independent adoption signal is materially weaker than the head products (C031).

**6 · Google Antigravity (Google)** — [ANALYSIS] A standalone desktop "agent command center" plus a CLI sharing the same harness/agents as Antigravity 2.0, with parallel/background subagents, MCP, plugins, browser/tool use (S057–S063). **Workflow:** agent command center + parallel asynchronous work. **Architecture significance:** human supervision re-centered around agent invocation/monitoring; family-level treatment includes the Gemini CLI migration (C023, H-23). **Category role:** Agent Command Center Leader. **Strategic relevance:** Google ecosystem distribution (Gemini, Chrome, Cloud, plugin) as a scaling path. **Evidence limitation:** long-horizon market adoption is still early; Google product-line integration is fast-moving (Phase 3 §7; PF-06 `unknowns`: exact model routing policies partial/rapidly changing).

**7 · Replit Agent (Replit)** — [ANALYSIS] Not a repo-centric coding agent but an **idea → application → deployment** system: design, development, runtime and shipping stay inside one managed product (S064–S068). **Workflow:** Idea → Production. **Architecture significance:** extends the workflow backward into product creation and forward into deployment; Agent 4 adds parallel agents (S064). **Category role:** Idea-to-Production Leader. **Strategic relevance:** the clearest stretch of the category boundary toward product-building. **Evidence limitation:** Replit's 50M+ users is a **platform-level** figure, not agent-only adoption (C031); agent-only denominator is unavailable (Phase 3 §13).

**8 · OpenCode (anomalyco, OSS)** — [ANALYSIS] An open-source MIT agent harness that is explicitly provider-agnostic (75+ providers, local models), TUI-centered, client/server-capable, with Build and Plan primary agents (S069–S073). **Workflow:** open, user-controlled terminal agent harness. **Architecture significance:** demonstrates that the harness can be decoupled from any model provider — an **architecture alternative** to model-vendor-owned stacks, not merely another terminal UI (Phase 6 §7.3). **Category role:** Open-source Agent Harness Leader. **Strategic relevance:** unusually strong independent survey signal (7%) for an OSS project (C001). **Evidence limitation:** commercial market scale and enterprise adoption are significantly below the head commercial products (PF-08 `unknowns`: semantic memory not defining).

**9 · Qoder (Alibaba/Qwen lineage)** — [ANALYSIS] Among the most complete global-facing Chinese agent product families: IDE + CLI + Cloud Agents, with memory, skills, MCP, browser/computer use, batch/schedule and a continuous planning/execution/verification/self-correction harness (S074–S082). **Workflow:** IDE → cloud agent platform / persistent task. **Architecture significance:** persistent task/spec + memory + execution state as a first-class workflow. **Category role:** Persistent Task-centric Leader. **Strategic relevance:** represents the Chinese AI-native IDE → cloud agent platform route; selection is **evidence-backed, not a geographic quota** (C021). **Evidence limitation:** 6M+ users / 100K+ businesses are **vendor claims**; China lacks a unified independent denominator (C031, C036).

**10 · Factory (Factory AI)** — [ANALYSIS] Enterprise autonomous SWE via deployable "Droids" that run across laptops, CI, VMs, Kubernetes and air-gapped environments (C027, S083–S088). **Workflow:** enterprise autonomous SWE / repeatable Droids. **Architecture significance:** runtime portability and policy/governance as the product boundary; the control plane owns execution across customer infrastructure. **Category role:** Enterprise Deploy-anywhere Runtime Leader. **Strategic relevance:** its inclusion keeps the Top 10 from over-concentrating on consumer/IDE/CLI products (C020, LOCK-20). **Evidence limitation:** it has the **lowest composite among the ten** and the weakest independent adoption evidence; its presence is a recorded Research-Judgment override, **not** a sign of weakness to be footnoted away** (C020, LOCK-01). Hundreds of thousands of developers and $1.5B valuation are vendor claims (C031).

---

## 6. Product Paradigms

[EVIDENCE/Phase 6 §10] Eight overlapping architecture paradigms — not one mutually exclusive taxonomy. A product can belong to several; the label names its **dominant architectural idea**. They coexist because the products share an agentic substrate yet compete by moving different parts of the loop inside the product boundary (C006).

### Terminal SWE Agent
Claude Code, OpenCode (Codex partially). The terminal/executable environment is where the agent observes, acts, verifies, repairs. The terminal itself becomes a persistent agent operating environment.

### AI-native IDE / Distributed Workspace
Cursor (Qoder overlaps). The IDE stays a first-class human surface while execution moves to remote/background workers, isolated VMs and self-hosted infrastructure.

### GitHub Lifecycle Agent
GitHub Copilot. The agent attaches to the software-delivery graph — repository, issue, PR, review, CI, enterprise policy — rather than forcing work into a new environment.

### Delegated Multi-agent SWE
Codex, Devin, Antigravity. The task/workstream/session is the unit; the human supervises asynchronous executions, parallel agents and long-running work.

### Persistent Task-centric Agent
Qoder. The task persists across specification, memory, execution, verification and cloud runtime rather than disappearing with one conversational session.

### Idea-to-Production Agent
Replit Agent. The agent begins before the repository and finishes after the code, inside one managed runtime/deployment system; the outcome is a running product.

### Enterprise Autonomous SWE
Factory (Devin partially). The organization treats the agent as an operational unit that runs in approved infrastructure under policy and human/automated gates; deploy-anywhere runtime is the product boundary.

### Open / Provider-agnostic Harness
OpenCode. Orthogonal to workflow: the model provider is a replaceable substrate while the harness stays user-owned/open. An architecture alternative to model-vendor-owned stacks.

[JUDGMENT — C006] This taxonomy explains **why two products with similarly strong coding ability can still feel fundamentally different** to users and organizations — the difference is the product boundary, not the feature list.

---

## 7. Agent System Architecture

The stack below is the **strategic layer model — 8 ordered layers** (Phase 7 §5; LOCK-07). It is **ordered**, not ranked; no layer scores are assigned, and the 8-layer set is not reordered or extended.

| Layer | Current importance | Differentiation | Commoditization risk | Potential moat | Evidence confidence |
|---|---|---|---|---|---|
| Model | Very high | Very high today | High–Medium | Medium unless proprietary access/cost/performance is durable | High |
| Harness | Very high | High | Medium | High | High |
| Runtime / Sandbox | Very high for autonomous agents | High | Medium | High (esp. enterprise) | High |
| Context / Memory | Very high | Medium–High | Medium | Medium–High | High |
| Tools / MCP | High as substrate | Medium | **High** | Low–Medium individually | High |
| Orchestration | High and rising | High | Medium | High | High |
| Workflow Integration | Very high | Very high | Low–Medium | **Very high** | High |
| Distribution / Platform | Very high | Very high | Low | **Very high** | High |

### Model
Model quality remains strategically critical and still affects the capability ceiling (Phase 7 §5.1). Multi-model routing and provider-agnostic products make model identity increasingly replaceable in parts of the market — but this is **not** a "model is commodity" claim (C007).

### Harness
[JUDGMENT — C008] The harness is already a first-class strategic layer: it owns planning/control loops, context assembly, permissions, tool use and iterative execution. Phase 5 showed observed agent outcomes are **scaffold/harness-sensitive** — the same model produces materially different results under minimal-bash, SWE-agent-style, Claude Code and Codex-CLI harnesses (C008, S014).

### Runtime
[JUDGMENT — C009] Runtime is becoming part of the product itself (C009). Cursor's cloud-agent docs treat isolated VMs, dependencies, secrets, network, browser/desktop and parallelism as prerequisites; Factory documents Droid execution across laptop/CI/VM/K8s/air-gapped (C027); Qoder Cloud Agents run in persistent containers. For autonomous agents, **runtime constraints define what autonomy is actually possible**.

### Context / Memory
Memory is differentiating but **not standardized** (Phase 7 §5.4). Rules, session continuity, project knowledge and semantic memory are different mechanisms; no universal memory leader is proven. Public documentation is insufficient to declare one memory architecture superior (Phase 6 §14).

### Tools / MCP
[JUDGMENT — C011] Basic MCP/tool-protocol support is moving toward commodity status (Confirmed across all ten Top 10 products). Remaining differentiation comes from tool quality, ecosystem density, permissioning, reliability and workflow integration — not protocol support itself (C011).

### Orchestration
[JUDGMENT — Phase 7 §5.6] Once multiple agents run concurrently, scheduling, isolation, monitoring, aggregation, retries, approval and cost control become explicit product capabilities. Orchestration is **one of the strongest emerging moat candidates** (C010).

### Workflow
[JUDGMENT — C010] Workflow integration — technical integration + switching costs + context + distribution + organizational process ownership — is **one of the strongest likely long-term moat layers**. The duration and strength of that moat remain unproven (C010, LOCK-08).

### Distribution
Distribution can dominate otherwise similar agent systems: existing repositories, collaboration graphs, cloud ecosystems and enterprise procurement channels reduce adoption friction (Phase 7 §5.8). This is why GitHub Copilot and OpenCode occupy structurally different positions despite overlapping coding ability.

[EVIDENCE/Phase 5] The central mental model for interpreting agent results is `Model × Harness × Context × Tool policy × Runtime × Verification → Observed Agent Result` — and even that does **not** guarantee developer productivity (Phase 6 §8.3, C016).

---

## 8. Capability Commoditization

[EVIDENCE/Phase 7 §9; LOCK-08] Three layers, preserved verbatim in structure (8 commodity / 6 differentiating / 6 potential moat). No per-product "moat score" is assigned; "Product X has a moat" is never asserted.

### Commodity / rapidly commoditizing
Basic code generation · repository search / basic codebase context · terminal access · basic planning · multi-file editing · basic testing / command execution · **MCP support (commoditizing)** · **Skills / reusable instructions (commoditizing)**.

### Differentiating
Reliable verification / repair · long-running execution · context / memory quality · agent orchestration · environment integration · human steering / review UX.

### Potential moat
Runtime infrastructure · workflow integration (strong) · orchestration / control plane (strong) · organizational memory / context graph · verification / evaluation system · distribution (strong).

[JUDGMENT — C012] The market is likely to **commoditize individual agent primitives faster than complete agent systems**. Durable differentiation is more likely to come from **composition** — harness + runtime + context + orchestration + verification + workflow — than from any single feature.

---

## 9. Competitive Structure

[EVIDENCE/Phase 7 §7; LOCK-17] Relations are typed, not ranked. The map is qualitative, not a positional score.

### Direct competitors
- **Claude Code ↔ Codex** — strongest overlap at terminal/repository SWE; differ at terminal-agent-environment vs delegated agent system.
- **Cursor ↔ Qoder** — AI-native environment + agentic task + cloud/background; Qoder differentiates on explicit persistent memory/spec, Cursor on mature IDE lineage + deep cloud/self-hosted runtime.
- **Devin ↔ Factory** — autonomous SWE as an organizational work unit; differ on runtime/control assumptions (session/fleet vs deploy-anywhere Droids).

### Adjacent competitors
- **Cursor ↔ Google Antigravity** — both agent-first surfaces; human-control surfaces differ (IDE vs command center).
- **Codex ↔ Devin** — both delegated workstreams + multi-agent; differ on OpenAI ecosystem integration vs autonomous workforce framing.
- **GitHub Copilot ↔ standalone agent platforms** — competes on agentic tasks but strongest where it owns the GitHub lifecycle graph.

### Workflow alternatives
- **Replit Agent ↔ repo-centric agents** — starts from idea/product, integrates runtime + deployment; different category boundary, not a weaker repo agent.
- **Antigravity ↔ Codex/Devin** — re-centers the human around command-center supervision.
- **GitHub Copilot ↔ standalone agents (lifecycle-heavy teams)** — removes context-switching by operating on the delivery graph.

### Architecture alternatives
- **OpenCode ↔ vendor-owned harnesses** — separates agent control from model provider (open vs managed substitution).
- **Factory ↔ SaaS-only cloud agents** — moves execution ownership into enterprise infrastructure.
- **Cursor self-hosted ↔ vendor-hosted** — makes network/environment ownership part of the product boundary.

### Strategic substitutes
[JUDGMENT — Phase 7 §7.5] The competition is partly for **engineering labor allocation**, not merely editor share: human engineer + AI assistant vs human + autonomous agent vs engineer + agent fleet vs traditional team process.

---

## 10. Workflow Evolution

[EVIDENCE/Phase 7 §10; LOCK-11] The work unit is clearly rising, but has **not** universally reached whole-workflow autonomy.

**Already happened:** code generation/editing is broadly agentic; repo-level task execution is mainstream among leaders; terminal/runtime interaction is standard; long-running/background agents are productized; multiple concurrent agents exist in several leaders; task delegation is a normal mode; some products own lifecycle or deployment beyond the repository.

**Emerging now:** human supervision of portfolios of agent tasks; editors evolving toward command centers/workspaces; runtime provisioning as part of autonomy; memory/organizational knowledge as persistent context; agent economics moving toward consumption/compute; enterprise deployment demanding explicit runtime ownership and governance.

**Not yet proven:** low-review, end-to-end autonomous software delivery; reliable ownership of multi-week engineering programs; a universal agent control plane replacing IDE + Git + CI + issue tracker + cloud; durable enterprise-scale substitution of large engineering labor.

[JUDGMENT — C033] The trajectory is:

```text
Code Completion → File/Component Editing → Issue/Task Resolution → Repository-level Execution
→ Project/Product Work → Delegated Agent Workstream → Parallel Agent Portfolio → Engineering Workflow Automation
```

The code remains the artifact; the **task/workstream is increasingly the primary unit of interaction** (Phase 6 §11.1). The transition to `Agent Workstream → Engineering Workflow` is visible in product design but only partially proven in independent productivity evidence.

---

## 11. Category Leadership

[EVIDENCE/Phase 7 §8; LOCK-10] Category judgments, **not** a second overall ranking. "Leader" = strongest representative of a category under the reviewed evidence, not universally best overall.

| Leadership category | Representative | Confidence |
|---|---|---|
| Market Adoption | Claude Code | High |
| Terminal SWE Agent | Claude Code | High |
| Open-source Agent Harness | OpenCode | High |
| AI-native IDE / Distributed Workspace | Cursor | High |
| GitHub Lifecycle | GitHub Copilot | High |
| Delegated Multi-agent | Codex | Medium–High |
| Agent-Fleet / Autonomous SWE | Devin | Medium–High |
| Agent Command Center | Google Antigravity | Medium–High |
| Idea-to-Production | Replit Agent | High |
| Persistent Task-centric | Qoder | Medium–High |
| Enterprise Deploy-anywhere Runtime | Factory | High on architecture; Medium on market leadership |

---

## 12. Strategic Scenarios

[EVIDENCE/Phase 7 §12; LOCK-12] Three scenarios; the support ordering is a strategic judgment, **not** a calibrated probability forecast. No percentages or timelines are assigned.

- **Scenario A — Model Dominates.** Frontier-model progress remains so rapid that model quality is the main differentiator and harness/runtime standardizes. *Plausible, but no longer sufficient as the default market model.* Limiting evidence: multi-model routing, provider-agnostic products, harness-sensitive benchmarks, runtime-heavy systems.
- **Scenario B — Agent System Dominates.** Harness + runtime + context + memory + tools + orchestration become the main differentiators around still-important models. *Most supported current trajectory.* Confidence: Medium–High.
- **Scenario C — Workflow Platform Dominates.** Agent systems embed in complete dev workflows (intake, spec, execution, review, deployment, governance, workforce management). *Strong strategic direction, but not yet proven as the final winning structure.*

[JUDGMENT] 2026 strategic support ordering: **Scenario B > Scenario C > Scenario A** (C007). This ordering is explicitly "not a calibrated probability forecast."

---

## 13. Risks, Unknowns & Evidence Gaps

### Key risks (Phase 7 §13)
1. **Benchmark limitations** — automated grading can overstate production acceptance (C013).
2. **Productivity measurement uncertainty** — real-world uplift is noisy and selection-sensitive (C014).
3. **Vendor-claim risk** — user/customer counts are not comparable across products (C031, LOCK-16).
4. **Market denominator gaps** — no unified public denominator covers commercial, OSS and China-market products (C036).
5. **Model-change risk** — frontier improvements can quickly shift product capability.
6. **Product-boundary risk** — families are actively acquiring, renaming and expanding surfaces (C022–C025).
7. **Runtime reliability risk** — provisioning, dependencies, network, secrets, browser state, flaky tests dominate long-horizon outcomes.
8. **Long-horizon autonomy risk** — background execution ≠ reliable multi-week autonomy.
9. **Enterprise adoption risk** — ROI, security outcomes and labor leverage remain under-measured.
10. **Ecosystem concentration risk** — distribution can increase dependency on a model/provider ecosystem.

### Standing Unknowns (preserved, not resolved — LOCK-13)
| Unknown | Why it matters | Status |
|---|---|---|
| Exact hidden planner architectures | Could explain capability differences | Not public for most vendors |
| Exact model routing policies | Determines economics/performance | Partial / rapidly changing |
| True agent-level market share | Needed for stronger market claims | No unified public denominator (C036) |
| Real long-horizon production success rates | Critical to "AI engineer" claims | Insufficient independent evidence |
| True enterprise ROI | Needed for labor-leverage thesis | Fragmented public evidence |
| Quality of semantic memory | Important for persistent workflows | Early / non-standardized |
| Reliability of multi-agent fleets | Necessary for organizational delegation | Thin independent measurement |
| Human review burden at scale | Determines real autonomy/economics | Under-measured |
| Security outcomes | Critical for enterprise deployment | No stable cross-product standard |
| Durability of workflow lock-in | Determines moat strength | Plausible, not proven |
| Persistence of current categories | Product boundaries change quickly | High uncertainty |

[UNKNOWN — C035] **End-to-end autonomous software engineering is NOT proven**; reliable low-supervision autonomous delivery remains unproven. This is a limit of the evidence, not a gap to be filled during asset production.

---

## 14. Research Limitations

- **No new research.** This note renders the locked Phase 0–7 record; it introduces no candidate, score, share, ranking, product judgment or strategic claim (G3).
- **Evidence window.** All findings are bounded to the August 2026 cutoff; fast-moving facts (model supply, acquisitions, product renames) are date-stamped, not stated as "current" (LOCK-19).
- **Benchmark as supporting only.** No public benchmark measures full product value; benchmark scores are never converted into product or productivity claims (C016, LOCK-15).
- **Vendor claims isolated.** All scale figures carry their vendor-claim label and are never normalized into a market share (C030, C031, LOCK-16).
- **No false precision.** The JetBrains figures are multi-select survey signals that do not sum to 100% and are never rendered as a share of total (C002, LOCK-04).
- **Known discrepancies preserved.** Jules' composite discrepancy (H-02), the Claude Code revenue-date anomaly (H-03), DevBench status conflict (H-12), Phase 1 count discrepancy (H-14) and benchmark version drift (H-13) are carried, not corrected.
- **Phase 0–7 untouched.** This asset adds no line to any Phase 1–7 file.

---

## 15. Update Protocol

This note is a living asset. Re-run the following before any refresh:

1. **Re-pull the independent denominator.** The single biggest gap is a unified, comparable adoption denominator across commercial, OSS and China-market products (C036). Until one exists, do **not** compute a market-share table.
2. **Re-verify vendor claims at the cutoff.** Re-confirm Codex >5M WAU, Copilot 4.7M/77K, Devin 1M+/4K, Qoder 6M+/100K, Replit 50M platform, Factory scale — each still as vendor claim (LOCK-16).
3. **Check product-boundary moves.** Family renames/mergers (Q Developer→Kiro, Gemini CLI→Antigravity, Windsurf→Devin Desktop, Tongyi Lingma→Qoder) must keep the dedup logic intact (C022–C025, LOCK-14).
4. **Refresh the Benchmark layer against versioned IDs.** Never merge Terminal-Bench 2.0 with 2.1; keep SWE-rebench as unvalidated; keep benchmark results pinned to version + configuration (H-13, LOCK-15).
5. **Re-test the three scenarios.** Support ordering B > C > A is a judgment, not a forecast; revisit if harness/runtime standardization or workflow-platform consolidation shifts.
6. **Preserve the semantic locks.** Top 10 order (LOCK-01), market-denominator caveat (LOCK-03), JetBrains non-share rendering (LOCK-04), vendor-claim separation (LOCK-16) and Unknown preservation (LOCK-13) are invariants across updates.
7. **Never silently fix history.** Any genuine factual error in Phase 1–7 is raised as a proposed versioned correction; the asset preserves the historical value and records the discrepancy (canonical model §10.4).

---

## Appendix A — Product Matrix

Condensed from `08-dataset/products.csv` (10 rows × 44 cols). Capability cells use `Confirmed / Partial / Unknown / Not primary`; `C*` denotes a configuration-dependent Confirmed (caveat preserved); `P/C` normalizes conservatively to Partial. `Unknown` is shown as Unknown, never blank.

| # | Product | Surfaces | Workflow paradigm | Planning | Exec | Verify | Long-run | Multi-agent | Memory | MCP | Skills | Sandbox | Cloud agent | Leadership role | Confidence |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Claude Code | CLI/IDE/desktop/cloud | Terminal-first repo task | C | C | C | C | C | C | C | C | P* | C | Market + Terminal Leader | High |
| 2 | Codex | App/CLI/IDE/cloud | Delegated multi-surface | C | C | C | C | C | P* | C | C | C | C | Delegated Multi-agent | High |
| 3 | Cursor | IDE/cloud workspace | AI-native IDE→distributed | C | C | C | C | C | P* | C | C | C | C | AI-native IDE Leader | High |
| 4 | GitHub Copilot | Lifecycle/IDE/CLI/cloud | Issue→Code→PR | C | C | C | C | C | C | C | C | C | C | GitHub Lifecycle Leader | High |
| 5 | Devin | Desktop/local+cloud | Autonomous SWE/fleet | C | C | C | C | C | C | C | C | C | C | Agent-Fleet Leader | Medium-High |
| 6 | Google Antigravity | Desktop/CLI | Agent command center | C | C | P/C* | C | C | P* | C | C | C | P* | Agent Command Center | Medium-High |
| 7 | Replit Agent | Cloud workspace | Idea→Production | C | C | C | C | C | P* | C | C | C | C | Idea-to-Production Leader | High |
| 8 | OpenCode | OSS TUI/client-server | Open provider-agnostic | C | C | C | P* | C | P* | C | C | P* | P* | Open-source Harness Leader | High |
| 9 | Qoder | IDE/CLI/Cloud Agent | Persistent task-centric | C | C | C | C | C | C | C | C | C | C | Persistent Task-centric | Medium-High |
| 10 | Factory | Control plane/Droids | Enterprise autonomous SWE | C | C | C | C* | C* | P* | P* | P* | P* | P* | Enterprise Deploy-anywhere | Medium |

\* `C*` = Confirmed with configuration/orchestration dependency caveat (Factory long-running/multi-agent depend on deployment config; Antigravity verification is `P/C` normalized to Partial). `P*` = Partial (e.g. Claude Code sandbox surface-dependent → Partial; OpenCode/Replit/Factory memory partially public → Partial). Legend: C = Confirmed, P = Partial, U = Unknown, Not primary = out of scope.

## Appendix B — Evidence / Source Index

All claims resolve to `08-sources.md`, which holds 36 claims (C001–C036) and 131 sources (S001–S123 external + S200–S208 internal). Key load-bearing references:

| Topic | Claim | Source(s) |
|---|---|---|
| Independent adoption signal + non-share | C001, C002 | S001 (JetBrains Aug 2026) |
| No global market-share table | C005 | S001; S031; S050; S056; S074; S208 |
| Umbrella market / substrate converging | C006 | S207; S208 |
| Model → Agent System → Workflow | C007 | S014; S023; S085; S208 |
| Harness is first-class layer | C008 | S023; S029; S085; S206 |
| Runtime is part of product | C009 | S040; S037; S084; S077 |
| Workflow integration as moat | C010 | S045; S064; S084; S208 |
| MCP commoditizing | C011 | S023; S040; S069; S078; S208 |
| Commoditization of primitives | C012 | S208 |
| Benchmark pass ≠ maintainer acceptance | C013 | S006 (METR 2026-03-10) |
| No clean productivity estimate | C014 | S007; S008 (METR) |
| METR 1.5×–13× is soft upper bound | C015 | S009 |
| No benchmark measures full product | C016 | S012–S020; S206 |
| Terminal-Bench 2.1 harness sensitivity | C018 | S014 |
| Phase 3 Top 10 is locked research ranking | C019 | S200; S203; S204; S206 |
| Factory override at #10 | C020 | S204; S087 |
| Qoder evidence-backed, not quota | C021 | S204; S074; S082 |
| Family dedup (Q→Kiro, Gemini→Antigravity, Windsurf→Devin, Lingma→Qoder) | C022–C025 | S089/S090; S062/S061; S052; S082 |
| Vendor scale claims | C030, C031 | S031; S056; S074; S066 |
| Cursor transition = context not regression | C032 | S042; S005; S208 |
| Work unit rising but not whole-workflow autonomy | C033 | S001; S008; S208 |
| 47% agent-generated = derived midpoint | C034 | S123 |
| End-to-end autonomy not proven | C035 | S006; S008; S208 |
| True agent-level share unknown | C036 | S001; S208 |

**Full ledger:** `08-sources.md` — Section A (Claim Ledger, C001–C036), Section B (Source Registry, S001–S123 + S200–S208), Section C (Phase provenance, normalization rules, known discrepancies H-02/03/12/13/14, universe boundary, time handling). Phase ownership: P1 Candidate Population · P2 Market/Evidence · P3 Selection · P4 Product Evidence · P5 Benchmark · P6 Cross-product · P7 Strategic Judgment · P8 Rendering only.

---

**Document status:** Phase 8 Task 3 deliverable. Renders the locked Phase 0–7 record. No Phase 1–7 file modified. No new research content introduced.
