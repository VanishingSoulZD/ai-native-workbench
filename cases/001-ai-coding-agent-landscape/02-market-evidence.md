# Case 001 — 2026 AI Coding Agent Landscape

## Phase 2 — Market & Evidence Collection

> Research snapshot: 2026-08-31
>
> Research cutoff: August 2026
>
> Status: Phase 2 evidence collection completed for the Core Candidate set; targeted boundary checks completed
>
> Research unit: AI Coding Agent Product / Product Family

---

## 1. Phase 2 Objective

本阶段严格承接 `00-research-charter.md` 与 `01-candidate-universe.md`，只完成 **Market & Evidence Collection**。

目标不是形成最终 Top 10，而是为后续 Phase 3 建立可审计的：

`Claim → Evidence → Source → Date → Confidence → Analysis`

证据基础。

本阶段重点回答：

1. Candidate 在现实市场中的采用与重要性如何？
2. 产品的 Agent Loop、Execution、Verification、Repair、Long-running、Subagents 等能力有哪些公开证据？
3. Product / Agent architecture 如何与 underlying model、runtime、sandbox、MCP、skills、memory/rules 区分？
4. 产品正在改变哪一段 Software Engineering Workflow？
5. 哪些证据可以支持后续 Ranking，哪些仍然 Unknown？
6. Phase 1 的产品家族边界是否出现了需要显式修正的重大状态变化？

**本阶段不计算最终 Composite Score，不进行 Final Top 10 Selection，不进入 Phase 3。**

---

## 2. Evidence Collection Methodology

### 2.1 Evidence hierarchy

优先级遵循：

`Tier 1 Primary → Tier 2 Independent → Tier 3 Community / Discovery → Tier 4 Individual Review`

关键市场事实优先寻找：

- 官方产品页 / 文档 / release notes
- 官方公司公告 / 财务披露 / 研究
- 独立开发者调查
- 高质量公开 benchmark
- GitHub ecosystem signals

社区资料只用于发现产品、用户体验、争议和趋势，不承担重大市场事实的唯一证明责任。

### 2.2 Evidence grade

| Grade | Meaning |
|---|---|
| A | Strong Evidence：一手来源或高质量独立来源，Claim 与 Evidence 高度匹配 |
| B | Good Evidence：可信官方/独立来源，但存在口径、时间或独立性限制 |
| C | Indicative Evidence：可作为方向信号，但不适合单独支撑重大结论 |
| D | Weak Evidence：信息不完整、单一来源或仅能做发现线索 |

**Evidence Grade ≠ Product Quality。**

### 2.3 Claim type discipline

本稿将以下三类明确分开：

- **Vendor Claim**：厂商自己公布的用户、客户、ARR、使用规模等数字；
- **Independent Evidence**：JetBrains 等独立调查或第三方 benchmark；
- **Product Fact**：官方文档对功能、架构、surface 的直接描述。

不同口径不做强行横向归一化。

---

## 3. Market Evidence Overview

### 3.1 Highest-value independent market signal

JetBrains 2026 年 8 月的 AI Coding Agents 调查覆盖 **15,000+ professional developers**，调查时间为 May–July 2026。报告显示：90% 的受访专业开发者在工作中至少每周使用 AI coding agents，68% 每天使用。

在“工作中使用的 agent”这一调查口径下，代表性采用率约为：

| Candidate | JetBrains May–Jul 2026 adoption signal | Interpretation |
|---|---:|---|
| Claude Code | 39% | Strong independent adoption signal |
| GitHub Copilot | 21% | Strong independent adoption signal；需注意与历史调查口径/产品形态差异 |
| Codex | 16% | Strong and rapidly rising independent signal |
| Cursor | 12% | Strong independent signal；2026 年较早期调查下降 |
| OpenCode | 7% | Strong independent signal for an OSS project |
| Google Antigravity | 6% | Emerging but material signal |
| JetBrains AI / Junie | ~9% combined | Product-family signal；二者存在用户重叠 |

该调查不能解释为“全球所有开发者的市场份额”。它是一个 **professional developer survey adoption signal**。尤其需要避免把 39% / 21% / 16% / 12% 直接放在同一统计口径下作为绝对市场份额排名。

### 3.2 Market evidence that is strong but vendor-reported

| Candidate | Current evidence | Date / scope | Evidence type |
|---|---|---|---|
| Codex | >5M weekly active users | OpenAI, 2026-06-02 | Vendor Claim |
| GitHub Copilot | 4.7M paid subscribers; 77K+ organizations | Current GitHub newsroom | Vendor Claim |
| Devin | 1M+ users; 4,000+ enterprise customers | Devin current product page | Vendor Claim |
| Qoder | 6M+ users worldwide; 100K+ businesses | Qoder, 2026-08 | Vendor Claim |
| Replit | 50M+ users globally; 85% of Fortune 500 use Replit | Replit, 2026 | Vendor Claim; applies to Replit platform, not agent-only adoption |
| Factory | Hundreds of thousands of developers; named enterprise users; $1.5B valuation | Factory, 2026-04-16 | Vendor Claim |
| Cursor | >50% Fortune 500 use reported in earlier company disclosure | 2025-06 historical baseline | Vendor Claim; stale relative to Aug 2026 |
| Claude Code | Anthropic reported >$2.5B run-rate revenue and weekly active users doubled since Jan 2026 in an Aug 2025 disclosure | 2025-08 historical baseline | Vendor Claim; important but stale |

The practical conclusion is not that any one vendor number is “the market truth”. The useful role is triangulation: independent survey + company disclosures + ecosystem signals.

---

## 4. Market Adoption Evidence

### 4.1 Core candidate market evidence matrix

| Candidate | Adoption / market evidence | Source quality | Assessment |
|---|---|---|---|
| Claude Code | 39% in JetBrains May–Jul 2026 survey; Anthropic separately reported strong growth and >$2.5B historical run-rate baseline | A/B | **High** |
| Codex | >5M weekly active users in OpenAI June 2026 disclosure; 16% JetBrains survey adoption | A | **High** |
| GitHub Copilot | 4.7M paid subscribers, 77K+ orgs in current GitHub newsroom; 21% JetBrains survey adoption | A | **High** |
| Cursor | 12% JetBrains survey adoption; historical Fortune 500/ARR disclosure; Aug 2026 SpaceX acquisition materially changes strategic context | A/B | **High** |
| Devin | 1M+ users / 4K+ enterprises reported by vendor; limited independent survey visibility | B | **Medium–High** |
| Google Antigravity | 6% JetBrains survey adoption; Google product ecosystem / Gemini CLI transition adds large installed-base adjacency | A/B | **Medium–High** |
| Kiro | No strong independent adoption number located; AWS distribution and Q migration provide strategic evidence | B | **Medium / Unknown on absolute adoption** |
| Replit Agent | Replit platform >50M users; Agent 4 has strong product adoption context, but agent-only user number not disclosed | B | **Medium–High (platform-level)** |
| OpenCode | 7% JetBrains survey adoption; GitHub repo ~194K stars and ~24.8K forks at research time | A | **Medium–High** |
| OpenHands | Large open-source ecosystem, Cloud / Enterprise adoption signals; no clean independent market-share number | B | **Medium** |
| Cline | ~63K GitHub stars / 6K+ forks; strong open-source activity; no comparable independent user denominator | A/B | **Medium** |
| Qoder | Vendor reports 6M+ users and 100K+ businesses; independent adoption data limited | B | **Medium–High, confidence constrained by vendor-only scale claims** |
| TRAE | Vendor reports hundreds of thousands of developers using TRAE historically; current independent adoption number not located | B | **Medium / Unknown** |
| Tencent CodeBuddy | Strong China strategic footprint; product docs show CLI/Cloud/enterprise capability; comparable independent adoption data not located | B/C | **Medium / Unknown** |
| JetBrains AI / Junie | ~9% combined JetBrains survey signal; JetBrains reports Junie 343K users in 2025 milestone | A/B | **Medium–High** |
| Kimi Code | Current CLI/IDE product and strong model-company momentum; product-specific independent adoption number not located | B/C | **Medium / Unknown** |
| Amazon Q Developer | Large AWS enterprise installed base historically, but coding CLI/IDE surface is being migrated/rebranded to Kiro | A | **Transitional / do not treat as independent modern market family in Phase 3** |

### 4.2 China adoption evidence

中国市场的主要证据问题不是“没有产品”，而是“缺少统一、独立、可比的公开 adoption denominator”。

目前更可靠的信号包括：

- JetBrains 2026 survey 的中国分市场数据，可用于观察国际产品在中国的相对采用情况；
- Qoder / Qoder CN、TRAE、Tencent CodeBuddy、Kimi Code、Qwen Code、Comate 等官方产品规模与生态数据；
- GitHub ecosystem signals；
- 企业客户案例与官方渠道。

但截至研究截点，没有找到一份同时覆盖上述中国 Coding Agent、具有统一样本和统计口径的公开独立市场份额调查。因此，中国候选的 **Market Adoption** 在 Phase 3 不应伪装成与 Claude Code / Copilot 同等精度的市场分数。

---

## 5. Product / Agent Capability Evidence

以下不是“功能清单”，而是对 Agent Loop 的证据化归纳。

### 5.1 Claude Code

**Observed loop**：Human task → repo/context discovery → reasoning → file edits / shell / tools → tests & verification → iterative repair。

官方 Claude Code 文档进一步支持 subagents、独立 context windows、custom instructions、tool permissions、MCP、hooks、memory scope 与 worktree isolation 等机制。

**Architecture evidence**：Agent/harness + terminal/tool layer + project/user memory/rules + MCP/hooks；underlying model 与 harness 分开处理。

**Workflow change**：从“IDE 中辅助写代码”向“terminal-first repository task executor”迁移。

Evidence: A/B.

### 5.2 Codex

**Observed loop**：Task delegation → repository context → agent reasoning → code/tool execution → tests/checks → repair → artifact/PR；支持多任务并行与 cloud delegation。

OpenAI 2026 年产品路线把 Codex 明确延伸为一个跨 App / CLI / IDE / Cloud 的 agent system，而非单一 editor feature。并行任务和 1 小时以上任务的使用增长是重要 workflow signal。

**Architecture evidence**：Codex product + Codex CLI/app/cloud harness + tools + skills/automations/MCP + remote execution。

**Workflow change**：从“问模型写代码”变为“把工程任务委派给可持续执行的 software agent”。

Evidence: A.

### 5.3 GitHub Copilot

**Observed loop**：Issue/PR/task → agent context → tools → code changes → build/test/validation → pull request / iteration。

GitHub 当前文档已明确支持 cloud agent、CLI agents、custom agents、subagents、agent skills、hooks、MCP、可配置 development environment 与 secrets。Cloud agent 可以在 GitHub 上启动，也能从 IDE、CLI、API、MCP 等多入口触发。

**Architecture evidence**：模型选择、agent profiles、skills、MCP servers、repository context、configured dev environment 和 GitHub workflow 是一个组合系统。

**Workflow change**：将 issue → code → PR → review/merge 的完整 GitHub workflow agent 化。

Evidence: A.

### 5.4 Cursor

**Observed loop**：Repo search/context → agent reasoning → multi-file edit → terminal execution → test/error observation → fix/iterate。

Cursor Cloud Agents 进一步提供 isolated cloud VMs、dependencies/secrets/network、browser/desktop control、MCP、multi-repo、parallel agents、artifacts，并允许 laptop 关闭后继续运行。

**Architecture evidence**：Agent = instructions + tools + model；local IDE 与 remote cloud execution 共存。

**Workflow change**：AI-native IDE 继续向 remote/background engineering environment 演进。

Evidence: A.

**Corporate status note**：2026-08 Cursor/Anysphere 的所有权状态发生重大变化：官方宣布加入 SpaceX，Reuters 在 2026-08-29 对交易及后续 model-provider 变化进行了独立报道。Phase 3 应把“公司控制权变化”与“产品能力变化”分开分析。

### 5.5 Devin / Devin Desktop

**Observed loop**：task → agent session → planning/delegation → IDE + tools → local/cloud execution → CI/wait → review → repair → PR/artifact。

Devin Desktop 当前定位为本地与云 agent fleet 的 command center，可 plan/delegate/review/ship；页面明确写明它是 Windsurf 的新名称。

**Architecture evidence**：local IDE + cloud agents + fleet/session orchestration + agent control surface。

**Workflow change**：把“一个开发者手工操作一套 IDE”变成“人管理多条 agent workstreams”。

Market numbers on the Devin page are vendor claims.

Evidence: A/B.

### 5.6 Google Antigravity

**Observed loop**：task → planning/reasoning → browser/Chrome and coding tools → parallel/background agents → artifacts → verification/iteration。

Google 在 I/O 2026 将 Antigravity 2.0 明确为 standalone desktop，并以 Antigravity CLI 调用同一类 agent ecosystem；文档支持 subagents、MCP、skills、background agent 管理等。

**Architecture evidence**：desktop command center + CLI + agent runtime/SDK + tools + MCP/skills。

**Workflow change**：从单 IDE 会话向 agent command center + parallel asynchronous work。

**Boundary evidence**：Google Developers Blog 2026-05-19 明确讨论 Gemini CLI 向 Antigravity CLI 的迁移：Gemini CLI 的用户社区、Stars、contributors 等资产被带入新的产品架构。因此 Gemini CLI 不应继续作为与 Antigravity 完全平行的独立市场产品计数。

Evidence: A.

### 5.7 Kiro

**Observed loop**：requirements → design → tasks/spec → implementation → validation → iteration。

Kiro 的核心差异不是“另一个 AI IDE”，而是 **spec-driven development**：将自然语言需求结构化成 requirements/design/tasks，并支持自动执行、hooks、MCP、skills、custom agents、subagents。

**Architecture evidence**：IDE + CLI + web/mobile surfaces sharing agent/harness; hooks and spec artifacts become workflow primitives。

**Workflow change**：将“写 prompt”向“specification as executable development plan”推进。

Evidence: A.

### 5.8 Replit Agent

**Observed loop**：idea → app plan → code generation/editing → environment provisioning → run/preview → tests / functional checks → iterative repair → deployable artifact。

Replit Agent 4 的一个关键研究信号是，它不要求用户从已有 repo、tests、framework 开始。Replit 的公开 evaluation 也强调：真实用户的目标常常是“一个能工作的产品”，因此单纯 SWE-bench 不足以覆盖这一类 workflow。

**Architecture evidence**：browser/cloud-native environment + agent + app runtime + deployment workflow。

**Workflow change**：从 repo-centric SWE 向 idea-to-production app creation。

Evidence: A/B.

### 5.9 OpenCode

**Observed loop**：Explore/read context → Plan or Build agent → tool execution → test/iteration。

OpenCode 的公开 docs 定义了 Build / Plan 两个 primary agents，以及 General / Explore 等 subagents；skills 可按项目/用户级 `SKILL.md` 按需加载；支持 75+ LLM providers 并可运行本地模型。

**Architecture evidence**：open agent harness + pluggable providers + native skills + primary/subagent model。

**Workflow change**：把 agent harness 本身开源化、provider-agnostic 化，成为一个可组合的 terminal-native execution layer。

Evidence: A.

### 5.10 OpenHands

**Observed loop**：task → Plan/Code mode → agent environment → shell/editor/tools → tests → iteration → artifact / PR；支持 parallel agent canvas、scheduled/event-driven automation 与 managed sandbox。

OpenHands 的产品路线已从单 agent coding 扩展到 Cloud Workspace、enterprise control plane、parallel agent execution 和 SDK。

**Architecture evidence**：agent server / orchestration + local/VM/cloud runtime + sandboxed workspaces。

**Workflow change**：把“open-source coding agent”推进为可自托管、可扩展、可批量运行的 agent platform。

Evidence: A.

### 5.11 Cline

**Observed loop**：repo exploration → planning/reasoning → tool use → edits → command execution → verification；headless CLI 可把同一能力带到 automation / CI 场景。

Cline 的公开 repo 将产品描述为 SDK + IDE extension + CLI assistant；支持 rules/skills，且具备 model-agnostic design。它的 subagent 机制又明显呈现“只读 research / explore”这类能力拆分。

**Architecture evidence**：open agent + IDE/CLI surfaces + scoped subagents + skills/rules。

**Workflow change**：从 IDE extension 向可编程、可 headless 的 coding agent 迁移。

Evidence: A.

### 5.12 Qoder

**Observed loop**：continuous planning → repository/context gathering → execution → verification → self-correction；Cloud Agents 再加 browser use、batch/scheduling、persistent memory、skills/MCP mounting。

Qoder 2026-08 的产品材料把“持续 planning/execution/verification/self-correction”作为 agentic platform 的核心。Cloud Agents release notes 又显示从 2026-07 到 2026-08 持续加入 browser use、GitHub repo mount、skills、batch/schedule、memory 和 observability。

**Architecture evidence**：IDE/CLI + Cloud Agent + isolated cloud sessions + skills/MCP/memory。

**Workflow change**：从 AI IDE 向 agent platform / cloud execution。

Evidence: A.

### 5.13 TRAE

**Observed loop**：complex task → agent reasoning / coding → multi-agent collaboration → sandbox/tool use → iteration → artifact/workspace。

TRAE SOLO 在 2026-06 演进为 TRAE Work，使产品从单一 coding surface 向更宽的 AI workspace 延伸。当前材料还覆盖 agent skills/rules、sandbox/security、mobile、design mode 等。

**Architecture evidence**：IDE/workspace + agent + multi-agent / skills / sandbox。

**Workflow change**：AI IDE → broader agent workspace。

Evidence: B.

### 5.14 Tencent CodeBuddy

**Observed loop**：interactive task → codebase exploration → worker/child agent delegation → tool use/MCP → shell/run → iteration；Cloud Agent 增加 sandboxed remote execution。

Tencent 2026-08 CLI docs 明确出现 agents、session restore、MCP、daemon、background worker / attach/kill 等 orchestration primitives，说明产品已经超出普通 autocomplete/chat。

**Architecture evidence**：CLI agent + worker/child agents + MCP + sandbox / cloud environment。

**Workflow change**：CLI-first agent + enterprise/cloud execution。

Market evidence remains primarily Chinese/vendor-side; confidence is lower than global survey-covered candidates.

Evidence: B.

### 5.15 JetBrains AI / Junie

**Observed loop**：IDE context → reasoning → edit/run/test/debug → iteration → PR/review；terminal surface 承担更长任务。

JetBrains 2026 年公开材料显示 Junie 已形成较完整的 agent workflow，并与 JetBrains AI 多入口整合；同时支持 Codex、Claude agent 等 ACP-style agents in IDE。

**Architecture evidence**：IDE-native agent + terminal + ACP/provider integration + project context。

**Workflow change**：将已有 enterprise IDE workflow 原生 agent 化，而不是要求用户迁移到新的 editor。

Evidence: A.

### 5.16 Kimi Code

**Observed loop**：repository analysis → planning → file/shell/web tools → subagents → execution → verification/adjustment。

Kimi Code CLI 文档明确描述读取与修改代码、运行 shell、搜索文件/网页、自动 planning/adjustment；ACP 让能力进入 JetBrains、Zed 等 IDE。

**Architecture evidence**：terminal agent + IDE ACP + MCP + skills/subagents。

**Workflow change**：中国 AI lab 从 model product 向 terminal/IDE coding agent stack 延伸。

Evidence: B.

### 5.17 Amazon Q Developer

**Observed loop**：AWS-aware repo task → code / tests / agent execution → enterprise workflow；但当前最重要的新事实是 **coding CLI/IDE surface 正在迁移到 Kiro**。

AWS 官方文档写明：Amazon Q Developer CLI 已 rebrand 为 Kiro；Q IDE extension / CLI upgrade 后变为 Kiro，并且未来更新主要在 Kiro。另有官方文档明确 Amazon Q Developer IDE plugins 将于 2027-04-30 结束支持，并建议迁移至 Kiro。

**Architecture / family finding**：对于 Phase 3，Amazon Q Developer 不应与 Kiro 当成两个完全独立的 modern coding-agent families 进行简单横向比较；更合理的处理是：**Kiro = current product trajectory；Amazon Q Developer = legacy / enterprise continuation / migration signal**。

Evidence: A.

---

## 6. Product Architecture Evidence Matrix

| Candidate | Underlying Model Layer | Agent / Harness | Context / Memory / Rules | Tools / MCP / Skills | Runtime / Sandbox / Cloud | Product UX / Surface |
|---|---|---|---|---|---|---|
| Claude Code | Model-agnostic across supported Anthropic models; model layer separated | CLI agent + subagents | memory, rules, hooks, worktrees | shell, file, MCP, skills | local execution; isolation/worktrees | terminal + IDE integration |
| Codex | OpenAI model family + selectable model strategy | Codex App/CLI/cloud agent system | repo context, instructions, skills | tools, MCP, automations | cloud/local execution | App + CLI + IDE + Cloud |
| GitHub Copilot | Multiple model options | cloud/IDE/CLI agents + custom agents | agent profiles, skills, repo context | tools, MCP, hooks | configured cloud dev env | GitHub + IDE + CLI + API |
| Cursor | Multi-model product strategy | Cursor Agent / Cloud Agents | rules, codebase context | terminal, browser/desktop, MCP | isolated remote VMs | AI-native IDE + CLI + Cloud |
| Devin | Model strategy largely abstracted | Devin agents + fleet/desktop orchestration | session context / workspaces | IDE/tool integrations | local + cloud | Desktop command center |
| Antigravity | Gemini-centered Google agent ecosystem | Antigravity agent runtime + SDK | workflows / skills / artifacts | browser/Chrome, MCP, subagents | desktop/CLI/cloud-oriented | Desktop command center + CLI |
| Kiro | AWS-selected coding models | spec agent / shared harness | steering, specs, hooks | MCP, skills, custom agents | IDE/CLI/web runtime | IDE + CLI + web/mobile |
| Replit Agent | Multi-model / vendor abstraction | Replit Agent 4 | project/app context | browser/app tools | managed app runtime / cloud | web-native product builder |
| OpenCode | 75+ providers + local models | open harness, Build/Plan + subagents | config + skills | native tools + provider ecosystem | local-first; extensible | CLI + Desktop |
| OpenHands | Model-agnostic | agent server + orchestration | PLAN.md, task state | shell/editor/web tools | local / VM / cloud / enterprise | CLI + Cloud + SDK |
| Cline | Model-agnostic | autonomous agent + subagents | rules, skills | IDE tools, CLI, MCP | local/headless | IDE + CLI + SDK |
| Qoder | Multiple Alibaba/global model options | agentic IDE + Cloud Agents | skills, memory, configuration | MCP, browser, tools | cloud sessions / containers | IDE + CLI + Cloud |
| TRAE | Vendor-selected model stack | IDE/SOLO/Work agent layer | rules/skills | tools, MCP, sandbox | local + cloud/workspace | IDE + Web/Desktop/Mobile |
| CodeBuddy | Tencent model ecosystem | CLI + worker/child agent model | sessions / agent config | MCP + workers | sandbox / CloudAgent | CLI + Web/Cloud |
| JetBrains AI / Junie | Multiple agent/model integrations | Junie + ACP-style agent layer | IDE/project context | terminal, tools, MCP-style integrations | IDE/terminal | JetBrains IDEs |
| Kimi Code | Kimi model family | terminal agent + ACP | skills, hooks, subagents | shell, web, MCP | local terminal execution | CLI + IDE integrations |
| Amazon Q Developer | AWS/Q model ecosystem | Q agentic CLI/IDE; migrating to Kiro | AWS-specific config | enterprise tools | AWS-integrated runtime | IDE + CLI; transition to Kiro |

**Architecture conclusion:** 当前竞争重点已明显从“哪个模型生成代码最好”转向 **Model + Harness + Context + Tools + Runtime + Workflow Integration** 的系统组合。模型 benchmark 不能直接替代产品 benchmark。

---

## 7. Workflow Evidence

| Candidate | Main workflow being changed | Evidence-backed interpretation |
|---|---|---|
| Claude Code | Terminal/repository workflow | Human stays in terminal; agent owns multi-step repo work |
| Codex | Task delegation / background work | Work is packaged as tasks that can run in parallel and continue independently |
| GitHub Copilot | Issue → code → PR → review | Agent enters the native GitHub lifecycle |
| Cursor | IDE → background cloud execution | IDE becomes a launch/control surface for remote agents |
| Devin | Individual developer → agent fleet | Human coordinates multiple agents rather than one interactive session |
| Antigravity | Single session → command center | Parallel agents, artifacts and async work become first-class |
| Kiro | Prompt → specification → execution | Specs become intermediate executable development artifacts |
| Replit Agent | Idea → production app | Repo-first assumptions are weakened; product artifact becomes the target |
| OpenCode | CLI → composable open harness | Agent itself becomes infrastructure users can configure/extend |
| OpenHands | One agent → agent platform | Parallel, cloud, scheduled and enterprise execution are built into the system |
| Cline | IDE helper → programmable/headless agent | Same agent capability becomes scriptable and automatable |
| Qoder | IDE → cloud agent platform | Cloud sessions, batch, scheduling and memory broaden task scope |
| TRAE | AI IDE → workspace | Coding is one part of a broader agent workspace |
| CodeBuddy | Interactive CLI → worker orchestration | Child/background workers make concurrency part of the CLI workflow |
| Junie | IDE workflow → agent-native IDE | Existing JetBrains users get agentic task execution without switching editor |
| Kimi Code | Model → terminal agent product | AI lab product becomes an actual software-engineering surface |
| Amazon Q → Kiro | AWS assistant → dedicated agentic IDE/CLI | Coding trajectory is consolidated under Kiro |

### Workflow taxonomy

The current population is better understood as a set of workflow families than as a single IDE category:

1. **Terminal-native SWE agents** — Claude Code, Codex CLI, OpenCode, Cline, Kimi Code.
2. **AI-native IDE agents** — Cursor, Qoder, TRAE, Junie, Kiro.
3. **Cloud/background SWE agents** — Codex Cloud, Copilot cloud agent, Devin, OpenHands, Qoder Cloud.
4. **Desktop agent command centers** — Devin Desktop, Antigravity, Codex App.
5. **Idea-to-production builders** — Replit Agent and adjacent Bolt/v0/Lovable.
6. **Enterprise workflow agents** — Copilot, Kiro, Qoder CN, CodeBuddy, Junie, Factory.

---

## 8. Ecosystem Evidence

### Open-source ecosystem signals

| Candidate | Current public ecosystem signal | Interpretation |
|---|---|---|
| OpenCode | ~194K GitHub stars, ~24.8K forks | Very strong OSS ecosystem signal; also appears in 7% independent survey adoption |
| Cline | ~63K stars, ~6.7K forks | Strong OSS adoption / developer interest |
| OpenHands | Large OSS repo and Cloud/Enterprise ecosystem | Strong architecture/ecosystem significance |
| Qwen Code | OSS model-native CLI ecosystem | Strategic ecosystem value, market denominator unknown |

GitHub stars/forks are **ecosystem signals, not user counts**.

### Enterprise/platform distribution signals

- GitHub Copilot inherits the full GitHub distribution surface; current GitHub newsroom reports 4.7M paid Copilot subscribers and 77K+ organizations, on top of a very large overall GitHub developer ecosystem.
- AWS provides Kiro a direct enterprise cloud distribution channel and is actively migrating Q Developer coding surfaces into Kiro.
- JetBrains brings Junie into an installed IDE base and explicitly integrates third-party agents through its IDE surface.
- Replit combines Agent with a large product-building platform and cloud runtime, meaning the agent is directly tied to deployment.
- Factory, Devin and OpenHands are building stronger “agent fleet / control plane / cloud execution” concepts than ordinary autocomplete products.

---

## 9. Momentum Evidence

| Candidate | Recent momentum evidence | Date | Evidence grade |
|---|---|---|---|
| Claude Code | Weekly active users and revenue growth were already accelerating in Anthropic disclosures; current independent survey remains strongest market signal | 2025–2026 | A/B |
| Codex | >5M WAU and >6x growth since desktop launch | 2026-06-02 | A |
| GitHub Copilot | Agent surface expanding across cloud, CLI, IDE, API, skills, custom agents | 2026 | A |
| Cursor | SpaceX acquisition / ownership transition; new model/provider strategy implications | Aug 2026 | A/B |
| Devin | Desktop/fleet positioning and continued enterprise packaging | 2026 | B |
| Antigravity | Antigravity 2.0 + CLI transition from Gemini CLI | May–Jun 2026 | A |
| Kiro | Rapid expansion of specs, hooks, CLI, skills, agents and shared harness | 2026 | A |
| Replit Agent | Agent 4 + evaluation at scale + platform growth | Mar–Jun 2026 | A/B |
| OpenCode | Large OSS repo growth + 7% independent survey adoption + Desktop beta | 2026 | A |
| OpenHands | Cloud Workspace, Agent Canvas, enterprise control plane, always-on/automations | 2026 | A/B |
| Cline | SDK/CLI/headless expansion and active release cadence | 2026 | A |
| Qoder | 6M user claim + rapid Cloud Agents release cadence including browser, batch, schedule, memory | Aug 2026 | A/B |
| TRAE | SOLO → TRAE Work and broader workspace positioning | Jun 2026 | B |
| CodeBuddy | CLI worker/daemon/sandbox/cloud-agent capabilities continuing to expand | Aug 2026 | B |
| JetBrains AI / Junie | Junie user milestone + integration of third-party agents in IDE | 2025–2026 | A/B |
| Kimi Code | Rapid CLI/IDE/MCP/skills/subagent evolution and Moonshot company momentum | 2026 | B |
| Amazon Q Developer | Strongest “momentum” signal is migration into Kiro, not independent Q expansion | 2026 | A |

---

## 10. Public Benchmark Evidence

### 10.1 Benchmark policy

Only existing public benchmarks are used. No benchmark was designed or run for this Case.

### 10.2 SWE-bench / SWE-rebench

SWE-bench evaluates software-engineering agents on real repository issues. SWE-rebench extends the public evaluation landscape and provides current 2026 comparisons under explicit methodology.

A representative 2026 SWE-rebench run reported approximately:

| System | Resolved | Pass@5 | Cost/problem | Notes |
|---|---:|---:|---:|---|
| Codex Agent | 58.0% | 73.0% | ~$1.59 | Third-party benchmark; configuration/model/version specific |
| Junie Agent | 61.8% | 73.9% | ~$0.81 | Third-party benchmark; configuration/model/version specific |

These numbers show that agent-level performance can be measured independently of raw model benchmark. They do **not** establish a global product ranking because:

- system configurations differ;
- model versions differ;
- environment and tool access differ;
- cost accounting differs;
- benchmark coverage is issue-centric rather than representative of all software work.

### 10.3 Terminal-Bench 2.0

Terminal-Bench provides another useful view of terminal-based agent execution. Public 2026 results include strong agent performance by Junie and other terminal agents, but again the metric represents a benchmark environment rather than complete software-engineering capability.

### 10.4 Benchmark interpretation rule

`Benchmark result → supporting evidence`, never:

`Benchmark result → final Top 10`

The relevant question is not only “can it solve SWE-bench?” but also “can it reliably gather context, use tools, run software, verify results, repair failures, manage long-running tasks, and fit into a real software workflow?”

---

## 11. Evidence Matrix

Qualitative labels below are **pre-ranking research states**, not final scores.

| Candidate | Market Adoption | Product / Agent Capability | Workflow Innovation | Ecosystem / Strategic Importance | Momentum | Confidence |
|---|---|---|---|---|---|---|
| Claude Code | High | High | High | High | High | High |
| Codex | High | High | High | High | High | High |
| GitHub Copilot | High | High | High | Very High | High | High |
| Cursor | High | High | High | High | High | High |
| Devin | Medium–High | High | High | High | High | Medium–High |
| Google Antigravity | Medium–High | High | High | Very High | High | High |
| Kiro | Medium / Unknown | High | High | Very High | High | Medium–High |
| Replit Agent | Medium–High | High | Very High (idea→app) | High | High | Medium–High |
| OpenCode | Medium–High | High | High | High | High | High |
| OpenHands | Medium | High | High | High | High | Medium–High |
| Cline | Medium | High | High | High | High | Medium–High |
| Qoder | Medium–High | High | High | High | High | Medium |
| TRAE | Medium / Unknown | High | High | High | High | Medium |
| Tencent CodeBuddy | Medium / Unknown | High | High | High in China | High | Medium |
| JetBrains AI / Junie | Medium–High | High | Medium–High | Very High | High | High |
| Kimi Code | Medium / Unknown | High | High | High in China | High | Medium |
| Amazon Q Developer | Transitional | Medium–High | Medium | Very High through AWS, but migration | Migration-driven | High on status; low as standalone future candidate |

**Important:** “High” here means **evidence-supported importance/capability signal**, not “best”. This matrix deliberately contains no weighted total and no Top 10 order.

---

## 12. Candidate-by-Candidate Evidence Summary

### 12.1 Core — evidence coverage status

**17 / 17 Core Candidates have effective Phase 2 evidence.**

All 17 have at least one strong official/independent product or market source sufficient to support a Phase 3 research dossier. The depth is not identical: global products with independent survey coverage have stronger Market Adoption evidence than Chinese products without public comparable denominators.

| Candidate | Market | Capability | Architecture | Workflow | Ecosystem | Momentum | Overall evidence grade |
|---|---|---|---|---|---|---|---|
| Claude Code | Strong | Strong | Strong | Strong | Strong | Strong | A |
| Codex | Strong | Strong | Strong | Strong | Strong | Strong | A |
| GitHub Copilot | Strong | Strong | Strong | Strong | Very strong | Strong | A |
| Cursor | Strong | Strong | Strong | Strong | Strong | Strong | A |
| Devin | Good | Strong | Strong | Strong | Strong | Good | B+/A- |
| Antigravity | Good | Strong | Strong | Strong | Very strong | Strong | A |
| Kiro | Limited market denominator | Strong | Strong | Strong | Very strong | Strong | A/B |
| Replit Agent | Good platform-level | Strong | Strong | Very strong | Strong | Strong | A/B |
| OpenCode | Strong OSS + survey | Strong | Very strong | Strong | Very strong | Strong | A |
| OpenHands | Good | Strong | Very strong | Strong | Very strong | Strong | A/B |
| Cline | Good OSS | Strong | Strong | Strong | Very strong | Strong | A/B |
| Qoder | Good vendor evidence | Strong | Strong | Strong | Strong | Very strong | A/B |
| TRAE | Limited independent market data | Strong | Good | Strong | Strong | Strong | B |
| Tencent CodeBuddy | Limited independent market data | Strong | Good | Strong | Strong in China | Strong | B |
| JetBrains AI / Junie | Good | Strong | Strong | Strong | Very strong | Strong | A |
| Kimi Code | Limited independent market data | Strong | Good/Strong | Strong | Strong in China | Strong | B |
| Amazon Q Developer | Historical/legacy | Good | Strong | Medium | Very strong via AWS | Migration signal | A for status, not standalone product future |

---

## 13. Boundary / Classification Findings

### 13.1 Google Antigravity / Jules / Gemini CLI

**Finding:** Gemini CLI should no longer be treated as a clean independent peer to Antigravity. Google explicitly described the transition of Gemini CLI to Antigravity CLI in 2026. The same broad agent ecosystem is being consolidated under Antigravity.

**Jules remains distinct for now.** Jules is a cloud/GitHub async coding-agent surface and should be treated as a separate Google product surface unless future evidence shows formal family consolidation. In Phase 3, avoid double-counting Google’s underlying agent ecosystem as if every surface were a separate company-level product.

**Classification action:** retain Antigravity as the primary Google Core candidate; track Jules as a secondary/adjacent product surface unless the Phase 3 unit definition requires a separate family.

### 13.2 Devin / Windsurf

**Finding:** Cognition currently says “Devin Desktop is the new name for Windsurf.”

**Classification action:** Phase 1’s combined Devin/Cognition family remains correct.

### 13.3 Qoder / Qoder CN / Tongyi Lingma

**Finding:** Qoder CN is the continuation/renaming path of Tongyi Lingma for the China market, and Qoder/Qoder CN share the same broader product-family identity while preserving China-specific deployment/compliance characteristics.

**Classification action:** Phase 1’s family merge remains correct.

### 13.4 Amazon Q Developer / Kiro

**Finding:** This is the clearest Phase 2 classification correction.

AWS officially states that Amazon Q Developer CLI has been rebranded to Kiro; Amazon Q IDE extensions and CLI can be upgraded to Kiro, and future updates are being delivered through Kiro. AWS also states Amazon Q Developer IDE plugin support will end on 2027-04-30 and recommends Kiro.

**Phase 1 status:** having both Kiro and Amazon Q Developer as independent Core candidates was understandable at the 2026-08-30 snapshot, but new official evidence now shows a **product-family convergence / migration**.

**Phase 3 handling:** treat **Kiro as the current product trajectory** and Amazon Q Developer as a **legacy / migration lineage**, not as a fully independent modern product family for ranking purposes.

This is a versioned correction, not a silent deletion.

### 13.5 Cursor corporate status

**Finding:** Cursor’s corporate ownership changed materially in August 2026 with SpaceX involvement/acquisition.

**Implication:** company ownership should be captured as a strategic-context field, not mixed into product capability. Current Cursor remains a product-family candidate; the parent-company relation is a Phase 2 market/strategy change.

### 13.6 Replit / Bolt / v0 / Lovable

**Finding:** These products are increasingly agentic and overlap strongly with “idea → application → deployment”. Replit is already Core in this research, while Bolt, v0 and Lovable are adjacent rather than pure repo-centric SWE agents.

Evidence from Vercel and Lovable shows that v0/Lovable are no longer safely described as static generators or pure no-code tools; both are moving toward coding-agent workflows. Replit has the clearest end-to-end product-building evidence in the current Core set.

**Phase 3 rule:** compare these candidates using **workflow coverage** rather than forcing them into an IDE-centric definition. Do not automatically exclude them merely because they begin from an idea rather than an existing repository.

No automatic promotion to Core is made in Phase 2 because the existing universe already includes Replit and the marginal research value of adding every app-builder is not yet established.

### 13.7 CodeRabbit / Qodo / Greptile / Cubic

**Finding:** these products materially automate code review, repo intelligence, test/quality or debugging workflows, but their primary job is not consistently the full:

`Task → Context → Plan → Edit → Execute → Verify → Repair → Artifact`

loop.

**Classification action:** keep as adjacent / boundary products, not core general-purpose Coding Agents, unless Phase 3 evidence shows that one has expanded into end-to-end SWE execution.

### 13.8 Factory / Amp / Augment / Poolside

**Factory** has the strongest current promotion signal among these: Factory reported a $150M Series C at a $1.5B valuation and claimed Droids were used daily by hundreds of thousands of developers across named enterprises.

**Amp / Augment / Poolside** remain strategically important, but current public adoption denominators are insufficient for a confident Core promotion in this Phase 2 pass.

**Phase 3 action:** Factory should receive a dedicated comparison against the current Core group; Amp/Augment/Poolside remain high-priority Secondary candidates until stronger comparable evidence appears.

---

## 14. Evidence Gaps

### Market gaps

1. No uniform global market share denominator exists across all Core candidates.
2. Chinese product adoption data are materially less standardized and less independent.
3. Replit platform users cannot be equated with Replit Agent users.
4. Qoder, Devin and several Chinese products rely heavily on vendor-reported user/business counts.
5. Enterprise customer counts often lack active-user or usage-intensity definitions.

### Capability gaps

1. Public docs show intended capability, not necessarily reliability.
2. Product surfaces frequently support multiple models, making “agent capability” model-dependent.
3. Long-running reliability, failure recovery and verification quality are not uniformly disclosed.
4. Memory quality is especially difficult to compare from product documentation alone.
5. “Parallel agents” can mean anything from UI-level concurrency to truly independent execution environments; Phase 3 should distinguish these.

### Benchmark gaps

1. Public coding benchmarks do not cover all workflow types.
2. SWE-bench-style tasks under-represent idea-to-production builders.
3. Terminal benchmarks under-represent team collaboration, review and deployment workflows.
4. Cost metrics are not directly comparable across vendor configurations.

---

## 15. Key Observations

### 15.1 The market is becoming a multi-surface agent market

The major product surfaces are now converging around a common agent architecture while diverging in UX: terminal, IDE, desktop command center, cloud/background and browser-native app builder.

### 15.2 The decisive product layer is the harness/runtime system

Across the market, durable differentiation increasingly sits in:

`Model → Harness → Context → Tools → Runtime/Sandbox → Memory/Rules/Skills → Workflow`

not only in raw model intelligence.

### 15.3 Workflow innovation is increasingly about delegation

The strongest product shifts are no longer just “AI edits code faster”. They are:

- delegate a task;
- let agents run in parallel;
- move execution to a cloud sandbox;
- preserve state across long-running sessions;
- use subagents for specialized work;
- turn specs/skills/rules into reusable execution primitives;
- return artifacts/PRs rather than snippets.

### 15.4 OSS is functioning as a harness laboratory

OpenCode, OpenHands and Cline provide evidence that open-source value is not limited to code ownership; they are experiments in provider abstraction, tool composition, skills, subagents, local/cloud runtime and agent control.

### 15.5 China is not simply cloning one Western product shape

Chinese candidates span IDE-native, terminal-native, cloud-agent and enterprise-first routes. The most important unresolved question is whether Chinese enterprise deployment and domestic model integration will create a distinct route or converge on the same multi-surface agent architecture.

### 15.6 Product-family consolidation itself is a market signal

Three important consolidation patterns are visible:

- Gemini CLI → Antigravity CLI;
- Amazon Q Developer coding surface → Kiro;
- Windsurf → Devin Desktop.

The market is increasingly organized around **agent platforms / product families**, not isolated named clients.

---

## 16. Open Questions for Phase 3

1. After deduplication, which product families remain genuinely distinct enough to compare?
2. Should Replit/Bolt/v0/Lovable be evaluated in the same ranking population, or as an adjacent “idea-to-product” category with a bridge into the main ranking?
3. Is Factory’s current enterprise momentum enough to elevate it from Secondary into the final research population?
4. Can a common Market Adoption normalization be built without falsely equating survey adoption, WAU, paid subscribers, and GitHub stars?
5. Should capability be assessed as a matrix rather than a scalar score, especially for terminal vs IDE vs cloud agent products?
6. How should Phase 3 separate “workflow novelty” from “execution reliability”?
7. Can an evidence-weighted score handle products whose market evidence is vendor-only?
8. How should corporate ownership transitions (Cursor / SpaceX) affect ecosystem/strategic importance without contaminating product capability scoring?
9. Should Google’s Antigravity + Jules be modeled as one family with multiple surfaces, or as two products sharing a platform?
10. How should enterprise agent platforms such as Factory, Kiro, CodeBuddy and OpenHands be compared with consumer-first IDE agents?

---

## 17. Phase 2 Coverage Review

### Global coverage

- AI-native IDE: covered
- CLI Coding Agent: covered
- Cloud Coding Agent: covered
- Desktop Agent: covered
- Autonomous SWE Agent: covered
- Open-source Agent: covered
- Big Tech agents: covered
- AI lab agents: covered
- Developer-tool companies: covered
- Enterprise coding agents: covered
- App-builder / vibe-coding boundary: covered at targeted depth

### China coverage

- AI-native IDE: Qoder, TRAE, Comate
- CLI: Kimi Code, Qwen Code, Reasonix
- Cloud / enterprise: CodeBuddy, Qoder CN, Comate
- Major Chinese AI companies: Alibaba, ByteDance, Tencent, Baidu, Moonshot, DeepSeek
- OSS route: Qwen Code and other open agent projects

No major missing global surface was identified that would justify rebuilding the Candidate Universe in Phase 2.

---

## 18. Sources

### Tier 1 / Primary

**S01 — JetBrains, AI Coding Agents: Adoption Trends, Aug 2026**  
https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/

**S02 — OpenAI, Codex is becoming a productivity tool for everyone, 2026-06-02**  
https://openai.com/index/codex-for-knowledge-work/

**S03 — GitHub Newsroom / Copilot current market metrics**  
https://github.com/newsroom

**S04 — GitHub Docs, Copilot cloud agent / custom agents / skills / MCP**  
https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent  
https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-custom-agents-in-your-ide  
https://docs.github.com/en/copilot/concepts/agents/about-agent-skills

**S05 — Cursor, joining SpaceX, Aug 2026**  
https://cursor.com/blog/joining-spacex

**S06 — Cursor Agent / Cloud Agents documentation**  
https://cursor.com/docs/agent/overview

**S07 — Devin Desktop**  
https://devin.ai/desktop

**S08 — Google Antigravity at I/O 2026**  
https://www.antigravity.google/blog/google-io-2026

**S09 — Google Developers Blog, Transitioning Gemini CLI to Antigravity CLI, 2026-05-19**  
https://developers.googleblog.com/

**S10 — AWS, Upgrade to Kiro**  
https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/upgrade-to-kiro.html

**S11 — AWS, Amazon Q Developer IDE plugins end of support**  
https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html

**S12 — Replit product / evaluation materials**  
https://replit.com/ai  
https://replit.com/blog/

**S13 — OpenCode GitHub repository**  
https://github.com/anomalyco/opencode

**S14 — OpenCode agents documentation**  
https://opencode.ai/docs/agents/

**S15 — OpenCode skills documentation**  
https://opencode.ai/docs/skills

**S16 — OpenCode providers documentation**  
https://opencode.ai/docs/providers/

**S17 — OpenHands Cloud Workspace / product docs**  
https://docs.openhands.dev/sdk/guides/agent-server/cloud-workspace

**S18 — Cline GitHub repository**  
https://github.com/cline/cline

**S19 — Qoder changelog / Cloud Agents**  
https://qoder.com/changelog  
https://docs.qoder.com/release-notes/cloud-agents

**S20 — Qoder Skills documentation**  
https://docs.qoder.com/extensions/skills

**S21 — TRAE Work**  
https://www.trae.ai/blog/trae_work_0609

**S22 — Tencent CodeBuddy CLI documentation, updated 2026-08-26**  
https://cloud.tencent.com/document/product/1831/137026

**S23 — JetBrains Annual Highlights 2026**  
https://www.jetbrains.com/lp/annualreport-2026/

**S24 — Kimi Code CLI getting started**  
https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html

**S25 — Factory Series C, 2026-04-16**  
https://factory.ai/news/series-c

**S26 — Lovable product / agent ecosystem**  
https://lovable.dev/blog

### Tier 2 / Independent

**S27 — Reuters, Cursor / SpaceX transaction reporting, 2026-08-29**  
Reuters reporting referenced in the research notes; used as independent corroboration for the August 2026 ownership transition and related model-access implications.

**S28 — SWE-rebench current 2026 benchmark**  
https://swe-rebench.com/

**S29 — SWE-bench official benchmark**  
https://www.swebench.com/

**S30 — JetBrains Jan/Apr 2026 AI developer ecosystem surveys**  
JetBrains Research / Developer Ecosystem reports, used only as historical trend context.

### Tier 3 / Discovery / Ecosystem

**S31 — GitHub ecosystem signals**  
GitHub repositories for OpenCode, OpenHands, Cline, Qwen Code and related projects.

**S32 — Community / third-party coding-agent ecosystem tracking**  
Used only for discovery, boundary identification and user-experience signals.

---

## 19. Phase 2 Conclusion

### Scope status

**Completed:** Market & Evidence Collection.

**Not completed:** Final Ranking, Top 10 Selection, Phase 3 deep product research.

### Core evidence status

- 17 / 17 Core candidates have effective evidence coverage.
- Global market evidence is strongest for Claude Code, Codex, GitHub Copilot and Cursor because they combine independent survey signals with substantial vendor/platform evidence.
- OpenCode has unusually strong independent + OSS ecosystem evidence relative to its company size.
- Several Chinese candidates have strong product/architecture evidence but insufficient comparable independent market denominators.
- Amazon Q Developer is now best treated as a migration lineage into Kiro, not as an independent modern coding-agent family.

### Research posture

The evidence base is intentionally asymmetric where the public market is asymmetric. Unknowns are preserved rather than fabricated, and vendor claims remain labeled as vendor claims.

**No final Top 10 is produced in this document.**
