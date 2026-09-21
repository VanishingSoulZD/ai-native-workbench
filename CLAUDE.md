# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

本仓库是「AI-native 工作能力实验场」：

> **通过真实任务，学习、实践和沉淀 AI 原生工作能力。**

项目不是以构建某个 Research Agent、AI Agent 或自动化平台为目的，而是训练如何利用当前 AI 生态完成真实复杂工作，并把经过验证、稳定且有价值的工作方式逐步工程化。

## 核心工作链

~~~text
Real Task
→ Problem Framing
→ Research Charter
→ AI Work Planning
→ AI Capability / Product / Model Selection
→ AI Tool Configuration
→ AI Orchestration
→ Artifacts / Evidence
→ Human Judgment
→ Final Delivery
→ Evaluation
~~~

核心能力目标：

1. **AI Task → AI Selection** — 从真实任务识别所需能力，并选择合适的 AI。
2. **AI Selection → AI Orchestration** — 决定一个还是多个 AI、如何配置、如何交接、如何验证。

固定的是选择与调度的方法，不是永久的产品映射。

## 核心原则

1. **真实任务优先** — 解决真实问题，不为展示技术制造 Demo。
2. **能力优先于工具数量** — 目标是建立可迁移的工作能力，而不是收集产品。
3. **Current over Memorized** — 产品、模型、套餐、功能、入口等可能变化的信息需要按需获取并核查。
4. **Capability over Brand** — 先识别需要什么能力，再比较具体产品。
5. **Minimal Effective Tool Set** — 一个 AI 足够时，不增加第二个 AI；不要为了“完整”堆工具。
6. **Existing AI over Rebuilding** — 已有 AI 能可靠完成的工作，不优先自建等价系统。
7. **Human judgment remains central** — 人负责问题定义、范围、关键判断、最终决策和最终审查。
8. **Evidence before Assertion** — 重要事实与判断尽量有可追溯证据。
9. **Workflow before Agent** — 先通过真实工作验证方法，再决定哪些部分值得工程化。
10. **Deliverables over code volume** — 重视实际交付物、证据和结果，不追求代码量。
11. **Just-in-Time Learning** — 由真实任务暴露的能力缺口驱动学习。
12. **避免过度工程化** — 任何工程实现都必须服务于真实工作能力。

## AI Work Guidance

标准规划关系：

~~~text
Research Charter
        ↓
AI Work Advisor Prompt
        ↓
AI Work Plan
        ↓
Actual Execution
~~~

### Research Charter

负责定义 **What / Why**：objective、research questions、scope、population、definitions、inclusion / exclusion、comparison / ranking、evidence requirements、cutoff、deliverables、success criteria、human decisions。

### AI Work Advisor

使用路径：docs/methodology/ai-work-advisor-v1.md

它负责 **How**：根据具体任务动态研究当前 AI 生态，进行能力、产品、模型、配置和编排决策。

不要把 Advisor 变成永久产品目录、Global Playbook 或固定的“任务 → 产品”映射。

### AI Work Plan

使用路径：docs/methodology/templates/ai-work-plan.md

它是 case-specific execution manual，回答每个重要 Task：用什么 AI、为什么、怎么配置、输入是什么、产物是什么、如何交接、如何验证、哪些责任仍由人承担。

### Session Templates

Research Charter Discussion：docs/methodology/templates/research-charter-discussion-session.md
AI Work Plan Generation：docs/methodology/templates/ai-work-plan-generation-session.md

两者分别负责“定义问题”和“生成执行计划”，不要在 Charter Session 中提前选工具，也不要在 Work Plan Session 中执行实际研究。

## Research System / Runtime 边界

Research 是项目的重要能力实验场，但不是整个项目的顶层身份。

### Research System

docs/methodology/research-system-v1.md

负责研究方法与研究语义，包括 Research lifecycle、evidence-first methodology、canonical research knowledge、evaluation、reproducible research delivery。

### Research Runtime

docs/architecture/research-runtime-v1.md

负责已经进入 Research execution context 后的运行时机制，包括 execution state、workflow coordination、artifacts、gates、control。

Research Runtime 不负责当前 AI 生态发现、用户级 AI 产品选择、模型选择、Session / Connector / Skill 等上层 AI 调度决策，也不维护永久 AI 产品 Playbook。

### Workflow Core

Workflow Core 保持 domain-agnostic。不要把 model selection、product selection、AI brand mapping、user-level orchestration methodology、session policy、tool-selection policy 塞进 Workflow Core。

## 当前项目推进方式

项目以真实任务驱动，而不是按固定的 Research Agent 阶段路线推进。

标准新 Research / 复杂知识工作流程：

~~~text
真实任务
↓
Problem Framing
↓
Research Charter
↓
AI Work Plan Generation
↓
Human Review
↓
Actual AI Execution
↓
Artifacts / Evidence
↓
Human Judgment
↓
Final Delivery
↓
Evaluation
~~~

当前不要求先完成 Research Agent，也不要求先完成未来的 Runtime 扩张。

只有当真实工作明确暴露出稳定、重复且值得工程化的问题时，才考虑增加 Workflow、Skill、Agent、Automation 或 System。

## 目录说明与维护规则

当前实际存在的核心目录：

| 目录 | 职责 |
| --- | --- |
| cases/ | 真实任务与 Research Case |
| workflows/ | 经过实践验证的工作流程 |
| skills/ | 可复用的 Skills |
| agents/ | Agent 实现与实验 |
| evaluations/ | 评估与验证 |
| docs/ | 方法论、设计决策和长期文档 |

目录随真实任务逐步演化，不为“看起来完整”而提前创建结构。
当一级核心目录新增、删除、重命名或职责发生变化时，同步更新 README 与本文件。
不在文档中描述尚未实际建立的结构。

## 工作方式

在仓库中工作时：

1. 先判断任务属于哪个 Case / Workflow / System，并读取相关文档。
2. 对 Research Case 优先使用 Research Charter → AI Work Plan 的规划链。
3. 对复杂 AI-assisted work，优先使用 AI Work Advisor；不要直接凭记忆指定产品。
4. 涉及变化快的产品、模型、价格、入口、功能和限制时，主动获取当前信息并保留不确定性。
5. 优先使用最小有效工具集；一个 AI 足够时不要为了编排而编排。
6. 不未经必要性判断创建 Agent、Multi-Agent、Memory、MCP 或复杂基础设施。
7. 不扩展 Research Runtime，除非真实 Research 工作已经证明需要该能力。
8. 文档是项目的一等产物；研究报告、证据矩阵、决策记录、Work Plan 与代码同等重要。
9. 重大结构变化先说明设计意图，再动手。
10. 如果新的实践发现与 foundation 文档发生冲突，先记录并分析，再决定是否修改基础约束。

## Git 提交规范

格式：<类型>: <描述>

类型：research、analysis、workflow、feat、eval、docs、refactor、chore、fix

示例：
~~~text
research: 完成 AI Coding Agent 信息源收集
analysis: 建立 Coding Agent 对比维度
workflow: 沉淀 Research 工作流
eval: 增加引用准确性评估
docs: 对齐 AI-native workbench 项目指导
~~~

每次提交对应一个明确的工作成果、认知增量或工程增量；禁止使用无信息量的提交说明。