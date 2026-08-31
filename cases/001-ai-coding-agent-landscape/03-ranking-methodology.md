# Case 001 — 2026 AI Coding Agent Landscape

## Phase 3 — Ranking Methodology

> Research snapshot: 2026-08-31
>
> Research cutoff: August 2026
>
> Research unit: AI Coding Agent Product / Product Family
>
> Status: Phase 3 methodology completed

---

## 1. Phase 3 Objective

本阶段只解决一个问题：

> **哪些候选最值得进入最终 Top 10，为什么？**

Phase 3 承接：

- `00-research-charter.md` — Research Methodology / Highest Constraint
- `01-candidate-universe.md` — Phase 1 Candidate Universe
- `02-market-evidence.md` — Phase 2 Broad Evidence Base

本阶段严格停留在 **Broad Research → Ranking & Final Top 10 Selection**，不进入 Phase 4 的完整 Product Research，也不提前完成 Phase 5–8。

Charter 明确规定 Phase 3 的执行顺序为：

```text
Evidence
↓
Normalization
↓
Assessment
↓
Composite Score
↓
Cross-source Review
↓
Research Judgment
↓
Final Selection
```

因此本文件回答：

> **我们是如何排名的？**

最终候选名单与选择理由记录在 `03-top10-selection.md`。

---

## 2. Research Population

### 2.1 Population source

严格以 `01-candidate-universe.md` 建立的 Candidate Universe 为研究人口，不重新创建候选池。

Phase 1 已建立约 44 个 active candidate product families / candidates，以及少量明确排除或合并对象。Core / Secondary / Watchlist 是研究优先级分层，不是预设排名。Phase 3 不把 Core 顺序直接视为 Ranking。

### 2.2 Product Family rule

同一 Product Family 的 CLI、IDE、Desktop、Cloud、Plugin 不重复计算。

本阶段确认以下处理：

| Family / Object | Phase 3 handling | Reason |
|---|---|---|
| GitHub Copilot / Copilot CLI / Copilot coding agent | One family | 同一 Copilot agent system，不重复计数 |
| Cursor IDE / Cursor CLI / Cursor Cloud Agents | One family | 同一 Cursor product family |
| TRAE IDE / TraeCode / TRAE Work / SOLO / TraeCode | One family | 同一 TRAE product family，但不同 surface 在深度研究阶段再拆 capability |
| Qoder / Qoder CN / Tongyi Lingma lineage | One family | 研究单位是 product family；2026 命名迁移后不重复计数 |
| Devin / Devin Desktop / Windsurf legacy | One family | Devin Desktop 官方明确为 Windsurf 的新名称 |
| Google Antigravity / Antigravity CLI / Gemini CLI lineage | One family | Gemini CLI 已向 Antigravity CLI 迁移，避免 Google 内部重复计算 |
| Amazon Q Developer / Q CLI → Kiro lineage | Kiro family only for modern selection | AWS 已将 Q CLI 重品牌为 Kiro，并持续引导用户迁移；Q Developer 保留为历史 / transitional evidence |
| JetBrains AI / Junie | One family | 本阶段按 family 处理，后续 capability matrix 可拆 surface |

### 2.3 Important boundary decisions

Phase 3 不会因为产品“不是传统 IDE”而自动排除。只要其 Software Engineering Workflow Coverage 与 AI Coding Agent Definition 相符，就可以参与 Selection，例如 Replit Agent。

相反，纯模型、plugin-only、已经停止或高度退化为 adjacent workflow 的对象，不应为了凑 Top 10 而进入主榜。

---

## 3. Evidence Normalization

### 3.1 Evidence hierarchy

证据优先级遵循 Charter：

1. **Tier 1 — Primary**：官方产品、官方文档、官方博客、官方 GitHub、官方公司公告 / 报告；
2. **Tier 2 — Independent**：JetBrains、GitHub ecosystem、公开 benchmark、可信技术媒体；
3. **Tier 3 — Community / Discovery**：Reddit、Hacker News、GitHub Issues/Discussions、社区追踪；
4. **Tier 4 — Individual Review**：个人体验与单篇博客。

重大市场结论优先使用 Tier 1 + Tier 2 交叉验证。

### 3.2 Market evidence normalization

Market Adoption 不强行把不同统计口径转成一个“真实用户数”。本阶段按以下优先级解释：

```text
Independent Adoption Signal
        ↓
Verified / Repeated Usage Signal
        ↓
Enterprise / Ecosystem Signal
        ↓
Vendor User / Customer Claim
        ↓
Community Signal
```

同一产品出现“用户数”“活跃用户”“企业客户”“调查采用率”“GitHub stars”时，不进行虚假等价。

特别遵守：

> **Vendor Claim ≠ Independent Market Fact**

例如，2026 年 8 月 JetBrains 调查给出了 Claude Code、Codex、GitHub Copilot、Cursor、OpenCode、Google Antigravity 等在专业开发者工作场景中的 adoption signal；这些数字用于横向判断相对 market significance，但不被解释为全球市场份额。[^market1]

### 3.3 Product / Agent capability normalization

Capability 采用 **selection-level assessment**，不是完整产品架构研究。

主要判断：

- Agent Autonomy
- Repository Understanding
- Planning
- Reasoning
- Tool Use
- Execution
- Verification
- Repair / Iteration
- Long-running / Background
- Parallel / Multi-agent
- Memory / Rules
- MCP / Skills
- Sandbox / Runtime
- Cloud Execution

Phase 3 只关心：

> 是否存在足以改变 Top 10 Selection 的能力差异。

### 3.4 Workflow innovation normalization

核心问题：

> **这个产品正在改变哪一段 Software Engineering Workflow？**

优先观察：

- IDE workflow
- Terminal workflow
- Issue → Code
- PR → Code
- Spec → Code
- Idea → Product
- Background development
- Multi-agent workflow
- Agent Workspace

功能数量不计入评分本身。只有当功能改变了工作流边界，才形成 Innovation evidence。

---

## 4. Five Evaluation Dimensions

Charter 的原始权重保持不变：

| Dimension | Weight | Core question |
|---|---:|---|
| Market Adoption | 30% | 这个产品在现实世界有多重要？ |
| Product / Agent Capability | 30% | Agent 实际能完成什么？ |
| Product / Workflow Innovation | 20% | 它是否正在重新定义 Software Engineering Workflow？ |
| Ecosystem / Strategic Importance | 10% | 是否形成重要生态与战略影响？ |
| Momentum | 10% | 是否具备明显增长和发展势能？ |

### 4.1 Why the original weights are retained

Phase 3 没有发现足以支持版本化改权的系统性问题。

主要原因：

1. Market Adoption 仍是 Research Mission 中“Market Leaders / Representative Leaders”的必要组成；
2. Product / Agent Capability 与 Workflow Innovation 分开，可以避免“用户多 = 技术先进”；
3. Ecosystem / Strategic Importance 可识别大平台带来的长期影响；
4. Momentum 使新进入者有机会挑战历史领导者；
5. 五维结构与 Phase 2 证据字段直接对应，没有发现明显 measurement bias 足以推翻原权重。

因此本阶段遵守：

> **No weight change after observing the result.**

---

## 5. Scoring Scale

每个维度采用 1–5 分，允许使用 0.5 increments。

> 分数是 **ordinal assessment / decision aid**，不是客观物理测量值。

### 5.1 Market Adoption

| Score | Interpretation |
|---:|---|
| 5.0 | 全球领先采用信号，且有强独立证据与/或大型商业规模交叉支持 |
| 4.5 | 强市场存在感，有独立调查、成熟商业规模或大型生态共同支持 |
| 4.0 | 明显市场重要性，但独立覆盖或口径存在限制 |
| 3.5 | 中等偏强市场信号，常由独立调查、生态或可靠 vendor evidence 支撑 |
| 3.0 | 有活跃用户/生态，但规模或独立验证有限 |
| 2.5 | 主要依赖 vendor / community / strategic distribution signal |
| 2.0 | 规模较有限或 adoption denominator 明显不足 |
| 1.0–1.5 | 很弱的市场信号或极早期 |

### 5.2 Product / Agent Capability

| Score | Interpretation |
|---:|---|
| 5.0 | 完整、成熟的 agent loop，并覆盖复杂/长任务/执行/验证/repair 等关键能力 |
| 4.5 | 强 agentic capability，已超出一般 IDE assistant，并具备多个高级 runtime / orchestration primitives |
| 4.0 | 成熟的 multi-step coding agent，可可靠完成主要 repo-level tasks |
| 3.5 | 已具备明确 agent loop，但复杂任务、runtime 或 autonomy 仍有限 |
| 3.0 | 基本 agentic coding 能力，能力边界较明显 |
| 2.0–2.5 | 有部分 agent workflow，但更接近 assistant / adjacent category |
| 1.0–1.5 | 主要是 completion / chat / narrow workflow |

### 5.3 Workflow Innovation

| Score | Interpretation |
|---:|---|
| 5.0 | 明显创建新的 Software Engineering Workflow paradigm |
| 4.5 | 对现有工作流产生结构性改变，并形成可观察的新工作方式 |
| 4.0 | 有清晰 workflow differentiation，但仍属于既有范式的强扩展 |
| 3.5 | 有明显 UX / workflow innovation，但影响范围较局部 |
| 3.0 | 主要是成熟 agent workflow 的执行与整合 |
| 2.0–2.5 | 增量式 feature innovation |
| 1.0–1.5 | 很少体现 workflow-level change |

### 5.4 Ecosystem / Strategic Importance

| Score | Interpretation |
|---:|---|
| 5.0 | 具备大型平台、企业生态、模型生态或行业级战略位置 |
| 4.5 | 强生态 / 平台分发能力，且能影响其他开发工具或工作流 |
| 4.0 | 生态成熟，拥有明显开发者/企业网络效应 |
| 3.5 | 有活跃社区 / provider / integration ecosystem |
| 3.0 | 生态有价值但规模或战略覆盖较有限 |
| 2.0–2.5 | 主要依赖 niche/community ecosystem |
| 1.0–1.5 | 生态影响有限 |

### 5.5 Momentum

| Score | Interpretation |
|---:|---|
| 5.0 | 2026 年增长、产品迭代、分发或战略升级极强 |
| 4.5 | 增长与迭代明显高于成熟市场基线 |
| 4.0 | 持续增强，具有清晰向上趋势 |
| 3.5 | 稳定增长或重要产品升级 |
| 3.0 | 稳定但未形成显著加速度 |
| 2.0–2.5 | 增长有限或战略方向不清晰 |
| 1.0–1.5 | 停滞、转型中或明显弱化 |

---

## 6. Composite Score

Composite Score 公式：

```text
Composite Score
=
Market Adoption × 0.30
+ Product / Agent Capability × 0.30
+ Workflow Innovation × 0.20
+ Ecosystem / Strategic Importance × 0.10
+ Momentum × 0.10
```

总分范围：1.0–5.0。

### Important limitation

Composite Score 不能解释为：

> “产品 A 客观上比产品 B 好 7%”。

它只回答：

> **在本研究定义的五个维度和权重下，候选的综合研究重要性大致位于什么区间。**

### Unknown handling

当关键市场或产品证据明确 Unknown 时：

- 不用其他维度“脑补”；
- 不把 Unknown 当成 Low；
- 在 score 中采用保守档位；
- 最终在 `03-top10-selection.md` 的 Evidence Gaps 中说明。

---

## 7. Research Judgment Method

Composite Score 不是自动 Selection。

使用以下决策规则：

### Rule 1 — Score is a filter, not a verdict

优先识别：

- 明显领先组
- Top 10 boundary group
- Near-miss group
- Adjacent / Boundary group

### Rule 2 — Strong representative value can override a small score disadvantage

当两个候选分数接近时，可以由 Research Judgment 决定，但必须回答：

1. Score result
2. Research judgment
3. Divergence
4. Reason
5. Evidence

### Rule 3 — Technology significance does not erase market significance

一个纯技术先锋候选必须有足够的 Product / Workflow / Strategic significance，才能挑战 market-heavy candidate。

### Rule 4 — Market scale does not erase workflow significance

一个高 adoption 产品不能仅凭规模自动压过真正代表下一代 workflow 的候选。

### Rule 5 — Family duplication must be resolved before ranking

产品 surface 不得占用额外 Top 10 名额。

---

## 8. Evidence Conflict Handling

所有可能改变 Top 10 的重大 Claim 做三层复核：

```text
Official Claim
vs
Independent Evidence
vs
Community Evidence
```

并记录：

- Official claim
- Independent evidence
- Conflict
- Current confidence
- Research implication

### High-impact conflicts identified in Phase 3

#### 8.1 Claude Code market leadership

JetBrains 的 May–July 2026 survey 显示 Claude Code 在 professional developers at work 的 adoption signal 达约 39%，显著高于其他单一产品；Anthropic 自身 2026 年研究也显示 Claude Code 用户、任务范围与企业使用继续增长。前者是 Independent Evidence，后者是 Vendor / proprietary evidence，不能混为一谈，但两者方向一致。[^market1][^market3]

#### 8.2 Devin / Qoder / TRAE user counts

Devin、Qoder、TRAE 都有较大的厂商口径用户数字，但这些数字并没有与 JetBrains 等独立 survey 形成完全可比的 denominator。因此它们可以提高 Market Significance 判断，但不能被当成与 Claude Code / Codex / Copilot adoption survey 完全同口径的全球市场份额。

Qoder 在 2026-08 的官方材料给出 6M+ users worldwide / 100K+ businesses，并在 2026-08-26/27 推出新的 agentic platform。TRAE 则公布了 2025 年底 6M registered users、约 60M sessions，并在 2026 年演进到 TRAE Work + TRAE IDE 双产品结构。这些均属于 Vendor Claim / product evidence。[^qoder][^trae]

#### 8.3 Cursor corporate transition

Cursor 仍具极强 Product / Workflow significance，但 2026-08 的 SpaceX acquisition 与 OpenAI model-access dispute 改变了其战略环境。该事件影响 Ecosystem / Strategic 与 Momentum 判断，但不应被错误地解释为 Cursor agent capability 本身下降。[^cursor]

#### 8.4 Amazon Q Developer / Kiro

AWS 已明确写明 Amazon Q Developer CLI 已 rebrand 为 Kiro，并要求用户升级以获得之后仅 Kiro 才有的新功能；AWS 也宣布 2027-04-30 停止 Amazon Q Developer IDE plugin 支持。故 Phase 3 不将 Q Developer 作为独立 modern market family。[^qdev]

#### 8.5 Gemini CLI / Antigravity

Google 已从 Gemini CLI 向 Antigravity CLI 迁移；因此不允许 Gemini CLI 与 Antigravity 双计。[^antigravity]

---

## 9. Benchmark Handling

Phase 3 允许 benchmark 作为 supporting evidence，但不做 Benchmark Deep Dive。

三类 evidence 严格区分：

```text
Model-level Benchmark
vs
Agent-level Benchmark
vs
Product-level Evidence
```

公开 SWE-bench 结果可以作为 Capability supporting evidence，但由于底层模型、harness、运行预算、评测方法和提交时间不同，不能直接作为市场排名。[^benchmark]

Phase 3 的 benchmark use rule：

1. 不因单个 benchmark 第一名直接进入 Top 10；
2. 不因单个 benchmark 落后直接排除产品；
3. 只在其与 Capability / Workflow Judgment 一致时增加 confidence；
4. 完整 methodology / comparability review 留给 Phase 5。

---

## 10. Sensitivity / Robustness Method

只进行轻量级权重扰动：

- Base: 30 / 30 / 20 / 10 / 10
- Market-heavy: 35 / 25 / 20 / 10 / 10
- Capability-heavy: 25 / 35 / 20 / 10 / 10
- Workflow-heavy: 25 / 30 / 25 / 10 / 10

目标不是生成第二套排行榜，而是识别：

- **Robust Selection**：小幅改权重仍稳定进入 Top 10；
- **Sensitive Selection**：位置容易变化；
- **Borderline Selection**：主要位于 9–12 区域，依赖 Research Judgment。

在本次 Phase 3 中，前 8 个位置总体稳定；真正敏感的是最后 2 个席位，尤其是 OpenCode / Qoder / Factory / TRAE / Kiro 之间的边界。见 `03-top10-selection.md`。

---

## 11. Limitations

### 11.1 Market data comparability

没有一份公开独立数据可以给所有候选提供同一时间、同一口径、同一 denominator 的全球 adoption。尤其中国市场更明显。因此本排名不是 market-share table。

### 11.2 Vendor claims

一些产品的用户数、企业客户数、收入等仍主要来自厂商。它们用于 triangulation，但不能被标成 Independent Evidence。

### 11.3 Fast-moving product status

2026 年 AI Coding Agent 市场迭代速度很快。Cursor corporate status、Qoder platform transition、Google terminal migration、AWS Q→Kiro transition 都说明产品边界会迅速变化。研究结果是 **as-of August 2026** 的 snapshot。

### 11.4 Capability evidence

Phase 3 只做 selection-level capability assessment。不能据此替代 Phase 4 的完整 architecture / agent-loop research。

### 11.5 Benchmark comparability

公开 benchmark 经常绑定特定模型与 harness，且 methodology 不完全一致。本阶段只能用于 supporting evidence。

---

## 12. Methodology Conclusion

Phase 3 保留 Charter v1.1 的原始五维权重，不做为了迎合结论而进行的权重调整。

最终方法是：

```text
Phase 2 Evidence
↓
Product Family Deduplication
↓
Evidence Normalization
↓
Five-dimension Assessment
↓
Composite Score
↓
Cross-source / Conflict Review
↓
Research Judgment
↓
Final Top 10
```

其核心原则是：

> **The final Top 10 is an evidence-backed Research Ranking, not an automatically generated universal truth.**

本阶段下一份文件 `03-top10-selection.md` 将记录：

- Candidate Population After Deduplication
- Research Decision Matrix
- Composite Scores
- Research Judgment
- Final Top 10
- Near-miss Candidates
- Evidence Gaps
- Robustness Check

---

## Sources

### Primary / Official

- OpenAI — Codex: https://openai.com/codex/
- GitHub — Copilot / agentic product updates: https://github.blog/news-insights/product-news/
- Anthropic — Claude Code research: https://www.anthropic.com/research/claude-code-expertise
- Cursor — Cloud Agents: https://cursor.com/docs/cloud-agent
- Cursor — Computer-use cloud agents: https://cursor.com/blog/agent-computer-use
- Google Antigravity CLI: https://www.antigravity.google/blog/introducing-google-antigravity-cli
- Google Antigravity migration: https://www.antigravity.google/docs/cli/gcli-migration/
- AWS — Upgrade to Kiro: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/upgrade-to-kiro.html
- AWS — Q Developer IDE plugin end of support: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html
- Kiro — Agent harness: https://kiro.dev/blog/one-agent/
- Kiro — Specs / Web: https://kiro.dev/blog/kiro-web-specs-gitlab/
- Replit — Agent: https://replit.com/ai
- Qoder — Changelog: https://qoder.com/changelog
- TRAE — TRAE Work: https://www.trae.ai/blog/trae_work_0609
- OpenCode — GitHub: https://github.com/sst/opencode
- OpenHands — GitHub: https://github.com/All-Hands-AI/OpenHands
- Cline — GitHub: https://github.com/cline/cline
- Factory — Series C: https://factory.ai/news/series-c

### Independent / Tier 2

- JetBrains — AI Coding Agents: Adoption Trends, August 2026: https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/
- Reuters — OpenAI / Cursor / SpaceX model-access dispute, August 29, 2026: https://www.reuters.com/business/media-telecom/openai-end-partnership-with-spacexs-cursor-2026-08-29/

### Benchmark supporting evidence

- SWE-bench ecosystem / agent summaries: https://www.swebench.com/
- 2026 SWE-bench agent comparison references: https://github.com/VincentTLe/coding-agent/blob/main/docs/reference/swe-bench/leaderboard-verified-may-2026.md

---

## Footnotes

[^market1]: JetBrains, “AI Coding Agents: Adoption Trends”, August 2026. Independent professional-developer survey; figures are adoption signals, not global market share.
[^market3]: Anthropic, “How AI is changing software development”, June 2026. Proprietary Claude Code usage research; not a market-wide census.
[^qoder]: Qoder official product and changelog materials, August 2026. Vendor product and scale evidence.
[^trae]: TRAE official product / TRAE Work materials, 2026. Vendor product and scale evidence.
[^cursor]: Cursor product documentation and Reuters reporting, August 2026, for product and strategic-status context.
[^qdev]: AWS documentation on Amazon Q Developer → Kiro migration and Q Developer IDE plugin end of support.
[^antigravity]: Google Antigravity documentation and Gemini CLI → Antigravity CLI migration materials, 2026.
[^benchmark]: SWE-bench public benchmark ecosystem and 2026 agent comparison references; benchmark results are supporting evidence only.
