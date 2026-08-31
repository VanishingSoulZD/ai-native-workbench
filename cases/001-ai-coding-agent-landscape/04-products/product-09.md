# Product 09 — Qoder

> Case 001 — 2026 AI Coding Agent Landscape
> Phase: 4 — Deep Product Research
> Research cutoff: August 31, 2026
> Research unit: Product / Product Family

## 1. Product Identity

| Field | Research finding | Evidence state |
|---|---|---|
| Company | Alibaba Cloud / Qoder | Confirmed |
| Product / Product Family | Qoder; Qoder CN is the renamed continuation of the former Tongyi Lingma coding product line; international Qoder family also includes IDE/CLI/Cloud Agents | Confirmed |
| Launch / Milestones | Qoder IDE launched Aug 2025; 2026 expanded into all-new Qoder, Quest workflow, CLI/SDK, Cloud Agents, memory, skills, plugins and connectors | Confirmed |
| Target users | Developers, teams and enterprises; increasingly non-expert users via task-centric agent workflows | Confirmed |
| Primary markets | Global + China | Confirmed |
| Product surfaces | IDE, CLI, JetBrains/VS Code ecosystem, QoderWork/CN surfaces, Cloud Agents, SDK/API | Confirmed |
| Business model | Subscription + credits; enterprise seat plans; Cloud Agent sandbox billed separately from Aug 10, 2026 | Confirmed |
| Status Aug 2026 | Rapidly expanding agentic coding platform with unusually explicit harness, memory and cloud-runtime primitives | Confirmed |

## 2. Product Positioning

Qoder has moved beyond “AI coding plugin” into a **task-centric agentic coding platform**. The current product language explicitly says work is shifting from codebases to agent tasks and from hands-on production to delegation and review.

Its distinctive workflow is the combination of:

- **Agent mode:** conversational, interruptible coding workflow;
- **Quest:** specification-driven autonomous delivery;
- **Cloud Agents:** persistent remote execution;
- **Memory:** reusable knowledge across sessions;
- **Skills/Plugins/MCP:** reusable workflow and integration layer.

The best workflow label is **IDE → cloud agent platform / persistent agent workflow**.

## 3. Product Architecture

### Model layer

Qoder advertises frontier-model aggregation and smart routing rather than locking users to one model vendor. Current docs expose model selection/routing as a product concern, separate from the agent harness.

### Agent / Harness

Qoder’s 2026 documentation is unusually explicit: the harness keeps planning, execution, verification and self-correction in a continuous loop; long-running tasks retain context, adapt to real results and can retry or roll back.

This is strong direct evidence for a product-level **agent harness** rather than merely model prompting.

### Context system

Context can include repository wiki, project instructions (`AGENTS.md`), rules, session state and persistent memory. The memory system has generation and consumption phases; learned knowledge can be written into memory files after a turn and reloaded at session initialization/refresh.

### Tools

File operations, shell, browser use, MCP, skills, plugins, code intelligence and application runtime interaction. Qoder Cloud Agents added Browser Use in Aug 2026.

### Runtime / cloud

Qoder Cloud Agents can run in Qoder Cloud containers and persist sessions for reuse across machines. Local-CLI-specific controls are not all available in cloud runtime, so the local and cloud harnesses should not be treated as identical implementations.

### Subagents / batch

Qoder supports custom agents/subagents, isolated worktree execution for batch operations and background tasks. The `/batch` skill can spawn parallel agents in isolated Git worktrees.

### Verification / repair

Built-in `/verify`, `/debug`, `/run` skills and the harness’s explicit verification/self-correction loop provide unusually direct evidence of post-execution validation. The current product also advertises proactive detection of unresolved errors, missing tests and inconsistent logic.

## 4. Agent Loop

```text
Intent
  ↓
Agent / Quest mode selection
  ↓
Repo Wiki + Rules + Memory + task context
  ↓
Planning / spec generation where applicable
  ↓
Tool selection
  ↓
Edit / shell / browser / MCP / runtime
  ↓
Observe real results
  ↓
Verify / test / run
  ↓
Self-correct / retry / rollback
  ↓
Artifact / completed task
```

Quest-specific outer loop:

```text
User requirement
  ↓
Structured requirements
  ↓
Architecture design
  ↓
Task list
  ↓
Autonomous implementation
  ↓
Validation
  ↓
Delivery
```

This is a strong example of turning **specification into executable agent plan**.

## 5. Workflow

| Stage | Qoder role |
|---|---|
| Intent | Natural-language goal |
| Task | Agent mode or Quest task |
| Repository | Repo Wiki + project context + memory |
| Agent | Local CLI/IDE or Cloud Agent |
| Code | Multi-file implementation |
| Test | Verify/run/debug skills + environment execution |
| Review | User interruption/review plus artifacts/status |
| Commit / PR | Git/GitHub integration; exact path varies by surface/CN vs global |
| Ongoing | Cloud persistence, schedules/batch and reusable memory |

### Workflow paradigm

**Persistent task-centric engineering.**

Qoder is distinctive because it explicitly combines **spec-driven planning, persistent memory and cloud execution** rather than offering them as isolated features.

## 6. Capability

| Capability | State | Notes |
|---|---|---|
| Coding | Confirmed | Full agent coding loop |
| Repository understanding | Confirmed | Repo Wiki/context |
| Planning | Confirmed | Agent planning + Quest specs |
| Tool use | Confirmed | Local/cloud tools + MCP |
| Terminal | Confirmed | CLI first-class |
| Browser / external tools | Confirmed | Browser Use + MCP |
| Testing | Confirmed | Verify/run/build/test workflows |
| Debugging | Confirmed | Built-in debug skill |
| Refactoring | Confirmed | Repo-level agent work |
| Context management | Confirmed | Rules, Wiki, memory, sessions |
| Long-running tasks | Confirmed | Cloud Agents/background tasks |
| Parallel / multi-agent | Confirmed | Batch/isolated worktrees/subagents |
| Memory | Confirmed | Native memory architecture |
| MCP | Confirmed | First-class |
| Skills | Confirmed | Built-in and custom skills |
| Sandbox | Confirmed | Cloud containers; local permissions/isolation |
| Cloud agent | Confirmed | Core product surface |

## 7. Economics

International Qoder pricing currently lists Free, Pro ($20/month), Pro+ ($60/month) and Ultra ($200/month), using monthly Credits quotas. Credit packs are also sold separately. Cloud Agent sandbox runtime began metered billing on Aug 10, 2026.

Qoder CN has a separate China pricing structure and was renamed from Tongyi Lingma on May 20, 2026. Enterprise CN plans include seat-based pricing and Credits quotas.

This is a strong example of **agent economics separating model/resource consumption from base seat subscription**. Cloud runtime introduces an additional infrastructure cost dimension.

## 8. Ecosystem

Qoder’s ecosystem includes IDE integrations, JetBrains/VS Code surfaces, GitHub repositories, 70+ plugins, thousands of skills/connectors, MCP, enterprise workspaces and cloud APIs. The ecosystem is unusually explicit about “Skills + Plugins + Connectors” as reusable system components.

China/global family convergence is strategically important because the CN lineage is not merely a localized fork; the product documentation identifies it as the renamed continuation of the former Tongyi Lingma product family.

## 9. Unique Insight

> **Qoder is one of the clearest examples of the coding agent becoming a persistent task runtime rather than a transient chat session.**

Its architecture links four layers that are often separate elsewhere: specification, memory, execution and reusable workflow modules. The result is a product closer to a lightweight **agentic development operating system** than a conventional AI IDE.

## Evidence Ledger

| Claim | Source | Date | Confidence |
|---|---|---|---|
| Current Qoder combines frontier-model routing with a harness for planning/execution/verification/self-correction | Qoder changelog | 2026-08-26 | High |
| Memory has generation/consumption phases and persists across sessions | Qoder Memory docs | 2026 | High |
| Cloud Agents run in persistent cloud containers | Qoder Cloud Agent docs | 2026 | High |
| Cloud Agent Browser Use and Batch/Schedule/Skill capabilities | Qoder Cloud Agent release notes | 2026-07 to 2026-08 | High |
| CLI exposes MCP, skills, agents, hooks, plugins and memory | Qoder slash reference | 2026 | High |
| Quest = structured requirements/design/tasks followed by autonomous execution | Qoder customer case/docs | 2026 | Medium-High |
| Qoder reached 6M+ users / 100K+ businesses | Qoder changelog | 2026-08-26 | Medium (vendor claim) |
| International pricing 20/60/200 USD plans and credits | Qoder pricing | 2026 | High |
| Qoder CN renamed from Tongyi Lingma May 20 2026 | Qoder CN billing docs | 2026-05-20 | High |

### Primary Sources

- https://qoder.com/changelog
- https://docs.qoder.com/cli/sdk/overview
- https://docs.qoder.com/cli/sdk/memory
- https://docs.qoder.com/cli/sdk/cloud-agent
- https://docs.qoder.com/cli/slash-reference
- https://docs.qoder.com/cli/builtins-reference
- https://docs.qoder.com/release-notes/cloud-agents
- https://docs.qoder.com/account/pricing
- https://docs.qoder.cn/product-overview/billing-description

### Research Status

**Deep research complete.** Qoder has unusually rich public architecture evidence. Some internal orchestration logic and implementation boundaries between local and cloud harness remain Unknown; market scale figures remain vendor claims.
