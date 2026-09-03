# Research System v1 — Canonical Knowledge + Provenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the minimum reusable Canonical Knowledge + Provenance Core for Research System v1 so research knowledge has stable logical identity, typed references, machine-checkable provenance, explicit Unknown states, and recoverable historical snapshots without coupling the Canonical Registry to Workflow Core or Case 001.

**Architecture:** Build a small standard-library Python domain package under `src/ai_native_workbench/research/canonical/`. Separate semantic authority from work artifacts: Workflow Core continues to execute declared workflow steps, while canonicalization promotes selected artifact content into six first-slice canonical object types. Store the current state by `CanonicalRef` and retain immutable historical states by deterministic fingerprint; use a separate immutable `ResearchSnapshot` membership map to recover historical research meaning.

**Tech Stack:** Python 3.11+, `dataclasses`, `enum`, `typing`, `hashlib`, `json`, `types.MappingProxyType`, and `pytest>=8,<9`. No runtime dependency is added.

**Spec:** `docs/superpowers/specs/2026-09-03-research-system-v1-canonical-knowledge-provenance-design.md`

**Methodology:** `docs/methodology/research-system-v1.md` — Research System v1 Canonical Knowledge layer and revised roadmap.

**System Contract:** `docs/superpowers/specs/2026-09-03-research-system-contract-design.md`

**Repository guidance:** `CLAUDE.md`

## Global Constraints

- **Artifacts carry research work; canonical objects carry semantic authority.**
- **Workflow Core and Canonical Registry remain separate responsibilities.** The `WorkflowRunner` must not own canonical object lifecycle.
- The first implementation slice contains exactly six canonical object types: `Entity`, `Claim`, `Evidence`, `Source`, `Unknown`, and `Relationship`.
- Deferred canonical objects are `Analysis`, `Metric`, `Score`, `Judgment`, `Recommendation`, `Decision`, and `Hypothesis`.
- `Hypothesis` is semantically distinct from `Claim` and must never be represented as an established factual Claim by changing Claim status.
- Cross-object references use the single representation `<object_type>:<logical_id>` through `CanonicalRef`.
- Logical ID is stable semantic identity; fingerprint identifies the immutable state of that logical object.
- Deterministic fingerprint serialization must be independent of mapping insertion order.
- Same logical ID + same fingerprint is idempotent; same logical ID + different fingerprint creates a new historical state; different logical IDs with identical content remain distinct.
- Existing logical IDs cannot be reused with a conflicting object type.
- `Claim.evidence_ids` is the forward provenance authority. Evidence reverse claim links are inspection/integrity links and are not silently rewritten.
- Factual Claims require at least one Evidence reference; Evidence requires a Source reference.
- Contradictions are preserved through `Evidence.contradicts_claim_ids`; Step 3 does not resolve contradictions.
- `Unknown` is a first-class semantic state and must not be collapsed into `False`, `No`, `0`, empty, or `N/A`.
- `ResearchSnapshot` stores exact `CanonicalRef -> fingerprint` membership and historical recovery must use `get_state(ref, fingerprint)`, never current `get(ref)` as historical truth.
- Use explicit error categories so callers can distinguish validation, registry, resolution, integrity, and snapshot failures.
- No database, ORM, graph database, vector store, Pydantic, LangChain, LangGraph, MCP, agent runtime, external persistence, event sourcing, CQRS, distributed state management, or universal ingestion pipeline.
- No semantic deduplication, automatic entity resolution, automatic contradiction resolution, search, RAG, evaluation, delivery, rendering, or agentization.
- No Case 001 migration, adapter, importer, reconstruction, or test fixture dependency.
- No changes to the approved System Contract, approved Design Spec, or Research System methodology are part of this implementation plan.
- Every implementation task follows TDD: write failing test → run it and confirm failure → implement the minimum change → run focused tests → run full suite → commit.

---

## 1. Implementation Boundary and File Structure

The execution order is deliberately dependency-aware. Each task leaves the repository in a coherent, testable state and introduces only the capability needed by later tasks.

### Files created by this plan

```text
src/ai_native_workbench/research/canonical/
├── __init__.py
├── errors.py
├── identity.py
├── model.py
├── provenance.py
├── registry.py
└── snapshot.py

tests/unit/research/canonical/
├── test_identity.py
├── test_model.py
├── test_registry.py
├── test_provenance.py
└── test_snapshot.py

tests/integration/research/canonical/
└── test_synthetic_research_case.py
```

### Existing files deliberately not modified by the implementation

- `src/ai_native_workbench/research/workflow/*.py` — Workflow Core stays independent.
- `tests/unit/research/workflow/*.py` — existing Step 2 tests remain the guardrail for the workflow boundary.
- `cases/001-ai-coding-agent-landscape/**` — no migration or coupling.
- `docs/methodology/research-system-v1.md` — methodology remains the approved baseline.
- `docs/superpowers/specs/2026-09-03-research-system-contract-design.md` — System Contract remains frozen.
- `docs/superpowers/specs/2026-09-03-research-system-v1-canonical-knowledge-provenance-design.md` — approved Step 3 design remains frozen.

### Responsibility of each new file

| File | Single responsibility |
|---|---|
| `errors.py` | Stable exception hierarchy for validation, registry, resolution, integrity, and snapshot failures. |
| `identity.py` | Object-type enum, `CanonicalRef`, deterministic canonical serialization, and state fingerprinting. |
| `model.py` | Six first-slice frozen canonical domain objects and intrinsic validation only. |
| `provenance.py` | Cross-object reference and Claim/Evidence/Source/Relationship integrity rules. |
| `registry.py` | Current state, immutable historical state retention, registration/replacement/resolution, registry-wide validation, and snapshot construction boundary. |
| `snapshot.py` | Immutable point-in-time membership and historical-state recoverability contract. |
| `__init__.py` | Public exports only; no lifecycle logic. |

### Public type contract established by the end of Task 2

```python
from ai_native_workbench.research.canonical.identity import (
    CanonicalObjectType,
    CanonicalRef,
    canonical_fingerprint,
    canonical_serialize,
)
from ai_native_workbench.research.canonical.model import (
    Entity,
    Claim,
    Evidence,
    Source,
    Unknown,
    Relationship,
)

CanonicalObject = Entity | Claim | Evidence | Source | Unknown | Relationship
```

### Public Registry contract established by the end of Task 6

```python
class CanonicalRegistry:
    def register(self, obj: CanonicalObject) -> CanonicalRef: ...
    def get(self, ref: CanonicalRef) -> CanonicalObject: ...
    def get_state(self, ref: CanonicalRef, fingerprint: str) -> CanonicalObject: ...
    def replace(self, ref: CanonicalRef, obj: CanonicalObject) -> str: ...
    def resolve(self, ref: CanonicalRef) -> CanonicalObject: ...
    def validate(self) -> None: ...
    def snapshot(
        self,
        snapshot_id: str,
        refs: tuple[CanonicalRef, ...],
        *,
        case_id: str = "synthetic-case",
        cutoff: str = "",
        workflow_version: str = "",
        schema_version: str = "1",
        transformation_version: str = "1",
        configuration_hash: str | None = None,
        assumptions_hash: str | None = None,
        status: str = "draft",
    ) -> ResearchSnapshot: ...
```

---

## 2. Task 1: Establish Canonical Identity and Deterministic Fingerprints

**Files:**
- Create: `src/ai_native_workbench/research/canonical/errors.py`
- Create: `src/ai_native_workbench/research/canonical/identity.py`
- Create: `src/ai_native_workbench/research/canonical/__init__.py`
- Create: `tests/unit/research/canonical/test_identity.py`

**Interfaces:**
- Consumes: Python 3.11 standard-library only.
- Produces:
  - `CanonicalObjectType(StrEnum-like string Enum)` with values `entity`, `claim`, `evidence`, `source`, `unknown`, `relationship`.
  - frozen/hashable `CanonicalRef(object_type: CanonicalObjectType, logical_id: str)`.
  - `CanonicalRef.parse(value: str) -> CanonicalRef`.
  - `str(ref) -> "<object_type>:<logical_id>"`.
  - `canonical_serialize(value: object) -> str`.
  - `canonical_fingerprint(value: object) -> str` returning `sha256:<64 lowercase hex characters>`.
  - `CanonicalValidationError`, `RegistryError`, `ResolutionError`, `IntegrityError`, `SnapshotError` base categories.

- [ ] **Step 1: Write the failing identity tests**

Create tests with concrete cases rather than abstract test placeholders:

```python
from dataclasses import dataclass

import pytest

from ai_native_workbench.research.canonical.errors import CanonicalValidationError
from ai_native_workbench.research.canonical.identity import (
    CanonicalObjectType,
    CanonicalRef,
    canonical_fingerprint,
)


def test_canonical_ref_round_trips():
    ref = CanonicalRef(CanonicalObjectType.CLAIM, "product-x-support")
    assert str(ref) == "claim:product-x-support"
    assert CanonicalRef.parse(str(ref)) == ref


def test_canonical_ref_is_hashable():
    ref = CanonicalRef(CanonicalObjectType.ENTITY, "product-x")
    assert {ref: "state"}[ref] == "state"


def test_invalid_canonical_ref_is_rejected():
    with pytest.raises(CanonicalValidationError):
        CanonicalRef.parse("not-a-valid-ref")


def test_empty_logical_id_is_rejected():
    with pytest.raises(CanonicalValidationError):
        CanonicalRef(CanonicalObjectType.ENTITY, "")


def test_fingerprint_is_independent_of_mapping_order():
    first = {"name": "Product X", "attributes": {"tier": "pro", "region": "global"}}
    second = {"attributes": {"region": "global", "tier": "pro"}, "name": "Product X"}
    assert canonical_fingerprint(first) == canonical_fingerprint(second)


def test_fingerprint_changes_when_state_changes():
    first = {"id": "product-x", "status": "active"}
    second = {"id": "product-x", "status": "deprecated"}
    assert canonical_fingerprint(first) != canonical_fingerprint(second)
```

Also assert that all six enum values parse and that `str(CanonicalRef(...))` is the sole wire representation.

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```bash
pytest tests/unit/research/canonical/test_identity.py -q
```

Expected: FAIL because the new package and identity types do not yet exist.

- [ ] **Step 3: Implement the minimum identity and error layer**

Use a string-valued enum so refs are easy to serialize:

```python
class CanonicalObjectType(str, Enum):
    ENTITY = "entity"
    CLAIM = "claim"
    EVIDENCE = "evidence"
    SOURCE = "source"
    UNKNOWN = "unknown"
    RELATIONSHIP = "relationship"
```

Implement `CanonicalRef` as a frozen dataclass and reject logical IDs containing `:` so parsing remains unambiguous:

```python
@dataclass(frozen=True)
class CanonicalRef:
    object_type: CanonicalObjectType
    logical_id: str

    def __post_init__(self) -> None:
        if not self.logical_id or not self.logical_id.strip():
            raise CanonicalValidationError("CanonicalRef logical_id must not be empty.")
        if ":" in self.logical_id:
            raise CanonicalValidationError("CanonicalRef logical_id must not contain ':'.")

    def __str__(self) -> str:
        return f"{self.object_type.value}:{self.logical_id}"

    @classmethod
    def parse(cls, value: str) -> "CanonicalRef":
        if not isinstance(value, str) or value.count(":") != 1:
            raise CanonicalValidationError(f"Invalid CanonicalRef: {value!r}.")
        object_type_value, logical_id = value.split(":", 1)
        try:
            object_type = CanonicalObjectType(object_type_value)
        except ValueError as error:
            raise CanonicalValidationError(
                f"Unknown canonical object type: {object_type_value!r}."
            ) from error
        return cls(object_type, logical_id)
```

Implement canonical serialization recursively for mappings, sequences, enums, dataclasses, and primitive values, with sorted mapping keys and compact JSON:

```python
def canonical_serialize(value: object) -> str:
    normalized = _normalize(value)
    return json.dumps(normalized, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def canonical_fingerprint(value: object) -> str:
    payload = canonical_serialize(value).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"
```

Normalize dataclasses with `dataclasses.fields`, enums through `.value`, mappings through sorted keys, tuples/lists through ordered lists, and primitive values directly. Raise `CanonicalValidationError` for unsupported values instead of hashing an unstable representation.

Export only identity types and exceptions from package `__init__.py` at this stage.

- [ ] **Step 4: Run focused tests and verify pass**

Run:

```bash
pytest tests/unit/research/canonical/test_identity.py -q
```

Expected: PASS for round-trip refs, invalid refs, hashability, deterministic mapping serialization, and state-sensitive fingerprints.

- [ ] **Step 5: Run the complete suite**

Run:

```bash
pytest -q
```

Expected: PASS; existing Workflow Core tests remain unchanged and green.

- [ ] **Step 6: Commit the identity slice**

```bash
git add src/ai_native_workbench/research/canonical tests/unit/research/canonical/test_identity.py
git commit -m "feat: add canonical identity and fingerprints"
```

---

## 3. Task 2: Implement the Six First-Slice Canonical Domain Objects

**Files:**
- Create: `src/ai_native_workbench/research/canonical/model.py`
- Modify: `src/ai_native_workbench/research/canonical/__init__.py`
- Create: `tests/unit/research/canonical/test_model.py`

**Interfaces:**
- Consumes: `CanonicalObjectType`, `CanonicalRef`, and `CanonicalValidationError` from Task 1.
- Produces frozen dataclasses with the exact fields below and intrinsic validation only.

### Object constructor contract

```python
@dataclass(frozen=True)
class Entity:
    id: str
    entity_type: str
    name: str
    status: str
    attributes: Mapping[str, object] = field(default_factory=dict)
```

```python
@dataclass(frozen=True)
class Claim:
    id: str
    statement: str
    subject_ref: CanonicalRef
    claim_type: str
    status: str
    confidence: float | None
    evidence_ids: tuple[CanonicalRef, ...]
```

```python
@dataclass(frozen=True)
class Evidence:
    id: str
    source_id: CanonicalRef
    observation: str
    date_or_period: str
    evidence_type: str
    evidence_grade: str
    supports_claim_ids: tuple[CanonicalRef, ...]
    contradicts_claim_ids: tuple[CanonicalRef, ...]
    note: str
```

```python
@dataclass(frozen=True)
class Source:
    id: str
    canonical_title: str
    publisher: str
    canonical_url: str
    source_type: str
    published_at: str
    accessed_at: str
    quality_tier: str
```

```python
@dataclass(frozen=True)
class Unknown:
    id: str
    question: str
    why_it_matters: str
    scope: str
    status: str
```

```python
@dataclass(frozen=True)
class Relationship:
    id: str
    subject_ref: CanonicalRef
    predicate: str
    object_ref: CanonicalRef
    evidence_ids: tuple[CanonicalRef, ...]
    status: str
```

Add an `object_type` property to each model returning its corresponding `CanonicalObjectType`, and a `canonical_ref` property returning `CanonicalRef(object_type, id)`. Keep those properties derived; do not duplicate them as mutable fields.

- [ ] **Step 1: Write failing model validation tests**

The tests must prove:

```python
def test_entity_has_stable_canonical_ref(): ...
def test_claim_defaults_to_no_implicit_evidence(): ...
def test_factual_claim_requires_evidence(): ...
def test_derived_claim_can_exist_without_factual_assertion_semantics(): ...
def test_claim_confidence_must_be_between_zero_and_one(): ...
def test_claim_rejects_unknown_claim_type(): ...
def test_evidence_requires_source_ref_of_source_type(): ...
def test_relationship_requires_canonical_refs(): ...
def test_unknown_requires_question_why_it_matters_and_scope(): ...
def test_models_are_frozen(): ...
```

Use concrete assertions such as:

```python
def test_factual_claim_requires_evidence():
    with pytest.raises(CanonicalValidationError):
        Claim(
            id="claim-1",
            statement="Product X supports indexing.",
            subject_ref=CanonicalRef(CanonicalObjectType.ENTITY, "product-x"),
            claim_type="factual",
            status="active",
            confidence=1.0,
            evidence_ids=(),
        )
```

The tests must not assert cross-object registry existence; an `Entity` may not yet be registered when a `Claim` object is constructed.

- [ ] **Step 2: Run the focused model tests and verify failure**

Run:

```bash
pytest tests/unit/research/canonical/test_model.py -q
```

Expected: FAIL because `model.py` does not exist.

- [ ] **Step 3: Implement frozen dataclasses with intrinsic validation**

Centralize common non-empty string validation and call it from `__post_init__`.

The following rules are mandatory:

```text
Entity: id/entity_type/name/status non-empty.
Claim: id/statement/status non-empty; claim_type in {factual, derived}; confidence is None or 0.0 <= confidence <= 1.0; factual requires at least one evidence_id.
Evidence: id/observation/date_or_period/evidence_type/evidence_grade/note non-empty as declared strings; source_id must be a CanonicalRef whose object_type is SOURCE; reverse claim refs must be CLAIM refs.
Source: id/canonical_title/publisher/canonical_url/source_type/published_at/accessed_at/quality_tier non-empty.
Unknown: id/question/why_it_matters/scope/status non-empty.
Relationship: id/predicate/status non-empty; evidence_ids must all be EVIDENCE refs; subject/object refs must use a supported canonical type.
```

Do not validate whether referenced objects exist. Do not rewrite reverse links. Do not introduce Pydantic or a generic validation framework.

- [ ] **Step 4: Run focused model tests and verify pass**

Run:

```bash
pytest tests/unit/research/canonical/test_model.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the complete suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit the domain model slice**

```bash
git add src/ai_native_workbench/research/canonical/model.py src/ai_native_workbench/research/canonical/__init__.py tests/unit/research/canonical/test_model.py
git commit -m "feat: add canonical research object models"
```

---

## 4. Task 3: Implement the Canonical Registry State Lifecycle

**Files:**
- Create: `src/ai_native_workbench/research/canonical/registry.py`
- Modify: `src/ai_native_workbench/research/canonical/__init__.py`
- Create: `tests/unit/research/canonical/test_registry.py`

**Interfaces:**
- Consumes: `CanonicalObject`, `CanonicalRef`, `canonical_fingerprint`, and error categories from Tasks 1–2.
- Produces `CanonicalRegistry` with the public methods defined in Section 1.

Internal representation:

```python
self._current: dict[CanonicalRef, str]
self._states: dict[CanonicalRef, dict[str, CanonicalObject]]
self._logical_id_types: dict[str, CanonicalObjectType]
```

`_states[ref][fingerprint]` is the only addressable historical state store. Returned objects are never mutated in place.

- [ ] **Step 1: Write failing registry tests**

Create concrete tests for:

```python
def test_register_stores_current_state(): ...
def test_register_same_state_is_idempotent(): ...
def test_register_same_logical_id_with_changed_state_keeps_history(): ...
def test_different_logical_ids_with_same_content_are_preserved(): ...
def test_same_logical_id_cannot_change_object_type(): ...
def test_get_returns_current_state_only(): ...
def test_get_state_returns_exact_historical_state(): ...
def test_get_unknown_ref_raises_resolution_error(): ...
def test_get_unknown_fingerprint_raises_resolution_error(): ...
def test_resolve_is_an_alias_for_current_resolution_without_mutation(): ...
def test_replace_requires_same_canonical_object_type(): ...
def test_historical_state_does_not_change_after_replace(): ...
```

The historical-state test should make the failure observable:

```python
entity_v1 = Entity("product-x", "product", "Product X", "active", {"tier": "pro"})
ref = registry.register(entity_v1)
fingerprint_v1 = canonical_fingerprint(entity_v1)
entity_v2 = Entity("product-x", "product", "Product X", "deprecated", {"tier": "pro"})
registry.replace(ref, entity_v2)
assert registry.get(ref).status == "deprecated"
assert registry.get_state(ref, fingerprint_v1).status == "active"
```

- [ ] **Step 2: Run focused registry tests and verify failure**

Run:

```bash
pytest tests/unit/research/canonical/test_registry.py -q
```

Expected: FAIL because `CanonicalRegistry` does not yet exist.

- [ ] **Step 3: Implement registration, resolution, replacement, and history**

Use the object-derived ref as the authority:

```python
def register(self, obj: CanonicalObject) -> CanonicalRef:
    ref = obj.canonical_ref
    fingerprint = canonical_fingerprint(obj)
    known_type = self._logical_id_types.get(obj.id)
    if known_type is not None and known_type is not ref.object_type:
        raise RegistryError("logical ID is already bound to a different object type")
    self._logical_id_types[obj.id] = ref.object_type
    states = self._states.setdefault(ref, {})
    states.setdefault(fingerprint, obj)
    self._current[ref] = fingerprint
    return ref
```

`replace(ref, obj)` must first validate that `obj.canonical_ref == ref`, then store the new fingerprint without deleting the previous fingerprint.

`get(ref)` must retrieve the current fingerprint and return the exact stored historical object. `get_state(ref, fingerprint)` must look up the exact state and raise `ResolutionError` if either the ref or fingerprint is unknown. `resolve(ref)` delegates to current resolution and performs no mutation.

Do not add semantic deduplication. Do not merge objects with identical content under different logical IDs.

- [ ] **Step 4: Run focused tests and verify pass**

Run:

```bash
pytest tests/unit/research/canonical/test_registry.py -q
```

Expected: PASS, including idempotency, historical retention, and type-conflict rejection.

- [ ] **Step 5: Run the complete suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit the registry lifecycle slice**

```bash
git add src/ai_native_workbench/research/canonical/registry.py src/ai_native_workbench/research/canonical/__init__.py tests/unit/research/canonical/test_registry.py
git commit -m "feat: add canonical registry state lifecycle"
```

---

## 5. Task 4: Implement Referential Integrity and Provenance Validation

**Files:**
- Create: `src/ai_native_workbench/research/canonical/provenance.py`
- Modify: `src/ai_native_workbench/research/canonical/registry.py`
- Modify: `tests/unit/research/canonical/test_provenance.py`
- Modify: `tests/unit/research/canonical/test_registry.py`

**Interfaces:**
- Consumes: registry resolution and six canonical models from Tasks 1–3.
- Produces:
  - `validate_object_references(obj: CanonicalObject, registry: CanonicalRegistry) -> None`
  - `validate_registry_integrity(registry: CanonicalRegistry) -> None`
- Registry `validate()` delegates to `validate_registry_integrity(self)`.

Validation is mechanical and raises `IntegrityError` with enough context to identify the invalid object/ref. It never returns `False` for invalid state.

- [ ] **Step 1: Write failing provenance tests**

Cover successful and failing cases:

```python
def test_claim_evidence_source_chain_is_valid(): ...
def test_claim_with_missing_evidence_fails_integrity_validation(): ...
def test_claim_subject_must_resolve_to_entity(): ...
def test_evidence_source_must_resolve_to_source(): ...
def test_evidence_support_reference_must_resolve_to_claim(): ...
def test_evidence_contradiction_reference_must_resolve_to_claim(): ...
def test_relationship_subject_and_object_must_resolve(): ...
def test_relationship_evidence_must_resolve_to_evidence(): ...
def test_forward_claim_provenance_is_not_rewritten_from_reverse_links(): ...
```

Use a minimal synthetic fixture built directly in the test file:

```python
def build_valid_provenance_registry():
    registry = CanonicalRegistry()
    source = Source("source-1", "Official Product Documentation", "Vendor", "https://example.com/docs", "official-docs", "2026-08-01", "2026-09-03", "A")
    entity = Entity("product-x", "product", "Product X", "active", {})
    evidence = Evidence("evidence-1", source.canonical_ref, "The documentation states that indexing is supported.", "2026-08-01", "documentation", "A", (CanonicalRef(CanonicalObjectType.CLAIM, "claim-1"),), (), "Direct statement in official documentation.")
    claim = Claim("claim-1", "Product X supports indexing.", entity.canonical_ref, "factual", "active", 0.95, (evidence.canonical_ref,))
    for obj in (source, entity, claim, evidence):
        registry.register(obj)
    return registry
```

Intentionally register incomplete/corrupt states by using private test setup only when needed to exercise registry-wide validation; public registration must not silently repair invalid relationships.

- [ ] **Step 2: Run focused provenance tests and verify failure**

Run:

```bash
pytest tests/unit/research/canonical/test_provenance.py -q
```

Expected: FAIL because provenance validation does not exist.

- [ ] **Step 3: Implement mechanical validation**

Validate the exact semantic targets:

```text
Claim.subject_ref               -> Entity
Claim.evidence_ids              -> Evidence
Evidence.source_id              -> Source
Evidence.supports_claim_ids     -> Claim
Evidence.contradicts_claim_ids  -> Claim
Relationship.subject_ref        -> existing supported canonical object
Relationship.object_ref         -> existing supported canonical object
Relationship.evidence_ids       -> Evidence
```

For Claim provenance, do not infer the forward relationship from Evidence reverse links. `Claim.evidence_ids` is authoritative. The validator may check that a declared reverse link is consistent when present, but it must not mutate either object.

For Relationship endpoints, allow any of the six supported canonical object types unless a later domain contract narrows a predicate; Step 3 does not invent an ontology.

- [ ] **Step 4: Wire registry-wide validation and run focused tests**

Implement:

```python
def validate(self) -> None:
    validate_registry_integrity(self)
```

Run:

```bash
pytest tests/unit/research/canonical/test_provenance.py tests/unit/research/canonical/test_registry.py -q
```

Expected: PASS for valid provenance and all required reference failures.

- [ ] **Step 5: Run the complete suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit the provenance slice**

```bash
git add src/ai_native_workbench/research/canonical/provenance.py src/ai_native_workbench/research/canonical/registry.py tests/unit/research/canonical/test_provenance.py tests/unit/research/canonical/test_registry.py
git commit -m "feat: add canonical referential integrity and provenance validation"
```

---

## 6. Task 5: Enforce Unknown Semantics and Historical Integrity Invariants

**Files:**
- Modify: `src/ai_native_workbench/research/canonical/model.py`
- Modify: `src/ai_native_workbench/research/canonical/provenance.py`
- Modify: `src/ai_native_workbench/research/canonical/registry.py`
- Modify: `tests/unit/research/canonical/test_model.py`
- Modify: `tests/unit/research/canonical/test_provenance.py`
- Modify: `tests/unit/research/canonical/test_registry.py`

**Interfaces:**
- Consumes: validation layer and registry history from Tasks 1–4.
- Produces stronger registry-wide checks without introducing an uncertainty engine.

- [ ] **Step 1: Write failing Unknown and historical integrity tests**

Test the semantic distinction explicitly:

```python
def test_unknown_is_preserved_as_unknown_object():
    unknown = Unknown("unknown-1", "Does Product X support feature Y?", "This affects product selection.", "Product X, current public capabilities", "unresolved")
    assert unknown.object_type is CanonicalObjectType.UNKNOWN
    assert unknown.question != "False"
    assert unknown.status == "unresolved"


def test_empty_unknown_semantics_are_rejected():
    with pytest.raises(CanonicalValidationError):
        Unknown("unknown-1", "", "This matters", "Product X", "unresolved")
```

Add registry integrity tests proving malformed historical state cannot pass validation if a corrupt state is deliberately injected by the test harness, and proving a snapshot-referenced prior object remains recoverable after replacement.

- [ ] **Step 2: Run focused tests and verify failure**

Run:

```bash
pytest tests/unit/research/canonical/test_model.py tests/unit/research/canonical/test_registry.py tests/unit/research/canonical/test_provenance.py -q
```

Expected: FAIL for the new historical and Unknown-specific assertions that are not yet enforced.

- [ ] **Step 3: Implement Unknown semantic checks and historical-state validation**

Keep Unknown as a normal canonical model with mandatory semantic strings; do not add truthiness coercion, sentinel values, or probability.

Extend registry validation so every stored historical object also satisfies intrinsic validation and its cross-object references are mechanically valid. The implementation must be able to report that an invalid historical object is invalid even if it is no longer current.

Do not delete historical states merely because they are superseded.

- [ ] **Step 4: Run focused tests and verify pass**

Run:

```bash
pytest tests/unit/research/canonical/test_model.py tests/unit/research/canonical/test_registry.py tests/unit/research/canonical/test_provenance.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the complete suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit the invariant slice**

```bash
git add src/ai_native_workbench/research/canonical/model.py src/ai_native_workbench/research/canonical/provenance.py src/ai_native_workbench/research/canonical/registry.py tests/unit/research/canonical/test_model.py tests/unit/research/canonical/test_provenance.py tests/unit/research/canonical/test_registry.py
git commit -m "feat: enforce unknown and canonical integrity invariants"
```

---

## 7. Task 6: Implement Immutable ResearchSnapshot Semantics

**Files:**
- Create: `src/ai_native_workbench/research/canonical/snapshot.py`
- Modify: `src/ai_native_workbench/research/canonical/registry.py`
- Modify: `src/ai_native_workbench/research/canonical/__init__.py`
- Create: `tests/unit/research/canonical/test_snapshot.py`

**Interfaces:**
- Consumes: current and historical registry state from Tasks 3–5.
- Produces immutable `ResearchSnapshot` and the registry `snapshot(...)` factory.

Use a frozen dataclass with immutable mapping storage:

```python
@dataclass(frozen=True)
class ResearchSnapshot:
    snapshot_id: str
    case_id: str
    cutoff: str
    workflow_version: str
    schema_version: str
    transformation_version: str
    configuration_hash: str | None
    assumptions_hash: str | None
    status: str
    members: Mapping[CanonicalRef, str]
```

Normalize `members` in `__post_init__` with `MappingProxyType(dict(members))`, reject empty `snapshot_id`, invalid member refs, empty fingerprints, and duplicate logical keys.

Provide:

```python
def fingerprint_for(self, ref: CanonicalRef) -> str: ...
def refs(self) -> tuple[CanonicalRef, ...]: ...
```

These are read-only accessors; no mutation API is provided.

- [ ] **Step 1: Write failing snapshot tests**

Cover:

```python
def test_snapshot_captures_exact_current_fingerprints(): ...
def test_snapshot_members_cannot_be_mutated(): ...
def test_snapshot_missing_ref_is_rejected(): ...
def test_snapshot_unknown_fingerprint_is_rejected(): ...
def test_snapshot_recovers_old_state_after_registry_replace(): ...
def test_current_registry_changes_do_not_change_snapshot_membership(): ...
def test_historical_recovery_uses_get_state_not_get(): ...
```

The critical historical test is:

```python
snapshot = registry.snapshot("s1", (claim.canonical_ref,))
old_fp = snapshot.fingerprint_for(claim.canonical_ref)
registry.replace(claim.canonical_ref, changed_claim)
assert registry.get(claim.canonical_ref) == changed_claim
assert registry.get_state(claim.canonical_ref, old_fp) == claim
assert snapshot.fingerprint_for(claim.canonical_ref) == old_fp
```

- [ ] **Step 2: Run focused snapshot tests and verify failure**

Run:

```bash
pytest tests/unit/research/canonical/test_snapshot.py -q
```

Expected: FAIL because snapshot support does not exist.

- [ ] **Step 3: Implement immutable snapshot creation and recoverability checks**

`CanonicalRegistry.snapshot(...)` must:

1. resolve every requested ref to its current state;
2. capture the current fingerprint for each ref;
3. construct the snapshot from exact ref/fingerprint pairs;
4. verify that every captured fingerprint is recoverable in `_states`;
5. return the immutable snapshot.

Do not store object instances as snapshot membership. Do not resolve a snapshot later by `get(ref)`.

Expose a registry helper or snapshot method that retrieves historical members via `registry.get_state(ref, snapshot.fingerprint_for(ref))`. Keep this explicit so the historical-vs-current distinction remains visible to callers and tests.

- [ ] **Step 4: Run focused tests and verify pass**

Run:

```bash
pytest tests/unit/research/canonical/test_snapshot.py -q
```

Expected: PASS, including immutable membership and historical recovery after replacement.

- [ ] **Step 5: Run the complete suite**

Run:

```bash
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit the snapshot slice**

```bash
git add src/ai_native_workbench/research/canonical/snapshot.py src/ai_native_workbench/research/canonical/registry.py src/ai_native_workbench/research/canonical/__init__.py tests/unit/research/canonical/test_snapshot.py
git commit -m "feat: add immutable research snapshot semantics"
```

---

## 8. Task 7: Build the Synthetic End-to-End Canonical Research Validation Case

**Files:**
- Create: `tests/integration/research/canonical/test_synthetic_research_case.py`
- Modify: `src/ai_native_workbench/research/canonical/__init__.py` only if final public exports are incomplete.

**Interfaces:**
- Consumes: the complete Canonical Core from Tasks 1–6.
- Produces: one executable, Case-001-independent proof that the Step 3 exit condition holds.

The synthetic case must use only local literals and the canonical APIs. It must not import anything from `cases/001-ai-coding-agent-landscape/` or any other case-specific module.

- [ ] **Step 1: Write the failing end-to-end test**

Use this complete synthetic scenario shape:

```python
source = Source(
    id="source-official-1",
    canonical_title="Product X Official Documentation",
    publisher="Example Vendor",
    canonical_url="https://example.com/product-x/docs",
    source_type="official-documentation",
    published_at="2026-08-20",
    accessed_at="2026-09-03",
    quality_tier="A",
)

entity = Entity(
    id="product-x",
    entity_type="product",
    name="Product X",
    status="active",
    attributes={"category": "developer-tool"},
)

evidence_ref = CanonicalRef(CanonicalObjectType.EVIDENCE, "evidence-indexing-1")
claim_ref = CanonicalRef(CanonicalObjectType.CLAIM, "claim-indexing-1")

evidence = Evidence(
    id="evidence-indexing-1",
    source_id=source.canonical_ref,
    observation="The official documentation describes repository indexing support.",
    date_or_period="2026-08-20",
    evidence_type="documentation",
    evidence_grade="A",
    supports_claim_ids=(claim_ref,),
    contradicts_claim_ids=(),
    note="Direct product documentation observation.",
)

claim = Claim(
    id="claim-indexing-1",
    statement="Product X supports repository indexing.",
    subject_ref=entity.canonical_ref,
    claim_type="factual",
    status="active",
    confidence=0.95,
    evidence_ids=(evidence_ref,),
)

unknown = Unknown(
    id="unknown-feature-y",
    question="Does Product X support feature Y?",
    why_it_matters="Feature Y affects the shortlist for a technical selection.",
    scope="Public capabilities as of the synthetic cutoff.",
    status="unresolved",
)

relationship = Relationship(
    id="rel-product-indexing",
    subject_ref=entity.canonical_ref,
    predicate="has_capability",
    object_ref=claim.canonical_ref,
    evidence_ids=(evidence_ref,),
    status="active",
)
```

Register all six objects, call `validate()`, then assert the complete lifecycle:

```python
assert registry.register(entity) == entity.canonical_ref
assert registry.register(entity) == entity.canonical_ref
assert registry.register(claim) == claim.canonical_ref
assert registry.register(evidence) == evidence.canonical_ref
assert registry.register(source) == source.canonical_ref
assert registry.register(unknown) == unknown.canonical_ref
assert registry.register(relationship) == relationship.canonical_ref
registry.validate()

snapshot = registry.snapshot(
    "synthetic-s1",
    (source.canonical_ref, entity.canonical_ref, evidence.canonical_ref,
     claim.canonical_ref, unknown.canonical_ref, relationship.canonical_ref),
    case_id="synthetic-case-001",
    cutoff="2026-09-03",
    workflow_version="synthetic-workflow-v1",
    schema_version="1",
    transformation_version="1",
)
```

Then replace the Claim with changed state, verify a new fingerprint, verify current lookup sees the new state, and verify the old snapshot resolves the exact old Claim through `get_state`.

Finally construct a broken Claim with a missing Evidence ref and assert that `registry.validate()` raises `IntegrityError` rather than silently accepting it.

- [ ] **Step 2: Run the focused integration test and verify failure**

Run:

```bash
pytest tests/integration/research/canonical/test_synthetic_research_case.py -q
```

Expected: FAIL until all preceding Step 3 APIs are wired together.

- [ ] **Step 3: Implement only the minimum missing exports/helpers needed to make the synthetic proof executable**

Do not introduce new infrastructure at this stage. The integration test should work by composing the already-established domain APIs. Any missing export must be added to `canonical/__init__.py`; any missing mechanical helper belongs in its previously designated module rather than in the integration test.

- [ ] **Step 4: Run the focused integration test and verify pass**

Run:

```bash
pytest tests/integration/research/canonical/test_synthetic_research_case.py -q
```

Expected: PASS and the test demonstrates:

```text
stable IDs
→ idempotent registration
→ Claim → Evidence → Source
→ typed references
→ explicit Unknown
→ Relationship
→ exact snapshot fingerprints
→ current-state replacement
→ historical-state recovery
→ mechanical invalid-reference failure
```

- [ ] **Step 5: Run the complete test suite and architecture guardrails**

Run:

```bash
pytest -q
```

Expected: PASS.

Run repository searches:

```bash
grep -R "WorkflowRunner" src/ai_native_workbench/research/canonical

grep -R "cases/001-ai-coding-agent-landscape" tests/integration/research/canonical tests/unit/research/canonical
```

Expected: both searches return no matches. The canonical layer must not import or depend on `WorkflowRunner`, and the synthetic integration test must not reference Case 001.

- [ ] **Step 6: Commit the end-to-end validation slice**

```bash
git add tests/integration/research/canonical/test_synthetic_research_case.py src/ai_native_workbench/research/canonical/__init__.py
git commit -m "test: validate canonical knowledge provenance end to end"
```

---

## 9. Final Verification Matrix

The following checks are part of the plan, not optional cleanup:

| Area | Verification | Expected result |
|---|---|---|
| Identity | `pytest tests/unit/research/canonical/test_identity.py -q` | PASS |
| Models | `pytest tests/unit/research/canonical/test_model.py -q` | PASS |
| Registry | `pytest tests/unit/research/canonical/test_registry.py -q` | PASS |
| Provenance | `pytest tests/unit/research/canonical/test_provenance.py -q` | PASS |
| Snapshot | `pytest tests/unit/research/canonical/test_snapshot.py -q` | PASS |
| Synthetic case | `pytest tests/integration/research/canonical/test_synthetic_research_case.py -q` | PASS |
| Full suite | `pytest -q` | PASS |
| Workflow boundary | grep canonical package for `WorkflowRunner` | no matches |
| Case independence | grep canonical tests for `cases/001` | no matches |

### Required final semantic assertions

The completed implementation must make all of these mechanically true:

```text
1. A canonical object has a stable logical identity independent of state changes.
2. A canonical state has a deterministic sha256 fingerprint.
3. Cross-object references use one typed CanonicalRef format.
4. Factual Claim → Evidence → Source provenance is mechanically validated.
5. Wrong reference types are rejected.
6. Relationship endpoints and evidence references are mechanically validated.
7. Unknown remains a first-class canonical object.
8. The registry does not semantically merge distinct logical IDs.
9. Re-registering the same object state is idempotent.
10. Replacing a logical object creates a new immutable state while retaining history.
11. ResearchSnapshot stores exact ref → fingerprint membership.
12. Snapshot meaning remains unchanged after current registry updates.
13. Historical state is recovered through get_state(ref, fingerprint).
14. Invalid current or historical states fail validation explicitly.
15. The canonical package has no WorkflowRunner dependency.
16. Step 3 contains no Case 001 migration or adapter.
```

---

## 10. Spec Coverage / Self-Review Record

This section is part of the implementation plan so an executor can verify scope before writing code.

### Spec coverage

| Approved Design Spec requirement | Plan coverage |
|---|---|
| Semantic authority vs artifacts | Global Constraints + Architecture + Task 7 |
| Separate Workflow Core and Canonical Registry | Global Constraints + File Structure + Task 7 architecture grep |
| Six first-slice canonical objects | Task 2 |
| Deferred Analysis/Metric/Score/Judgment/Recommendation/Decision/Hypothesis | Global Constraints |
| CanonicalRef `<type>:<logical-id>` | Task 1 |
| Logical identity separate from fingerprint | Tasks 1 and 3 |
| Deterministic serialization | Task 1 |
| No semantic deduplication | Tasks 1 and 3 |
| Claim/Evidence/Source provenance | Tasks 2 and 4 |
| Reverse Evidence links do not silently rewrite forward provenance | Task 4 |
| Contradiction preservation | Global Constraints + Task 4 |
| Relationship reference integrity | Tasks 2 and 4 |
| First-class Unknown semantics | Task 2 + Task 5 |
| Explicit error categories | Task 1 + Task 4 + Task 6 |
| Immutable historical registry states | Task 3 + Task 5 |
| ResearchSnapshot ref → fingerprint | Task 6 |
| Historical snapshot recovery | Task 6 + Task 7 |
| No Case 001 migration | Global Constraints + Task 7 |
| Synthetic end-to-end validation | Task 7 |
| Minimal sufficient engineering | Entire architecture and negative scope |

### Placeholder scan

The plan contains no `TBD`, `TODO`, "implement later", "add appropriate error handling", "write tests for the above", or "similar to Task N" instructions. Every implementation stage names files, interfaces, concrete behaviors, tests, commands, expected outcomes, and commit messages.

### Type/interface consistency

The plan uses one canonical object union throughout:

```python
CanonicalObject = Entity | Claim | Evidence | Source | Unknown | Relationship
```

Every later task consumes the exact public names established by earlier tasks. `CanonicalRegistry.register`, `get`, `get_state`, `replace`, `resolve`, `validate`, and `snapshot` signatures remain stable across Tasks 3–7. Snapshot membership always remains `Mapping[CanonicalRef, str]`, and historical recovery always uses `get_state(ref, fingerprint)`.

---

## 11. Exit Condition

Step 3 is complete only when the implementation and test suite demonstrate:

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

At that point:

- Step 4 remains Evaluation.
- Step 5 remains Reproducible Build + Delivery.
- Step 6 remains Case 001 end-to-end validation.
- Step 7 remains generalization to a second research problem.
- Step 8 remains system revision.
- Step 9 remains automation / Skills / Agentization.

No implementation work in this plan crosses those boundaries.