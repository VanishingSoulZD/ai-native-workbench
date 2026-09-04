# Research System v1 — Step 6 End-to-End Validation Design

> **Status:** Approved design · Step 6 — End-to-End Validation Case  
> **Date:** 2026-09-04  
> **Repository:** `VanishingSoulZD/ai-native-workbench`  
> **Baseline:** `main@d5c9585adaba17401ae2ff7ed3276b74de9519a7`  
> **Validation case:** `cases/001-ai-coding-agent-landscape/`

## 0. Executive Summary

Step 6 is the first validation of Research System v1 against a real research case. Its purpose is not to add infrastructure or repair the Case 001 legacy pipeline. Its purpose is to determine whether the system already implemented through Steps 1–5 can carry a real research problem from definition through evidence, canonicalization, evaluation, reproducible delivery, and archival while preserving canonical authority, provenance, human judgment, and reproducibility.

The validation therefore treats Case 001 as a **Reference / Legacy Research Case** and re-uses its historical research assets as source material. The case is not mechanically migrated phase-by-phase and its Phase 8 pipeline is not reimplemented.

The validation flow is:

```text
Case 001 Historical Research
        ↓
R0–R8 Reconstruction / Mapping
        ↓
Working Research State
        ↓
Human-controlled Canonicalization
        ↓
Canonical Research State
        ↓
ResearchSnapshot
        ↓
Mechanical Evaluation
        ↓
Human Review / Quality Gate
        ↓
Step 5 Build
        ↓
Dataset + Research Note
        ↓
Rebuild / Equivalence Check
        ↓
E2E Validation Report
        ↓
Gap Analysis
        ↓
Recommendation
```

The outcome is intentionally allowed to be `VALIDATED`, `PARTIALLY VALIDATED`, or `NOT VALIDATED`. A discovered gap is not automatically a failure of the experiment; forcing the case to pass by changing system semantics during validation would invalidate the experiment.

---

# 1. Validation Objective

The primary validation question is:

> **Can Research System v1 carry one complete real research case from Define through Evaluate, Deliver, and Archive while preserving Canonical Authority, Provenance, Human Judgment, and Reproducibility?**

The validation must establish evidence for six dimensions:

1. **Workflow usability** — R0–R8 can describe the actual research lifecycle without requiring a one-file-per-stage interpretation.
2. **Canonical adequacy** — important research semantics can be represented without uncontrolled schema expansion or material semantic loss.
3. **Provenance integrity** — important factual claims retain inspectable Claim → Evidence → Source paths, including support, contradiction, and qualification where applicable.
4. **Evaluation sufficiency** — Step 4 mechanical validation, human review, and quality gates can meaningfully assess the real case.
5. **Delivery usefulness** — Step 5 can generate useful Dataset and Research Note deliveries from the same canonical snapshot.
6. **Reproducibility** — the declared snapshot and semantic transformation inputs are sufficient to rebuild equivalent deliveries without manually re-authoring research content.

---

# 2. Validation Questions

The validation must explicitly answer the following questions.

## Q1 — Workflow

Can the real Case 001 research process be reasonably located in R0–R8?

The answer must be based on semantic activity, not on file naming. Multiple historical files may belong to one stage, and one file may contain evidence relevant to more than one stage.

## Q2 — Definition

Can R0 capture the actual research problem, research unit, scope, exclusions, cutoff/snapshot definition, and success criteria without relying on hidden assumptions in historical documents?

## Q3 — Evidence

Can important historical observations be normalized into Evidence and connected to their Sources and Claims without losing material qualifiers?

## Q4 — Canonical

Can the important knowledge of Case 001 be expressed using the current v1 canonical object vocabulary:

```text
Entity
Claim
Evidence
Source
Unknown
Relationship
```

The validation must surface material `Green / Yellow / Red` cases rather than silently creating new canonical object types.

## Q5 — Judgment

Can historical research judgments, selections, recommendations, hypotheses, rankings, scenarios, and unknowns be preserved without confusing human judgment with factual claims?

Where the current implementation does not have a dedicated canonical type, the validation must record where the information belongs instead of forcing it into an inappropriate type.

## Q6 — Evaluation

Can Step 4 meaningfully detect important quality defects in the real case, and can the human review layer capture defects that mechanical evaluation cannot express?

## Q7 — Build

Can Step 5 consume a real Case 001 snapshot and build from snapshot-resolved historical state rather than from current Registry state?

## Q8 — Delivery

Are the generated Dataset and Research Note actually useful representations of the research rather than merely technically valid serializations?

## Q9 — Reproducibility

Can the same declared snapshot state and semantic build inputs produce equivalent Dataset and Research Note deliveries on rebuild?

## Q10 — System Gap

Which observed problems are case-specific and which represent reusable Research System v1 gaps that should be considered in Step 7 or Step 8?

---

# 3. Scope

## 3.1 In Scope

- Case 001 historical research assets already present in the repository.
- Mapping those assets to R0–R8.
- Mapping between Definition, Working, Canonical Knowledge, Evaluation, and Delivery roles.
- Human-controlled reconstruction of a Case 001 canonical state.
- Provenance inspection.
- ResearchSnapshot creation and validation.
- Step 4 evaluation and quality gate.
- Step 5 Dataset and Research Note delivery.
- Rebuild / equivalent-delivery validation.
- Human review records.
- E2E validation report.
- Gap classification and recommendation.

## 3.2 Out of Scope

- Re-running the entire internet research program merely for freshness.
- Reimplementing or repairing Case 001 Phase 8.
- Recomputing the historical Top 10.
- Re-ranking historical selections.
- Redesigning the v1 canonical model before evidence exists.
- Adding new infrastructure solely to support this case.
- PPT or HTML delivery implementation.
- Research agents or autonomous browsing.
- Multi-agent architecture.
- Step 7 generalization.
- Step 8 system revision.

External web research may be used only when an existing historical source is materially insufficient to validate a critical claim or provenance relationship.

---

# 4. Case 001 Reuse Strategy

Case 001 remains a Reference / Legacy Research Case.

Historical assets are reused by semantic role:

| Role | Primary historical sources |
|---|---|
| Definition | `00-research-charter.md`, `03-ranking-methodology.md` |
| Working Research | `01-candidate-universe.md`, `02-market-evidence.md`, `03-top10-selection.md`, `04-products/*`, `05-benchmarks.md`, `06-cross-product-analysis.md`, `07-decision.md` |
| Historical Canonical Reference | `08-canonical-research-model.md` |
| Historical Dataset Reference | `08-dataset/*` |
| Historical delivery/reference artifacts | `08-research-note.md`, `08-sources.md`, presentation assets where present |

The Phase 8 Canonical Research Model is treated as historical research methodology and evidence about how the old case represented knowledge. It is not treated as the schema of Research System v1.

The historical case is not converted with the rule:

```text
Phase 1 → R1
Phase 2 → R2
...
Phase 8 → R8
```

Instead, each historical artifact is inspected for the semantic research activity it contains.

---

# 5. R0–R8 Execution Model

R0–R8 are logical lifecycle stages, not mandatory file boundaries.

Each validation record for a stage should capture:

```text
stage
purpose
historical_inputs
validation_inputs
outputs
human_gate
canonical_impact
evaluation_status
notes
```

The expected semantic flow is:

```text
R0 Define
  → Charter, questions, scope, unit, cutoff, success criteria

R1 Discover
  → research population, taxonomy, source map, research plan

R2 Evidence
  → Source, Evidence, Claim candidates, provenance links

R3 Analyze
  → comparisons, patterns, relationships, analytical working artifacts

R4 Decide
  → selection decisions, strategic judgments, recommendations,
    hypotheses, unresolved unknowns

R5 Synthesize
  → canonical research state + durable research narrative

R6 Evaluate
  → mechanical validation + human review + quality gate

R7 Deliver
  → Dataset + Research Note

R8 Archive / Update
  → immutable snapshot, manifests, update/correction record
```

A stage is considered covered when its actual research activity can be explained using the lifecycle contract, even if several historical documents participate in that activity.

---

# 6. Evidence Requirements

Step 6 must retain four evidence classes.

## 6.1 Execution Evidence

Evidence that R0–R8 were actually applied to the case, including mapping records and gate records.

## 6.2 Canonical Evidence

Evidence sufficient to inspect:

```text
important Claim
  ↓
Evidence
  ↓
Source
```

and, where applicable:

```text
Evidence supports Claim
Evidence contradicts Claim
Claim qualification / uncertainty
Unknown state
```

## 6.3 Evaluation Evidence

Evidence must include:

```text
mechanical validation outcome
evaluation run
quality gate
affected rules
human review
unresolved issues
```

## 6.4 Delivery Evidence

Evidence must include enough information to connect the delivery back to:

```text
snapshot identity
snapshot member fingerprints
build-input identity
delivery specification
artifact digest
build/audit manifest
```

The evidence package should prove the chain rather than merely list that each artifact exists.

---

# 7. Canonicalization Strategy

Canonicalization is treated as a semantic transformation with human approval, not as a blind parser.

The operating sequence is:

```text
Historical Artifact
      ↓
Candidate Canonical Record
      ↓
Semantic Review
      ↓
Human Confirmation
      ↓
Canonical Registry
```

The candidate record should explain:

```text
historical source
proposed object type
proposed canonical identity
semantic interpretation
provenance
qualification
uncertainty
reason for mapping
```

Final approval is required whenever the mapping changes what the system treats as known, asserted, inferred, unknown, or decided.

---

# 8. Canonical Adequacy Assessment

For each important research semantic, the validation records:

| Status | Meaning |
|---|---|
| Green | Naturally represented by existing v1 objects and relationships |
| Yellow | Representable, but with explicit friction, qualification, or semantic loss requiring human acceptance |
| Red | Not responsibly representable without inventing a new semantic or misusing an existing one |

The following are specifically examined without assuming they require new canonical objects:

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

A Red result becomes a system-level gap only if the same semantic problem is plausibly reusable across research cases. A one-off Case 001 representation problem remains case-specific until generalization evidence exists.

---

# 9. Provenance Validation

The validation must verify that important externally verifiable statements can be traced through the canonical provenance graph.

At minimum:

```text
Claim.evidence_ids
Evidence.source_id
Evidence.supports_claim_ids
Evidence.contradicts_claim_ids
```

must resolve against the snapshot state used for validation.

The validation must explicitly inspect:

1. supported claims;
2. contradicted claims;
3. unresolved or conflicting evidence;
4. qualified quantitative statements;
5. unknowns that must not be converted into negative assertions.

No automatic provenance repair is permitted merely to make the case pass.

---

# 10. Evaluation Strategy

Evaluation has three layers.

## 10.1 Mechanical Evaluation

Reuse existing Step 3 and Step 4 validators rather than implementing parallel validation logic.

The validation should cover, as applicable:

```text
schema validity
reference integrity
provenance integrity
Unknown preservation
snapshot recoverability
evaluation rule execution
quality gate behavior
build preconditions
projection / renderer correctness
manifest consistency
content digest consistency
```

## 10.2 Human Evaluation

The human review must inspect at least:

```text
scope correctness
population / selection correctness
canonicalization correctness
claim qualification
contradiction handling
judgment preservation
final note usefulness
omission / compression distortion
```

## 10.3 E2E Evaluation

The final evaluation asks whether the complete chain functions as one coherent research process:

```text
Define
→ Discover
→ Evidence
→ Analyze
→ Decide
→ Synthesize
→ Evaluate
→ Deliver
→ Archive
```

A technically successful build with materially incorrect research meaning is not considered E2E success.

---

# 11. Human Gates

Step 6 uses the project-level human gate philosophy and makes Canonicalization Confirmation operationally explicit.

## H1 — Research Scope Gate

Human confirms research question, boundaries, unit, exclusions, cutoff/snapshot definition, and success criteria.

## H2 — Population / Selection Gate

Human confirms consequential inclusion, exclusion, ranking, and exception decisions remain faithful to the historical research state.

## H3 — Canonicalization / Judgment Gate

Human confirms high-consequence semantic mappings and distinguishes fact, inference, judgment, hypothesis, and Unknown.

## H4 — Evaluation Gate

Human reviews mechanical results and unresolved quality issues before accepting the case as delivery-eligible.

## H5 — Final Delivery Gate

Human reviews factual correctness, provenance, uncertainty representation, usefulness, and compression/omission risks in the Dataset and Research Note.

Historical corrections or reinterpretations require explicit versioned action rather than silent mutation.

---

# 12. Delivery Strategy

Step 6 uses only the two delivery forms already implemented in Step 5:

```text
Dataset
Research Note
```

The purpose is to validate semantic projection, not to expand the renderer surface.

## 12.1 Dataset

The Dataset is successful only if it preserves the useful machine-oriented subset of the canonical state, including stable identifiers, relevant semantic fields, provenance references, and explicit Unknown states where applicable.

Technical serialization success alone is insufficient.

## 12.2 Research Note

The Research Note is successful only if a reviewer who did not perform the case reconstruction can understand the research context, key findings, evidence-backed claims, material Unknowns, limitations, and provenance from the output.

The Note Renderer must not independently introduce new research conclusions.

---

# 13. Reproducibility Validation

The primary proof is:

```text
same snapshot
+ same workflow/schema/transformation versions
+ same projection/renderer versions
+ same configuration
+ same assumptions
+ same delivery specification
        ↓
rebuild
        ↓
equivalent semantic delivery
```

The negative proof is:

```text
snapshot member state changes
        ↓
build-input identity changes
        ↓
old delivery must not silently represent new state
```

The validation must distinguish:

```text
semantic equivalence
```

from:

```text
byte-for-byte identity
```

The latter is not required system-wide unless a particular renderer can provide it cheaply and reliably.

---

# 14. Success Criteria

Step 6 is considered `VALIDATED` only when all of the following hold:

1. R0–R8 can coherently describe the reconstructed case.
2. Core research semantics are representable without unaccepted material semantic distortion.
3. Important factual claims retain usable Claim → Evidence → Source provenance.
4. Mechanical evaluation passes its mandatory checks and human gates are explicitly recorded.
5. Dataset and Research Note are both generated from the same canonical snapshot.
6. The same declared state and semantic build inputs can rebuild equivalent delivery.
7. No build, projection, renderer, or evaluation operation silently mutates canonical authority.
8. Every discovered gap is classified and supported by evidence.

A practical adequacy heuristic may be used for reporting core semantics coverage, but it must never substitute for inspection of high-consequence semantics. A numerical percentage is a reporting aid, not the definition of correctness.

---

# 15. Failure Criteria

The result is `PARTIALLY VALIDATED` or `NOT VALIDATED` when any material condition below occurs:

- a lifecycle stage cannot be meaningfully represented;
- critical research meaning requires undocumented reinterpretation;
- provenance cannot be reconstructed for important factual claims;
- mechanical evaluation passes while human review reveals material defects that the system cannot express;
- delivery output is technically valid but semantically unusable;
- the build cannot operate from a real snapshot without bypassing the declared contracts;
- reproducibility depends on manually re-authoring research content;
- the only practical way to pass the case is to silently alter historical judgments or canonical semantics.

A failure caused by a Case 001-specific peculiarity is not, by itself, evidence that the system should be changed.

---

# 16. Gap Classification

Every observed problem must be entered into the Gap Register with:

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
Step 7 / Step 8 relevance
Change justified? (No / Maybe / Yes)
```

Allowed classifications are:

```text
Case-specific
Workflow gap
Canonical model gap
Provenance gap
Evaluation gap
Build gap
Delivery gap
Human-gate gap
```

A change is `Yes` only when the observed issue is both systemic and reusable enough to justify altering a shared contract.

---

# 17. Expected Validation Package

The validation package should remain separate from Case 001 legacy research assets.

Recommended structure:

```text
validation/
  research-system-v1/
    case-001/
      00-validation-protocol.md
      01-case-mapping.md
      02-execution-record.md
      03-canonicalization-record.md
      04-validation-evidence.md
      05-delivery-evidence.md
      06-e2e-validation-report.md
      07-gap-analysis.md
      08-recommendation.md
```

The exact number of files may be reduced if a smaller package preserves the same semantic boundaries. No validation file is required merely because the template names one.

The central artifact is:

```text
06-e2e-validation-report.md
```

It must contain:

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
13. Observed Friction / Failures
14. Gap Classification
15. Case-specific vs System-level Analysis
16. Recommendation
17. Conclusion
```

The conclusion must report per-dimension status:

```text
Workflow
Canonical
Provenance
Evaluation
Delivery
Reproducibility
Human Gates

Overall:
VALIDATED / PARTIALLY VALIDATED / NOT VALIDATED
```

---

# 18. Human / ChatGPT / Codex Responsibility Boundary

## 18.1 Human — Research Authority

The human researcher owns:

```text
research scope
research purpose
selection decisions
canonicalization approval
major claim interpretation
judgment
ranking / decision fidelity
Unknown confirmation
quality acceptance
final delivery approval
system-gap acceptance
```

Any operation that changes what the research treats as known, unknown, inferred, or decided requires human authority.

## 18.2 ChatGPT — Semantic and Methodology Copilot

ChatGPT may:

```text
interpret historical research assets
map research activities to R0–R8
propose canonical mappings
identify semantic mismatches
analyze provenance
identify contradictions
design evaluation checks
classify gaps
draft the E2E Validation Report
```

ChatGPT must not silently make final consequential research decisions on behalf of the researcher.

## 18.3 Codex — Mechanical Repository Executor

Codex may:

```text
read and inventory repository files
construct approved records
instantiate registry state
run existing validators
create snapshots
execute evaluation/build pipelines
generate datasets and notes
compare rebuilds
run tests and mechanical consistency checks
produce diffs and manifests
```

Codex must not independently decide major semantic mappings, rankings, Unknown semantics, historical judgment changes, or strategic conclusions.

## 18.4 Not to Automate in Step 6

The following remain deliberately human-controlled:

```text
research scope
consequential selection
final canonicalization of ambiguous semantics
major contradiction resolution
final strategic judgment
final delivery acceptance
```

Automation is not considered successful when it removes required human judgment without evidence that the judgment can be safely delegated.

---

# 19. Execution Sequence

The recommended execution sequence is:

```text
Stage 0 — Validation Protocol
        ↓
Stage 1 — Case 001 Asset Inventory
        ↓
Stage 2 — Historical Asset → R0–R8 Mapping
        ↓
Stage 3 — Definition / Working State Reconstruction
        ↓
Stage 4 — Candidate Canonicalization
        ↓
Stage 5 — Human Canonicalization / Judgment Confirmation
        ↓
Stage 6 — ResearchSnapshot Formation
        ↓
Stage 7 — Mechanical Evaluation
        ↓
Stage 8 — Human Evaluation
        ↓
Stage 9 — Quality Gate
        ↓
Stage 10 — Dataset + Research Note Build
        ↓
Stage 11 — Rebuild / Reproducibility Check
        ↓
Stage 12 — E2E Validation Report
        ↓
Stage 13 — Gap Analysis
        ↓
Stage 14 — Recommendation
```

Stages 4–5 are explicitly human-controlled semantic work. Stages 7, 9, 10, and 11 should maximize reuse of existing Step 3–5 mechanics.

---

# 20. Engineering Constraint

Step 6 does not authorize system changes by default.

The decision rule is:

```text
Observe
  ↓
Classify
  ↓
Assess repeatability / reuse
  ↓
Record evidence
  ↓
Only then consider system change
```

Do not add:

```text
database
object storage
artifact registry
message queue
distributed execution
multi-agent architecture
plugin marketplace
universal renderer registry
```

unless the real Case demonstrates that the existing architecture cannot complete the validation without such infrastructure.

A Case-specific workaround must remain Case-specific unless repeated evidence later justifies promotion to a shared capability.

---

# 21. Step 7 / Step 8 Boundary

Step 6 ends at evidence-backed recommendation.

It does not begin:

```text
Step 7 — Generalization to a Second Research Problem
```

and it does not perform:

```text
Step 8 — System Revision
```

The intended sequence remains:

```text
Step 6
Case 001 E2E Validation
        ↓
Gap Analysis
        ↓
Step 7
Second Research Problem
        ↓
Generalization Evidence
        ↓
Step 8
System Revision
```

A Step 6 gap may be documented as a future revision candidate without changing the system during the validation experiment.

---

# 22. Definition of Success

Step 6 succeeds when it produces credible evidence for the system-level statement:

> **Research System v1 can, or cannot, carry a real research case from Define through Evaluate, Deliver, and Archive without losing canonical authority, provenance, human judgment, or reproducibility.**

The value of Step 6 is therefore the evidence about the system boundary, not the amount of code added to the repository.
