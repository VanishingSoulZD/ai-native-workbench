# Product 06 — Google Antigravity

> Case 001 — 2026 AI Coding Agent Landscape
> Phase: 4 — Deep Product Research
> Research cutoff: August 31, 2026
> Research unit: Product / Product Family

## 9.1 Product Identity

| Field | Research finding | Evidence state |
|---|---|---|
| Company | Google | Confirmed |
| Product / Product Family | Google Antigravity; modern family includes Antigravity 2.0 desktop, Antigravity CLI and related agent runtime/SDK lineage | Confirmed |
| Launch / Milestones | Evolved from Antigravity IDE/Agent Manager to standalone Antigravity 2.0 desktop in May 2026; CLI provides same harness/agent model for terminal use | Confirmed |
| Target users | Developers and teams adopting agent-first software development; enterprise users via Google Cloud | Confirmed |
| Primary markets | Global | Confirmed |
| Product surfaces | Standalone desktop, CLI, SDK/runtime, integrated browser/Chrome and cloud/enterprise integration | Confirmed |
| Business model | Product/enterprise access tied to Google/Gemini ecosystem; exact August 2026 consumer packaging is time-sensitive | Partially confirmed |
| Status Aug 2026 | Standalone agent command center rather than conventional IDE | Confirmed |

## 9.2 Product Positioning

Antigravity 2.0 is explicitly **not an IDE**. Google describes it as a standalone desktop command center for launching, steering, monitoring and orchestrating agents that perform coding and broader knowledge tasks.

This is a significant category boundary. Instead of optimizing the human’s editor interaction, Antigravity optimizes the human’s **management of asynchronous agent work**. The product supports synchronous and asynchronous interaction, artifacts, subagents, Chrome, file operations, system commands, skills and MCP.

Its workflow paradigm is therefore **agent command center + parallel asynchronous work**.

## 9.3 Product Architecture

### Model layer

Powered by Gemini model families; exact model variants can evolve. Google Cloud documentation also supports enterprise use through Gemini Enterprise Agent Platform projects.

### Agent / Harness

Google states that Antigravity CLI provides the **same harness and agent** as Antigravity 2.0, with a terminal-oriented experience. This is unusually strong public evidence that the desktop and CLI are surfaces over a shared agent runtime.

### Context

Context consists of project/repository files, instructions/configuration, skills, MCP integrations, tool outputs and artifacts. The CLI and desktop share authentication, context, skills and configurations.

### Tools

System commands, file read/write, web search, Chrome interaction, MCP-connected tools and skills. Subagents can be launched and monitored.

### Runtime / sandbox

Antigravity includes terminal sandboxing and enterprise cloud controls. Exact low-level runtime isolation mechanisms are only partially documented.

### Subagents / plugins

A plugin is a bundle that can contain skills, agents, rules, MCP servers and hooks. `/agents` acts as an agent manager and monitors background subagents.

### Verification

The product emphasizes **artifacts as the verification surface**: agents can create implementation plans, code changes and other artifacts; users inspect them and provide feedback. Coding tasks can include system execution and testing, but a full internal evaluator architecture is not public.

## 9.4 Agent Loop

```text
Human intent
  ↓
Task planning / agent selection
  ↓
Context + skills + MCP
  ↓
Agent reasoning
  ↓
Code / shell / browser execution
  ↓
Artifacts + execution results
  ↓
Human feedback / verification
  ↓
Repair / continuation
  ↓
Completed artifact / code change
```

Parallel loop:

```text
High-level goal
  ↓
Spawn subagents / background agents
  ↓
Concurrent execution
  ↓
Monitor status / inspect artifacts
  ↓
Intervene selectively
```

The second loop is as important as the first.

## 9.5 Workflow

| Stage | Antigravity role |
|---|---|
| Intent | High-level task or knowledge/coding request |
| Task | Agent work item |
| Repository | Project files and context |
| Agent | Desktop/CLI agent with shared harness |
| Code | File edits and command execution |
| Test | Environment execution and inspection |
| Review | Artifacts, events and user feedback |
| Commit / PR | Possible through standard tooling; exact delivery depends on repo integrations |
| Ongoing | Background subagents and asynchronous orchestration |

### Workflow paradigm

**Agent command center.**

Google is treating “agent supervision” as a first-class product surface, closer to an operations console than a coding editor.

## 9.6 Capability

| Capability | State | Notes |
|---|---|---|
| Coding | Confirmed | Complex coding tasks |
| Repository understanding | Confirmed | Project/file context |
| Planning | Confirmed | Plans/artifacts and agent reasoning |
| Tool use | Confirmed | System/file/web/Chrome/MCP |
| Terminal | Confirmed | Native CLI surface |
| Browser / external tools | Confirmed | Chrome + MCP |
| Testing | Confirmed / task-dependent | Execution environment available |
| Debugging | Confirmed | Agent execution/iteration |
| Refactoring | Confirmed | Product examples include refactoring |
| Context management | Confirmed | Shared context/config/skills across surfaces |
| Long-running tasks | Confirmed | Asynchronous/background model |
| Parallel / multi-agent | Confirmed | Subagents and parallel orchestration |
| Memory | Partially confirmed | Context/config persistence; general semantic long-term memory semantics are less explicit |
| MCP | Confirmed | First-class |
| Skills | Confirmed | Plugin/skill system |
| Sandbox | Confirmed / internal detail limited | Terminal sandbox is documented |
| Cloud agent | Partially confirmed | Enterprise runtime exists; product is primarily desktop/CLI command center |

## 9.7 Economics

Antigravity is tied to Google’s broader Gemini and Google Cloud ecosystem. Consumer/individual pricing is less central to its architecture than Google’s distribution through Gemini and enterprise cloud infrastructure.

Enterprise teams can route agent inference through Google Cloud’s Agent Platform, with regional model endpoints and Google Cloud privacy controls. This creates an enterprise deployment path in which agent usage becomes part of existing cloud procurement and security boundaries.

## 9.8 Ecosystem

Antigravity benefits from Google’s Gemini ecosystem, Chrome/browser integration, Google Cloud, MCP and a plugin architecture that bundles agents, skills, rules, hooks and MCP.

The explicit migration lineage from Gemini CLI toward Antigravity CLI is also ecosystem-significant: it reduces fragmentation inside Google’s coding-agent stack and brings an established CLI developer community into the new product family.

## 9.9 Unique Insight

> **Antigravity’s key innovation is replacing the IDE as the primary human interface with an agent operations console.**

It makes a conceptual bet that as coding agents become autonomous, the limiting factor is no longer typing code efficiently but **launching, monitoring, steering and evaluating multiple asynchronous agents**.

This is a distinct workflow paradigm from both Claude Code’s terminal-first loop and Cursor’s IDE-to-cloud evolution.

## Evidence Ledger

| Claim | Source | Date | Confidence |
|---|---|---|---|
| Antigravity 2.0 is a standalone desktop app and not an IDE | Antigravity Blog — Introducing Antigravity 2.0 | 2026-05-19 | High |
| CLI uses same harness/agent and shares context, skills and configuration | Google Cloud Blog — I/O 26 agent developer news | 2026-05 | High |
| Agents can run synchronously/asynchronously and orchestrate complex coding tasks | Antigravity 2.0 Blog / Docs | 2026 | High |
| Plugins bundle skills, agents, rules, MCP servers and hooks | Antigravity CLI Features | 2026 | High |
| `/agents` monitors and controls concurrent background subagents | Antigravity CLI Agents command | 2026 | High |
| Enterprise deployment through Gemini Enterprise Agent Platform | Google Cloud Blog | 2026 | High |
| Gemini CLI → Antigravity CLI migration lineage | Phase 2 evidence / Google developer materials | 2026 | High |

### Primary Sources

- https://www.antigravity.google/blog/introducing-google-antigravity-2
- https://www.antigravity.google/docs/overview
- https://www.antigravity.google/docs/cli/features
- https://www.antigravity.google/docs/cli/commands/agents/
- https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud

### Research Status

**Deep research complete.** Agent-command-center, shared harness and subagent architecture are well evidenced. Internal planning/evaluation logic and detailed consumer economics remain Unknown/partially public.
