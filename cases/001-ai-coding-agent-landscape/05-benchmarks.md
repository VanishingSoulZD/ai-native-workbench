# Case 001 — 2026 AI Coding Agent Landscape

## Phase 5 — Public Benchmark & Independent Evidence Analysis

> Research snapshot: 2026-08-31
>
> Research cutoff: August 2026
>
> Status: Phase 5 completed
>
> Research unit: AI Coding Agent Product / Product Family
>
> Scope constraint: This phase does not recreate the Candidate Universe, recompute Top 10, or perform the final cross-product decision. Public benchmarks and independent studies are supporting evidence for the Phase 4 product judgments.

---

## 1. Phase 5 Objective

本阶段回答的不是“哪个 Benchmark 排名最高”，而是：

> **公开 Benchmark 与高质量独立证据到底测量了 AI Coding Agent 的哪一层能力，以及这些证据能否验证 Phase 4 对 Product / Agent Capability 的判断。**

本阶段严格继承 `00-research-charter.md` 的约束：

- Research Scope 不变；
- Research Population 不变；
- Research Unit 仍为 Product / Product Family；
- Top 10 不因 benchmark 结果自动改变；
- 不把 Model Benchmark 当作 Product Benchmark；
- 不把 Leaderboard 当作 Market Ranking；
- 不把 Benchmark Result 自动解释为 Real-world Productivity；
- 不自行设计、运行新的 Standard Coding Agent Benchmark。

最终 Phase 5 只新增本文件：

`cases/001-ai-coding-agent-landscape/05-benchmarks.md`

---

## 2. Research Method

### 2.1 Evidence hierarchy

优先级：

1. **Tier 1 — Primary**：Benchmark 官方站点、官方 GitHub、论文、technical report、官方 leaderboard、官方 methodology；
2. **Tier 2 — Independent**：METR、学术研究、独立开发者调查、独立代码审查研究；
3. **Tier 3 — Community / Discovery**：GitHub issues、社区讨论、benchmark commentary；
4. **Tier 4 — Individual Review**：单次体验或个人博客，仅作补充。

### 2.2 Classification rule

本阶段统一采用以下分层：

```text
Model
  ↓
Model + Prompt / Minimal Scaffold
  ↓
Agent + Harness
  ↓
Agent + Runtime / Environment
  ↓
Product / Product Family
  ↓
Developer Workflow / Real-world Productivity
```

Benchmark 的结果只能映射到它真正测量的层级，禁止跨层推断。

### 2.3 Core decision criteria

一个 benchmark 是否值得进入本 Case，主要看五件事：

- 是否接近真实 Software Engineering Task；
- 是否允许真实工具/环境交互；
- 是否存在多步骤 execution / verification / repair；
- 是否能够区分 model capability 与 agent/harness capability；
- 对 Top 10 Product / Product Family 判断是否具有增量解释力。

---

## 3. Benchmark Candidate Universe & Selection

### 3.1 Candidates screened

本阶段检查了以下方向：

| Candidate | Decision | Reason |
|---|---|---|
| SWE-bench / SWE-bench Verified | **Core** | 真实 GitHub issue + repository + executable validation，是 repo-level SWE 的主流公开基线 |
| Terminal-Bench 2.1 | **Core** | 真正评估 agent 在 container/terminal 环境中的连续工具使用与任务完成 |
| SWE-bench Pro | **Core** | 面向更长、更复杂、企业级 repo-level SWE，直接针对传统 SWE-bench 的深度与现实性不足 |
| ProjDevBench | **Core** | 从项目需求出发进行 end-to-end project development，显式包含架构、执行、code review 与迭代 |
| SWE-Lancer | **Core** | 任务来自真实 freelance software engineering，并以真实历史支付金额建立经济价值尺度 |
| Kotlin Benchmark | **Core** | 2026 新发布的 agent-level、language-specific repository SWE benchmark，能够检验 agent 对真实 Kotlin repo 的迁移能力 |
| Long-Horizon-Terminal-Bench | **Core / Emerging** | 进一步拉长 terminal agent 任务，并提供 dense intermediate grading，对长期 autonomy 有增量解释力 |
| DevBench / DevEval | **Supporting** | 覆盖 software design、environment setup、implementation、testing，但主要仍以 model/scaffold 为中心，时间较早 |
| HCAST / METR software autonomy tasks | **Independent supporting evidence** | 不是传统 Coding Agent market benchmark，但可帮助理解 autonomy/time-horizon，尤其是任务时长与 agent 能力边界 |
| MirrorCode | **Independent supporting evidence** | 对 weeks-long software reimplementation 提供比传统 benchmark 更长的 horizon 信号，但仍属早期研究 |
| Aider Polyglot | **Low relevance / background** | 多语言代码能力有价值，但主要是 model-level code editing，缺少复杂 agent loop |
| HumanEval / MBPP / APPS | **Excluded from core** | 主要是 function / problem-level generation，无法解释 repo navigation、tool use、verification、long-horizon autonomy |
| WebArena / BrowserGym | **Adjacent only** | 对 browser/computer-use 能力有价值，但不是 Software Engineering-specific benchmark，不能直接作为 Coding Agent 能力基准 |

### 3.2 Selection judgment

因此，本阶段的核心 benchmark set 为：

1. SWE-bench / SWE-bench Verified
2. Terminal-Bench 2.1
3. SWE-bench Pro
4. ProjDevBench
5. SWE-Lancer
6. Kotlin Benchmark
7. Long-Horizon-Terminal-Bench
8. DevBench / DevEval

另外使用 HCAST、MirrorCode、METR developer-productivity studies、Stack Overflow Developer Survey 与 BNY Mellon/academic longitudinal studies作为 Independent Evidence，而不把它们强行塞进同一 Benchmark leaderboard。

---

## 4. Benchmark Evidence Matrix

| Benchmark | Organization | Date / Version | Evaluation Unit | Task Type | Runtime / Tools | Primary Metric | Model-level vs Agent-level | Long-horizon | Relevance | Major Limitation |
|---|---|---|---|---|---|---|---|---|---|---|
| SWE-bench Verified | SWE-bench / OpenAI collaboration | 2024-08; 500 verified tasks | Agent/model + scaffold | Repo-level GitHub issue resolution | Repository + Docker + test harness | Resolved / pass rate | **Mixed; leaderboard can contain agents, while minimal-bash LM comparisons isolate models** | Low–Medium | High | Static public GitHub data; contamination risk; automated grader is narrower than maintainer acceptance |
| Terminal-Bench 2.1 | Terminal-Bench / Harbor | 2026-05 | **Agent + model + runtime** | Terminal/container tasks | Shell/terminal + containerized environment | Accuracy / task success | **Agent-level** | Medium–High | High | Task mix broader than SWE; environment/resource sensitivity; agent/model confounding remains |
| SWE-bench Pro | Scale AI / research team | 2025-09; public/held-out/commercial splits | Agent/model + harness | Long-horizon repo-level SWE | Docker / standardized eval | Patch resolution | **Agent-level in practice, but model + scaffold jointly determine result** | High | High | Public leaderboard/issues have had corrections; cross-run comparability depends on harness and version |
| ProjDevBench | Research team | 2026-02 | **Agent + runtime** | End-to-end project development | Multi-turn environment + OJ + LLM-assisted review | Execution / code review / weighted final score | **Agent-level** | High | High | Only 20 tasks, heavily C++, young benchmark, limited external replication |
| SWE-Lancer | OpenAI Preparedness | 2025-02; updated 2025-07 | Model + SWE scaffold | Real freelance engineering + managerial decisions | Docker; offline updated version; Playwright tests | Pass@1 + dollars earned / managerial agreement | **Primarily model/scaffold evaluation** | Medium | High | Real task realism is strong, but it is not a product benchmark and public split is smaller than original task pool |
| Kotlin Benchmark | JetBrains | 2026-07; first public iteration | **Agent + environment** | Real Kotlin issue resolution | Containerized Kotlin repos + tests | Resolution rate | **Agent-level** | Medium | High | Kotlin-only, 105 tasks, first iteration; future metrics still planned |
| Long-Horizon-Terminal-Bench | Research team | 2026-07 | **Agent + runtime** | Long-horizon terminal tasks | Terminal-style sandbox | Dense / subtask reward + final success | **Agent-level** | **Very High** | Medium–High | Only 46 tasks and mixed-domain task set; not specific to software engineering |
| DevBench / DevEval | OpenCompass / academic research | 2024 paper; COLING 2025 | Model + prompt + baseline agent | Design → environment → implementation → testing | Docker + repo environments | Pass@k, coverage, LLM-judge | **Mostly model-level / scaffold-assisted** | Low–Medium | Medium | Earlier generation of models, small curated set, LLM-judge components, less autonomous tool-driven loop |

### Matrix interpretation

三个明显层级已经出现：

```text
Model-centric
  HumanEval / Aider / DevBench portions
          ↓
Repo-level SWE
  SWE-bench / Kotlin Benchmark / SWE-bench Pro
          ↓
Environment-operating Agent
  Terminal-Bench / ProjDevBench / Long-Horizon-Terminal-Bench
          ↓
Workflow / Productivity
  METR RCTs / maintainer review / developer surveys / field studies
```

真正接近 Product-level 的 benchmark 并不存在一个单一、行业统一的“Gold Standard”。因此本阶段不能把任何 leaderboard 当成最终产品排名。

---

# 5. Benchmark 01 — SWE-bench / SWE-bench Verified

## Benchmark Identity

- **Benchmark Name**：SWE-bench / SWE-bench Verified
- **Organization**：SWE-bench team / Princeton NLP; Verified 与 OpenAI Preparedness 合作
- **Publication / Evaluation Date**：原始 benchmark 2024；Verified 2024-08-13
- **Current Status**：仍是最重要的公开 repo-level SWE 参考系之一，并持续出现变体与下游评测
- **Scope**：真实 GitHub issue + codebase → patch → executable tests

## What It Measures

它主要测量：

- Repository-level issue understanding
- Code navigation / context use
- Patch generation
- Execution against tests
- Compatibility with existing functionality

SWE-bench 的核心任务是给系统 codebase 与 issue，要求生成解决该问题的 patch；Verified 是经过人工筛选的 500 个实例子集。官方明确说明 Verified 的目标是过滤掉难以判断、描述不清或测试存在问题的样本。

## Evaluation Unit

必须分层理解：

- leaderboard 可以接受完整 coding agents；
- 官方也提供 minimal-bash / mini-SWE-agent 风格的模型比较，以尽量隔离模型能力；
- 因此 **SWE-bench 不是纯 Model Benchmark，也不是纯 Product Benchmark**。

更准确的表述是：

> **Benchmark task + chosen scaffold/harness + model** 的联合结果。

## Task Design

- Task source：真实 GitHub issues / resolved PRs
- Repository：公开开源 Python repositories；Verified 首版来自 12 个 repo
- Tool access：agent/scaffold 决定，常见为 shell / file editing / search
- Execution：Dockerized
- Test access：评测时执行隐藏/预定义测试
- Human intervention：benchmark run 本身无实时人工协助
- Time budget：由具体 scaffold/evaluation harness 决定，不能直接视为无限 autonomous execution

## Metrics

核心是 issue resolution / pass rate。

SWE-bench 官方使用 `FAIL_TO_PASS` 与 `PASS_TO_PASS` 测试来判断 patch 是否既解决 issue，又没有明显破坏现有行为。

## Methodology

- Docker 化显著提高了可复现性；
- Verified 通过人工筛选提高任务可判定性；
- 但模型/agent 版本、scaffold、prompt、测试执行方式都会影响最终成绩；
- benchmark 来自公开 GitHub，因此训练污染风险一直存在。

## Results

历史上 SWE-bench 的进步非常快。OpenAI 在 Verified 发布时报告 GPT-4o 的最佳 scaffold 从原始 SWE-bench 的 16% 提升到 Verified 的 33.2%，说明 benchmark composition 本身会显著影响可测得能力。

截至 2026 年的公共 leaderboard，头部系统已经达到极高分数区间，但这些结果必须按具体 model/scaffold/version 阅读，不能把某个模型分数写成产品总体能力。

## What It Proves

**Fact / Evidence**：系统能够在真实开源仓库 issue 上产生可通过自动化测试的修复。

**Analysis**：这比 function-level coding benchmark 更接近 Software Engineering，但仍主要聚焦“issue → patch”。

## What It Does NOT Prove

不能直接证明：

- Product UX 是否优秀；
- Agent 是否善于长时间自主工作；
- Agent 是否能在复杂未知环境中自由选择工具；
- patch 是否符合真实 maintainer 的代码质量标准；
- developer productivity / ROI；
- enterprise adoption。

## Limitations

### Benchmark saturation

随着头部模型分数快速上升，区分更先进系统的空间变小。

### Contamination

官方自己明确提示：静态 public GitHub 数据可能进入预训练数据，因此污染风险是真实问题。

### Automated grader gap

METR 2026-03 的独立研究直接验证了一个关键限制：约一半通过 SWE-bench Verified 自动评分的近期 AI PR，经过真实仓库 maintainer review 后不会被直接合入；在其样本中，maintainer acceptance 相比自动 grader 平均低约 24 个百分点。METR 同时强调，这不是“AI 永远做不到”的证明，因为真实开发者会根据反馈继续迭代，而该研究让 agent 只有一次提交机会。

## Relevance to Case 001

**High**。

它是评价 Phase 4 中“repo-level issue resolution”能力最重要的公共基线之一，但只能验证 Product Agent Loop 的一部分，不能独立决定 Top 10。

**Key judgment**：SWE-bench 是 **necessary evidence, not sufficient evidence**。

---

# 6. Benchmark 02 — Terminal-Bench 2.1

## Benchmark Identity

- **Benchmark Name**：Terminal-Bench 2.1
- **Organization**：Terminal-Bench / Harbor ecosystem
- **Publication / Evaluation Date**：2026-05-06
- **Current Status**：活跃公开 benchmark，2.1 是对 2.0 的修正版
- **Scope**：复杂 containerized terminal tasks

## What It Measures

核心是：

> **Agent 能否在真实可执行环境里，通过 terminal/shell 工具连续操作并完成目标。**

与 SWE-bench 相比，它显著扩大了任务范围：不仅是修改代码，还包含环境搭建、系统操作、调试、安全、数据科学、机器学习等复杂 terminal work。

## Evaluation Unit

这是明显的 **Agent + Runtime** benchmark：

```text
Model
 +
Agent software / harness
 +
Container / sandbox
 +
Tool interaction
```

官方 leaderboard 直接按 Agent + Model + effort 展示结果；同一模型在不同 agent harness 下结果可以明显不同。

## Task Design

- Terminal/container environment
- 多步骤 shell interaction
- 任务完成通常需要反复观察、修改、执行
- 资源、时间、网络等由评测环境控制
- 最新公开机制要求至少 5 trials/task 才能上传 leaderboard

## Metrics

Primary：task accuracy / completion。

Leaderboard 还公开 tokens、cost、release date、PR、hacks 等辅助信息。

## Methodology

2.1 专门修复了 2.0 中 28 个任务的问题；官方指出部分问题来自 bug、timeout/resource 配置、reward-hacking robustness 等。

这非常重要，因为它说明：

> **对于 Agent Benchmark，environment engineering 本身就是 evaluation methodology 的一部分。**

## Results

2026-05 的 2.1 官方报告显示：

- GPT-5.3-Codex + Codex CLI：73.3% → 79.1%
- GPT-5.4 + Codex CLI：76.0% → 77.3%
- Opus 4.6 + Claude Code：58.0% → 70.1%
- Gemini 3.1 Pro + Terminus 2：63.0% → 70.7%

当前 2.1 leaderboard 仍持续更新，因此结果必须锁定 benchmark version 与 submission date。

## What It Proves

它能更直接证明：

- terminal tool use
- environment interaction
- iterative execution
- error recovery
- multi-step task completion

## What It Does NOT Prove

不能直接证明：

- IDE UX
- repository-specific coding excellence
- frontend interaction
- product adoption
- real developer productivity
- enterprise ROI

## Limitations

官方 2.1 revision 本身暴露出 resource mismatch、network、security settings 等环境依赖问题；GitHub issues 中还出现 leaderboard traces 可见性等可复现性讨论。

因此，Terminal-Bench 很强，但并不是“纯 agent intelligence meter”。它同时测量：

> model × harness × runtime × tool policy × environment robustness。

## Relevance to Case 001

**High**。

它是本 Case 中最能直接观察 Agent 行为与 runtime interaction 的公开 benchmark 之一。

---

# 7. Benchmark 03 — SWE-bench Pro

## Benchmark Identity

- **Organization**：Scale AI research team / SWE-bench Pro
- **Publication**：2025-09
- **Scope**：long-horizon、enterprise-like software engineering
- **Dataset**：1,865 problems；覆盖 41 个 active repositories；包含 public、held-out 与 commercial splits

## What It Measures

它试图解决经典 SWE-bench 的一个核心问题：

> **真实企业级软件问题往往比单一 issue → patch 更长、更复杂、更跨文件。**

因此强调：

- long-horizon repo work
- complex dependencies
- larger engineering context
- business applications / developer tools / B2B services

## Evaluation Unit

实际 evaluation 是 **agent/model + scaffold** 联合结果，而不是纯 model benchmark。

## Task Design

- issue + repository state
- standardized Docker evaluation
- public / held-out / commercial splits
- 长任务执行
- patch correctness via tests

## Metrics

主要是 task resolution / patch correctness；不同 leaderboard 与 harness 会进一步报告成本、tokens 等。

## Methodology

一个重要设计是同时保留公开集与 held-out/commercial tasks，以降低公开数据完全暴露导致的过拟合风险。

## Results

该 benchmark 的核心价值并不在某个单独榜单数字，而在于它把问题从：

> “模型能否解决一个真实 issue？”

进一步推向：

> “Agent 能否在更长 horizon 下完成更接近企业代码库的问题？”

## What It Proves

能够更强地测试：

- repo reasoning
- complex multi-file modifications
- persistence
- longer task horizon
- real-world issue complexity

## What It Does NOT Prove

仍不能单独证明：

- product UX
- human-agent collaboration quality
- long-term project ownership
- team-level productivity
- enterprise governance

## Limitations

截至研究截点，官方 GitHub 仍保留对 leaderboard 问题和测试更新的记录，因此必须记录具体 benchmark revision。不同 agent scaffold 结果也不能直接横向等同。

## Relevance to Case 001

**High**。

它是对 SWE-bench 最重要的现实性补充之一，尤其用于验证 Phase 4 中关于“复杂 repo-level / enterprise SWE agent”能力的判断。

---

# 8. Benchmark 04 — ProjDevBench

## Benchmark Identity

- **Organization**：Academic research team
- **Publication**：2026-02
- **Scope**：End-to-end project development
- **Dataset**：20 programming problems / 8 categories

## What It Measures

它不是“修一个 issue”，而是给 agent 一个项目级需求，要求系统完成：

1. system architecture design
2. implementation
3. execution / testing
4. iterative refinement
5. code review

这是本阶段少数真正显式把：

```text
Planning → Construction → Execution → Verification → Refinement
```

放在同一任务中的 benchmark。

## Evaluation Unit

**Agent + Runtime**。

论文对多个 coding agents 做评测，而不是只给模型一个静态 prompt。

## Task Design

- multi-turn agent-environment interaction
- 平均约 138 turns/task
- 平均约 4.81M tokens/problem
- 最复杂任务可达约 2 小时
- OJ execution + LLM-assisted code review

## Metrics

- execution acceptance
- code review score
- weighted final score

## Methodology

它同时评价功能正确性与测试难以捕捉的代码质量/规范问题，这是非常重要的 methodological advance。

## Results

论文报告 overall acceptance rate 仅 27.38%。系统在基础功能和数据结构任务上相对更强，在复杂 system design、time-complexity optimization 与 resource management 上明显更弱。

## What It Proves

ProjDevBench 对本 Case 的最大价值在于，它揭示：

> **当任务从“issue repair”进一步扩展为“build a project”，当前 agent 的成功率仍显著下降。**

## What It Does NOT Prove

- 不代表所有商业 Coding Agent 的真实成功率；
- 只有 20 个任务；
- 主要为 C++；
- 不足以形成市场产品 ranking。

## Limitations

规模小、语言集中、任务构建成本高；论文自己指出扩展到更多任务困难。

## Relevance to Case 001

**High**。

它对“复杂端到端项目开发”这一 Phase 4 产品能力的解释力高于传统单轮 coding benchmark。

---

# 9. Benchmark 05 — SWE-Lancer

## Benchmark Identity

- **Organization**：OpenAI Preparedness / academic publication
- **Publication**：2025-02；ICML 2025 published version
- **Scope**：real freelance software engineering
- **Task scale**：1,400+ tasks；对应历史真实支付总额约 $1M

## What It Measures

两类任务：

1. **IC SWE tasks**：feature development、frontend work、performance improvements、bug fixes 等；
2. **SWE Manager tasks**：从多个技术实现方案中选出最优方案。

## Evaluation Unit

主要是 **model + SWE scaffold**，不是 commercial product。

因此必须写成：

> “某 model/scaffold 在 SWE-Lancer 上的表现”

而不能写成：

> “某 Coding Agent product 已具备相应商业软件工程能力”。

## Task Design

- real Upwork tasks
- codebase checkpoint
- issue / requirement
- end-to-end tests
- Playwright for frontend/browser-connected validation
- updated public version removes internet dependency during execution to reduce variance

## Metrics

- pass@1
- dollars earned / economic value
- manager decision agreement

其中“dollars earned”不是预测值，而是这些历史 freelance tasks 实际支付给人类工程师的金额尺度。

## Methodology

SWE-Lancer 的真实工作来源使它比纯 synthetic benchmark 更接近经济意义上的 Software Engineering。

但它仍主要评估 model/scaffold，并不能覆盖完整产品 UX、agent fleet、permissions、team workflow 等。

## Results

论文结论是：即使 frontier models，也无法解决大多数任务。其价值更多在于指出：

> 真实、经济上有价值的软件工程任务仍明显难于标准 coding benchmark。

## What It Proves

- software work complexity 比传统 benchmark 更高；
- “能修一个 issue”与“能交付一项有真实经济价值的软件工作”之间存在明显距离。

## What It Does NOT Prove

- product superiority
- enterprise adoption
- end-user satisfaction
- full autonomy in an unrestricted environment

## Limitations

公开 evaluation split 小于原始任务池；不同执行设置和数据更新版本也必须单独标记。

## Relevance to Case 001

**High**。

它是连接“Benchmark capability”与“real economic software work”的重要桥梁。

---

# 10. Benchmark 06 — Kotlin Benchmark for AI Coding Agents

## Benchmark Identity

- **Organization**：JetBrains
- **Release**：2026-07
- **Scope**：real-world Kotlin repository tasks
- **Dataset**：105 engineering tasks

## What It Measures

它明确强调：

> **不是 Kotlin syntax / language understanding，而是 coding agent 在真实 Kotlin 项目中从 issue 到 validated patch 的能力。**

## Evaluation Unit

**Agent + environment**。

JetBrains 发布的示例结果直接以 Claude Code、Junie、Codex 等 agent/model setups 展示。

## Task Design

- active open-source repositories
- issue description
- repository navigation
- patch generation
- containerized verification
- success requires passing required tests

## Metrics

Resolution rate。

首轮公开结果：

- Claude Code + Opus 4.7 xhigh：90/105 = 85.71%
- Junie + Opus 4.7 max：81.9%
- Codex + GPT-5.5 xhigh：81.9%

这些分数是 **第一轮 public benchmark run**，不是永久性的 product ranking。

## Methodology

基于 SWE-bench / Multi-SWE-bench infrastructure，数据与 test harness 均公开。

## What It Proves

它对“真实 repository issue resolution”的解释力较强，并提供了多语言生态的重要校准。

## What It Does NOT Prove

- 不代表多语言通用能力；
- 不代表完整 end-to-end software delivery；
- 不代表 UX / team productivity；
- 不代表所有 Kotlin codebase。

## Limitations

- Kotlin-only；
- 105 tasks；
- first iteration；
- 官方自己计划未来增加 Android / Kotlin Multiplatform、更丰富 metrics、cost / performance / maintainability 等指标。

## Relevance to Case 001

**High**。

它说明行业正在从“通用 model benchmark”转向“特定语言 + agent + real repository”评价。

---

# 11. Benchmark 07 — Long-Horizon-Terminal-Bench

## Benchmark Identity

- **Publication**：2026-07
- **Scope**：long-horizon terminal agents
- **Task count**：46
- **Domains**：software engineering、experiment reproduction、multimodal analysis、interactive games、scientific computing 等

## What It Measures

其核心创新不是更多任务，而是更长 horizon + dense intermediate grading：

```text
Task
 ↓
Subtask 1
 ↓
Subtask 2
 ↓
Subtask 3
 ↓
...
 ↓
Final outcome
```

这允许研究者观察部分进展，而不只是最终 binary pass/fail。

## Evaluation Unit

**Agent + runtime**。

## Task Design

- terminal-style execution
- multi-step interaction
- fine-grained graded subtasks
- long-horizon completion

## Metrics

- dense subtask reward
- final outcome
- configurable reward thresholds

## What It Proves

它开始回答传统 Agent benchmark 长期欠缺的问题：

> **Agent 在非常长的 execution chain 中，到底是在什么时候、以什么方式失败。**

## What It Does NOT Prove

- 不是纯软件工程 benchmark；
- 46 tasks 较小；
- 不适合直接对 AI Coding Agent 产品做市场排名。

## Limitations

mixed-domain、样本量小、仍处于早期研究阶段。

## Relevance to Case 001

**Medium–High**。

对“long-running autonomy”解释力高，但对具体 Coding Product 的 domain validity 低于 SWE-bench Pro / ProjDevBench。

---

# 12. Benchmark 08 — DevBench / DevEval

## Benchmark Identity

- **Organization**：OpenCompass / academic research
- **Publication**：2024 paper; COLING 2025
- **Scope**：full software development lifecycle

## What It Measures

覆盖：

- software design
- environment setup
- implementation
- acceptance testing
- unit testing

数据包括 22 个 repositories、4 类语言：Python、C/C++、Java、JavaScript。

## Evaluation Unit

主要是 **model + prompt / baseline agent system**，因此比现代 Agent Benchmark 更接近“model capability across lifecycle”。

## Task Design

作者提供自动评测 suite，也提供基于 ChatDev 的 baseline agent。

## Metrics

- Pass@k
- implementation test performance
- code coverage
- software design LLM-as-a-judge

## Results

历史结果显示 GPT-4-class models 在环境搭建、实现等部分任务仍有明显失败，说明跨生命周期的任务比单一 coding question 更难。

## What It Proves

可以证明：

> “software development ≠ code generation”

设计、环境与测试也会成为模型瓶颈。

## What It Does NOT Prove

- 不足以评价 2026 commercial coding-agent products；
- agent runtime autonomy 较弱；
- 数据和模型版本较旧。

## Limitations

任务规模有限、LLM-judge 成分明显、模型年代偏早。

## Relevance to Case 001

**Medium**。

它更适合作为方法史上的重要桥梁，帮助解释行业为何从 model-level coding benchmark 继续演进到 agent-level benchmark。

---

# 13. Independent Evidence

## 13.1 METR — SWE-bench Automated Grader vs Maintainer Review

### Fact

2026-03-10，METR 对来自 3 个 SWE-bench Verified repositories 的 296 个 AI-generated PR 进行 maintainer review，并与 47 个真实人类 merged PR 的 golden baseline 比较。

### Evidence

- 自动 grader 的通过率平均比 maintainer merge decision 高约 24.2 个百分点；
- 约一半的 automated-pass PR 不会直接被 maintainer merge；
- 常见拒绝原因包括 code quality、breaking other code、core functionality 等。

### Analysis

这是本 Phase 最重要的 independent evidence 之一，因为它没有否定 SWE-bench，而是说明：

> **“测试通过”只是“可被真实工程团队接受”的必要条件之一，而非充分条件。**

### Relevance

**Very High**。

它直接改变了我们读取 SWE-bench leaderboard 的方式。

---

## 13.2 METR — Developer Productivity RCT / methodology updates

### Fact

METR 2025 RCT 研究发现，在早期 2025 AI 条件下，经验丰富的 open-source developers 完成任务反而慢约 19%。

但 2026-02 的方法更新指出：随着开发者对 AI 的依赖增加，研究出现严重 selection effects，因此 later-study data 不能被可靠地解释为当前 AI productivity 的无偏估计。

### Analysis

同一研究机构的变化本身就说明：

> **Developer productivity 是一个明显比 benchmark score 更困难的 measurement problem。**

不能把任何单次 uplift 数字直接当成产品 ROI。

### Relevance

**Very High**，用于证明 Benchmark Result ≠ Productivity。

---

## 13.3 METR — Transcript-based coding-agent analysis

2026-02，METR 对 7 名技术工作人员在 2026-01 生成的 5,305 条 Claude Code transcripts 做探索性分析，得到的任务 time-savings factor 约为 1.5×–13×。

但 METR 明确称这一数字只是 **soft upper bound**，因为：

- task substitution
- task selection effects
- workers only use AI where helpful
- saved time ≠ equivalent value

因此该研究不能用来证明“Claude Code 让工程师生产力提升 13×”，恰恰相反，它提醒我们区分：

```text
Task Time Saved
≠
Productivity
≠
Value Created
```

Relevance：**High**。

---

## 13.4 Academic longitudinal study — AI coding assistants

2026-05，Annie Vella 与 Kelly Blincoe 的 longitudinal mixed-method study 跟踪 95 名匹配参与者，并报告：

- 82% 报告写代码所需时间减少；
- 84% 在两个时间点都报告 productivity improvement；
- 同时，报告 developer experience 至少一个维度变差的人从 14% 增至 27%；
- 工作重心从 creation 向 verification 转移；
- 作者提出“supervisory engineering work”。

### Analysis

这与 benchmark 的关系非常重要：

> Benchmark 看到的是“机器是否成功完成”；长期真实工作看到的可能是“机器完成得更多，但人类监督、验证、纠错也更多”。

因此，verification burden 本身就是 Agent Product 的真实能力指标，而传统 benchmark 往往没有直接测量它。

Relevance：**High**。

---

## 13.5 BNY Mellon / Carnegie Mellon-oriented productivity measurement study

2026-02 的 `Beyond the Commit` 对 BNY Mellon 2,989 名开发者进行了调查，并进行了 11 次深度访谈，结论之一是：developer productivity 需要多维度衡量，尤其应纳入长期技术能力、ownership 等因素。

### Analysis

这进一步证明：

```text
Benchmark success
      ≠
Developer productivity
      ≠
Long-term engineering health
```

Relevance：**Medium–High**。

---

## 13.6 Stack Overflow 2025 Developer Survey

Stack Overflow 2025 调查覆盖约 49,000 名开发者。

重要发现：

- 84% 使用或计划使用 AI tools；
- 但 46% 不信任 AI output accuracy，而只有 33% trust；
- 66% 最大的 frustration 是“almost right, but not quite”；
- 52% 开发者认为 AI tools/agents 对 productivity 有正面影响；
- 约 70% agent users 同意 agents 减少了某些 development tasks 的耗时；
- 只有 17% 认为 agents 改善了 team collaboration；
- 87% 对 agent accuracy 有担忧，81% 对 security/privacy 有担忧。

### Analysis

这类 evidence 不能衡量模型能力，但能补齐 Benchmark 完全没有覆盖的：

- trust
- user-perceived productivity
- collaboration
- security concerns
- adoption resistance

Relevance：**High**，但独立于 benchmark leaderboard。

---

# 14. Model-level vs Agent-level vs Product-level Analysis

## 14.1 Model-level evidence still dominates

大量历史 coding benchmarks，包括：

- HumanEval
- MBPP
- APPS
- Aider Polyglot
- DevBench 的很多 setup

本质上仍回答：

> **模型会不会写出正确代码？**

它们对模型选择很有价值，却不能回答：

> **模型能否作为一个 autonomous software engineer 稳定工作？**

## 14.2 Repo-level benchmarks are intermediate layer

SWE-bench、SWE-bench Verified、Kotlin Benchmark、SWE-bench Pro 开始测试：

```text
Repository context
 +
Issue understanding
 +
Code modification
 +
Test validation
```

这已经比纯 model benchmark 更接近 Agent，但仍然偏向：

> **issue → patch**。

## 14.3 Agent/runtime benchmarks are a newer layer

Terminal-Bench、ProjDevBench、Long-Horizon-Terminal-Bench 更接近：

```text
Plan
 ↓
Tool Use
 ↓
Environment Interaction
 ↓
Execute
 ↓
Observe
 ↓
Verify
 ↓
Repair
 ↓
Finish
```

这才开始真正测“Agent”而不是“code generator”。

## 14.4 Product-level benchmark remains missing

即使 Terminal-Bench 已经是 agent-level，也仍然通常不能测到：

- UX
- interruption/replanning quality
- permission model
- workspace integration
- enterprise governance
- collaboration
- GitHub / Slack / ticket workflow integration
- long-term memory quality
- onboarding / learning curve
- total cost of ownership

因此：

> **当前没有一个被行业广泛认可的 single benchmark，可以完整代表 AI Coding Agent Product Capability。**

---

# 15. Capability Coverage Matrix

| Capability Dimension | SWE-bench | Terminal-Bench | SWE-bench Pro | ProjDevBench | SWE-Lancer | Kotlin Benchmark | Long-Horizon-Terminal-Bench | DevBench |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Context / Repo Understanding | ✓ | △ | ✓ | ✓ | ✓ | ✓ | △ | ✓ |
| Planning | △ | ✓ | ✓ | **✓** | △ | △ | **✓** | △ |
| Tool Use | △ | **✓** | ✓ | **✓** | △ | ✓ | **✓** | △ |
| Execution | ✓ | **✓** | ✓ | **✓** | ✓ | ✓ | **✓** | ✓ |
| Verification | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | ✓ | **✓** |
| Repair / Iteration | △ | **✓** | **✓** | **✓** | △ | △ | **✓** | △ |
| Long-horizon | △ | ✓ | **✓** | **✓** | ✓ | △ | **✓** | △ |
| End-to-end project construction | ✗ | △ | △ | **✓** | ✓ | ✗ | △ | ✓ |
| Maintainer / human quality review | ✗ | ✗ | ✗ | **✓** | ✗ | ✗ | ✗ | △ |
| Economic realism | ✗ | ✗ | △ | ✗ | **✓** | ✗ | ✗ | ✗ |
| Product UX | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Developer productivity | ✗ | ✗ | ✗ | ✗ | △ | ✗ | ✗ | ✗ |
| Team collaboration | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Enterprise ROI / TCO | ✗ | ✗ | △ | ✗ | △ | ✗ | ✗ | ✗ |

Legend：**✓ = meaningful coverage；△ = partial / indirect；✗ = not measured**。

---

# 16. Why Benchmark Results Diverge

Benchmark 间出现巨大结果差异并不异常，因为它们测的不是同一个 latent variable。

## 16.1 Task distribution

```text
Function generation
vs
Issue resolution
vs
Project construction
vs
Terminal execution
```

难度与技能结构完全不同。

## 16.2 Harness

同一模型在：

- minimal bash agent
- SWE-agent style harness
- Claude Code
- Codex CLI
- Terminus

上可以产生显著不同结果。

因此 leaderboard 上的 agent score 包含 harness contribution。

## 16.3 Runtime / Environment

网络、CPU、GPU、timeouts、security policy、base image、package availability 都会影响结果。

Terminal-Bench 2.1 专门修复 resource/network/security mismatch，就是明确案例。

## 16.4 Test quality

自动测试如果：

- 太宽松 → false positives
- 太严格 → false negatives
- 覆盖不足 → reward hacking

都会扭曲 benchmark signal。

## 16.5 Static-data contamination

SWE-bench、Aider 等公开数据容易被训练语料覆盖。Benchmark 越公开、越成熟，越需要考虑 contamination / memorization。

## 16.6 Retry / budget policy

一个 agent 是否允许：

- 1 次尝试
- 5 次尝试
- 无限时间
- 并行 subagents
- 自主搜索

会直接改变结果。

## 16.7 Metric definition

“通过一次测试”与：

- 代码质量
- maintainability
- user satisfaction
- mergeability
- economic value

并不是同一指标。

---

# 17. What Benchmark Evidence Supports from Phase 4

Phase 4 的产品研究已经把 Top 10 描述为：

- repo-level coding agents
- terminal / environment operating agents
- long-running/background agents
- multi-agent / subagent systems
- cloud execution / sandbox
- workflow agents

Phase 5 可以支持其中一部分：

## Strongly supported

### 17.1 Repo-level issue resolution

SWE-bench / SWE-bench Verified / Kotlin Benchmark / SWE-bench Pro 对此有直接支撑。

### 17.2 Terminal / environment interaction

Terminal-Bench 明确提供直接证据。

### 17.3 Long-horizon execution

SWE-bench Pro、ProjDevBench、Long-Horizon-Terminal-Bench 提供更直接的支持。

### 17.4 Iterative verification / repair

Terminal-Bench、ProjDevBench、部分 SWE-bench setup 提供证据。

### 17.5 Agent + runtime contribution

Terminal-Bench 的 agent/model leaderboard 以及 ProjDevBench 的结果说明：harness/runtime 不是可以忽略的变量。

---

# 18. What Benchmark Evidence Cannot Validate from Phase 4

以下 Phase 4 产品判断不能靠现有 benchmark 单独验证：

- Claude Code / Codex / Cursor 哪个 UX 最好；
- 哪个产品更适合个人开发者；
- 哪个产品更适合企业采购；
- MCP / Skills / Memory 的真实长期价值；
- interruption / steering 体验；
- security / permissions 是否足够安全；
- team collaboration；
- developer adoption；
- enterprise ROI / TCO；
- pricing / economics；
- customer support；
- product reliability at market scale。

这些必须使用 Phase 2/4 产品证据和 Independent Evidence，而不能通过 benchmark score 推导。

---

# 19. Evaluation Gap

## 19.1 The central gap

截至 2026-08，最明显的 Evaluation Gap 是：

> **AI Coding Agent Products 已经从“代码生成工具”演进为能操作环境的 Agent，但公开 benchmark 体系仍主要围绕“模型/patch 是否正确”构建。**

这个 gap 并不是说“没有 Agent benchmark”。Terminal-Bench、ProjDevBench、SWE-bench Pro、Kotlin Benchmark 等已经明显向 Agent-level 前进。

真正的问题是：

```text
Product reality
= Agent + Harness + Runtime + Context + Memory + Tools + Workflow + Human oversight

Benchmark reality
= usually one task + one environment + one score
```

## 19.2 Missing dimensions

### A. Product UX

Benchmark 很少测试：

- agent steering
- interruptions
- approvals
- context recovery
- session management
- artifact review

### B. Workflow integration

现实产品越来越进入：

```text
Issue
→ Agent
→ Branch
→ Test
→ PR
→ Review
→ Merge
→ Deploy
```

而 benchmark 多数只测中间一个环节。

### C. Persistent memory

长期项目中真正重要的是 agent 是否持续理解：

- project conventions
- prior decisions
- architecture constraints
- user preferences

这一层目前公开 benchmark 很少系统评估。

### D. Human-agent collaboration

METR maintainer study 已经证明：自动测试通过与真实人类接受之间有显著 gap。

因此 future evaluation 应包含：

```text
Agent completion
 +
Human review
 +
Iteration after feedback
```

而不是只看第一次 patch。

### E. Cost / latency / throughput

真实产品的竞争不仅是：

> “做不做得到？”

还包括：

- 成本
- 延迟
- token efficiency
- concurrency
- throughput
- developer attention cost

### F. Long-term engineering quality

当前 benchmark 很少真正回答：

> **Agent 连续工作数周后，代码库是否更健康？**

这涉及 maintainability、technical debt、regression、architecture consistency。

---

# 20. Core Research Questions — Final Answers

## Q1. 当前主流 Benchmark 主要在测什么？

### Judgment

**仍以 Model capability / Model+Scaffold capability 为主，但 Agent-level benchmark 正快速增长。**

可粗略理解为：

```text
传统 benchmark
      ↓
Model-heavy

SWE-bench family
      ↓
Repo-level / scaffold-dependent

Terminal-Bench / ProjDevBench
      ↓
Agent + runtime

Product capability
      ↓
仍缺乏统一 benchmark
```

因此，“行业 benchmark 已经全面转向 Agent”并不成立；更准确的是：

> **行业正处于 Model-centric → Agent-centric 的过渡期。**

---

## Q2. 是否真正覆盖 Context + Planning + Tool Use + Execution + Verification + Repair？

### Judgment

**没有一个主流公开 benchmark 完整、稳定、无争议地覆盖全部六项。**

最接近的组合是：

- ProjDevBench：planning + execution + review + iterative refinement
- Terminal-Bench：tool use + execution + environment interaction
- SWE-bench Pro：long-horizon repo work
- SWE-bench / Kotlin Benchmark：repo context + patch + verification
- Long-Horizon-Terminal-Bench：extended horizon + intermediate progress

因此需要组合解读，而不是寻找一个“全能 benchmark”。

---

## Q3. 哪些最接近真实 Software Engineering Agent？

### Judgment

按 **agentic workflow coverage** 而不是 leaderboard 分数排序，本阶段认为最有解释力的是：

1. **ProjDevBench** — 最接近完整 end-to-end project development
2. **Terminal-Bench 2.1** — 最接近 environment-operating agent
3. **SWE-bench Pro** — 最接近长 horizon repo-level enterprise SWE
4. **SWE-bench Verified / Kotlin Benchmark** — 最成熟的 repo-level issue-resolution family
5. **Long-Horizon-Terminal-Bench** — 对极长 horizon 的补充证据
6. **SWE-Lancer** — 对真实经济价值软件工作的现实性补充

这里不是一个“能力排名”，而是 **explanatory power ranking**。

---

## Q4. 哪些仍然主要偏 Model capability？

主要包括：

- HumanEval
- MBPP
- APPS
- Aider Polyglot
- DevBench 的 model-centered setup
- 以及任何只给静态 prompt / code context 并直接测 code correctness 的 benchmark

它们很适合测：

> “这个模型会不会写代码？”

但不适合单独回答：

> “这个产品是不是优秀的 Coding Agent？”

---

## Q5. 为什么不同 Benchmark 结论会不同？

### Judgment

因为 benchmark 不是在测一个“绝对 coding intelligence”，而是在测：

```text
Capability
×
Task distribution
×
Prompt
×
Harness
×
Tools
×
Runtime
×
Budget
×
Tests
```

所以：

> **Benchmark disagreement is often methodological disagreement, not necessarily measurement failure.**

---

## Q6. Benchmark 对 Phase 4 哪些判断形成支持？

支持最明显的是：

- Top 10 中头部产品确实已经超越简单 autocomplete；
- repo-level issue resolution 已成为真实能力基线；
- tool use + execution + verification 是 agent capability 的核心组成；
- long-running / environment-operating agents 正在成为新的能力边界；
- harness/runtime 本身会显著影响最终表现。

这与 Phase 4 对 Claude Code、Codex、Cursor、Devin、Antigravity、OpenCode、Qoder、Factory 等产品的 agentic characterization 是一致的。

---

## Q7. 哪些 Phase 4 判断无法由 Benchmark 验证？

主要是：

- Product UX
- workflow fit
- human-agent collaboration
- pricing / economics
- adoption
- enterprise ROI
- product reliability
- memory / skills / MCP 的长期组织价值

这些需要继续依赖 Phase 2 / 4 evidence 与 independent field evidence。

---

## Q8. 当前是否存在明显 Evaluation Gap？

### Judgment

**是，而且是结构性的。**

但应更精确地表述为：

> **Evaluation Gap = Product complexity grows faster than public evaluation coverage.**

不是“行业完全没有 Agent benchmark”，而是：

> **Agent benchmark 已经出现，但 Product-level / Workflow-level / Human-in-the-loop evaluation 仍明显落后。**

---

# 21. Implications for Phase 4 Product Interpretation

Phase 4 的 Product Capability 不应继续用单一 benchmark score 排序，而应采用：

```text
Product claim
    ↓
Observed product workflow
    ↓
Relevant benchmark evidence
    ↓
Independent evidence
    ↓
Confidence
```

例如：

### Claude Code

SWE-bench / Kotlin Benchmark / Terminal-Bench 可以支持其 repo-level + terminal agent 能力；METR transcript 与 maintainer studies 则帮助理解其实际工作中“高 autonomous execution + high supervision burden”的两面性。

### Codex

Terminal-Bench 对其 agent+runtime 能力提供直接证据，但不能由 benchmark score 单独推导其 cross-surface UX 或 enterprise workflow superiority。

### Cursor

Terminal/repo benchmark 能支持其 agentic coding capability；但 AI-native IDE UX 与 cloud/background workflow 仍需要产品证据。

### Devin / Factory / Antigravity / Replit Agent / Qoder / OpenCode

公开 benchmark 覆盖不完整，尤其是产品独有 workflow；因此更应使用 benchmark 作为 supporting evidence，而不能要求每个产品都有一套同构 leaderboard 才允许判断。

---

# 22. Phase 5 Judgment on Top 10

本阶段没有发现足以构成 **versioned correction** 的重大事实错误，因此：

> **Phase 3 Top 10 保持不变。**

尤其没有发现“某个 benchmark 排名反转，因此必须把 Top 10 改成 benchmark Top 10”的理由。

原因：

1. Charter 定义的 Top 10 是 Market Leaders / Representative Leaders，而不是 benchmark winners；
2. benchmark 测量层级与 market/product importance 不相同；
3. 多个产品没有对称的公开 benchmark coverage；
4. leaderboard 不能替代市场 adoption、workflow innovation、ecosystem、momentum 等研究维度。

因此 Phase 5 的正确作用是：

> **验证、补充、限制 Phase 4 product claims，而不是重写 Phase 3 selection。**

---

# 23. Phase 5 Exit Criteria

根据 Charter，本阶段完成情况如下：

| Exit criterion | Status | Evidence |
|---|---|---|
| Build benchmark candidate universe | **PASS** | 本文件 §3 |
| Select relevant benchmarks with explicit rationale | **PASS** | 本文件 §3 |
| Analyze benchmark methodology | **PASS** | 本文件 §5–12 |
| Distinguish Model / Agent / Runtime / Product | **PASS** | 本文件 §2、§14 |
| Build unified benchmark matrix | **PASS** | 本文件 §4 |
| Analyze independent evidence | **PASS** | 本文件 §13 |
| Identify what benchmarks prove / do not prove | **PASS** | 本文件 §5–12、§20 |
| Identify Evaluation Gap | **PASS** | 本文件 §19 |
| Cross-check against Phase 4 | **PASS** | 本文件 §17–22 |
| Preserve Top 10 unless major factual correction is found | **PASS** | 本文件 §22 |
| No Phase 6–8 artifact creation | **PASS** | 仅新增 `05-benchmarks.md` |
| Record dates / versions / limitations / Unknowns | **PASS** | Matrix + benchmark sections |

### Overall Exit Judgment

> **Phase 5 satisfies the Charter exit requirements for Public Benchmark & Independent Evidence Analysis.**

---

# 24. Source Ledger

## Tier 1 — Benchmark / Primary

1. SWE-bench official GitHub / README  
   https://github.com/SWE-bench/SWE-bench
2. SWE-bench Verified official page  
   https://www.swebench.com/verified.html
3. OpenAI — Introducing SWE-bench Verified  
   https://openai.com/index/introducing-swe-bench-verified/
4. Terminal-Bench 2.1 official GitHub  
   https://github.com/harbor-framework/terminal-bench-2-1
5. Terminal-Bench 2.1 official release note  
   https://www.tbench.ai/news/terminal-bench-2-1
6. Terminal-Bench 2.1 leaderboard  
   https://www.tbench.ai/leaderboard/terminal-bench/2.1
7. SWE-bench Pro paper  
   https://arxiv.org/abs/2509.16941
8. SWE-bench Pro repository  
   https://github.com/scaleapi/SWE-bench_Pro-os
9. ProjDevBench paper  
   https://arxiv.org/abs/2602.01655
10. DevBench / DevEval repository  
    https://github.com/open-compass/DevEval
11. DevBench / DevEval paper  
    https://aclanthology.org/2025.coling-main.502/
12. SWE-Lancer official OpenAI publication  
    https://openai.com/index/swe-lancer/
13. SWE-Lancer PMLR publication  
    https://proceedings.mlr.press/v267/miserendino25a.html
14. SWE-Lancer updated repository / evaluation artifacts  
    https://github.com/openai/frontier-evals/tree/main/project/swelancer
15. Kotlin Benchmark — JetBrains official announcement  
    https://blog.jetbrains.com/kotlin/2026/07/introducing-the-kotlin-benchmark-evaluate-ai-coding-agents-on-real-world-kotlin-tasks/
16. SWE-bench Multilingual  
    https://www.swebench.com/multilingual.html
17. BrowserGym / WebArena adjacent evidence  
    https://github.com/ServiceNow/BrowserGym
    https://github.com/web-arena-x/webarena

## Tier 2 — Independent / Research

18. METR — Many SWE-bench-Passing PRs Would Not Be Merged into Main  
    https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
19. METR — Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity  
    https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
20. METR — We are Changing our Developer Productivity Experiment Design  
    https://metr.org/blog/2026-02-24-uplift-update/
21. METR — Analyzing coding agent transcripts to upper bound productivity gains from AI agents  
    https://metr.org/notes/2026-02-17-exploratory-transcript-analysis-for-estimating-time-savings-from-coding-agents/
22. METR Research index — HCAST / MirrorCode / 2026 work  
    https://metr.org/research/
23. The Impact of AI Coding Assistants on Software Engineering: A Longitudinal Study  
    https://arxiv.org/abs/2605.23135
24. Beyond the Commit: Developer Perspectives on Productivity with AI Coding Assistants  
    https://arxiv.org/abs/2602.03593
25. Stack Overflow 2025 AI / Developer Survey  
    https://survey.stackoverflow.co/2025/ai
26. Stack Overflow 2025 survey press release  
    https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/

---

# 25. Final Research Judgment

本阶段最重要的结论不是“哪个 benchmark 分最高”，而是：

> **2026 年 AI Coding Agent 的能力已经明显超出单纯 code generation，但公开 evaluation 体系仍在从 Model-centric 向 Agent-centric 迁移。**

真正具有解释力的研究框架应该是：

```text
Model capability
      +
Agent harness
      +
Tools / Runtime
      +
Long-horizon execution
      +
Verification / Repair
      +
Human review
      +
Developer productivity
      +
Product workflow
```

没有任何单一 leaderboard 可以覆盖这整个 stack。

因此对本 Case 最稳健的判断是：

> **Benchmark 能够验证 AI Coding Agent 的局部能力边界，但不能替代 Product Research。**

并且：

> **Evaluation Gap 是当前 AI Coding Agent 行业的重要结构性问题：产品层已经进入 agentic workflow，而公开评价仍主要围绕 task-level success 建模。**

这也是 Phase 5 对整个 Case 001 最重要的新增认知资产。 

## Research Status

**Phase 5 complete.**

Top 10 unchanged. No versioned correction triggered.
