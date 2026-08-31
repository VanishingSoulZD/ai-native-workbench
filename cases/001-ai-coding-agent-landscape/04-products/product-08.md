# Product 08 — OpenCode

> Case 001 — 2026 AI Coding Agent Landscape
> Phase: 4 — Deep Product Research
> Research cutoff: August 31, 2026
> Research unit: Product / Product Family

## 1. Product Identity

| Field | Research finding | Evidence state |
|---|---|---|
| Company / steward | OpenCode / anomalyco / SST ecosystem | Confirmed at project level |
| Product / Product Family | OpenCode open-source coding agent, with terminal TUI and desktop client plus client/server architecture | Confirmed |
| Launch / Milestones | Open-source terminal coding agent; by 2026 added desktop surface, configurable agents, broad provider support and increasingly mature extension model | Confirmed |
| Target users | Developers who want open-source, provider-agnostic, terminal-first coding agents | Confirmed |
| Primary markets | Global, open-source community | Confirmed |
| Product surfaces | CLI/TUI, desktop; client/server architecture supports remote driving | Confirmed |
| Business model | Open-source MIT software; optional OpenCode Zen pay-as-you-go model routing | Confirmed |
| Status Aug 2026 | One of the most significant open-source agent harnesses, with large GitHub/community adoption | Confirmed |

## 2. Product Positioning

OpenCode is best understood as an **open agent harness**, rather than simply an open-source alternative UI to Claude Code.

Its key strategic decisions are: provider agnosticism, first-class terminal/TUI UX, open configuration, built-in agent modes, LSP support and a client/server architecture. This makes the harness itself the product surface of interest.

The workflow paradigm is **Open, provider-agnostic terminal agent harness**. It demonstrates that the agent layer can be decoupled from the model vendor and can function as infrastructure-like software for developers.

## 3. Product Architecture

### Model layer

OpenCode supports many providers including OpenAI, Anthropic, Google, Bedrock, Azure OpenAI, OpenRouter, xAI and OpenAI-compatible endpoints. Optional OpenCode Zen supplies a curated provider/route layer with pay-as-you-go prices.

### Agent / Harness

OpenCode has primary agents such as Build and Plan plus subagents. Agents have configurable prompts, tools/permissions and model selection. This creates a transparent, user-modifiable agent layer.

### Context

Repository files, search results, LSP information, tool output and configuration feed the agent. Because the software is open source, the exact context assembly is inspectable in the repository rather than limited to vendor documentation.

### Tools

Read/edit, glob/grep, bash, web fetch/search, LSP, task/subagent, skill and related tools. Permission configuration determines what each agent can use.

### Runtime

The main runtime is local/terminal-oriented. Client/server architecture allows the TUI/frontend to be separated from the coding-agent process, enabling remote clients such as mobile control patterns.

### Memory / rules / skills / MCP

OpenCode supports project configuration and reusable skills, and its agent definitions can specify allowed tools and models. MCP integrates external services. The open-source architecture makes these boundaries explicit and inspectable.

**Unknown / partial:** compared with Qoder/Devin, a first-class semantic long-term memory system is not the product's defining documented primitive; persistent context is mainly configuration/project artifacts and session mechanisms.

### Verification

The Plan agent is read-only and intended for analysis/review; Build has full tool access. This creates an explicit “analysis → execution” separation. Runtime commands/tests are performed by the agent through the terminal tool loop.

## 4. Agent Loop

```text
Task
  ↓
Build or Plan agent selection
  ↓
Context gathering
  ↓
Reasoning
  ↓
Read/search/LSP
  ↓
Edit/bash/web/task tools
  ↓
Observe results
  ↓
Test / inspect
  ↓
Repair / iterate
  ↓
Final patch / artifact
```

Subagent loop:

```text
Main agent
  ↓
@general / custom subagent
  ↓
Independent task context + restricted tools
  ↓
Result summary
  ↓
Main agent continues
```

## 5. Workflow

| Stage | OpenCode role |
|---|---|
| Intent | Natural-language task in terminal |
| Task | Agent session |
| Repository | Local repository + LSP/search |
| Agent | Build / Plan / custom agents |
| Code | Multi-file edits |
| Test | Bash/tool execution |
| Review | Plan agent, diffs, terminal output |
| Commit / PR | User-controlled Git workflow |
| Ongoing | Sessions/client-server; external automation possible |

### Workflow paradigm

**Open, provider-agnostic terminal agent harness.**

OpenCode is notable because its main competitive moat is not model ownership or hosted infrastructure but **control over the harness layer**.

## 6. Capability

| Capability | State | Notes |
|---|---|---|
| Coding | Confirmed | Repo-level coding agent |
| Repository understanding | Confirmed | Search/LSP/files |
| Planning | Confirmed | Dedicated Plan agent |
| Tool use | Confirmed | Large built-in tool set |
| Terminal | Confirmed | Core UX |
| Browser / external tools | Confirmed / extensible | Web tools + MCP |
| Testing | Confirmed | Bash/environment |
| Debugging | Confirmed | Tool-driven iterative loop |
| Refactoring | Confirmed | General repo changes |
| Context management | Confirmed | Context/tool architecture is open |
| Long-running tasks | Partially confirmed | Session/runtime supports extended work; no equivalent cloud fleet is core product |
| Parallel / multi-agent | Confirmed / extensible | Subagents; architecture supports multiple agent types |
| Memory | Partially confirmed | Not a defining first-class semantic memory layer |
| MCP | Confirmed | Extensible external integrations |
| Skills | Confirmed | Agent skill capability |
| Sandbox | Partially confirmed | Local permissions/isolation; hosted sandbox is not primary proposition |
| Cloud agent | Not primary | Client/server can be remote-controlled, but product is primarily local/open harness |

## 7. Economics

The core OpenCode software is open source under MIT. OpenCode Zen is a separate managed model-routing layer with pay-as-you-go pricing per 1M tokens. Because OpenCode is provider-agnostic, users can also bring providers/models outside Zen.

This gives the product a distinctive economic model:

- software/harness commoditized via OSS;
- model access remains interchangeable;
- hosted routing can monetize convenience without owning the agent codebase.

## 8. Ecosystem

The ecosystem consists of GitHub contributors, model providers, OpenCode Zen, MCP servers, skills, community configurations and the broader terminal/Neovim culture.

The provider-agnostic strategy matters because users can switch between proprietary frontier models, open models and local/self-hosted endpoints without replacing the harness.

## 9. Unique Insight

> **OpenCode proves that the agent harness itself can become an open software layer independent of model vendors.**

This is architecturally important for the category: the model can become a replaceable backend while the user-owned harness controls tools, permissions, context, skills and workflow.

## Evidence Ledger

| Claim | Source | Date | Confidence |
|---|---|---|---|
| OpenCode is open-source MIT coding agent with TUI and desktop | OpenCode GitHub README | 2026 | High |
| Build and Plan are distinct primary agents; general subagent exists | OpenCode GitHub README / docs | 2026 | High |
| Custom agents expose model/tool/permission controls | OpenCode Agents docs | 2026 | High |
| Provider layer supports many model providers | OpenCode LLM package docs | 2026 | High |
| OpenCode Zen uses pay-as-you-go token pricing | OpenCode Zen docs | 2026-08 | High |
| Client/server architecture is part of product philosophy | OpenCode GitHub README | 2026 | High |
| Large OSS community signal | OpenCode GitHub | 2026 | High for ecosystem, not user count |

### Primary Sources

- https://github.com/anomalyco/opencode
- https://github.com/anomalyco/opencode/blob/dev/packages/web/src/content/docs/agents.mdx
- https://github.com/anomalyco/opencode/blob/dev/packages/web/src/content/docs/cli.mdx
- https://github.com/anomalyco/opencode/blob/dev/packages/llm/README.md
- https://dev.opencode.ai/docs/zen/

### Research Status

**Deep research complete.** Architecture is unusually inspectable because the project is open source. Hosted cloud-fleet capabilities are not the core product and should not be inferred.
