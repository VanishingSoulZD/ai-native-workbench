# Product 10 — Factory

> Case 001 — 2026 AI Coding Agent Landscape
> Phase: 4 — Deep Product Research
> Research cutoff: August 31, 2026
> Research unit: Product / Product Family

## 1. Product Identity

| Field | Research finding | Evidence state |
|---|---|---|
| Company | Factory | Confirmed |
| Product / Product Family | Factory Droids; coding/workflow agents plus Droid Control Plane / Droid Fleet concepts | Confirmed |
| Launch / Milestones | Product evolved from autonomous coding agents toward enterprise Droid workflows and deploy-anywhere runtime infrastructure | Confirmed |
| Target users | Software engineering teams, enterprises, platform engineering and organizations automating repeatable development work | Confirmed |
| Primary markets | Global, enterprise-oriented | Confirmed |
| Product surfaces | Web/control plane, IDE integrations, terminal, Slack, browser and deployment environments including CI/VM/Kubernetes/air-gapped systems | Confirmed |
| Business model | Subscription tiers + usage; enterprise/custom deployment | Confirmed at public-plan level |
| Status Aug 2026 | Enterprise autonomous SWE / agent-orchestration platform with strong deploy-anywhere positioning | Strongly indicated |

## 2. Product Positioning

Factory's core concept is the **Droid**: an autonomous software agent that can take a natural-language engineering objective, plan and execute changes, run tools/tests and return a shippable artifact. Rather than tying autonomy to one IDE or hosted sandbox, Factory emphasizes that Droids can run wherever enterprise engineering work already executes: developer machines, CI, VMs, Kubernetes, private environments and air-gapped deployments.

That makes Factory different from a purely cloud-hosted coding assistant. It is closer to an **enterprise agent control plane plus deployable coding-agent runtime**.

Its workflow paradigm is **Enterprise autonomous software engineering / Droids**: encode repeatable engineering jobs as agents, let them execute in controlled infrastructure, and supervise outcomes at team scale.

## 3. Product Architecture

### Model layer

Factory routes tasks across multiple model providers/model families, including Claude, GPT and Gemini classes. This makes model choice a replaceable substrate under the Droid abstraction.

### Agent / Harness

A Droid is the product-level agent unit. Factory's public architecture materials describe the harness as responsible for deciding when to inspect code, patch files, execute tools and continue the loop. Droids can be given adjustable autonomy and organization-specific instructions.

**Confirmed:** agent execution is mediated through a filesystem-native/runtime-oriented harness; the agent reads code when needed, writes patches to disk and executes in a target environment.

**Unknown:** complete internal planner graph, hidden routing/evaluation system, and exact policy engine are not publicly specified.

### Context

The strongest architectural choice is **just-in-time repository context**. Factory's data-flow documentation emphasizes that Droids do not require a pre-built remote static copy of the entire codebase; they inspect the filesystem and retrieve what they need while working.

This keeps repository state close to execution and can simplify privacy/deployment constraints.

### Tools

Terminal/shell, filesystem, code search, git, browser and external services are available depending on deployment. Droids can be invoked from Slack and other interfaces, making the agent surface broader than the development editor.

### Runtime / sandbox

Factory can run Droids on laptops, CI, VMs, Kubernetes and air-gapped infrastructure. Devcontainers and VMs can provide isolation. Public guidance explicitly notes that higher-autonomy agents should run in sandboxed environments.

This is a key distinction from SaaS-only agents: **runtime portability is a first-class product requirement**.

### Memory / rules / skills / MCP

Factory supports reusable Droid instructions/workflows and organization-specific configuration. Public material clearly supports extensible agent workflows and integrations; however, a semantically rich persistent memory architecture equivalent to Claude Code auto memory or Qoder Memory Store is not as clearly documented.

**Memory status:** Partially confirmed / Unknown at implementation level.

MCP and tool integrations are available where enabled by the deployment and workflow. Skills/workflow definitions are conceptually central to reusable Droids, although Factory's terminology and packaging differ from CLI-first products that expose a standard `/skills` directory.

### Verification

The Droid loop includes execution and testing rather than returning only text. Factory positions agents around plan → write → test → ship; CI/runtime access provides a natural observation and verification mechanism.

Factory also documents adjustable autonomy, allowing organizations to place human approval gates where risk requires them.

## 4. Agent Loop

```text
Human / system goal
  ↓
Droid task definition
  ↓
Repository / environment inspection
  ↓
Planning + reasoning
  ↓
Read / search / patch filesystem
  ↓
Execute tests / commands / external tools
  ↓
Observe results
  ↓
Repair / iterate
  ↓
Commit / PR / deployed artifact
  ↓
Human or policy gate
```

Enterprise orchestration loop:

```text
Engineering workflow
  ↓
Select / trigger Droid
  ↓
Run in approved environment
  ↓
Collect artifact + logs
  ↓
Automated checks / human approval
  ↓
Ship or retry
```

The outer orchestration and governance layer is unusually important in Factory's architecture.

## 5. Workflow

| Stage | Factory role |
|---|---|
| Intent | Natural-language request, ticket or workflow trigger |
| Task | Droid work item / repeatable automation |
| Repository | Filesystem-native repo access in target environment |
| Agent | Autonomous Droid with adjustable autonomy |
| Code | Multi-file repository edits |
| Test | CI/local/VM/K8s execution and validation |
| Review | Artifacts, diffs, logs and approval gates |
| Commit / PR | Git-based delivery; pull requests and integration workflows |
| Delivery | Can continue into enterprise CI/deployment environments |

### Workflow paradigm

**Enterprise autonomous software engineering / Droids.**

Factory's distinctive move is to package the agent as an **operational unit that can be deployed into an organization's existing engineering infrastructure**.

## 6. Capability

| Capability | State | Notes |
|---|---|---|
| Coding | Confirmed | Autonomous multi-file work |
| Repository understanding | Confirmed | Agentic search + filesystem-native access |
| Planning | Confirmed | Natural-language task planning; internals Unknown |
| Tool use | Confirmed | Shell, filesystem, git, browser/external tooling |
| Terminal | Confirmed | One supported execution surface |
| Browser / external tools | Confirmed | Browser/Slack/integration paths vary by setup |
| Testing | Confirmed | Test/build/CI workflows |
| Debugging | Confirmed | Observe failures and iterate |
| Refactoring | Confirmed | General SWE task support |
| Context management | Confirmed | Just-in-time repo/environment context |
| Long-running tasks | Confirmed / deployment-dependent | Runtime can live in CI/VM/K8s and support extended work |
| Parallel / multi-agent | Confirmed / orchestration-dependent | Fleet / multiple Droids can run independently |
| Memory | Partially confirmed | Reusable instructions/workflows clear; semantic long-term memory architecture not fully public |
| MCP | Confirmed / integration-dependent | External tool connectivity available in supported workflows |
| Skills | Partially confirmed | Reusable Droid/workflow definitions are central; exact skill packaging differs by surface |
| Sandbox | Confirmed / deployment-dependent | VMs/devcontainers/K8s/air-gapped controls |
| Cloud agent | Partially confirmed | Hosted/control-plane option exists, but deploy-anywhere runtime is the stronger product proposition |

## 7. Economics

Public individual/team pricing has historically centered on subscription tiers such as Pro, Plus, Max and Teams, with higher tiers increasing usage and access to agent-compute features; enterprise pricing is custom. Publicly listed 2026 prices include approximately $20/month Pro, $100/month Plus, $200/month Max and $60/user/month Teams, with enterprise sales-led.

Factory's deeper economic distinction is deployment flexibility. The same agent concept can consume customer-managed compute in CI/VM/Kubernetes rather than forcing all execution through a vendor-hosted environment. This lets enterprises trade infrastructure ownership/control against SaaS convenience.

The economically relevant unit is therefore **agent work performed under organizational policy**, not autocomplete volume.

## 8. Ecosystem

Factory integrates with IDEs, terminal, browser, Slack and enterprise infrastructure. Its deploy-anywhere model connects the agent to existing CI/CD, Kubernetes and security environments rather than asking enterprises to rebuild their stack around a new hosted runtime.

Model-provider diversity is another ecosystem advantage: the Droid layer can survive model-provider changes because the harness is the stable organizational abstraction.

## 9. Unique Insight

> **Factory's strongest idea is that enterprise coding agents should be deployable software infrastructure, not only SaaS features.**

The Droid abstraction separates the autonomous worker from the place it runs. That makes sandboxing, governance, network policy, compute ownership and execution environment first-class design concerns.

This is particularly important for regulated or security-sensitive organizations where “just send the repository to a cloud agent” may not be acceptable.

## Evidence Ledger

| Claim | Source | Date | Confidence |
|---|---|---|---|
| Droids can plan, write, test and ship software from natural language | Factory Droids product page | 2026 | High |
| Droids can run across laptop, CI, VM, Kubernetes and air-gapped environments | Factory deployment docs | 2026 | High |
| Filesystem-native execution retrieves code as needed and patches local disk | Factory data-flow docs | 2026 | High |
| Higher-autonomy agents should use sandboxed environments | Factory deployment/security docs | 2026 | High |
| Multiple model providers can be routed beneath Droids | Factory product/model docs | 2026 | Medium-High |
| Enterprise Droid workflows and fleet/orchestration are core positioning | Factory product / docs | 2026 | High |
| Public pricing around $20/$100/$200 individual tiers and $60/user Teams | Factory Pricing | 2026 | Medium-High; pricing is time-sensitive |
| Hundreds of thousands of developers, enterprise customers and $1.5B valuation | Phase 2 vendor evidence | 2026-04 | Medium (vendor claim) |

### Primary Sources

- https://www.factory.ai/droids
- https://www.factory.ai/blog/deployment-patterns
- https://www.factory.ai/blog/how-droids-work
- https://www.factory.ai/pricing

### Research Status

**Deep research complete.** Factory's Droid/runtime/deploy-anywhere model is well evidenced. Major Unknowns are hidden planner/evaluator internals and a less explicit semantic long-term memory architecture; neither blocks product-level analysis.
