# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

本仓库是「AI-native 工作能力实验场」：通过真实任务、工作流与逐步工程化，训练一套使用 AI 高质量完成复杂知识工作的能力体系。完整背景叙述见 `README.md`，此处只保留对工作有约束力的部分。

核心工作链：

```text
Real Task → Problem Framing → Research → Reasoning → Judgment
→ Communication → Decision → Delivery → Evaluation → Agentization
```

两条定位约束：

- **Agentization 是成熟工作流程的产物，不是项目起点。**
- 训练目标是从 Knowledge Collector 成长为 Capability Builder，衡量标准不是工具数量或代码量。

## 核心原则

以下原则在每次工作中适用：

1. **真实任务优先** — 解决真实问题，不为展示技术制造 Demo。
2. **能力建设优先于工具数量** — 目标是建立可独立解决问题的能力。
3. **Workflow before Agent** — 先人工理解、实践、验证工作流，再 Agent 化。
4. **Human judgment remains central** — 问题定义、关键判断、最终决策和最终审查由人负责，不能交给 AI。
5. **Evaluation before Automation** — 扩大自动化之前，先建立质量验证机制。
6. **Deliverables over code volume** — 重视最终交付物，不追求代码量。
7. **Just-in-Time Learning** — 由真实任务暴露的能力缺口驱动学习，不为完成课程而学习。
8. 不为了使用新技术而使用新技术。
9. 避免过度工程化。
10. 每一次工程实现都应服务于真实工作能力的提升。

## 当前阶段与路线

当前处于**第一阶段**。阶段按顺序推进、不跳级：只有当前阶段通过真实任务完整走通后，才进入下一阶段。

### 第一阶段：先不做复杂 Agent

先由人完整走完一个 Research Case 的整个生命周期。

当前 Case：**`cases/001-ai-coding-agent-landscape/` — 2026 AI Coding Agent Landscape**

该 Case 至少形成：Research Question、Research Plan、Source Map、Evidence Matrix、Analysis、Final Report。

重点不是结论多复杂，而是完整走完研究工作的生命周期。本阶段禁止创建 Research Agent、Multi-Agent、Memory、MCP 等复杂结构。

### 第二阶段：研究 OpenAI / Anthropic 的 Research 方法

理解成熟 Research 系统在以下方面的设计与方法：问题定义、Research Planning、Source Selection、Multi-step Research、Citation、Report Generation、Agent Coordination、Evaluation、Reliability。

目标不是学 API，而是理解方法与设计思想。

### 第三阶段：Human + AI

把人工 Research 流程中适合的部分交给 AI，寻找最佳分工：

- Human 负责：Problem Framing、Research Scope、Final Judgment、Final Review。
- AI 负责：Search、Extraction、Summarization、Candidate Analysis、Draft Generation。

### 第四阶段：Research Agent

把稳定、重复、可程序化的工作自动化。第一版保持简单：

```text
Query → Plan → Search → Collect Evidence → Synthesize → Citation → Report
```

基础流程稳定后，再考虑：Dynamic Research、Parallel Agents、Evidence Store、Citation Verification、Research Evaluation。

### 第五阶段：把 Research 能力扩展到不同任务

依次用真实任务测试：Technology Research、Competitive Analysis、Product Comparison、Technical Selection、Decision Support。

观察：哪些能力通用？哪些必须领域化？

### 第六阶段：形成 Evaluation

建立 Research 质量评估体系，覆盖：Research Quality、Coverage、Source Quality、Citation Accuracy、Factual Accuracy、Contradiction Handling、Reasoning Quality、Final Answer Usefulness。

## 目录说明与维护规则

当前实际存在的核心目录：

| 目录 | 职责 |
| --- | --- |
| `cases/` | 真实任务与 Research Case，每个 Case 一个编号子目录（如 `001-ai-coding-agent-landscape/`） |
| `workflows/` | 经过实践验证的工作流程（现有 `workflows/research/`） |
| `skills/` | 可复用的 Skills |
| `agents/` | Agent 实现（当前为空，第四阶段后才会有实际内容） |
| `evaluations/` | 评估与验证（当前为空） |
| `docs/` | 项目方法论、设计决策和长期文档（现有 `decisions/`、`methodology/`、`foundation/`） |

### docs/foundation/

保存定义项目存在原因、核心目标、总体理念和长期方向的基础文档。

除非项目整体定位发生变化，否则不应随意修改其中的核心原则。

结构演化规则：

- 目录随真实任务逐步演化，**不为「看起来完整」而提前创建目录或工程结构**。
- 当一级核心目录新增、删除、重命名，或其职责发生变化时，需同步更新 `README.md` 的「仓库结构」和本文件的「目录说明」，保证二者与实际结构一致；二级目录（如 `docs/foundation/`）若影响新成员或 Claude Code 对整体结构、工作方式的理解，同样需要同步；Case 内部文件与临时实验目录不纳入同步范围。
- 不在文档中描述尚未实际建立的结构。

## 工作方式

在仓库中工作时：

1. 先判断任务属于哪个 Case / Workflow / System，在已有结构中定位。
2. 动手前先检查已有文档、工作流和项目原则；优先复用已有 Workflow / Skill，不重复创建。
3. `docs/foundation/` 中的文档属于项目基础约束：实施具体任务时，应优先遵循其中已经确定的项目定位、阶段路线和核心原则；若新的实践发现与其发生冲突，应先记录并分析冲突，再决定是否修改基础文档。
4. 未经必要性判断，不创建 Agent、Multi-Agent、Memory、MCP 或复杂架构；保持修改范围与当前阶段匹配。
5. 不为了「看起来完整」而提前实现未来阶段的功能。
6. 重大结构变化先说明设计意图，再动手。
7. 文档是项目的一等产物：研究报告、证据矩阵、决策记录与代码同等重要；最终交付体现真实工作成果，而非代码数量。
8. 本仓库目前没有代码、构建、测试或 lint 命令。后续出现时，应在相关目录的文档中记录，并补充到本文件。

## Git 提交规范

格式：`<类型>: <描述>`

类型：`research`、`analysis`、`workflow`、`feat`、`eval`、`docs`、`refactor`、`chore`、`fix`

示例：

```text
research: 完成 AI Coding Agent 信息源收集
analysis: 建立 Coding Agent 对比维度
workflow: 沉淀 Research 工作流
eval: 增加引用准确性评估
```

每次提交对应一个明确的工作成果、认知增量或工程增量；禁止 `update stuff` 这类无信息量的提交。
