# Global Product Work-Positioning & Capability Cards

> Case 002 — AI for Knowledge Work / Work AI Landscape
>
> Task: **2.3.1 — Produce representative product work-positioning and capability cards**
>
> Status: **REVIEW**
>
> Snapshot: **2026-09-24**
>
> Producer: Task 2.3.1
>
> Consumer tasks: 4.1.1, 4.2.1, 5.1.1
>
> Governing artifacts:
> - `00-research-charter.md`
> - `01-ai-work-plan.md`
> - `research-packets/global-landscape.md`
> - `research-packets/task-briefs.md`
>
> Research rule: product facts, vendor claims, independent evidence, analysis, and unknowns are kept separate. This packet is a characterization layer, not a ranking, recommendation, or permanent product-to-task map.

---

## 1. Card Schema & Interpretation

Each card uses the same dimensions:

1. **Identity** — product family, company, region, snapshot.
2. **Work positioning** — what the product is for in a knowledge-worker workflow.
3. **Task fit** — the role of the product across the Charter's Knowledge Work task classes.
4. **Work interaction model** — prompt/workspace/artifact interaction, context persistence, delegation and review.
5. **Agentic execution** — planning, context gathering, tool use, browser/external systems, files, artifacts, long-running work, verification, retry/repair, approvals.
6. **Artifact model** — durable outputs and work objects.
7. **Integration / context** — work systems, enterprise knowledge, web, apps, identity and permissions.
8. **Usage model** — direct Q&A, co-working, delegation, background work, artifact review, persistent project context, specialist invocation, verification.
9. **Orchestration role** — analytical role(s) supported by evidence or explicitly labeled analysis.
10. **Constraints / economics** — plan/access, enterprise restrictions, switching/setup friction and other material limits.
11. **Evidence / uncertainty** — explicit evidence status and limitations.

Task-fit terms are descriptive rather than scores:

- **Primary** — a central use case or product workflow.
- **Material** — clearly supported and useful, but not the product's main work surface.
- **Possible** — capability exists or can be assembled, but is not a central documented workflow.
- **Unclear** — insufficient evidence at the snapshot date.

---

# 2. Global Representative Product Cards

## G-01 — ChatGPT (OpenAI)

### Identity
- **Company:** OpenAI
- **Region:** Global
- **Product family:** ChatGPT, including current Work / research / connected-work capabilities
- **Snapshot:** 2026-09-24
- **Source anchors:** S01, S21, S56, S57; OpenAI ChatGPT Work / Enterprise release materials.

### Work positioning
**What is this AI for?**  
A broad general-purpose Work AI surface for turning open-ended knowledge-work objectives into research, analysis, drafting, transformation, and finished artifacts, with connected context and multi-step execution where the user's plan/entitlements support it.

**Primary roles:** researcher, knowledge interface, writer, analyst, planner, operator.  
**Secondary roles:** reviewer, document worker, coordinator.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Primary | Deep Research is an explicit multi-step research capability with source-backed reports. |
| Synthesis | Primary | Core ChatGPT workflow and research outputs. |
| Writing / editing | Primary | Core product surface and document-generation workflows. |
| Document transformation | Material | File/context-based work and artifact generation. |
| Presentation | Material | ChatGPT Work can create presentation artifacts. |
| Communication / meeting work | Material | Connected work context and document/communication workflows; exact app support varies. |
| Analysis | Primary | Research and data/knowledge-work workflows. |
| Planning | Primary | Work can plan and execute longer tasks. |
| Structured knowledge work | Primary | Broad product positioning. |
| Multi-step execution | Primary | Current ChatGPT Work is explicitly positioned for longer, involved tasks. |

### Work interaction model
- Prompt-driven entry with iterative steering.
- Supports research/work flows that can run beyond a single response.
- Connected files/apps provide external context where enabled.
- User can follow progress, answer questions, change direction, and approve important actions.
- Project/context persistence is available in the broader ChatGPT product family; exact behavior depends on product surface and plan.

### Agentic execution
- **Planning:** supported for longer Work tasks.
- **Context gathering:** web, files, and connected apps where enabled.
- **Tool use:** supported through product tools/connectors.
- **Browser/external systems:** ChatGPT Work cloud-browser capabilities are documented; current cloud browser does not support website sign-in or payments.
- **File/artifact creation:** documents, spreadsheets, presentations, reports, Sites.
- **Long-running/background work:** Scheduled Tasks can run once, repeatedly, or on triggers.
- **Verification:** user can inspect progress and intervene; source citations are available in research workflows.
- **Retry/repair:** iterative steering and continued task execution are supported, but a universal autonomous repair guarantee is not established.
- **Approval:** pauses for clarification/confirmation where required.

### Artifact model
Documents, spreadsheets, presentations, reports, research results, web/Sites and other generated work products.

### Integration / context
- Web and files.
- Connected apps where available.
- Enterprise sync/app context for eligible workspaces.
- Cloud browser as an execution surface.
- Product-family capability rather than a single fixed connector bundle.

### Usage model
Direct Q&A → iterative co-working → delegation/long-running work → artifact review → scheduled follow-up.

### Orchestration role
**Primary worker + researcher + synthesizer + operator.**  
Analysis: the breadth of the product family allows it to absorb multiple roles before another specialist is introduced.

### Constraints / economics
- Plan- and workspace-dependent access to advanced Work/research/connector capabilities.
- Current official documentation says the former standalone ChatGPT agent mode is no longer available and points users to ChatGPT Work for longer multi-step tasks.
- Exact quotas and feature availability are account/plan dependent and were not normalized here.

### Evidence / uncertainty
- **Product fact:** ChatGPT Work is positioned for longer tasks, connected apps/files, finished documents and scheduled work.
- **Vendor claim:** broad autonomy and task-completion capabilities.
- **Independent evidence:** not treated as established here; product capabilities are not equated with guaranteed end-to-end reliability.
- **Unknown:** exact feature/plan matrix at any individual account.

**Sources:**  
S01 — https://openai.com/chatgpt/  
S21 — https://openai.com/index/introducing-deep-research/  
S56 — https://developers.openai.com/api/docs/guides/tools-computer-use  
S57 — https://help-lb.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt  
Additional current source — https://help.openai.com/en/articles/10128477-chatgpt-enterprise-amp-edu

---

## G-02 — Claude (Anthropic)

### Identity
- **Company:** Anthropic
- **Region:** Global
- **Product family:** Claude, including Claude for Work, Cowork, Artifacts and computer-use capability layers
- **Snapshot:** 2026-09-24
- **Source anchors:** S02, S53, S60; Anthropic product/release materials.

### Work positioning
**What is this AI for?**  
A general-purpose knowledge-work assistant that combines long-context reasoning, artifact creation, project context, and increasingly agentic desktop/work workflows through Cowork and related product capabilities.

**Primary roles:** writer, analyst, researcher, reviewer, knowledge interface.  
**Secondary roles:** operator, coordinator.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Primary | Long-context reasoning and research workflows are established product uses. |
| Synthesis | Primary | Core Claude interaction and artifact production. |
| Writing / editing | Primary | Core product role. |
| Document transformation | Primary | Long-form document and artifact workflows. |
| Presentation | Material | Artifacts can produce reusable content; exact presentation workflow depends on tool/context. |
| Communication / meeting work | Material | Team integrations such as Slack support delegated work; meeting-specific depth varies. |
| Analysis | Primary | Anthropic explicitly discusses financial/data/knowledge-work applications. |
| Planning | Primary | Agentic planning is a documented capability of current Claude systems. |
| Structured knowledge work | Primary | Projects, knowledge, artifacts and long-context workflows. |
| Multi-step execution | Primary | Cowork, computer use, agentic planning and managed workflows. |

### Work interaction model
- Chat remains the core interface.
- Projects provide persistent knowledge/context across chats.
- Artifacts separate durable work objects from the conversation stream.
- Cowork extends Claude's agentic behavior into desktop work.
- Claude Tag allows teams to delegate work from shared Slack channels.

### Agentic execution
- **Planning:** supported in agentic workflows.
- **Context gathering:** project knowledge, files, connected tools and team surfaces.
- **Tool use:** MCP/connectors and product integrations.
- **Browser/computer:** computer-use capability; Cowork provides a desktop-oriented product surface.
- **File/artifact manipulation:** supported; artifacts are reusable standalone outputs.
- **Long-running/background:** Cowork / managed-agent style workflows support longer delegated work; exact background behavior is product-surface dependent.
- **Verification:** human review remains important; Anthropic emphasizes steering and enterprise controls.
- **Retry/repair:** iterative conversational correction is supported; universal autonomous recovery is not established.
- **Approval:** human can interrupt/guide; sensitive computer-use operations require appropriate access controls.

### Artifact model
Documents, reports, websites, SVGs, diagrams, interactive components, code and other standalone artifacts.

### Integration / context
- Projects and project knowledge.
- Slack / Claude Tag for team delegation.
- MCP ecosystem and connected tools.
- Microsoft 365 add-ins for Excel/PowerPoint/Word/Outlook workflows are documented by Anthropic for relevant use cases.
- Enterprise permissions differ by product/plan.

### Usage model
Iterative co-working → persistent project work → artifact review → team delegation → agentic desktop execution.

### Orchestration role
**Primary worker + writer/editor + researcher + reviewer; operator when computer-use/Cowork is engaged.**

### Constraints / economics
- Product features differ by Free/Pro/Max/Team/Enterprise surfaces.
- Cowork and advanced work capabilities are product/plan dependent.
- Computer use in Anthropic's API is a developer-enabled capability and should not be conflated with universal autonomous desktop access.

### Evidence / uncertainty
- **Product fact:** Projects provide shared context, artifacts create durable outputs, and Cowork brings agentic capability to desktop work.
- **Vendor claim:** broad agentic knowledge-work capability.
- **Independent evidence:** Anthropic's Economic Index provides usage research, but it is vendor-generated and is therefore not treated as independent validation.
- **Unknown:** exact feature parity across regions/plans.

**Sources:**  
S02 — https://www.anthropic.com/claude  
S53 — https://www.anthropic.com/news/developing-computer-use  
S60 — https://code.claude.com/docs/en/agent-sdk/overview  
Additional current sources — https://www.anthropic.com/news/introducing-anthropic-labs  
https://www.anthropic.com/news/claude-sonnet-4-6  
https://www.anthropic.com/news/introducing-claude-tag  
https://support.anthropic.com/en/articles/9519177-how-can-i-create-and-manage-projects

---

## G-03 — Gemini (Google)

### Identity
- **Company:** Google
- **Region:** Global
- **Product family:** Gemini, including Workspace integration, Deep Research and computer-use capability layers
- **Snapshot:** 2026-09-24
- **Source anchors:** S03, S04, S54.

### Work positioning
**What is this AI for?**  
A general-purpose Work AI family whose differentiation comes from combining broad reasoning with Google's web/search and Workspace context, allowing research and document workflows to use organizational files, email, chat and productivity surfaces.

**Primary roles:** researcher, knowledge interface, writer, analyst, planner.  
**Secondary roles:** operator, coordinator.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Primary | Gemini Deep Research is a dedicated multi-step research mode. |
| Synthesis | Primary | Research and Workspace workflows. |
| Writing / editing | Primary | Gemini in Docs and related Workspace surfaces. |
| Document transformation | Primary | Workspace file context and generation. |
| Presentation | Primary | Gemini in Slides / Workspace generation workflows. |
| Communication / meeting work | Material | Gmail/Chat context and Workspace integrations. |
| Analysis | Primary | Sheets and research workflows. |
| Planning | Material | General assistant + research/workspace workflows. |
| Structured knowledge work | Primary | Workspace context and persistent business information. |
| Multi-step execution | Material | Research and agentic capability layers; exact execution surface is product dependent. |

### Work interaction model
- Conversational entry point plus in-context Workspace surfaces.
- Deep Research can combine public web information with selected Gmail, Drive, Docs, Slides, Sheets and Chat context.
- Artifact work happens inside familiar Workspace applications.
- The user's selected sources become part of the task context.

### Agentic execution
- **Planning:** explicit in Deep Research.
- **Context gathering:** public web + Google Workspace sources.
- **Tool use:** Workspace tools and Google ecosystem.
- **Browser/computer:** Google documents a computer-use API capability; availability/productization varies.
- **File/artifact manipulation:** Docs, Sheets and Slides are central output surfaces.
- **Long-running/background:** some newer Google Workspace agent features are designed for recurring/personal-agent workflows; exact availability is product dependent.
- **Verification:** research outputs can cite sources; Workspace edits remain human-reviewable.
- **Retry/repair:** iterative conversational refinement supported; no blanket guarantee of autonomous recovery.
- **Approval:** product surface and Workspace permissions govern actions.

### Artifact model
Docs, Sheets, Slides, research reports and work-product updates in Workspace surfaces.

### Integration / context
- Gmail, Drive, Docs, Slides, Sheets, Google Chat.
- Web/search context.
- Google Workspace identity and permissions.
- Product/plan dependent access to advanced agent capabilities.

### Usage model
Direct Q&A → research delegation → Workspace co-working → artifact review → recurring/personal-agent workflows where enabled.

### Orchestration role
**Primary worker + researcher + knowledge interface + document worker.**

### Constraints / economics
- Workspace and advanced Gemini capabilities vary by subscription, organization, region and product.
- The exact 2026 Workspace feature matrix was not normalized across all Google plans in this card set.

### Evidence / uncertainty
- **Product fact:** Gemini Deep Research can use Gmail/Drive/Chat context; Gemini is embedded into Docs/Sheets/Slides/Drive.
- **Vendor claim:** broader agentic execution beyond research.
- **Independent evidence:** not established for end-to-end work reliability here.
- **Unknown:** exact access to newer agent features for a specific account.

**Sources:**  
S03 — https://gemini.google.com/  
S04 — https://support.google.com/gemini/  
S54 — https://ai.google.dev/gemini-api/docs/computer-use  
Additional current sources — https://blog.google/products-and-platforms/products/gemini/deep-research-workspace-app-integration/  
https://blog.google/products-and-platforms/products/workspace/gemini-workspace-updates-march-2026/

---

## G-04 — Microsoft 365 Copilot (Microsoft)

### Identity
- **Company:** Microsoft
- **Region:** Global
- **Product family:** Microsoft 365 Copilot, including Researcher, Analyst and Word/Excel/PowerPoint Agents
- **Snapshot:** 2026-09-24
- **Source anchors:** S05, S06.

### Work positioning
**What is this AI for?**  
An office-native enterprise Work AI layer embedded in the Microsoft 365 work stack, using organizational content and application context to support documents, analysis, communication, meetings and specialized agent workflows.

**Primary roles:** document worker, analyst, meeting assistant, researcher, planner.  
**Secondary roles:** writer, coordinator, reviewer.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Primary | Researcher agent is explicitly designed for complex multi-step research. |
| Synthesis | Primary | Researcher/Copilot and document workflows. |
| Writing / editing | Primary | Word/Outlook/Copilot surfaces. |
| Document transformation | Primary | Office-native content editing and agents. |
| Presentation | Primary | PowerPoint and PowerPoint Agent workflows. |
| Communication / meeting work | Primary | Outlook and Teams integration. |
| Analysis | Primary | Excel and Analyst workflows. |
| Planning | Material | Copilot agents and work-graph context support planning tasks. |
| Structured knowledge work | Primary | Microsoft 365 content and Graph/enterprise context. |
| Multi-step execution | Primary | Researcher and file-creation agents are explicitly multi-step. |

### Work interaction model
- Embedded in Office applications and the Copilot app.
- Researcher distinguishes complex multi-step research from standard chat.
- Work context spans files, emails, meetings and chats that the user is permitted to access.
- Specialized agents provide more structured work flows than ordinary Q&A.

### Agentic execution
- **Planning:** Researcher plans complex research workflows.
- **Context gathering:** web + permitted Microsoft work content.
- **Tool use:** Microsoft 365/Graph context and installed agents.
- **Browser/external:** web research is built into Researcher; external-app execution varies.
- **File/artifact manipulation:** Word, Excel and PowerPoint Agents can create files.
- **Long-running/background:** scheduled prompts and agent capabilities exist, with availability varying by plan.
- **Verification:** source citations in Researcher; Office artifacts remain reviewable/editable.
- **Retry/repair:** iterative Office/Copilot interaction; autonomous retry depth varies.
- **Approval:** admin controls, licensing and enterprise permissions constrain access and agent availability.

### Artifact model
Word documents, Excel workbooks, PowerPoint presentations, reports, analyses, meeting summaries and related Microsoft 365 artifacts.

### Integration / context
- Word, Excel, PowerPoint, Outlook, Teams, OneNote.
- Work content via Microsoft Graph and eligible connectors.
- Enterprise identity, licensing and admin controls.

### Usage model
Embedded co-working → specialist-agent invocation → research delegation → artifact creation/review → enterprise workflow.

### Orchestration role
**Primary worker + document worker + analyst + researcher + meeting assistant.**

### Constraints / economics
- Many advanced capabilities require a paid Microsoft 365 Copilot license.
- Microsoft documents that Word/Excel/PowerPoint Agents are premium capabilities and currently depend on enabled Anthropic models at the tenant level.
- Feature availability differs by license, tenant, region and cloud environment.

### Evidence / uncertainty
- **Product fact:** Researcher is a multi-step research agent using web and permitted work content; file-creation agents create Office artifacts.
- **Vendor claim:** broader Copilot productivity gains.
- **Independent evidence:** not treated as proof of end-to-end reliability.
- **Unknown:** precise tenant-level availability for every agent feature.

**Sources:**  
S05 — https://learn.microsoft.com/microsoft-365-copilot/  
S06 — https://learn.microsoft.com/en-us/microsoft-365/copilot/researcher-agent  
Additional current sources — https://learn.microsoft.com/en-us/microsoft-365/copilot/wordexcelppt-agents  
https://learn.microsoft.com/en-us/microsoft-365/copilot/faq-researcher  
https://learn.microsoft.com/zh-tw/office365/servicedescriptions/office-365-platform-service-description/microsoft-365-copilot

---

## G-05 — Perplexity

### Identity
- **Company:** Perplexity
- **Region:** Global
- **Product family:** Perplexity, including Research, Computer, Comet and related work-agent surfaces
- **Snapshot:** 2026-09-24
- **Source anchors:** S07, S08, S55.

### Work positioning
**What is this AI for?**  
A research-first Work AI family that moves from web information discovery and cited synthesis toward executable browser/computer work.

**Primary roles:** researcher, analyst, knowledge interface.  
**Secondary roles:** operator, writer, coordinator.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Primary | Research is the central product archetype. |
| Synthesis | Primary | Cited web synthesis and research reports. |
| Writing / editing | Material | Research-to-report workflows and file/app creation. |
| Document transformation | Material | Files and Create files/apps features. |
| Presentation | Possible | Can create files/apps; exact presentation depth varies. |
| Communication / meeting work | Material | Comet Agent can act on email/calendar workflows in supported environments. |
| Analysis | Primary | Research/competitive-intelligence and complex analysis use cases. |
| Planning | Primary | Agentic browser workflows require multi-step planning. |
| Structured knowledge work | Primary | Research, files and enterprise knowledge workflows. |
| Multi-step execution | Primary | Comet Agent is explicitly a digital executor for multi-step tasks. |

### Work interaction model
- Research/search-first interface.
- Computer/Comet surfaces extend work into browser execution.
- Enterprise Comet includes Assistant and Agent as distinct interaction modes.
- Agent pauses for important or sensitive confirmations.

### Agentic execution
- **Planning:** multi-step research and Comet actions.
- **Context gathering:** web, browser tabs, files and enterprise app context.
- **Tool use:** browser/computer actions and connected applications.
- **Browser/external systems:** central product differentiator.
- **File/artifact manipulation:** files and app creation are part of the product family.
- **Long-running/background:** agentic tasks can span multiple actions; exact background semantics vary.
- **Verification:** citations in research; confirmation before important/sensitive actions in Comet Agent.
- **Retry/repair:** conversational corrections and agent continuation supported; universal autonomous recovery not established.
- **Approval:** explicit confirmations for important/sensitive operations in enterprise Comet.

### Artifact model
Research reports, cited answers, files and generated applications/artifacts.

### Integration / context
- Web and browser.
- Comet integrates AI into the browsing environment.
- Enterprise controls include MDM, browser policies, agent permissions and audit/telemetry capabilities for qualifying plans.
- Connected apps depend on product/enterprise configuration.

### Usage model
Research delegation → iterative evidence review → browser execution → artifact creation → action confirmation.

### Orchestration role
**Researcher + analyst + operator.**  
Analysis: a natural product role is “research-to-action bridge”.

### Constraints / economics
- Features are tier dependent; Enterprise Pro/Max expose different security, collaboration and access features.
- Enterprise Comet adds administrative controls and enterprise security.
- Exact limits were not normalized across all plans.

### Evidence / uncertainty
- **Product fact:** Comet Agent performs multi-step browser tasks and can require confirmation for sensitive operations.
- **Vendor claim:** broad research/action automation.
- **Independent evidence:** not established here.
- **Unknown:** exact capabilities available in non-enterprise Comet configurations.

**Sources:**  
S07 — https://www.perplexity.ai/hub  
S08 — https://www.perplexity.ai/help-center/  
S55 — https://www.perplexity.ai/help-center/zh-CN/articles/12781449-mianxiang-enterprise-de-comet  
Additional current source — https://www.perplexity.ai/help-center/en/articles/12310544-what-is-enterprise-max

---

## G-06 — Glean

### Identity
- **Company:** Glean
- **Region:** Global / Enterprise
- **Product family:** Glean Work AI / Glean Agents
- **Snapshot:** 2026-09-24
- **Source anchor:** S09.

### Work positioning
**What is this AI for?**  
Enterprise-first Work AI that grounds assistants and agents in organizational knowledge, permissions, context, tools and processes, then lets agents execute work across enterprise surfaces.

**Primary roles:** knowledge interface, researcher, analyst, coordinator, execution agent.  
**Secondary roles:** reviewer, document worker.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Primary | Enterprise knowledge + external/internal context. |
| Synthesis | Primary | Cross-source enterprise synthesis. |
| Writing / editing | Material | Agents produce work outputs and reports. |
| Document transformation | Material | Depends on connected applications and workflows. |
| Presentation | Possible | Not the defining product surface. |
| Communication / meeting work | Material | Slack/Teams and enterprise workflows can provide context/actions. |
| Analysis | Primary | Enterprise investigation and issue analysis. |
| Planning | Material | Agents use instructions, tools, context and workflow steps. |
| Structured knowledge work | Primary | Core product position. |
| Multi-step execution | Primary | Glean explicitly describes agents that own workflows. |

### Work interaction model
- Search/knowledge interface combined with reusable agent surface.
- Agent Builder supports **Auto mode** and **Workflow mode**.
- Workflow mode makes steps, branches and hand-offs explicit.
- Agents can be reused by teams, embedded in enterprise work surfaces and governed by permissions.
- Independent agents can proactively act without a fresh prompt.

### Agentic execution
- **Planning:** Auto mode and workflow definitions.
- **Context gathering:** enterprise knowledge graph/indexing, connected apps, permissions.
- **Tool use:** configured tools/actions.
- **Browser/external:** not primarily browser-first; enterprise apps are the core execution context.
- **File/artifact:** outputs and memory are retained as part of agent runs; exact artifact types vary by workflow.
- **Long-running/background:** independent agents are explicitly designed to act proactively.
- **Verification:** traceability/accountability are part of the documented design.
- **Retry/repair:** iterative workflow execution is supported; autonomous self-repair depth varies by agent design.
- **Approval:** organization-defined permissions and human decision points.

### Artifact model
Reports, workflow outputs, agent-run results and updates to connected enterprise systems.

### Integration / context
- Enterprise search/knowledge graph.
- Slack, Teams, Jira, GitHub and other connected systems where configured.
- Identity, permissions and agent-specific provisioned access are central to the model.

### Usage model
Knowledge Q&A → delegated agent execution → proactive/background work → workflow reuse → human escalation when a real decision is needed.

### Orchestration role
**Enterprise knowledge interface + researcher + coordinator + execution agent.**

### Constraints / economics
- Enterprise-first; deployment, connector, permission and admin work are part of the setup burden.
- Publishing/sharing agents is permissioned.
- Product value depends on the quality and coverage of organizational context.

### Evidence / uncertainty
- **Product fact:** Glean Agents combine instructions, knowledge, tools, context, execution, output and memory; independent agents can act proactively with their own provisioned identity.
- **Vendor claim:** improvements to productivity and autonomous work.
- **Independent evidence:** not established here.
- **Unknown:** actual end-to-end reliability for arbitrary enterprise workflows outside documented examples.

**Sources:**  
S09 — https://www.glean.com/  
Additional current sources — https://www.glean.com/blog/introducing-independent-agents  
https://docs.glean.com/agents/how-agents-work  
https://docs.glean.com/administration/managing-agents/agent-access  
https://docs.glean.com/agents/concepts/sharing-permissions

---

## G-07 — Notion

### Identity
- **Company:** Notion
- **Region:** Global
- **Product family:** Notion Agents / Custom Agents / external-agent orchestration
- **Snapshot:** 2026-09-24
- **Source anchors:** S11, S12.

### Work positioning
**What is this AI for?**  
A workspace-native Work AI family in which AI operates directly on persistent pages, databases and connected tools, turning knowledge and recurring workflows into executable team processes.

**Primary roles:** document worker, planner, coordinator, knowledge interface, reviewer.  
**Secondary roles:** researcher, operator, writer.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Material | Web and connected knowledge can be used where granted. |
| Synthesis | Primary | Workspace knowledge and status/report workflows. |
| Writing / editing | Primary | Native page/document context. |
| Document transformation | Primary | Pages, databases and supported files. |
| Presentation | Material | 2026 releases include Excel/PowerPoint file handling; presentation depth varies. |
| Communication / meeting work | Material | Slack and meeting-related workflows are integrated. |
| Analysis | Material | Database/report workflows. |
| Planning | Primary | Project/task/workspace context. |
| Structured knowledge work | Primary | This is the core product surface. |
| Multi-step execution | Primary | Custom Agents execute workflows across triggers, context and actions. |

### Work interaction model
- Artifact/workspace-centric rather than chat-only.
- Notion Agent can work interactively in the workspace.
- Custom Agents are designed to run automatically from schedules or events.
- Agents can read granted Notion pages/databases and connected apps.
- External agents such as Claude and Cursor can be orchestrated from Notion in supported workflows.

### Agentic execution
- **Planning:** user defines job/outcome/instructions; Custom Agent follows configured workflow.
- **Context gathering:** Notion pages/databases + permitted apps + optional web.
- **Tool use:** connected applications, database actions, messaging and workflow actions.
- **Browser/external:** web access can be enabled; external agent integration is a distinct surface.
- **File/artifact manipulation:** pages, databases, reports and supported Office files.
- **Long-running/background:** central differentiator—schedule/event-triggered agents run automatically.
- **Verification:** runs are logged; changes can be visible/reversible depending on workflow.
- **Retry/repair:** workflow can be decomposed into multiple agents; exact automatic recovery is configuration dependent.
- **Approval:** access controls and agent permissions govern what the agent can see/do.

### Artifact model
Notion pages, database records, reports, task updates, external workflow outputs and supported office files.

### Integration / context
- Notion pages/databases.
- Slack, Mail, Calendar, Figma, Linear and custom MCP servers are documented for Custom Agents.
- External agents such as Claude and Cursor can be orchestrated from Notion.
- Workspace permissions are central to the model.

### Usage model
Workspace co-working → custom agent setup → scheduled/triggered background work → shared team agent → external-agent handoff.

### Orchestration role
**Workspace coordinator + document worker + execution agent.**

### Constraints / economics
- Custom Agents moved to usage-based Notion Credits after the public beta period beginning May 4, 2026.
- Feature availability depends on plan, workspace and enabled integrations.
- Setup quality is sensitive to instruction quality, trigger design and access configuration.

### Evidence / uncertainty
- **Product fact:** Custom Agents run on schedules/triggers, use granted workspace/connected-app context and can take actions such as reports, bug filing, record updates and messages.
- **Vendor claim:** productivity benefits.
- **Independent evidence:** not established here.
- **Unknown:** behavior and limits across all connected applications.

**Sources:**  
S11 — https://www.notion.com/product/agents  
S12 — https://www.notion.com/help/notion-agent  
Additional current sources — https://www.notion.com/help/custom-agents  
https://www.notion.com/releases/2026-02-24  
https://www.notion.com/releases/2026-07-01

---

## G-08 — Harvey

### Identity
- **Company:** Harvey
- **Region:** Global / Legal enterprise
- **Product family:** Harvey legal AI / agents / workflows
- **Snapshot:** 2026-09-24
- **Source anchor:** S28.

### Work positioning
**What is this AI for?**  
A vertical Knowledge Work platform for legal professionals that applies domain context, matter files, legal sources, workflow templates and agentic execution to research, drafting, review and analysis while leaving professional judgment with the lawyer.

**Primary roles:** researcher, analyst, writer, reviewer, execution agent.  
**Secondary roles:** coordinator, document worker.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Primary | Legal research and authority synthesis. |
| Synthesis | Primary | Matter-level legal analysis. |
| Writing / editing | Primary | Drafting and redline workflows. |
| Document transformation | Primary | Contract review, redlining and document generation. |
| Presentation | Material | Harvey agents can produce PowerPoint in documented workflows. |
| Communication / meeting work | Material | Professional workflow support, but not the defining surface. |
| Analysis | Primary | Contract, diligence, regulatory and litigation analysis. |
| Planning | Primary | Legal agents execute matter workflows across steps. |
| Structured knowledge work | Primary | Core product category. |
| Multi-step execution | Primary | Agentic platform and long-horizon legal work are explicit product goals. |

### Work interaction model
- Matter/workspace context is central.
- Agents are task-specific and can be reused across legal workflows.
- Humans review outputs and retain responsibility for strategy/judgment.
- Harvey provides both ready-to-use agents and customization/building surfaces.

### Agentic execution
- **Planning:** legal agents plan multi-step work.
- **Context gathering:** matter files, legal materials, structured data and workflow context.
- **Tool use:** domain-specific retrieval and document operations.
- **Browser/external:** depends on supported legal/data integrations; not primarily a browser-agent product.
- **File/artifact manipulation:** Word, PowerPoint and Excel outputs are documented.
- **Long-running:** longer processes and end-to-end legal workflows are explicit product direction.
- **Verification:** sources/citations and lawyer review are central to professional use.
- **Retry/repair:** specialized agent workflows can iterate; actual recovery behavior is workflow dependent.
- **Approval:** professional review is the human boundary.

### Artifact model
Drafts, redlines, issue lists, legal research reports, diligence outputs, review tables, Word/PowerPoint/Excel work products.

### Integration / context
- Legal matter context and documents.
- Legal research/evidence sources.
- Professional workflow and confidentiality controls.
- Integrations vary by enterprise deployment.

### Usage model
Matter intake → research/review delegation → artifact generation → lawyer review → iterative revision → reusable workflow/agent.

### Orchestration role
**Vertical specialist + researcher + analyst + writer + reviewer.**

### Constraints / economics
- Enterprise/legal deployment model.
- High-stakes professional context raises review, confidentiality and citation requirements.
- Product value depends on domain grounding and matter context, not only generic model capability.

### Evidence / uncertainty
- **Product fact:** Harvey documents agents for drafting, analysis, research and review-ready work; its platform includes reusable/custom agents and durable professional deliverables.
- **Vendor claim:** broad legal-agent performance.
- **Independent evidence:** Harvey's LAB is an evaluation framework, but it is vendor-created and is not treated as independent proof of product effectiveness.
- **Unknown:** exact parity of every legal workflow across jurisdictions and products.

**Sources:**  
S28 — https://www.harvey.ai/  
Additional current sources — https://www.harvey.ai/blog/ai-agents-for-legal-work  
https://www.harvey.ai/blog/agentic-platform-updates  
https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark  
https://www.harvey.ai/blog/legal-workflow-automation

---

## G-09 — Writer

### Identity
- **Company:** Writer
- **Region:** Global / Enterprise
- **Product family:** WRITER enterprise AI / agents / Enterprise Brain / Knowledge Graph
- **Snapshot:** 2026-09-24
- **Source anchor:** S10.

### Work positioning
**What is this AI for?**  
An enterprise agent platform for content and revenue/marketing work that combines organizational knowledge, brand standards, reusable workflows and agentic execution to produce finished business deliverables.

**Primary roles:** writer, editor, reviewer, coordinator, knowledge interface.  
**Secondary roles:** analyst, execution agent.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Material | Enterprise knowledge and agent workflows can support information gathering. |
| Synthesis | Primary | Enterprise context + generated deliverables. |
| Writing / editing | Primary | Core product position. |
| Document transformation | Primary | Finished documents/workflows are explicit outputs. |
| Presentation | Material | WRITER documents finished presentation deliverables. |
| Communication / meeting work | Material | WRITER Meet and Slack/Teams integrations extend into communication. |
| Analysis | Material | Enterprise agents can execute data/context-driven workflows. |
| Planning | Primary | Product documentation says agents break goals into steps and select tools/workflows. |
| Structured knowledge work | Primary | Company knowledge, brand standards and workflows are central. |
| Multi-step execution | Primary | Agents plan, execute and produce finished deliverables. |

### Work interaction model
- Goal/outcome-driven rather than only chat response.
- Company knowledge and standards are embedded into the agent runtime.
- Knowledge Graph supplies grounded enterprise context.
- Enterprise Brain adds a broader context/memory layer.
- Autopilot/background execution is part of the current positioning.

### Agentic execution
- **Planning:** breaks goals into steps.
- **Context gathering:** organizational knowledge and live business context.
- **Tool use:** Gmail, Slack, Teams and other connected systems.
- **Browser/external:** not the defining work surface; connected application execution is more central.
- **File/artifact manipulation:** documents, spreadsheets, presentations and completed actions.
- **Long-running/background:** product documentation explicitly describes autopilot/automatic workflows.
- **Verification:** governed knowledge/brand/compliance layers and workflow controls.
- **Retry/repair:** workflow execution can be refined; autonomous repair depth is not independently established.
- **Approval:** enterprise controls and workflow configuration define human boundaries.

### Artifact model
Documents, spreadsheets, presentations, reports and completed actions in connected systems.

### Integration / context
- Enterprise Brain / institutional knowledge.
- Knowledge Graph.
- Gmail, Slack, Teams, Figma and browser extensions where supported.
- Enterprise governance, brand and compliance context.

### Usage model
Goal delegation → contextual planning → autonomous workflow → artifact review → repeatable process.

### Orchestration role
**Enterprise content worker + coordinator + reviewer; increasingly an execution agent.**

### Constraints / economics
- Enterprise-oriented procurement and deployment.
- Knowledge quality, governance configuration and connector setup materially affect outcomes.
- Plan eligibility differs by feature; current Knowledge Graph documentation distinguishes Starter/Enterprise access.

### Evidence / uncertainty
- **Product fact:** WRITER documents agentic work that plans, executes and produces finished deliverables; current materials describe Enterprise Brain, Agent Memory, and multiple communication surfaces.
- **Vendor claim:** enterprise-agent productivity/transformation claims.
- **Independent evidence:** not established here.
- **Unknown:** end-to-end performance across arbitrary enterprise processes.

**Sources:**  
S10 — https://writer.com/  
Additional current sources — https://support.writer.com/articles/3099016123-what-is-writer  
https://support.writer.com/articles/6965386512-how-to-create-and-manage-a-knowledge-graph  
https://writer.com/blog/enterprise-brain-press-release/

---

## G-10 — Zapier Agents

### Identity
- **Company:** Zapier
- **Region:** Global
- **Product family:** Zapier Agents
- **Snapshot:** 2026-09-24
- **Source anchor:** S50.

### Work positioning
**What is this AI for?**  
A cross-application execution layer that turns natural-language objectives into agentic work across connected business applications, especially where the value lies in taking actions rather than only generating information.

**Primary roles:** operator, coordinator, execution agent.  
**Secondary roles:** researcher, analyst, reviewer.

### Task fit
| Task class | Fit | Evidence basis |
|---|---|---|
| Research | Material | Can gather/use knowledge sources where configured. |
| Synthesis | Material | Agent can combine information before taking actions. |
| Writing / editing | Material | Generated content can be passed into downstream apps. |
| Document transformation | Material | Depends on connected application actions. |
| Presentation | Possible | Not the defining capability. |
| Communication / meeting work | Primary | Email/messaging/workflow automation is a core connected-app scenario. |
| Analysis | Material | Can process/contextualize inputs before action. |
| Planning | Primary | Agents execute multi-step tasks from instructions. |
| Structured knowledge work | Material | Strong when work crosses multiple systems. |
| Multi-step execution | Primary | Core category: multi-step automation across apps. |

### Work interaction model
- Agent creation/configuration defines instructions, knowledge and action scope.
- Trigger/event and instruction design matter.
- Agents can call other agents, enabling modular workflows.
- This is more workflow-centric than artifact-centric.

### Agentic execution
- **Planning:** natural-language task decomposition/execution.
- **Context gathering:** configured knowledge sources and app data.
- **Tool use:** connected apps/actions.
- **Browser/external:** application integrations are the main execution surface.
- **File/artifact:** writes outputs into connected systems; exact artifact type depends on apps.
- **Long-running/background:** trigger-driven automation is central.
- **Verification:** Zapier recommends testing with real workflow data before deployment.
- **Retry/repair:** modular agent-to-agent calls can split work; self-repair depth depends on agent design.
- **Approval:** workflow configuration and app permissions determine where human action is required.

### Artifact model
Email/messages, records, documents/files, task updates, CRM objects, workflow outputs and other application-native artifacts.

### Integration / context
- Large connected-app ecosystem.
- Knowledge sources can be synchronized to agents.
- Agents can invoke other agents.
- Access and app permissions are core to execution boundaries.

### Usage model
Trigger → delegated execution → cross-app actions → downstream artifact creation/update → human exception handling.

### Orchestration role
**Operator + coordinator + cross-app execution agent.**  
Analysis: Zapier is most informative when a task has already been decomposed enough to map actions across systems.

### Constraints / economics
- Setup/configuration effort is non-trivial for reliable agent behavior.
- Zapier recommends focused agents with limited action scope and thorough testing.
- Costs/limits depend on the Zapier product plan and usage of connected automation resources; exact economics are not normalized here.

### Evidence / uncertainty
- **Product fact:** Zapier Agents are documented as AI assistants that automate complex workflows through natural language, knowledge sources, triggers and actions.
- **Vendor claim:** productivity and scale benefits.
- **Independent evidence:** not established here.
- **Unknown:** end-to-end reliability for arbitrary unstructured workflows; agent quality is strongly affected by scope and source configuration.

**Sources:**  
S50 — https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents  
Additional current source — https://help.zapier.com/hc/en-us/articles/24593355420429-Best-practices-for-working-with-Zapier-Agents

---

# 3. Cross-Product Normalization Notes

## 3.1 Product-family boundary

The cards intentionally keep the following as **capabilities or modes of the representative family**, not additional product rows:

| Capability / mode | Parent family |
|---|---|
| Deep Research / Work / computer-use capability | ChatGPT |
| Cowork / computer use / Claude Tag | Claude |
| Deep Research / Computer Use / Workspace agent layers | Gemini |
| Researcher / Analyst / Word-Excel-PowerPoint Agents | Microsoft 365 Copilot |
| Research / Computer / Comet | Perplexity |

This follows the product-family normalization rule in `global-landscape.md`.

## 3.2 Work-positioning archetypes surfaced by the cards

These labels are **analytical shorthand for downstream synthesis**, not permanent market categories:

| representative_id | Product family | Primary analytical position |
|---|---|---|
| G-01 | ChatGPT | Broad general-purpose Work AI |
| G-02 | Claude | General-purpose knowledge-work + agentic work surface |
| G-03 | Gemini | General-purpose Work AI + Workspace context |
| G-04 | Microsoft 365 Copilot | Office-native enterprise Work AI |
| G-05 | Perplexity | Research-first Work AI → browser execution |
| G-06 | Glean | Enterprise knowledge + governed agents |
| G-07 | Notion | Workspace-native persistent agents |
| G-08 | Harvey | Vertical professional Knowledge Work agent |
| G-09 | Writer | Enterprise content/context + agentic workflows |
| G-10 | Zapier Agents | Cross-application execution / automation boundary |

## 3.3 Recurring capability dimensions

Across the ten families, the most reusable capability dimensions are:

- **Knowledge access:** web, files, workspace content, enterprise knowledge.
- **Reasoning/synthesis:** turning heterogeneous inputs into a coherent work result.
- **Artifact production:** documents, spreadsheets, presentations, reports, records or other durable work objects.
- **Tool/action execution:** moving from advice to actions in connected software.
- **Persistent context:** projects, workspace state, enterprise knowledge, memory or agent configuration.
- **Autonomy/time:** one-shot response → delegated multi-step work → trigger/schedule-driven execution.
- **Governance:** permissions, approvals, auditability, enterprise policy.
- **Specialization:** general-purpose capability vs domain/workflow-specific agent.

These are observations for Tasks 4.1.1 / 4.2.1, not a final taxonomy.

---

# 4. Cross-Product Usage Pattern Summary

| Pattern | Representative examples | Boundary / meaning |
|---|---|---|
| **Ask → answer** | ChatGPT, Claude, Gemini | Low coordination; suitable for bounded knowledge tasks. |
| **Delegate → finished artifact** | ChatGPT Work, Claude/Cowork, Microsoft 365 Copilot, Writer | AI carries more of the execution burden and returns a durable work product. |
| **Workspace-native co-working** | Microsoft 365 Copilot, Gemini, Notion, Glean | Context is embedded where work already lives. |
| **Research → cited synthesis** | ChatGPT Deep Research, Gemini Deep Research, Perplexity, Microsoft Researcher, Glean | Source discovery and synthesis are first-class workflow stages. |
| **Persistent agent → recurring work** | Notion Custom Agents, Glean independent agents, Writer autopilot, Zapier Agents | The value shifts from completing one task to keeping a process moving. |
| **Specialist agent → professional review** | Harvey | Domain context and human judgment remain tightly coupled. |
| **Research → browser action** | Perplexity / Comet | Agent crosses from information retrieval into external-system operation. |
| **Workflow → cross-app execution** | Zapier Agents | The main product contribution is coordinated action across systems. |

---

# 5. Evidence & Uncertainty Register

## Product facts with strong primary-source support
- Current ChatGPT Work is positioned for longer tasks, connected apps/files, finished deliverables and scheduled work.
- Claude provides projects, artifacts and agentic/Cowork capabilities; Anthropic documents computer-use capability.
- Gemini Deep Research can combine web information with Google Workspace context, and Gemini is embedded into Workspace apps.
- Microsoft Researcher is a multi-step research agent over web and permitted work content; Office file-creation agents exist for paid Copilot tenants.
- Perplexity's Enterprise Comet includes Assistant and Agent surfaces, with Agent able to perform multi-step browser actions and request confirmation for sensitive actions.
- Glean Agents combine instructions, knowledge, tools, context, execution, output and memory; independent agents add proactive execution with provisioned identity.
- Notion Custom Agents run from triggers/schedules and can act on workspace/connected-app context; Notion also exposes external-agent orchestration.
- Harvey positions agents around legal research, drafting, review and durable professional work products.
- Writer documents enterprise agents that plan, execute and produce finished deliverables using organizational knowledge and standards.
- Zapier Agents are documented as natural-language-driven, multi-step, connected-app workflow agents.

## Vendor-claim boundary
The following are intentionally not treated as independently proven:
- universal autonomous reliability;
- productivity uplift percentages;
- broad claims that a product can complete arbitrary Knowledge Work end-to-end;
- claims that one product is universally superior to another.

## Open / unresolved questions for later QA
1. Exact account/plan/region feature availability for every advanced agent mode.
2. Comparable adoption metrics across product families.
3. End-to-end reliability under realistic multi-step workloads rather than individual feature demonstrations.
4. Precise enterprise governance differences where public documentation is incomplete.
5. Product behavior changes after the 2026-09-24 snapshot.

---

# 6. Mechanical Completion Checks

- [x] Ten cards present, matching the Global Representative Top 10.
- [x] One product-family card per representative product.
- [x] Global/China region label present.
- [x] Work-positioning statement present for every card.
- [x] Primary and secondary analytical roles present.
- [x] Task-fit assessment covers all required task classes.
- [x] Interaction model recorded.
- [x] Persistent context / memory recorded where material.
- [x] Agentic execution dimensions recorded.
- [x] Artifact model recorded.
- [x] Integration/context recorded.
- [x] Usage model recorded.
- [x] Orchestration role recorded.
- [x] Constraints/economics recorded where material.
- [x] Evidence / uncertainty separation present.
- [x] Change-sensitive facts tied to the 2026-09-24 snapshot framing.
- [x] No numeric product-quality score.
- [x] No universal “best” ranking.
- [x] No permanent product-to-task mapping.
- [x] Product modes are normalized under parent product families.
- [ ] Atomic claim → evidence → source → date normalization — **Task 5.1.1**.
- [ ] Independent source audit of all material claims — **Task 5.1.1**.
- [ ] Human review of representative-set and consequential interpretation — **Task 5.2.1 / human review gate**.

---

## 7. Handoff to Downstream Tasks

### Task 4.1.1 — Canonical Work AI taxonomy / task-capability / work-role model
Use the cards to derive:
- recurring capability dimensions;
- task-fit distinctions;
- work-role patterns;
- the difference between general, contextual, specialized and action-oriented work.

Do not turn this packet into a timeless product-routing table.

### Task 4.2.1 — Orchestration patterns
Use:
- Perplexity as a research-to-action bridge;
- Glean / Notion / Writer as persistent or proactive agent examples;
- Harvey as specialist + professional-review boundary;
- Zapier as cross-app execution boundary;
- general-purpose families as one-AI baselines.

For every proposed multi-AI pattern, identify the concrete capability gap before introducing the second AI.

### Task 5.1.1 — Evidence QA
Normalize all material claims from these cards into:
`claim → evidence → source → date → confidence → limitation`.

Prioritize:
- plan/access-sensitive claims;
- autonomy claims;
- enterprise governance claims;
- adoption/significance claims;
- any comparative claim between product families.

---

## 8. Status

**Task 2.3.1 deliverable status: REVIEW**

The Global section is complete at the product-characterization layer. It is ready for source-register normalization and downstream analytical use, but should not yet be treated as FROZEN authority until Task 5.1.1 completes evidence QA.
