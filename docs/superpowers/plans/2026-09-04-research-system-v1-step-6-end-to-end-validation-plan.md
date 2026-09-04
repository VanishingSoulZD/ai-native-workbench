# Research System v1 — Step 6 End-to-End Validation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to execute this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Validate Research System v1 against the real Case 001 research without repairing the legacy pipeline or prematurely changing shared system semantics.

**Architecture:** Step 6 is a validation exercise, not a new subsystem implementation. Historical Case 001 assets are reconstructed into the Research System v1 lifecycle, human-approved canonical state, evaluation boundary, and snapshot; existing Step 4 and Step 5 capabilities then produce and rebuild Dataset and Research Note deliveries. Observed gaps are recorded before any system revision is considered.

**Tech Stack:** Existing repository Markdown artifacts; existing Python 3.11+ Research System v1 APIs; existing pytest suite and Step 3–5 public APIs; no new runtime dependency is required by this plan.

**Spec:** `docs/superpowers/specs/2026-09-04-research-system-v1-step-6-end-to-end-validation-design.md`

## Global Constraints

- Treat `cases/001-ai-coding-agent-landscape/` as a Reference / Legacy Research Case; do not repair or reimplement its Phase 8 pipeline.
- Reuse historical research assets before performing any new external research.
- Do not recompute or re-rank the historical Top 10.
- Treat R0–R8 as logical lifecycle stages, not one-file-per-stage requirements.
- Human approval is required for scope, consequential selection, canonicalization/judgment, evaluation acceptance, and final delivery.
- Keep the current canonical vocabulary unchanged during validation: `Entity`, `Claim`, `Evidence`, `Source`, `Unknown`, `Relationship`.
- Do not silently coerce facts, inferences, judgments, hypotheses, scenarios, scores, or Unknowns into misleading canonical semantics.
- Reuse Step 3 validation and Step 4 evaluation/quality-gate semantics rather than creating parallel validators.
- Build only from an explicit `ResearchSnapshot`; historical members must be resolved through snapshot state.
- Use only the Step 5 v1 delivery pair: Dataset + Research Note.
- Do not add databases, artifact registries, queues, distributed execution, agents, multi-agent orchestration, or new renderer infrastructure for Step 6.
- Record every observed gap before deciding whether any shared system change is justified.
- Do not enter Step 7 or Step 8 as part of this plan.

---

## Task 1: Freeze Validation Baseline and Asset Inventory

**Files:**
- Read: `docs/superpowers/specs/2026-09-04-research-system-v1-step-6-end-to-end-validation-design.md`
- Read: `docs/methodology/research-system-v1.md`
- Read: `cases/001-ai-coding-agent-landscape/00-research-charter.md`
- Read: `cases/001-ai-coding-agent-landscape/01-candidate-universe.md`
- Read: `cases/001-ai-coding-agent-landscape/02-market-evidence.md`
- Read: `cases/001-ai-coding-agent-landscape/03-ranking-methodology.md`
- Read: `cases/001-ai-coding-agent-landscape/03-top10-selection.md`
- Read: `cases/001-ai-coding-agent-landscape/04-products/*`
- Read: `cases/001-ai-coding-agent-landscape/05-benchmarks.md`
- Read: `cases/001-ai-coding-agent-landscape/06-cross-product-analysis.md`
- Read: `cases/001-ai-coding-agent-landscape/07-decision.md`
- Read: `cases/001-ai-coding-agent-landscape/08-canonical-research-model.md`
- Read: `cases/001-ai-coding-agent-landscape/08-dataset/*`
- Read: historical delivery/reference artifacts present under `cases/001-ai-coding-agent-landscape/`
- Create: `validation/research-system-v1/case-001/01-case-mapping.md`

**Interfaces:**
- Consumes: the approved Step 6 spec plus the complete current Case 001 asset set.
- Produces: a versioned asset inventory and semantic mapping record used by all later validation tasks.

- [ ] **Step 1: Inventory the historical case**

Record, for every relevant historical artifact:

```text
path
role
research activity
primary lifecycle stage
secondary lifecycle stage(s), when justified
content authority
candidate provenance value
notes / known hazards
```

Do not infer canonical object types yet.

- [ ] **Step 2: Map semantic activity to R0–R8**

Use semantic activity, not filenames, to map the research. Explicitly record why an artifact belongs to a stage when the mapping is non-obvious.

- [ ] **Step 3: Map artifacts to Definition / Working / Canonical / Evaluation / Delivery roles**

Keep the legacy Phase 8 model separate from the Research System v1 model. Record it as historical reference material.

- [ ] **Step 4: Record historical locks and invariants**

At minimum preserve:

```text
research unit
research cutoff
locked Top 10
selection rules
major Unknowns
known discrepancies
historical judgments
```

- [ ] **Step 5: Human gate H1 — Scope confirmation**

The human owner confirms that the validation is replaying the intended historical research problem rather than silently redefining it.

- [ ] **Step 6: Verify the mapping artifact**

Check that every required Case 001 source artifact is represented, every R0–R8 stage has at least one justified activity, and no legacy artifact is treated as authoritative merely because it is named `canonical` or `dataset`.

---

## Task 2: Reconstruct the Working Research State

**Files:**
- Create: `validation/research-system-v1/case-001/02-execution-record.md`
- Create: `validation/research-system-v1/case-001/03-canonicalization-record.md`

**Interfaces:**
- Consumes: Task 1 mapping plus historical Case 001 artifacts.
- Produces: the human-reviewed reconstruction record and candidate canonicalization record.

- [ ] **Step 1: Record R0–R4 reconstruction**

Create one stage record per logical stage containing:

```text
stage
historical_inputs
validation_inputs
reconstructed outputs
human gate
canonical impact
evaluation status
notes
```

The execution record must distinguish direct historical observation from interpretation added during reconstruction.

- [ ] **Step 2: Identify candidate canonical records**

For important research semantics, propose only one of:

```text
Entity
Claim
Evidence
Source
Relationship
Unknown
```

Each candidate record must contain:

```text
historical source
proposed canonical type
proposed identity
semantic interpretation
provenance
qualification / uncertainty
mapping rationale
```

- [ ] **Step 3: Classify non-core semantics**

Explicitly inspect:

```text
Ranking
Selection Decision
Strategic Judgment
Recommendation
Hypothesis
Scenario
Metric
Score
Near-miss / exception
```

For each, record whether it should remain a Working artifact, be represented through existing v1 objects/relationships, or be flagged as Yellow/Red.

Do not add a new canonical object solely to avoid a Yellow/Red result.

- [ ] **Step 4: Human gate H2 — Population / Selection confirmation**

Confirm that consequential historical inclusion, exclusion, ranking, and exception decisions remain unchanged unless the artifact itself explicitly records a historical change.

- [ ] **Step 5: Human gate H3 — Canonicalization / Judgment confirmation**

Confirm all high-consequence mappings and the distinction between:

```text
fact
inference
judgment
hypothesis
Unknown
```

- [ ] **Step 6: Record canonical adequacy matrix**

For every important semantic, record:

```text
Green / Yellow / Red
impact
acceptance decision
reason
```

---

## Task 3: Construct and Validate the Real Canonical Snapshot

**Files:**
- Create or generate the Case 001 validation snapshot using existing Step 3 APIs.
- Create or extend: `validation/research-system-v1/case-001/04-validation-evidence.md`

**Interfaces:**
- Consumes: Task 2 human-approved canonicalization and existing Step 3 public APIs.
- Produces: a real Case 001 `ResearchSnapshot` plus mechanical validation evidence.

- [ ] **Step 1: Construct legal canonical objects**

Build only approved mappings. Respect dependency order:

```text
Source
→ Evidence
→ Claim
→ Entity / Unknown / Relationship as needed
```

Use immutable v1 objects and existing `CanonicalRef` identity semantics.

- [ ] **Step 2: Establish provenance links**

For every important factual claim, preserve:

```text
Claim.evidence_ids
Evidence.source_id
Evidence.supports_claim_ids
Evidence.contradicts_claim_ids
```

Do not repair inconsistent legacy references automatically.

- [ ] **Step 3: Create the snapshot**

Use `CanonicalRegistry.snapshot(...)` and record the resulting:

```text
snapshot_id
case_id
cutoff
workflow_version
schema_version
transformation_version
members
member fingerprints
```

- [ ] **Step 4: Run existing Step 3 validation**

Run the repository's existing canonical validation path and record pass/fail plus relevant evidence. Do not create a Case 001-specific replacement validator.

- [ ] **Step 5: Validate provenance manually for high-consequence claims**

Spot-check critical claims across:

```text
support
contradiction
qualification
Unknown preservation
```

- [ ] **Step 6: Record any normalization loss**

A loss is acceptable only when explicitly documented and human-approved as non-material. Material loss becomes a gap.

---

## Task 4: Run Step 4 Evaluation on the Real Snapshot

**Files:**
- Create or generate evaluation artifacts under `validation/research-system-v1/case-001/04-validation-evidence.md`

**Interfaces:**
- Consumes: the real Case 001 snapshot and existing Step 4 evaluation APIs.
- Produces: evaluation run, results, human review record, and quality-gate decision evidence.

- [ ] **Step 1: Select existing applicable evaluation rules**

Prefer current v1 rules already implemented for:

```text
snapshot integrity
factual claim support
```

Add no new rule merely to make Case 001 appear more complete.

- [ ] **Step 2: Execute mechanical evaluation**

Record:

```text
rule id/version
run id/status
result status
failures/inconclusive results
```

- [ ] **Step 3: Inspect evaluation blind spots**

Compare mechanical results with human-observable quality issues such as:

```text
coverage
source quality
citation accuracy
reasoning quality
contradiction handling
judgment preservation
```

- [ ] **Step 4: Human gate H4 — Evaluation acceptance**

Review the mechanical results and explicitly record unresolved issues. Do not treat human review as an undocumented escape hatch.

- [ ] **Step 5: Resolve the quality gate**

Use existing `QualityGatePolicy` semantics. A non-PASS outcome must block delivery unless the existing declared human-review semantics legally resolve it.

- [ ] **Step 6: Record evaluation gaps**

Any defect detectable by a human but not representable or evaluable by the current v1 system is an Evaluation Gap candidate.

---

## Task 5: Execute Step 5 Delivery on the Real Snapshot

**Files:**
- Create: `validation/research-system-v1/case-001/05-delivery-evidence.md`
- Generate: Case 001 Dataset delivery evidence
- Generate: Case 001 Research Note delivery evidence

**Interfaces:**
- Consumes: the real Case 001 snapshot, the accepted Step 4 gate, and existing Step 5 build APIs.
- Produces: Dataset artifact, Research Note artifact, build manifest, audit manifest, and delivery inspection evidence.

- [ ] **Step 1: Define Dataset delivery spec**

Use an existing supported format and explicit versions/configuration. Do not add a renderer.

- [ ] **Step 2: Build the Dataset**

Invoke the existing snapshot-bound `build_delivery(...)` path with a PASS gate. Verify the payload contains historical snapshot state, not current Registry state.

- [ ] **Step 3: Define Research Note delivery spec**

Use the existing Markdown renderer and explicit versions/configuration.

- [ ] **Step 4: Build the Research Note**

Invoke the same snapshot-bound build path. Verify the note does not introduce unsupported research conclusions.

- [ ] **Step 5: Inspect build and audit manifests**

Confirm:

```text
snapshot identity
member fingerprints
workflow/schema/transformation versions
projection/renderer versions
configuration
assumptions
gate context
build-input digest
artifact digest
```

- [ ] **Step 6: Human gate H5 — Final delivery review**

Review semantic correctness, provenance, Unknowns, omission/compression risk, usefulness, and consistency between Dataset and Research Note.

- [ ] **Step 7: Record delivery gaps**

Distinguish a renderer limitation from a deeper canonical/evaluation/workflow limitation.

---

## Task 6: Prove Rebuild and Snapshot-Bound Reproducibility

**Files:**
- Modify: `validation/research-system-v1/case-001/05-delivery-evidence.md`
- Create: `validation/research-system-v1/case-001/06-e2e-validation-report.md`

**Interfaces:**
- Consumes: Task 5 artifacts and manifests.
- Produces: reproducibility evidence for Dataset and Research Note plus the first E2E result table.

- [ ] **Step 1: Rebuild Dataset from the same declared state**

Use the same snapshot, delivery specification, configuration, assumptions, projection version, and renderer version. Compare semantic delivery content and content digests where the renderer is byte-stable.

- [ ] **Step 2: Rebuild Research Note from the same declared state**

Apply the same comparison rule. Do not require byte equality when non-semantic serialization metadata can differ.

- [ ] **Step 3: Exercise the negative state-change proof**

Create or use a new canonical member state without altering the original snapshot. Demonstrate that:

```text
new state
→ different snapshot member fingerprint / build input
→ different semantic build identity
```

and that the old snapshot delivery does not silently change.

- [ ] **Step 4: Record reproducibility result**

Explicitly distinguish:

```text
semantic equivalence
byte-for-byte identity
```

- [ ] **Step 5: Verify no hidden current-state dependency**

Change current Registry state after snapshot creation and confirm delivery remains bound to snapshot-resolved historical state.

---

## Task 7: Produce the E2E Validation Report

**Files:**
- Create: `validation/research-system-v1/case-001/06-e2e-validation-report.md`

**Interfaces:**
- Consumes: all previous validation evidence, manifests, evaluation records, and human gates.
- Produces: the authoritative Step 6 E2E Validation Report.

- [ ] **Step 1: Write the report sections**

Use this structure:

```text
1. Executive Result
2. Case Background
3. Validation Scope
4. R0–R8 Validation
5. Canonical Model Validation
6. Provenance Validation
7. Evaluation Validation
8. Human Gate Validation
9. Reproducible Build Validation
10. Dataset Validation
11. Research Note Validation
12. Reproducibility Result
13. Observed Failures / Friction
14. Gap Classification
15. Case-specific vs System-level
16. Recommendation
17. Conclusion
```

- [ ] **Step 2: Assign dimension outcomes**

Record independently:

```text
Workflow
Canonical
Provenance
Evaluation
Delivery
Reproducibility
Human Gates
```

Use `PASS`, `PARTIAL`, or `FAIL` with evidence.

- [ ] **Step 3: Determine overall outcome**

Use exactly one:

```text
VALIDATED
PARTIALLY VALIDATED
NOT VALIDATED
```

Do not force a PASS merely because the mechanical build succeeds.

- [ ] **Step 4: Check evidence completeness**

Every material conclusion in the report must point back to one or more validation artifacts or human review records.

- [ ] **Step 5: Perform methodology consistency review**

Confirm the report does not imply Step 7 generalization or Step 8 revision was completed.

---

## Task 8: Produce the Gap Register and Recommendation

**Files:**
- Create: `validation/research-system-v1/case-001/07-gap-analysis.md`
- Create: `validation/research-system-v1/case-001/08-recommendation.md`

**Interfaces:**
- Consumes: Task 7 E2E report and all observed friction.
- Produces: classified gap register and recommendation for the next phase.

- [ ] **Step 1: Record every observed gap**

Use this schema:

```text
Gap ID
Stage
Observed Problem
Expected Behavior
Actual Behavior
Classification
Severity
Case-specific?
Reusable?
Evidence
Recommendation
Step 7/8 relevance
```

- [ ] **Step 2: Classify each gap**

Use one primary classification:

```text
Case-specific
Workflow gap
Canonical gap
Provenance gap
Evaluation gap
Build gap
Delivery gap
Human-gate gap
```

- [ ] **Step 3: Test for generality**

For every candidate system-level gap, ask:

```text
Could the same semantic problem plausibly recur in a different research domain?
Is the problem caused by the shared architecture rather than this case's historical peculiarities?
Would changing the shared system be more appropriate than handling the case locally?
```

A gap is not system-level merely because the current Case 001 mapping is inconvenient.

- [ ] **Step 4: Decide whether system change is justified**

For each gap, record exactly one:

```text
No
Maybe
Yes
```

- [ ] **Step 5: Write the recommendation**

The recommendation must choose among:

```text
Proceed to Step 7 unchanged
Proceed to Step 7 with explicitly tracked constraints
Repeat a focused part of Step 6
Defer system change until generalization evidence
```

Do not recommend Step 8 solely because a gap is uncomfortable.

---

## Task 9: Final Step 6 Review and Release Decision

**Files:**
- Review: `validation/research-system-v1/case-001/06-e2e-validation-report.md`
- Review: `validation/research-system-v1/case-001/07-gap-analysis.md`
- Review: `validation/research-system-v1/case-001/08-recommendation.md`

**Interfaces:**
- Consumes: the complete Step 6 validation package.
- Produces: final human release decision; no code change is implied.

- [ ] **Step 1: Human final review**

Confirm the report reflects what actually happened, including failures and friction. Do not rewrite gaps into successes.

- [ ] **Step 2: Check Step 6 success criteria**

Verify the seven validation dimensions in the approved spec have evidence and explicit outcomes.

- [ ] **Step 3: Check experiment integrity**

Confirm no validation step silently changed the historical Case 001 research judgment, weakened canonical invariants, bypassed evaluation gates, or introduced unvalidated shared infrastructure.

- [ ] **Step 4: Release decision**

Record one final result:

```text
Step 6 Validated
Step 6 Partially Validated
Step 6 Not Validated
```

- [ ] **Step 5: Stop boundary**

After the final release decision, stop. Any proposed shared-system correction becomes a separately approved Step 8 activity after Step 7 generalization, unless a narrowly scoped verification issue must be repaired to make the validation evidence trustworthy.

---

## Ownership Boundary

### Human

Owns:

```text
research meaning
scope
selection
canonicalization approval
major judgment
Unknown interpretation
contradiction resolution
quality acceptance
final delivery approval
system-gap classification
next-step recommendation
```

### ChatGPT

Owns assistance with:

```text
semantic mapping
historical artifact interpretation
provenance analysis
canonicalization proposals
evaluation-gap analysis
cross-artifact consistency review
gap classification
E2E report synthesis
```

ChatGPT must present consequential semantic mappings as proposals for human approval, not silently commit them as truth.

### Codex

Owns mechanical execution such as:

```text
repository inspection
approved data transformation
registry construction from approved mappings
snapshot construction
existing validator/evaluator execution
build invocation
manifest inspection
deterministic consistency checks
reproducibility checks
```

Codex must not make new consequential research judgments or silently alter historical semantics.

### Do Not Automate

Do not automate final decisions about:

```text
research scope
consequential population/selection
fact vs inference vs judgment
Unknown vs negative
major contradiction resolution
strategic recommendation
final research quality acceptance
```

---

## Verification Commands

Use the repository's existing commands as applicable; do not introduce new test infrastructure solely for Step 6.

```bash
pytest -q
python -m compileall -q src
```

For any approved mechanical validation script, also require:

```bash
git diff --check
```

The final Step 6 result is based on the evidence package and human review, not on the full-suite test count alone.
