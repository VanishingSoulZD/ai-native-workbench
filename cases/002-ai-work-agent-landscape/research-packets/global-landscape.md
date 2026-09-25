# Global Landscape — Representative Top 10 Selection

> Case 002 — AI for Knowledge Work / Work AI Landscape
>
> Task: **2.2.1 — Select the Global Representative Top 10 and record inclusion/exclusion logic**
>
> Status: **REVIEW**
>
> Selection snapshot: **2026-09-24**
>
> Producer: Task 2.2.1
>
> Consumer tasks: 2.3.1, 4.1.1, 4.2.1, 5.1.1
>
> Governing sources: Research Charter v1.0; AI Work Plan v1.0; `research-packets/task-briefs.md`; `research-packets/global-candidate-universe.md`

## 1. Selection Contract

This artifact converts the broad candidate universe into a **representative Global Top 10**.

The set is a **research representation**, not a universal quality ranking. The row order below has **no ordinal meaning**.

The selection follows the Charter's product-family boundary:

```
Company
  ↓
Product / Product Family
  ↓
Work Surface(s)
  ↓
AI Capability
  ↓
Work Role
  ↓
Workflow Contribution
```

Consequences:

- Different modes of the same product family are not double-counted.
- A vendor's model, agent mode, research mode, or computer-use mode is treated as a capability when it belongs to the same product family.
- A product is retained because it materially helps explain an important 2026 Work AI category, work role, workflow model, or market direction.
- A product is not retained merely because it is famous, highly funded, highly starred, or frequently mentioned.
- No fixed numeric scoring formula is used. The Charter explicitly requires evidence-traceable representative selection and does not authorize a fixed weighting scheme.

## 2. Selection Lens

The following dimensions were used as **qualitative decision lenses**, not as a point-based rubric:

| Lens | Selection question |
|---|---|
| Market significance | Does the product materially represent an important current Work AI market position, adoption pattern, or enterprise/individual usage mode? |
| Knowledge Work relevance | Does it materially support or execute information-intensive work rather than only an adjacent technical or creative task? |
| Work-role significance | Does it represent a distinct role such as researcher, analyst, writer, knowledge interface, operator, execution agent, or coordinator? |
| Workflow significance | Does it demonstrate an important interaction model: general assistant, workspace-native agent, enterprise agent, research agent, vertical agent, or cross-app automation? |
| Category coverage | Does its inclusion help the Top 10 cover important parts of the 2026 Work AI landscape without excessive duplication? |
| Distinctive contribution | Does it add materially different insight from already selected product families? |
| Evidence quality | Is there sufficient primary evidence, supplemented by strong independent evidence where needed, to characterize the product at the snapshot date? |
| Boundary fit | Does it stay within the Charter's Work AI population without requiring an adjacent-market expansion? |

### Selection principle

A candidate is selected when its **combined significance and distinctiveness** materially improve the explanatory coverage of the landscape, while preserving the Charter's boundaries.

This is intentionally different from:

- highest revenue;
- highest user count;
- highest GitHub stars;
- highest benchmark score;
- “best AI” ranking;
- vendor self-reported capability alone.

## 3. Global Representative Top 10

> **Important:** The following entries are a representative set. They are deliberately not ranked from #1 to #10.

| representative_id | product_family | primary archetype / category coverage | principal work roles represented | Why included | Confidence |
|---|---|---|---|---|---|
| G-01 | **ChatGPT (OpenAI)** | General-purpose Work AI; broad assistant; research / computer-use capability family | Knowledge interface, researcher, writer, analyst, planner, operator | Represents the broad general-purpose Work AI archetype whose value spans many Knowledge Work tasks. The research packet also documents Deep Research and computer-use as capabilities of the same OpenAI family rather than separate products. This makes ChatGPT a useful anchor for examining how one general system can absorb multiple work roles and delegate longer tasks. Evidence anchors: S01, S21, S56, S57. | Confirmed |
| G-02 | **Claude (Anthropic)** | General-purpose Work AI; agentic assistant; computer-interaction capability family | Writer, analyst, researcher, knowledge interface, operator | Represents a second major general-purpose work-oriented product family with a distinct product/workflow position and explicit computer-use capability. Including it is useful for cross-family comparison without treating model benchmarks as product rankings. Evidence anchors: S02, S53, S60; Anthropic computer-use and 2026 model/product materials. | Confirmed |
| G-03 | **Gemini (Google)** | General-purpose Work AI; Google ecosystem / workspace-connected AI; research and computer-use capability family | Researcher, knowledge interface, writer, analyst, operator | Represents a general-purpose Work AI family whose value is strongly connected to Google's information and productivity ecosystem. Deep Research and computer-use are treated as capability modes under the Gemini family, preserving product-family normalization. Evidence anchors: S03, S04, S54. | Confirmed |
| G-04 | **Microsoft 365 Copilot (Microsoft)** | Office / productivity-suite AI; enterprise work assistant; embedded research agent family | Document worker, writer, analyst, meeting assistant, researcher, coordinator | Represents office-native Work AI embedded in everyday enterprise surfaces. Microsoft documents Researcher as a complex, multi-step research agent that can work across web and permitted work content such as files, email, meetings, and chats. This makes the family important for understanding how enterprise context changes the work role of an AI assistant. Evidence anchors: S05, S06; Microsoft Learn Researcher documentation. | Confirmed |
| G-05 | **Perplexity** | Research-first Work AI; web research; browser/computer agent capability family | Researcher, analyst, knowledge interface, operator | Represents the research-first / information-retrieval-to-action archetype. Its current product family combines research workflows with Computer and Comet-style agentic interaction. The selection preserves the distinction between a research-oriented work surface and the broader general-purpose assistants. Evidence anchors: S07, S08, S55. | Confirmed |
| G-06 | **Glean** | Enterprise knowledge AI; enterprise agent platform; governed organizational context | Knowledge interface, researcher, analyst, coordinator, execution agent | Represents the enterprise-first Work AI archetype centered on organizational knowledge, permissions, context, governed action, and reusable agents. Glean's 2026 materials explicitly describe agents that combine instructions, knowledge, tools, execution, output, memory, and enterprise governance. It therefore adds a distinct enterprise-context dimension that general assistants do not fully capture as a product category. Evidence anchors: S09; current Glean agent documentation / 2026 agent lifecycle materials. | Confirmed |
| G-07 | **Notion** | AI-native workspace; persistent context; custom / recurring agents | Document worker, knowledge interface, planner, coordinator, reviewer | Represents the workspace-native Work AI archetype in which AI works directly against documents, databases, projects, and connected tools rather than existing only as a separate chat surface. Notion documents on-demand agents as well as custom agents that can run on schedules/triggers, use permissions, connect to external tools, and leave auditable/reversible changes. Evidence anchors: S11, S12; Notion 3.6 external-agent release. | Confirmed |
| G-08 | **Harvey** | Vertical Knowledge Work AI; legal agent/workflow platform | Researcher, analyst, writer, reviewer, execution agent | Represents the vertical-specialization archetype where domain context, workflows, confidentiality requirements, and professional review boundaries materially shape AI behavior. 2026 Harvey materials describe agentic legal workflows, matter/project context, reusable workflows, and durable professional deliverables. The product therefore contributes category insight that a general assistant cannot provide through generic positioning alone. Evidence anchor: S28; Harvey 2026 workflow / agent / Harvey II materials. | Confirmed |
| G-09 | **Writer** | Enterprise content / knowledge-work AI; agent platform for work teams | Writer, editor, reviewer, knowledge interface, coordinator | Represents enterprise content and governed generative-workflow AI as a distinct Work AI archetype. It is useful for analyzing how organization-specific knowledge, content operations, and enterprise controls shape AI-assisted writing and workflow execution. Evidence anchor: S10. | Likely |
| G-10 | **Zapier Agents** | Cross-application agentic automation; Work AI ↔ automation boundary | Operator, coordinator, execution agent | Represents the boundary where Knowledge Work shifts from generating information to taking actions across connected applications. Zapier documents agents that use connected apps to perform work, making the product important for understanding action-oriented workflows and human/AI handoff boundaries. Evidence anchor: S50. | Confirmed |

## 4. Why This Set Is Representative

The Top 10 collectively cover the most important explanatory archetypes identified in the candidate universe:

| Landscape dimension | Representative coverage |
|---|---|
| General-purpose Work AI | ChatGPT, Claude, Gemini |
| Office / productivity-native AI | Microsoft 365 Copilot |
| Research-first work | Perplexity |
| Enterprise knowledge + governed agents | Glean |
| AI-native persistent workspace | Notion |
| Vertical specialized Knowledge Work | Harvey |
| Enterprise content / governed generation | Writer |
| Cross-app execution / automation boundary | Zapier Agents |
| Multi-role general assistant | ChatGPT / Claude / Gemini |
| Persistent context / permissions / scheduled work | Glean / Notion / Microsoft 365 Copilot |
| Action-oriented agent execution | Glean / Notion / Perplexity / Zapier Agents |
| Human review / professional judgment boundary | Harvey / Microsoft 365 Copilot / Glean |

### Coverage logic

The set is deliberately **not** dominated by one category.

Three general-purpose families are retained because they establish a necessary baseline for asking:

> How much Knowledge Work can a single broad AI system absorb before specialist or workflow-native AI becomes useful?

Beyond that baseline, the set adds:

- office-native enterprise context;
- research-first behavior;
- enterprise knowledge and permissions;
- persistent workspace context;
- vertical specialization;
- enterprise content operations;
- cross-application action execution.

This yields a landscape that can answer both:

1. **What kinds of Work AI products exist?**
2. **What changes when the user moves from general assistance to specialized, contextual, or agentic execution?**

## 5. Meaningful Exclusions

The following are important candidates from the broad universe that were explicitly considered but not selected for the representative set. Exclusion means **not needed in this fixed representative set**, not “irrelevant product”.

| candidate | status | Exclusion logic |
|---|---|---|
| **ChatGPT Deep Research** | Folded into G-01 | Product-family normalization: Deep Research is a major capability/mode of the OpenAI family, not an independent vendor/product family for Top 10 counting. |
| **ChatGPT computer-use capability** | Folded into G-01 | Same product-family rule; valuable capability but not a separate representative product family. |
| **Claude Computer Use / Cowork** | Folded into G-02 | Same family; capability/work mode rather than independent product-family slot. |
| **Gemini Deep Research / Computer Use** | Folded into G-03 | Same family; separate rows would double-count Google's Work AI family. |
| **Microsoft Researcher** | Folded into G-04 | Researcher is explicitly positioned as an agent within Microsoft Copilot rather than a separate market family. It is represented as a capability of Microsoft 365 Copilot. |
| **Elicit** | Not selected | Strong research-specific candidate, but the fixed set already contains a research-first archetype (Perplexity). Elicit remains a meaningful specialist reference for the later task-fit comparison, but adds less category coverage to this Top 10 than the selected enterprise/workspace/vertical families. |
| **AlphaSense** | Not selected | Strong market / financial research product, but its specialization is narrower than the landscape-level research role represented by Perplexity and the broader enterprise-knowledge role represented by Glean. |
| **Hebbia** | Borderline / not selected | Important enterprise research and knowledge-agent direction, but overlaps materially with Glean and Perplexity in the current representative set. Retained as a downstream comparison candidate if evidence shows a materially distinct work interaction model. |
| **Salesforce Agentforce** | Important adjacent candidate; not selected | Strategically important enterprise agent platform, but current product positioning is heavily centered on customer service, CRM, field service, and customer-facing interactions. This makes it an important enterprise-agent boundary/reference case rather than a necessary core member of a Knowledge Work-focused Top 10. |
| **Atlassian Rovo** | Not selected | Important enterprise search/knowledge/agent direction, but the enterprise knowledge-agent archetype is already represented by Glean and the workspace-native archetype by Notion. |
| **Dust** | Borderline / not selected | Strong AI-coworker / agent-workspace candidate, but the persistent workspace and custom-agent archetype is already represented by Notion. Preserve for later workflow comparison. |
| **Relevance AI** | Not selected | More strongly positioned as an agent-building / automation platform than as a direct Knowledge Work product family for end users; therefore closer to the orchestration/infrastructure boundary. |
| **Lindy** | Not selected | Strong assistant/automation candidate, but its cross-application execution role is substantially overlapped by Zapier Agents for the purpose of this representative landscape. |
| **Gamma** | Not selected | Important presentation-native artifact product, but presentation generation is treated as a Work AI task/artifact dimension rather than a required separate representative category in this Top 10. |
| **Canva AI** | Not selected | Broad creative/productivity utility, but the strongest product distinction is creative and design work; the final set prioritizes broader Knowledge Work and agent/workflow archetypes. |
| **Zoom AI Companion** | Not selected | Meeting-focused Work AI is important, but a meeting assistant alone does not add a sufficiently distinct landscape category after broader workspace / office products are included. |
| **Box AI** | Not selected | Enterprise document/knowledge capability is relevant, but the same contextual enterprise-document direction is already represented by Microsoft 365 Copilot, Glean, and Notion. |
| **11x / Artisan** | Borderline / not selected | Important emerging “digital worker” direction, especially for sales work, but narrower workflow specialization plus thinner independent evidence at the snapshot date makes it less useful as a core landscape representative than established broad/enterprise/vertical families. |
| **Sierra / Intercom Fin / Decagon** | Adjacent / not selected | Primarily customer-support or service-agent products. They are important for agentic enterprise automation but sit closer to the customer-service boundary than the core Knowledge Work population. |
| **Cursor / Codex / Claude Code / GitHub Copilot / Devin** | Excluded by boundary | Pure or predominantly coding-agent products are explicitly treated as an adjacent category in the Charter rather than the primary Global Work AI population. They can be used later to study which agent patterns generalize from coding to broader Knowledge Work. |
| **n8n / UiPath** | Excluded by boundary | Primarily workflow automation / RPA infrastructure. They are useful boundary references, but the Charter excludes pure RPA/workflow infrastructure from the primary product population. |
| **LangChain / LlamaIndex / CrewAI / Agent frameworks** | Excluded by boundary | Developer/model infrastructure and agent-building frameworks. They enable Work AI but are not the end-user Work AI product population selected by this case. |
| **ReAct / Toolformer / HuggingGPT / CAMEL / MetaGPT** | Excluded by boundary | Research methods or research systems rather than current end-user Work AI product families. They remain relevant historical/technical context but do not satisfy the final representative product unit. |
| **Foundation models (GPT, Claude models, Gemini models, Llama, Qwen, etc.)** | Excluded by boundary | Model layer rather than product layer. The Charter explicitly requires product-vs-model separation. |

## 6. Borderline Cases Preserved for Downstream Review

The following cases should remain visible because their classification may matter to later analysis:

### 6.1 Hebbia vs Glean

Both are relevant to enterprise research / knowledge agents. The current decision keeps Glean as the enterprise-wide representative while preserving Hebbia as a specialist comparison case. Reconsider only if later evidence demonstrates a materially different workflow contribution rather than simply a different vendor positioning statement.

### 6.2 Salesforce Agentforce

Agentforce is a major enterprise agent platform and could become relevant if the research expands the role of customer-facing enterprise work into the broader Knowledge Work model. The present selection keeps the core Top 10 centered on Knowledge Work performed by workers/teams rather than customer-service operations.

### 6.3 Dust / Lindy / Relevance AI

These products are relevant to the AI-coworker / agent-builder direction. They are not rejected as low-value products; they are held outside the fixed set because Notion, Glean, and Zapier provide stronger category coverage for the specific landscape objective.

### 6.4 11x / Artisan

These products represent an emerging “digital worker” model in narrow business functions. They are strategically interesting, but their inclusion would make the representative set more sales-centric and would rely more heavily on vendor claims / emerging evidence.

## 7. Evidence Rules Applied

Each selection decision separates:

- **Product Fact** — supported by official product documentation or official announcements.
- **Vendor Claim** — capability stated by the vendor but not independently validated.
- **Independent Evidence** — adoption, workflow, or observed behavior supported by a strong external source.
- **Analysis** — interpretation used to decide representativeness.
- **Unknown** — unresolved evidence gap.

Important evidence constraints:

1. Vendor claims about autonomy are not treated as independent proof that the system performs reliably in every workflow.
2. Model benchmarks are not used as direct evidence of end-to-end product effectiveness.
3. Popularity metrics are treated as significance signals only, not as automatic selection criteria.
4. Lack of a public metric is not interpreted as lack of product significance.
5. Change-sensitive claims must be date-anchored to the 2026-09-24 snapshot or explicitly justified as describing a pre-cutoff state.

## 8. Selection Confidence Summary

| confidence level | representative products | interpretation |
|---|---|---|
| High / Confirmed | ChatGPT, Claude, Gemini, Microsoft 365 Copilot, Perplexity, Glean, Notion, Harvey, Zapier Agents | Strong product-family fit, clear Work AI relevance, and sufficiently explicit primary-source evidence. |
| Moderate / Likely | Writer | Clear enterprise content / Work AI relevance, but less central to the landscape than the larger product families above and with less cross-source evidence captured in this task packet. |

The confidence field describes **confidence in the representativeness rationale**, not product quality.

## 9. Decision Record

### Selected set

The representative Global Top 10 is:

- ChatGPT
- Claude
- Gemini
- Microsoft 365 Copilot
- Perplexity
- Glean
- Notion
- Harvey
- Writer
- Zapier Agents

### Selection logic in one sentence

> Select the smallest fixed set that gives the reader a useful, evidence-traceable view of the major 2026 Work AI modes — general assistance, office-native work, research, enterprise knowledge, AI-native workspace, vertical specialization, enterprise content, and cross-application execution — without double-counting product families or expanding the scope into coding, pure automation, models, or developer infrastructure.

### What this set is not

It is not:

- a “best AI” list;
- a revenue ranking;
- a user-count ranking;
- a benchmark ranking;
- a GitHub-star ranking;
- a universal recommendation for every Knowledge Work task.

## 10. Downstream Handoff

Task 2.2.1 outputs this packet as the authoritative **Global Representative Set** for the next stage.

### Consumer instructions

**Task 2.3.1**
- Produce one product card for each of the 10 selected product families.
- Treat Deep Research, Researcher, Computer Use, Cowork, etc. as capabilities/modes unless later evidence proves they are materially separate product families.
- Do not add new products to the card set without a recorded representative-set revision.

**Task 4.1.1**
- Use the Top 10 to derive Work AI categories, task/capability relationships, and analytical work roles.
- Do not convert the representative set into a timeless product-to-task mapping.

**Task 4.2.1**
- Use selected products and preserved borderline cases to identify recurring orchestration patterns.
- Explicitly compare one-AI sufficiency against multi-AI handoff cases.

**Task 5.1.1**
- Verify every material factual claim against the source register.
- Normalize atomic claim → evidence → source → date → confidence links.
- Audit whether any exclusion relies only on unsupported popularity or vendor framing.

## 11. Open Verification Items

Before the artifact is marked **FROZEN**, verify:

- [ ] Writer evidence is sufficient for the same depth as the other nine representatives.
- [ ] Current adoption / significance claims are normalized across vendors rather than compared using incompatible metrics.
- [ ] Salesforce Agentforce exclusion remains defensible under the Knowledge Work boundary.
- [ ] Hebbia remains a boundary specialist rather than a materially distinct enterprise knowledge archetype.
- [ ] Any later source published after 2026-09-24 is used only when it explicitly describes a pre-cutoff state.

## 12. Source Anchors

Primary source anchors inherited from the candidate-universe packet:

- S01 — OpenAI: https://openai.com/chatgpt/
- S02 — Anthropic: https://www.anthropic.com/claude
- S03 — Google: https://gemini.google.com/
- S04 — Google Gemini Help: https://support.google.com/gemini/
- S05 — Microsoft 365 Copilot docs: https://learn.microsoft.com/microsoft-365-copilot/
- S06 — Microsoft Researcher agent: https://learn.microsoft.com/en-us/microsoft-365/copilot/researcher-agent
- S07 — Perplexity hub: https://www.perplexity.ai/hub
- S08 — Perplexity Help Center: https://www.perplexity.ai/help-center/
- S09 — Glean: https://www.glean.com/
- S10 — Writer: https://writer.com/
- S11 — Notion Agents: https://www.notion.com/product/agents
- S12 — Notion Agent Help: https://www.notion.com/help/notion-agent
- S28 — Harvey: https://www.harvey.ai/
- S50 — Zapier Agents: https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents
- S53 — Anthropic computer use: https://www.anthropic.com/news/developing-computer-use
- S54 — Gemini computer use: https://ai.google.dev/gemini-api/docs/computer-use
- S55 — Perplexity Enterprise Comet: https://www.perplexity.ai/help-center/zh-CN/articles/12781449-mianxiang-enterprise-de-comet
- S56 — OpenAI computer use: https://developers.openai.com/api/docs/guides/tools-computer-use
- S57 — OpenAI ChatGPT Work cloud browser: https://help-lb.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt

Additional verification anchors used by the selection:

- Microsoft Learn — Researcher agent: https://learn.microsoft.com/en-us/microsoft-365/copilot/researcher-agent
- Glean — Independent agents: https://www.glean.com/blog/introducing-independent-agents
- Glean — How agents work: https://docs.glean.com/agents/how-agents-work
- Notion — 3.6 external agents: https://www.notion.com/releases/2026-07-01
- Harvey — Legal workflow automation: https://www.harvey.ai/blog/legal-workflow-automation
- Harvey — AI agents for legal work: https://www.harvey.ai/blog/ai-agents-for-legal-work
- Harvey — Harvey II: https://www.harvey.ai/blog/introducing-harvey-ii
- Salesforce Agentforce (exclusion reference): https://www.salesforce.com/agentforce/
