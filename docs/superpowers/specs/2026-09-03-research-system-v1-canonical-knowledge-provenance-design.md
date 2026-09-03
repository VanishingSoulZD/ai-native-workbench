# Research System v1 — Canonical Knowledge + Provenance Design

> **Status:** Approved design · Step 3 — Canonical Knowledge + Provenance
> **Date:** 2026-09-03
> **Repository:** `VanishingSoulZD/ai-native-workbench`
> **Depends on:** `docs/superpowers/specs/2026-09-03-research-system-contract-design.md`, Research System v1 Step 2 Workflow Core

## 0. Purpose

Step 3 establishes the minimum reusable **Canonical Knowledge + Provenance Core** for Research System v1.

The goal is not to build a universal knowledge graph or a general-purpose knowledge-management platform. The goal is to establish a small semantic authority layer in which important research knowledge has stable identity, explicit object semantics, inspectable references, machine-checkable provenance, first-class Unknown states, and recoverable historical snapshots.

The central rule is:

> **Artifacts carry research work; canonical objects carry semantic authority.**

The resulting flow is:

```text
Workflow Core
    ↓
Research Artifacts
    ↓
Canonicalization
    ↓
Canonical Registry
    ↓
Claims / Evidence / Sources / Entities / Unknowns / Relationships
    ↓
Provenance Validation
    ↓
Research Snapshot
```

Step 3 does not implement Evaluation, Delivery, rendering, agentization, or Case 001 migration.

---

# 1. Design Principles

## 1.1 Semantic authority

Canonical objects are the authoritative semantic representation of research knowledge. Markdown, HTML, PPT, CSV, working notes, and other artifacts may contain representations of canonical objects, but those representations do not become semantic authority merely because they are rendered or stored in a file.

## 1.2 Stable identity and historical state are separate concerns

A canonical object has a stable logical identity. A particular state of that object is identified within the registry by a content fingerprint. ResearchSnapshot records the exact object state used at a historical point in time.

Therefore:

```text
Logical ID = who this semantic object is
Fingerprint = what state this object had
Snapshot = which states constituted the research at that point in time
```

## 1.3 Evidence before assertion

Externally verifiable factual claims require an explicit path through Evidence to Source. The existence of a Claim object alone is never sufficient provenance.

## 1.4 Unknown is a knowledge state

Unknown represents a material unresolved research state. It is not a missing value or presentation convention.

```text
Unknown ≠ No
Unknown ≠ False
Unknown ≠ 0
Unknown ≠ Empty
Unknown ≠ Not Applicable
```

## 1.5 Minimal sufficient engineering

The first implementation is an in-memory/domain-model registry using Python standard-library structures. No database, graph database, vector store, ORM, semantic search, universal ingestion pipeline, or external knowledge graph is introduced.

---

# 2. Scope

## 2.1 Canonical objects implemented in the first slice

The first implementation slice contains exactly six canonical object types:

```text
Entity
Claim
Evidence
Source
Unknown
Relationship
```

These are sufficient to demonstrate the core canonical knowledge and provenance loop.

## 2.2 Canonical objects deferred

The following remain defined by the System Contract but are not implemented as Step 3 registry objects:

```text
Analysis
Metric
Score
Judgment
Recommendation
Decision
Hypothesis
```

They are deferred because the first Step 3 slice can establish semantic authority, provenance, Unknown preservation, and snapshot semantics without implementing the full reasoning and decision layer.

`Hypothesis` remains semantically distinct from `Claim`; it must never be represented as an established factual Claim by merely changing a Claim status.

## 2.3 Out of scope

Step 3 does not include:

- Case 001 migration, adapters, importers, or reconstruction;
- database or graph persistence;
- vector retrieval or RAG;
- semantic duplicate detection;
- automatic entity resolution;
- automatic contradiction resolution;
- LLM-powered canonicalization;
- search or query language;
- event sourcing, CQRS, or distributed state management;
- Evaluation records or reusable evaluator implementation;
- HumanGate persistence/governance records;
- Delivery rendering or dataset generation;
- workflow runner ownership of canonical state.

---

# 3. Relationship to Workflow Core

Step 2 and Step 3 have separate responsibilities:

```text
Workflow Core
    = execute declared workflow steps

Canonical Registry
    = own and validate canonical semantic state
```

The `WorkflowRunner` MUST NOT directly manage the lifecycle of canonical claims, evidence, sources, judgments, decisions, scores, or snapshots. A workflow execution may produce research artifacts; a later canonicalization boundary may convert selected material into canonical objects.

No Step 3 object should require the Step 2 runner implementation in order to exist or be validated.

---

# 4. Canonical Identity

## 4.1 CanonicalRef

All cross-object references use one representation:

```text
<object_type>:<logical_id>
```

Examples:

```text
entity:product-x
claim:product-x-repo-indexing
evidence:official-doc-001
source:vendor-docs-001
unknown:feature-y-support
```

This is the only reference form used for cross-object links in Step 3.

## 4.2 Logical ID

A logical ID is stable across ordinary state changes.

The object type is represented in `CanonicalRef`, not duplicated in the logical ID itself. Logical IDs are explicit identifiers rather than random per-ingestion identifiers. They do not depend on content hashing.

A logical ID identifies a semantic object; it does not assert that two different logical IDs are semantically equivalent.

## 4.3 Fingerprint

Every canonical state stored by the registry has a deterministic fingerprint derived from its canonical serialized state.

The fingerprint is used to distinguish historical states without changing logical identity.

Conceptually:

```text
(ref, fingerprint) → immutable canonical state
```

The implementation MUST use deterministic serialization before hashing so equivalent in-memory states do not receive different fingerprints merely because mapping iteration order differs.

The exact hashing algorithm and serialization implementation are implementation details of Step 3 and MUST remain deterministic and standard-library based.

## 4.4 Identity versus semantic deduplication

Registry identity and semantic equivalence are different problems.

The Registry MUST:

- reject duplicate logical IDs with conflicting object types;
- treat repeated registration of the same logical ID and identical canonical state as idempotent;
- preserve different logical IDs even when their current contents happen to be identical.

The Registry MUST NOT attempt semantic deduplication across different logical IDs.

---

# 5. Canonical Object Model

## 5.1 Entity

```python
Entity(
    id,
    entity_type,
    name,
    status,
    attributes,
)
```

`entity_type` is extensible and is not globally taxonomized in v1.

Minimum semantics:

- identifies a research subject;
- provides a stable canonical target for claims and relationships;
- does not encode domain-specific ontology machinery.

## 5.2 Claim

```python
Claim(
    id,
    statement,
    subject_ref,
    claim_type,
    status,
    confidence,
    evidence_ids,
)
```

`claim_type` distinguishes at minimum:

```text
factual
 derived
```

`status` is lifecycle/epistemic state and is not used to encode `hypothesis` or `unknown` as alternate object types.

A factual Claim without required provenance is invalid.

## 5.3 Evidence

```python
Evidence(
    id,
    source_id,
    observation,
    date_or_period,
    evidence_type,
    evidence_grade,
    supports_claim_ids,
    contradicts_claim_ids,
    note,
)
```

Evidence records an observation plus its source binding. It does not itself own the truth of a Claim.

## 5.4 Source

```python
Source(
    id,
    canonical_title,
    publisher,
    canonical_url,
    source_type,
    published_at,
    accessed_at,
    quality_tier,
)
```

A Source is a citable information source. Its URL is citation metadata and does not serve as the canonical identity mechanism.

## 5.5 Relationship

```python
Relationship(
    id,
    subject_ref,
    predicate,
    object_ref,
    evidence_ids,
    status,
)
```

Relationships are typed references between canonical objects. They are not an abstraction for a graph database.

## 5.6 Unknown

```python
Unknown(
    id,
    question,
    why_it_matters,
    scope,
    status,
)
```

An Unknown explicitly records an unresolved research state. The first implementation does not introduce probability, confidence intervals, Bayesian state, or automated resolution forecasts.

The fields `question`, `why_it_matters`, and `scope` must be non-empty so an Unknown remains meaningful after canonicalization and delivery.

---

# 6. Provenance Model

## 6.1 Core path

The first implementation must make the following chain mechanically inspectable:

```text
Claim
  ↓ supported_by
Evidence
  ↓ extracted_from
Source
```

For a delivery or higher-level reasoning object, the broader conceptual chain remains:

```text
Delivery Element
      ↓
Claim / Judgment
      ↓
Evidence
      ↓
Source
      ↓
Original Source
```

Step 3 implements the canonical Claim/Evidence/Source portion only.

## 6.2 Claim provenance

For `claim_type="factual"`, `evidence_ids` MUST contain at least one Evidence reference.

For `claim_type="derived"`, Step 3 permits the same Evidence linkage and does not introduce a separate analysis engine. More advanced derived-claim semantics belong to the later reasoning layer.

Every referenced Evidence object MUST exist.

## 6.3 Evidence provenance

Every Evidence MUST reference an existing Source through `source_id`.

Every `supports_claim_ids` and `contradicts_claim_ids` entry MUST resolve to an existing Claim.

A source cannot be supplied in an Evidence claim-binding field as a substitute for Evidence.

## 6.4 Reverse links

`Claim.evidence_ids` is the authoritative provenance declaration for the Claim.

`Evidence.supports_claim_ids` and `Evidence.contradicts_claim_ids` are reverse indexes used for inspection and integrity checking.

Step 3 does not introduce an automatic bidirectional synchronization subsystem. Validation may require declared reverse links to agree with forward links when both are present, but registration does not silently rewrite either side.

## 6.5 Contradicting evidence

Contradicting Evidence is represented explicitly through `contradicts_claim_ids`. Contradiction resolution is outside Step 3. The Registry preserves the contradiction rather than choosing a winner.

---

# 7. Reference Integrity

The Registry MUST validate:

1. every `CanonicalRef` has a valid object-type prefix and logical ID;
2. every reference resolves to an existing object state/current object as appropriate;
3. reference object type matches the field's declared semantic target;
4. every `Evidence.source_id` resolves to `Source`;
5. every Claim evidence reference resolves to `Evidence`;
6. every Evidence claim reference resolves to `Claim`;
7. every Relationship endpoint resolves to a supported canonical object;
8. every Relationship evidence reference resolves to `Evidence`.

The validator MUST report invariant violations as explicit exceptions rather than returning `False`, `None`, or silently skipping invalid references.

---

# 8. Registry API

The minimum Registry interface is:

```python
class CanonicalRegistry:
    def register(self, obj) -> CanonicalRef: ...
    def get(self, ref: CanonicalRef) -> CanonicalObject: ...
    def get_state(self, ref: CanonicalRef, fingerprint: str) -> CanonicalObject: ...
    def replace(self, ref: CanonicalRef, obj) -> str: ...
    def resolve(self, ref: CanonicalRef) -> CanonicalObject: ...
    def validate(self) -> None: ...
    def snapshot(self, snapshot_id: str, refs: Iterable[CanonicalRef]) -> ResearchSnapshot: ...
```

The concrete implementation may use more private helpers, but public behavior MUST remain within this conceptual boundary for the first slice.

## 8.1 Register

`register(obj)`:

- derives or validates the object's `CanonicalRef`;
- validates the object's own required fields;
- stores its canonical state and fingerprint;
- is idempotent when the same logical ID and identical state are registered again;
- rejects an existing logical ID paired with a conflicting object type;
- does not perform semantic deduplication across different logical IDs.

## 8.2 Get

`get(ref)` returns the current state for that logical object.

It does not return an arbitrary historical state.

## 8.3 Get state

`get_state(ref, fingerprint)` returns the exact immutable historical state identified by both logical reference and fingerprint.

Unknown references or fingerprints MUST raise a Registry/Resolution error.

## 8.4 Replace

`replace(ref, obj)` creates a new state under the same logical identity when the object type is compatible.

The prior state remains addressable by its fingerprint.

A snapshot-referenced state MUST NOT be mutated in place.

## 8.5 Resolve

`resolve(ref)` provides canonical reference resolution without creating or mutating objects.

It is the common entry point for provenance and referential-integrity checks.

## 8.6 Validate

`validate()` performs mechanical integrity checks over all registered current states and their references.

It MUST detect:

```text
invalid object fields
invalid CanonicalRef syntax
missing references
wrong reference types
broken Claim → Evidence → Source provenance
broken Relationship references
invalid Unknown state
invalid historical-state records
```

## 8.7 Snapshot

`snapshot(snapshot_id, refs)` freezes a set of exact object states into a ResearchSnapshot.

The snapshot MUST store object logical references together with their fingerprints.

Conceptually:

```python
members = {
    "entity:product-x": "sha256:...",
    "claim:product-x-repo-indexing": "sha256:...",
    "evidence:official-doc-1": "sha256:...",
    "source:vendor-doc-1": "sha256:...",
}
```

The snapshot API MUST reject references that cannot be resolved to a current or explicitly selected valid state.

---

# 9. Duplicate and Replace Semantics

The first slice uses exactly three duplicate cases:

| Condition | Behavior |
|---|---|
| Same logical ID + same canonical fingerprint | Idempotent success; no duplicate state |
| Same logical ID + different fingerprint | New immutable state under same logical ID |
| Different logical IDs + identical content | Preserve both; no automatic merge |

The Registry does not infer semantic equivalence.

A logical ID that changes object type is invalid. For example, an existing `claim:foo` cannot become a `source:foo` state through replace.

---

# 10. Snapshot Semantics

## 10.1 Snapshot identity

A `ResearchSnapshot` is a versioned point-in-time research state governed by the System Contract.

Its minimum implementation-relevant membership semantics are:

```text
snapshot_id
case_id
cutoff
workflow_version
schema_version
transformation_version
configuration_hash?
assumptions_hash?
status
members: CanonicalRef → fingerprint
```

The exact surrounding lifecycle fields remain aligned with the System Contract; Step 3 only adds the canonical membership boundary and historical-state resolution needed for integrity.

## 10.2 Immutability

Once a snapshot is validated/published/superseded/archived, its membership and referenced state MUST NOT be silently mutated.

A historical correction creates a new versioned state and normally a new snapshot rather than modifying the old state in place.

## 10.3 Current registry changes do not rewrite history

If:

```text
claim:c1 → fingerprint:A
```

is captured by Snapshot S1, and the current Registry later advances to fingerprint B, then S1 continues resolving to A.

The implementation MUST never resolve historical snapshot membership merely by calling `get(ref)` and assuming the returned current state is historical truth.

## 10.4 Snapshot recoverability

For every member `(ref, fingerprint)` in a valid snapshot:

```text
get_state(ref, fingerprint)
```

MUST recover the exact canonical state.

If any member cannot be recovered, snapshot validation fails.

---

# 11. Error Model

Step 3 uses explicit error categories:

```text
CanonicalValidationError
RegistryError
ResolutionError
IntegrityError
SnapshotError
```

The exact exception hierarchy may be implemented with shared base classes, but callers must be able to distinguish malformed objects from registry conflicts and broken references/snapshots.

No invalid state may be silently accepted.

---

# 12. Testing Strategy

The Step 3 test suite must cover:

### Object validation

- required fields;
- stable identity format;
- valid and invalid object types;
- Claim type/status rules;
- Unknown required semantic fields.

### Registry behavior

- registration;
- idempotent duplicate registration;
- conflicting type rejection;
- replacement and historical state retention;
- current-state resolution;
- historical-state resolution.

### Provenance

- Claim → Evidence → Source success;
- missing Evidence rejection;
- missing Source rejection;
- wrong-type reference rejection;
- support/contradiction references;
- Relationship reference validation.

### Snapshot

- snapshot creation;
- exact fingerprint membership;
- historical recovery after replacement;
- invalid/missing historical state rejection;
- immutable validated/published snapshot behavior.

### Unknown

- Unknown is preserved as an explicit object;
- Unknown is not converted to False/No/0/empty;
- invalid Unknown fields are rejected.

The first implementation should include a small synthetic validation case built entirely from test fixtures. It must not import, read, or adapt Case 001.

---

# 13. Interface with Research Artifacts

Research artifacts remain work carriers. A research note can contain text corresponding to a Claim or Evidence, but the artifact is not the semantic identity of that object.

The canonicalization boundary is conceptually:

```text
ResearchArtifact
    ↓ extraction / normalization
Canonical Object
    ↓ register
Canonical Registry
```

Step 3 does not implement a universal extraction pipeline. It only defines the domain boundary that such a pipeline will use later.

---

# 14. Success Criteria / Exit Condition

Step 3 is successful when a synthetic research package can demonstrate all of the following without Case 001-specific code:

1. canonical objects have stable logical identities;
2. current and historical states can be distinguished by fingerprint;
3. Claim/Evidence/Source provenance is machine-checkable;
4. typed canonical references resolve correctly;
5. Unknown survives as an explicit semantic state;
6. duplicate registration is controlled and deterministic;
7. replacing a canonical object does not mutate its prior state;
8. a ResearchSnapshot records exact state fingerprints;
9. an old snapshot remains recoverable after current registry changes;
10. invalid references and malformed states fail mechanically.

The Methodology Step 3 exit condition is therefore met only when important research facts can be represented independently of delivery format and traced through provenance. The first slice intentionally proves the mechanism with a synthetic case rather than rebuilding Case 001.

---

# 15. Architectural Decisions Summary

| Decision | Choice | Reason |
|---|---|---|
| Stable identity | Logical ID | Stable semantic reference independent of content changes |
| Historical identity | Logical ID + fingerprint | Separates object identity from historical state |
| Cross-object references | `type:logical-id` CanonicalRef | Uniform validation and provenance traversal |
| Registry storage | In-memory/simple serialized state | Minimal infrastructure and easy testing |
| Deduplication | Identity/state idempotency only | Avoids premature semantic entity resolution |
| Provenance | Claim → Evidence → Source | Directly satisfies core evidence-first invariant |
| Unknown | First-class canonical object | Prevents false certainty and information loss |
| Snapshot | Immutable membership of `(ref, fingerprint)` | Prevents silent historical mutation |
| Graph technology | None | Relationships are typed references, not graph infrastructure |
| Canonicalization | Explicit boundary, no universal pipeline | Preserves scope and keeps artifacts separate from authority |
