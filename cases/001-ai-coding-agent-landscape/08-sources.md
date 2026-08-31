# Case 001 — 2026 AI Coding Agent Landscape

## Phase 8 — Source Ledger

> Research snapshot: **2026-08-31** · Research cutoff: **August 2026**
> Verification date: **2026-08-31**
> Research unit: Product / Product Family
> Governing document: `00-research-charter.md` (v1.1)
> Canonical model: `08-canonical-research-model.md` (Phase 8 Task 1)
> Status: Phase 8 Task 2 complete — structured evidence layer

---

## Purpose and scope

This file is the **traceability layer** for the Phase 8 assets. It registers the major claims
carried out of Phases 1–7, the sources that back them, and the phase that owns each type of
information.

It creates no research content. Every row is copied from the locked Phase 0–7 record.

### What this ledger guarantees

```text
Claim (C-nnn)
   ↓
Evidence (E-nnn)
   ↓
Source (S-nnn)
   ↓
Date
   ↓
Evidence Grade (A/B/C/D)
   ↓
Confidence (High / Medium-High / Medium / Medium-Low / Low)
   ↓
Phase (P0–P8)
```

### Discipline rules applied

1. **No manufactured traceability.** Only major, load-bearing claims are registered
   (Task 2 §6). 36 claims are recorded; the absence of a claim for a minor
   descriptive fact is deliberate.
2. **No new scores, shares, rankings, product judgments or strategic claims.**
3. **Unknown stays Unknown.** An Unknown is never rendered as Low, Partial or an estimate.
4. **No false precision.** Survey adoption, weekly active users, paid subscribers, platform
   users and enterprise customer counts are never collapsed into one market-share percentage.
5. **Dates are explicit.** `as_of_date` and `verification_date` are used; the word "current"
   is never used as a date.

---

# Section A — Claim Ledger

Columns: `Claim ID · Claim Type · Claim · Evidence ID · Evidence Summary · Source ID ·
Source · Date · Evidence Grade · Confidence · Phase · Product / Scope`

Claim types are drawn from the controlled vocabulary:
`Fact · Market Evidence · Product Evidence · Benchmark Evidence · Analysis · Judgment ·
Hypothesis · Unknown`.

| Claim ID | Claim Type | Claim | Evidence ID | Evidence Summary | Source ID | Source | Date | Evidence Grade | Confidence | Phase | Product / Scope |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C001 | Market Evidence | Claude Code has the strongest comparable independent adoption signal among measured products in the JetBrains May-Jul 2026 survey, at 39% work adoption. | E001 | JetBrains surveyed 15,000+ professional developers in May-Jul 2026; 90% use AI coding agents at work weekly and 68% daily. Work-adoption signals: Claude Code 39%, GitHub Copilot 21%, Codex 16%, Cursor 12%, OpenCode 7%, Google Antigravity 6%; JetBrains AI / Junie ~9% combined. | S001 | JetBrains - AI Coding Agents: Adoption Trends | 2026-08 | A | High | P2;P7 | Claude Code; market-wide |
| C002 | Market Evidence | The JetBrains adoption figures are multi-select survey responses that do not sum to 100%, and they are not market shares. | E002 | The published figures sum to 110%, which is only possible under multi-select response. They are survey adoption signals, not shares of a single denominator. | S001 | JetBrains - AI Coding Agents: Adoption Trends | 2026-08 | A | High | P2;P7 | Market-wide |
| C003 | Market Evidence | Adoption figures from different JetBrains survey waves are not directly comparable. | E003 | The April 2026 publication (January 2026 data) reports GitHub Copilot ~29%, Cursor ~18% and Claude Code ~18%. The May-Jul 2026 wave reports GitHub Copilot 21%, Cursor 12% and Claude Code 39%. Instrument, period and referent differ. | S002;S001 | JetBrains - two survey waves (Apr 2026; Aug 2026) | 2026-04; 2026-08 | B | High | P1;P2 | Market-wide |
| C004 | Market Evidence | The ~90% adoption figure changes referent between Phase 1 and Phase 2/7 and the two formulations must not be merged. | E004 | Phase 1 §2.5 reports ~90% of developers regularly using at least one AI TOOL for coding/development. Phase 2 §3.1 and Phase 7 §2.3 report 90% using AI CODING AGENTS at work weekly. Same number, different referent. | S201;S001 | 01-candidate-universe.md §2.5; JetBrains Aug 2026 | 2026-08 | B | High | P1;P2;P7 | Market-wide |
| C005 | Judgment | There is no defensible single global AI Coding Agent market-share table for August 2026 using the evidence reviewed here. | E005 | Survey adoption, paid seats, weekly active users, platform users, enterprise customer counts and GitHub stars measure different objects. No public source provides one denominator across commercial, OSS and China-market products. | S001;S031;S050;S056;S074;S208 | JetBrains; OpenAI; GitHub Newsroom; Devin; Qoder; 07-decision.md §4.3 | 2026-08-31 | B | High | P7 | Market-wide |
| C006 | Judgment | AI Coding Agent is best understood as an umbrella market of agentic software-engineering systems, not a single homogeneous product category: the technical substrate is converging while the product boundary is diverging. | E006 | All ten products share intent, context, reasoning, tool use, execution, verification and repair, but each product manages a different primary work object (task, repository, issue/PR, agent session, product, enterprise job). | S207;S208 | 06-cross-product-analysis.md §5.2/§16; 07-decision.md §3 | 2026-08-31 | A | High | P6;P7 | Market-wide |
| C007 | Judgment | Model -> Agent System -> Workflow is the dominant strategic direction; durable differentiation is moving above the model layer. | E007 | Harness-sensitive benchmark outcomes plus product architecture evidence show the competitive unit is Model + Harness + Runtime + Context/Memory + Tools + Verification + Workflow, not model identity alone. | S014;S023;S085;S208 | Terminal-Bench 2.1; Claude Code docs; Factory data-flow; 07-decision.md §3 | 2026-08-31 | B | Medium-High | P5;P6;P7 | Market-wide |
| C008 | Judgment | The agent harness is already a first-class strategic layer, and observed agent outcomes are scaffold/harness sensitive. | E008 | Phase 4 separates model, harness, tools, context and runtime across all ten products. Phase 5 shows the same model producing materially different results under minimal-bash, SWE-agent-style, Claude Code and Codex CLI harnesses. | S023;S029;S085;S206 | Claude Code docs; OpenAI Codex upgrades; Factory data-flow; 05-benchmarks.md §16 | 2026-08-31 | A | High | P4;P5 | Market-wide |
| C009 | Judgment | Runtime and sandbox are becoming part of the product itself, because runtime constraints define what autonomy is actually possible. | E009 | Cursor Cloud Agents treat isolated VMs, dependencies, secrets, network, browser/desktop access and artifacts as prerequisites. Factory documents Droid execution across laptop, CI, VM, Kubernetes and air-gapped environments. Qoder Cloud Agents run in persistent cloud containers. | S040;S037;S084;S077 | Cursor Cloud Agents; Cursor self-hosted; Factory deployment patterns; Qoder Cloud Agent docs | 2026 | A | High | P4;P6 | Cursor; Factory; Qoder |
| C010 | Judgment | Workflow integration is one of the strongest candidates for a durable long-term moat, but the duration and strength of that moat remain unproven. | E010 | Workflow integration combines technical integration, switching costs, context, distribution and organizational process ownership. Phase 7 records it as a strong candidate, not an established economic law. | S045;S064;S084;S208 | GitHub cloud agent docs; Replit Agent 4; Factory deployment patterns; 07-decision.md §5.7 | 2026-08-31 | B | Medium-High | P7 | Market-wide |
| C011 | Analysis | Basic MCP and tool-protocol support is moving toward commodity status; differentiation shifts to tool quality, permissioning, reliability and workflow integration. | E011 | MCP support is Confirmed across all ten Top 10 products. Protocol support alone therefore no longer discriminates between them. | S023;S040;S069;S078;S208 | Claude Code docs; Cursor docs; OpenCode repo; Qoder slash reference; 07-decision.md §5.5 | 2026-08-31 | B | High | P4;P7 | Top 10 |
| C012 | Analysis | The market is likely to commoditize individual agent primitives faster than complete agent systems; durable differentiation comes from composition. | E012 | Phase 7 classifies 8 capabilities as Commodity, 6 as Differentiating and 6 as Potential moat. Basic code generation, repository search, terminal access, basic planning, multi-file editing, MCP support and skills are all classified as commodity or commoditizing. | S208 | 07-decision.md §9 | 2026-08-31 | B | High | P7 | Market-wide |
| C013 | Benchmark Evidence | Automated SWE-bench grading can materially overstate real maintainer acceptance; automated grader pass rates averaged about 24.2 percentage points above maintainer merge decisions in the METR sample. | E013 | METR reviewed 296 AI-generated PRs from 3 SWE-bench Verified repositories against a golden baseline of 47 human merged PRs. About half of automated-pass PRs would not be merged directly. Common rejection reasons were code quality, breaking other code and core functionality. | S006 | METR - Many SWE-bench-Passing PRs Would Not Be Merged into Main | 2026-03-10 | A | High | P5 | Benchmark validity |
| C014 | Benchmark Evidence | Benchmark results do not establish developer productivity, and no clean unbiased estimate of current productivity uplift is available. | E014 | METR's 2025 RCT found experienced open-source developers about 19% SLOWER under early-2025 AI conditions. METR's 2026-02 methodology update reports severe selection effects that prevent reading later-study data as an unbiased current uplift estimate. | S007;S008 | METR - 2025 RCT; METR - 2026-02 uplift update | 2025-07-10; 2026-02-24 | A | High | P5 | Benchmark validity |
| C015 | Benchmark Evidence | The METR transcript analysis indicates a task time-savings factor of 1.5x-13x, but METR itself labels this a soft upper bound. | E015 | 5,305 Claude Code transcripts from 7 technical workers generated in January 2026. Caveats: task substitution, task selection effects, workers only use AI where helpful, and saved time is not equivalent value. | S009 | METR - Analyzing coding agent transcripts | 2026-02-17 | B | Medium-High | P5 | Claude Code |
| C016 | Judgment | No single public benchmark currently measures the full value of an AI Coding Agent product. | E016 | The Phase 5 capability coverage matrix shows Product UX, team collaboration, enterprise ROI/TCO and long-term memory quality are not measured by any of the reviewed benchmarks; economic realism and maintainer review are covered by at most one or two. | S012;S013;S014;S015;S016;S017;S018;S019;S020;S206 | SWE-bench; SWE-bench Verified; Terminal-Bench 2.1; SWE-bench Pro; ProjDevBench; SWE-Lancer; Kotlin Benchmark; Long-Horizon-Terminal-Bench; DevBench; 05-benchmarks.md §15 | 2026-08-31 | A | High | P5 | Benchmark validity |
| C017 | Benchmark Evidence | The Kotlin Benchmark first public iteration reports Claude Code + Opus 4.7 xhigh at 85.71% (90/105), Junie + Opus 4.7 max at 81.9% and Codex + GPT-5.5 xhigh at 81.9%; these are AGENT + MODEL configurations, not product results. | E017 | JetBrains published the resolution rates as agent/model setups on 105 containerized Kotlin tasks. Phase 5 explicitly states these are a first public benchmark run, not a permanent product ranking. | S018 | JetBrains - Kotlin Benchmark for AI Coding Agents | 2026-07 | B | Medium-High | P5 | Benchmark results |
| C018 | Benchmark Evidence | Terminal-Bench 2.1 shows the same benchmark family producing materially different results across agent+model configurations. | E018 | May 2026 2.1 report: GPT-5.3-Codex + Codex CLI 73.3% -> 79.1%; GPT-5.4 + Codex CLI 76.0% -> 77.3%; Opus 4.6 + Claude Code 58.0% -> 70.1%; Gemini 3.1 Pro + Terminus 2 63.0% -> 70.7%. Results must be pinned to benchmark version and submission date. | S014 | Terminal-Bench 2.1 release note and leaderboard | 2026-05-06 | B | Medium-High | P5 | Benchmark results |
| C019 | Judgment | Phase 3 Top 10 is locked and is a Market Leaders / Representative Leaders research ranking, not a user-count Top 10 and not a capability ranking. | E019 | Charter §3.2 defines the final research population as Market Significance x Technology/Product Significance. Phase 5 §22 and Phase 6 both confirm the Top 10 unchanged with no versioned correction triggered. | S200;S203;S204;S206 | 00-research-charter.md §3.2; 03-ranking-methodology.md; 03-top10-selection.md §16; 05-benchmarks.md §22 | 2026-08-31 | A | High | P3;P5;P6 | Top 10 |
| C020 | Judgment | Factory is selected for the locked Top 10 despite the lowest composite score among the ten, on representative workflow value and enterprise strategic significance. | E020 | Phase 3 §8.1 records the divergence explicitly: the Droids / autonomous enterprise SWE workflow is an independent paradigm, enterprise positioning does not fully overlap with Copilot or Devin, and exclusion would leave the Top 10 over-concentrated on consumer/IDE/CLI products. | S204;S087 | 03-top10-selection.md §8.1; Factory Series C | 2026-08-31 | C | Medium | P3 | Factory |
| C021 | Judgment | Qoder's selection is evidence-backed rather than the result of a geographic quota. | E021 | Phase 3 §8.5 grounds the selection in IDE + CLI + Cloud Agent surface coverage, memory/skills/MCP/browser/batch primitives, the Tongyi Lingma to Qoder family lineage and the AI IDE to agent platform evolution. | S204;S074;S082 | 03-top10-selection.md §8.5; Qoder changelog; Qoder CN billing docs | 2026-08-31 | B | Medium-High | P3 | Qoder |
| C022 | Product Evidence | Amazon Q Developer CLI has been rebranded to Kiro and Amazon Q Developer IDE plugin support ends on 2027-04-30, so Q Developer is not a standalone modern product family for ranking purposes. | E022 | AWS official documentation states the CLI rebrand and the IDE plugin end-of-support date, and directs users to upgrade to Kiro for subsequent features. | S089;S090 | AWS - Upgrade to Kiro; AWS - Q Developer IDE end of support | 2026 | A | High | P2;P3 | Amazon Q Developer; Kiro |
| C023 | Product Evidence | Gemini CLI has migrated to Antigravity CLI and shares the same harness and agent with Antigravity 2.0, so it must not be double-counted as a separate Google product family. | E023 | Google's 2026-05-19 developer blog describes the transition, including the transfer of the Gemini CLI user community, stars and contributors. Google Cloud I/O 26 materials state the CLI provides the same harness and agent as Antigravity 2.0. | S062;S061 | Google Developers Blog; Google Cloud - I/O 26 agent developer news | 2026-05 | A | High | P2;P3 | Google Antigravity |
| C024 | Product Evidence | Devin Desktop is the new name for Windsurf, so Windsurf is not a separate market candidate. | E024 | Cognition's official Devin Desktop pages state the renaming directly. | S052 | Devin Desktop | 2026 | A | High | P1;P4 | Devin |
| C025 | Product Evidence | Qoder CN is the renamed continuation of the former Tongyi Lingma product line, renamed on 2026-05-20, so Tongyi Lingma is not separately counted. | E025 | Qoder CN billing documentation records the rename; the Alibaba/Qoder product materials describe the 2026 naming transition. | S082 | Qoder CN - billing description | 2026-05-20 | A | High | P1;P4 | Qoder |
| C026 | Product Evidence | Claude Code executes across three documented environments: local machine, Anthropic-managed cloud VMs, and Remote Control from a browser. | E026 | Claude Code official documentation describes the three execution environments, meaning the product is no longer CLI-only at the operating-model level. | S023 | Claude Code Docs - How Claude Code works | 2026 | A | High | P4 | Claude Code |
| C027 | Product Evidence | Factory Droids can run across laptops, CI pipelines, VMs, Kubernetes and air-gapped environments, with devcontainers and VMs providing isolation. | E027 | Factory's deployment-pattern documentation enumerates these targets, and public guidance states that higher-autonomy agents should run in sandboxed environments. | S084 | Factory - Deployment patterns | 2026 | A | High | P4;P6 | Factory |
| C028 | Product Evidence | OpenCode is an open-source MIT agent harness that is explicitly provider-agnostic, with Build and Plan as distinct primary agents. | E028 | The OpenCode repository and agents documentation describe the MIT licence, TUI focus, client/server architecture, Build/Plan primary agents and support for many providers plus local models. | S069;S070;S072 | OpenCode GitHub repository; agents docs; LLM package docs | 2026 | A | High | P4 | OpenCode |
| C029 | Product Evidence | GitHub Copilot's Pro plan makes the third-party agents Claude Code and Codex available; this is a distribution fact, not a ranking input or an endorsement. | E029 | Recorded in the Phase 4 product-04 evidence ledger from the GitHub plans page. Not surfaced in Phase 6 or Phase 7. | S044 | GitHub Copilot plans | 2026 | A | High | P4 | GitHub Copilot |
| C030 | Market Evidence | Codex reported more than 5 million weekly active users as of 2026-06-02; this is a vendor claim, not an independently normalized market denominator. | E030 | OpenAI's own productivity report. Separate from the 16% independent survey signal. | S031 | OpenAI - Codex is becoming a productivity tool for everyone | 2026-06-02 | B | High | P2;P3 | Codex |
| C031 | Market Evidence | Devin's 1M+ users and 4,000+ enterprise customers, Qoder's 6M+ users and 100K+ businesses, and Replit's 50M+ platform users are all vendor claims and must not be converted into independent market facts. | E031 | Devin figures come from vendor product pages; Qoder figures from the 2026-08-26 changelog; Replit's figure is explicitly platform-level rather than agent-only. | S056;S074;S066 | Devin product claims; Qoder changelog; Replit Pricing | 2026 | C | Medium-High | P2;P3 | Devin; Qoder; Replit Agent |
| C032 | Analysis | Cursor's August 2026 corporate transition is strategic context and is not evidence of a product capability regression. | E032 | Acquisition by SpaceX completed 2026-08-14; OpenAI announced a model-supply wind-down on 2026-08-28 with a proposed 2026-11-12 cutoff; Reuters reported on 2026-08-29. Phase 3, 6 and 7 all treat this as ecosystem/model-supply risk rather than capability change. | S042;S005;S208 | Cursor - Joining SpaceX; Reuters 2026-08-29; 07-decision.md §2.3 | 2026-08-29 | A | High | P4;P6;P7 | Cursor |
| C033 | Judgment | The software-engineering work unit has clearly risen above the line/file level, but it has not universally reached whole-workflow autonomy. | E033 | Product design shows delegated agent workstreams and parallel portfolios; independent productivity evidence remains incomplete and noisy. Phase 7 separates 'already happened', 'emerging now' and 'not yet proven'. | S001;S008;S208 | JetBrains Aug 2026; METR uplift update; 07-decision.md §10 | 2026-08-31 | B | High | P7 | Market-wide |
| C034 | Analysis | The estimate that roughly 47% of produced code was fully agent-generated on average is a DERIVED midpoint calculation across survey buckets, not a measured fact. | E034 | Phase 7 §10.2 attributes the figure to a JetBrains companion analysis using midpoint calculations across buckets, with about 22% of developers in the >80% agent-generated group. | S123 | JetBrains - agent-generated code companion analysis | 2026-08 | C | Medium | P7 | Market-wide |
| C035 | Unknown | End-to-end autonomous software engineering is NOT proven, and reliable low-supervision autonomous delivery remains unproven. | E035 | METR's maintainer study shows automated pass is not maintainer acceptance; METR's methodology update blocks an unbiased productivity estimate. Phase 7 §18 lists this under 'Not Yet Proven'. | S006;S008;S208 | METR maintainer study; METR uplift update; 07-decision.md §18 | 2026-08-31 | B | High | P5;P7 | Market-wide |
| C036 | Unknown | True agent-level market share cannot be established from the public evidence reviewed in this Case. | E036 | No unified public denominator covers commercial, open-source and China-market coding agents. Phase 7 §14 records this as a standing Unknown. | S001;S208 | JetBrains Aug 2026; 07-decision.md §14 | 2026-08-31 | C | High | P2;P7 | Market-wide |

### Claim Ledger notes

- **C002** is the operational reason the dataset carries no market-share column: the published
  adoption figures sum to 110% under multi-select response.
- **C013, C014, C015** are the three benchmark-validity claims that prevent any asset from
  converting a benchmark score into a product or productivity claim.
- **C022–C025** are the product-family normalization claims. They are why `candidates.csv`
  carries `canonical_product_family` separately from `candidate_name`, and why Google's
  Antigravity + Gemini CLI and AWS's Q Developer + Kiro are never double-counted.
- **C030, C031** carry the vendor-claim label that must survive into every rendering. A vendor
  number never loses that label and is never upgraded to independent evidence.
- **C035, C036** are registered Unknowns. They are assertions about the limits of the evidence,
  not gaps to be filled during asset production.

---

# Section B — Source Registry

Columns: `Source ID · Source Type · Organization · Title · URL · Publication Date ·
Verification Date · Tier · Notes`

**Registry conventions**

- IDs are **opaque and stable**. An ID never encodes rank, quality, grade, date or region.
- `S0nn` / `S1nn` = external sources. `S2nn` = internal Case repository artifacts.
- **S116 is intentionally unassigned** (skipped during the merge of the four legacy schemes).
  ID gaps are permitted; IDs are never renumbered or reused.
- Where Phase 1–7 gives **two different URLs for the same document**, one URL is canonical and
  the other is preserved under `alt:`. No live link-check was performed, because selecting a
  canonical URL from a live check would add evidence outside the research record.
- `Verification Date` is the Phase 8 research snapshot **2026-08-31** for every
  entry: the date this ledger was assembled from the Phase 1–7 record.
- Tier follows Charter §10; `Internal - research record` is used for the Case's own Phase
  documents, which are the authority for judgments and for the locked record itself.

## B1 — External sources


| Source ID | Source Type | Organization | Title | URL | Publication Date | Verification Date | Tier | Notes |
|---|---|---|---|---|---|---|---|---|
| S001 | Independent Survey | JetBrains | AI Coding Agents: Adoption Trends | `https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/` <br>alt: https://blog.jetbrains.com/ai/2026/08/ai-coding-agents-adoption-trends/ | 2026-08 | 2026-08-31 | Tier 2 Independent | 15,000+ professional developers; survey field May-Jul 2026. Multi-select work-adoption signal, NOT global market share. Two different URLs appear in Phase 1 vs Phase 2/3/6 (hazard H-05); no live link check was performed. |
| S002 | Independent Survey | JetBrains | AI developer ecosystem analysis (April 2026; January 2026 data) | `https://blog.jetbrains.com/research/2026/04/ai-developer-ecosystem/` | 2026-04 | 2026-08-31 | Tier 2 Independent | Historical trend context only. Reports ~90% of developers regularly using at least one AI tool for coding/development; GitHub Copilot ~29%, Cursor ~18%, Claude Code ~18%. Referent differs from the Aug 2026 survey (hazard H-04). |
| S003 | Independent Research | Anthropic | How AI is changing software development | `https://www.anthropic.com/research/claude-code` | 2026-06 | 2026-08-31 | Tier 2 Independent | Anthropic's OWN Claude Code usage research (~235,000 users, ~400,000 sessions). Proprietary sample; not a market-wide census. |
| S004 | Independent Survey | Stack Overflow | 2025 Developer Survey | `https://survey.stackoverflow.co/2025/ai` | 2025 | 2026-08-31 | Tier 2 Independent | 2025 survey, NOT 2026 (hazard H-25). ~49,000 developers. |
| S005 | Independent Research | Reuters | OpenAI to end partnership with SpaceX's Cursor, escalating feud with Musk | `https://www.reuters.com/business/media-telecom/openai-end-partnership-with-spacexs-cursor-escalating-feud-with-musk-2026-08-29/` <br>alt: https://www.reuters.com/business/media-telecom/openai-end-partnership-with-spacexs-cursor-2026-08-29/ | 2026-08-29 | 2026-08-31 | Tier 2 Independent | Two different URLs for the same article in Phase 3 vs Phase 6 (hazard H-06). Used for the Aug 2026 ownership transition and model-supply context. |
| S006 | Independent Research | METR | Many SWE-bench-Passing PRs Would Not Be Merged into Main | `https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/` | 2026-03-10 | 2026-08-31 | Tier 2 Independent | 296 AI-generated PRs across 3 SWE-bench Verified repos vs 47 human merged PRs. Maintainer merge decisions ~24.2 percentage points below automated grader. |
| S007 | Independent Research | METR | Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity | `https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/` | 2025-07-10 | 2026-08-31 | Tier 2 Independent | Found experienced OSS developers ~19% SLOWER under early-2025 AI conditions. |
| S008 | Independent Research | METR | We are Changing our Developer Productivity Experiment Design | `https://metr.org/blog/2026-02-24-uplift-update/` | 2026-02-24 | 2026-08-31 | Tier 2 Independent | Methodology update: severe selection effects; later-study data cannot be read as an unbiased estimate of current AI productivity. |
| S009 | Independent Research | METR | Analyzing coding agent transcripts to upper bound productivity gains from AI agents | `https://metr.org/notes/2026-02-17-exploratory-transcript-analysis-for-estimating-time-savings-from-coding-agents/` | 2026-02-17 | 2026-08-31 | Tier 2 Independent | 5,305 Claude Code transcripts from 7 workers, Jan 2026. Time-savings factor 1.5x-13x, explicitly a SOFT UPPER BOUND (hazard H-24). |
| S010 | Technical Paper | Vella & Blincoe | The Impact of AI Coding Assistants on Software Engineering: A Longitudinal Study | `https://arxiv.org/abs/2605.23135` | 2026-05 | 2026-08-31 | Tier 2 Independent | 95 matched participants. 82% report reduced time writing code; 84% report productivity improvement; those reporting worse developer experience rose 14% to 27%. |
| S011 | Technical Paper | BNY Mellon / academic | Beyond the Commit: Developer Perspectives on Productivity with AI Coding Assistants | `https://arxiv.org/abs/2602.03593` | 2026-02 | 2026-08-31 | Tier 2 Independent | 2,989 developers surveyed, 11 deep interviews. |
| S012 | Benchmark | SWE-bench / Princeton NLP | SWE-bench official benchmark | `https://www.swebench.com/` <br>alt: https://github.com/SWE-bench/SWE-bench | 2024 | 2026-08-31 | Tier 2 Independent | Repo-level GitHub issue resolution with executable validation. |
| S013 | Benchmark | SWE-bench / OpenAI | SWE-bench Verified | `https://www.swebench.com/verified.html` <br>alt: https://openai.com/index/introducing-swe-bench-verified/ | 2024-08-13 | 2026-08-31 | Tier 2 Independent | 500 human-filtered instances. Mixed evaluation unit: leaderboard accepts full agents while minimal-bash LM comparisons isolate models. |
| S014 | Benchmark | Terminal-Bench / Harbor | Terminal-Bench 2.1 (release note, repository and leaderboard) | `https://www.tbench.ai/news/terminal-bench-2-1` <br>alt: https://github.com/harbor-framework/terminal-bench-2-1; https://www.tbench.ai/leaderboard/terminal-bench/2.1 | 2026-05-06 | 2026-08-31 | Tier 2 Independent | Agent + model + runtime. 2.1 corrected 28 tasks from 2.0. Phase 2 references 2.0; 2.0 and 2.1 results must never be merged (hazard H-13). |
| S015 | Benchmark | Scale AI research team | SWE-bench Pro | `https://arxiv.org/abs/2509.16941` <br>alt: https://github.com/scaleapi/SWE-bench_Pro-os | 2025-09 | 2026-08-31 | Tier 2 Independent | 1,865 problems across 41 active repositories; public/held-out/commercial splits. |
| S016 | Benchmark | Academic research team | ProjDevBench | `https://arxiv.org/abs/2602.01655` | 2026-02 | 2026-08-31 | Tier 2 Independent | 20 programming problems across 8 categories. Overall acceptance rate 27.38%. Avg ~138 turns/task, ~4.81M tokens/problem. |
| S017 | Benchmark | OpenAI Preparedness | SWE-Lancer | `https://openai.com/index/swe-lancer/` <br>alt: https://proceedings.mlr.press/v267/miserendino25a.html; https://github.com/openai/frontier-evals/tree/main/project/swelancer | 2025-02 | 2026-08-31 | Tier 2 Independent | 1,400+ real Upwork tasks; ~$1M historical payments. Primarily model + SWE scaffold, NOT a product benchmark. |
| S018 | Benchmark | JetBrains | Kotlin Benchmark for AI Coding Agents | `https://blog.jetbrains.com/kotlin/2026/07/introducing-the-kotlin-benchmark-evaluate-ai-coding-agents-on-real-world-kotlin-tasks/` | 2026-07 | 2026-08-31 | Tier 2 Independent | 105 Kotlin tasks. First public iteration. Results are AGENT + MODEL configurations, not product results (hazard H-26). |
| S019 | Benchmark | Research team | Long-Horizon-Terminal-Bench | `https://metr.org/research/` | 2026-07 | 2026-08-31 | Tier 2 Independent | 46 tasks, mixed-domain, dense subtask grading. |
| S020 | Benchmark | OpenCompass / academic | DevBench / DevEval | `https://github.com/open-compass/DevEval` <br>alt: https://aclanthology.org/2025.coling-main.502/ | 2024 paper; COLING 2025 | 2026-08-31 | Tier 2 Independent | Status conflict: Phase 5 3.1 marks it 'Supporting' while 3.2 lists it in the core set. Phase 8 follows 3.1 (hazard H-12). |
| S021 | Benchmark | SWE-rebench | SWE-rebench current 2026 benchmark | `https://swe-rebench.com/` | 2026 | 2026-08-31 | Tier 2 Independent | Cited only in Phase 2 10.2 (Codex Agent 58.0%, Junie Agent 61.8%). NOT part of the Phase 5 benchmark set and not re-validated there (hazard H-13). |
| S022 | Official Company Announcement | Anthropic | Claude 3.7 Sonnet and Claude Code | `https://www.anthropic.com/news/claude-3-7-sonnet` | 2025-02-24 | 2026-08-31 | Tier 1 Primary | Claude Code introduced 2025-02-24. |
| S023 | Official Documentation | Anthropic | Claude Code Docs - How Claude Code works | `https://code.claude.com/docs/en/how-claude-code-works` | 2026 | 2026-08-31 | Tier 1 Primary | Agentic loop and harness architecture. |
| S024 | Official Documentation | Anthropic | Claude Code Docs - Create custom subagents | `https://code.claude.com/docs/en/sub-agents` | 2026 | 2026-08-31 | Tier 1 Primary | Subagent isolation, memory scopes, worktrees. |
| S025 | Official Documentation | Anthropic | Claude Code Docs - Hooks reference | `https://code.claude.com/docs/en/hooks` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S026 | Official Documentation | Anthropic | Using Claude Code with your Max plan | `https://support.anthropic.com/en/articles/11145838-using-claude-code-with-your-max-plan` | 2025/2026 doc | 2026-08-31 | Tier 1 Primary | Max 5x USD 100/month, Max 20x USD 200/month. Evidence confidence Medium in Phase 4; date string is ambiguous in the source (hazard H-19). |
| S027 | Official Company Announcement | OpenAI | Introducing Codex | `https://openai.com/index/introducing-codex/` | 2025-05-16 | 2026-08-31 | Tier 1 Primary | Cloud SWE agent launch with isolated task environments and iterative testing. |
| S028 | Official Company Announcement | OpenAI | Introducing the Codex app | `https://openai.com/index/introducing-the-codex-app/` | 2026-02-02 | 2026-08-31 | Tier 1 Primary | Command center for parallel agents and long-running tasks. |
| S029 | Official Company Announcement | OpenAI | Introducing upgrades to Codex | `https://openai.com/index/introducing-upgrades-to-codex/` | 2025-2026 | 2026-08-31 | Tier 1 Primary | Cross-surface coverage: app, CLI, IDE and cloud. |
| S030 | Official Blog | OpenAI | Codex flexible pricing for teams | `https://openai.com/index/codex-flexible-pricing-for-teams/` | 2026-04-02 | 2026-08-31 | Tier 1 Primary | Token-based PAYG Codex-only seats; new Business PAYG seats stopped 2026-06-24. |
| S031 | Official Blog | OpenAI | Codex is becoming a productivity tool for everyone | `https://openai.com/index/codex-for-knowledge-work/` | 2026-06-02 | 2026-08-31 | Tier 1 Primary | Source of the >5M weekly active users VENDOR CLAIM. |
| S032 | Official Documentation | OpenAI | Codex CLI (Help Center) | `https://help.openai.com/en/articles/11096431` | 2026 update | 2026-08-31 | Tier 1 Primary | Local CLI is open source and can modify/run code locally with approval modes. |
| S122 | Official Blog | OpenAI | Unrolling the Codex agent loop | `https://openai.com/index/unrolling-the-codex-agent-loop/` | 2026-01 | 2026-08-31 | Tier 1 Primary | Cited in Phase 1 footnote codex2. |
| S033 | Official Release Note | Cursor | Changelog 0.2.0 | `https://cursor.com/changelog/0-2-0` | 2023-04-06 | 2026-08-31 | Tier 1 Primary |  |
| S034 | Official Release Note | Cursor | Changelog - Codebase Context v1 | `https://cursor.com/changelog/codebase-context-v1` | 2023-06-06 | 2026-08-31 | Tier 1 Primary |  |
| S035 | Official Blog | Cursor | Cloud Agents | `https://cursor.com/blog/cloud-agents` | 2025-10-30 | 2026-08-31 | Tier 1 Primary |  |
| S036 | Official Blog | Cursor | Agent computer use | `https://cursor.com/blog/agent-computer-use` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S037 | Official Blog | Cursor | Run cloud agents in your own infrastructure (self-hosted) | `https://cursor.com/blog/self-hosted-cloud-agents` | 2026-03-25 | 2026-08-31 | Tier 1 Primary | Control plane separated from customer-managed workers. |
| S038 | Official Blog | Cursor | What we've learned building cloud agents | `https://cursor.com/blog/cloud-agent-lessons` | 2026-06-02 | 2026-08-31 | Tier 1 Primary | Reframes cloud-agent engineering as an operating layer around agents. |
| S039 | Official Blog | Cursor | Meet the new Cursor (Cursor 3) | `https://cursor.com/blog/cursor-3` | 2026-04-02 | 2026-08-31 | Tier 1 Primary |  |
| S040 | Official Documentation | Cursor | Cloud Agents documentation | `https://cursor.com/docs/cloud-agent` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S041 | Official Product | Cursor | Cursor Pricing | `https://cursor.com/pricing` | 2026 | 2026-08-31 | Tier 1 Primary | Phase 4 cites the pricing page but records NO numeric tiers (hazard H-19). |
| S042 | Official Blog | Cursor | Joining SpaceX | `https://cursor.com/blog/joining-spacex` | 2026-08 | 2026-08-31 | Tier 1 Primary | Phase 7 2.3 dates completion to 2026-08-14; OpenAI wind-down announced 2026-08-28 with a proposed 2026-11-12 cutoff (hazard H-21). |
| S043 | Official Product | GitHub | GitHub Copilot | `https://github.com/features/copilot` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S044 | Official Product | GitHub | GitHub Copilot plans | `https://github.com/features/copilot/plans` | 2026 | 2026-08-31 | Tier 1 Primary | Free / Pro USD 10 / Pro+ USD 39 / Max USD 100. Also records that third-party agents Claude Code and Codex are available through Pro (hazard H-28). |
| S045 | Official Documentation | GitHub | About Copilot cloud agent | `https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S046 | Official Documentation | GitHub | Customize Copilot cloud agent | `https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S047 | Official Documentation | GitHub | About Copilot CLI | `https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S048 | Official Documentation | GitHub | Invoking custom agents (Copilot CLI) | `https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S049 | Official Documentation | GitHub | Customizing the GitHub Copilot app | `https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S050 | Official Company Announcement | GitHub | GitHub Newsroom | `https://github.com/newsroom` | 2026 | 2026-08-31 | Tier 1 Primary | Source of the 4.7M paid subscribers and 77K+ organizations VENDOR CLAIM. |
| S051 | Official Blog | GitHub | GitHub Blog product news | `https://github.blog/news-insights/product-news/` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S052 | Official Product | Cognition | Devin Desktop | `https://devin.ai/desktop` | 2026 | 2026-08-31 | Tier 1 Primary | States Devin Desktop is the new name for Windsurf. |
| S053 | Official Documentation | Cognition | Devin advanced capabilities | `https://docs.devin.ai/work-with-devin/advanced-capabilities` | 2026 | 2026-08-31 | Tier 1 Primary | Child/parallel sessions, playbooks, knowledge. |
| S054 | Official Documentation | Cognition | Devin MCP docs | `https://docs.devin.ai/work-with-devin/devin-mcp` | 2026 | 2026-08-31 | Tier 1 Primary | Exposes sessions, playbooks, knowledge and scheduling. |
| S055 | Official Release Note | Cognition | Devin 2026 release notes | `https://docs.devin.ai/release-notes/2026` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S056 | Official Product | Cognition | Devin official FAQ / enterprise claims | `https://devin.ai/` | 2026 | 2026-08-31 | Tier 1 Primary | 1M+ users and 4,000+ enterprise customers are VENDOR CLAIMS. |
| S057 | Official Blog | Google | Introducing Antigravity 2.0 | `https://www.antigravity.google/blog/introducing-google-antigravity-2` | 2026-05-19 | 2026-08-31 | Tier 1 Primary | Standalone desktop app, not an IDE. |
| S058 | Official Documentation | Google | Antigravity overview | `https://www.antigravity.google/docs/overview` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S059 | Official Documentation | Google | Antigravity CLI features | `https://www.antigravity.google/docs/cli/features` | 2026 | 2026-08-31 | Tier 1 Primary | Plugins bundle skills, agents, rules, MCP servers and hooks. |
| S060 | Official Documentation | Google | Antigravity CLI - agents command | `https://www.antigravity.google/docs/cli/commands/agents/` | 2026 | 2026-08-31 | Tier 1 Primary | Monitors and controls concurrent background subagents. |
| S061 | Official Blog | Google Cloud | I/O 26 news for agent developers on Google Cloud | `https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud` | 2026-05 | 2026-08-31 | Tier 1 Primary | CLI uses the same harness/agent as Antigravity 2.0. |
| S062 | Official Blog | Google | Transitioning Gemini CLI to Antigravity CLI | `https://developers.googleblog.com/` | 2026-05-19 | 2026-08-31 | Tier 1 Primary | Basis for merging Gemini CLI into the Antigravity family; must not be double-counted. |
| S063 | Official Documentation | Google | Antigravity CLI - Gemini CLI migration | `https://www.antigravity.google/docs/cli/gcli-migration/` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S064 | Official Blog | Replit | Introducing Agent 4 | `https://replit.com/blog/introducing-agent-4-built-for-creativity` | 2026-03-11 | 2026-08-31 | Tier 1 Primary | Parallel agents; Design Canvas. |
| S065 | Official Blog | Replit | What changed from Agent 3 to Agent 4 | `https://replit.com/blog/whats-changed-agent3-to-agent4` | 2026-03-19 | 2026-08-31 | Tier 1 Primary | Plan-while-building replaced strict plan-then-build. |
| S066 | Official Product | Replit | Replit Pricing | `https://replit.com/pricing` | 2026 | 2026-08-31 | Tier 1 Primary | Core USD 20/month, Pro USD 100/month. |
| S067 | Official Blog | Replit | Evaluating Replit Agent at scale | `https://replit.com/blog/` | 2026-06-23 | 2026-08-31 | Tier 1 Primary | Real user scenarios without repo/tests/framework; evaluation loop. |
| S068 | Official Product | Replit | Replit AI / Agent | `https://replit.com/ai` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S069 | Official Product | OpenCode / anomalyco | OpenCode GitHub repository | `https://github.com/anomalyco/opencode` <br>alt: https://github.com/sst/opencode | 2026 | 2026-08-31 | Tier 1 Primary | Two GitHub orgs appear in the record: anomalyco (Phase 1/4/6) and sst (Phase 3). anomalyco treated as canonical (hazard H-07). |
| S070 | Official Documentation | OpenCode | OpenCode agents documentation | `https://github.com/anomalyco/opencode/blob/dev/packages/web/src/content/docs/agents.mdx` | 2026 | 2026-08-31 | Tier 1 Primary | Build/Plan primary agents. |
| S071 | Official Documentation | OpenCode | OpenCode CLI documentation | `https://github.com/anomalyco/opencode/blob/dev/packages/web/src/content/docs/cli.mdx` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S072 | Official Documentation | OpenCode | OpenCode LLM package (providers) | `https://github.com/anomalyco/opencode/blob/dev/packages/llm/README.md` | 2026 | 2026-08-31 | Tier 1 Primary | 75+ providers, local models. |
| S073 | Official Documentation | OpenCode | OpenCode Zen docs | `https://dev.opencode.ai/docs/zen/` | 2026-08 | 2026-08-31 | Tier 1 Primary | Pay-as-you-go model routing per 1M tokens. |
| S074 | Official Release Note | Qoder | Qoder changelog | `https://qoder.com/changelog` | 2026-08-26 | 2026-08-31 | Tier 1 Primary | Source of the 6M+ users / 100K+ businesses VENDOR CLAIM and of the continuous planning/execution/verification/self-correction harness description. |
| S075 | Official Documentation | Qoder | Qoder CLI/SDK overview | `https://docs.qoder.com/cli/sdk/overview` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S076 | Official Documentation | Qoder | Qoder Memory docs | `https://docs.qoder.com/cli/sdk/memory` | 2026 | 2026-08-31 | Tier 1 Primary | Memory generation/consumption phases. |
| S077 | Official Documentation | Qoder | Qoder Cloud Agent docs | `https://docs.qoder.com/cli/sdk/cloud-agent` | 2026 | 2026-08-31 | Tier 1 Primary | Persistent cloud containers. |
| S078 | Official Documentation | Qoder | Qoder slash reference | `https://docs.qoder.com/cli/slash-reference` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S079 | Official Documentation | Qoder | Qoder builtins reference | `https://docs.qoder.com/cli/builtins-reference` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S080 | Official Release Note | Qoder | Qoder Cloud Agents release notes | `https://docs.qoder.com/release-notes/cloud-agents` | 2026-07 to 2026-08 | 2026-08-31 | Tier 1 Primary | Browser use, GitHub repo mount, batch/schedule, memory. |
| S081 | Official Product | Qoder | Qoder pricing / account | `https://docs.qoder.com/account/pricing` | 2026 | 2026-08-31 | Tier 1 Primary | Free / Pro 20 / Pro+ 60 / Ultra 200 USD. |
| S082 | Official Documentation | Qoder CN | Qoder CN billing description (rename from Tongyi Lingma) | `https://docs.qoder.cn/product-overview/billing-description` | 2026-05-20 | 2026-08-31 | Tier 1 Primary | Basis for merging Tongyi Lingma into the Qoder family. |
| S083 | Official Product | Factory | Factory Droids | `https://www.factory.ai/droids` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S084 | Official Blog | Factory | Deployment patterns | `https://www.factory.ai/blog/deployment-patterns` | 2026 | 2026-08-31 | Tier 1 Primary | Laptops, CI, VMs, Kubernetes, air-gapped. |
| S085 | Official Blog | Factory | How Droids work (data flow) | `https://www.factory.ai/blog/how-droids-work` | 2026 | 2026-08-31 | Tier 1 Primary | Just-in-time filesystem context. |
| S086 | Official Product | Factory | Factory Pricing | `https://www.factory.ai/pricing` | 2026 | 2026-08-31 | Tier 1 Primary | ~20 / 100 / 200 USD individual; ~60 USD/user Teams. Medium-High, time-sensitive. |
| S087 | Official Company Announcement | Factory | Factory Series C | `https://factory.ai/news/series-c` | 2026-04-16 | 2026-08-31 | Tier 1 Primary | USD 150M Series C at USD 1.5B valuation; hundreds of thousands of developers and enterprise customers are VENDOR CLAIMS. |
| S088 | Official Documentation | Factory | Network and deployment (enterprise) | `https://docs.factory.ai/enterprise/network-and-deployment` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S089 | Official Documentation | AWS | Upgrade to Kiro | `https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/upgrade-to-kiro.html` | 2026 | 2026-08-31 | Tier 1 Primary | Amazon Q Developer CLI rebranded to Kiro. Basis for the Q to Kiro family normalization. |
| S090 | Official Documentation | AWS | Amazon Q Developer IDE plugins end of support | `https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html` | 2026 | 2026-08-31 | Tier 1 Primary | End of support 2027-04-30. |
| S091 | Official Product | AWS | Kiro product and docs | `https://kiro.dev/` <br>alt: https://kiro.dev/docs/ | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S092 | Official Blog | AWS | Kiro - one agent (agent harness) | `https://kiro.dev/blog/one-agent/` | 2026 | 2026-08-31 | Tier 1 Primary | Shared agent/harness across surfaces. |
| S093 | Official Blog | AWS | Kiro - Web specs and GitLab | `https://kiro.dev/blog/kiro-web-specs-gitlab/` | 2026 | 2026-08-31 | Tier 1 Primary | Spec-driven development. |
| S094 | Official Documentation | AWS | Amazon Q Developer user guide | `https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S095 | Official Product | OpenHands | OpenHands GitHub repository | `https://github.com/All-Hands-AI/OpenHands` | 2026 | 2026-08-31 | Tier 1 Primary | MIT core, AI-driven development platform. |
| S096 | Official Documentation | OpenHands | OpenHands Cloud Workspace / agent server | `https://docs.openhands.dev/sdk/guides/agent-server/cloud-workspace` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S097 | Official Product | Cline | Cline GitHub repository | `https://github.com/cline/cline` | 2026 | 2026-08-31 | Tier 1 Primary | Autonomous coding agent across IDE/CLI/headless/SDK. |
| S098 | Official Product | ByteDance | TRAE official site | `https://www.trae.ai/` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S099 | Official Product | ByteDance | TRAE SOLO | `https://www.trae.ai/solo` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S100 | Official Blog | ByteDance | TRAE Work | `https://www.trae.ai/blog/trae_work_0609` | 2026-06-09 | 2026-08-31 | Tier 1 Primary | SOLO evolved into TRAE Work in June 2026. |
| S101 | Official Documentation | Tencent | Tencent CodeBuddy CLI documentation | `https://cloud.tencent.com/document/product/1831/137026` | 2026-08-26 | 2026-08-31 | Tier 1 Primary | Agents, session restore, MCP, daemon, background workers. |
| S102 | Official Product | Tencent Cloud | CodeBuddy CloudAgent | `https://cloud.tencent.com/product/codebuddy` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S103 | Official Product | JetBrains | JetBrains Junie | `https://www.jetbrains.com/junie/` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S104 | Official Product | JetBrains | JetBrains AI | `https://www.jetbrains.com/ai/` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S105 | Official Company Announcement | JetBrains | JetBrains Annual Highlights 2026 | `https://www.jetbrains.com/lp/annualreport-2026/` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S106 | Official Product | Moonshot AI | Kimi Code | `https://www.kimi.com/code` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S107 | Official Product | Moonshot AI | Kimi Code CLI repository | `https://github.com/MoonshotAI/kimi-cli` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S108 | Official Documentation | Moonshot AI | Kimi Code CLI getting started | `https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S109 | Official Product | Mistral AI | Mistral Vibe | `https://mistral.ai/products/vibe` | 2026 | 2026-08-31 | Tier 1 Primary | Code/Work modes, subagents, skills. |
| S110 | Official Product | Alibaba / Qwen | Qwen Code GitHub repository | `https://github.com/QwenLM/qwen-code` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S111 | Official Product | Block / Linux Foundation ecosystem | Goose project materials | `https://github.com/block/goose` | 2026 | 2026-08-31 | Tier 1 Primary | General-purpose agent with coding support; desktop + CLI + API. |
| S112 | Official Product | Princeton / OSS community | SWE-agent and mini-SWE-agent repositories | `https://github.com/SWE-agent/SWE-agent` | 2026 | 2026-08-31 | Tier 1 Primary | SWE-bench oriented open-source agent harnesses. |
| S113 | Official Blog | Lovable | Lovable blog | `https://lovable.dev/blog` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S114 | Official Documentation | DeepSeek | DeepSeek Reasonix API guide | `https://api-docs.deepseek.com/guides/reasonix` | 2026 | 2026-08-31 | Tier 1 Primary |  |
| S115 | Official Product | Baidu | Baidu Comate | `https://comate.baidu.com/` | 2026 | 2026-08-31 | Tier 1 Primary | Named in Phase 1 5.1/9.2 but has NO row in the Phase 1 4.x classification tables and is excluded from Phase 1's own 13 count (hazard H-15). |
| S117 | Community | Agentic Index | Coding agent comparison index | `https://agenticindex.com/` | 2026 | 2026-08-31 | Tier 3 Community/Discovery | Discovery/coverage signal only; never a market fact. |
| S118 | Community | Voltagent | Awesome Coding Agents | `https://github.com/Voltagent/awesome-coding-agents` | 2026 | 2026-08-31 | Tier 3 Community/Discovery | Candidate discovery and coverage only. |
| S119 | Community | Inclusion AI | Agentic coding landscape | `https://www.inclusion.ai/blog/agentic-coding/` | 2026-08 | 2026-08-31 | Tier 3 Community/Discovery | Discovery signal. |
| S120 | Community | Ry Walker / community tracking | Open coding agent ecosystem tracking | `https://substack.com/` | 2026 | 2026-08-31 | Tier 3 Community/Discovery | Used for project activity / shutdown signals. Lower confidence than primary sources; drives the low-confidence exclusions of Roo Code and Sweep. |
| S121 | Community | GitHub | GitHub ecosystem signals (stars/forks) | `https://github.com/` | 2026 | 2026-08-31 | Tier 3 Community/Discovery | GitHub stars/forks are ECOSYSTEM signals, not user counts. |
| S123 | Independent Survey | JetBrains | Agent-generated code companion analysis | `(URL not recorded in Phase 7 §10.2)` | 2026-08 | 2026-08-31 | Tier 2 Independent | Cited by Phase 7 §10.2 for the ~47% fully-agent-generated midpoint estimate and the ~22% of developers in the >80% bucket. Phase 7 records no separate URL. The 47% figure is a DERIVED midpoint estimate, not a measured fact (hazard H-23). |


## B2 — Internal repository artifacts

These are the Case's own Phase documents. They are registered so that every row of the Claim
Ledger resolves to an ID, and because Phase 7 §22.3 explicitly cites repository evidence as
part of the evidence system.


| Source ID | Source Type | Organization | Title | URL | Publication Date | Verification Date | Tier | Notes |
|---|---|---|---|---|---|---|---|---|
| S200 | Repository artifact | Case 001 repository | 00-research-charter.md (v1.1) | `cases/001-ai-coding-agent-landscape/00-research-charter.md` | 2026-08 | 2026-08-31 | Internal - research record | Governing document. Owns definitions, taxonomy, weights, source strategy and evidence rules. |
| S201 | Repository artifact | Case 001 repository | 01-candidate-universe.md (Phase 1) | `cases/001-ai-coding-agent-landscape/01-candidate-universe.md` | 2026-08-30 | 2026-08-31 | Internal - research record | Owns the Candidate Universe, classification and family deduplication. Phase 1 snapshot is 2026-08-30, one day earlier than the case snapshot. |
| S202 | Repository artifact | Case 001 repository | 02-market-evidence.md (Phase 2) | `cases/001-ai-coding-agent-landscape/02-market-evidence.md` | 2026-08-31 | 2026-08-31 | Internal - research record | Owns the broad market and evidence base, vendor-claim labeling and evidence grades. |
| S203 | Repository artifact | Case 001 repository | 03-ranking-methodology.md (Phase 3) | `cases/001-ai-coding-agent-landscape/03-ranking-methodology.md` | 2026-08-31 | 2026-08-31 | Internal - research record | Owns weights, scoring scale, composite formula, research-judgment rules and the sensitivity method. |
| S204 | Repository artifact | Case 001 repository | 03-top10-selection.md (Phase 3) | `cases/001-ai-coding-agent-landscape/03-top10-selection.md` | 2026-08-31 | 2026-08-31 | Internal - research record | Owns the locked Top 10, the Phase 3 score table, selection/near-miss rationales and the robustness check. |
| S205 | Repository artifact | Case 001 repository | 04-products/product-01.md … product-10.md (Phase 4) | `cases/001-ai-coding-agent-landscape/04-products/` | 2026-08-31 | 2026-08-31 | Internal - research record | Owns product-level evidence, architecture, agent loop, workflow, economics and per-product evidence ledgers. File index equals locked Top 10 position. |
| S206 | Repository artifact | Case 001 repository | 05-benchmarks.md (Phase 5) | `cases/001-ai-coding-agent-landscape/05-benchmarks.md` | 2026-08-31 | 2026-08-31 | Internal - research record | Owns benchmark selection, methodology review and the model/agent/product layering. |
| S207 | Repository artifact | Case 001 repository | 06-cross-product-analysis.md (Phase 6) | `cases/001-ai-coding-agent-landscape/06-cross-product-analysis.md` | 2026-08-31 | 2026-08-31 | Internal - research record | Owns the four cross-product matrices, paradigm taxonomies and the competition structure. |
| S208 | Repository artifact | Case 001 repository | 07-decision.md (Phase 7) | `cases/001-ai-coding-agent-landscape/07-decision.md` | 2026-08-31 | 2026-08-31 | Internal - research record | Owns strategic judgments, the strategic layer model, category and leadership maps, commoditization, scenarios, risks and unknowns. |

---

# Section C — Phase Provenance

## C1 — Phase ownership of information

The Phase that produces a fact owns that fact. Phase 8 renders; it never originates.

```text
Phase 1 → Candidate Population
Phase 2 → Market / Evidence Base
Phase 3 → Selection / Ranking
Phase 4 → Product Evidence
Phase 5 → Benchmark Evidence
Phase 6 → Cross-product Analysis
Phase 7 → Strategic Judgment
Phase 8 → Asset Production (rendering only)
```

| Phase | Owns | Asset fields it authorises |
|---|---|---|
| **P1** | Candidate Universe, classification, family deduplication, exclusions | `phase1_class`, `phase1_evidence_grade`, `phase1_key_rationale`, `canonical_product_family`, `agentic_level` |
| **P2** | Broad market and evidence base, vendor-claim labeling, evidence grades | `market_evidence_grade`, `current_confidence` (candidate-level), market signal typing |
| **P3** | Selection, ranking, composite scores, near-miss and boundary rationale | `phase3_selection_status`, `phase3_selection_position`, all `phase3_*_score`, `phase3_research_judgment`, `phase3_selection_rationale` |
| **P4** | Product-level evidence, architecture, agent loop, workflow, economics | `model_layer_summary`, `harness_summary`, `runtime_summary`, `workflow_integration_summary`, `orchestration_summary`, `human_steering_model`, `economics_model`, `ecosystem_summary`, `unique_insight`, `unknowns`, and the Phase-4-only capability columns `mcp`, `skills`, `sandbox`, `cloud_agent` |
| **P5** | Benchmark selection, methodology review, model/agent/product layering | `phase5_evidence_relevance` |
| **P6** | Cross-product matrices, paradigms, competition structure, market confidence | `market_significance`, capability columns `planning`, `context`, `tools`, `execution`, `verification`, `repair`, `long_running`, `multi_agent`, `memory`; `phase6_category_role`; product-level `confidence` |
| **P7** | Strategic judgments, category and leadership maps, commoditization, scenarios, risks, unknowns | `phase7_leadership_role` |
| **P8** | Rendering, projection, packaging. **No content creation** | `product_id`, `candidate_id`, `as_of_date`, `source_refs`, `phase_refs`, `notes` |

## C2 — Normalization rules applied in the dataset

These are the rules that resolve the compound and heterogeneous values found in Phase 1–7.
Every rule preserves the source string; none silently overwrites it.

| Rule | Domain | Rule | Worked example |
|---|---|---|---|
| **R1** | Selection status | A compound Phase 3 label maps to a single canonical value; the verbatim label is preserved in `notes`. | Jules: `"Boundary / Reserve"` → `Boundary`. `Reserve` never occurs standalone, so it is **not** a vocabulary value (hazard H-09). |
| **R2** | Evidence grade | The canonical Evidence Grade is the **Phase 1** candidate grade. Phase 2 §12.1 coverage grades are a **separate field** and never overwrite it. | Devin: Phase 1 `B`; Phase 2 coverage `B+/A-` kept in `notes`. Antigravity: Phase 1 `A`; Phase 2 `A/B` kept in `notes`. |
| **R3** | Capability (Phase 6 matrix) | `P/C` → **Partial** (conservative member). `C*` → **Confirmed** with the configuration caveat preserved in `notes`. | Antigravity `verification` `P/C` → Partial. Factory `long_running` / `multi_agent` `C*` → Confirmed + caveat. |
| **R4** | Capability (Phase 4) | `Confirmed / <dependency qualifier>` → **Partial**. Qualifiers: task-, surface-, environment-, deployment-, orchestration-, integration-dependent; partially public; partially visible. | Claude Code `sandbox` `Confirmed / surface-dependent` → Partial. Factory `mcp` `Confirmed / integration-dependent` → Partial. |
| **R5** | Capability (Phase 4) | `Confirmed / <detail qualifier>` → **Confirmed**. Qualifiers: internal detail limited; not always central; extensible. | Antigravity `sandbox` `Confirmed / internal detail limited` → Confirmed. |
| **R6** | Family / state corrections | Where a later Phase issues a versioned correction, the later Phase governs and the correction is recorded in `notes`. | Amazon Q Developer: Phase 1 Core → Phase 3 excluded from the modern ranking population as a Kiro migration lineage. |
| **R7** | Agentic level | **Not normalized.** Phase 1 §4.1 assigns compound continuum labels (e.g. `"Autonomous / Product-building Agent"`) that resist reduction to the three-value vocabulary without distortion, so the Phase 1 string is carried verbatim. | Replit Agent: `Autonomous / Product-building Agent`. |
| **R8** | Compound confidence | A compound confidence resolves to the assessed component and the verbatim string is preserved in `notes`. | Amazon Q Developer: `"High on status; low as standalone future candidate"` → `High` (status assessment) + verbatim note. |

**Normalization decision log.** Every cell resolved by R1, R3, R4, R5 or R8 requires human
sign-off before Task 3 begins. The affected cells are:

| Entity | Field | Raw | Canonical | Rule |
|---|---|---|---|---|
| PF-01 | `sandbox` | `Confirmed / surface-dependent` | Partial | R4 |
| PF-05 | `skills` | `Partially confirmed` | Partial | R4 |
| PF-05 | `sandbox` | `Confirmed / environment-dependent` | Partial | R4 |
| PF-06 | `verification` | `P/C` | Partial | R3 |
| PF-06 | `sandbox` | `Confirmed / internal detail limited` | Confirmed | R5 |
| PF-06 | `cloud_agent` | `Partially confirmed` | Partial | R4 |
| PF-07 | `mcp`, `skills` | `Partially confirmed` | Partial | R4 |
| PF-08 | `sandbox` | `Partially confirmed` | Partial | R4 |
| PF-10 | `long_running`, `multi_agent` | `C*` | Confirmed + caveat | R3 |
| PF-10 | `mcp` | `Confirmed / integration-dependent` | Partial | R4 |
| PF-10 | `sandbox` | `Confirmed / deployment-dependent` | Partial | R4 |
| PF-10 | `cloud_agent` | `Partially confirmed` | Partial | R4 |
| CAND-002 | `memory` | `Confirmed / partially public` | Partial | R4 |
| CAND-005 | `current_evidence_grade` | `B+/A-` (Phase 2) | B (Phase 1) | R2 |
| CAND-017 | `current_confidence` | `High on status; low as standalone future candidate` | High | R8 |
| CAND-018 | `phase3_selection_status` | `Boundary / Reserve` | Boundary | R1 |

## C3 — Known discrepancies

Recorded, **not corrected**. Phase 8 never edits history; a genuine factual error is raised as
a proposed versioned correction, never fixed in place.

| # | Item | Record says | Discrepancy | Handling |
|---|---|---|---|---|
| **H-02** | Jules composite score | `03-top10-selection.md` §3.1 prints **3.70**; the stated 30/30/20/10/10 weights compute **3.75** | 0.05 | Printed value preserved verbatim in `candidates.csv`. Flagged for a proposed versioned correction. All other 19 candidates were re-derived and match exactly. |
| **H-03** | Claude Code revenue disclosure date | Phase 2 §3.2: ">..$2.5B run-rate revenue and WAU doubled since **Jan 2026** in an **Aug 2025** disclosure" | Chronologically impossible | Carried with `date_quality = suspect`. The figure is not used as a dated market number in any asset. |
| **H-12** | DevBench status | Phase 5 §3.1 marks it **Supporting**; §3.2 lists it in the **core** set | Contradictory | Follow §3.1 (Supporting); §3.2 read as an enumeration of *reviewed* benchmarks. |
| **H-14** | Phase 1 excluded-object count | §13 says **5** excluded and **~49** total; the §8 table has **6** rows | 1 object | Dataset carries the 6 table rows (table is authoritative). Both counts recorded. |
| **H-05 / H-06 / H-07** | Duplicate URLs | JetBrains Aug 2026 report, the Reuters Cursor article and the OpenCode repository each have two different URLs across phases | — | One canonical URL per source; the alternate preserved under `alt:`. No live link-check performed. |
| **H-13** | Benchmark versions | Phase 2 §10.3 discusses **Terminal-Bench 2.0**; Phase 5/6 use **2.1**. Phase 2 §10.2 cites **SWE-rebench** results that Phase 5 does not include | Version drift | Benchmark entities are versioned. 2.0 and 2.1 results are never merged. SWE-rebench is carried as unvalidated in Phase 5. |

## C4 — Universe boundary notes

- **Baidu Comate** is named in Phase 1 §5.1 and §9.2 with sources, but has **no row** in the
  Phase 1 §4 classification tables and is excluded from Phase 1's own §13 count
  (44 active + 5 excluded). It is therefore **not a row in `candidates.csv`**. Adding a 45th
  active candidate would require a classification Phase 1 never made. This is the pending
  **H-15** decision from Task 1 and is flagged for human sign-off.
- **Watchlist candidates** (CAND-037 … CAND-044) have **no** `product_surfaces` and **no**
  `agentic_level`, because Phase 1 §4.3 records neither field. Those cells are empty, not
  Unknown-by-inference.
- **Phase 1 excluded objects** (CAND-045 … CAND-050) have no `phase1_evidence_grade`, because
  the Phase 1 §8 exclusion table records no grade. Grade cells are empty; the Evidence Grade
  vocabulary is A–D only and has no Unknown member.
- **`canonical_product_family`** is `Not applicable - model layer` for pure models and
  `Not applicable - surface-only` for plugin-only extensions, because neither is a product
  family under Charter §2.3.

## C5 — Time handling

| Field | Value | Meaning |
|---|---|---|
| `as_of_date` | `2026-08-31` | The research snapshot every dataset row is projected to |
| `verification_date` | `2026-08-31` | The date this ledger was assembled from the Phase 1–7 record |
| Publication date (per source) | as recorded | The date the external document itself carries |

Phase 1's own snapshot is **2026-08-30**, one day earlier. Where Phase 2 or Phase 3 issued a
versioned correction to a Phase 1 state (notably Amazon Q Developer → Kiro), the correction
governs and is recorded in `notes` under rule R6.

---

## Research Status

**Phase 8 Task 2 complete.**

Deliverables: `08-dataset/candidates.csv` (50 rows × 26 columns),
`08-dataset/products.csv` (10 rows × 44 columns), `08-sources.md` (this file).

**Validation result: PASS** — structure, row counts, universe composition, Top 10 order,
identifier integrity, vocabularies, Source-ID and Phase-ID referential integrity, dates,
Unknown handling, banned-phrasing scan, numeric fidelity (20/20 Phase 3 scores verbatim, none
recomputed) and the 90-cell Phase 6 capability cross-check all passed. One expected warning:
the Jules composite discrepancy (H-02), preserved as printed.

**No research content was created.** No new candidate, score, market share, ranking, product
judgment or strategic claim was introduced. No Phase 1–7 file was modified.
