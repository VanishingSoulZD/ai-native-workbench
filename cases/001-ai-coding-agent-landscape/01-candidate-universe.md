# Case 001 — 2026 AI Coding Agent Landscape

## Phase 1 — Candidate Universe Construction

> Research snapshot: 2026-08-30
>
> Research cutoff: August 2026
>
> Status: Phase 1 completed
>
> Research unit: AI Coding Agent Product / Product Family

---

## 1. Phase 1 Objective

本阶段只完成 **Candidate Universe Construction**，不进行最终 TOP10 排名，也不执行 Phase 2 的系统化 Market & Evidence Collection。

本阶段的目标是：

1. 建立尽可能完整的全球 AI Coding Agent 候选池；
2. 覆盖 Market Leaders、Technology / Product Leaders、Emerging Candidates，以及中国市场的重要产品；
3. 按 **Company → Product Family → Product Surface → Agent Capability** 去重；
4. 明确区分市场采用度、技术/产品能力、工作流创新、生态和发展势能；
5. 对重要排除项记录可审计的原因；
6. 为 Phase 2 的统一证据采集与后续 Ranking 提供稳定研究人口。

本阶段遵循 Research Charter：研究重点不是功能数量，而是哪些产品正在重新定义 Software Engineering Workflow；Market Adoption、Product Capability 与 Technology Leadership 不能混为一谈。见 `00-research-charter.md`。

---

## 2. Candidate Universe Methodology

### 2.1 Scope rule

纳入对象必须基本满足以下条件：

- 面向 Software Development / Coding / Software Engineering；
- 能接受相对高层的软件开发目标；
- 能执行多步骤任务，而非只有一次性生成或补全；
- 具备一定的代码修改、工具调用、执行、测试/验证或迭代修复能力；
- 产品形态可为 CLI、IDE、Desktop 或 Cloud；
- Plugin-only 产品不作为独立候选。

### 2.2 Agentic maturity rule

候选池重点覆盖：

`Agentic Coding Tool → Software Engineering Agent → Autonomous Software Engineering Agent`

传统 Coding Assistant 只有在已经显著向 Agentic Workflow 演进时才保留。

### 2.3 Product-family deduplication

同一家公司如果同时拥有 CLI、IDE、Desktop、Cloud、Plugin 等入口，不拆成多个候选。

典型处理：

- **Qoder / Qoder CN / 原 Tongyi Lingma** → 一个 Qoder Product Family；
- **Devin / Devin Desktop / Windsurf legacy** → 一个 Devin/Cognition Product Family；
- **TRAE IDE / TraeCode / SOLO / TRAE Work** → 一个 TRAE Product Family；
- **GitHub Copilot / Copilot CLI / Copilot coding agent** → 一个 GitHub Copilot Product Family；
- **Cursor IDE / Cursor CLI / Cloud Agents** → 一个 Cursor Product Family。

### 2.4 Evidence strategy

本阶段采用：

`Primary Sources → High-quality Independent Sources → Community / Discovery Sources`

其中：

- **Tier 1**：官方产品页、官方文档、官方博客、官方 GitHub、官方公告、公司资料；
- **Tier 2**：JetBrains、Stack Overflow、GitHub ecosystem、公开开发者调查、公开 benchmark；
- **Tier 3**：Reddit、Hacker News、GitHub Issues/Discussions、社区列表等；
- **Tier 4**：个人博客和单次体验文章。

Candidate Universe 阶段允许使用 Discovery Sources 发现产品，但不会把社区榜单自动当作市场事实。Phase 2 将进一步对 Core / Secondary 候选进行一手来源核验。

### 2.5 Market evidence interpretation

2026 年 8 月的 JetBrains 开发者调查是本轮候选池最重要的独立市场信号之一：May–July 2026 期间，全球专业开发者工作场景中的 Claude Code 使用率约 39%，Codex 约 16%，GitHub Copilot 约 21%，Cursor 约 12%，OpenCode 约 7%，Google Antigravity 约 6%；JetBrains AI / Junie 合计约 9%。这些数据是调查口径，不应直接解释成全球所有开发者的绝对市场份额。该调查同时显示 2026 年上半年 Coding Agent 的采用速度明显加快。[^market1]

JetBrains 2026 年 4 月的上一期调查显示，2026 年 1 月约 90% 的开发者经常使用至少一种 AI 工具进行 coding/development，GitHub Copilot 工作场景采用率约 29%，Cursor 与 Claude Code 各约 18%。这支持“市场快速迁移到 Agentic Coding 工具”的趋势判断，但仍不能用于精确比较所有产品的全球市场份额。[^market2]

Anthropic 对约 235,000 名 Claude Code 用户、约 400,000 个交互 session 的研究则提供了一个重要的产品使用结构信号：用户平均每周投入 Claude Code 约 20 小时；GitHub 上使用 coding agents 的项目明显增加；任务逐渐从“修代码”扩展到运行软件、数据分析和其他更高层软件工作。该数据是 Anthropic 自有样本，不代表整个市场，但对“Agent 正从代码编辑器走向 Software Engineering Workflow”这一趋势具有较高解释价值。[^market3]

---

## 3. Candidate Classification

### Core Candidate

满足以下至少两项：

- 已有明显市场采用度或行业品牌影响力；
- 在 Agentic Coding / SWE Workflow 上具有明显产品代表性；
- 具有独立且成熟的产品家族或重要生态；
- 对后续 Top 10 判断具有较高信息价值。

**Core ≠ Top 10。** Core 表示 Phase 2 优先研究候选。

### Secondary Candidate

具有明显产品价值、生态意义或技术意义，但当前缺少足够市场证据、规模有限、与 Core 的路线高度重叠，或产品定位仍处于发展阶段。

### Watchlist

快速变化、刚进入市场、信息不足、范围边界较模糊，或者主要价值集中于某一细分 Software Engineering Workflow 的候选。

### Excluded

不符合研究范围、属于模型层、仅为 plugin-only、已停止、重复计算，或者在当前时间截点缺乏足够独立研究价值。

---

## 4. Global Candidate Universe

> Evidence Grade 表示**当前证据对候选定位的支持强度**，不是产品好坏评分。

### 4.1 Core Candidates

| # | Product / Product Family | Company | Region | Product Surface | Agentic Level | Primary Use Case | Key Evidence / Why in Core | Evidence Grade |
|---:|---|---|---|---|---|---|---|---|
| 1 | Claude Code | Anthropic | Global | CLI, IDE integration | Software Engineering Agent / Autonomous | Repo-level coding, debugging, refactoring, execution | 2026 独立调查使用率处于最前列；Anthropic 自有研究覆盖约 23.5 万用户，且显示使用场景持续向更高层 software work 扩展。[^market1][^market3] | A |
| 2 | Codex | OpenAI | Global | App, CLI, IDE, Cloud | Software Engineering Agent / Autonomous | 多 Agent coding、long-running tasks、cloud delegation、repo work | 具备 CLI + App + IDE + Cloud 一体化产品家族；支持并行 agent、skills、automations、MCP 等。[^codex1][^codex2][^codex3] | A |
| 3 | GitHub Copilot | GitHub / Microsoft | Global | IDE, CLI, Cloud, GitHub | Agentic Coding / Software Engineering Agent | Repo coding、issue/PR、cloud agent、review | 有广泛开发者生态，同时已具备 CLI agent、cloud coding agent、custom agents、skills、MCP。[^copilot1][^copilot2][^copilot3] | A |
| 4 | Cursor | Anysphere / SpaceX | Global | IDE, CLI, Cloud, Desktop | Software Engineering Agent | AI-native IDE、repo agents、cloud execution | Agent 能独立完成 coding task、使用 terminal/tools；Cloud Agents 可在远程 VM 中执行和测试。2026 年 8 月已发生所有权重大变化，当前公司关系应在 Phase 2 单独核实。[^cursor1][^cursor2][^cursor3][^cursor4] | A |
| 5 | Devin | Cognition | Global | Desktop, Cloud, IDE, CLI ecosystem | Autonomous Software Engineering Agent | Long-running software engineering、fleet / multi-agent、cloud execution | Devin Desktop 为 Windsurf 新名称，当前产品强调本地+云端 agent fleet；官方页面声称超过 100 万用户和 4000+ enterprise customers，但这些是 vendor claims，应作为厂商口径单独记录。[^devin1][^devin2] | B |
| 6 | Google Antigravity | Google | Global | Desktop, CLI, Cloud/API, IDE integrations | Autonomous Software Engineering Agent | Agent command center、复杂 coding tasks、subagents、browser/tool use | 独立 Desktop + CLI + agent SDK/runtime；支持并行/异步 agents、MCP、subagents、web/Chrome、artifacts 与长任务工作流。[^anti1][^anti2][^anti3][^anti4] | A |
| 7 | Kiro | AWS | Global | IDE, CLI, Web, Mobile | Software Engineering Agent / Autonomous | Spec-driven development、requirements/design/tasks、validation、hooks | AWS 明确将 Kiro 定位为 agentic development，强调 spec-driven development、hooks、多 surface 共享 agent/harness。[^kiro1][^kiro2][^kiro3][^kiro4] | A |
| 8 | Replit Agent | Replit | Global | Web / Cloud, Desktop-adjacent workflow | Autonomous / Product-building Agent | Idea-to-production app、end-to-end app building、iteration | Agent 4 强调从需求到可运行产品的端到端工作流；官方 evaluation 讨论了无 repo/测试/框架的真实用户场景和 evaluation loop。[^replit1][^replit2][^replit3] | A |
| 9 | OpenCode | OpenCode / SST ecosystem | Global | CLI, Desktop | Agentic Coding / Software Engineering Agent | Terminal coding、provider-agnostic agent、build/plan | 开源、MIT、终端原生；当前公开 repo 具备很大社区规模，并已有 Desktop beta；支持多 provider 与 build/plan agents。[^opencode1] | A |
| 10 | OpenHands | OpenHands | Global | CLI, Cloud, SDK | Software Engineering Agent / Autonomous | SWE tasks、repo modification、agent environment | 开源 AI-driven development platform，MIT core；拥有大型 GitHub 社区，适合代表 open-source SWE-agent 路线。[^openhands1] | A |
| 11 | Cline | Cline | Global | IDE, CLI, headless | Agentic Coding / Software Engineering Agent | IDE agent、CLI automation、tool use、MCP | 开源 autonomous coding agent，已扩展到 SDK、IDE extension、CLI/headless，具备较大 GitHub 社区。[^cline1] | A |
| 12 | Qoder | Alibaba Cloud / Qoder | Global + China | IDE, CLI, Mobile, Cloud Agents, JetBrains | Software Engineering Agent / Autonomous | Agentic coding、large repo、cloud agents、enterprise | 全球 Qoder 与中国 Qoder CN 应合并研究；Qoder CN 是原 Tongyi Lingma 的产品线延续并于 2026 年完成名称迁移。具备 IDE、CLI、Cloud Agent 与企业路线。[^qoder1][^qoder2][^qoder3] | A |
| 13 | TRAE | ByteDance | Global + China | IDE, Desktop, Web, Mobile, CLI/workspace ecosystem | Agentic Coding / Autonomous | AI-native IDE、SOLO / Work、multi-agent coding | TRAE 已从单纯 IDE 扩展到 SOLO / Work；官方持续强调复杂 coding task、多-agent、agent ecosystem。[^trae1][^trae2][^trae3] | B |
| 14 | Tencent CodeBuddy | Tencent | China + Global-facing | IDE/Web, CLI, Cloud Agent | Software Engineering Agent / Autonomous | Coding agent、cloud agent、enterprise workflow、MCP | 已具备 CLI agents、child agents、MCP、web/terminal workflow，以及带持久 sandbox 的 CloudAgent；中国市场代表性较高。[^codebuddy1][^codebuddy2] | B |
| 15 | JetBrains AI / Junie | JetBrains | Global | IDE, Terminal | Agentic Coding / Software Engineering Agent | IDE-native coding、debugging、PR review、long-running tasks | JetBrains AI 与 Junie 应作为一个主要产品家族研究；2026 年 Junie 已脱离 beta，进入 IDE + terminal 的完整 agent workflow。JetBrains 公开调查亦把二者作为重要 IDE AI 采用信号。[^jetbrains1][^market1] | A |
| 16 | Kimi Code | Moonshot AI | China + Global-facing | CLI, IDE | Software Engineering Agent | Repo analysis、multi-step planning、shell、web、subagents | Kimi Code 已形成 terminal + IDE agent 产品，支持多步骤规划、执行、子 agents、web search 与文件修改；2026 年持续快速迭代。[^kimi1][^kimi2] | B |
| 17 | Amazon Q Developer | AWS | Global | IDE, CLI, Cloud | Agentic Coding / Software Engineering Agent | AWS-aware coding、multi-file、tests、enterprise development | 具备 IDE + CLI agentic coding；但 AWS 正引导用户转向 Kiro，且部分 IDE plugin 生命周期已明确，因此作为 Core 但需关注产品迁移。[^qdev1][^qdev2][^qdev3] | B |

### 4.2 Secondary Candidates

| # | Product / Product Family | Company | Region | Product Surface | Agentic Level | Why Included | Evidence Grade |
|---:|---|---|---|---|---|---|---|
| 18 | Jules | Google | Global | Cloud / GitHub | Autonomous Software Engineering Agent | 异步 cloud coding agent，代表 Google 的另一条 cloud-first SWE 路线；与 Antigravity 存在生态/产品重叠，Phase 2 需核对长期产品关系。 | B |
| 19 | Mistral Vibe | Mistral AI | Global | CLI, Desktop/workspace | Agentic Coding / General Agent hybrid | Terminal-native coding agent，具备 subagents、skills、Code/Work modes；Work Mode 使其产品边界比纯 coding agent 更宽。[^vibe1][^vibe2] | B |
| 20 | Qwen Code | Alibaba / Qwen | Global + China | CLI | Software Engineering Agent | 开源 CLI agent，生态活跃，与 Qoder 的产品边界不同；适合代表 model-company-driven CLI agent 路线。[^qwen1][^qwen2] | B |
| 21 | Goose | Block / Linux Foundation ecosystem | Global | Desktop, CLI, API | General-purpose Agent with strong coding use | 开源桌面+CLI agent，可用于 code、workflows 等；因定位并非 coding-only，放 Secondary 而非 Core。[^goose1] | B |
| 22 | Aider | Aider | Global | CLI | Agentic Coding | 经典 terminal coding agent，生态与影响力长期存在；但 2026 年市场势能相对 Core 产品有限。 | C |
| 23 | SWE-agent | Princeton / community | Global | CLI / OSS | Software Engineering Agent | SWE-bench / GitHub issue 自动修复路线的重要开源代表，研究价值高，但商业/市场规模有限。[^swe1] | B |
| 24 | mini-SWE-agent | OSS research community | Global | CLI / OSS | Software Engineering Agent | 极简 agent harness、SWE-bench 影响力强；适合研究 agent architecture，而非市场规模。[^swe1] | B |
| 25 | Kilo Code | Kilo Code | Global | IDE / CLI ecosystem | Agentic Coding | 开源/社区驱动 coding agent，活跃于 agent ecosystem；需要 Phase 2 用一手资料核实当前独立 surface。[^index1][^index2] | C |
| 26 | Warp | Warp | Global | Terminal, Desktop, Cloud agents | Agentic Coding / Dev workspace | Terminal-first workflow、agents 与 developer environment 结合，代表“agentic terminal/workspace”路线。[^index1][^index2] | C |
| 27 | Continue | Continue | Global | IDE / Agent tooling | Agentic Coding / Open-source | 开源 coding agent / developer AI tooling 生态的重要项目；产品形态和独立 surface 在 2026 年变化快，需核实。[^index1][^index2] | C |
| 28 | Amp | Sourcegraph | Global | CLI / IDE ecosystem | Agentic Coding | Sourcegraph 生态中的 coding agent 路线，适合研究 enterprise developer-agent 工作流。[^index1][^index2][^index3] | C |
| 29 | Augment Code | Augment | Global | IDE / Agent | Software Engineering Agent | 强调大型代码库 context/reasoning 与 enterprise coding；市场数据不足，但技术路线具有代表性。[^index2][^index3] | C |
| 30 | Factory | Factory AI | Global | Cloud / IDE / CLI ecosystem | Autonomous Software Engineering Agent | “Droids”/autonomous workflow 路线在企业 SWE agent 市场具有代表性；当前独立 product surface 与 adoption 需 Phase 2 进一步核实。[^index2][^index3] | C |
| 31 | Poolside | Poolside | Global | Cloud / Agent platform | Autonomous Software Engineering Agent | 代表 enterprise/autonomous coding agent 与模型/agent 基础设施结合路线；公开 adoption 数据有限。[^index2][^index3] | C |
| 32 | Zed AI | Zed Industries | Global | AI-native IDE | Agentic Coding | 独立高性能 IDE + agents，适合代表编辑器重构/开源生态方向；需要区分 Zed IDE 与 agent 本身。[^index1][^index2] | C |
| 33 | Bolt.new | StackBlitz | Global | Web / Cloud | Autonomous Product-building Agent | 浏览器内从自然语言到应用的端到端生成/修改/部署，偏 app builder，但与 Agentic SWE Workflow 有明显交集。 | C |
| 34 | v0 | Vercel | Global | Web / Cloud | Autonomous Product-building Agent | 从自然语言到 UI / full-stack app 的 agentic workflow；更偏 web product builder，作为边界型候选保留。 | C |
| 35 | CodeRabbit | CodeRabbit | Global | GitHub / IDE integrations | Software Engineering / Review Agent | PR/code-review 自动化影响力较高，但核心 workflow 更偏 review 而不是从任务到代码的完整 coding agent；作为边界候选。[^index1] | C |
| 36 | Qodo | Qodo | Global | GitHub / IDE / CI | Software Engineering / Review Agent | 测试、review、repo quality agents 具有代表性，但不是最典型的任务→代码→执行主链路。[^index1][^index2] | C |

### 4.3 Watchlist

| # | Product / Product Family | Company | Region | Current Signal | Why Watch | Evidence Grade |
|---:|---|---|---|---|---|---|
| 37 | DeepSeek Reasonix | DeepSeek | China + Global-facing | New coding agent | 官方 API 已提供 terminal coding agent；当前生态、独立产品规模和长期路线仍较早期。[^reasonix1] | B |
| 38 | Lovable | Lovable | Global | Rapid app-builder / vibe-coding category | 强调从自然语言到完整 web product 的 agentic workflow，但与传统 repo-centric SWE agent 边界明显。 | C |
| 39 | Plandex | Plandex | Global | Long-task terminal agent | 多步骤 coding / planning 路线具有概念代表性，但市场规模有限。[^index2][^index3] | C |
| 40 | Crush | Charm | Global | Terminal agent | 开源 terminal agent，属于 fast-moving ecosystem；影响力和成熟度仍待验证。[^index2] | C |
| 41 | Refact.ai | Refact | Global | Agentic coding | 开源/企业 coding agent 路线，市场公开数据有限。[^index2][^index3] | C |
| 42 | Greptile | Greptile | Global | Repo/code understanding + review agent | 适合作为“code intelligence → agent”路线观察对象；更偏 review/repo analysis。[^index2] | C |
| 43 | Cubic | Cubic | Global | Code review / debugging agent | 代表自动 review/debugging 的垂直 agent 路线；是否应归入主 coding-agent universe 仍存在边界问题。[^index2] | C |
| 44 | Tabnine | Tabnine | Global | IDE / coding AI | Longstanding developer AI vendor，正在向 agentic workflow 演进；当前独立 agent capability 与市场数据需进一步核验。 | C |

---

## 5. China Candidate Signals

中国市场在 2026 年已经不只是“国外 Coding Agent 的本地替代”，而是开始出现 **CLI Agent + AI IDE + Cloud Agent + Enterprise Workflow** 并行发展的产品结构。

### 5.1 中国市场第一层代表

- **Qoder / Qoder CN（原 Tongyi Lingma）**：Alibaba Cloud 体系，兼顾 IDE、CLI、Cloud Agent 与 enterprise 路线。应视为一个 Product Family，而不是 Lingma、Qoder、Qoder CN 多个产品。[^qoder1][^qoder2][^qoder3]
- **TRAE**：从 AI IDE 进一步扩展到 SOLO / Work 和更完整的 agent ecosystem，代表大厂 AI-native IDE → agent workspace 路线。[^trae1][^trae2]
- **Tencent CodeBuddy**：CLI、Web、CloudAgent、MCP、child agents 和 enterprise sandbox 使其成为中国企业 coding agent 的重要候选。[^codebuddy1][^codebuddy2]
- **Kimi Code**：terminal + IDE agent 路线，强调 repository understanding、planning、subagents、web/tool use，是中国 AI lab 进入 coding agent 的代表。[^kimi1][^kimi2]
- **Qwen Code**：开源 CLI agent，依托 Qwen 生态，适合作为 OSS / model-company-driven coding agent 路线观察对象。[^qwen1][^qwen2]
- **DeepSeek Reasonix**：截至研究截点仍较新，但进入了官方 API 的 coding agent 层，具有潜在高战略意义。[^reasonix1]
- **Baidu Comate**：百度的 AI-native coding ecosystem，具备独立 AI IDE、插件以及 coding agents / multi-agent collaboration，属于重要企业开发者候选。[^comate1][^comate2]

### 5.2 中国市场的结构性特征

目前可以观察到四条互相重叠但尚未完全收敛的路线：

1. **AI IDE → Agent Workspace**：TRAE、Qoder、Comate 等；
2. **CLI / Terminal Agent**：Kimi Code、Qwen Code、Reasonix 等；
3. **Enterprise Coding Agent**：CodeBuddy、Qoder CN、Comate、Q Developer/Kiro 的中国市场替代竞争；
4. **Open-source / model-native agent**：Qwen Code、Kimi Code 相关生态，以及其他开源 terminal agents。

因此，Phase 2 不应仅比较“谁更像 Cursor”，而要比较这些产品承担的 Software Engineering Workflow 是否不同。

---

## 6. Product Family / Surface Mapping

| Product Family | Current / Major Surfaces | Research Handling |
|---|---|---|
| Claude Code | CLI, IDE integrations | One candidate |
| Codex | App, CLI, IDE, Cloud | One candidate |
| GitHub Copilot | IDE, CLI, GitHub, Cloud agent | One candidate |
| Cursor | IDE, CLI, Cloud agents | One candidate |
| Devin | Desktop, Cloud, IDE / Windsurf legacy | One candidate |
| Google Antigravity | Desktop, CLI, Agent SDK/API, IDE integrations | One candidate |
| Kiro | IDE, CLI, Web, Mobile | One candidate |
| Replit Agent | Web / Cloud | One candidate |
| OpenCode | CLI, Desktop | One candidate |
| OpenHands | CLI, Cloud, SDK | One candidate |
| Cline | IDE, CLI, headless | One candidate |
| Qoder | Qoder IDE, CLI, Mobile, Qoder CN IDE, Cloud Agents | One candidate |
| TRAE | IDE, Desktop, Web, Mobile, SOLO / Work | One candidate |
| Tencent CodeBuddy | Web, IDE-ish surfaces, CLI, CloudAgent | One candidate |
| JetBrains AI / Junie | IDE, Terminal | One candidate |
| Kimi Code | CLI, IDE | One candidate |
| Amazon Q Developer | IDE, CLI, AWS workflow | One candidate |

### Known deduplication decisions

- **Tongyi Lingma**：不单独计数；2026 年 Qoder CN 是其当前产品线名称/继承关系的一部分，因此归入 Qoder Family。[^qoder2]
- **Windsurf**：不与 Devin Desktop 分开作为新的市场候选；Cognition 当前将 Devin Desktop 明确描述为 Windsurf 的新名称。[^devin1]
- **Copilot CLI / Copilot coding agent**：不拆分。
- **Cursor Cloud Agent / Cursor IDE / Cursor CLI**：不拆分。
- **TRAE SOLO / TRAE Work / TraeCode**：不拆分。
- **JetBrains AI Assistant / Junie**：本阶段合并处理；Phase 2 再判断两者是否需要在 capability matrix 中拆分 surface，而不是拆成两个市场候选。

---

## 7. Core Candidates — Why They Matter

Core Candidate 并非预选 Top 10，而是 Phase 2 优先研究集。

### Market-heavy Core

Claude Code、Codex、GitHub Copilot、Cursor、Devin、Google Antigravity、Kiro、Replit Agent、Amazon Q Developer。

这些产品要么已有独立市场/开发者采用信号，要么具备大型平台生态与 enterprise distribution。

### Technology / Workflow-heavy Core

OpenCode、OpenHands、Cline、Qoder、TRAE、Tencent CodeBuddy、JetBrains AI / Junie、Kimi Code。

这些产品的重要性不仅来自规模，也来自：

- Terminal-native workflow；
- Open-source agent harness；
- Spec-driven development；
- Multi-agent / parallel execution；
- Cloud sandbox / long-running tasks；
- MCP / Skills / custom agents；
- 从 IDE 向 Agent Workspace 迁移；
- 中国市场独立 agent 生态。

**这里刻意没有把 Core 排成 1–17。** 排名属于 Phase 3。

---

## 8. Excluded Candidates

| Candidate / Object | Status | Exclusion Reason | Evidence / Notes |
|---|---|---|---|
| GPT / Claude / Gemini / Qwen / DeepSeek models | Excluded | Pure model；属于 Underlying Model / Model Layer，不是本研究的 Agent Product。 | 遵循 Charter 的 Model-vs-Agent rule。 |
| Roo Code | Excluded | 截至 2026 年中后期已停止/关闭，不再适合作为当前市场候选。 | Secondary ecosystem tracking indicates shutdown in May 2026；若未来恢复，应重新进入候选池。[^discovery3] |
| Sweep | Excluded | 当前活跃度明显不足；社区/生态追踪显示 2026 年持续发布活动有限，不值得在本阶段作为独立核心候选。 | 需要注意这是低置信度排除，不应等同于项目永久关闭。[^discovery3] |
| Gemini CLI（作为独立候选） | Excluded / Merge pending | 不单独计数，避免与 Google 当前 Antigravity CLI / agent ecosystem 重复；是否完全退休需 Phase 2 用官方资料最终确认。 | 当前仅作产品家族去重处理，标记为 **Merge pending**，而非声称已正式停止。[^anti2][^discovery1] |
| Tongyi Lingma（作为独立候选） | Excluded / Merged | 当前研究按 Qoder / Qoder CN 产品家族统一处理。 | 官方命名迁移证据较强。[^qoder2][^qoder3] |
| Plugin-only coding extensions with no independent CLI/IDE/Desktop/Cloud agent | Excluded | 不满足 Product Surface scope。 | Charter explicit exclusion。 |

> Roo Code、Sweep 的当前状态证据属于社区/二级发现信号，证据等级低于 Core 的官方产品事实；这是有意保守处理，Phase 2 不应继续把它们当作活跃市场主流，除非找到相反的一手证据。

---

## 9. Coverage Review

### 9.1 Global coverage

| Coverage Axis | Covered? | Representative Candidates |
|---|---|---|
| AI-native IDE | Yes | Cursor, TRAE, Qoder, JetBrains Junie, Kiro, Zed |
| CLI Coding Agent | Yes | Claude Code, Codex, OpenCode, Cline, Kimi Code, Qwen Code, Reasonix |
| Cloud Coding Agent | Yes | Codex, Copilot, Devin, Antigravity, Kiro, Replit, OpenHands, Jules |
| Desktop Agent | Yes | Codex App, Devin Desktop, Antigravity, OpenCode, Goose |
| Autonomous SWE Agent | Yes | Devin, Codex, Antigravity, Kiro, OpenHands, Replit, Jules |
| Open-source Agent | Yes | OpenCode, OpenHands, Cline, Qwen Code, SWE-agent, mini-SWE-agent, Goose |
| Major Big Tech | Yes | OpenAI, Microsoft/GitHub, Google, AWS, Alibaba, Tencent, ByteDance, Baidu |
| Major AI labs | Yes | Anthropic, OpenAI, Google, Mistral, Moonshot, DeepSeek, Alibaba/Qwen |
| Developer-tool companies | Yes | Anysphere, JetBrains, Sourcegraph, Augment, Factory, Zed, Replit, Warp |
| Enterprise developer tooling | Yes | Copilot, Kiro, Q Developer, CodeBuddy, Qoder, Junie, Factory, Augment |
| App-builder / Vibe Coding boundary | Yes | Replit Agent, Bolt.new, v0, Lovable |

### 9.2 China coverage

中国市场至少覆盖：

- AI-native IDE：TRAE、Qoder、Baidu Comate；
- CLI / terminal agents：Kimi Code、Qwen Code、DeepSeek Reasonix；
- Enterprise coding agent：Tencent CodeBuddy、Qoder CN、Baidu Comate；
- Major Chinese AI companies：Alibaba/Qwen、ByteDance、Tencent、Baidu、Moonshot、DeepSeek；
- OSS / developer ecosystem：Qwen Code 与其他中国开发者生态。

### 9.3 Coverage gaps to keep open

仍存在几个需要 Phase 2 明确核验的区域：

1. **Sourcegraph / Amp、Augment、Factory、Poolside** 的 2026 产品 surface 与 adoption；
2. **Google Antigravity 与 Jules / Gemini CLI** 的产品边界与长期整合关系；
3. **App Builder vs Coding Agent** 的研究边界（Bolt、v0、Lovable、Replit）；
4. **Code Review / Repo Intelligence Agent** 是否属于主研究 population（CodeRabbit、Qodo、Greptile、Cubic）；
5. **中国企业市场份额** 的公开、可比、独立数据仍非常有限。

这些不是本阶段的缺陷，而是下一阶段需要转成明确 Evidence Collection Questions 的开放问题。

---

## 10. Key Observations

### 10.1 Market is splitting into multiple surfaces, not converging on one IDE

截至 2026 年 8 月，市场已经明显同时存在：

- IDE-native agent；
- terminal-native agent；
- cloud/background agent；
- desktop agent command center；
- application-builder / browser-native agent。

因此“谁是最好的 IDE”已经不是完整问题。更关键的问题是：**谁在掌握 Software Engineering Workflow 的哪个阶段。**

### 10.2 The important product unit is increasingly the agent system, not the editor

Copilot、Codex、Antigravity、Kiro、Devin、Cursor 等正在把 agent、tools、sandbox、cloud execution、MCP、skills、memory/rules、parallelism 组合成完整的 system。

这意味着未来分析产品时，不能仅看 UI，而必须看：

`Model → Harness → Tools → Runtime/Sandbox → Context/Memory → Product → Workflow`

这与 Charter 的研究原则完全一致。

### 10.3 Open-source is becoming an architecture laboratory

OpenCode、OpenHands、Cline、SWE-agent、mini-SWE-agent、Qwen Code、Goose 等构成了一个重要开源实验场。它们未必拥有最大的市场，但能快速验证：

- provider-agnostic agent；
- open harness；
- local/cloud runtime；
- subagents；
- tool protocols；
- agent composability。

因此 Open-source candidates 不能因用户量不足而全部排除。

### 10.4 China is developing a parallel product stack

中国候选已经不是单一的“国产 AI IDE”，而是在形成：

`AI IDE + CLI Agent + Cloud Agent + Enterprise Platform + Model-native Agent`

这使 Qoder、TRAE、CodeBuddy、Comate、Kimi Code、Qwen Code、Reasonix 等值得作为全球研究 population 的一部分，而不是单独隔离成“中国 TOP5”。

### 10.5 Product boundaries are becoming fuzzy

最明显的边界模糊包括：

- Coding Agent vs General Agent：Goose、Mistral Vibe、TRAE Work；
- Coding Agent vs App Builder：Replit、Bolt、v0、Lovable；
- Coding Agent vs Review Agent：CodeRabbit、Qodo、Greptile、Cubic；
- IDE vs Agent Workspace：Cursor、TRAE、Qoder、Kiro、Antigravity。

Phase 2 必须用“Software Engineering Workflow Coverage”而不是品牌标签判断这些边界。

---

## 11. Open Questions for Phase 2

### Market evidence

1. 是否可以建立一份按统一口径记录的 2026 adoption evidence matrix？
2. 哪些产品拥有可靠的企业客户、活跃用户、usage volume 或 revenue evidence？
3. 哪些中国产品有可独立验证的 adoption / enterprise evidence？

### Product / architecture

4. 每个 Core Candidate 的真实 agent loop 是什么？
5. 哪些产品具备真正独立的 runtime / sandbox，而不仅是 IDE wrapper？
6. 哪些产品拥有真正有效的 long-running / background / parallel agent capability？
7. Skills、MCP、memory、rules、subagents 在不同产品中到底承担什么架构角色？

### Market structure

8. AI-native IDE、CLI Agent、Cloud Agent、Desktop Agent 是否正在收敛到统一 Agent Workspace？
9. “Model provider + open harness” 与“vertically integrated agent product”谁更可能成为长期主导形态？
10. 中国市场是否正在形成与美国不同的 enterprise-first coding-agent route？

### Boundary / selection

11. Replit / Bolt / v0 / Lovable 应在最终 Top10 中作为 Coding Agent 研究还是作为 adjacent category？
12. CodeRabbit / Qodo / Greptile / Cubic 是否属于本研究定义的 Coding Agent？
13. Jules、Gemini CLI 与 Antigravity 如何按 Product Family 处理，才能避免 Google 自身产品重复计数？
14. Factory、Amp、Augment、Poolside 的当前 2026 市场采用度是否足以提升为 Core？

---

## 12. Sources

### Tier 1 / Primary

- Anthropic — Claude Code product / research materials: https://www.anthropic.com/research/claude-code
- OpenAI — Codex overview / Codex app / Codex CLI: https://openai.com/codex/ ; https://openai.com/index/unrolling-the-codex-agent-loop/
- GitHub — Copilot CLI / coding agent / custom agents: https://docs.github.com/en/copilot/concepts/agents/copilot-coding-agent ; https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli
- Cursor — Agent / Cloud Agents: https://cursor.com/ ; https://cursor.com/docs/agent/overview
- Devin — Devin Desktop / Windsurf transition: https://devin.ai/ ; https://devin.ai/desktop
- Google — Antigravity / Antigravity 2.0 / SDK: https://antigravity.google/ ; https://developers.googleblog.com/en/google-antigravity-2/
- AWS — Kiro / Kiro docs: https://kiro.dev/ ; https://kiro.dev/docs/
- Replit — Agent / Agent 4 / evaluation: https://replit.com/ai ; https://blog.replit.com/agent-4 ; https://blog.replit.com/evaluating-replit-agent-at-scale
- OpenCode — GitHub repository: https://github.com/anomalyco/opencode
- OpenHands — GitHub repository: https://github.com/All-Hands-AI/OpenHands
- Cline — GitHub repository: https://github.com/cline/cline
- Alibaba/Qoder — Qoder / Qoder CN / product announcements: https://qoder.com/ ; https://qoder.com/cn ; https://www.aliyun.com/
- TRAE — product / SOLO / Work materials: https://www.trae.ai/ ; https://www.trae.ai/solo
- Tencent CodeBuddy — docs / announcements: https://www.codebuddy.ai/ ; https://cloud.tencent.com/product/codebuddy
- JetBrains — Junie / JetBrains AI: https://www.jetbrains.com/junie/ ; https://www.jetbrains.com/ai/
- Kimi Code — product / CLI: https://www.kimi.com/code ; https://github.com/MoonshotAI/kimi-cli
- Amazon Q Developer — docs / agentic coding: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html
- Mistral Vibe: https://mistral.ai/products/vibe
- Qwen Code: https://github.com/QwenLM/qwen-code
- DeepSeek Reasonix: https://api-docs.deepseek.com/guides/reasonix
- Baidu Comate: https://comate.baidu.com/

### Tier 2 / Independent research

- JetBrains — AI Coding Agents: Adoption Trends, Aug 2026: https://blog.jetbrains.com/ai/2026/08/ai-coding-agents-adoption-trends/
- JetBrains — State of Developer Ecosystem / AI tools, Apr 2026: https://blog.jetbrains.com/research/2026/04/ai-developer-ecosystem/
- JetBrains — State of Developer Ecosystem 2025: https://www.jetbrains.com/lp/devecosystem-2025/
- Stack Overflow — 2025 Developer Survey: https://survey.stackoverflow.co/2025/technology/

### Tier 3 / Discovery / ecosystem signals

- Agentic Index — coding agent comparison: https://agenticindex.com/
- Awesome Coding Agents: https://github.com/Voltagent/awesome-coding-agents
- Inclusion AI — agentic coding landscape (Aug 2026): https://www.inclusion.ai/blog/agentic-coding/
- Ry Walker — open coding agent ecosystem tracking: https://substack.com/

---

## 13. Research Status

**Phase 1 conclusion:** Candidate Universe 已建立，可进入 Phase 2。

Approximate research population at this stage:

- **44 active candidate product families / candidates**：17 Core + 19 Secondary + 8 Watchlist；
- **5 explicitly excluded / merged objects**：主要是 models、已停止/低活跃项目、以及为防止重复计算而合并的产品名称；
- 总共约 **49 个被审计/处理的名称或产品家族对象**。

注意：这里的“49”不是市场规模数字，而是本阶段研究处理的候选/别名/排除对象数量。Core/Secondary/Watchlist 是研究优先级分层，不是排名。

### Phase 1 Exit Criteria

- [x] Research Charter 已读取并作为最高约束；
- [x] Candidate Universe 已建立；
- [x] Global 主要 product surfaces 已覆盖；
- [x] China candidate signals 已覆盖；
- [x] Product Family 去重已执行；
- [x] Model vs Agent 已区分；
- [x] Excluded candidates 已记录原因；
- [x] Market adoption 与 capability/innovation 分开；
- [x] 尚未进行正式 Top 10 排名；
- [x] Phase 2 未被提前执行。

---

[^market1]: JetBrains, “AI Coding Agents: Adoption Trends”, August 2026. Independent developer survey; figures are survey adoption signals, not total global market share.
[^market2]: JetBrains, AI developer ecosystem analysis, April 2026.
[^market3]: Anthropic, “How AI is changing software development”, June 2026; based on Anthropic's own Claude Code usage research, not a market-wide census.
[^codex1]: OpenAI Codex product / app announcement, February–March 2026.
[^codex2]: OpenAI, “Unrolling the Codex agent loop”, January 2026.
[^codex3]: OpenAI Codex CLI documentation / GitHub.
[^copilot1]: GitHub Copilot coding agent documentation.
[^copilot2]: GitHub Copilot CLI documentation.
[^copilot3]: GitHub agent/custom agents/skills/MCP documentation.
[^cursor1]: Cursor Agent documentation.
[^cursor2]: Cursor Cloud Agents documentation.
[^cursor3]: Cursor product documentation for CLI / agent workflows.
[^cursor4]: Reuters, August 29, 2026 reporting on SpaceX's acquisition of Anysphere/Cursor and related model-access changes; corporate status should be separately re-verified in Phase 2.
[^devin1]: Devin official desktop pages stating “Devin Desktop is the new name for Windsurf.”
[^devin2]: Devin official FAQ / enterprise claims; user and customer counts are vendor claims.
[^anti1]: Google Antigravity 2.0 announcement, May 2026.
[^anti2]: Antigravity documentation for CLI / agent runtime / SDK.
[^anti3]: Antigravity documentation for subagents, tools, MCP and lifecycle hooks.
[^anti4]: Google Antigravity August 2026 product updates.
[^kiro1]: Kiro official product and IDE documentation.
[^kiro2]: Kiro spec-driven development documentation.
[^kiro3]: Kiro CLI / Web agent documentation.
[^kiro4]: Kiro agent surface / shared harness documentation.
[^replit1]: Replit Agent 4 announcement, March 11, 2026.
[^replit2]: Replit product / plan-while-building materials.
[^replit3]: Replit evaluation at scale, June 23, 2026.
[^opencode1]: OpenCode GitHub repository and releases; current public repository includes terminal agent, desktop beta, build/plan modes and provider flexibility.
[^openhands1]: OpenHands GitHub repository; MIT core, AI-driven development, current public repository stats and releases.
[^cline1]: Cline GitHub repository; autonomous coding agent, IDE/CLI/headless/SDK surfaces.
[^qoder1]: Qoder official product site and Qoder CN documentation.
[^qoder2]: Alibaba/Qoder CN product materials describing the 2026 naming transition from Tongyi Lingma.
[^qoder3]: Qoder/Qoder CN pricing and product updates, August 2026.
[^trae1]: TRAE official product site.
[^trae2]: TRAE SOLO / TRAE Work announcements and product materials.
[^trae3]: TRAE ecosystem / agentic IDE documentation.
[^codebuddy1]: Tencent CodeBuddy current documentation for CLI, agents, MCP, workers / child agents.
[^codebuddy2]: Tencent Cloud / CodeBuddy CloudAgent product materials.
[^jetbrains1]: JetBrains Junie product documentation and June 2026 release materials.
[^kimi1]: Kimi Code official product materials.
[^kimi2]: Kimi Code CLI GitHub repository and current 2026 product updates.
[^qdev1]: Amazon Q Developer docs for agentic coding, IDE and CLI.
[^qdev2]: AWS documentation on Q Developer CLI / agentic coding.
[^qdev3]: AWS documentation noting migration toward Kiro and future IDE plugin support changes.
[^vibe1]: Mistral Vibe official product page.
[^vibe2]: Mistral Vibe documentation for Code / Work modes, subagents and skills.
[^qwen1]: Qwen Code GitHub repository.
[^qwen2]: Qwen Code current 2026 release / ecosystem documentation.
[^goose1]: Goose GitHub / official project materials; open-source desktop + CLI + API, general-purpose agent with coding support.
[^swe1]: SWE-agent / mini-SWE-agent GitHub repositories and public SWE-bench-oriented materials.
[^index1]: Agentic Index public coding-agent comparison, used only as discovery/coverage signal.
[^index2]: Awesome coding-agent ecosystem lists, used only for candidate discovery and coverage.
[^index3]: Community coding-agent ecosystem tracking, used only as a secondary discovery signal.
[^reasonix1]: DeepSeek official API documentation for Reasonix coding agent.
[^comate1]: Baidu Comate official documentation describing AI IDE, plugins, coding agents and multi-agent collaboration.
[^comate2]: Baidu Comate 2026 product/news materials.
[^discovery1]: Public 2026 coding-agent ecosystem lists that include Google CLI/Antigravity relationships; requires official verification in Phase 2.
[^discovery3]: Public community ecosystem tracking used as discovery evidence for project activity/shutdown; lower-confidence than primary sources.
