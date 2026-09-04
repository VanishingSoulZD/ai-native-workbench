# Research System v1 — Evaluation Core Design

> **Status:** Approved design candidate · Step 4 — Evaluation
>
> **Date:** 2026-09-04
>
> **Repository:** `VanishingSoulZD/ai-native-workbench`
>
> **Depends on:**
> - `docs/superpowers/specs/2026-09-03-research-system-contract-design.md`
> - `docs/methodology/research-system-v1.md`
> - `docs/superpowers/specs/2026-09-03-research-system-v1-canonical-knowledge-provenance-design.md`
> - Research System v1 Step 2 Workflow Core
>
> **Scope:** Define the minimum reusable Evaluation Core for Research System v1 without introducing benchmark infrastructure, LLM judges, persistence infrastructure, autonomous evaluation, or changes to the Step 3 canonical authority model.

---

## 0. Executive Summary

Step 4 establishes the reusable **Evaluation Core** for Research System v1.

Its purpose is not to create a generic scoring framework. Its purpose is to establish a small, explicit layer that can determine whether a research state or delivery has sufficient quality to proceed, while preserving the distinction between:

```text
Validation
Evaluation
Metric
Score
Judgment
Quality Gate
Human Review
```

The central architectural rule is:

> **Evaluation assesses canonical research state; it does not become the authority for canonical research knowledge.**

The resulting flow is:

```text
Research Snapshot / Delivery
        ↓
Evaluation Run
        ↓
Versioned Evaluation Rules
        ↓
Evaluation Results
        ↓
Quality Gate
        ↓
PASS / REVIEW / FAIL
        ↓
Human Review when required
```

Step 4 deliberately preserves the Step 3 boundary:

```text
Step 3
Canonical Knowledge + Provenance
        ↓
provides semantic research state

Step 4
Evaluation
        ↓
assesses the quality of that state
```

Evaluation objects are **evaluation-layer artifacts**, not Step 3 canonical research objects.

The first implementation is intentionally small and should remain in-memory and standard-library based, consistent with the existing Workflow Core and Canonical Registry approach.

---

# 1. Design Principles

## 1.1 Evaluation before Automation

A research capability must be evaluable before additional automation is introduced. A reduction in human effort is not sufficient evidence of successful automation if quality and failure modes are unknown.

## 1.2 Canonical Knowledge remains the semantic authority

Canonical objects remain the authoritative representation of what the research knows.

Evaluation may reference:

```text
CanonicalRef
ResearchSnapshot
Evidence
Source
Delivery Artifact
```

but does not duplicate or replace those objects.

Evaluation MUST NOT silently mutate canonical objects.

## 1.3 Evaluation is distinct from Validation

Validation asks:

> Does the state satisfy structural and invariant requirements?

Evaluation asks:

> Does the state satisfy a declared quality criterion?

Existing Step 3 validation remains the authority for canonical structural integrity. Step 4 may consume validation outcomes but MUST NOT duplicate the same validation authority.

## 1.4 Evaluation is contextual

An evaluation result only has meaning within an explicit:

```text
Target
Rule
Rule Version
Evaluation Run
Evaluation Context
```

The same canonical state may legitimately receive different evaluation results under different rules or evaluation protocols.

## 1.5 Human authority remains explicit

Machine evaluation may determine purely mechanical criteria. It may assist with criteria requiring interpretation. Criteria that require human judgment remain explicitly human-required.

Human review is not an undocumented override mechanism. It is an explicit part of the evaluation record when a rule requires it.

## 1.6 Reproducibility without false determinism

Evaluation history must be explainable from the recorded target, rule versions, protocol/version context and relevant configuration. The system does not require byte-for-byte deterministic output from future model-assisted evaluators.

## 1.7 Minimal sufficient engineering

Step 4 introduces only the abstractions required to establish a reusable evaluation contract. It does not introduce:

- database persistence;
- benchmark orchestration;
- vector search;
- LLM judge infrastructure;
- external evaluation SaaS;
- statistical experiment platforms;
- distributed evaluation workers;
- autonomous browsing;
- agent runtime;
- generic governance platform.

---

# 2. Problem Definition

Research System v1 currently has a canonical knowledge layer capable of representing and validating:

```text
Entity
Claim
Evidence
Source
Unknown
Relationship
```

and a historical snapshot mechanism capable of reconstructing exact canonical states from fingerprints.

That layer can answer questions such as:

- Does a referenced Evidence object exist?
- Does an Evidence object reference a Source?
- Does a Claim's declared provenance resolve?
- Can a historical snapshot member be recovered?

These are validation questions.

Step 4 must additionally answer questions such as:

- Is evidence coverage sufficient for the research questions?
- Are factual claims adequately supported?
- Are citations accurate?
- Is source quality acceptable?
- Are contradictions explicitly handled?
- Is factual accuracy adequate?
- Is reasoning quality acceptable?
- Is the final delivered answer useful and appropriately qualified?
- Which findings can be decided mechanically?
- Which require human review?
- Does the research satisfy a declared quality gate?

Therefore the core Step 4 problem is:

> **Given a stable research or delivery target, define and execute reusable quality criteria, preserve the resulting findings as immutable evaluation history, incorporate required human review explicitly, and determine process eligibility through a simple quality gate.**

---

# 3. Non-Goals

Step 4 does not attempt to solve:

- universal research quality measurement;
- objective determination of truth for arbitrary claims;
- automatic resolution of contradictions;
- autonomous final judgment;
- automatic final decision making;
- universal benchmark support;
- general LLM evaluation platforms;
- automatic evaluator discovery;
- automatic weighting of heterogeneous quality dimensions;
- one-number research quality scores;
- database-backed evaluation history;
- replacement of Step 3 provenance or validation;
- replacement of human judgment;
- Case 001 migration or retrofitting.

In particular, Step 4 MUST NOT introduce a weighted aggregate score merely to simplify the Quality Gate.

---

# 4. Evaluation versus Validation

The two layers have distinct authorities.

## 4.1 Validation

Validation is concerned with invariants.

Examples:

```text
CanonicalRef syntax
required canonical fields
reference resolution
Claim → Evidence integrity
Evidence → Source integrity
reverse provenance consistency
fingerprint correctness
snapshot recoverability
```

Step 3 owns this behavior.

## 4.2 Evaluation

Evaluation is concerned with quality relative to declared criteria.

Examples:

```text
support coverage
citation accuracy
source quality
factual accuracy
contradiction handling
reasoning quality
usefulness
```

A validation failure may be consumed by an evaluation rule, but Step 4 must not silently redefine the validation invariant.

## 4.3 Evaluation execution failure

An evaluator implementation failure is not a quality failure.

For example:

```text
Evaluator crashed
```

must result in an Evaluation Run failure, not:

```text
Research quality = FAIL
```

This distinction is required for trustworthy auditability.

---

# 5. Evaluation Scope

Step 4 supports three conceptual evaluation scopes:

```text
Object Scope
Snapshot Scope
Delivery Scope
```

## 5.1 Object Scope

Evaluates an individual canonical object or closely related set of canonical objects.

Examples:

```text
Claim
Evidence
Source
Relationship
Unknown
```

Use cases include:

- factual Claim support;
- source metadata quality;
- citation binding;
- relationship evidence coverage.

## 5.2 Snapshot Scope

Evaluates the research state represented by a `ResearchSnapshot`.

Examples:

```text
coverage
cross-object consistency
contradiction handling
research completeness
factual quality
```

The Snapshot is the principal stable target for Step 4 research-level evaluation because it fixes the canonical state being assessed.

## 5.3 Delivery Scope

Evaluates a delivery projection derived from canonical knowledge.

Examples:

```text
citation correctness
factual fidelity
compression distortion
uncertainty preservation
audience usefulness
```

A valid canonical snapshot does not imply that every delivery projection is valid. Delivery evaluation is therefore allowed to exist independently from canonical evaluation.

## 5.4 Shared Evaluation Contract

The three scopes MUST use the same Evaluation Core model rather than separate evaluation frameworks.

Scope is part of the target/rule context rather than a reason to create:

```text
ObjectEvaluator
SnapshotEvaluator
DeliveryEvaluator
```

as separate architectural systems.

---

# 6. Core Architecture

The Evaluation Core consists of five concepts:

```text
EvaluationRule
EvaluationRun
EvaluationResult
QualityGate
HumanReviewRecord
```

The relationship is:

```text
ResearchSnapshot / Delivery
            ↓
      EvaluationRun
            ↓
      EvaluationRule(s)
            ↓
    EvaluationResult(s)
            ↓
      QualityGate Policy
            ↓
      PASS / REVIEW / FAIL
            ↓
  HumanReviewRecord when required
```

The concepts have different authority:

| Concept | Authority |
|---|---|
| Canonical Object | What the research knows |
| EvaluationRule | How quality is assessed |
| EvaluationRun | One concrete evaluation execution/context |
| EvaluationResult | What the evaluation found |
| QualityGate | Whether the target satisfies process requirements |
| HumanReviewRecord | Explicit human assessment required by the evaluation process |

---

# 7. EvaluationRule

## 7.1 Definition

`EvaluationRule` describes a reusable quality criterion.

It answers:

> What should be evaluated, at what scope, under what evaluation mode and severity, using which versioned rule definition?

## 7.2 Conceptual fields

```yaml
rule_id
name
description
target_scope
mode
severity
version
```

Where:

```text
target_scope:
  object | snapshot | delivery

mode:
  mechanical | human_assisted | human_required

severity:
  informational | warning | critical
```

The exact severity taxonomy is implementation-level and must remain minimal.

## 7.3 Rule boundary

An EvaluationRule MUST define evaluation semantics, not execution technology.

A Rule MUST NOT expose or require:

```text
prompt
model
agent
runtime
specific tool implementation
```

A rule may be executed by Python code, an external tool, a human review form, or a future model-assisted mechanism without changing the rule's semantic identity.

## 7.4 Rule versioning

Material semantic changes require a new Rule version.

A historical EvaluationRun MUST identify the Rule version used for that run.

---

# 8. EvaluationRun

## 8.1 Definition

`EvaluationRun` represents one concrete execution of one evaluation configuration against one stable target.

## 8.2 Target requirement

Every EvaluationRun MUST identify an explicit immutable evaluation target.

For research-level evaluation the default target is:

```text
ResearchSnapshot
```

A delivery evaluation may instead target a specific delivery artifact/version.

An EvaluationRun MUST NOT rely on an implicit "current Registry" target.

## 8.3 Conceptual fields

```yaml
run_id
target_type
target_id
evaluation_rule_versions
evaluation_protocol_version
configuration
created_at
status
```

The first implementation does not require a separate `EvaluationTarget` class.

## 8.4 Lifecycle

The Run lifecycle is intentionally small:

```text
created
running
completed
failed
```

No larger state machine is required for v1.

## 8.5 Run semantics

A completed Run is historical evaluation evidence.

It MUST NOT be mutated in place to reflect later rule changes, target changes, or human review outcomes.

A new evaluation produces a new Run.

---

# 9. EvaluationResult

## 9.1 Definition

`EvaluationResult` represents what one EvaluationRule found for one target during one EvaluationRun.

It is an assessment record, not a canonical knowledge object.

## 9.2 Conceptual fields

```yaml
result_id
run_id
rule_id
target
status
severity?
finding
subject_refs?
value?
notes?
```

## 9.3 Status

The Result status vocabulary is:

```text
pass
fail
inconclusive
not_applicable
```

`review` is not a Result status. Review is a Quality Gate outcome indicating that human action is required before process eligibility can be determined.

## 9.4 Severity

Severity describes the importance of a finding, not the Gate outcome.

The Gate MUST NOT infer its outcome solely from a generic severity value. Gate behavior is defined by explicit policy.

## 9.5 Finding

`finding` is a concise human-readable observation describing what the evaluator found.

Example:

```text
2 factual claims have insufficient supporting evidence.
```

The first implementation does not introduce a separate EvaluationFinding semantic object.

## 9.6 Subject references

`subject_refs` may identify the canonical objects or delivery elements affected by the finding.

Canonical object references MUST use existing `CanonicalRef` values from Step 3.

Evaluation MUST NOT create a second reference namespace for canonical research objects.

## 9.7 Optional value

`value` is optional and may carry a quantitative result when a particular rule produces one.

For example:

```text
coverage = 0.82
```

The existence of a value does not create a separate `Score` object and does not imply the existence of an independent `Metric` abstraction.

## 9.8 Deliberately excluded fields

`EvaluationResult` does not include, by default:

```text
confidence
chain_of_thought
reasoning_trace
embedded canonical object
embedded evidence copy
embedded source copy
```

If an evaluator needs supporting material, it should reference existing canonical or evaluation records rather than duplicate them.

---

# 10. Metric and Score Decision

Step 4 does not create independent core objects named:

```text
EvaluationMetric
Score
```

in the first implementation.

A rule may produce an optional numeric `value`, but that value remains contextual to:

```text
EvaluationRule
EvaluationRule version
EvaluationRun
EvaluationResult
```

The abstraction threshold for introducing independent Metric/Score objects is deliberately left to later evidence. Independent metric identity becomes justified only when the system demonstrates repeated need for capabilities such as:

```text
standardized scale
unit semantics
cross-run aggregation
comparability across cases
metric reuse independent of one evaluation rule
```

Until that need is demonstrated, a separate Metric/Score model would be premature abstraction.

A general weighted aggregate research quality score is explicitly out of scope for Step 4 v1.

---

# 11. Mechanical, Human-Assisted, and Human-Required Evaluation

Evaluation rules are divided into three modes.

## 11.1 Mechanical

The system can determine the result without human judgment.

Examples:

```text
canonical integrity
factual Claim has required Evidence
Evidence references Source
snapshot recoverability
required structure present
```

Where appropriate, mechanical rules should reuse Step 3 capabilities rather than duplicate them.

## 11.2 Human-Assisted

The system can gather evidence or propose an assessment, but a human must verify the result.

Examples:

```text
citation accuracy
source quality
some factual accuracy checks
some contradiction handling
```

The system may generate findings, but it must not silently convert those findings into authoritative human acceptance.

## 11.3 Human-Required

The criterion requires explicit human judgment.

Examples:

```text
reasoning quality
final answer usefulness
consequential strategic judgment
```

A Human-Required rule cannot reach process eligibility merely because an automated evaluator produced a plausible answer.

---

# 12. QualityGate

## 12.1 Definition

A `QualityGate` applies a declared policy to Evaluation Results and determines whether the target satisfies the process requirements for the next stage.

The Gate is a policy layer, not another evaluator.

## 12.2 Outcome vocabulary

The only v1 Gate outcomes are:

```text
PASS
REVIEW
FAIL
```

### PASS

All mandatory criteria are satisfied, including required human reviews.

### FAIL

At least one mandatory criterion has an explicit failure that blocks progression.

### REVIEW

No blocking failure has been established, but required human assessment or another declared review condition remains unresolved.

`REVIEW` therefore means:

> The system cannot yet grant process eligibility within its current authority boundary.

It does not itself mean that the research is poor.

## 12.3 Gate policy

A Gate policy may specify conditions such as:

```text
all critical mechanical rules must pass
all mandatory human-required rules must have accepted review
specific rule failures block progression
inconclusive mandatory results require review
```

The policy MUST be explicit.

## 12.4 Gate does not re-evaluate canonical state

A QualityGate MUST consume evaluation outcomes rather than independently re-running canonical integrity or research-quality logic.

This preserves separation between:

```text
Rule
Result
Gate
```

---

# 13. HumanReviewRecord

## 13.1 Definition

`HumanReviewRecord` records an explicit human action required by an evaluation process.

It is an evaluation/governance artifact, not a canonical research object.

## 13.2 Conceptual fields

```yaml
review_id
target
evaluation_run_id
reviewer
decision
reviewed_at
comment
```

The initial decision vocabulary is:

```text
accepted
rejected
needs_revision
```

## 13.3 Review semantics

Human review does not mutate the historical `EvaluationResult`.

Instead:

```text
EvaluationResult
    ↓
HumanReviewRecord
    ↓
QualityGate determination
```

The original machine or evaluator assessment remains preserved.

## 13.4 Human review is not an override channel

The system MUST NOT treat human review as an undocumented escape hatch of the form:

```text
FAIL → click override → PASS
```

Human review must correspond to a declared evaluation requirement or review path.

---

# 14. Evaluation Flow

The normal research-level flow is:

```text
ResearchSnapshot
        ↓
EvaluationRun
        ↓
EvaluationRule(s)
        ↓
EvaluationResult(s)
        ↓
QualityGate
        ↓
┌───────────────┬───────────────┬───────────────┐
│     PASS      │    REVIEW     │      FAIL     │
└───────────────┴───────────────┴───────────────┘
                       │
                       ▼
             HumanReviewRecord
                       │
                       ▼
                Gate determination
```

For a typical run:

```text
Rule A → PASS
Rule B → PASS
Rule C → INCONCLUSIVE
Rule D → PASS
```

may produce:

```text
Gate → REVIEW
```

After the required human review is explicitly recorded:

```text
HumanReviewRecord → accepted
```

and the same declared Gate policy may determine:

```text
Gate → PASS
```

The historical Result remains unchanged.

---

# 15. Example Evaluation Rule Set

A minimal research-level case may declare:

```text
canonical_integrity
    scope: snapshot
    mode: mechanical
    mandatory: true

factual_claim_support
    scope: snapshot
    mode: mechanical
    mandatory: true

citation_accuracy
    scope: snapshot or delivery
    mode: human_assisted
    mandatory: true

source_quality
    scope: snapshot
    mode: human_assisted
    mandatory: true

contradiction_handling
    scope: snapshot
    mode: human_required
    mandatory: true

reasoning_quality
    scope: snapshot or delivery
    mode: human_required
    mandatory: true

final_answer_usefulness
    scope: delivery
    mode: human_required
    mandatory: true
```

These names are illustrative rule identifiers rather than a frozen universal taxonomy. A concrete case may choose a smaller or different set while remaining compatible with the Evaluation Core.

---

# 16. Step 3 Integration Boundary

Step 4 consumes Step 3 through stable public semantics.

## 16.1 Canonical validation

A mechanical integrity evaluation may invoke the existing canonical validation capability.

Conceptually:

```text
CanonicalRegistry.validate()
        ↓
validation outcome
        ↓
EvaluationResult
```

Step 4 MUST NOT reimplement:

```text
CanonicalRef validation
fingerprint validation
Claim/Evidence/Source provenance validation
historical state validation
snapshot recoverability
```

## 16.2 Canonical references

Evaluation Results may point to canonical objects with `CanonicalRef`.

No parallel evaluation-specific canonical identity scheme is introduced.

## 16.3 No canonical mutation

Evaluation MUST NOT:

```text
change Claim status
change Claim confidence
rewrite Evidence
replace Source metadata
rewrite Snapshot membership
```

when merely recording evaluation findings.

Any correction belongs to a separately authorized research action and follows the existing versioned snapshot semantics.

---

# 17. Immutability and Historical Integrity

Step 4 follows the same historical philosophy established by Step 3.

## 17.1 Rule immutability

A materially changed EvaluationRule receives a new version.

## 17.2 Run immutability

A completed EvaluationRun is immutable.

## 17.3 Result immutability

An EvaluationResult is immutable once recorded as part of a completed run.

## 17.4 Human review immutability

A completed HumanReviewRecord is historical evidence of a human action and is not silently rewritten.

## 17.5 New evaluation instead of mutation

If a rule, protocol, target, or configuration changes materially:

```text
New context
    ↓
New EvaluationRun
    ↓
New EvaluationResult(s)
```

The prior evaluation remains recoverable.

---

# 18. Reproducibility

Evaluation reproducibility means that a historical evaluation can be understood and, where the execution mechanism permits, rerun from its declared context.

A completed EvaluationRun MUST identify at minimum:

```text
stable target
rule identity and version
protocol/version context
relevant configuration
run identity/time
```

For a Snapshot target, historical reproducibility is grounded in Step 3's snapshot semantics:

```text
EvaluationRun
    ↓
ResearchSnapshot
    ↓
CanonicalRef → fingerprint
```

This prevents later Registry changes from changing what a historical evaluation meant.

The system does not promise identical results from future non-deterministic model-assisted evaluators.

---

# 19. Error Model

Step 4 uses a small error hierarchy:

```text
EvaluationError
├── EvaluationValidationError
├── EvaluationExecutionError
└── EvaluationResolutionError
```

## 19.1 EvaluationValidationError

Raised when a Rule, Run, Result, Gate policy, or HumanReviewRecord violates its own declared structural contract.

## 19.2 EvaluationExecutionError

Raised when an evaluation mechanism fails to execute correctly.

An execution failure does not become an EvaluationResult with `fail` status.

## 19.3 EvaluationResolutionError

Raised when a required target, evaluation context, canonical reference, or related historical record cannot be resolved.

No evaluation-related invalid state may be silently accepted.

---

# 20. Mechanical versus Human Authority Matrix

| Dimension | Mechanical | Human-Assisted | Human-Required |
|---|---:|---:|---:|
| Canonical integrity | ✓ | | |
| Snapshot recoverability | ✓ | | |
| Required factual Claim provenance | ✓ | | |
| Coverage counting | ✓ | ✓ | |
| Citation accuracy | | ✓ | |
| Source quality | | ✓ | |
| Contradiction handling | | ✓ | ✓ |
| Factual accuracy | | ✓ | ✓ |
| Reasoning quality | | | ✓ |
| Final Answer Usefulness | | | ✓ |

This table is a default architectural classification, not a claim that every future case will use exactly the same allocation.

A concrete Workflow/Case may strengthen a human requirement but must not silently remove a human requirement established as mandatory by its declared evaluation policy.

---

# 21. Quality Gate Policy Principles

Quality Gates must remain declarative and explainable.

The first implementation should support policy patterns such as:

```text
Rule X is mandatory.
Rule Y is mandatory and must be PASS.
Rule Z is human-required and must have an accepted review.
Any critical FAIL blocks progression.
Any unresolved mandatory INCONCLUSIVE result requires REVIEW.
```

The implementation MUST NOT require:

```text
weighted averages
statistical optimization
machine-learned gate policies
LLM-generated gate decisions
complex state machines
```

A Gate is a process eligibility mechanism, not a truth oracle.

---

# 22. Relationship to Workflow Core

Step 2 and Step 4 remain separate responsibilities:

```text
Workflow Core
    = execute declared workflow steps

Evaluation Core
    = assess declared quality criteria
```

The existing `WorkflowRunner` remains responsible for execution semantics. It does not become an Evaluation orchestrator.

A future workflow may include an evaluation step whose executor invokes the Evaluation Core, but the public WorkflowStep contract does not need to become evaluator-specific.

Similarly, a Gate may eventually influence workflow progression, but that integration is a later workflow/build concern rather than a reason to couple the current Runner to the Evaluation Core.

---

# 23. Evaluation Artifacts versus Canonical Knowledge

Evaluation outputs belong to the existing `evaluation` artifact class defined by the system methodology.

Conceptually:

```text
Canonical Knowledge
    ↓
ResearchSnapshot
    ↓
Evaluation Run
    ↓
Evaluation Results
    ↓
Quality Gate
    ↓
Evaluation Artifact
```

Evaluation artifacts are durable and auditable, but they are not semantic authority for Claims, Evidence, Sources, Entities, Relationships, or future reasoning objects.

This preserves the existing authority rule:

> **Artifacts carry research work; canonical objects carry semantic authority.**

---

# 24. Testing Strategy

Step 4 testing must verify both the Evaluation Core contract and its integration with Step 3.

## 24.1 Unit tests

Test:

- Rule validation;
- Rule version semantics;
- Run validation;
- target declaration;
- Result status semantics;
- Result value optionality;
- QualityGate policy behavior;
- HumanReviewRecord validation;
- immutability expectations.

## 24.2 Mechanical rule tests

Test representative rules such as:

```text
canonical_integrity
factual_claim_support
snapshot_recoverability
```

These tests should demonstrate reuse of Step 3 capabilities rather than reimplementing them.

## 24.3 Integration tests

At minimum verify:

```text
CanonicalRegistry
      ↓
ResearchSnapshot
      ↓
EvaluationRun
      ↓
EvaluationResult(s)
      ↓
QualityGate
```

Test:

- successful mechanical evaluation;
- explicit evaluation failure;
- evaluator execution failure;
- missing target resolution;
- historical snapshot evaluation after Registry mutation;
- human-required result leading to REVIEW;
- accepted HumanReviewRecord enabling PASS under policy;
- failed mandatory rule leading to FAIL.

## 24.4 Synthetic end-to-end test

A small synthetic research case should demonstrate:

```text
canonical research state
        ↓
snapshot
        ↓
evaluation run
        ↓
mechanical results
        ↓
human-required result
        ↓
human review
        ↓
quality gate
```

The synthetic case MUST remain independent of Case 001 legacy artifacts.

## 24.5 Explicit non-requirements for tests

Step 4 tests do not need to introduce:

```text
OpenCompass
MT-Bench
LLM Judge benchmarks
external evaluation SaaS
large statistical datasets
real production research corpus
```

---

# 25. Acceptance Criteria

Step 4 is considered architecturally complete when the implementation can demonstrate all of the following:

1. A stable Snapshot or Delivery target can be evaluated explicitly.
2. Reusable versioned Evaluation Rules can be declared.
3. Mechanical evaluation can execute through a stable boundary.
4. Evaluation Results can represent `pass`, `fail`, `inconclusive`, and `not_applicable`.
5. Evaluation Results can point to affected canonical objects using existing `CanonicalRef` values.
6. Optional numeric values can be preserved without introducing Metric/Score objects.
7. Completed Runs and Results retain historical integrity.
8. Required human review can be explicitly recorded.
9. Quality Gates can produce `PASS`, `REVIEW`, or `FAIL` through declarative policy.
10. Evaluation execution failure remains distinguishable from research-quality failure.
11. Historical evaluations remain tied to the exact evaluated Snapshot or delivery version.
12. Step 3 validation/provenance remains the single authority for canonical integrity.
13. Evaluation does not silently mutate canonical research state.
14. No duplicate provenance model is introduced.
15. No LLM Judge, benchmark platform, database, SaaS, or autonomous evaluation infrastructure is required.
16. A synthetic end-to-end research case can demonstrate the complete evaluation loop.

---

# 26. Explicitly Deferred Abstractions

The following may be reconsidered only when real use cases demonstrate the need:

```text
EvaluationMetric
Score
EvaluationTarget object
EvaluationFinding object
GateRun object
EvaluationPolicy object
Reviewer object
Evaluation persistence/database
LLM Judge
benchmark framework
statistical aggregation layer
```

This is intentional. Absence from Step 4 v1 is not an omission; it is scope control.

---

# 27. Architectural Invariants

The following are frozen invariants for Step 4 v1:

```text
1. Evaluation ≠ Validation.
2. Evaluation ≠ Judgment.
3. EvaluationResult ≠ Canonical Object.
4. Evaluation evaluates; it does not own canonical knowledge.
5. Evaluation is observational by default and MUST NOT silently mutate canonical state.
6. EvaluationRun MUST identify an explicit stable target.
7. Historical evaluation uses historical target state, not implicit current Registry state.
8. EvaluationRule version changes produce new evaluation context.
9. Completed EvaluationRun and EvaluationResult are immutable.
10. HumanReviewRecord does not rewrite the historical EvaluationResult.
11. QualityGate is policy, not a duplicate evaluator.
12. Gate outcomes are PASS / REVIEW / FAIL.
13. Result outcomes are PASS / FAIL / INCONCLUSIVE / NOT_APPLICABLE.
14. Metric and Score are not independent core objects in Step 4 v1.
15. A numeric Result value does not imply a canonical Score object.
16. Step 3 remains the authority for canonical integrity and provenance.
17. Evaluation reuses Step 3 validation instead of duplicating it.
18. Evaluation execution failure is not automatically a quality failure.
19. Human-required evaluation cannot silently become machine-approved.
20. No weighted aggregate research quality score is required by the v1 Gate.
21. No LLM Judge or benchmark framework is required for the Evaluation Core.
22. Evaluation history must be explainable from target, rule/version and evaluation context.
```

---

# 28. Future Compatibility

## Step 5 — Reproducible Build + Delivery

Step 5 can consume:

```text
EvaluationResult
QualityGate
HumanReviewRecord
```

to determine whether a delivery projection is eligible for generation or publication.

## Step 6 — End-to-End Validation Case

A new research case can exercise:

```text
Define
→ Discover
→ Evidence
→ Canonicalize
→ Snapshot
→ Evaluate
→ Human Review
→ Gate
→ Deliver
```

without modifying the Evaluation Core contract.

## Step 7 — Generalization Case

A second domain can demonstrate whether the current Rules and scopes are truly reusable. Case-specific rules remain possible without changing the core architecture.

## Step 9 — Automation / Skills / Agentization

Future automation may execute Evaluation Rules using models, tools, or agents, but the automation mechanism remains subordinate to the evaluation contract and human authority model.

A future LLM Judge, if later justified by evidence, would be an implementation mechanism behind a declared evaluation rule rather than an authority source that replaces the Evaluation Core contract.

---

# 29. Final Design Position

Step 4 should be implemented as a **small, versioned, evidence-aware Evaluation Layer** sitting above the canonical research state.

The architecture is:

```text
               Canonical Research State
                         │
                         ▼
                  Evaluation Run
                         │
                  Versioned Rules
                         │
                         ▼
                Evaluation Results
                         │
                         ▼
                   Quality Gate
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
            PASS       REVIEW      FAIL
                         │
                         ▼
                  Human Review
```

The architectural center is not the score.

It is the **explicit relationship between a stable research state, a declared quality criterion, an auditable result, and the human authority required to determine whether the work is ready to proceed.**

That is the minimum Evaluation Core required to move Research System v1 from:

```text
Canonical Knowledge
```

to:

```text
Canonical Knowledge
        ↓
Reliable Evaluation
        ↓
Controlled Progression
```

without collapsing knowledge, evaluation, governance, and automation into one subsystem.
