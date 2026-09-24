# Global Work AI Candidate Universe & Boundary Map

> Task: 2.1.1 — Build the broad Global candidate universe and boundary map
>
> Case: 002 — AI for Knowledge Work / Work AI Landscape
>
> Snapshot: **2026-09-24**
>
> Status: **REVIEW**
>
> Producer: Task 2.1.1
>
> Consumer: Task 2.2.1 (Global Representative Top 10) and Task 5.1.1 (Evidence QA)
>
> Governing sources: Research Charter v1.0; AI Work Plan v1.0; research-packets/task-briefs.md
>
> Important interpretation: this is a **broad research universe, not a ranking**. Candidate order within sections is categorical, not ordinal.

---

## 1. Task Outcome

This packet establishes a deliberately broad global population from which the later **Global Representative Top 10** can be selected.

The research unit is **Product / Product Family**, not an underlying model, API primitive, database, investment firm, standards body, or isolated feature.

The universe is built around the following operational definition from the Charter:

> **Work AI = AI products whose meaningful product value includes assisting or executing Knowledge Work.**

A **Work Agent** is treated as a Work AI product or product mode that can perform a multi-step Knowledge Work objective with meaningful autonomy across context gathering, reasoning, tool use, artifact creation, execution, or verification.

This packet distinguishes:

1. **Core / near-core Work AI products** — should remain in the Global candidate pool.
2. **Borderline / adjacent Work AI products** — retained where they help explain important workflow boundaries.
3. **Out-of-scope boundary examples** — recorded explicitly so later selection does not silently expand into model, developer infrastructure, pure creative generation, pure search, pure transcription, pure RPA, or pure coding markets.

No product is ranked here.

---

## 2. Reconciliation of the Prior Deep Research Output

The 2026-09-24 Deep Research run is used as a **discovery and hypothesis input**, not as an authoritative product taxonomy.

The run successfully surfaced important ecosystems such as general-purpose AI, agent frameworks, customer-support agents, legal AI, sales agents, computer-use systems, and agent infrastructure. It also contained several category errors or stale labels that would violate the current Charter if copied directly into the candidate universe.

### Normalizations applied

| Prior research pattern | Normalization in this packet | Reason |
|---|---|---|
| “OpenAI GPT-4 Agents” | **ChatGPT / ChatGPT Work / relevant agentic modes** | The model and product surface must be separated. Current OpenAI documentation says the former ChatGPT agent experience is no longer available and points to ChatGPT Work for longer multi-step tasks. |
| LangChain / LangGraph / Deep Agents | **Adjacent developer / agent infrastructure** | Important to the ecosystem, but they are primarily building/runtime infrastructure rather than end-user Knowledge Work products. |
| Pinecone / Qdrant / Weaviate / Milvus | **Out of core scope: retrieval infrastructure** | They enable Work AI but are not themselves Work AI products for the Charter's product-level population. |
| OpenAI / Anthropic / Google model names | **Underlying-model layer, not separate Work AI candidates** | Model capability is not equivalent to product/workflow capability. |
| EU AI Act / IEEE / Partnership on AI | **Ecosystem / regulatory context, not candidates** | They affect the boundary but are not Work AI products. |
| a16z / Insight Partners / YC | **Market context, not candidates** | Investors can be evidence sources but are not product population members. |
| Babylon Health / AstraZeneca AI examples | **Exclude unless a distinct Work AI product is evidenced** | Enterprise use of AI is not enough; the research unit must be an identifiable product/product family materially serving Knowledge Work. |
| Pure coding agents such as Cursor / Claude Code / Codex | **Adjacent boundary examples** | Coding is knowledge work, but the Charter explicitly asks the Global execution track to account for pure coding agents as out-of-scope areas. They remain visible for boundary analysis. |
| Pure image/video generation | **Out of scope** | Creative generation is explicitly excluded by the Charter unless the product has a materially broader Knowledge Work role. |
| Pure browser/search products | **Borderline depending on execution** | Search alone is too narrow; browser/computer-use products become relevant when they execute multi-step Knowledge Work objectives. |

This reconciliation is important because the prior report mixed **product, product mode, framework, infrastructure, model, ecosystem organization, and enterprise deployment example** at the same level.

---

## 3. Boundary Map

### 3.1 Primary boundary

The central test is:

> **Does this identifiable product / product family materially help a knowledge worker manipulate, interpret, create, organize, communicate, decide with, or execute against information, concepts, documents, or knowledge?**

A product enters the **Candidate** population when that capability is substantial enough to explain an important Work AI category, workflow, market direction, or product archetype.

### 3.2 Boundary dimensions

| Boundary | In-scope signal | Out-of-scope signal |
|---|---|---|
| Work relevance | Research, analysis, writing, documents, meetings, planning, communication, structured execution, enterprise knowledge | Primarily non-work consumer entertainment or non-knowledge operational tasks |
| Product layer | User-facing product / product family | Model-only, API-only primitive, database, runtime, SDK |
| Agenticity | Multi-step planning, tool use, execution, artifact production, verification | Single-turn generation only |
| Office / productivity | Meaningful work inside docs, sheets, presentations, email, calendar, workspace, project systems | Feature is only cosmetic / autocomplete and not materially useful for Knowledge Work |
| Search / research | Research, synthesis, source gathering, report production | Pure search / answer retrieval without a broader work workflow |
| Browser / computer use | Executes multi-step work across web / desktop applications | Browser shell or automation primitive without Knowledge Work role |
| Coding | Coding agent can be analytically useful as a boundary example | Pure coding product is not part of the core Global Work AI selection population under this track |
| Creative | Business/knowledge-work content creation may qualify | Pure image/video/music generation does not |
| Automation / RPA | AI-led work execution that materially involves Knowledge Work | Pure deterministic RPA / workflow infrastructure |
| Vertical domain | Legal, finance, sales, support, HR, enterprise analytics, etc. when knowledge work is central | Purely physical/operational automation |
| Geography | Global relevance can be established even if feature access varies by region | Product unavailable to meaningful global users and lacking ecosystem significance |

### 3.3 Boundary Map — Mermaid

~~~mermaid
flowchart TB
    W["Work AI / AI for Knowledge Work"]

    W --> CORE["Core candidate population"]
    W --> BORDER["Borderline / adjacent candidates"]
    W --> OUT["Explicit out-of-scope boundary"]

    CORE --> G["General-purpose Work AI"]
    CORE --> O["Office / productivity AI"]
    CORE --> R["Research / knowledge agents"]
    CORE --> V["Vertical knowledge-work agents"]
    CORE --> E["Enterprise work-agent platforms"]
    CORE --> CUA["Computer-use / browser work agents"]

    BORDER --> AUTO["AI workflow / automation"]
    BORDER --> SEARCH["Research/search products with limited execution"]
    BORDER --> MEET["Meeting / communication assistants"]
    BORDER --> CREATIVE["Creative products with meaningful business workflow"]
    BORDER --> CODE["Pure coding agents"]

    OUT --> MODEL["Model-only"]
    OUT --> INFRA["Developer / model infrastructure"]
    OUT --> VECTOR["Vector DB / retrieval infrastructure"]
    OUT --> RPA["Pure RPA / deterministic workflow infrastructure"]
    OUT --> PURESEARCH["Pure search"]
    OUT --> TRANSCRIBE["Pure transcription"]
    OUT --> CREATIVEPURE["Pure image/video/music generation"]
    OUT --> REG["Regulators / standards / investors / communities"]

    G --> W
    O --> W
    R --> W
    V --> W
    E --> W
    CUA --> W
~~~

---

## 4. Candidate Universe

### 4.1 Global general-purpose Work AI

| candidate_id | company | product_family | category_bucket | work_surfaces | work_roles | relevant_capability | significance_evidence | geography_access | inclusion_status | boundary_reason | source_refs | as_of | confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G-001 | OpenAI | ChatGPT / ChatGPT Work | General-purpose Work AI; agentic work | Chat, files, web, cloud-browser/work surfaces | researcher, writer, analyst, planner, operator | Broad reasoning, research, artifact work, connected context, multi-step execution | Major general-purpose AI product with an explicit Work product surface and current multi-step work capabilities | Global subject to plan/region/feature differences | Candidate | Core umbrella product | S01 | 2026-09-24 | Confirmed |
| G-002 | Anthropic | Claude / Claude for Work / Cowork | General-purpose Work AI; computer use | Chat, files, artifacts, desktop/browser workflows | researcher, writer, analyst, reviewer, operator | Long-context knowledge work, artifacts, computer use, agent planning | Official product material describes knowledge work, agent planning, artifacts and computer use | Broad international access; feature/plan differences | Candidate | Core umbrella product | S02 | 2026-09-24 | Confirmed |
| G-003 | Google | Gemini | General-purpose Work AI; Workspace AI | Chat, Workspace, web, files | researcher, writer, analyst, planner | General reasoning, Workspace integration, research and agentic features | Gemini is integrated into Google's AI / Workspace ecosystem and has current research and computer-use capability layers | Global with product/region differences | Candidate | Core umbrella product | S03,S04 | 2026-09-24 | Confirmed |
| G-004 | Microsoft | Microsoft 365 Copilot | Office / enterprise Work AI | Word, Excel, PowerPoint, Outlook, Teams, Copilot | document worker, analyst, meeting assistant, researcher, planner | Work-graph context, document/meeting/email assistance and agent extensions | Microsoft describes Copilot as the work surface and exposes Researcher / Analyst agents | Global / enterprise licensing varies | Candidate | Core Office AI family | S05,S06 | 2026-09-24 | Confirmed |
| G-005 | Perplexity | Perplexity / Research / Computer / Comet | Research-first Work AI; computer/browser agent | Web, browser, research, files, Computer | researcher, analyst, writer, operator | Cited research plus computer/browser execution and multi-model orchestration | Current product pages position it around research, computer workflows and agentic web work | Broad global access; enterprise/browser controls vary | Candidate | Core research/agent family | S07,S08 | 2026-09-24 | Confirmed |
| G-006 | Glean | Glean Work AI / Agents | Enterprise knowledge agent | Enterprise search, workspace, connected apps | knowledge interface, researcher, analyst, coordinator | Enterprise knowledge retrieval, assistants and agents over organizational context | Product is explicitly positioned around workplace knowledge and AI agents | Enterprise/global | Candidate | Core enterprise knowledge-work product | S09 | 2026-09-24 | Likely |
| G-007 | Writer | Writer | Enterprise generative AI / agents | Enterprise content, workflows, applications | writer, analyst, coordinator, domain specialist | Enterprise agents and domain-grounded content/workflow execution | Product ecosystem is explicitly enterprise/work focused | Global enterprise | Candidate | Core enterprise Work AI | S10 | 2026-09-24 | Likely |
| G-008 | Notion | Notion Agent / Custom Agents | Workspace-native Work Agent | Pages, databases, connected apps, tasks | coordinator, writer, researcher, project worker | Agent runs multi-step work in a persistent knowledge workspace | Notion documents agents that create/edit pages, update databases and automate recurring work | Global; plan/region differences | Candidate | Core workspace-native Work Agent | S11,S12 | 2026-09-24 | Confirmed |
| G-009 | Atlassian | Rovo | Enterprise knowledge / workflow agent | Jira, Confluence, connected business apps | researcher, coordinator, knowledge interface | Search, reasoning and agentic actions across team knowledge and work systems | Product is positioned as AI for enterprise knowledge and work | Global enterprise | Candidate | Core enterprise work product | S13 | 2026-09-24 | Likely |
| G-010 | Grammarly | Grammarly AI / Enterprise | Writing and communication Work AI | Browser, documents, email, enterprise apps | writer, editor, communicator | Drafting, rewriting, communication support, enterprise style/context | Strong established business/work positioning with current AI capabilities | Broad global access | Candidate | Narrower but material Work AI role | S14 | 2026-09-24 | Likely |
| G-011 | Box | Box AI / Agents | Document / enterprise content AI | Files, documents, enterprise content | document worker, researcher, analyst | Grounded document Q&A, extraction, transformation and agentic content workflows | Enterprise content is the product's core work surface | Global enterprise | Candidate | Content-centric Work AI | S15 | 2026-09-24 | Likely |
| G-012 | Zoom | AI Companion | Meeting / communication Work AI | Meetings, chat, email/work communication | meeting assistant, coordinator, writer | Meeting synthesis and work-context assistance | Major business collaboration platform with a broad AI work assistant | Global, feature availability varies | Candidate | Office/meeting subset; keep for category coverage | S16 | 2026-09-24 | Likely |
| G-013 | Adobe | Acrobat AI Assistant | Document Work AI | PDFs, documents | document worker, researcher, summarizer | Document understanding, extraction, generation | Strong document workflow surface and enterprise adoption | Global / plan dependent | Candidate | Narrow but important document archetype | S17 | 2026-09-24 | Likely |
| G-014 | Gamma | Gamma | AI-native document/presentation creation | Documents, presentations, web pages | writer, presenter, creator, planner | Artifact-first generation and iterative document/presentation work | Clear AI-native business-content workflow | Global | Candidate | Creative/document boundary; retained because artifacts are work outputs | S18 | 2026-09-24 | Likely |
| G-015 | Canva | Canva AI | Productivity/creative work AI | Presentations, docs, whiteboards, content | presenter, communicator, creator | Work-content creation and transformation | Strong workplace content/productivity role | Global with regional differences | Borderline | Significant Work AI surface but overlaps heavily with creative generation | S19 | 2026-09-24 | Likely |
| G-016 | Miro | Miro AI | Collaborative work AI | Whiteboards, planning, workshops | planner, coordinator, facilitator, analyst | Ideation, synthesis, planning and collaborative artifacts | Work-collaboration surface directly maps to Knowledge Work | Global enterprise | Candidate | Collaborative-work subset | S20 | 2026-09-24 | Likely |

### 4.2 Research, knowledge and analytical products

| candidate_id | company | product_family | category_bucket | work_surfaces | work_roles | relevant_capability | significance_evidence | geography_access | inclusion_status | boundary_reason | source_refs | as_of | confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G-017 | OpenAI | ChatGPT Deep Research | Research agent mode within ChatGPT | Web, files, connected sources | researcher, analyst | Multi-step source discovery, synthesis and cited report production | Official OpenAI positions Deep Research as a multi-step research agent | Global/plan dependent | Candidate | Mode within G-001; do not double-count as separate product family | S21 | 2026-09-24 | Confirmed |
| G-018 | Microsoft | Researcher agent | Research agent within Copilot | Web + Microsoft work content | researcher, analyst | Complex multi-step research using work content and web with citations | Microsoft documents Researcher as a dedicated complex-research agent | Microsoft 365 plan/licensing dependent | Candidate | Mode within G-004; retained for capability analysis | S06 | 2026-09-24 | Confirmed |
| G-019 | Google | Gemini Deep Research | Research agent mode | Web, Google ecosystem | researcher, analyst | Multi-step research and synthesis | Official Google product documentation positions Deep Research as multi-step research | Global/plan dependent | Candidate | Mode within G-003; do not double-count as standalone vendor | S04 | 2026-09-24 | Likely |
| G-020 | Elicit | Elicit | Research assistant / literature research | Academic papers, structured evidence | researcher, analyst | Literature search, extraction, synthesis | Clear research workflow specialization | Global web service | Candidate | Research-specific Work AI | S22 | 2026-09-24 | Likely |
| G-021 | Consensus | Consensus | Research assistant | Academic / scientific literature | researcher, analyst | Evidence-backed paper discovery and synthesis | Strong niche research workflow significance | Global | Candidate | Research-specific Work AI | S23 | 2026-09-24 | Likely |
| G-022 | AlphaSense | AlphaSense | Enterprise research / market intelligence AI | Proprietary + web business information | analyst, researcher | Search, synthesis and market intelligence workflows | Enterprise research is the core product proposition | Global enterprise | Candidate | Specialized analytical Work AI | S24 | 2026-09-24 | Likely |
| G-023 | Hebbia | Hebbia | Research / knowledge agent | Enterprise documents and data | researcher, analyst | Multi-source analysis and agentic retrieval over enterprise information | Product is explicitly positioned around AI for complex knowledge work | Global enterprise | Candidate | Important AI-native analyst archetype | S25 | 2026-09-24 | Likely |
| G-024 | Rogo | Rogo | Financial research AI | Finance research, documents, market data | financial analyst, researcher | Research, synthesis, memo / model support | Clear financial knowledge-work specialization | Global/enterprise | Candidate | Vertical analytical Work AI | S26 | 2026-09-24 | Likely |
| G-025 | You.com | You.com | Research / multi-model work assistant | Web, research, file/work surfaces | researcher, analyst | Search, multi-model orchestration and task workflows | Current product positioning includes research and agentic work | Global | Borderline | Relevant to research/agent category, but identity overlaps strongly with broader general AI/search | S27 | 2026-09-24 | Likely |

### 4.3 Vertical Knowledge Work agents

| candidate_id | company | product_family | category_bucket | work_surfaces | work_roles | relevant_capability | significance_evidence | geography_access | inclusion_status | boundary_reason | source_refs | as_of | confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G-026 | Harvey | Harvey | Legal Work AI / agent | Legal research, drafting, documents | lawyer, researcher, reviewer | Legal research, drafting, analysis and workflow support | Leading legal AI product with explicit professional workflow orientation | International legal-market access | Candidate | Strong vertical knowledge-work archetype | S28 | 2026-09-24 | Likely |
| G-027 | Thomson Reuters | CoCounsel | Legal research / drafting AI | Legal content, documents, research | lawyer, researcher, reviewer | Legal research, document analysis and drafting | Deep legal content + enterprise workflow integration | Global legal markets with feature differences | Candidate | Strong vertical Work AI | S29 | 2026-09-24 | Likely |
| G-028 | Clio | Clio Duo | Legal practice AI | Matter management, client/service workflows | lawyer, coordinator, document worker | Practice-context assistance and workflow support | Direct integration into legal practice-management work | Legal-market access dependent | Borderline | More practice-management assistant than general Work Agent | S30 | 2026-09-24 | Likely |
| G-029 | Legora | Legora | Legal AI workspace / agent | Legal documents, research, matters | lawyer, researcher, reviewer | End-to-end legal research/drafting workflows | AI-native legal work platform with agentic workflow ambitions | Global legal market / enterprise | Candidate | Strong vertical Work AI archetype | S31 | 2026-09-24 | Likely |
| G-030 | Sierra | Sierra | Customer-service Work Agent | Customer operations, CRM/helpdesk systems | support operator, coordinator | Autonomous service resolution and enterprise action execution | Product is designed around customer-service agents operating across systems | Enterprise/global | Candidate | Customer support is knowledge work; retain for agentic execution category | S32 | 2026-09-24 | Likely |
| G-031 | Intercom | Fin | Customer-support AI agent | Support inbox, help center, customer context | support operator, knowledge interface | Answering and resolving support tasks | Established support platform with dedicated AI-agent product | Global | Candidate | Vertical work-agent archetype | S33 | 2026-09-24 | Likely |
| G-032 | Decagon | Decagon | Customer-support agent | Support channels and enterprise systems | support operator | Autonomous customer-support execution | Product is explicitly built as an enterprise customer-support agent | Enterprise/global | Candidate | Strong agentic support archetype | S34 | 2026-09-24 | Likely |
| G-033 | Maven AGI | Maven AGI | Customer-support agent | Support knowledge and workflows | support operator, knowledge worker | Autonomous support and resolution workflows | Explicit AI-agent positioning in enterprise customer support | Enterprise/global | Candidate | Strong support-agent archetype | S35 | 2026-09-24 | Likely |
| G-034 | Ada | Ada | Customer-service AI agent | Customer service channels | support operator | Automated customer support and task resolution | Long-standing enterprise conversational/agent platform | Global enterprise | Candidate | Retained for category breadth; later selection should validate agent depth | S36 | 2026-09-24 | Likely |
| G-035 | Salesforce | Agentforce | Enterprise business-agent platform | CRM, service, sales, data | sales, support, coordinator, analyst | Agents grounded in enterprise CRM/data with actions | Salesforce directly positions Agentforce as an enterprise agent layer | Global enterprise with regional product constraints | Candidate | Major enterprise agent platform | S37 | 2026-09-24 | Confirmed |
| G-036 | HubSpot | Breeze Agents | CRM / marketing / sales agents | CRM, marketing, customer operations | salesperson, marketer, coordinator | AI-assisted and agentic business workflows | Current HubSpot suite includes agentic business-workflow capabilities | Global | Candidate | Enterprise work-agent category | S38 | 2026-09-24 | Likely |
| G-037 | ServiceNow | AI Agents / Now Assist | Enterprise workflow agents | IT, HR, customer service, enterprise workflows | operator, coordinator, analyst | Agentic execution inside enterprise workflow systems | Major enterprise workflow vendor explicitly investing in AI agents | Global enterprise | Candidate | Important enterprise-agent archetype | S39 | 2026-09-24 | Likely |
| G-038 | SAP | Joule | Enterprise business AI / agents | ERP, HR, finance, business workflows | analyst, coordinator, operator | Contextual enterprise assistance and agentic workflow execution | Major enterprise software vendor integrating Joule into workflows | Global enterprise | Candidate | Enterprise Work AI / workflow-agent boundary | S40 | 2026-09-24 | Likely |
| G-039 | Workday | Illuminate | HR/finance Work AI | HR, finance, planning | HR/finance analyst, coordinator | Enterprise knowledge and workflow assistance / agents | Embedded in a major enterprise knowledge-work system | Global enterprise | Candidate | Strong vertical enterprise-work archetype | S41 | 2026-09-24 | Likely |
| G-040 | Oracle | AI Agents / Agent Studio | Enterprise business agents | ERP, CRM, HR, finance | analyst, coordinator, operator | Agentic enterprise application execution | Oracle positions AI agents within enterprise applications | Global enterprise | Candidate | Enterprise work-agent platform | S42 | 2026-09-24 | Likely |
| G-041 | 11x | AI Digital Workers | Sales agent / digital worker | CRM, prospecting, email, communication | SDR, researcher, coordinator | Prospect research, personalization, outreach, qualification | Product explicitly claims end-to-end autonomous sales workflows | Global enterprise/SMB access | Candidate | Strong autonomous-work archetype; independent performance evidence should be checked later | S43 | 2026-09-24 | Likely |
| G-042 | Artisan | Artisan | Sales automation / AI worker | Email, LinkedIn, outbound sales | SDR, researcher | Prospecting and outbound automation | Clear AI-worker positioning | Global | Candidate | Sales-agent category | S44 | 2026-09-24 | Likely |
| G-043 | Regie.ai | Regie.ai | Sales AI | CRM, outreach, sales workflows | SDR, writer, coordinator | Prospecting, sequence generation and sales automation | Material role in AI SDR landscape; current product is more copilot/workflow oriented than fully autonomous agent | Global/enterprise | Borderline | Retain to distinguish assistant vs autonomous-agent boundary | S45 | 2026-09-24 | Likely |
| G-044 | Clay | Clay | GTM research/automation | Web, CRM, enrichment, outbound | researcher, salesperson, analyst | Prospect research, enrichment and agentic GTM workflows | Significant workflow platform at the sales/knowledge-work boundary | Global | Candidate | GTM knowledge-work category; autonomy level needs later validation | S46 | 2026-09-24 | Likely |

### 4.4 AI-native work agents and agentic workspaces

| candidate_id | company | product_family | category_bucket | work_surfaces | work_roles | relevant_capability | significance_evidence | geography_access | inclusion_status | boundary_reason | source_refs | as_of | confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G-045 | Dust | Dust | Team AI agents / workspace | Connected enterprise sources, team workspace | specialist, researcher, coordinator | Custom agents grounded in team/company context | Explicit team-agent/workflow product orientation | Global enterprise | Candidate | AI-native team agent archetype | S47 | 2026-09-24 | Likely |
| G-046 | Relevance AI | Relevance AI | Agent/workforce platform | Business systems, workflows | operator, coordinator, specialist | Build and deploy AI workers/agents for business tasks | Product explicitly framed around AI workforce/agents | Global | Candidate | Agent platform closer to application layer than generic infrastructure | S48 | 2026-09-24 | Likely |
| G-047 | Lindy | Lindy | Personal/Business AI agent | Email, calendar, apps, workflows | assistant, coordinator, operator | Personal/business agents that act across connected services | Clear agentic personal/work workflow focus | Global | Candidate | Work-agent/personal-agent boundary | S49 | 2026-09-24 | Likely |
| G-048 | Zapier | Zapier Agents | AI workflow agents | Thousands of connected apps | coordinator, operator | Agents can act independently across connected apps | Official docs describe agents doing work on behalf of users and using thousands of app integrations | Global | Borderline | Important automation boundary; retain because AI agent, but pure workflow automation remains outside the core | S50 | 2026-09-24 | Confirmed |
| G-049 | n8n | n8n | AI workflow automation | APIs, business apps, workflows | coordinator, operator, developer | Agentic workflow building with broad integrations | Strong ecosystem significance in AI workflow automation | Global/self-hosted/cloud | Borderline | Primarily automation infrastructure rather than end-user Work AI product | S51 | 2026-09-24 | Likely |
| G-050 | UiPath | UiPath AI / agentic automation | Enterprise automation | Business processes, desktop/web applications | operator, coordinator | Agentic automation combined with RPA | Major enterprise automation platform adding AI agents | Global enterprise | Borderline | Retain for RPA/agent boundary; pure RPA is out of scope | S52 | 2026-09-24 | Likely |

### 4.5 Computer-use / browser work agents

| candidate_id | company | product_family | category_bucket | work_surfaces | work_roles | relevant_capability | significance_evidence | geography_access | inclusion_status | boundary_reason | source_refs | as_of | confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G-051 | Anthropic | Claude Computer Use / Claude for Chrome / Cowork | Computer-use Work Agent | Browser, desktop apps, files | operator, researcher, coordinator | Screenshot-driven computer control, agent planning and live-app execution | Anthropic documents computer use and current work-oriented agent capabilities | Global/plan dependent | Candidate | Strong computer-use work-agent archetype | S02,S53 | 2026-09-24 | Confirmed |
| G-052 | Google | Gemini Computer Use / Project Mariner | Computer/browser agent | Browser/desktop environments | operator, researcher | UI interaction and multi-step execution | Google documents computer-use capabilities for browser/mobile/desktop agents | Global/API/product availability varies | Candidate | Important agent execution layer; product maturity should be checked in later selection | S54 | 2026-09-24 | Confirmed |
| G-053 | Perplexity | Comet / Computer | Browser + desktop Work Agent | Browser, files, applications | researcher, operator | Research plus browser/desktop task execution | Current official product material explicitly describes Comet Agent and Computer workflows | Global, enterprise controls vary | Candidate | Strong browser/computer Work AI archetype | S07,S08,S55 | 2026-09-24 | Confirmed |
| G-054 | OpenAI | Computer use / cloud browser within ChatGPT Work | Computer-use Work Agent capability | Browser/web applications | operator, researcher | Model-driven UI interaction and long-running cloud-browser work | OpenAI documents computer use and current ChatGPT Work cloud-browser workflows | Plan/region dependent | Candidate | Capability belongs to ChatGPT Work family; not separately counted from G-001 | S56,S57 | 2026-09-24 | Confirmed |
| G-055 | Browser Use | Browser Use | Open-source browser-agent framework / execution layer | Browser | developer/operator | Browser automation controlled by agent models | Important ecosystem project, but primarily a framework/execution layer | Global/open source | Borderline | Retain only as boundary/technology context, not default end-user population | S58 | 2026-09-24 | Likely |

---

## 5. Explicit Adjacent / Excluded Universe

These are not part of the core Work AI candidate population, but they must remain visible so later analysis does not accidentally confuse ecosystem layers.

### 5.1 Pure coding agents — excluded from the Global Work AI population

| candidate_id | product_family | category | status | reason | source_refs |
|---|---|---|---|---|---|
| X-001 | Cursor | Coding agent | Exclude / boundary example | Strong agentic software-development product, but pure coding focus is explicitly out of scope for this Global track | S59 |
| X-002 | Claude Code | Coding agent | Exclude / boundary example | Pure software-development workflow | S60 |
| X-003 | Codex | Coding agent | Exclude / boundary example | Pure software-development workflow; important ecosystem context only | S61 |
| X-004 | GitHub Copilot | Coding assistant/agent | Exclude / boundary example | Development-only Work AI surface | S62 |
| X-005 | Devin | Coding agent | Exclude / boundary example | Software-engineering specialist rather than broad Knowledge Work | S63 |

### 5.2 Agent-development frameworks / runtimes — excluded from the product population

| candidate_id | product_family | category | status | reason | source_refs |
|---|---|---|---|---|---|
| X-006 | LangChain / LangGraph / Deep Agents | Agent framework / runtime | Exclude / ecosystem boundary | Developer infrastructure for building Work AI, not itself an end-user Knowledge Work product | S64 |
| X-007 | LlamaIndex / Workflows | Agent/data framework | Exclude / ecosystem boundary | Developer framework and data workflow layer | S65 |
| X-008 | CrewAI | Multi-agent framework | Exclude / ecosystem boundary | Application-building/orchestration framework | S66 |
| X-009 | OpenAI Agents SDK | Agent SDK | Exclude / ecosystem boundary | Developer SDK | S67 |
| X-010 | Google ADK | Agent framework | Exclude / ecosystem boundary | Developer framework/runtime | S68 |
| X-011 | Microsoft Agent Framework | Agent framework | Exclude / ecosystem boundary | Developer framework/runtime | S69 |
| X-012 | PydanticAI | Agent framework | Exclude / ecosystem boundary | Developer framework | S70 |
| X-013 | Mastra | Agent application framework | Exclude / ecosystem boundary | Developer framework | S71 |
| X-014 | smolagents | Agent framework | Exclude / ecosystem boundary | Developer framework | S72 |

### 5.3 Retrieval / model infrastructure — excluded

| candidate_id | product_family | category | status | reason | source_refs |
|---|---|---|---|---|---|
| X-015 | Pinecone | Vector database / retrieval infrastructure | Exclude | Infrastructure supporting Work AI rather than Work AI product | S73 |
| X-016 | Weaviate | Vector database / retrieval infrastructure | Exclude | Same boundary | S74 |
| X-017 | Qdrant | Vector database / retrieval infrastructure | Exclude | Same boundary | S75 |
| X-018 | Milvus / Zilliz | Vector database / retrieval infrastructure | Exclude | Same boundary | S76 |
| X-019 | OpenAI models | Foundation/model layer | Exclude | Model capability ≠ product/workflow capability | S77 |
| X-020 | Anthropic models | Foundation/model layer | Exclude | Same boundary | S78 |
| X-021 | Gemini models | Foundation/model layer | Exclude | Same boundary | S79 |
| X-022 | Llama | Foundation/model layer | Exclude | Same boundary | S80 |
| X-023 | Qwen | Foundation/model layer | Exclude | Same boundary | S81 |

### 5.4 Other explicit boundaries

| candidate_id | product_family / category | status | Boundary reason |
|---|---|---|---|
| X-024 | Midjourney | Exclude | Primarily image generation; does not materially represent general Knowledge Work execution. |
| X-025 | Runway | Exclude | Primarily video/creative generation. |
| X-026 | Adobe Firefly | Exclude / boundary | Creative-generation layer; Adobe Acrobat is retained separately because document work is materially different. |
| X-027 | Automation Anywhere | Exclude / boundary | Primarily RPA/automation infrastructure; relevant only to the automation boundary. |
| X-028 | Blue Prism | Exclude / boundary | Same RPA boundary. |
| X-029 | Otter.ai | Exclude / borderline | Pure meeting transcription is too narrow; meeting/work assistants with broader execution remain in scope where evidenced. |
| X-030 | Fireflies.ai | Exclude / borderline | Same transcription-first boundary; re-enter only if broader agentic Knowledge Work capability is materially evidenced. |
| X-031 | Standards / regulators / alliances | Exclude | Important ecosystem context, not product candidates. |
| X-032 | Venture investors / accelerators | Exclude | Market evidence sources, not products. |

---

## 6. Category Coverage Matrix

The broad universe intentionally covers the following Work AI categories.

| Category bucket | Core examples | Why retained | Expected downstream question |
|---|---|---|---|
| General-purpose Work AI | ChatGPT, Claude, Gemini, Perplexity | Establish broad work-assistant archetypes and product-vs-model differences | How much work can one general system already absorb? |
| Office / productivity AI | Microsoft 365 Copilot, Notion, Grammarly, Box, Zoom, Acrobat | Directly embedded in common work surfaces | Does context integration change the work role? |
| Research / knowledge agents | Deep Research, Researcher, Elicit, Consensus, AlphaSense, Hebbia, Rogo | Research is a central Knowledge Work family | When is research a standalone agent vs a capability inside a general assistant? |
| Enterprise knowledge / agent platforms | Glean, Writer, Rovo, Agentforce, ServiceNow, SAP, Workday, Oracle | Show organizational context, permissions and action layers | What makes enterprise agents different from consumer assistants? |
| Vertical knowledge-work agents | Harvey, CoCounsel, Legora, 11x, Sierra, Decagon, Intercom Fin | Show domain specialization | When does specialization materially change task fit? |
| AI-native workspaces / workers | Notion Agents, Dust, Relevance AI, Lindy | Show persistent context and user-defined agents | Does workspace-native execution create a new work interaction model? |
| Browser / computer-use agents | Claude CUA, Gemini Computer Use, Perplexity Computer/Comet, ChatGPT Work computer use | Show tool/API-independent execution | When does the agent become an operator rather than an assistant? |
| Automation boundary | Zapier Agents, n8n, UiPath | Shows where agentic Work AI meets workflow/RPA | Where should Knowledge Work end and generic automation begin? |
| Coding boundary | Cursor, Claude Code, Codex, GitHub Copilot, Devin | Important adjacent category but explicitly outside this Global population | Which properties generalize from coding agents to broader Work AI? |
| Developer / model infrastructure | Frameworks, SDKs, vector DBs, models | Explains ecosystem but is not the product population | Which technology layers enable Work AI without being Work AI themselves? |

---

## 7. Initial Shortlist for Downstream Review

This is **not a ranking**. It is a review pool for Task 2.2.1, chosen because each item either represents a major category, an important workflow archetype, or a material boundary question.

### General-purpose / workspace review pool
- ChatGPT / ChatGPT Work
- Claude
- Gemini
- Microsoft 365 Copilot
- Perplexity
- Glean
- Notion Agents
- Writer
- Atlassian Rovo
- Grammarly
- Box AI

### Research / analysis review pool
- ChatGPT Deep Research
- Microsoft Researcher
- Gemini Deep Research
- Elicit
- AlphaSense
- Hebbia
- Rogo

### Vertical-agent review pool
- Harvey
- CoCounsel
- Legora
- Salesforce Agentforce
- ServiceNow AI Agents
- Sierra
- Intercom Fin
- Decagon
- Maven AGI
- 11x
- Artisan
- Clay

### AI-native agent/workspace review pool
- Dust
- Relevance AI
- Lindy
- Zapier Agents

### Computer-use review pool
- Claude Computer Use / Cowork
- Gemini Computer Use / Project Mariner
- Perplexity Computer / Comet
- ChatGPT Work computer-use capability

The existence of this review pool does **not** imply that all listed products belong in the eventual Global Representative Top 10.

---

## 8. Candidate Record Quality Notes

### 8.1 Product-family normalization

Where the same vendor exposes several work modes, the preferred research unit is the **product family**, with modes recorded as capabilities.

Examples:

- ChatGPT + Deep Research + computer-use capability → one OpenAI product family, not three independent vendors/products.
- Microsoft 365 Copilot + Researcher + Analyst → one Microsoft 365 Copilot family, with specialized agents as modes.
- Gemini + Deep Research + Computer Use → one Gemini family, with capability/mode distinctions.
- Perplexity + Research + Computer + Comet → potentially one Perplexity work-agent family, with browser/desktop surfaces explicitly documented.
- Claude + Cowork + computer use → one Claude family unless downstream evidence shows a materially distinct product family.

This prevents a vendor from appearing artificially multiple times in the later representative set.

### 8.2 Work-role vocabulary

The following analytical roles will be reused downstream:

- Researcher
- Analyst
- Writer
- Editor
- Planner
- Coordinator
- Document Worker
- Meeting Assistant
- Knowledge Interface
- Operator
- Execution Agent
- Reviewer

These are **analytical role labels**, not market labels claimed by vendors.

### 8.3 Evidence classes

For later QA, candidate claims should be split into:

- **Product Fact** — directly supported by official documentation.
- **Vendor Claim** — capability stated by vendor but not independently validated.
- **Independent Evidence** — external evidence about adoption, workflow, or observed behavior.
- **Analysis** — interpretation derived from evidence.
- **Unknown** — not sufficiently supported at the snapshot date.

This packet deliberately uses conservative wording where independent evidence is incomplete.

---

## 9. Source Register — Initial Embedded References

The URLs below are intended as first-pass source anchors. Task 5.1.1 should normalize them into the canonical source register and verify publication/update dates.

| source_id | publisher | source kind | canonical entry point / evidence | tier |
|---|---|---|---|---|
| S01 | OpenAI | Official | https://openai.com/chatgpt/ | 1 |
| S02 | Anthropic | Official | https://www.anthropic.com/claude | 1 |
| S03 | Google | Official | https://gemini.google.com/ | 1 |
| S04 | Google | Official | https://support.google.com/gemini/ | 1 |
| S05 | Microsoft | Official | https://learn.microsoft.com/microsoft-365-copilot/ | 1 |
| S06 | Microsoft | Official | https://learn.microsoft.com/en-us/microsoft-365/copilot/researcher-agent | 1 |
| S07 | Perplexity | Official | https://www.perplexity.ai/hub | 1 |
| S08 | Perplexity | Official | https://www.perplexity.ai/help-center/ | 1 |
| S09 | Glean | Official | https://www.glean.com/ | 1 |
| S10 | Writer | Official | https://writer.com/ | 1 |
| S11 | Notion | Official | https://www.notion.com/product/agents | 1 |
| S12 | Notion | Official | https://www.notion.com/help/notion-agent | 1 |
| S13 | Atlassian | Official | https://www.atlassian.com/software/rovo | 1 |
| S14 | Grammarly | Official | https://www.grammarly.com/business | 1 |
| S15 | Box | Official | https://www.box.com/ai | 1 |
| S16 | Zoom | Official | https://www.zoom.com/en/products/ai-assistant/ | 1 |
| S17 | Adobe | Official | https://www.adobe.com/acrobat/generative-ai-pdf.html | 1 |
| S18 | Gamma | Official | https://gamma.app/ | 1 |
| S19 | Canva | Official | https://www.canva.com/ai/ | 1 |
| S20 | Miro | Official | https://miro.com/ai/ | 1 |
| S21 | OpenAI | Official | https://openai.com/index/introducing-deep-research/ | 1 |
| S22 | Elicit | Official | https://elicit.com/ | 1 |
| S23 | Consensus | Official | https://consensus.app/ | 1 |
| S24 | AlphaSense | Official | https://www.alpha-sense.com/ | 1 |
| S25 | Hebbia | Official | https://www.hebbia.com/ | 1 |
| S26 | Rogo | Official | https://rogo.ai/ | 1 |
| S27 | You.com | Official | https://you.com/ | 1 |
| S28 | Harvey | Official | https://www.harvey.ai/ | 1 |
| S29 | Thomson Reuters | Official | https://legal.thomsonreuters.com/en/products/cocounsel | 1 |
| S30 | Clio | Official | https://www.clio.com/ai/ | 1 |
| S31 | Legora | Official | https://legora.com/ | 1 |
| S32 | Sierra | Official | https://sierra.ai/ | 1 |
| S33 | Intercom | Official | https://www.intercom.com/fin | 1 |
| S34 | Decagon | Official | https://decagon.ai/ | 1 |
| S35 | Maven AGI | Official | https://www.mavenagi.com/ | 1 |
| S36 | Ada | Official | https://www.ada.cx/ | 1 |
| S37 | Salesforce | Official | https://www.salesforce.com/agentforce/ | 1 |
| S38 | HubSpot | Official | https://www.hubspot.com/products/artificial-intelligence | 1 |
| S39 | ServiceNow | Official | https://www.servicenow.com/now-platform/ai.html | 1 |
| S40 | SAP | Official | https://www.sap.com/products/artificial-intelligence/joule.html | 1 |
| S41 | Workday | Official | https://www.workday.com/en-us/products/ai/illuminate.html | 1 |
| S42 | Oracle | Official | https://www.oracle.com/artificial-intelligence/ | 1 |
| S43 | 11x | Official | https://www.11x.ai/ | 1 |
| S44 | Artisan | Official | https://www.artisan.co/ | 1 |
| S45 | Regie.ai | Official | https://www.regie.ai/ | 1 |
| S46 | Clay | Official | https://www.clay.com/ | 1 |
| S47 | Dust | Official | https://dust.tt/ | 1 |
| S48 | Relevance AI | Official | https://relevanceai.com/ | 1 |
| S49 | Lindy | Official | https://www.lindy.ai/ | 1 |
| S50 | Zapier | Official | https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents | 1 |
| S51 | n8n | Official | https://n8n.io/ai/ | 1 |
| S52 | UiPath | Official | https://www.uipath.com/platform/agentic-automation | 1 |
| S53 | Anthropic | Official | https://www.anthropic.com/news/developing-computer-use | 1 |
| S54 | Google | Official | https://ai.google.dev/gemini-api/docs/computer-use | 1 |
| S55 | Perplexity | Official | https://www.perplexity.ai/help-center/zh-CN/articles/12781449-mianxiang-enterprise-de-comet | 1 |
| S56 | OpenAI | Official | https://developers.openai.com/api/docs/guides/tools-computer-use | 1 |
| S57 | OpenAI | Official | https://help-lb.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt | 1 |
| S58 | Browser Use | Official / Open Source | https://github.com/browser-use/browser-use | 1 |
| S59 | Cursor | Official | https://www.cursor.com/ | 1 |
| S60 | Anthropic | Official | https://code.claude.com/docs/en/agent-sdk/overview | 1 |
| S61 | OpenAI | Official | https://openai.com/codex/ | 1 |
| S62 | GitHub | Official | https://github.com/features/copilot | 1 |
| S63 | Cognition | Official | https://www.cognition.ai/ | 1 |
| S64 | LangChain | Official | https://www.langchain.com/ | 1 |
| S65 | LlamaIndex | Official | https://www.llamaindex.ai/ | 1 |
| S66 | CrewAI | Official | https://www.crewai.com/ | 1 |
| S67 | OpenAI | Official | https://openai.github.io/openai-agents-python/ | 1 |
| S68 | Google | Official | https://google.github.io/adk-docs/ | 1 |
| S69 | Microsoft | Official | https://github.com/microsoft/agent-framework | 1 |
| S70 | Pydantic | Official | https://ai.pydantic.dev/ | 1 |
| S71 | Mastra | Official | https://mastra.ai/ | 1 |
| S72 | Hugging Face | Official | https://huggingface.co/docs/smolagents/ | 1 |
| S73 | Pinecone | Official | https://www.pinecone.io/ | 1 |
| S74 | Weaviate | Official | https://weaviate.io/ | 1 |
| S75 | Qdrant | Official | https://qdrant.tech/ | 1 |
| S76 | Zilliz / Milvus | Official | https://milvus.io/ | 1 |
| S77 | OpenAI | Official | https://platform.openai.com/docs/models | 1 |
| S78 | Anthropic | Official | https://docs.anthropic.com/ | 1 |
| S79 | Google | Official | https://ai.google.dev/gemini-api/docs | 1 |
| S80 | Meta | Official | https://www.llama.com/ | 1 |
| S81 | Alibaba Cloud | Official | https://qwenlm.github.io/ | 1 |

---

## 10. Current External Verification Anchors

The packet was normalized against current evidence available at the 2026-09-24 cutoff:

- OpenAI currently documents **ChatGPT agent as no longer available** and directs users toward ChatGPT Work for longer multi-step tasks; this is why the older “GPT-4 Agents” label from the prior Deep Research output is not retained as a product-family name.
- OpenAI's current computer-use documentation describes browser/desktop operation as an executable capability layer rather than simply a model benchmark.
- Anthropic documents computer use and describes current models/products as supporting agent planning, knowledge work and computer interaction.
- Microsoft currently documents **Researcher** as a multi-step research agent operating over web and permitted work content, distinguishing it from normal Copilot chat.
- Notion documents agents that can create/edit pages and databases and run recurring work, and its 2026 releases describe external-agent orchestration.
- Perplexity's current product surface combines research, Computer and Comet; its Enterprise documentation explicitly describes Comet Agent as performing multi-step actions such as scheduling, forms and email-related workflows.
- Zapier's current documentation defines its agents as AI-powered assistants that can independently perform work using connected apps.
- Current 2026 agent-framework landscape references identify LangGraph, CrewAI, Microsoft Agent Framework, LlamaIndex Workflows, Google ADK, OpenAI Agents SDK and Mastra as developer frameworks. They are therefore retained as ecosystem/boundary references, not as core end-user Work AI products.

Primary current evidence includes:
- OpenAI — ChatGPT agent / Work: https://help.openai.com/en/articles/11752874-chatgpt-agent
- OpenAI — computer use: https://developers.openai.com/api/docs/guides/tools-computer-use
- OpenAI — ChatGPT Work cloud browser: https://help-lb.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt
- Anthropic — computer use: https://www.anthropic.com/news/developing-computer-use
- Anthropic — Sonnet 4.6 / knowledge work & computer use: https://www.anthropic.com/news/claude-sonnet-4-6
- Microsoft — Researcher agent: https://learn.microsoft.com/en-us/microsoft-365/copilot/researcher-agent
- Notion — Agents: https://www.notion.com/product/agents
- Notion — external agents: https://www.notion.com/releases/2026-07-01
- Perplexity — product hub: https://www.perplexity.ai/hub
- Perplexity — Enterprise Comet: https://www.perplexity.ai/help-center/zh-CN/articles/12781449-mianxiang-enterprise-de-comet
- Zapier — Agents: https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents
- LangChain — 2026 agent-framework overview: https://www.langchain.com/resources/ai-agent-frameworks

---

## 11. Uncertainty / Verification Queue

The following items should **not** be treated as fully verified merely because they appear in the candidate universe.

### Product-family / capability uncertainties
- Exact product-family boundaries where one vendor exposes several agent modes under one umbrella.
- Current availability of advanced agent modes by country, plan, enterprise tenant, or invitation.
- Whether certain vertical products' autonomy is materially different from an advanced copilot/workflow.
- Whether enterprise agent platforms should be treated as direct Work AI products or as application ecosystems in the final Top 10.

### Market-significance uncertainties
- Comparable adoption metrics are not yet normalized across vendors.
- Funding, valuation, or press coverage should not be treated as a proxy for Work AI usefulness.
- Vendor-reported customer counts require independent verification before use as comparative evidence.

### Evidence gaps to carry forward
- Independent workflow evidence for newer AI-native workers such as 11x, Artisan, Dust, Relevance AI and Lindy.
- Current enterprise availability / pricing of vertical agents.
- Precise China/global availability differences for products that may appear in both the Global and China research.
- Whether products such as You.com, Canva AI and Miro AI warrant final representative-set consideration after category-coverage analysis.
- Whether browser-agent products should be represented independently or as capabilities of a broader Work AI family.

---

## 12. Mechanical Integrity Checks

- [x] Broad universe created before any representative-set decision.
- [x] Candidate identifiers are stable within this packet.
- [x] Product / product family is used as the primary unit.
- [x] Category buckets are explicit.
- [x] Work surfaces and work roles are recorded.
- [x] Relevance/significance evidence is stated separately from boundary status.
- [x] Geography/access notes are included where material.
- [x] Candidate / Borderline / Exclude status is explicit.
- [x] Boundary reason is explicit.
- [x] Source references are embedded.
- [x] Snapshot date is explicit.
- [x] No ranking is used.
- [x] Pure models, infrastructure, pure coding, pure creative generation, pure search, pure transcription, pure RPA, and ecosystem organizations are explicitly bounded.
- [ ] Full atomic source-to-claim ledger normalization — **Task 5.1.1**
- [ ] Independent evidence audit for the eventual representative set — **Task 2.2.1 / Task 5.1.1**
- [ ] Human review of representative-set selection — **Task 2.2.1**

---

## 13. Handoff to Task 2.2.1

Task 2.2.1 should treat this packet as the **selection universe**, not as a hidden ranking.

The selection session should:

1. compare the Candidate population against the Charter's representative-set criteria;
2. preserve category coverage intentionally;
3. record meaningful exclusions;
4. preserve unresolved borderline cases;
5. avoid fixed numeric scoring;
6. explain why each selected product materially contributes to understanding the 2026 Work AI landscape;
7. keep product-family normalization intact so a vendor is not double-counted through multiple modes.

The downstream question is therefore:

> **Which subset of this broad, normalized population best explains the important 2026 Work AI directions, work roles, task-fit differences, and workflow patterns?**

That question belongs to **Task 2.2.1**, not this task.

---

## 14. Status

**Task 2.1.1 deliverable status: REVIEW**

This packet is intended to satisfy the Task 2.1.1 discovery contract while preserving the explicit research boundary required by the Charter.

It should be source-audited before being treated as **FROZEN**.
