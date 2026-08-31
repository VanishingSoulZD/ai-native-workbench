# Product 02 — Codex

> Case 001 — 2026 AI Coding Agent Landscape
> Phase: 4 — Deep Product Research
> Research cutoff: August 31, 2026
> Research unit: Product / Product Family

## 1. Product Identity

| Field | Research finding | Evidence state |
|---|---|---|
| Company | OpenAI | Confirmed |
| Product / Product Family | Codex; unified family across cloud, CLI, IDE extension and desktop app | Confirmed |
| Launch / Milestones | Cloud SWE agent launched May 16, 2025; Codex CLI followed in 2025; 2026 Codex app became a cross-platform command center for multiple agents | Confirmed |
| Target users | Professional developers, engineering teams and organizations delegating software work to agents | Confirmed |
| Primary markets | Global | Confirmed |
| Product surfaces | Codex app, CLI, IDE extension, cloud/web/GitHub-connected workflows | Confirmed |
| Business model | Included in ChatGPT plans with plan-dependent limits; team/enterprise also supports Codex-only pay-as-you-go seats for eligible plans | Confirmed |
| Status Aug 2026 | Mature multi-surface software-engineering agent with explicit multi-agent and background-work positioning | Strongly indicated |

## 2. Product Positioning

Codex is positioned less as an “AI coding assistant” and more as a **delegation and supervision system for software engineering agents**. OpenAI’s 2026 product language explicitly describes the Codex app as a command center for multiple agents, parallel work and long-running tasks. The product family therefore spans two modes: local interaction in terminal/IDE, and delegated execution in cloud/worktree environments.

The fundamental workflow change is **from synchronous coding assistance to task delegation and supervision**. Instead of keeping one agent attached to the active editor, users can assign multiple coding tasks, move work between local and cloud environments, let background jobs continue while offline, and review outcomes later.

## 3. Product Architecture

### Model layer

Codex uses OpenAI coding/reasoning models. The exact active model set changes over time, so product capability should be separated from any single model generation. OpenAI’s 2025 launch explicitly described codex-1 as a software-engineering optimized model; later product releases make model choice part of a larger Codex system.

### Agent / Harness

The product architecture is best described as **Codex harness + execution environment + tools + worktree/context primitives + user supervision surfaces**. OpenAI publicly emphasizes the system role of the app, CLI and cloud rather than exposing every internal planner component.

**Confirmed:** Cloud tasks are isolated by task environment and can iterate over code, run tests, propose PRs and report results. The app manages multiple agents in parallel.

**Unknown:** Internal planner topology, hidden evaluator design, routing heuristics and exact agent state machine are not fully public.

### Context

Context is repository-aware and can include repo files, instructions such as `AGENTS.md`, task conversation, tool outputs and persistent work state. The family is explicitly designed so that local and cloud work can share task context.

### Tools / Skills / MCP / Automations

Codex supports Skills, MCP and Automations. Skills encode team standards and workflows. Automations schedule recurring agent work such as issue triage or CI investigation. MCP extends external tool/data access.

### Runtime / Sandbox

Cloud Codex tasks run in isolated environments. The local CLI executes on the developer machine with approval modes. Worktrees provide isolated concurrent change sets. The system therefore has both **local execution** and **remote sandboxed execution**.

### Verification / Repair

The original Codex launch explicitly described agents iteratively running tests until they pass. 2026 product positioning further stresses end-to-end tasks, code review and background work. Verification remains an execution-stage loop rather than merely text-level critique.

## 4. Agent Loop

```text
Human Intent
  ↓
Task Delegation / Planning
  ↓
Repository Context + Instructions
  ↓
Reasoning
  ↓
Tool Calls / File Changes / Shell
  ↓
Build / Test / Inspect
  ↓
Observe Results
  ↓
Repair / Iterate
  ↓
Commit / PR / Report
```

For multi-agent use, an outer orchestration loop is added:

```text
Human
  ↓
Task decomposition / parallel assignment
  ↓
Agent A ─┐
Agent B ─┼─> independent worktrees/environments
Agent C ─┘
  ↓
Review queue / aggregation
  ↓
Human supervision
  ↓
Merge / ship
```

**Key distinction:** Codex makes orchestration itself a first-class product object, not just an internal implementation detail.

## 5. Workflow

| Stage | Codex role |
|---|---|
| Intent | Natural-language software goal |
| Task | Explicit delegation unit, often long-running |
| Repository | Repo + instruction files + task context |
| Agent | Local or cloud coding agent |
| Code | Multi-file edits and repository operations |
| Test | Agent runs tests/builds/checks |
| Review | User reviews outputs, diffs and PR proposals |
| Commit / PR | Git/PR artifacts and cloud handoff |
| Ongoing | Automations can repeat routine tasks on schedule |

### Workflow paradigm

**Delegated multi-surface / cloud software engineering.**

The new unit of work is the **delegated task**, and the new user role is increasingly **agent supervisor/orchestrator** rather than typist.

## 6. Capability

| Capability | State | Notes |
|---|---|---|
| Coding | Confirmed | End-to-end coding tasks |
| Repository understanding | Confirmed | Repo-aware cloud/local work |
| Planning | Confirmed | Agent task decomposition and iterative planning |
| Tool use | Confirmed | Shell/files/git plus MCP/extensions |
| Terminal | Confirmed | CLI is a first-class surface |
| Browser / external tools | Confirmed / task dependent | Internet/tool access varies by environment and configuration |
| Testing | Confirmed | Explicitly part of cloud loop |
| Debugging | Confirmed | Bug fixing and iterative repair |
| Refactoring | Confirmed | Major advertised workload |
| Context management | Confirmed | Shared task context; worktree/environment isolation |
| Long-running tasks | Confirmed | Hours/days/weeks positioning |
| Parallel / multi-agent | Confirmed | Central product proposition |
| Memory | Confirmed / partially public | Instructions and task continuity are public; exact persistent memory internals are less documented |
| MCP | Confirmed | Extensible tool/data integration |
| Skills | Confirmed | Reusable team workflows |
| Sandbox | Confirmed | Cloud isolated environments / worktrees |
| Cloud agent | Confirmed | Core product surface |

## 7. Economics

Codex is economically coupled to ChatGPT plans for many users. OpenAI’s 2026 pricing move also introduced Codex-only pay-as-you-go seats for Business and Enterprise pilots, billed on token consumption and without fixed seat rate limits; an update on June 24, 2026 stopped new PAYG Codex-only seats for Business while existing seats remained unaffected.

This creates a useful economic distinction:

- **Subscription economics:** predictable access with plan limits.
- **Agent economics:** highly variable token/runtime consumption.
- **Team economics:** organization budget and delegated-work throughput.

The latter is increasingly important because multi-agent workflows can turn one human seat into many concurrent agent workstreams.

## 8. Ecosystem

Codex inherits the OpenAI ecosystem and integrates with GitHub, IDEs and the terminal. Its Skills and MCP surfaces provide a reusable extension layer, while Automations make it possible to connect the coding agent to organizational operating rhythms such as issue triage and CI monitoring.

The strategically important ecosystem feature is **cross-surface continuity**: local terminal, IDE, desktop and cloud are increasingly different interfaces over one agentic product family.

## 9. Unique Insight

> **Codex treats agent orchestration—not code generation—as the product.**

Its strongest industry lesson is that once agents can work for hours, the bottleneck moves from “how do I prompt this agent?” to “how do I distribute, supervise, review and operationalize many agent tasks?” The desktop command-center pattern, worktrees and Automations are direct responses to that shift.

## Evidence Ledger

| Claim | Source | Date | Confidence |
|---|---|---|---|
| Codex launched as cloud SWE agent with isolated task environments and iterative testing | OpenAI — Introducing Codex | 2025-05-16 | High |
| Codex app is a command center for parallel agents and long-running tasks | OpenAI — Introducing the Codex app | 2026-02-02 | High |
| Codex spans app, CLI, IDE and cloud | OpenAI — Codex / upgrades | 2025-2026 | High |
| Skills and Automations are first-class Codex capabilities | OpenAI — Introducing the Codex app | 2026-02-02 | High |
| Codex supports token-based PAYG for team Codex-only seats, with June 24 restriction update | OpenAI — Codex flexible pricing for teams | 2026-04-02 / 2026-06-24 | High |
| Local CLI is open-source and can modify/run code locally with approval modes | OpenAI Help — Codex CLI | 2026 update | High |

### Primary Sources

- https://openai.com/index/introducing-codex/
- https://openai.com/index/introducing-the-codex-app/
- https://openai.com/index/introducing-upgrades-to-codex/
- https://openai.com/index/codex-flexible-pricing-for-teams/
- https://openai.com/codex/
- https://help.openai.com/en/articles/11096431

### Research Status

**Deep research complete.** Core operating model is well evidenced; internal planner/routing implementation remains Unknown and is not inferred.
