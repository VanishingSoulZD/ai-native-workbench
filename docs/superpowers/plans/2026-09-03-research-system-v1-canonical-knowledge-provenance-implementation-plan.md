# Research System v1 — Canonical Knowledge + Provenance Implementation Plan

> **Status:** Approved implementation plan · Step 3 — Canonical Knowledge + Provenance
> **Date:** 2026-09-03
> **Design:** `docs/superpowers/specs/2026-09-03-research-system-v1-canonical-knowledge-provenance-design.md`
> **Methodology:** `docs/methodology/research-system-v1.md`

## Goal

Implement the minimum reusable Canonical Knowledge + Provenance Core so canonical research objects have stable identity, typed references, machine-checkable provenance, explicit Unknown states, and recoverable historical snapshot membership.

## Architecture

Use a small Python standard-library domain layer under `src/ai_native_workbench/research/canonical/`. Keep Workflow Core and Canonical Registry separate: Workflow produces research artifacts; canonicalization promotes selected material into semantic authority. The Registry is an in-memory typed registry with immutable historical states keyed by deterministic fingerprints.

## Technical constraints

- Python 3.11+
- `dataclasses`, `enum`, `typing`, `hashlib`, `json`
- pytest
- No database, ORM, graph database, vector store, Pydantic, LangChain, LangGraph, MCP, agent runtime, or external persistence
- No Case 001 migration, adapter, importer, or coupling
- No semantic deduplication, automatic entity resolution, contradiction resolution, search, RAG, evaluation, delivery, or agentization
- TDD for every task: failing test → minimal implementation → focused verification → full suite → commit

## Target file structure

Create:

```text
src/ai_native_workbench/research/canonical/
├── __init__.py
├── errors.py
├── identity.py
├── model.py
├── provenance.py
├── registry.py
└── snapshot.py
```

Tests:

```text
tests/unit/research/canonical/
├── test_identity.py
├── test_model.py
├── test_registry.py
├── test_provenance.py
└── test_snapshot.py

tests/integration/research/canonical/
└── test_synthetic_research_case.py
```

## Task 1 — Canonical Identity

Implement `CanonicalObjectType`, frozen/hashable `CanonicalRef`, deterministic canonical serialization, and `canonical_fingerprint()`.

Reference format:

```text
<object_type>:<logical_id>
```

Fingerprint format:

```text
sha256:<hex digest>
```

Tests MUST cover round-trip parsing, invalid references, deterministic hashing independent of mapping order, and fingerprint changes after state changes.

Commit:

```text
feat: add canonical identity and fingerprints
```

## Task 2 — Canonical Domain Model

Implement exactly these six first-slice canonical objects:

```text
Entity
Claim
Evidence
Source
Unknown
Relationship
```

Use frozen dataclasses. Intrinsic validation covers required fields, Claim `factual`/`derived` type semantics, factual Claim evidence requirement, confidence range, and meaningful Unknown fields.

Do not perform cross-object existence checks here.

Commit:

```text
feat: add canonical research object models
```

## Task 3 — Canonical Registry

Implement:

```python
register(obj) -> CanonicalRef
get(ref) -> CanonicalObject
get_state(ref, fingerprint) -> CanonicalObject
replace(ref, obj) -> str
resolve(ref) -> CanonicalObject
validate() -> None
snapshot(...) -> ResearchSnapshot
```

Internal state may use current `CanonicalRef -> fingerprint` and historical `CanonicalRef -> fingerprint -> object` mappings.

Rules:

- same ref + same fingerprint = idempotent
- same ref + different fingerprint = new immutable state
- different refs with identical content = preserve both
- conflicting object type for an existing logical ID = reject
- historical states are never mutated
- no semantic deduplication

Commit:

```text
feat: add canonical registry state lifecycle
```

## Task 4 — Referential Integrity + Provenance

Implement mechanical validation for:

```text
Claim → Evidence → Source
Claim.subject_ref → Entity
Claim.evidence_ids → Evidence
Evidence.source_id → Source
Evidence.supports_claim_ids → Claim
Evidence.contradicts_claim_ids → Claim
Relationship endpoints → existing canonical objects
Relationship.evidence_ids → Evidence
```

`Claim.evidence_ids` is the forward provenance authority. Reverse Evidence claim links are inspection/integrity links; registration does not silently rewrite them.

Contradictions are preserved, not resolved.

Commit:

```text
feat: add canonical referential integrity and provenance validation
```

## Task 5 — Unknown + Registry-Wide Validation

Keep Unknown as a first-class object:

```text
Unknown ≠ False
Unknown ≠ No
Unknown ≠ 0
Unknown ≠ Empty
Unknown ≠ N/A
```

Mechanically validate malformed objects, invalid refs, wrong reference types, broken provenance, broken relationships, invalid Unknown states, and invalid historical states.

Use explicit exception categories such as:

```text
CanonicalValidationError
RegistryError
ResolutionError
IntegrityError
SnapshotError
```

Commit:

```text
feat: enforce unknown and canonical integrity invariants
```

## Task 6 — ResearchSnapshot

Implement immutable `ResearchSnapshot` membership as:

```text
CanonicalRef → fingerprint
```

The snapshot captures the exact current fingerprints at creation. Historical recovery MUST use `get_state(ref, fingerprint)`, never current `get(ref)` as a substitute for historical truth.

Snapshot validation MUST ensure every member fingerprint remains recoverable. Current registry replacement MUST NOT mutate old snapshot meaning.

Commit:

```text
feat: add immutable research snapshot semantics
```

## Task 7 — Synthetic End-to-End Validation

Create a completely synthetic research case, independent of Case 001, containing:

```text
Source
Entity
Evidence
Claim
Unknown
Relationship
ResearchSnapshot
```

The test MUST prove:

```text
stable IDs
→ idempotent duplicate registration
→ Claim/Evidence/Source validation
→ explicit Unknown preservation
→ Relationship validation
→ snapshot fingerprint capture
→ replacement creates new current state
→ old snapshot resolves old state
→ invalid reference fails mechanically
```

Commit:

```text
 test: validate canonical knowledge provenance end to end
```

## Verification matrix

After every task:

```bash
pytest <focused-tests> -q
pytest -q
```

After Task 7, full suite MUST pass and the integration test MUST contain no Case 001 imports.

Verify additionally that canonical modules do not import `WorkflowRunner` or make Step 2 responsible for canonical lifecycle.

## Exit condition

Step 3 is complete only when the synthetic case demonstrates:

```text
Research Artifacts
      ↓
Canonical Objects
      ↓
Stable Logical Identity
      ↓
Typed Canonical References
      ↓
Claim → Evidence → Source
      ↓
Mechanical Validation
      ↓
Snapshot(ref → fingerprint)
      ↓
Historical Recovery
```

The implementation stops at this boundary. Evaluation is Step 4; reproducible build/delivery is Step 5; Case 001 validation is Step 6.
