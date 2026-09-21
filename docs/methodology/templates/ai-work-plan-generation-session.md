# AI Work Plan Generation Session

> Purpose: Convert an approved Research Charter into a concrete case-specific 01-ai-work-plan.md.
> Boundary: Planning only. Do not execute research or delivery work in this session.

## 1. Session Role

Load the approved Research Charter and reusable AI Work Advisor Prompt v1, then dynamically determine how the current AI ecosystem should be used for the case.

## 2. Required Inputs

Research Charter:
~~~text
cases/<case-id>/00-research-charter.md
~~~

AI Work Advisor Prompt:
~~~text
docs/methodology/ai-work-advisor-v1.md
~~~

Optional:
- user constraints;
- available AI subscriptions / tools;
- relevant files;
- repository context;
- existing artifacts;
- cost / time limits;
- required output formats;
- connector / MCP / Skill availability.

Do not assume the optional tool list is complete.

## 3. Input Validation

Before planning:
1. confirm the Charter is approved;
2. read enough of the Charter to preserve intent;
3. identify questions, scope, population, evidence requirements, deliverables, success criteria, and human decisions;
4. do not silently change Charter intent.

If materially ambiguous, record an explicit assumption or recommend Charter revision.

## 4. Current AI Ecosystem Discovery

Actively obtain current information where it can affect product/model/configuration selection.

Research only what is needed about:
- current AI capabilities;
- available products;
- model / mode / thinking options;
- access / subscription / cost;
- context limits;
- connectors / MCP / Skills;
- product entry points and relevant workflow capabilities.

Source priority:
1. official;
2. high-quality independent;
3. community.

Stop when sufficient for candidate generation, comparison, selection, and configuration.

## 5. Planning Workflow

Apply:

Understand Task
→ Decompose Work
→ Identify Required Capabilities
→ Identify Current-Ecosystem Knowledge Requirements
→ Acquire & Verify Current AI Ecosystem Knowledge
→ Generate Candidates
→ Select Products
→ Select Models
→ Configure Mode / Thinking
→ Choose Session Strategy
→ Choose Context Strategy
→ Choose File Strategy
→ Choose Connector / MCP Strategy
→ Choose Skill / Instruction Strategy
→ Design AI Orchestration
→ Define Artifacts
→ Define Verification
→ Self-review

## 6. Selection Rules

Use:
- current over memorized;
- capability over brand;
- evidence over assertion;
- minimal effective tool set;
- existing AI over rebuilding.

Before adding another AI, identify the concrete gap it fills.

## 7. Configuration & Orchestration

For each meaningful task specify, as applicable:
- Product
- Model
- Mode
- Thinking
- Session
- Context
- Files
- Connectors
- Skills
- Instruction

For each handoff specify producer, artifact, consumer, purpose, and verification point.

Prefer durable artifact handoffs.

## 8. Output Contract

Write:

~~~text
cases/<case-id>/01-ai-work-plan.md
~~~

Use exactly:
- 0. Plan Metadata
- 1. Executive Work Strategy
- 2. AI Ecosystem Selection Summary
- 3. Global Execution Rules
- 4. Detailed Work Plan
- 5. Artifact & Handoff Map
- 6. Verification & Human Review
- 7. Plan Assumptions / Uncertainties

Every meaningful Task uses all fixed Work Plan fields.

## 9. Self-review

Before output, verify:
- every Charter requirement is represented;
- Charter intent was preserved;
- volatile product facts were checked;
- tool set is minimal;
- one-AI sufficiency was considered;
- meaningful alternatives are recorded;
- inputs / outputs are concrete;
- handoffs are traceable;
- verification is explicit;
- human responsibility is visible;
- access / cost constraints are visible;
- uncertainty is not hidden;
- no execution happened.

## 10. Planning-only Boundary

The session ends after producing the Work Plan and its assumptions / uncertainties.

Do not continue into:
- research;
- source collection;
- ranking;
- product testing;
- coding;
- report writing;
- document production;
- external actions.

The human reviews the Work Plan before execution.

## 11. Replanning Rules

Re-run the affected planning segment when:
- access constraints change;
- a selected product becomes unavailable;
- material ecosystem information changes;
- a handoff becomes infeasible.

If the Charter materially changes, revise the Charter and generate a new Work Plan version.

Version semantics:
- Charter v1 → Work Plan v1
- execution-constraint adjustment → Work Plan v1.1
- material Charter change → Charter v2 → Work Plan v2
