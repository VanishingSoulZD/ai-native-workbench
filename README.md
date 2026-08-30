# AI Native Workbench

> 通过真实任务、工作流与逐步工程化，构建个人 AI-native 工作能力。

## 项目定位

`ai-native-workbench` 是一个长期的个人实践项目。

它不是单纯的 AI 工具收藏，也不是单纯的 Research Agent 项目，而是一个用于训练和沉淀 **AI-native 工作能力** 的实验场。

我希望通过真实任务，逐渐建立一套能够使用 AI 高质量完成复杂知识工作的工作方法：

```text
发现问题
↓
定义问题
↓
研究
↓
分析
↓
判断
↓
沟通
↓
决策
↓
交付
↓
验证
↓
工程化
```

最终希望形成的不是一堆孤立的 GitHub 项目，而是一套可以迁移到不同工作和生活场景中的 AI-native 工作系统。

---

## 核心模型

本项目的核心工作链：

```text
Problem Framing
      ↓
Research
      ↓
Reasoning
      ↓
Judgment
      ↓
Communication
      ↓
Decision
      ↓
Delivery
      ↓
Evaluation
      ↓
Agentization
```

其中：

> **Agent 应该是成熟工作流程的产物，而不是工作流程的起点。**

因此项目遵循：

> **先成为一个优秀的 AI-native Worker，再把优秀的工作方式变成 Agent。**

---

## 核心原则

### 1. 真实任务优先

优先解决真实问题，而不是为了展示技术而制造 Demo。

### 2. 能力优先于工具

目标不是掌握尽可能多的 AI 工具，而是建立可以独立解决问题的能力。

### 3. Workflow before Agent

先理解、实践和验证工作流，再考虑 Agent 化。

### 4. Human Judgment remains central

问题定义、关键判断、最终决策和最终审查仍然由人负责。

### 5. Evaluation before Automation

在扩大自动化之前，先验证工作质量。

### 6. Deliverables over Code Volume

重视最终交付物，而不是代码量。

### 7. Just-in-Time Learning

以真实任务暴露出的能力缺口驱动学习：

```text
真实问题
↓
暴露能力缺口
↓
针对性学习
↓
解决问题
↓
沉淀能力
```

---

## 当前项目阶段

项目按照以下六个阶段逐步推进。

### 第一阶段：先不做复杂 Agent

先人工完成完整 Research Case。

第一个 Case：

> **2026 AI Coding Agent Landscape**

至少形成：

```text
Research Question
Research Plan
Source Map
Evidence Matrix
Analysis
Final Report
```

这一阶段的重点不是研究结论本身，而是完整走完一次真实研究工作的生命周期。

---

### 第二阶段：研究 OpenAI / Anthropic 的 Research 方法

重点研究成熟 Research 系统如何处理：

```text
问题定义
↓
Research Planning
↓
Source Selection
↓
Multi-step Research
↓
Citation
↓
Report Generation
↓
Agent Coordination
↓
Evaluation
↓
Reliability
```

目标不是简单学习 API，而是理解其 Research 方法和系统设计思想。

---

### 第三阶段：Human + AI

逐步将人工 Research 流程中的部分工作交给 AI。

Human 主要负责：

```text
Problem Framing
Research Scope
Final Judgment
Final Review
```

AI 主要负责：

```text
Search
Extraction
Summarization
Candidate Analysis
Draft Generation
```

目标是找到 Human 与 AI 的最佳工作分工。

---

### 第四阶段：Research Agent

把稳定、重复、可程序化的工作进行自动化。

第一版保持简单：

```text
Query
↓
Plan
↓
Search
↓
Collect Evidence
↓
Synthesize
↓
Citation
↓
Report
```

在基础流程稳定后，再逐步考虑：

```text
Dynamic Research
Parallel Agents
Evidence Store
Citation Verification
Research Evaluation
```

---

### 第五阶段：把 Research 能力扩展到不同任务

逐步测试：

```text
Technology Research
↓
Competitive Analysis
↓
Product Comparison
↓
Technical Selection
↓
Decision Support
```

核心问题：

> 哪些能力可以通用？

> 哪些能力必须领域化？

通过真实任务判断 Research Architecture 的通用边界。

---

### 第六阶段：形成 Evaluation

建立 Research 工作和 Research Agent 的质量评估体系：

```text
Research Quality
├── Coverage
├── Source Quality
├── Citation Accuracy
├── Factual Accuracy
├── Contradiction Handling
├── Reasoning Quality
└── Final Answer Usefulness
```

最终将 Evaluation 与后续更广泛的 LLM / Agent Evaluation 能力连接起来。

---

## 第一个 Case

### 001 — 2026 AI Coding Agent Landscape

第一个 Case 选择 AI Coding Agent Landscape，并不是因为这个项目最终要成为一个“AI Coding Agent 研究项目”。

真正的目标是训练：

```text
Problem Framing
→ Research
→ Evidence
→ Reasoning
→ Writing
→ Delivery
→ Evaluation
→ Automation
```

研究对象只是训练这些能力的第一个真实任务。

---

## 仓库结构

```text
ai-native-workbench/
│
├── README.md
├── CLAUDE.md
│
├── cases/
│   └── 001-ai-coding-agent-landscape/
│
├── workflows/
│   └── research/
│
├── skills/
│
├── agents/
│
├── evaluations/
│
└── docs/
    └── foundation/
```

目录职责：

| 目录           | 作用                       |
| -------------- | -------------------------- |
| `cases/`       | 真实任务与 Research Case   |
| `workflows/`   | 经过实践验证的工作流程     |
| `skills/`      | 可复用的 Skills            |
| `agents/`      | Agent 实现                 |
| `evaluations/` | 评估与验证                 |
| `docs/`        | 方法论、设计决策和长期文档 |
| `docs/foundation/` | 项目背景、核心理念与总体方法 |

项目不会为了“看起来完整”而提前实现所有目录中的内容。

目录将随着真实任务逐步演化。

---

## 项目推进方式

这个仓库遵循：

```text
Real Task
↓
Human Work
↓
AI Collaboration
↓
Workflow
↓
Evaluation
↓
Automation
↓
Agent / Skill / System
```

也就是说：

> 不先决定“我要做什么 Agent”，而是先找到值得解决的真实工作问题。

---

## Git 提交规范

采用简洁的 Conventional-style 提交格式：

```text
<类型>: <描述>
```

常用类型：

```text
research
analysis
workflow
feat
eval
docs
refactor
chore
fix
```

示例：

```text
research: 完成 AI Coding Agent 信息源收集
analysis: 建立 Coding Agent 对比维度
workflow: 沉淀 Research 工作流
eval: 增加引用准确性评估
docs: 更新项目阶段说明
feat: 实现第一版 Research Workflow
```

一次提交尽量对应一个明确的：

> **工作成果、认知增量或工程增量。**

详细规则与 Claude Code 工作规范见 `CLAUDE.md`。

---

## 长期目标

最终希望形成的不是：

> “一个会使用很多 AI 工具的人”

也不是：

> “一个会开发 Research Agent 的人”

而是：

> **一个能够定义问题、独立研究、利用 AI、形成判断、完成高质量交付，并能够进一步把稳定工作流程工程化的人。**

即：

```text
AI-Native Worker
        ↓
AI-Native Workflow
        ↓
AI-Native Work System
        ↓
Agent / Skills / Automation
```

这套能力最终可以迁移到：

```text
职业工作
项目开发
技术研究
产品分析
决策支持
学习
生活决策
```

---

## 当前状态

> **阶段：第一阶段**

> **当前 Case：001 — 2026 AI Coding Agent Landscape**

> **当前原则：先人工完成完整 Research Workflow，不做复杂 Agent。**

---

## 项目精神

> **先成为一个优秀的 AI-native Worker，再把优秀的工作方式变成 Agent。**
