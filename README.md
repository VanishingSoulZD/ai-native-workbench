# AI Native Workbench

> 通过真实任务，学习、实践和沉淀 AI 原生工作能力。

## 项目使命

`ai-native-workbench` 是一个用于培养个人 **AI-native Work Capability** 的长期实践实验场。

项目的核心目标不是构建某一个 AI Agent、Research System 或 AI 工具产品，而是通过真实工作任务，系统学习如何利用整个 AI 生态完成复杂工作，并逐步形成可迁移的 AI-native 工作能力。

我希望最终建立的能力是：

```text
面对一个真实问题
↓
理解问题需要什么能力
↓
判断应该使用什么 AI
↓
选择合适的具体产品 / 模型 / 模式
↓
正确配置 AI 的工作方式
↓
调度多个 AI 工具协同工作
↓
获得可验证的工作产物
↓
形成判断并完成高质量交付
```

最终希望形成的不是：

> “我会使用很多 AI 工具。”

也不是：

> “我开发了一个 Research Agent。”

而是：

> **面对不同类型的真实工作，我知道什么问题应该交给什么 AI，并且知道如何调度整个 AI 生态把问题做好。**

---

## 核心工作模型

项目围绕以下工作链展开：

```text
Real Task
    ↓
Problem Framing
    ↓
AI Work Planning
    ↓
AI Capability Selection
    ↓
AI Product / Model Selection
    ↓
AI Tool Configuration
    ↓
AI Orchestration
    ↓
Artifacts / Evidence
    ↓
Human Judgment
    ↓
Final Delivery
    ↓
Evaluation
```

其中：

> **AI Work Planning 决定如何利用 AI，具体工作由现有 AI 工具完成。**

> **固定的是 AI 调度与选择的方法，不固定“永远应该使用哪个 AI 产品”。**

> **AI Work Advisor 应根据当前任务主动获取和核查最新的 AI Ecosystem Knowledge，再生成具体的 Case-specific AI Work Plan。**

---

## 核心原则

### 1. Real Work First

优先解决真实问题，而不是为了展示技术而制造 Demo。

### 2. Capability over Tool

目标不是掌握尽可能多的 AI 工具，而是建立可以独立解决问题的 AI-native 工作能力。

### 3. Orchestration over Memorization

学习的不是固定的“任务 → 产品”映射，而是如何根据任务能力、当前 AI 生态和实际约束选择并配置最合适的工具。

### 4. Existing AI over Rebuilding AI

优先利用已经存在的优秀 AI 产品和服务解决问题，而不是重新实现已经成熟的能力。

### 5. Human Judgment remains Central

问题定义、关键判断、最终决策和最终审查仍然由人负责。

### 6. Evidence Before Assertion

对于需要研究、分析和决策支持的工作，重要结论应有可追溯的证据或明确的依据。

### 7. Deliverables over Code Volume

重视真实工作成果、证据、判断和交付，而不是代码量。

### 8. Just-in-Time Learning

以真实任务驱动能力学习，而不是脱离实际工作进行大规模工具学习。

---

## AI Work Guidance

项目采用以下工作指导关系：

```text
Research Charter
        +
AI Work Advisor Prompt
        +
Current AI Ecosystem Knowledge
        ↓
Case-specific AI Work Plan
        ↓
Actual AI Tool Execution
```

### Research Charter

回答：

> **我们要解决什么问题？**

它负责定义研究或工作目标、范围、对象、约束、成功标准和交付要求。

### AI Work Advisor Prompt

回答：

> **应该如何利用整个 AI 生态解决这个问题？**

它不是一个硬编码的工具说明书，而是一套 AI 工作调度与选择方法。

Advisor 应主动分析当前任务需要什么能力，并在涉及实时变化的产品、模型、套餐、入口、功能和可用性时主动获取最新信息，再比较候选 AI 工具和配置方案。

### Case-specific AI Work Plan

回答：

> **这个 Case 的每个阶段、步骤和任务，具体应该由什么 AI 完成，以及应该怎样配置和衔接？**

Work Plan 可以明确到：

```text
Stage
Step
Task
AI Capability
Specific Product
Model
Mode / Thinking
Session Strategy
Context Strategy
Files
Connectors
Skills
Prompt / Instruction Strategy
Expected Artifact
Handoff
Verification
Reasoning for Selection
Rejected Alternatives
```

它是实际执行的工作计划，而不是一个需要通过不断试错才能逐渐形成的宽泛初版方案。

---

## Research 在项目中的位置

Research 是 `ai-native-workbench` 的重要能力实验场，但不是整个项目的唯一目标。

项目将通过真实 Research Case 训练：

```text
Problem Framing
→ Research
→ Evidence
→ Analysis
→ Judgment
→ Writing
→ Delivery
→ Evaluation
```

Research System、Research Runtime、Canonical Knowledge 等工程化工作，属于 Research 能力的一部分；它们不再代表整个项目的总体方向。

项目当前阶段优先学习如何利用现有 AI 产品完成真实工作，而不是优先构建新的 Research Agent、自动化平台或通用执行基础设施。

---

## 学习与实践路径

项目通过不同真实任务逐步建立 AI-native 工作能力。

### Case 001 — AI Coding Agent Landscape

第一个 Case 聚焦 AI Coding Agent，并训练：

```text
Research
Evidence
Comparison
Evaluation
AI Coding Workflow
```

它研究的是 AI Coding Agent，但更重要的是训练如何使用 AI 完成复杂技术研究与分析。

### Case 002 — AI Work Agent / AI Office Agent Landscape

第二个 Case 聚焦 Work / Office / Knowledge Work 类 AI 产品。

核心目标不仅是形成：

```text
Global Top 10
China Top 5
```

还要建立对不同 Work AI 的实际工作定位、适用任务、使用方式和调度方法的理解。

### Case 003 — 2026 AI Model / Subscription / Coding Plan / Token Plan

研究国内外主流 AI 模型、产品能力、订阅体系、Coding Plan、Token Plan、上下文、推理、多模态和实际使用成本。

目标是建立模型与产品选择能力。

### Case 004 — Deep Research Landscape

研究国内外主流 AI 厂商提供的 Deep Research 能力。

目标是建立：

```text
什么时候应该使用 Deep Research
哪个产品更适合当前问题
如何进入和配置
如何与 Chat / Work / Coding Agent 协同
```

### 后续 Cases

继续扩展到更多 AI-native work 场景，例如：

```text
Image Generation
Video Generation
Data Analysis
Knowledge Management
Document Work
Presentation
Automation
其他前沿 AI 工作场景
```

这些 Case 的目的不是单纯收集产品信息，而是持续训练：

> **“什么问题应该交给什么 AI，以及如何调度整个 AI 生态。”**

---

## Case 工作方式

新的研究或复杂工作任务，原则上采用以下流程：

```text
新任务
↓
Research Charter Discussion
↓
Research Charter
↓
AI Work Advisor
↓
Case-specific AI Work Plan
↓
实际 AI 工具执行
↓
Artifacts / Evidence
↓
Human Judgment
↓
Final Delivery
↓
Evaluation
```

因此，一个 Case 不仅记录“研究出了什么”，还记录“为了完成这个任务，AI 应该如何被调度”。

---

## AI 生态

项目不预设某个厂商或产品永久占据某个工作环节。

可能参与实际任务的 AI 包括但不限于：

```text
Chat / Reasoning
├── ChatGPT
├── Claude
├── Gemini
├── DeepSeek
├── Qwen
├── Kimi
└── 其他模型 / 产品

Coding Agents
├── Codex
├── Claude Code
├── Qoder
├── Trae
├── CodeBuddy
└── 其他 Coding Agents

Work / Office Agents
├── ChatGPT Work
├── Claude Work / Cowork
├── Gemini / Google Workspace
├── Microsoft 365 Copilot / Cowork
├── 国内 Work / Office Agents
└── 其他产品

Research
├── OpenAI Deep Research
├── Claude Research
├── Gemini Deep Research
├── Perplexity Research
├── 国内 Deep Research
└── 其他研究工具

Creation
├── Image AI
├── Video AI
└── 其他多模态工具
```

具体产品选择由当前任务的 AI Work Advisor 决定，并应结合最新能力和使用条件，而不是由项目仓库预先硬编码固定答案。

---

## 仓库结构

```text
ai-native-workbench/
│
├── README.md
├── CLAUDE.md
│
├── cases/
│   ├── 001-ai-coding-agent-landscape/
│   ├── 002-ai-work-agent-landscape/
│   └── ...
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
    ├── foundation/
    ├── methodology/
    └── superpowers/
```

目录职责：

| 目录 | 作用 |
| --- | --- |
| `cases/` | 真实任务与 Research / Work Case |
| `workflows/` | 经过实践验证的工作流程 |
| `skills/` | 可复用的 Skills |
| `agents/` | Agent 实现与实验 |
| `evaluations/` | 评估与验证 |
| `docs/` | 方法论、设计决策和长期文档 |

项目不会为了“看起来完整”而提前实现所有目录中的内容。

---

## 项目推进原则

仓库遵循：

```text
Real Task
↓
Human + AI Collaboration
↓
AI Work Planning
↓
AI Tool Orchestration
↓
Artifacts / Evidence
↓
Human Judgment
↓
Final Delivery
↓
Evaluation
```

项目不要求为了形成工作能力而开发新的 AI 产品。

只有当真实工作明确需要新的工程能力时，才考虑增加代码、自动化、Skill、Agent 或其它系统能力。

---

## 长期目标

最终希望形成的不是一个独立的软件产品，而是一套可以迁移到不同工作和生活场景中的个人 AI-native 工作能力：

```text
AI Task
    ↓
Task Understanding
    ↓
AI Capability Selection
    ↓
AI Product / Model Selection
    ↓
AI Configuration
    ↓
AI Orchestration
    ↓
Evidence / Artifacts
    ↓
Human Judgment
    ↓
High-quality Delivery
```

最终形成：

> **知道什么问题应该交给什么 AI。**

以及：

> **学会调度整个 AI 生态。**

---

## 当前状态

> **项目方向已更新：以真实任务驱动 AI-native 工作能力建设。**

> **当前下一阶段：Case 002 — AI Work Agent / AI Office Agent Landscape。**

> **Research Runtime v1：作为 Research 能力的工程探索保留，当前不继续沿着 Runtime 扩张作为项目主线。**

---

## 项目精神

> **先成为一个优秀的 AI-native Worker，再决定哪些工作值得进一步工程化。**
