# Research Charter

# Case 001 — 2026 AI Coding Agent Landscape

> Research Charter v1.1
>
> Research date: August 2026
>
> Status: Approved for execution

---

## 1. Research Mission

### 1.1 Research purpose

本 Case 的目标不是简单制作一份“AI Coding Agent 工具排行榜”，而是通过一次真实、完整的行业研究，理解 2026 年 AI Coding Agent 市场正在发生什么，并建立一套以后可以迁移到其他 Research Case 的标准研究方法。

本研究同时承担两个目标：

1. **行业认知目标**：理解 2026 年全球 AI Coding Agent 的主要产品、市场格局、技术路线与发展趋势。
2. **Research OS 实验目标**：完整实践从问题定义、证据收集、分析、判断到交付的 Research Workflow，为后续 Human + AI、Research Agent 和 Evaluation 阶段提供真实案例。

### 1.2 First Principle

> **本研究不是比较哪个 AI Coding Agent 的功能更多，而是研究：哪些产品正在重新定义 Software Engineering Workflow，以及这种变化正在如何重塑 Coding 工作。**

### 1.3 Core Research Question

> **截至 2026 年 8 月，全球 AI Coding Agent 市场由哪些 Market Leaders / Representative Leaders 构成？它们分别代表怎样的产品形态、Agent 架构和 Software Engineering Workflow？哪些产品正在形成主流，哪些产品正在定义下一代方向？**

### 1.4 Supporting Questions

本研究需要回答以下问题：

1. **Market**：哪些 AI Coding Agent 具有真实的市场重要性？
2. **Product**：主要产品的产品形态、定位和能力有什么差异？
3. **Agent**：它们如何处理 Context、Planning、Reasoning、Tool Use、Execution、Verification、Memory 等 Agent Workflow？
4. **Landscape**：2026 年 AI Coding Agent 正形成哪些主要产品与技术路线？
5. **Evidence**：哪些判断有可靠的一手资料、市场数据、公开 Benchmark 或第三方证据支撑？
6. **Decision**：哪些产品最值得持续关注和深入研究？

---

# 2. Research Scope, Definitions & Taxonomy

## 2.1 AI Coding Agent Definition

本研究中的 **AI Coding Agent** 定义为：

> 能够接收相对高层的软件开发目标，并通过自主或半自主的多步骤推理、代码修改、工具调用、执行与验证，完成部分 Software Engineering Task 的 AI 产品或产品家族。

核心判断标准是 **Agentic Software Engineering Capability**，而不是是否具有 AI Chat 或代码生成能力。

### 典型 Agent Loop

```text
Human Intent
    ↓
Planning
    ↓
Context Gathering
    ↓
Reasoning
    ↓
Tool Selection
    ↓
Code / Environment Modification
    ↓
Execution
    ↓
Verification
    ↓
Iteration / Repair
    ↓
Software Artifact
```

---

## 2.2 Agentic Maturity Continuum

研究采用连续谱，而不是僵硬地把产品分成互斥类别：

```text
Coding Assistant
      ↓
Agentic Coding Tool
      ↓
Software Engineering Agent
      ↓
Autonomous Software Engineering Agent
```

本研究重点覆盖后面三个层级。

传统 Coding Assistant 只有在已经显著向 Agentic Coding 转型的情况下才进入候选池。

---

## 2.3 Research Unit: Product / Product Family

本研究以 **AI Coding Agent Product / Product Family** 为研究单位，而不是以公司、模型、客户端或单一 Feature 为单位。

统一采用：

```text
Company
   ↓
Product Family
   ↓
Product Surface
   ↓
Agent Capability
```

这样可以避免同一个产品家族因为同时提供 CLI、IDE、Desktop、Cloud 等多个入口而重复占据榜单名额。

---

## 2.4 Product Surface Taxonomy

| Product Surface | Definition | Scope |
|---|---|---|
| CLI | Terminal / Shell 中运行的 Coding Agent | Included |
| IDE | 独立 AI Native IDE 或深度集成的 IDE Agent | Included |
| Desktop | 独立桌面 AI Coding Agent | Included |
| Cloud | 主要在云端执行 Coding Task 的 Agent | Included |
| Plugin | 依附于第三方 IDE 的插件/扩展 | Plugin-only excluded from main ranking |

### Plugin Rule

> **Plugin-only 产品不进入主榜。**

但如果一个产品同时拥有独立 CLI、IDE、Desktop 或 Cloud Agent，即使同时提供 Plugin，其 Product / Product Family 仍然可以进入研究范围。

Plugin 在这种情况下作为一个 Product Surface 进行分析，而不是作为独立研究对象。

---

## 2.5 Explicit Exclusions

以下对象不作为本 Case 的核心研究对象：

### A. Pure Models

例如 GPT、Claude、Gemini、Qwen 等基础模型。

它们作为 **Underlying Model / Model Layer** 被研究，但不作为独立 Coding Agent 产品排名。

### B. Pure Code Completion Tools

主要价值仍然是 Autocomplete / Inline Completion、单轮代码生成或代码问答，且没有足够成熟 Agent Workflow 的产品，不进入核心候选池。

### C. General-purpose Agents

非 Software Development / Coding / Software Engineering 为核心场景的通用 Agent，不自动归入 AI Coding Agent。

### D. Software Engineering Infrastructure

CI/CD、Git Hosting、Issue Tracker、Observability 等开发基础设施不作为 Coding Agent 研究对象，除非其本身已经提供独立且成熟的 AI Coding Agent。

---

## 2.6 Product vs Feature Rule

本研究研究的是产品，而不是产品内部的单一 Feature。

例如 Background Agent、Cloud Agent、Code Review Agent、SWE Agent 等，如果只是同一产品中的能力，则归属于同一个 Product / Product Family。

只有当其形成独立产品或独立产品家族时，才作为独立研究对象处理。

---

# 3. Research Population: Candidate Universe

## 3.1 Candidate Universe First

不得直接从“TOP10”开始研究。

首先建立尽可能完整的 **AI Coding Agent Candidate Universe**，再通过统一方法进行筛选。

候选池原则上覆盖：

- 全球主要 AI Coding Agent
- 中国主要 AI Coding Agent
- CLI、IDE、Desktop、Cloud 等主要产品形态
- 商业闭源产品
- 重要开源产品
- 已形成明显市场影响力的产品
- 技术路线具有代表性的产品
- 快速增长、可能改变竞争格局的新兴产品

候选池规模不预设为最终数量，但应足以覆盖主要市场参与者。

---

## 3.2 Final Research Population

最终研究对象定义为：

> **10 个最值得深入研究、且能够代表 2026 年 AI Coding Agent 市场主要方向的 Market Leaders / Representative Leaders。**

因此：

> **TOP10 ≠ User Count Top 10**

而是：

> **Market Significance × Technology / Product Significance**

最终目标是选择能够解释 2026 年 AI Coding Agent 市场的代表性产品，而不是机械选择用户最多的十个产品。

---

# 4. Market Representation Principle

市场采用度必须纳入研究，因为真实用户规模、开发者采用率、使用率和生态规模会显著影响一个 Coding Agent 的现实价值与行业影响力。

同时必须避免：

> **High Adoption = Best Product**

本研究明确区分：

```text
Market Adoption
≠
Product Capability
≠
Technology Leadership
```

### Market Adoption 的意义

Market Adoption 用于回答：

> “这个产品在现实世界有多重要？”

可考虑：

- Developer Adoption
- User Base
- Active Users / Usage
- Market Share
- Enterprise Adoption
- Developer Surveys
- Repository / CLI Usage
- Ecosystem Size
- Community Size

由于不同市场数据的定义、样本和统计口径可能不同，任何单一数据源不得自动视为整个市场的真实排名。

---

# 5. Ranking & Selection Framework

## 5.1 Principle

本研究允许使用**多源综合排名**，不指定某一个外部榜单作为唯一权威排名。

研究排名的基本流程为：

```text
Multiple Market Sources
        +
Product / Technology Evidence
        +
Public Benchmarks
        +
Ecosystem / Strategic Evidence
        ↓
Cross-source Normalization
        ↓
Composite Assessment
        ↓
Research Judgment
        ↓
Final Top 10
```

最终排名是本研究基于证据形成的 **Research Ranking**，而不是声称存在一个绝对客观的“全球唯一正确排名”。

---

## 5.2 Proposed Composite Dimensions

候选产品的综合重要性初步采用以下五个维度：

| Dimension | Weight | Core Question |
|---|---:|---|
| Market Adoption | 30% | 有多少真实用户/开发者/企业在使用？ |
| Product / Agent Capability | 30% | Agent 实际能完成什么？ |
| Product / Workflow Innovation | 20% | 是否正在重新定义 Software Engineering Workflow？ |
| Ecosystem / Strategic Importance | 10% | 是否形成重要生态与战略影响？ |
| Momentum | 10% | 是否具有明显增长与发展势能？ |

这些权重作为 Charter 的**初始方法论设定**，在正式研究开始后，如果发现行业数据结构导致权重明显失真，可以进行版本化调整，但必须记录调整原因，不得在看到最终结果后为了迎合结论而反向修改权重。

---

## 5.3 Quantitative Score Is Not Automatic Selection

Composite Score 只用于辅助筛选和排序，不自动决定最终 TOP10。

最终流程为：

```text
Quantitative Evidence
        ↓
Composite Score
        ↓
Cross-source Review
        ↓
Research Judgment
        ↓
Final Research Selection
```

如果某产品市场规模较小，但具有显著技术创新或代表新的 Software Engineering Workflow，可以进入 TOP10；反之，一个用户规模很大的产品，如果技术/产品代表性不足，也不应仅凭用户规模自动获得研究名额。

任何偏离综合分数的最终选择，都必须记录明确的入选/落选理由与证据。

---

# 6. Market Ranking vs Capability Ranking

本研究不把所有维度压缩成一个“谁最好”的结论。

最终至少区分两种视角：

## 6.1 Market Landscape Ranking

回答：

> **2026 年哪些 AI Coding Agent 最具有市场重要性与代表性？**

主要依据：

- Adoption
- Usage
- User Base
- Enterprise Adoption
- Developer Survey
- Ecosystem
- Market Presence
- Momentum

最终形成：

> **2026 AI Coding Agent Market Leaders / Representative Leaders — Top 10**

---

## 6.2 Capability / Workflow View

回答：

> **哪些产品代表当前 AI Coding Agent 的先进能力和 Software Engineering Workflow？**

重点分析：

- Agent Autonomy
- Coding Quality
- Repository Understanding
- Context Management
- Planning
- Reasoning
- Tool Use
- Execution
- Testing
- Debugging
- Verification
- Memory
- MCP
- Skills
- Sandbox / Runtime
- Cloud Execution
- Workflow Integration

不强制将 Capability View 再压缩成一个具有绝对意义的“第二名次榜”。必要时使用 Capability Matrix、Category Leaders 或二维图进行表达。

---

# 7. Model Capability vs Agent Product Capability

这是本研究的基本原则：

> **必须严格区分 Model Capability 与 Agent Product Capability。**

统一采用：

```text
Underlying Model
        ↓
Agent Harness / Runtime
        ↓
Tools / Context / Memory / Execution
        ↓
Coding Agent Product
        ↓
Software Engineering Workflow
```

因此：

> **模型能力强 ≠ Coding Agent 产品能力强。**

研究某产品时必须尽可能区分：

1. Underlying Model
2. Agent / Harness
3. Tools
4. Runtime / Sandbox
5. Context System
6. Memory / Rules
7. Product UX
8. Workflow Integration

避免把模型 benchmark 的成绩直接当成产品 benchmark 的成绩。

---

# 8. Public Benchmark Policy

## 8.1 No Self-built Benchmark

本 Case **不自行设计、构建或运行 Standard Coding Agent Benchmark**。

原因：

- 会显著扩大研究范围
- 引入环境、Prompt、模型版本、Agent Harness 等额外变量
- 自建 Benchmark 的权威性和可复现性不足
- 本 Case 的核心目标是行业研究与 Research Workflow，而不是建立新的 Benchmark

---

## 8.2 Public Benchmark as Supporting Evidence

允许并鼓励引用公开、行业主流的 Coding / SWE / Agent Benchmark 结果作为研究证据。

Benchmark 的定位是：

> **Supporting Evidence，而不是唯一 Ranking Authority。**

对于每个重要 Benchmark，记录：

```text
Benchmark Name
Organization
Publication / Evaluation Date
Task Type
Metric
Models / Agents Covered
Methodology
Result
Known Limitations
Relevance to This Research
```

必须判断：

> **这个 Benchmark 到底能够证明什么？**

不得简单将某个 benchmark 的第一名直接等同于“最佳 AI Coding Agent”。

---

## 8.3 Model Benchmark Caution

如果 Benchmark 实际测量的是基础模型，而不是完整 Coding Agent，则必须明确标注：

> **Model-level evidence**

不得直接作为：

> **Agent Product-level evidence**

---

# 9. Deep Research Framework for Each Product

最终入选 TOP10 后，所有产品使用统一研究模板，以保证横向可比性。

## 9.1 Product Identity

- Company
- Product / Product Family
- Launch / Major Milestones
- Target Users
- Primary Markets
- Product Surfaces
- Business Model
- Current Status as of August 2026

## 9.2 Product Positioning

回答：

- 它到底是什么？
- 解决什么问题？
- 核心用户是谁？
- 与传统 IDE / Coding Assistant 的根本区别是什么？
- 它试图改变哪一个 Software Engineering Workflow？

## 9.3 Product Architecture

重点研究：

- Underlying Models
- Agent / Harness
- Context System
- Tools
- Runtime
- Sandbox
- Memory
- Rules
- MCP
- Skills
- Execution
- Verification

## 9.4 Agent Loop

尽可能还原：

```text
Task
↓
Planning
↓
Context Gathering
↓
Reasoning
↓
Tool Selection
↓
Execution
↓
Observation
↓
Verification
↓
Repair / Iteration
↓
Final Artifact
```

重点不是描述 UI，而是理解：

> **这个产品实际上如何让 Agent 完成 Software Engineering Task？**

## 9.5 Workflow

研究从：

```text
Intent
→ Task
→ Repository
→ Agent
→ Code
→ Test
→ Review
→ Commit / PR
→ Delivery
```

各阶段产品承担什么角色。

## 9.6 Capability

统一分析：

- Coding
- Repository Understanding
- Reasoning
- Planning
- Tool Use
- Terminal
- Browser / External Tools
- Testing
- Debugging
- Refactoring
- Context Management
- Long-running Tasks
- Parallel / Multi-agent
- Memory
- MCP
- Skills
- Sandbox
- Cloud Agent

## 9.7 Economics

- Pricing
- Subscription
- Usage Limits
- Model Cost
- API / Token Economics where relevant
- Enterprise Offering

## 9.8 Ecosystem

- GitHub
- Git
- IDE
- CI/CD
- MCP ecosystem
- Skills ecosystem
- Community
- Open Source
- Enterprise integrations

## 9.9 Unique Insight

每个产品最终必须回答：

> **这个产品最值得行业学习的是什么？**

---

# 10. Source Strategy

研究资料必须建立 Source Hierarchy。

## Tier 1 — Primary Sources

最高优先级：

- Official Website
- Official Documentation
- Official Blog
- Official Changelog
- Official GitHub
- Official Pricing
- Company Reports / Filings
- Official Developer / Product Announcements

用于确认产品事实、功能、价格、架构声明和官方定位。

## Tier 2 — High-quality Independent Sources

包括但不限于：

- JetBrains Developer Ecosystem
- Stack Overflow Developer Survey
- GitHub ecosystem data
- Gartner / IDC / Forrester 等行业研究（若有直接相关公开资料）
- 高质量开发者调查
- 高质量技术媒体
- 主流公开 Benchmark

用于市场、采用率、趋势与独立验证。

## Tier 3 — Community Evidence

包括：

- Reddit
- Hacker News
- GitHub Issues / Discussions
- X
- Discord / Community Forums
- 中文开发者社区

用于发现真实用户体验、争议、痛点和趋势信号。

## Tier 4 — Individual Reviews / Blogs

用于：

- 产品体验补充
- 实际工作流案例
- 辅助发现问题

不得作为重要行业事实的唯一依据。

---

# 11. Evidence Management

本研究采用 Evidence-driven Research。

重要结论必须尽可能建立：

```text
Claim
↓
Evidence
↓
Source
↓
Date
↓
Confidence
```

## 11.1 Evidence Grade

建议采用四级证据等级：

### A — Strong Evidence

多个高质量、相互独立的可靠来源一致支持。

### B — Good Evidence

存在权威来源支持，但样本、范围或独立验证有限。

### C — Indicative Evidence

第三方实测、社区反馈或单一高质量来源，可以作为趋势/体验信号，但不足以作为强事实。

### D — Weak Evidence

营销宣传、单个人体验、未经验证的说法或明显缺乏独立验证的信息。

### Evidence Rule

> Evidence Grade 衡量的是“当前证据支持该 Claim 的强度”，而不是产品好坏。

---

# 12. Candidate Inclusion / Exclusion Record

所有最终入选和重要落选候选都应记录决策依据。

建议使用统一结构：

| Product | Market Evidence | Capability Evidence | Innovation | Ecosystem | Momentum | Decision | Reason |
|---|---|---|---|---|---|---|---|
| Candidate A |  |  |  |  |  | Selected / Rejected |  |

禁止出现：

> “感觉不重要，所以不研究。”

应该写成：

> “Market Adoption 较低、技术创新与已入选产品高度重叠、缺乏独立产品路线，因此研究优先级低于 Candidate X。”

这样未来复盘时可以理解当时的研究判断。

---

# 13. Cross-product Analysis

TOP10 完成 Deep Research 后，不立即写总结，而是建立统一 Comparison Matrix。

## 13.1 Market Matrix

比较：

- Adoption
- Usage
- User Base
- Enterprise Presence
- Ecosystem
- Momentum

## 13.2 Product Matrix

比较：

- Product Surface
- Target User
- UX
- Workflow
- Pricing

## 13.3 Agent Matrix

比较：

- Planning
- Reasoning
- Context
- Tool Use
- Execution
- Verification
- Memory
- Autonomy

## 13.4 Architecture Matrix

比较：

- Model Layer
- Harness
- Runtime
- Sandbox
- MCP
- Skills
- Extensibility
- Cloud Execution

最终重点回答：

> **不同产品背后是否正在出现不同的 Agent Architecture / Software Engineering Workflow Paradigm？**

---

# 14. Final Decision Framework

本研究不输出未经证据支持的“个人喜好排行榜”。

正式输出以：

## 14.1 Market Landscape Ranking

> **2026 AI Coding Agent Market Leaders / Representative Leaders — Top 10**

回答：

> 哪些产品最具有市场重要性和代表性？

## 14.2 Capability / Workflow View

通过 Capability Matrix、Category Leaders、二维图等形式回答：

> 谁代表当前先进 Agent 能力？

> 谁正在重新定义 Software Engineering Workflow？

## 14.3 Research-backed Decision Matrix

不是“Personal Ranking”，而是针对明确决策问题给出有证据支撑的判断，例如：

- 市场主流代表
- Agentic Coding 代表
- AI IDE 代表
- CLI Agent 代表
- Open-source 代表
- Cloud Agent 代表
- Software Engineering Workflow 创新代表
- 中国市场重要代表

每个 Decision 都必须能够追溯到前面的 Research Evidence。

---

# 15. Research Workflow

## 15.1 Operational Rule

> **本节是本 Case 的唯一 Operational Workflow。实际执行时，以本节的 Phase 顺序为准；§18 用于说明 Phase 与交付物的映射；§20 用于描述更高层的 Research Lifecycle，不定义第二套执行顺序。**

整个 Case 采用“**广度筛选 → 深度研究 → 横向分析 → 决策 → 资产化**”的两阶段研究结构。

```text
Phase 0 — Research Charter
        ↓
Phase 1 — Candidate Universe
        ↓
Phase 2 — Broad Market & Evidence Collection
        ↓
Phase 3 — Ranking & Final Top 10 Selection
        ↓
Phase 4 — Deep Product Research
        ↓
Phase 5 — Benchmark & Independent Evidence Analysis
        ↓
Phase 6 — Cross-product Analysis
        ↓
Phase 7 — Decision & Research Conclusions
        ↓
Phase 8 — Research Asset Production
```

### Phase 0 — Research Charter

**Objective**：定义研究问题、范围、分类体系、评价框架和研究方法。

**Main Activities**：

- Research Mission / Core Questions
- Scope & Taxonomy
- Research Population Definition
- Ranking & Selection Framework
- Source Strategy
- Evidence Rules
- Research Quality Gates

**Primary Deliverable**：`00-research-charter.md`

**Exit Criteria**：Charter Approved，且研究范围与执行方法稳定。

### Phase 1 — Candidate Universe Construction

**Objective**：建立尽可能完整的候选池，不提前只研究“TOP10”。

**Main Activities**：

- Product discovery
- Company / Product Family deduplication
- Product Surface classification
- Initial inclusion / exclusion
- Candidate rationale recording

**Primary Deliverable**：`01-candidate-universe.md`

**Exit Criteria**：Candidate Universe 足以覆盖主要市场参与者，且候选对象已有基本分类与入池理由。

### Phase 2 — Broad Market & Evidence Collection

**Objective**：对候选进行**广度、浅层、可比较的证据收集**，为 Top 10 Selection 提供输入。

**Main Activities**：

- Market Adoption evidence
- Basic Product / Agent Capability evidence
- Product / Workflow Innovation signals
- Ecosystem / Strategic evidence
- Momentum evidence
- Initial public benchmark signals
- Source and Evidence Grade recording

**Important Boundary**：Phase 2 不要求对所有候选执行完整 Deep Product Research。Phase 2 只回答“这个产品是否值得进入 Top 10，以及为什么”。

**Primary Deliverable**：`02-market-evidence.md`

**Exit Criteria**：主要候选能够基于统一维度进行横向筛选，Composite Assessment 所需证据基本齐备。

### Phase 3 — Ranking & Final Top 10 Selection

**Objective**：基于 Phase 2 的广度证据完成综合评分、跨来源复核和 Research Judgment，锁定最终研究对象。

**Main Activities**：

- Cross-source normalization
- Composite scoring
- Ranking review
- Selected / Rejected decision
- Explicit inclusion / exclusion rationale

**Primary Deliverables**：

- `03-ranking-methodology.md`
- `03-top10-selection.md`

**Exit Criteria**：Top 10 已锁定；重要落选产品有可复盘的理由；任何偏离 Composite Score 的判断均有证据与解释。

### Phase 4 — Deep Product Research

**Objective**：仅对最终 Top 10 进行系统、统一模板的深度研究。

**Main Activities**：

- Product Identity
- Positioning
- Architecture
- Agent Loop
- Workflow
- Capability
- Economics
- Ecosystem
- Unique Insight

**Primary Deliverables**：

- `04-products/product-01.md`
- `04-products/product-02.md`
- …

即目录 `04-products/` 下的 Top 10 产品研究文件。

**Exit Criteria**：Top 10 全部完成统一深度研究，且核心事实、架构、Workflow 与能力分析均有证据支撑。

### Phase 5 — Public Benchmark & Independent Evidence Analysis

**Objective**：系统整理并审查公开 Benchmark 与高质量独立证据，验证关键产品结论。

**Main Activities**：

- Benchmark methodology review
- Model-level vs Agent-level distinction
- Independent evaluation comparison
- Limitations / comparability analysis
- Relevance assessment

**Important Boundary**：Public Benchmark 并不是只在 Phase 5 才开始出现。它是贯穿 Phase 2–6 的 Supporting Evidence；Phase 5 的作用是集中、系统地进行整理和深度验证。

**Primary Deliverable**：`05-benchmarks.md`

**Exit Criteria**：关键 Benchmark 已正确解释其能够证明与不能证明的内容，且没有发生 Model Benchmark 与 Agent Product Benchmark 混淆。

### Phase 6 — Cross-product Analysis

**Objective**：将 Top 10 的产品研究、Benchmark 和独立证据转化为统一横向 Comparison Matrix，并识别市场与技术模式。

**Main Activities**：

- Market Matrix
- Product Matrix
- Agent Matrix
- Architecture Matrix
- Pattern / Paradigm identification

**Primary Deliverable**：`06-cross-product-analysis.md`

**Exit Criteria**：主要产品差异、共性、Agent Architecture Paradigm 与 Software Engineering Workflow Paradigm 已被系统识别。

### Phase 7 — Decision & Research Conclusions

**Objective**：基于完整 Evidence System 形成最终 Market View、Capability / Workflow View 与 Research-backed Decisions。

**Main Activities**：

- Market Landscape Ranking
- Capability / Workflow View
- Category Leaders
- Research-backed Decision Matrix
- Final Conclusions
- Future Research Questions

**Primary Deliverable**：`07-decision.md`

**Exit Criteria**：最终判断能够追溯到前面的 Evidence、Analysis 与明确的 Research Judgment。

### Phase 8 — Research Asset Production

**Objective**：将已经完成的研究转化为可长期复用、更新和展示的 Research Assets。

**Main Activities**：

- Research Note
- Structured Dataset
- Sources consolidation
- Interactive HTML
- Executive PPT
- Optional PDF / Excel / CSV

**Primary Deliverables**：

- `08-research-note.md`
- `08-dataset/`
- `08-presentation/`
- `08-sources.md`

**Exit Criteria**：Research Note、Dataset、主要 Presentation Asset 和 Sources 已完成，Case 可以被复盘、更新和复用。

### 15.2 Broad Research vs Deep Research Boundary

为了避免研究范围失控，本 Case 明确区分两种研究深度：

```text
Phase 1–3
= Broad Research
= Candidate Discovery + Screening + Selection

Phase 4–7
= Deep Research
= Product Understanding + Validation + Comparison + Decision

Phase 8
= Knowledge / Asset Production
```

因此：

> **Phase 3 选择 Top 10 不要求完成 Phase 4 的完整 Product Research。**

Phase 2 的证据只需要足以支持：

> “这个候选是否值得进入 Top 10？”

而 Phase 4 才回答：

> “这个产品到底是如何工作的，以及它代表了什么 Agent / Workflow Paradigm？”

### 15.3 Public Benchmark Positioning

Public Benchmark 是贯穿式 Supporting Evidence：

```text
Phase 2 → collect initial benchmark signals
Phase 3 → optionally use benchmark as selection evidence
Phase 4 → incorporate relevant benchmark into product research
Phase 5 → systematically review and validate benchmarks
Phase 6 → use validated benchmark evidence in cross-product analysis
```

---

# 16. Research Execution Principles

## 16.1 Evidence before Conclusion

先收集证据，再形成结论。

## 16.2 Multiple Sources

重要市场判断不得依赖单一来源。

## 16.3 Primary Source First

产品事实优先使用官方一手资料。

## 16.4 Separate Fact and Interpretation

明确区分：

- Fact
- Evidence
- Analysis
- Judgment

## 16.5 Date Awareness

所有市场数据记录其**数据时间**和**发布时间**。

研究截点为 2026 年 8 月，不得把不同时期的数据无标记地混合比较。

## 16.6 No False Precision

当数据口径不可直接比较时，不制造看似精确但实际上没有意义的数字。

## 16.7 No Single-source Authority

任何一个第三方榜单都不能自动成为最终市场排名。

## 16.8 No Model-Agent Conflation

模型 benchmark 不得直接等同于 Agent 产品 benchmark。

## 16.9 No Feature-count Ranking

不能通过“功能数量”判断产品先进程度。

## 16.10 Human Judgment Remains Central

研究中的关键判断由人负责，AI 可以辅助搜索、提取、整理和分析，但不得在没有证据审查的情况下自动生成最终行业结论。

---

# 17. Deliverables

本 Case 最终形成四层 Research Asset。

## 17.1 Research Note — Primary Knowledge Asset

记录：

- 核心问题
- 关键事实
- 研究结论
- 关键判断
- 市场认知
- 方法论
- Decision
- Future Questions

这是长期认知资产的核心。

## 17.2 Structured Dataset — Data Asset

建议至少包含：

```text
product
company
region
product_family
surface
models
market_adoption
capability
innovation
ecosystem
momentum
selection_status
evidence_grade
sources
```

数据结构以后应支持更新，而不是只服务于一次报告。

## 17.3 Interactive HTML — Primary Presentation Asset

HTML 是本 Case 推荐的最佳展示形式。

原因：

- 适合 TOP10 产品卡片
- 适合多维 Comparison Matrix
- 适合二维市场/技术图
- 适合筛选和排序
- 适合展示证据与来源
- 可以持续更新

目标可以是：

> **2026 AI Coding Agent Landscape Explorer**

## 17.4 PPT — Executive Presentation

PPT 作为高层摘要，而不是原始研究材料。

建议控制在约 10–15 页：

```text
1. Executive Summary
2. Market Landscape
3. AI Coding Agent Evolution
4. Global Top 10
5. Market Adoption
6. Product / Agent Architecture
7. Capability Comparison
8. Major Market Trends
9. Representative Leaders
10. Decision Matrix
11. Key Conclusions
12. Future Outlook
```

## 17.5 Optional PDF / Excel / CSV

根据实际需求生成：

- PDF：研究报告固化版
- CSV / Excel：结构化数据交换与分析

它们不是主要知识资产。

---

# 18. Recommended Repository Structure

本 Case 的推荐结构必须与 §15 的 Phase 顺序保持一一对应。目录结构表达“产物是什么”，§15 表达“什么时候产生这些产物”。

```text
cases/
└── 001-ai-coding-agent-landscape/
    ├── 00-research-charter.md
    ├── 01-candidate-universe.md
    ├── 02-market-evidence.md
    ├── 03-ranking-methodology.md
    ├── 03-top10-selection.md
    ├── 04-products/
    │   ├── product-01.md
    │   ├── product-02.md
    │   └── ...
    ├── 05-benchmarks.md
    ├── 06-cross-product-analysis.md
    ├── 07-decision.md
    ├── 08-research-note.md
    ├── 08-sources.md
    ├── 08-dataset/
    │   ├── candidates.csv
    │   └── products.csv
    └── 08-presentation/
        ├── landscape.html
        └── executive-summary.pptx
```

### Phase → Deliverable Mapping

| Phase | Goal | Primary Deliverable | Exit Criteria |
|---|---|---|---|
| Phase 0 | 定义研究 | `00-research-charter.md` | Charter Approved |
| Phase 1 | 建立候选池 | `01-candidate-universe.md` | Candidate Universe Stable |
| Phase 2 | 广度证据收集 | `02-market-evidence.md` | Candidates Comparable |
| Phase 3 | 评分与选 Top 10 | `03-ranking-methodology.md` + `03-top10-selection.md` | Top 10 Locked |
| Phase 4 | 深度产品研究 | `04-products/*.md` | All Top 10 Researched |
| Phase 5 | Benchmark / Independent Validation | `05-benchmarks.md` | Major Claims Validated |
| Phase 6 | 横向分析 | `06-cross-product-analysis.md` | Major Patterns Identified |
| Phase 7 | 最终判断 | `07-decision.md` | Research Conclusions Stable |
| Phase 8 | 资产化 | `08-research-note.md` + `08-dataset/` + `08-presentation/` + `08-sources.md` | Case Complete |

### Structural Rule

> **阶段性主交付物的文件名前缀必须与 Phase 编号一致。**

例如：

- Phase 3 → `03-ranking-methodology.md`、`03-top10-selection.md`
- Phase 4 → `04-products/*.md`
- Phase 7 → `07-decision.md`
- Phase 8 → `08-research-note.md`、`08-dataset/`、`08-presentation/`

目录可以随着研究实际推进进行调整，但不能改变已经定义好的 Phase 编号与核心交付物语义，除非 Charter 经过版本化更新。

---

# 19. Research Quality Gate

在宣布 Case 完成前，必须至少通过以下检查：

### Scope

- [ ] AI Coding Agent 定义明确
- [ ] Product / Product Family 研究单位明确
- [ ] Plugin-only 排除规则执行
- [ ] Model 与 Agent 产品分离

### Market

- [ ] Candidate Universe 建立
- [ ] Global Top 10 有明确选择逻辑
- [ ] 重要落选产品有理由
- [ ] 市场采用度有多源证据
- [ ] 数据时间与发布时间明确

### Product Research

- [ ] TOP10 使用统一研究模板
- [ ] Product Surface 已分类
- [ ] Agent Workflow 已分析
- [ ] Model / Agent / Runtime 已区分

### Evidence

- [ ] 重要结论有来源
- [ ] 一手来源优先
- [ ] Public Benchmark 已正确解释
- [ ] Model Benchmark 与 Agent Benchmark 未混淆
- [ ] Evidence Grade 已应用于关键判断

### Analysis

- [ ] Market View 与 Capability View 分开
- [ ] 未使用功能数量作为核心排名依据
- [ ] Composite Score 与 Research Judgment 有明确区分
- [ ] 重要判断可以追溯到 Evidence

### Delivery

- [ ] Research Note 完成
- [ ] Dataset 完成
- [ ] HTML / Presentation 完成或有明确取舍
- [ ] 最终 Decision Matrix 完成
- [ ] Future Research Questions 已记录

---

# 20. Final Research Philosophy

本 Case 最终不追求：

> “找到一个永远正确的 AI Coding Agent 排名。”

而追求：

> **建立一个能够解释 2026 年 AI Coding Agent 市场、技术与工作流变化的证据体系，并基于该体系形成可复盘、可更新、可迁移的判断。**

这里的流程图不是第二套 Operational Workflow，而是对整个 Research Lifecycle 的抽象：

```text
Problem Framing
      ↓
Scope & Taxonomy
      ↓
Candidate Universe
      ↓
Broad Evidence Collection
      ↓
Screening & Research Judgment
      ↓
Research Population
      ↓
Deep Research
      ↓
Independent Validation
      ↓
Cross-product Analysis
      ↓
Decision
      ↓
Knowledge Asset Production
      ↓
Evaluation
      ↓
Reusable Research Workflow
```

其中：

- **Broad Evidence Collection** 对应 Phase 2
- **Screening & Research Judgment** 对应 Phase 3
- **Deep Research** 对应 Phase 4
- **Independent Validation** 对应 Phase 5
- **Cross-product Analysis** 对应 Phase 6
- **Decision** 对应 Phase 7
- **Knowledge Asset Production** 对应 Phase 8
- **Evaluation** 作为 Case 完成后的质量复盘活动，而不是一个额外的、与 §15 平行的 Research Phase

> **本 Case 的真正成果不是一份 AI Coding Agent 排行榜，而是第一次完整验证一套 AI-native Research Workflow。**

---

## Charter Status

**Status:** Approved for execution

**Research Charter Version:** v1.1

**Research Cutoff:** August 2026

**Next Phase:** Candidate Universe Construction

**Next Deliverable:** `01-candidate-universe.md`
