# Case 001 — 2026 AI Coding Agent Landscape

## Phase 6 — Cross-product Analysis

> Research snapshot: 2026-08-31  
> Research cutoff: August 2026  
> Status: Phase 6 completed  
> Research unit: AI Coding Agent Product / Product Family  
> Top 10 policy: **No ranking recomputation**; Phase 3 Top 10 is preserved unless a versioned correction is explicitly required.

---

## 1. Phase 6 Objective

Phase 6 does not ask which individual product is “best.” It asks what becomes visible only after the ten Phase 3 selections are placed into the same analytical frame.

The scope therefore remains exactly the one established by `00-research-charter.md`: compare product families as software-engineering agents, distinguish market significance from capability, distinguish model capability from product capability, and use public benchmarks only as supporting evidence. The Phase 6 task is to identify the structural relationships among:

- product surfaces and product forms;
- agent harnesses and execution runtimes;
- context, memory, tools, MCP and skills;
- human/agent control models;
- software-engineering workflow entry and exit points;
- market positioning and distribution;
- competitive overlap and strategic substitutes.

The strongest synthesis question is:

> **Are the Top 10 still variations of one product category, or are they already different product paradigms sharing the same underlying agentic substrate?**

The answer from the cross-product evidence is: **they are no longer a homogeneous product category in the narrow “AI coding assistant / AI IDE” sense. They form a family of related agentic software-development systems with materially different product, architecture and workflow paradigms.**

This conclusion does **not** imply that the ten products have become unrelated. They share a common agent loop—intent, context, reasoning, tool use, execution, verification and repair—but compete by moving different parts of that loop into the product boundary.

---

## 2. Research Method

### 2.1 Inputs

Phase 6 is based on the completed research chain:

1. `00-research-charter.md` — highest constraint and taxonomy;
2. `01-candidate-universe.md` — candidate population and family-level deduplication;
3. `02-market-evidence.md` — market and broad product evidence;
4. `03-ranking-methodology.md` — Phase 3 scoring and selection logic;
5. `03-top10-selection.md` — locked Top 10 and selection judgments;
6. `04-products/product-01.md` through `product-10.md` — deep product research;
7. `05-benchmarks.md` — public benchmark and independent evidence analysis;
8. targeted web verification through 2026-08-31 for time-sensitive product and market claims.

The supplied Phase 6 execution brief explicitly requires Market Matrix, Product Matrix, Agent Matrix, Architecture Matrix, benchmark integration, competition structure, paradigm identification and a final self-review. fileciteturn0file0L231-L319

### 2.2 Comparison method

Each product is first represented using the same primitives:

```text
Market
  ↓
Product Surface / UX
  ↓
Agent Harness
  ↓
Context + Memory
  ↓
Tools + MCP + Skills
  ↓
Runtime / Sandbox
  ↓
Orchestration
  ↓
Human Steering
  ↓
Workflow Outcome
```

This prevents a common analytical error: treating every visible feature as equivalent. For example, “supports MCP” is only one tool-boundary fact; it does not by itself imply stronger autonomy, better enterprise fit or better engineering outcomes.

### 2.3 Evidence states

For architecture/capability fields, this phase uses:

- **Confirmed** — directly documented by the product or supported by strong external evidence;
- **Partial** — a capability exists, but scope, semantics or surface coverage is limited/ambiguous;
- **Unknown** — the implementation detail is not publicly disclosed and is not inferred.

For market evidence, this phase keeps the distinctions established in Phase 2/3:

- **Independent signal** — survey or independent research;
- **Vendor claim** — company-reported users, customers, revenue or scale;
- **Ecosystem signal** — GitHub, distribution, enterprise/platform reach;
- **Unknown** — no comparable denominator.

### 2.4 Web verification principle

Web research was used where the August 2026 state is especially fast-moving. The most material verified updates are:

- JetBrains’ May–July 2026 developer survey reports Claude Code at 39% work adoption, Codex 16%, GitHub Copilot 21%, Cursor 12% and OpenCode 7%; the survey also notes Codex’s rapid growth and Claude Code’s leading position. These are survey adoption signals, **not global market shares**. (JetBrains, Aug 2026.)
- OpenAI reports more than 5 million weekly active Codex users as of June 2, 2026. This is a vendor metric and is retained as such.
- Qoder’s August 2026 release notes report 6M+ users and 100K+ businesses; again, this is a vendor claim, not an independently normalized market denominator.
- Cursor Cloud Agents continue to run in isolated VMs, support parallel agents, browser/desktop control, MCP and self-hosted execution; this materially strengthens the runtime/enterprise dimension of the Cursor product.
- Devin’s current product surface explicitly positions Devin Desktop as a way to manage fleets of local and cloud agents.
- Google’s Antigravity CLI uses the same harness and agents as Antigravity 2.0, supporting the family-level treatment of desktop + CLI.
- Replit Agent 4 explicitly supports parallel agents while keeping design, development, runtime and shipping inside Replit.
- Factory documents deploy-anywhere Droid execution across laptops, CI, VMs, Kubernetes and air-gapped environments.
- METR’s March 2026 study reports maintainer merge decisions about 24 percentage points below SWE-bench automated-grader scores, reinforcing the distinction between benchmark pass and real-world acceptance.

These updates reinforce the Phase 4 evidence base rather than overturn the Phase 3 selection.

---

## 3. Cross-product Comparison Framework

The four central matrices answer four different questions:

| Matrix | Question | What it should not become |
|---|---|---|
| Market Matrix | Where does each product have real-world significance? | A fake global market-share table |
| Product Matrix | How does a user start and finish software work? | A feature checklist |
| Agent Matrix | How much of the agent loop is productized? | A claim that every documented feature implies high reliability |
| Architecture Matrix | Where does the product place model, harness, runtime, context and orchestration boundaries? | A speculative reverse-engineering exercise |

The matrices are deliberately orthogonal. A product can have high market adoption but a relatively conservative architecture, or high workflow innovation but limited independent adoption evidence.

---

## 4. Market Matrix

### 4.1 Market evidence

| Product | Market adoption signal | User-base / scale evidence | Enterprise presence | Ecosystem momentum | Confidence |
|---|---|---|---|---|---|
| **Claude Code** | 39% work adoption in JetBrains May–Jul 2026 survey; highest among measured tools | Anthropic reports rapid growth; large user base, but historical vendor metrics are not used as independent denominator | Strong enterprise availability | MCP / skills / CLI ecosystem | **High** |
| **Codex** | 16% work adoption in JetBrains survey; roughly 5× January-to-May/July growth in survey | >5M weekly active users reported by OpenAI in June 2026 | Strong OpenAI enterprise footprint | Cross-surface app/CLI/IDE/cloud ecosystem | **High** |
| **Cursor** | 12% work adoption in JetBrains survey; down from 18% in Jan 2026 | Historical large enterprise footprint; latest independent user denominator unavailable | Strong and expanding, including self-hosted agents | Large AI-native developer ecosystem | **High** |
| **GitHub Copilot** | 21% work adoption in JetBrains survey | 4.7M paid subscribers and 77K+ organizations reported by GitHub | Very strong | GitHub/Actions/IDE/MCP/custom-agent ecosystem | **High** |
| **Devin** | No equivalent independent survey signal in Phase 6 | 1M+ users / 4K+ enterprise customers reported by vendor | Strongly enterprise-oriented | API/MCP/session/fleet ecosystem | **Medium–High** |
| **Google Antigravity** | 6% work adoption in JetBrains survey | Google/Gemini distribution adjacency; exact agent-only denominator unavailable | Strong Google Cloud path | Gemini/Chrome/Cloud/plugin ecosystem | **Medium–High** |
| **Replit Agent** | Agent-only independent denominator unavailable | Replit reports 50M+ platform users and 85% Fortune 500 usage; **platform-level, not agent-only** | Strong | Vertical development/runtime/deployment platform | **Medium–High** |
| **OpenCode** | 7% work adoption in JetBrains survey | Large OSS GitHub ecosystem | Community/technical-enterprise reach; weaker direct enterprise denominator | Strong OSS/provider/MCP ecosystem | **High** |
| **Qoder** | No unified independent denominator | Qoder reports 6M+ users and 100K+ businesses | Growing enterprise positioning | Skills/plugins/connectors/MCP/cloud-agent ecosystem | **Medium–High; vendor-scale constrained** |
| **Factory** | No clean independent adoption denominator located | Vendor reports hundreds of thousands of developers, enterprise customers and $1.5B valuation | Core proposition | Enterprise/runtime/deployment ecosystem | **Medium** |

### 4.2 Market interpretation

Three market layers are visible.

**First layer: independently observable mainstream adoption.** Claude Code, GitHub Copilot, Codex and Cursor have the strongest comparable independent survey signals. Claude Code is the clearest current market-adoption leader in the available August 2026 independent signal; Copilot remains structurally important despite the survey decline; Codex is the fastest-growing major product in that survey window. citeturn107849search8

**Second layer: strategic-scale products with weaker independent denominators.** Devin, Qoder, Replit and Factory all have meaningful vendor-reported scale or enterprise reach, but their numbers are not directly comparable to the JetBrains adoption percentages. Their market importance therefore comes partly from strategic positioning rather than from an independently normalized market-share estimate.

**Third layer: ecosystem-significant challengers.** OpenCode has unusually strong independent adoption evidence for an open-source project, plus a large GitHub ecosystem. This makes it more than a niche OSS experiment, but its market position still should not be equated with commercial subscriber counts. The current official OpenCode repository describes the project as open source, provider-agnostic, TUI-centered and client/server-capable, with Build and Plan agents. citeturn107849search13

### 4.3 Market judgment

> **The Top 10 is not a market-share ladder.**

It combines three kinds of significance: observed adoption, strategic distribution and product/workflow representation. This is consistent with the Charter’s distinction between Market Adoption, Product Capability and Technology Leadership.

---

## 5. Product Matrix

| Product | Primary user | Product form | UX paradigm | Workflow entry | Workflow exit |
|---|---|---|---|---|---|
| **Claude Code** | Developer / technical engineer | CLI-centered agent with multiple integrations | Terminal-first agent session | High-level engineering task in repo | Verified code change / commit / PR artifact |
| **Codex** | Developer / team | App + CLI + IDE + cloud | Delegation + supervision | Delegated software task | Code / test / PR / report; can continue in background |
| **Cursor** | Developer / team | AI-native IDE + cloud agent workspace | IDE + distributed agents | Editor task, repo task or remote task | Tested diff / artifact / PR |
| **GitHub Copilot** | Developer / enterprise team | GitHub lifecycle + IDE + CLI + cloud | Platform-native workflow agent | Prompt, issue, PR or GitHub task | PR / review / merge-oriented artifact |
| **Devin** | Engineer / engineering manager | Desktop + local/cloud agents | Agent workforce / session management | Outcome-oriented task | PR / artifact / reviewed session |
| **Google Antigravity** | Developer / agent operator | Standalone desktop + CLI | Agent command center | High-level agent task | Artifact / code change / continued agent work |
| **Replit Agent** | Developer + product/design/business builder | Cloud product-building workspace | Idea-to-production | Idea / product requirement | Running/deployed application |
| **OpenCode** | Developer | OSS terminal/TUI + desktop/client-server | User-controlled open harness | Terminal task | User-controlled patch / commit / PR |
| **Qoder** | Developer / team | IDE + CLI + Cloud Agent | Persistent task-centric workspace | Goal / Agent / Quest | Completed task / validated artifact |
| **Factory** | Enterprise engineering team | Control plane + deployable Droids | Operational agent infrastructure | Ticket / workflow trigger / engineering objective | PR / artifact / CI or deployment handoff |

### 5.1 The critical product difference

The most important cross-product distinction is not “does it edit code?” All ten do.

The more revealing question is **what object the UX treats as the primary unit of work**:

```text
Claude Code / OpenCode
    = engineering task in an executable terminal environment

Cursor
    = developer workspace + agent execution environment

Copilot
    = GitHub delivery object / lifecycle state

Codex / Devin / Antigravity
    = delegated agent workstream

Qoder
    = persistent task/spec + execution state

Factory
    = repeatable enterprise agent operation

Replit
    = product/application outcome
```

This is why a feature-by-feature comparison obscures more than it explains.

### 5.2 Product conclusion

> **The market is converging on a shared agent loop while diverging on the object that the product manages.**

This is the strongest product-level pattern in Phase 6.

---

## 6. Agent Matrix

Legend: **C = Confirmed; P = Partial; U = Unknown / not publicly disclosed**.

| Product | Planning | Context | Tools | Execution | Verification | Repair | Long-running | Multi-agent | Memory | Human steering |
|---|---|---|---|---|---|---|---|---|---|---|
| **Claude Code** | C | C | C | C | C | C | C | C | C | C |
| **Codex** | C | C | C | C | C | C | C | C | P | C |
| **Cursor** | C | C | C | C | C | C | C | C | P | C |
| **GitHub Copilot** | C | C | C | C | C | C | C | C | C | C |
| **Devin** | C | C | C | C | C | C | C | C | C | C |
| **Google Antigravity** | C | C | C | C | P/C | C | C | C | P | C |
| **Replit Agent** | C | C | C | C | C | C | C | C | P | C |
| **OpenCode** | C | C | C | C | C | C | P | C | P | C |
| **Qoder** | C | C | C | C | C | C | C | C | C | C |
| **Factory** | C | C | C | C | C | C | C* | C* | P | C |

`*` Factory’s long-running and multi-agent capabilities depend on deployment/orchestration configuration; the product model supports them, but exact fleet semantics vary by environment.

### 6.1 Planning is no longer the key differentiator

All ten products now expose some form of planning, structured reasoning or task decomposition. Therefore “has planning” is no longer a meaningful differentiator at the Top-10 level.

The stronger distinction is:

> **What is planning attached to, and what happens after planning?**

Examples:

- Kiro, although outside the final ten, shows how planning can be turned into a formal specification workflow.
- Qoder turns planning into a persistent task/Quest plus memory/execution system.
- Codex turns planning into delegation and parallel workstreams.
- Factory turns planning into a repeatable organizational Droid.
- Replit turns planning into product creation and deployment.

### 6.2 Execution + verification are the real capability boundary

Phase 5’s benchmark evidence strengthens a crucial cross-product finding: agent capability is increasingly defined by whether the system can operate an environment, observe consequences, verify and recover—not simply whether the model can write a correct code snippet.

Terminal-Bench 2.1 explicitly evaluates agent + model + runtime behavior in a terminal/container environment. In its May 2026 report, Codex CLI and Claude Code configurations showed materially different outcomes on the same benchmark family, illustrating the effect of the overall agent setup rather than model identity alone. fileciteturn8file0

The independent METR result adds a second constraint: automated SWE-bench scores can overstate real maintainer acceptance. METR observed maintainer merge decisions averaging about 24 percentage points below automated-grader results. citeturn670926search0

Therefore:

> **“Can the agent execute and pass the benchmark?” and “Will engineers accept the resulting change?” are different layers of evidence.**

### 6.3 Long-running autonomy is becoming a product primitive

Codex, Devin, Cursor, Antigravity, Replit and Qoder all make extended or background work explicit. This is qualitatively different from single-turn IDE assistance because human interaction becomes intermittent rather than continuous.

However, public documentation does not establish a common reliability threshold for “autonomous.” The term should therefore describe the **operating model**, not imply zero supervision.

---

## 7. Architecture Matrix

| Product | Model architecture | Harness | Runtime | Context | Memory | Tools | Orchestration | Sandbox / Cloud |
|---|---|---|---|---|---|---|---|---|
| **Claude Code** | Primarily Anthropic/Claude-centered | Proprietary agentic harness | Local + Anthropic cloud + remote control | Repo/file/session/rules | CLAUDE.md + auto memory + subagent memory | Shell, file, git, web, MCP | Subagents / background work | Local permissions + isolated worktrees + cloud VMs |
| **Codex** | OpenAI model family | Proprietary Codex harness | Local + cloud | Repo + AGENTS.md + task state | Partial/persistent task context | Shell, file, git, MCP, Skills | Parallel agents + Automations | Cloud isolated environments + worktrees |
| **Cursor** | Multi-model / routed | Proprietary Cursor agent harness | Local + cloud workers + self-hosted | Repo + environment | Rules/skills/context; semantic persistence less explicit | Terminal, browser/desktop, MCP, repo tools | Parallel local/cloud agents | Isolated VMs; self-hosted workers |
| **GitHub Copilot** | Multi-model / provider-agnostic at product layer | Multiple related agent runtimes | Local IDE/CLI + GitHub cloud | Repo + issues/PRs + enterprise context | Copilot Memory + instructions | GitHub tools, shell, MCP, Playwright, skills | Custom agents/subagents | Configured cloud dev environment |
| **Devin** | Multi-model / product-level abstraction | Session-centric proprietary harness | Local + cloud | Repo + session + org knowledge | Knowledge + playbooks + session history | Shell, browser, git, MCP | Child / parallel sessions + fleets | Cloud/local runtime; exact isolation varies |
| **Google Antigravity** | Gemini-centered | Shared Antigravity harness across desktop/CLI | Desktop + CLI + enterprise cloud path | Project + skills + MCP + artifacts | Partial | System/file/web/Chrome/MCP | Background agents + subagents | Terminal sandbox; enterprise cloud controls |
| **Replit Agent** | Multi-model substrate under managed platform | Tightly integrated platform harness | Managed cloud | Project + runtime + DB + design | Persistent project state; semantic memory less explicit | Platform tools + runtime/deploy | Parallel agents | Managed cloud runtime |
| **OpenCode** | Explicitly provider-agnostic | Open-source user-modifiable harness | Primarily local; remote client/server possible | Repo + LSP + session + config | Session/config persistence; rich semantic memory not defining | File, shell, web, LSP, MCP | Build/Plan/subagents | Local permissions; hosted runtime not core |
| **Qoder** | Multi-model / smart routing | Explicit task-centric harness | Local + cloud containers | Repo Wiki + rules + memory + session | First-class native memory | Shell, browser/computer use, MCP, skills | Batch/subagents/cloud agents | Cloud containers + local controls |
| **Factory** | Multi-model/provider routing | Droid harness / control plane | Laptop + CI + VM + Kubernetes + air-gapped | Just-in-time filesystem/environment context | Reusable workflows; semantic memory less explicit | Shell, filesystem, git, browser, integrations | Multiple Droids / fleet | VMs/devcontainers/K8s/air-gapped |

### 7.1 The architecture split is not “model A vs model B”

Across the ten products, five architecture boundaries repeatedly matter more than the model brand:

1. **Where execution happens** — laptop, vendor cloud, customer cloud or deploy-anywhere infrastructure.
2. **Who owns the harness** — vendor-controlled versus open/modifiable.
3. **How context is assembled** — static prompt, dynamic repository context, environment context, project memory or organizational knowledge.
4. **How many agents can act at once** — single session, parallel subagents, fleet or repeatable workflow.
5. **Where the agent enters the organization’s system** — editor, terminal, GitHub lifecycle, cloud workspace or enterprise control plane.

### 7.2 Runtime is becoming part of the product

Cursor’s public cloud-agent documentation explicitly treats isolated VMs, repositories, dependencies, secrets, network access, browser/desktop control and parallelism as prerequisites for agents that can build and verify software. Its self-hosted offering pushes this further by keeping code and tool execution inside the customer network. citeturn107849search1turn107849search0

Factory takes the same insight to the enterprise extreme: the Droid runtime is designed to operate across laptops, CI pipelines, VMs, Kubernetes and air-gapped environments. citeturn670926search1

This means the runtime is no longer merely infrastructure underneath the “real” product. **For autonomous agents, runtime constraints define what autonomy is actually possible.**

### 7.3 OpenCode represents a different architectural thesis

OpenCode is not primarily trying to win by controlling a frontier model or a vendor-hosted runtime. Its GitHub project explicitly emphasizes open source, provider agnosticism, TUI focus and client/server architecture. citeturn107849search13

Therefore OpenCode is best interpreted as an **architecture alternative** to model-vendor-owned agent stacks, rather than merely another terminal UI.

---

## 8. Benchmark Integration

### 8.1 What benchmark evidence can support

The Phase 5 benchmark layer strongly supports the following product-level propositions:

| Capability | Benchmark / evidence support | Product implication | Confidence |
|---|---|---|---|
| Repo-level issue resolution | SWE-bench / SWE-bench Verified / Kotlin Benchmark / SWE-bench Pro | Validates repo-level agent task capability | High |
| Terminal/environment operation | Terminal-Bench 2.1 / ProjDevBench | Validates continuous tool + runtime interaction | High |
| Long-horizon execution | SWE-bench Pro / Long-Horizon-Terminal-Bench | Supports the trend toward extended agent tasks | Medium–High |
| Repair / verification loops | Terminal-Bench / SWE benchmarks with executable grading | Shows that execution and feedback are part of the measured task | High |
| Language/project transfer | Kotlin Benchmark | Shows movement toward agent + real-repository evaluation across languages | High |
| Real-world acceptance gap | METR maintainer review study | Qualifies interpretation of automated pass rates | High |

### 8.2 What benchmark evidence cannot support

Existing public benchmarks do **not** provide reliable cross-product evidence for:

- best UX;
- best memory architecture;
- best human interruption/steering experience;
- enterprise security/governance quality;
- MCP ecosystem quality;
- skills/reusability quality;
- deployment convenience;
- real-world ROI;
- market adoption;
- “best product” overall.

Phase 5 explicitly concluded that these dimensions cannot be inferred from benchmark leaderboards. fileciteturn8file5

### 8.3 Product benchmark evidence is still harness-sensitive

One of the most important cross-product findings is that benchmark outcomes can move materially with the agent scaffold/harness. Phase 5 observed the same model producing different results under minimal-bash, SWE-agent-style harnesses, Claude Code, Codex CLI and other environments. fileciteturn8file4

That is not a reason to ignore models. It is a reason to reject the equation:

```text
Model score
=
Product capability
```

The correct chain is closer to:

```text
Model
×
Harness
×
Context
×
Tool policy
×
Runtime
×
Verification
→
Observed Agent Result
```

And even that does not guarantee developer productivity.

---

## 9. Product Competition Structure

### 9.1 Direct competitors

Direct competition is strongest where product surface, user, workflow and operating model overlap substantially.

#### Claude Code ↔ Codex

**Relationship: Direct competitor + architecture differentiation.**

Both compete for developers who want a terminal/command-line software-engineering agent capable of repo-level task execution. Codex extends the same category into app/cloud/parallel-agent orchestration, while Claude Code retains a particularly strong terminal-first identity. Their overlap is therefore direct at the task-execution layer, but their product center differs: **terminal agent environment vs delegated agent system**.

#### Cursor ↔ Qoder

**Relationship: Direct competitor + workflow differentiation.**

Both combine an AI-native development environment with agentic coding, multi-file changes, cloud/background work and an extensibility layer. Qoder differentiates through stronger explicit persistent memory/specification/task semantics; Cursor differentiates through its mature AI-native IDE lineage and increasingly deep cloud/self-hosted agent runtime.

#### Devin ↔ Factory

**Relationship: Direct competitor at enterprise autonomous SWE, with architecture differentiation.**

Both treat the agent as an autonomous unit of engineering labor rather than simply an editor companion. Devin emphasizes session/fleet management and human supervision; Factory emphasizes deploy-anywhere Droid infrastructure, enterprise policy and runtime portability.

### 9.2 Adjacent competitors

#### Cursor ↔ Google Antigravity

**Relationship: Adjacent competitor.**

Both are shifting toward agent-first development surfaces with local/remote/background agents. Cursor remains rooted in the AI-native IDE and engineering environment, while Antigravity more directly treats the human interface as an agent command center.

#### Codex ↔ Devin

**Relationship: Adjacent competitor.**

Both sell delegated software work and multi-agent supervision. Codex is more tightly integrated with the OpenAI/ChatGPT ecosystem and cross-surface product family; Devin is more explicitly framed as an autonomous engineering workforce and session/fleet system.

#### GitHub Copilot ↔ Claude Code / Codex / Cursor

**Relationship: Adjacent/direct in specific workflows; broader platform substitute strategically.**

Copilot can compete directly on agentic coding tasks, but its strongest differentiation is that the agent enters through GitHub’s existing software-delivery graph: issue, repository, PR, review, CI and organizational controls.

### 9.3 Workflow alternatives

#### Replit Agent ↔ Cursor / Copilot / Devin

**Relationship: Workflow alternative.**

The same user intent—“build this software”—can be solved without starting from an existing repository. Replit instead owns a vertically integrated idea → runtime → deployment workflow. This is a different category boundary rather than a weaker version of repo-centric coding.

#### Antigravity ↔ Codex / Devin

**Relationship: Workflow alternative at the human-control layer.**

All three respond to the emergence of parallel asynchronous agent work, but they choose different control surfaces: desktop command center, delegated coding app, and agent-fleet workspace.

### 9.4 Architecture alternatives

#### OpenCode ↔ Claude Code / Codex

**Relationship: Architecture alternative.**

OpenCode directly demonstrates that the harness can be decoupled from any one model provider. The competition is therefore partly about who controls the agent abstraction layer.

#### Factory ↔ SaaS-only cloud agents

**Relationship: Architecture alternative.**

Factory’s deploy-anywhere model changes the hosting/control-plane assumption itself. The alternative is not simply “another coding agent”; it is “agent runtime owned or controlled by the enterprise.”

### 9.5 Competition map

```text
                    Enterprise / Organizational Control
                                  ↑
                                  |
                         Factory  |  GitHub Copilot
                                  |
                 Devin ----------+---------- Codex
                    \            |             /
                     \           |            /
                      \      Antigravity    /
                       \         |          /
                        \        |         /
               Qoder ----+---- Cursor -----+
                         |
               Claude Code / OpenCode
                         |
                         ↓
                Developer / Terminal Control

             Replit sits orthogonally toward:
             Idea → Product → Deployment
```

This map is qualitative, not a new ranking.

---

## 10. Agent Architecture Paradigms

The final taxonomy is evidence-derived. Products can belong to more than one paradigm, but each label should identify the **dominant architectural idea** rather than every supported feature.

### Paradigm A — Terminal-first Software Engineering Agent

**Representative products:** Claude Code, OpenCode; Codex partially.

**Defining property:** the terminal/executable environment is the primary place where the agent observes, acts, verifies and repairs software.

Claude Code’s architecture makes the terminal itself a persistent agent operating environment, while OpenCode shows how that harness can remain provider-agnostic and open. Codex shares the execution model but shifts product emphasis toward cross-surface delegation.

**Core primitives:** shell, file system, repo context, tool loop, git, subagents, explicit permissions.

### Paradigm B — AI-native IDE → Distributed Agent Workspace

**Representative product:** Cursor; Qoder also overlaps.

**Defining property:** the development environment remains a first-class human surface while agent execution increasingly moves into remote/background workers.

Cursor’s Cloud Agents and self-hosted workers make environment provisioning, isolation and parallel execution part of the core product. citeturn107849search0turn107849search1

### Paradigm C — GitHub-native Software Lifecycle Agent

**Representative product:** GitHub Copilot.

**Defining property:** the agent is attached to the software-delivery graph rather than forcing users to move their work to a new agent environment.

**Core primitives:** repository, issue, PR, CI, review, enterprise policy, GitHub-native context.

This makes Copilot the clearest example of **platform-native agentification**.

### Paradigm D — Delegated Multi-agent Software Engineering System

**Representative products:** Codex, Devin, Antigravity.

**Defining property:** the product treats a task/workstream/agent session as the primary unit and assumes the human will supervise multiple asynchronous executions.

Codex explicitly describes its desktop app as a command center for multiple agents and long-running tasks. citeturn107849search5 Devin Desktop similarly positions itself as a way to manage fleets of local and cloud agents. citeturn670926search4 Antigravity uses a standalone desktop plus the same-harness CLI for invoking and monitoring agents. citeturn107849search9

### Paradigm E — Persistent Task-centric Agent Workspace

**Representative product:** Qoder.

**Defining property:** the task is persistent across specification, memory, execution, verification and cloud runtime rather than disappearing with one conversational session.

Qoder’s August 2026 release explicitly frames its product around task-centric work, continuous planning/execution/verification/self-correction, memory, plugins, skills and cloud agents. citeturn670926search5

### Paradigm F — Idea-to-Production Agent

**Representative product:** Replit Agent.

**Defining property:** the agent begins before the repository and finishes after the code, inside one managed product/runtime/deployment system.

Agent 4 explicitly supports parallel agents while keeping application design, implementation, runtime and shipping integrated. citeturn107849search6

### Paradigm G — Enterprise Autonomous SWE Control Plane / Deploy-anywhere Runtime

**Representative product:** Factory; Devin partially overlaps.

**Defining property:** the organization treats the agent as an operational unit that can run in approved infrastructure, under policy and human/automated gates.

Factory’s deployment documentation explicitly supports laptops, CI, VMs, Kubernetes and air-gapped environments. citeturn670926search1

### Paradigm H — Open / Provider-agnostic Agent Harness

**Representative product:** OpenCode.

This paradigm is orthogonal to workflow. Its key thesis is that the model provider should be a replaceable substrate while the harness remains user-owned/open.

### 10.1 Paradigm conclusion

The strongest evidence supports **eight overlapping paradigms**, not one mutually exclusive taxonomy. Some products span several:

| Product | Dominant paradigm | Secondary overlap |
|---|---|---|
| Claude Code | Terminal-first SWE Agent | Open-ish extensibility / agent-harness orientation |
| Codex | Delegated multi-agent SWE system | Terminal-first + cloud execution |
| Cursor | AI-native IDE → distributed workspace | Enterprise runtime / cloud agents |
| GitHub Copilot | GitHub-native lifecycle agent | Multi-agent cloud workflow |
| Devin | Delegated multi-agent SWE system | Enterprise agent workforce |
| Antigravity | Agent command center | Delegated multi-agent + cloud/enterprise |
| Replit Agent | Idea-to-production agent | Cloud product-building |
| OpenCode | Open/provider-agnostic harness | Terminal-first SWE |
| Qoder | Persistent task-centric workspace | Spec-driven + cloud/background agents |
| Factory | Enterprise autonomous SWE control plane | Deploy-anywhere runtime |

The taxonomy is more useful than a single “agent maturity” score because it explains **why two products with similarly strong coding ability can still feel fundamentally different to users and organizations**.

---

## 11. Software Engineering Workflow Paradigms

The architectural paradigms above describe the system design. The workflow paradigms describe what the human actually treats as the unit of work.

### Workflow A — Prompt → Code

This is the historical assistant paradigm and is no longer sufficient to explain the Top 10.

The Top 10 still supports it, but it is not the differentiator for most of them.

### Workflow B — Task → Repository → Verified Change

**Representative:** Claude Code, OpenCode.

The work unit is the engineering task. The repository is the context, and execution/testing closes the loop.

This is the strongest continuation of traditional software engineering practice with a much larger autonomous envelope.

### Workflow C — Issue → Code → PR → Review

**Representative:** GitHub Copilot.

Here the unit of work is not just a code change but a GitHub lifecycle state transition.

### Workflow D — Task Delegation → Agent Workstream → Human Review

**Representative:** Codex, Devin, Antigravity.

The human stops continuously operating the development environment and instead manages a queue or portfolio of agent workstreams.

### Workflow E — Specification → Autonomous Implementation

**Representative:** Qoder; Kiro as a near-miss comparator.

The workflow is no longer “prompt and react”; the natural-language objective becomes a structured artifact that the agent can execute against.

### Workflow F — Idea → Application → Deployment

**Representative:** Replit Agent.

This extends the workflow backward into product creation and forward into deployment.

### Workflow G — Engineering Job → Repeatable Droid → Enterprise Runtime

**Representative:** Factory.

Here the unit of work becomes an operationally repeatable engineering job governed by infrastructure and organizational policy.

### Workflow H — Agent Fleet → Engineering Workflow

**Representative:** Devin, Codex, Antigravity, and increasingly Cursor.

This is a higher-order workflow. The object is no longer one task; it is the **system for coordinating many tasks**.

### 11.1 Workflow evolution judgment

The evidence supports the following progression:

```text
Line / Function
      ↓
File / Component
      ↓
Issue / Task
      ↓
Repository
      ↓
Project / Product
      ↓
Agent Workstream
      ↓
Engineering Workflow
```

Not every product is at the last stage, but the Top 10 clearly spans from repository-task execution to workflow orchestration.

The important point is not that “code has disappeared.” It has not.

The shift is:

> **Code remains the artifact, but the task/workstream is increasingly becoming the primary unit of interaction.**

---

## 12. Capability Leaders

These are **category leaders**, not a new overall ranking.

### Terminal Agent Leader — Claude Code

**Judgment: High confidence.**

Claude Code combines the strongest independent adoption signal in the available survey with a highly developed terminal-centric agent loop and mature context/extensibility primitives. The claim is category-specific: terminal-first SWE, not “best agent overall.” citeturn107849search8

### Open-source Agent Harness Leader — OpenCode

**Judgment: High confidence.**

OpenCode’s open-source, provider-agnostic architecture and substantial community adoption make it the clearest representative of the user-owned/open harness paradigm. citeturn107849search13

### AI-native IDE / Distributed Agent Workspace Leader — Cursor

**Judgment: High confidence at category level.**

Cursor’s AI-native IDE lineage, cloud-agent VMs, parallel execution and self-hosted workers make it a defining reference for IDE-to-runtime convergence. citeturn107849search0turn107849search1

### GitHub-native Lifecycle Leader — GitHub Copilot

**Judgment: High confidence.**

No other Top-10 product has the same combination of native repository, issue, PR, review, CI, identity and enterprise-policy integration.

### Delegated Multi-agent Workspace Leader — Codex

**Judgment: Medium–High confidence.**

Codex makes multiple agents, parallel execution and long-running work a first-class user experience. This category claim is supported by product evidence; it is not a benchmark-derived “agent intelligence” ranking. citeturn107849search5

### Autonomous SWE / Agent-Fleet Leader — Devin

**Judgment: Medium–High confidence.**

Devin is the clearest product representation of the “agent as engineer / workforce” abstraction. Market-scale numbers remain vendor-reported, but the session/fleet operating model is directly documented. citeturn670926search4

### Agent Command Center Leader — Google Antigravity

**Judgment: Medium–High confidence.**

Antigravity makes agent invocation, monitoring and asynchronous work the primary UX, and its CLI shares the same harness as its desktop surface. citeturn107849search9turn107849search12

### Idea-to-Production Leader — Replit Agent

**Judgment: High confidence.**

Replit is the clearest Top-10 example where the agent’s outcome is a running/deployed product rather than a repository patch. Agent 4’s parallel-agent design reinforces this product model. citeturn107849search6

### Persistent Task-centric Agent Leader — Qoder

**Judgment: Medium–High confidence.**

Qoder’s explicit integration of memory, spec/task structure, cloud execution, skills, plugins and self-correction makes it particularly representative of persistent task-centric agent workflows. citeturn670926search5

### Enterprise Deploy-anywhere SWE Leader — Factory

**Judgment: High confidence on architecture; medium on market leadership.**

Factory is unusually explicit about runtime portability across CI, VM, Kubernetes and air-gapped environments. That supports the architecture category strongly; market leadership itself is less independently evidenced. citeturn670926search1

---

## 13. Major Market Patterns

### Pattern 1 — Independent adoption is concentrating around agentic products, not only legacy assistants

The JetBrains 2026 survey is especially important because it places Claude Code, Codex, Copilot, Cursor and OpenCode on the same professional-developer survey instrument while also showing rapid adoption growth for Codex and continued decline in relative Copilot adoption. citeturn107849search8

This supports the broader conclusion that the center of gravity has moved beyond simple autocomplete.

### Pattern 2 — Product families are expanding across surfaces

The strongest products no longer live on exactly one surface:

```text
CLI ↔ IDE ↔ Desktop ↔ Cloud ↔ GitHub/API
```

Codex, Cursor, Copilot, Devin, Antigravity and Qoder all demonstrate this. The implication is strategic: **surface convergence is becoming a product-family feature.**

### Pattern 3 — Scale and architectural significance are diverging

OpenCode and Factory illustrate opposite sides of the same issue:

- OpenCode has unusually strong ecosystem and adoption signals for an OSS project but less commercial scale;
- Factory has enterprise architecture significance that is not captured by a comparable independent adoption denominator.

Therefore market significance cannot be inferred from one numeric dimension.

### Pattern 4 — Enterprise value is increasingly about control boundaries

The enterprise differentiation is moving from “which model is smarter?” toward:

- where code executes;
- whether the runtime is isolated;
- who owns network access;
- how secrets are managed;
- whether policy gates exist;
- whether agents can run inside existing infrastructure.

Cursor self-hosting and Factory deploy-anywhere capabilities are particularly clear expressions of this trend. citeturn107849search0turn670926search1

---

## 14. Major Architecture Patterns

### Pattern 1 — Harness abstraction is becoming explicit

Phase 4 product research repeatedly found explicit separation among model, harness, tools and runtime. Phase 5’s benchmark evidence further showed that changing the harness can materially change observed performance. fileciteturn8file4

This makes the harness a first-class strategic layer.

### Pattern 2 — Runtime is moving into the product boundary

The best agents increasingly require:

```text
Code
+
Dependencies
+
Secrets
+
Network
+
Shell
+
Browser / Desktop
+
Tests
```

The environment is no longer just a place to run the result; it is part of how the agent reasons and verifies.

### Pattern 3 — Memory is becoming differentiated architecture

There is a noticeable range:

```text
Configuration / rules
  ↓
Session continuity
  ↓
Project memory
  ↓
Organizational knowledge
```

Claude Code, Copilot, Devin and Qoder make memory/rules increasingly explicit, but the semantics differ substantially. Public documentation is not yet sufficient to declare one memory architecture universally superior.

### Pattern 4 — Orchestration is becoming an externalized product layer

Once users can run multiple agents in parallel, orchestration stops being hidden implementation detail.

Codex, Devin, Antigravity, Cursor and Factory all expose some form of outer orchestration. Their key differences are the unit being orchestrated:

- agent tasks;
- sessions;
- cloud workers;
- Droids;
- enterprise workflows.

### Pattern 5 — Provider agnosticism is a strategic alternative

OpenCode and Qoder show two different approaches to model abstraction:

- OpenCode makes provider neutrality foundational and open;
- Qoder hides provider complexity behind model routing in a managed product.

This demonstrates two distinct forms of model commoditization:

> **open substitution** vs **managed substitution**.

---

## 15. Workflow Evolution

### 15.1 Is the work unit changing?

**Judgment: Yes, materially.**

The code artifact remains essential, but the user’s interaction unit is shifting upward.

Old model:

```text
Human → File → Code → Commit
```

Emerging model:

```text
Human → Task / Goal → Agent → Environment → Verification → Artifact
```

And at the organizational level:

```text
Engineering Goal
      ↓
Agent Workstreams
      ↓
Parallel Execution
      ↓
Review / Approval
      ↓
Delivery Workflow
```

### 15.2 Which products are furthest toward Level 5/6?

The evidence suggests a rough conceptual placement—not a ranking:

| Product | Dominant work-unit level | Why |
|---|---|---|
| Claude Code | Level 3–4 | Task + repository execution |
| OpenCode | Level 3–4 | Task + repo in user-controlled harness |
| Cursor | Level 4–5 | Repo + project/environment + cloud workstreams |
| GitHub Copilot | Level 3–5 | Issue/PR lifecycle and repository workflow |
| Codex | Level 4–6 | Delegated tasks + parallel workstreams + automations |
| Devin | Level 4–6 | Sessions/fleet + organizational delegation |
| Antigravity | Level 5–6 | Agent workspaces + asynchronous orchestration |
| Qoder | Level 4–5 | Persistent task/spec/memory/cloud workflow |
| Replit Agent | Level 5 | Idea → application → deployment |
| Factory | Level 5–6 | Repeatable engineering jobs + enterprise runtime |

This table is not an overall ranking. It describes **where the primary workflow abstraction sits**.

### 15.3 The likely category trajectory

The strongest evidence supports this strategic trajectory:

```text
AI generates code
        ↓
AI edits code
        ↓
AI solves tasks
        ↓
AI operates repositories
        ↓
AI executes software in environments
        ↓
AI handles projects / products
        ↓
AI runs parallel engineering workstreams
        ↓
AI becomes part of the engineering operating model
```

The Top 10 show that this is no longer only a future hypothesis. Different products are already occupying different points on the spectrum.

---

## 16. What the Top 10 Have in Common

Despite their differences, the ten products share a common substrate:

1. natural-language or high-level task intake;
2. dynamic context acquisition;
3. model-driven reasoning;
4. tool calling;
5. file/code modification;
6. executable environment interaction;
7. verification/feedback;
8. repair/iteration;
9. human review or steering;
10. increasingly long-running/background execution.

This common substrate explains why they belong in one research case.

The category therefore still has a coherent technical core.

---

## 17. What Fundamentally Differentiates Them

The differences are increasingly located above the model layer.

### 17.1 Primary control surface

- terminal;
- IDE;
- GitHub lifecycle;
- desktop command center;
- cloud workspace;
- enterprise control plane.

### 17.2 Primary work object

- task;
- repository;
- issue/PR;
- agent session;
- product/application;
- enterprise engineering job.

### 17.3 Runtime ownership

- local machine;
- vendor cloud;
- customer-managed workers;
- deploy-anywhere enterprise runtime.

### 17.4 Orchestration scope

- one agent;
- subagents;
- parallel agents;
- fleet;
- repeatable workflow automation.

### 17.5 Context and memory

- repo context;
- rules/instructions;
- session state;
- project memory;
- organizational knowledge.

### 17.6 Economic model

- subscription;
- credits;
- token/usage metering;
- managed compute;
- enterprise infrastructure costs.

These dimensions produce genuinely different businesses even when the underlying agent loop looks similar.

---

## 18. What Phase 4 Got Right

### 18.1 Correctly treating the harness as a first-class layer

Phase 4 repeatedly separated model capability from harness, tools, context and runtime. Phase 5 independently reinforced this through harness-sensitive benchmark results. fileciteturn8file4

### 18.2 Correctly identifying workflow differences

Phase 4’s labels—terminal-first, AI-native IDE, GitHub-native, cloud/autonomous, idea-to-production, provider-agnostic, persistent task-centric and enterprise Droids—survive cross-product comparison because they describe different product boundaries rather than superficial features.

### 18.3 Correctly elevating runtime and environment

Cursor, Devin, Codex, Antigravity, Qoder and Factory all show that autonomy depends on where and how the agent runs. This has become a central industry design problem rather than an implementation footnote.

### 18.4 Correctly treating memory as architecture, not prompt decoration

Qoder, Devin, Copilot and Claude Code demonstrate that persistent instruction/knowledge layers increasingly shape agent behavior over time.

### 18.5 Correctly including Replit and Factory despite imperfect comparability

Cross-product analysis confirms that excluding Replit would lose the idea-to-production paradigm and excluding Factory would lose the enterprise control/runtime paradigm. Their inclusion is analytically useful precisely because they stretch the category boundary.

---

## 19. What Phase 4 Needs Qualification

### 19.1 “Autonomous” must be treated as an operating model, not a reliability guarantee

Public product claims often use autonomous language. Cross-product benchmark and METR evidence show that autonomous execution can still require substantial human verification and that automated success does not equal maintainer acceptance. citeturn670926search0

### 19.2 Internal planner and evaluator claims remain mostly Unknown

Even strong product documentation rarely exposes the complete internal planner topology, routing policies or hidden evaluators. Phase 4 appropriately marked these details as Unknown; Phase 6 confirms that they should stay Unknown.

### 19.3 Memory claims need semantic qualification

“Has memory” does not mean the same thing across products. Rules, project knowledge, session continuity and learned semantic memory are different mechanisms. Cross-product analysis therefore keeps memory categories separate instead of declaring a single leader from feature presence alone.

### 19.4 Cloud-agent claims must distinguish product surface from runtime capability

Antigravity has a strong enterprise cloud path but is not identical to a cloud-first SWE service like Devin. OpenCode can be remote-driven but does not become a hosted cloud agent merely because client/server architecture exists. These distinctions matter.

### 19.5 Market scale claims remain heterogeneous

Vendor users, paid subscribers, enterprise customers, survey adoption and GitHub stars are not interchangeable. The Phase 3 ranking did not silently change because the same evidence problem remains in Phase 6.

### 19.6 Cursor’s corporate transition is strategic context, not product invalidation

As of August 2026, Cursor’s parent was acquired by SpaceX and OpenAI announced plans to stop providing models after November 12, 2026; Reuters also reported Anthropic increasing Claude support. This materially affects ecosystem risk and model-supply strategy, but it does not invalidate the product/workflow classification itself. citeturn670926news98

---

## 20. Key Research Judgments

### Q1 — Are the Top 10 actually one product category?

**Judgment: Not in a narrow product sense.**

They share the same technical substrate—agentic software engineering—but represent different product paradigms. “AI Coding Agent” is best treated as an umbrella category containing several distinct product forms.

### Q2 — Which Agent Architecture Paradigms exist?

**Judgment:** The evidence supports eight overlapping paradigms:

1. Terminal-first Software Engineering Agent;
2. AI-native IDE → Distributed Agent Workspace;
3. GitHub-native Software Lifecycle Agent;
4. Delegated Multi-agent Software Engineering System;
5. Persistent Task-centric Agent Workspace;
6. Idea-to-Production Agent;
7. Enterprise Autonomous SWE Control Plane / Deploy-anywhere Runtime;
8. Open / Provider-agnostic Agent Harness.

### Q3 — Which Software Engineering Workflow Paradigms exist?

**Judgment:** The most visible workflow forms are:

- Task → Repository → Verified Change;
- Issue → Code → PR → Review;
- Task Delegation → Agent Workstream → Human Review;
- Specification → Autonomous Implementation;
- Idea → Application → Deployment;
- Engineering Job → Repeatable Droid → Enterprise Runtime;
- Agent Fleet → Engineering Workflow.

### Q4 — Which are direct competitors?

**Judgment:**

- Claude Code ↔ Codex;
- Cursor ↔ Qoder;
- Devin ↔ Factory.

These pairings have the strongest overlap in product surface, user, workflow and architecture, while still retaining meaningful differentiation.

### Q5 — Which are workflow alternatives?

**Judgment:**

- Replit Agent vs repo-centric coding agents;
- Antigravity vs other agent command/delegation systems;
- GitHub Copilot vs standalone coding environments in lifecycle workflows.

### Q6 — Which products represent different leadership categories?

| Category | Representative leader / exemplar | Confidence |
|---|---|---|
| Market adoption | Claude Code | High |
| Terminal SWE agent | Claude Code | High |
| Open-source harness | OpenCode | High |
| AI-native IDE / distributed workspace | Cursor | High |
| GitHub lifecycle | GitHub Copilot | High |
| Delegated multi-agent | Codex | Medium–High |
| Agent fleet / autonomous SWE | Devin | Medium–High |
| Agent command center | Antigravity | Medium–High |
| Idea-to-production | Replit Agent | High |
| Persistent task-centric | Qoder | Medium–High |
| Enterprise deploy-anywhere runtime | Factory | High on architecture |

These are category judgments, not a new overall Top 10.

### Q7 — Is Model → Harness + Runtime + Workflow becoming the main competition unit?

**Judgment: Yes at the product-system level, with an important caveat.**

Model quality remains a major input. But the product evidence and benchmark evidence together show that competitive differentiation is increasingly created by the system around the model: harness, context, tools, execution environment, memory, orchestration, verification and workflow integration.

The emerging competition unit is better described as:

```text
Model
+
Agent Harness
+
Runtime
+
Context / Memory
+
Tools
+
Verification
+
Workflow
```

rather than model alone. Phase 5’s harness-sensitive evidence directly supports this interpretation. fileciteturn8file4

### Q8 — Is Software Engineering’s basic work unit changing from Code to Task / Repository / Project / Workflow?

**Judgment: Yes, and the Top 10 already demonstrate the transition.**

The code remains the final artifact, but the interaction object is moving upward. Replit and Factory demonstrate Level 5/6 behavior; Codex, Devin and Antigravity demonstrate multi-agent workstreams; Copilot makes the lifecycle object explicit; Claude Code and OpenCode show mature task/repository execution.

### Q9 — Which Phase 4 judgments receive joint support from cross-product comparison and benchmarks?

**Strongly supported:**

- repo-level execution is a core agent capability;
- terminal/tool interaction matters;
- verification and repair are part of the agent loop;
- long-running/environment-operating agents are becoming more important;
- harness/runtime materially affect observed outcomes;
- product differentiation cannot be reduced to model identity.

Phase 5 explicitly concluded that repo-level issue resolution, tool use + execution + verification, long-running agents and harness/runtime are all supported dimensions. fileciteturn8file6

### Q10 — Which Phase 4 judgments need lower confidence or additional caveat?

**Needs qualification:**

- “autonomous” should not imply low supervision burden;
- benchmark performance should not be treated as real-world acceptance;
- memory semantics must be differentiated by mechanism;
- cloud-agent capability must be separated from cloud/desktop surface branding;
- vendor adoption numbers remain non-comparable across products;
- internal planner/evaluator architectures remain Unknown unless directly disclosed;
- fast-moving corporate/model-provider changes can alter strategic context without immediately changing product category.

---

## 21. Phase 6 Exit Criteria

The Charter exit criterion asks whether the major product differences, commonalities, Agent Architecture Paradigms and Software Engineering Workflow Paradigms have been systematically identified.

### Assessment

| Exit criterion | Status | Evidence |
|---|---|---|
| Major product differences identified | **Complete** | Product Matrix + competition analysis |
| Major commonalities identified | **Complete** | Agent Matrix + Section 16 |
| Agent Architecture Paradigms identified | **Complete** | Eight evidence-derived overlapping paradigms |
| Software Engineering Workflow Paradigms identified | **Complete** | Seven workflow forms + evolution model |
| Market structure identified without re-ranking | **Complete** | Market Matrix + competition map |
| Benchmark integrated as supporting evidence | **Complete** | Benchmark Integration section |
| Fact / Evidence / Analysis / Judgment separated | **Complete** | Evidence states, market signal labels, judgment sections |
| Vendor claims kept distinct from independent evidence | **Complete** | Market Matrix + caveats |
| Phase 3 Top 10 preserved | **Complete** | No ranking recomputation or replacement |
| Only Phase 6 file created | **Complete** | One new repository file on Phase 6 branch |

### Phase 6 status

> **COMPLETE**

The research now has a coherent cross-product explanation of the Top 10. The ten products are not a single undifferentiated class; they are a set of related agentic software-engineering systems converging on a common execution loop while differentiating through product boundary, runtime, orchestration and workflow.

---

## 22. Source Ledger

### 22.1 Repository research inputs

- `00-research-charter.md` — Research scope, definitions, ranking guardrails and Phase 6 requirements.
- `01-candidate-universe.md` — Candidate population and family normalization.
- `02-market-evidence.md` — Market/adoption evidence and product capability evidence.
- `03-ranking-methodology.md` — Phase 3 weighting and assessment logic.
- `03-top10-selection.md` — Locked Top 10 and selection judgments.
- `04-products/product-01.md` through `product-10.md` — Product-level architecture/workflow evidence.
- `05-benchmarks.md` — Public benchmark and independent evidence.

### 22.2 Key external sources verified for Phase 6

| Source | Type | Date | Used for |
|---|---|---|---|
| JetBrains — AI coding agent adoption trends | Independent survey | Aug 2026 | Market adoption comparison |
| OpenAI — Codex app | Official | Mar 2026 | Delegation / command-center paradigm |
| OpenAI — Codex productivity report | Official | Jun 2026 | Codex weekly active users / broader usage |
| GitHub Copilot CLI/customization docs | Official | 2026 | Skills, agents, hooks, MCP, memory |
| Cursor — Cloud Agents docs | Official | 2026 | VM runtime, parallel execution, environment |
| Cursor — Self-hosted Cloud Agents | Official | Mar 2026 | Enterprise runtime boundary |
| Devin Desktop | Official | 2026 | Agent fleet / command center |
| Google Antigravity CLI | Official | May 2026 | Shared harness between CLI and desktop |
| Google Antigravity I/O 2026 | Official | May 2026 | Antigravity ecosystem / desktop paradigm |
| Replit Agent 4 | Official | Mar 2026 | Parallel agents / idea-to-production |
| OpenCode repository | Official GitHub | 2026 | Open-source, provider-agnostic harness |
| Qoder changelog / release notes | Official | Aug 2026 | Memory, continuous harness, skills, cloud agents, vendor scale |
| Factory deployment patterns | Official | 2026 | Deploy-anywhere runtime |
| METR — SWE-bench maintainer merge study | Independent | Mar 2026 | Benchmark/real-world acceptance gap |
| Reuters — OpenAI / SpaceX-owned Cursor | Independent media | Aug 29, 2026 | Current Cursor corporate/model-provider context |

### 22.3 Selected live source links

- JetBrains: https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/
- Codex app: https://openai.com/index/introducing-the-codex-app/
- Codex adoption: https://openai.com/index/codex-for-knowledge-work/
- Cursor Cloud Agents: https://cursor.com/docs/cloud-agent
- Cursor self-hosted: https://cursor.com/blog/self-hosted-cloud-agents
- Devin Desktop: https://devin.ai/desktop
- Antigravity CLI: https://www.antigravity.google/blog/introducing-google-antigravity-cli
- Antigravity I/O: https://www.antigravity.google/blog/google-io-2026
- Replit Agent 4: https://replit.com/blog/introducing-agent-4-built-for-creativity
- OpenCode: https://github.com/anomalyco/opencode
- Qoder changelog: https://qoder.com/changelog
- Factory deployment: https://docs.factory.ai/enterprise/network-and-deployment
- METR: https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- Reuters on Cursor: https://www.reuters.com/business/media-telecom/openai-end-partnership-with-spacexs-cursor-escalating-feud-with-musk-2026-08-29/

---

## 23. Final Research Judgment

> **The 2026 AI Coding Agent market is no longer primarily a contest between models embedded in coding interfaces. It is becoming a contest between agent systems that choose different boundaries for the software-engineering work they own.**

The common technical substrate is now well defined:

```text
Model
  ↓
Agent Harness
  ↓
Context / Memory
  ↓
Tools
  ↓
Runtime / Sandbox
  ↓
Verification / Repair
  ↓
Human Steering
```

But the product boundary is fragmenting into different forms:

```text
Terminal Agent
IDE Agent
GitHub Lifecycle Agent
Cloud SWE Agent
Agent Command Center
Agent Fleet
Persistent Task Workspace
Idea-to-Production Agent
Enterprise Agent Runtime
Open Provider-agnostic Harness
```

That fragmentation is not evidence that the category lacks coherence. It is evidence that the category is **maturing upward**.

The fundamental product question is shifting from:

> “How good is the model at writing code?”

toward:

> **“What part of Software Engineering can this agent system reliably own, in which environment, under which control model, and as part of which workflow?”**

This is the principal cross-product judgment of Phase 6.

The strongest strategic implication is therefore:

> **AI Coding Agent competition is moving from Model → Agent System → Engineering Workflow.**

The model remains important, but the durable product differentiation increasingly lives in **Harness + Runtime + Context/Memory + Tools + Orchestration + Verification + Workflow Integration**.

Likewise, the basic unit of interaction is moving upward:

> **Code remains the artifact; Task becomes the work unit; Repository/Project becomes the context; Workflow becomes the system boundary.**

The Top 10 already contain examples at nearly every point on this trajectory. That is the clearest evidence that the category is in the middle of a structural transition rather than a simple feature arms race.

---

## Appendix A — Self-review Checklist

| Check | Result |
|---|---|
| 1. Did Phase 6 redefine the Charter? | **No** |
| 2. Did Phase 6 recreate the Candidate Universe? | **No** |
| 3. Did Phase 6 modify the Top 10? | **No** |
| 4. Did it equate Model Capability with Product Capability? | **No** |
| 5. Did it treat benchmark ranking as product ranking? | **No** |
| 6. Did it treat vendor claims as independent evidence? | **No** |
| 7. Are major product differences sourced or clearly marked as analysis? | **Yes** |
| 8. Are functions separated from strategic/workflow differences? | **Yes** |
| 9. Is the document genuinely cross-product rather than ten mini product summaries? | **Yes** |
| 10. Are structural paradigms identified from evidence? | **Yes** |
| 11. Are Fact / Evidence / Analysis / Judgment distinguished? | **Yes** |
| 12. Was only the Phase 6 document created? | **Yes** |

---

## Appendix B — Boundary Notes

1. **Kiro** is intentionally referenced as a near-miss comparator for spec-driven workflow because Phase 3 did not include it in the locked Top 10. Its presence here does not modify the research population.
2. **Gemini CLI** is not separately counted; Phase 3 treated it as part of the Antigravity lineage based on the documented migration path.
3. **Amazon Q Developer** is not separately counted as a modern Top-10 family because of the Q → Kiro transition recorded in Phase 3.
4. **TRAE** remains a Phase 3 near-miss and is not substituted into the Top 10 merely because it overlaps strongly with AI-native IDE/agent workspace paradigms.
5. The market matrix intentionally avoids deriving a single current market-share percentage across heterogeneous evidence sources.
6. Benchmark figures are versioned and contextual; no benchmark number in this document is presented as a universal product ranking.
