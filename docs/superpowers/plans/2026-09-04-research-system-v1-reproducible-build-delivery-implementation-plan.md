# Research System v1 — Reproducible Build + Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the minimum reusable Reproducible Build + Delivery Core so one exact `ResearchSnapshot` can produce at least two independently rebuildable delivery forms with explicit build identity, provenance, and evaluation eligibility.

**Architecture:** Add an isolated `research.build` package that treats `ResearchSnapshot` as the only canonical build state, resolves historical members through the existing Step 3 APIs, verifies the existing Step 4 gate, projects the resolved state into delivery-specific views, and renders those views into deterministic machine/narrative outputs. Keep the implementation synchronous, in-memory, and standard-library based; do not introduce a persistent `BuildRun`, artifact registry, renderer registry, storage service, or Case 001 migration.

**Tech Stack:** Python 3.11+, standard-library `dataclasses`, `enum`, `hashlib`, `json`, `csv`, `collections.abc`, `typing`; existing `pytest>=8,<9`; existing Step 3 and Step 4 public APIs; no new runtime dependencies.

**Spec:** `docs/superpowers/specs/2026-09-04-research-system-v1-reproducible-build-delivery-design.md`

## Global Constraints

- **Canonical Model remains the semantic authority; delivery artifacts are projections and must never become a source of truth.**
- Build MUST consume an explicit `ResearchSnapshot`; it MUST NOT use the Registry's current state as an implicit build target.
- Historical snapshot members MUST be resolved with `snapshot.resolve(registry, ref)`, not `registry.get(ref)`.
- Step 3 validation remains the authority for canonical structural/intrinsic integrity; Step 5 MUST reuse it rather than creating a parallel validator.
- Step 4 Quality Gate remains the authority for process eligibility; Step 5 MUST NOT reinterpret or silently bypass a blocking gate outcome.
- Build, projection, and rendering MUST NOT mutate the `CanonicalRegistry`, `ResearchSnapshot`, or canonical objects.
- Build identity MUST include exact snapshot member state, declared versions, configuration, assumptions, projection version, renderer version, and delivery type/format.
- Runtime metadata such as `build_id`, `created_at`, and output path MUST NOT alter semantic build-input identity.
- Reproducibility means equivalent semantic delivery from the same declared state and transformation inputs; byte-for-byte identity is not a universal requirement.
- Projection MUST NOT invent facts, scores, rankings, judgments, or silently resolve `Unknown` / hypotheses.
- Renderer MUST format/serialize an already projected view and MUST NOT perform research inference or hidden external retrieval.
- Delivery editing MUST remain outside canonical authority; edited delivery artifacts MUST NOT be consumed as future canonical build inputs.
- First delivery pair is Dataset Export + Research Note; PPT and HTML remain deferred.
- First implementation is synchronous and in-memory; no persistence, queueing, distributed execution, caching, artifact registry, plugin marketplace, or universal renderer registry.
- Synthetic integration tests MUST construct legal canonical state from literals and MUST NOT import or depend on Case 001.
- All tasks follow TDD: failing test, focused implementation, focused verification, full-suite verification, focused commit.

---

## 1. Implementation Boundary and File Structure

Create the shared Step 5 package under:

```text
src/ai_native_workbench/research/build/
├── __init__.py
├── errors.py
├── model.py
├── projection.py
├── engine.py
└── renderers/
    ├── __init__.py
    ├── dataset.py
    └── research_note.py
```

Create tests under:

```text
tests/unit/research/build/
├── test_model.py
├── test_projection.py
├── test_engine.py
└── test_renderers.py

tests/integration/research/build/
└── test_synthetic_research_build.py
```

Responsibilities:

- `errors.py` — Build-specific exception hierarchy only.
- `model.py` — immutable enums/records for delivery specification, projections, artifacts, and build manifest; no orchestration.
- `projection.py` — deterministic canonical-to-delivery view transformations; no I/O, network, model calls, or renderer behavior.
- `engine.py` — build preconditions, snapshot resolution, gate enforcement, build-input digest, orchestration, and artifact/manifest assembly.
- `renderers/dataset.py` — deterministic structured serialization for the dataset delivery.
- `renderers/research_note.py` — deterministic Markdown serialization for the research-note delivery.
- `__init__.py` files — stable public exports only.

Do not modify Step 3 or Step 4 implementation files unless a missing public export makes a direct integration impossible. Prefer existing public APIs.

---

## 2. Task 1: Establish Immutable Build Contracts

**Files:**
- Create: `src/ai_native_workbench/research/build/__init__.py`
- Create: `src/ai_native_workbench/research/build/errors.py`
- Create: `src/ai_native_workbench/research/build/model.py`
- Create: `tests/unit/research/build/test_model.py`

**Interfaces:**
- Consumes: Step 3 `CanonicalRef`, Step 4 `GateOutcome`, and repository dataclass/testing conventions.
- Produces:
  - `DeliveryType`
  - `BuildStatus`
  - `DeliverySpec`
  - `BuildManifest`
  - `DeliveryArtifact`
  - `BuildError`
  - `BuildValidationError`
  - `BuildPreconditionError`
  - `BuildExecutionError`

- [ ] **Step 1: Write the failing tests**

```python

def test_delivery_spec_is_immutable(): ...
def test_delivery_spec_requires_type_projection_and_renderer_versions(): ...
def test_delivery_spec_rejects_invalid_delivery_type_or_empty_versions(): ...
def test_delivery_spec_configuration_is_immutable(): ...
def test_build_manifest_is_immutable(): ...
def test_build_manifest_records_snapshot_members_and_gate_context(): ...
def test_build_manifest_build_input_digest_is_non_empty(): ...
def test_delivery_artifact_is_immutable(): ...
def test_delivery_artifact_requires_manifest_build_id_match(): ...
def test_delivery_artifact_payload_is_not_mutable(): ...
```

Use actual `CanonicalRef` instances for member maps. Use `MappingProxyType` recursively enough to prevent mutation of nested mappings/lists accepted by the model.

- [ ] **Step 2: Run focused tests to verify failure**

Run:

```bash
pytest tests/unit/research/build/test_model.py -q
```

Expected: FAIL because the Step 5 build package does not yet define these contracts.

- [ ] **Step 3: Implement the exact public vocabulary**

Use these enum values:

```python
class DeliveryType(str, Enum):
    DATASET = "dataset"
    RESEARCH_NOTE = "research_note"

class BuildStatus(str, Enum):
    COMPLETED = "completed"
```

`BuildStatus` is intentionally a single terminal value in v1 because `build()` is a synchronous operation and no persistent run lifecycle is being introduced.

Implement immutable records:

```python
@dataclass(frozen=True)
class DeliverySpec:
    delivery_type: DeliveryType
    format: str
    projection_version: str
    renderer_version: str
    configuration: Mapping[str, object]
```

```python
@dataclass(frozen=True)
class BuildManifest:
    build_id: str
    created_at: str
    snapshot_id: str
    case_id: str
    cutoff: str
    member_fingerprints: Mapping[CanonicalRef, str]
    workflow_version: str
    schema_version: str
    transformation_version: str
    projection_version: str
    renderer_version: str
    delivery_type: DeliveryType
    format: str
    configuration: Mapping[str, object]
    assumptions: Mapping[str, object]
    evaluation_gate_id: str
    evaluation_gate_version: str
    evaluation_outcome: str
    evaluation_run_id: str
    build_input_digest: str
```

```python
@dataclass(frozen=True)
class DeliveryArtifact:
    artifact_id: str
    delivery_type: DeliveryType
    format: str
    build_id: str
    manifest: BuildManifest
    payload: str
    content_digest: str
```

Validation rules:

```text
all text identity/version/timestamp fields are non-empty
DeliverySpec.delivery_type is a DeliveryType
DeliverySpec.configuration is an immutable mapping
BuildManifest.member_fingerprints keys are CanonicalRef values and fingerprints are non-empty strings
BuildManifest.delivery_type/format match the DeliverySpec used to create it
BuildManifest.evaluation_outcome is a declared gate outcome string from Step 4
BuildManifest.build_input_digest is a sha256-form digest string
DeliveryArtifact.manifest.build_id == DeliveryArtifact.build_id
DeliveryArtifact.payload/content_digest are non-empty
```

The build contracts must not embed canonical objects, claims, evidence copies, or renderer implementation details.

- [ ] **Step 4: Implement build-specific errors**

```python
class BuildError(RuntimeError): ...
class BuildValidationError(BuildError): ...
class BuildPreconditionError(BuildError): ...
class BuildExecutionError(BuildError): ...
```

`BuildValidationError` is used for malformed build-layer contracts, `BuildPreconditionError` for a valid contract that cannot legally start from the supplied research state/gate, and `BuildExecutionError` for execution failures after preconditions have been accepted.

- [ ] **Step 5: Export only the public contracts and errors**

`__init__.py` should export exactly the types defined in this task and keep implementation helpers private.

- [ ] **Step 6: Run focused and full tests**

```bash
pytest tests/unit/research/build/test_model.py -q
pytest -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/ai_native_workbench/research/build tests/unit/research/build/test_model.py
git commit -m "feat: add build and delivery contracts"
```

---

## 3. Task 2: Implement Deterministic Snapshot Resolution and Build Input Identity

**Files:**
- Modify: `src/ai_native_workbench/research/build/model.py`
- Modify: `src/ai_native_workbench/research/build/errors.py`
- Create: `src/ai_native_workbench/research/build/engine.py`
- Create: `tests/unit/research/build/test_engine.py`

**Interfaces:**
- Consumes: Task 1 contracts; Step 3 `CanonicalRegistry`, `ResearchSnapshot`, `CanonicalRef`, `canonical_serialize`, `canonical_fingerprint`.
- Produces:
  - `ResolvedSnapshot`
  - `BuildInput`
  - `resolve_snapshot_state(...)`
  - `compute_build_input_digest(...)`

- [ ] **Step 1: Write the failing tests**

```python

def test_resolve_snapshot_uses_historical_fingerprints(): ...
def test_resolve_snapshot_rejects_unrecoverable_member(): ...
def test_resolve_snapshot_does_not_use_current_registry_state(): ...
def test_build_input_digest_is_order_independent_for_mappings(): ...
def test_build_input_digest_changes_when_member_fingerprint_changes(): ...
def test_build_input_digest_changes_when_projection_version_changes(): ...
def test_build_input_digest_changes_when_renderer_version_changes(): ...
def test_build_input_digest_changes_when_configuration_changes(): ...
def test_build_input_digest_changes_when_assumptions_change(): ...
def test_build_input_digest_excludes_build_id_and_created_at(): ...
```

The historical-state test must use `registry.replace(...)` after snapshot creation and assert that snapshot resolution still returns the earlier state.

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/build/test_engine.py -q
```

Expected: FAIL because the resolver and build-input digest do not exist.

- [ ] **Step 3: Define the read-only resolved-state view**

Implement:

```python
@dataclass(frozen=True)
class ResolvedSnapshot:
    snapshot: ResearchSnapshot
    states: Mapping[CanonicalRef, CanonicalObject]
```

The `states` mapping must be immutable. Populate it exclusively with:

```python
for ref in snapshot.refs():
    states[ref] = snapshot.resolve(registry, ref)
```

Do not call `registry.get(ref)` in this code path.

- [ ] **Step 4: Implement explicit build input data**

Implement:

```python
@dataclass(frozen=True)
class BuildInput:
    snapshot_id: str
    case_id: str
    cutoff: str
    member_fingerprints: Mapping[CanonicalRef, str]
    workflow_version: str
    schema_version: str
    transformation_version: str
    delivery_type: DeliveryType
    format: str
    projection_version: str
    renderer_version: str
    configuration: Mapping[str, object]
    assumptions: Mapping[str, object]
```

Do not place `build_id`, `created_at`, output path, or environment metadata in `BuildInput`.

- [ ] **Step 5: Implement deterministic digest calculation**

Implement:

```python
def compute_build_input_digest(build_input: BuildInput) -> str:
    payload = canonical_serialize(build_input)
    return canonical_fingerprint(payload)
```

The implementation must serialize the complete `BuildInput` through the existing deterministic canonical serializer or an equivalent deterministic standard-library normalization. The resulting digest must be independent of mapping insertion order and must include exact `member_fingerprints`.

The digest algorithm must not contain `build_id` or `created_at` because those are runtime metadata rather than semantic input identity.

- [ ] **Step 6: Implement snapshot resolution**

Implement:

```python
def resolve_snapshot_state(
    snapshot: ResearchSnapshot,
    registry: CanonicalRegistry,
) -> ResolvedSnapshot:
    ...
```

Requirements:

1. call `snapshot.validate(registry)` before resolution;
2. resolve each member via `snapshot.resolve(registry, ref)`;
3. return an immutable mapping;
4. propagate a wrapped `BuildPreconditionError` when the snapshot is not recoverable;
5. never mutate the registry or snapshot.

- [ ] **Step 7: Run focused, canonical, and full tests**

```bash
pytest tests/unit/research/build/test_engine.py -q
pytest tests/unit/research/canonical -q
pytest -q
```

Expected: PASS with no Step 3 regressions.

- [ ] **Step 8: Commit**

```bash
git add src/ai_native_workbench/research/build/model.py src/ai_native_workbench/research/build/errors.py src/ai_native_workbench/research/build/engine.py tests/unit/research/build/test_engine.py
git commit -m "feat: add snapshot-bound build identity"
```

---

## 4. Task 3: Define the Projection Boundary and Two Minimal Delivery Views

**Files:**
- Create: `src/ai_native_workbench/research/build/projection.py`
- Create: `tests/unit/research/build/test_projection.py`
- Modify: `src/ai_native_workbench/research/build/__init__.py`

**Interfaces:**
- Consumes: Task 2 `ResolvedSnapshot`, `BuildInput`, Step 3 canonical object classes.
- Produces:
  - `DatasetRow`
  - `DatasetProjection`
  - `ResearchNoteSection`
  - `ResearchNoteProjection`
  - `project_dataset(...)`
  - `project_research_note(...)`

- [ ] **Step 1: Write the failing tests**

```python

def test_dataset_projection_preserves_canonical_identity(): ...
def test_dataset_projection_preserves_provenance_references(): ...
def test_dataset_projection_preserves_unknown_objects(): ...
def test_dataset_projection_uses_snapshot_state_not_registry_current_state(): ...
def test_research_note_projection_contains_only_projected_canonical_content(): ...
def test_research_note_projection_preserves_unknowns_and_qualification(): ...
def test_projection_is_deterministic_for_same_resolved_snapshot(): ...
def test_projection_does_not_mutate_input_objects(): ...
def test_projection_does_not_introduce_untracked_semantic_fields(): ...
```

Use a synthetic legal snapshot containing at least one Entity, factual Claim, Evidence, Source, and Unknown. Include a replacement after snapshot creation to prove that projections remain snapshot-bound.

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/build/test_projection.py -q
```

Expected: FAIL because projection contracts do not exist.

- [ ] **Step 3: Define immutable delivery-view records**

Implement:

```python
@dataclass(frozen=True)
class DatasetRow:
    ref: CanonicalRef
    object_type: str
    logical_id: str
    fields: Mapping[str, object]
```

```python
@dataclass(frozen=True)
class DatasetProjection:
    version: str
    rows: tuple[DatasetRow, ...]
```

```python
@dataclass(frozen=True)
class ResearchNoteSection:
    heading: str
    paragraphs: tuple[str, ...]
    refs: tuple[CanonicalRef, ...]
```

```python
@dataclass(frozen=True)
class ResearchNoteProjection:
    version: str
    sections: tuple[ResearchNoteSection, ...]
```

- [ ] **Step 4: Implement the deterministic dataset projection**

Use the minimal canonical flattening rules:

```text
Entity   -> id/name/entity_type/status + selected attributes
Claim    -> id/statement/claim_type/status/confidence + evidence refs + subject ref
Evidence -> id/observation/date_or_period/evidence_type/evidence_grade + source/claim refs
Source   -> id/canonical_title/publisher/canonical_url/source_type/published_at/accessed_at/quality_tier
Unknown  -> id/question/why_it_matters/scope/status
Relationship -> id/subject_ref/predicate/object_ref/status + evidence refs
```

Represent references as their existing canonical wire form `str(ref)`. Preserve Unknown as an explicit object row rather than translating it into null/false/zero.

Sort rows by `str(ref)` so projection order is deterministic and independent of registry insertion order.

Do not add derived rankings, scores, inferred booleans, or semantic summaries.

- [ ] **Step 5: Implement the deterministic research-note projection**

Produce exactly these first-slice sections:

```text
Research Context
Key Findings
Unknowns / Limitations
Provenance
```

Rules:

- `Research Context` contains case id, cutoff, and snapshot id supplied by the build state.
- `Key Findings` contains only factual Claims present in the resolved snapshot, ordered by canonical ref, with their statement and explicit evidence references.
- `Unknowns / Limitations` contains Unknown objects, ordered by canonical ref, preserving question and why-it-matters text.
- `Provenance` contains Source records referenced by selected Claims/Evidence, ordered by canonical ref, preserving source title and canonical URL.

Do not synthesize judgments or recommendations that are not represented in canonical objects. Do not silently omit an Unknown merely because it makes the narrative less convenient.

- [ ] **Step 6: Prove projection purity**

No projection function may accept or read a mutable global registry. The only canonical state input is the immutable `ResolvedSnapshot.states` plus explicit snapshot metadata.

- [ ] **Step 7: Run focused and full tests**

```bash
pytest tests/unit/research/build/test_projection.py -q
pytest -q
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/ai_native_workbench/research/build/projection.py src/ai_native_workbench/research/build/__init__.py tests/unit/research/build/test_projection.py
git commit -m "feat: add deterministic delivery projections"
```

---

## 5. Task 4: Implement Deterministic Dataset and Research Note Renderers

**Files:**
- Create: `src/ai_native_workbench/research/build/renderers/__init__.py`
- Create: `src/ai_native_workbench/research/build/renderers/dataset.py`
- Create: `src/ai_native_workbench/research/build/renderers/research_note.py`
- Create: `tests/unit/research/build/test_renderers.py`
- Modify: `src/ai_native_workbench/research/build/__init__.py`

**Interfaces:**
- Consumes: Task 3 projections only.
- Produces:
  - `render_dataset_json(...)`
  - `render_dataset_csv(...)`
  - `render_research_note_markdown(...)`

- [ ] **Step 1: Write the failing tests**

```python

def test_dataset_json_render_is_deterministic(): ...
def test_dataset_json_contains_only_projected_rows(): ...
def test_dataset_csv_render_has_stable_header_and_order(): ...
def test_research_note_markdown_has_declared_sections(): ...
def test_research_note_markdown_preserves_unknowns(): ...
def test_renderers_do_not_add_untracked_content(): ...
def test_renderers_produce_stable_output_for_same_projection(): ...
```

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/build/test_renderers.py -q
```

Expected: FAIL because renderer functions do not exist.

- [ ] **Step 3: Implement Dataset JSON rendering**

Implement:

```python
def render_dataset_json(projection: DatasetProjection) -> str:
    ...
```

Render a JSON object with:

```json
{
  "projection_version": "...",
  "rows": [ ... ]
}
```

Use `ensure_ascii=False`, sorted object keys, compact separators, and stable row ordering already guaranteed by projection.

- [ ] **Step 4: Implement Dataset CSV rendering**

Implement:

```python
def render_dataset_csv(projection: DatasetProjection) -> str:
    ...
```

Use a fixed header:

```text
ref,object_type,logical_id,fields_json
```

Serialize `fields` using the same deterministic JSON normalization used elsewhere. Use `csv.DictWriter` with `\n` line endings. Do not include timestamps or runtime metadata in the payload.

- [ ] **Step 5: Implement Research Note Markdown rendering**

Implement:

```python
def render_research_note_markdown(projection: ResearchNoteProjection) -> str:
    ...
```

Use exactly one `# Research Note` title followed by each declared section as `## <heading>`. Each paragraph is emitted verbatim after projection. When `refs` are present, append one provenance reference line per ref using their canonical wire form.

Do not compute new claims, conclusions, or summaries in the renderer.

- [ ] **Step 6: Run focused and full tests**

```bash
pytest tests/unit/research/build/test_renderers.py -q
pytest -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/ai_native_workbench/research/build/renderers src/ai_native_workbench/research/build/__init__.py tests/unit/research/build/test_renderers.py
git commit -m "feat: add dataset and research note renderers"
```

---

## 6. Task 5: Integrate Evaluation Gate, Build Orchestration, and Manifest Assembly

**Files:**
- Modify: `src/ai_native_workbench/research/build/engine.py`
- Modify: `src/ai_native_workbench/research/build/model.py`
- Modify: `src/ai_native_workbench/research/build/errors.py`
- Modify: `src/ai_native_workbench/research/build/__init__.py`
- Create: `tests/unit/research/build/test_engine.py` additions

**Interfaces:**
- Consumes: Tasks 1–4; Step 3 `CanonicalRegistry`/`ResearchSnapshot`; Step 4 `QualityGateEvaluation` and `GateOutcome`.
- Produces:
  - `BuildResult`
  - `build_delivery(...)`
  - `create_build_manifest(...)`

- [ ] **Step 1: Write the failing orchestration tests**

```python

def test_build_rejects_unrecoverable_snapshot(): ...
def test_build_rejects_non_pass_quality_gate(): ...
def test_build_requires_declared_configuration_and_assumptions(): ...
def test_build_creates_manifest_with_exact_snapshot_fingerprints(): ...
def test_build_manifest_records_gate_identity_and_run_id(): ...
def test_build_identity_excludes_runtime_metadata(): ...
def test_build_returns_delivery_artifact_with_matching_manifest(): ...
def test_build_does_not_mutate_registry_snapshot_or_canonical_objects(): ...
def test_build_uses_selected_renderer_for_selected_delivery_type(): ...
```

Use a completed Step 4 `QualityGateEvaluation` with `PASS` for the happy path and `REVIEW`/`FAIL` for rejected paths. Do not fake canonical-invalid state to demonstrate a build failure.

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/build/test_engine.py -q
```

Expected: FAIL because build orchestration does not exist.

- [ ] **Step 3: Define the build result record**

Implement:

```python
@dataclass(frozen=True)
class BuildResult:
    status: BuildStatus
    artifact: DeliveryArtifact
```

A successful synchronous build always returns `BuildStatus.COMPLETED`. Exceptions represent failed builds; do not add a persistent failed-run record.

- [ ] **Step 4: Implement manifest construction**

Implement:

```python
def create_build_manifest(
    *,
    build_id: str,
    created_at: str,
    snapshot: ResearchSnapshot,
    delivery_spec: DeliverySpec,
    assumptions: Mapping[str, object],
    gate: QualityGateEvaluation,
    build_input_digest: str,
) -> BuildManifest:
    ...
```

Populate:

```text
snapshot_id
case_id
cutoff
member_fingerprints
workflow_version
schema_version
transformation_version
projection_version
renderer_version
delivery_type
format
configuration
assumptions
evaluation_gate_id
evaluation_gate_version
evaluation_outcome
evaluation_run_id
build_input_digest
```

Use snapshot metadata for workflow/schema/transformation version fields; do not create duplicate version systems.

- [ ] **Step 5: Implement delivery dispatch without a global registry**

Implement private functions that dispatch on the finite v1 enum values:

```python
if delivery_spec.delivery_type is DeliveryType.DATASET:
    projection = project_dataset(resolved)
    payload = render_dataset_json(projection)  # or CSV when format == "csv"
elif delivery_spec.delivery_type is DeliveryType.RESEARCH_NOTE:
    projection = project_research_note(resolved)
    payload = render_research_note_markdown(projection)
else:
    raise BuildValidationError(...)
```

Do not introduce a plugin registry. The finite v1 delivery set is intentionally explicit.

- [ ] **Step 6: Implement `build_delivery(...)`**

Implement:

```python
def build_delivery(
    *,
    snapshot: ResearchSnapshot,
    registry: CanonicalRegistry,
    delivery_spec: DeliverySpec,
    assumptions: Mapping[str, object],
    gate: QualityGateEvaluation,
    build_id: str,
    created_at: str,
) -> BuildResult:
    ...
```

Execution order MUST be:

```text
validate snapshot/recoverability
→ require gate PASS
→ resolve snapshot state
→ construct BuildInput
→ compute build-input digest
→ project
→ render
→ create manifest
→ create content digest
→ create DeliveryArtifact
```

Build preconditions:

1. `snapshot.validate(registry)` succeeds;
2. every snapshot member is recoverable at the recorded fingerprint;
3. `gate.outcome is GateOutcome.PASS`;
4. `delivery_spec.configuration` is declared, even when empty;
5. `assumptions` is declared, even when empty;
6. delivery type/format combination is supported.

A gate outcome of `REVIEW` or `FAIL` MUST raise `BuildPreconditionError`; do not produce a partial delivery artifact.

- [ ] **Step 7: Compute artifact content digest**

Use:

```python
content_digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

The digest is a property of the rendered artifact payload only. It is not the build-input identity.

- [ ] **Step 8: Run focused, Step 3, Step 4, and full tests**

```bash
pytest tests/unit/research/build/test_engine.py -q
pytest tests/unit/research/canonical -q
pytest tests/unit/research/evaluation -q
pytest -q
```

Expected: PASS.

- [ ] **Step 9: Commit**

```bash
git add src/ai_native_workbench/research/build tests/unit/research/build/test_engine.py
git commit -m "feat: integrate gated reproducible build"
```

---

## 7. Task 6: Add Audit Manifest Projection and Validation Package

**Files:**
- Modify: `src/ai_native_workbench/research/build/model.py`
- Modify: `src/ai_native_workbench/research/build/engine.py`
- Create: `tests/unit/research/build/test_audit.py`
- Modify: `src/ai_native_workbench/research/build/__init__.py`

**Interfaces:**
- Consumes: `BuildManifest`, `DeliveryArtifact`, Step 4 gate evaluation references.
- Produces:
  - `AuditManifest`
  - `build_audit_manifest(...)`

- [ ] **Step 1: Write the failing audit tests**

```python

def test_audit_manifest_is_derived_only_from_build_manifest(): ...
def test_audit_manifest_contains_snapshot_members_and_versions(): ...
def test_audit_manifest_contains_evaluation_reference(): ...
def test_audit_manifest_contains_delivery_reference_and_digest(): ...
def test_audit_manifest_is_deterministic_for_same_build_manifest(): ...
def test_audit_manifest_does_not_embed_duplicate_canonical_objects(): ...
```

- [ ] **Step 2: Run focused tests to verify failure**

```bash
pytest tests/unit/research/build/test_audit.py -q
```

Expected: FAIL because `AuditManifest` does not exist.

- [ ] **Step 3: Implement the minimum audit record**

Implement:

```python
@dataclass(frozen=True)
class AuditManifest:
    build_manifest: BuildManifest
    artifact_id: str
    content_digest: str
```

This intentionally embeds the already-defined build manifest rather than creating a second copy of every field under different names.

- [ ] **Step 4: Implement deterministic audit serialization**

Implement:

```python
def build_audit_manifest(artifact: DeliveryArtifact) -> AuditManifest:
    ...
```

The returned manifest must allow a reviewer to answer:

```text
which snapshot?
which exact member fingerprints?
which versions?
which configuration/assumptions?
which gate/run?
which delivery type/format?
which build-input digest?
which artifact digest?
```

Do not include canonical object payloads, evidence copies, or delivery text in the audit manifest.

- [ ] **Step 5: Run focused and full tests**

```bash
pytest tests/unit/research/build/test_audit.py -q
pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/ai_native_workbench/research/build tests/unit/research/build/test_audit.py
 git commit -m "feat: add build audit manifest"
```

---

## 8. Task 7: Prove the Complete Synthetic Reproducibility Flow

**Files:**
- Create: `tests/integration/research/build/test_synthetic_research_build.py`

**Interfaces:**
- Consumes: complete Tasks 1–6 plus real Step 3 and Step 4 APIs.
- Produces: integration proof of `PASS`-gated Dataset + Research Note delivery, historical-state correctness, audit traceability, and rebuild semantics.

- [ ] **Step 1: Write independent legal synthetic scenarios**

Construct a canonical registry entirely from literals using:

```text
Source
Entity
Evidence
factual Claim
Unknown
Relationship
ResearchSnapshot
```

Create a factual Claim with explicitly supporting Evidence and a completed Step 4 `EvaluationRun`/`QualityGateEvaluation` that yields `PASS` for the delivery path.

Do not import any file from `cases/001-ai-coding-agent-landscape/`.

- [ ] **Step 2: Prove one snapshot generates two delivery forms**

Build both:

```text
DeliveryType.DATASET
DeliveryType.RESEARCH_NOTE
```

using exactly the same `ResearchSnapshot`, Registry, configuration, assumptions, and gate.

Assert:

```text
same snapshot_id
same member_fingerprints
same build-input semantics
separate delivery types
separate artifacts
```

- [ ] **Step 3: Prove historical state recovery**

After creating the snapshot:

```python
claim_v1 = registry.get(claim_ref)
registry.replace(claim_ref, claim_v2)
```

Then assert:

```python
registry.get(claim_ref) == claim_v2
snapshot.resolve(registry, claim_ref) == claim_v1
```

Build again from the same snapshot and assert the delivery contains v1 semantics, not v2 semantics.

- [ ] **Step 4: Prove rebuild equivalence**

Run two Dataset builds with:

```text
same snapshot
same delivery spec
same configuration
same assumptions
same gate
```

Use different runtime `build_id` and `created_at` values. Assert:

```text
build_input_digest is identical
projection semantics are identical
payload is identical for the deterministic dataset renderer
content_digest is identical for the deterministic dataset renderer
```

This proves strong deterministic behavior where v1 can cheaply guarantee it without making binary artifacts a universal contract.

- [ ] **Step 5: Prove build identity changes when canonical state changes**

Create a second snapshot with a changed Claim state and a new member fingerprint. Build it with the same delivery spec/configuration/assumptions and assert:

```text
snapshot member fingerprints differ
build_input_digest differs
```

Do not modify the original snapshot.

- [ ] **Step 6: Prove gate enforcement**

Run builds with:

```text
Gate = PASS  -> delivery succeeds
Gate = REVIEW -> BuildPreconditionError
Gate = FAIL   -> BuildPreconditionError
```

Assert no partial `DeliveryArtifact` is created for the rejected paths.

- [ ] **Step 7: Prove mutation safety**

Take stable serialized/fingerprint representations of:

```text
input ResearchSnapshot
registry current states
registry historical states
canonical objects
input gate evaluation
```

Build both deliveries and assert all remain unchanged.

- [ ] **Step 8: Prove audit traceability**

Create the audit manifest from each artifact and assert it records:

```text
snapshot_id
member_fingerprints
versions
configuration
assumptions
gate identity/outcome
build_input_digest
artifact_id
content_digest
```

Also assert it does not contain embedded canonical object payloads.

- [ ] **Step 9: Run the integration and full verification matrix**

```bash
pytest tests/integration/research/build/test_synthetic_research_build.py -q
pytest tests/unit/research/build -q
pytest tests/unit/research/canonical -q
pytest tests/integration/research/canonical -q
pytest tests/unit/research/evaluation -q
pytest tests/integration/research/evaluation -q
pytest -q
```

Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add tests/integration/research/build/test_synthetic_research_build.py
 git commit -m "test: prove reproducible multi-delivery build"
```

---

## 9. Task 8: Final API Review, Documentation Alignment, and Global Verification

**Files:**
- Modify: `src/ai_native_workbench/research/build/__init__.py` only if exports changed during implementation.
- Modify: `docs/superpowers/specs/2026-09-04-research-system-v1-reproducible-build-delivery-design.md` only when implementation reveals an actual contract mismatch that must be documented.
- Modify: `docs/superpowers/plans/2026-09-04-research-system-v1-reproducible-build-delivery-implementation-plan.md` only to mark completed tasks when implementation is actually performed.
- Create/modify: Step 5 unit/integration tests only for regression coverage discovered during verification.

**Interfaces:**
- Consumes: complete Step 5 implementation.
- Produces: verified public API and a passing Step-level test matrix.

- [ ] **Step 1: Inspect the public package boundary**

Verify that `research.build.__init__` exposes only the intended contracts/functions:

```text
BuildError
BuildValidationError
BuildPreconditionError
BuildExecutionError
DeliveryType
BuildStatus
DeliverySpec
BuildInput
ResolvedSnapshot
BuildManifest
DeliveryArtifact
AuditManifest
DatasetProjection
ResearchNoteProjection
build_delivery
create_build_manifest
build_audit_manifest
resolve_snapshot_state
compute_build_input_digest
project_dataset
project_research_note
render_dataset_json
render_dataset_csv
render_research_note_markdown
```

Do not export private implementation helpers.

- [ ] **Step 2: Scan for prohibited architecture**

Search the Step 5 code for:

```text
sqlite
sqlalchemy
redis
celery
queue
asyncio
httpx
requests
plugin registry
artifact registry
BuildRun
current registry lookup inside projection/renderer
Case 001 imports
```

The v1 implementation must not introduce these capabilities.

- [ ] **Step 3: Verify canonical authority boundary**

Inspect all Step 5 code and ensure no function:

```text
mutates canonical objects;
registers/replaces canonical objects;
rewrites snapshot membership;
creates a second canonical reference namespace;
converts Unknown into a confirmed answer;
creates canonical facts from delivery content.
```

- [ ] **Step 4: Verify evaluation boundary**

Ensure Step 5 only consumes Step 4 gate results and does not:

```text
recompute heterogeneous quality scores;
override FAIL to PASS;
reinterpret REVIEW as PASS;
create a second gate state machine.
```

- [ ] **Step 5: Run the global verification matrix**

```bash
pytest tests/unit/research/workflow -q
pytest tests/unit/research/canonical -q
pytest tests/integration/research/canonical -q
pytest tests/unit/research/evaluation -q
pytest tests/integration/research/evaluation -q
pytest tests/unit/research/build -q
pytest tests/integration/research/build -q
pytest -q
```

Expected: PASS with no regressions in Steps 1–4.

- [ ] **Step 6: Commit final verification changes**

```bash
git add src/ai_native_workbench/research/build tests/unit/research/build tests/integration/research/build docs/superpowers/specs/2026-09-04-research-system-v1-reproducible-build-delivery-design.md docs/superpowers/plans/2026-09-04-research-system-v1-reproducible-build-delivery-implementation-plan.md
 git commit -m "test: verify research build and delivery core"
```

Only include documentation modifications in this commit when they are evidence-backed corrections required by the implemented contract; do not rewrite Step 1–4 methodology for cosmetic alignment.

---

## 10. Task Dependency and Review Boundaries

The intended dependency chain is:

```text
Task 1
Build contracts
    ↓
Task 2
Snapshot resolution + identity
    ↓
Task 3
Projection boundary
    ↓
Task 4
Renderers
    ↓
Task 5
Gate + build orchestration
    ↓
Task 6
Audit manifest
    ↓
Task 7
Synthetic end-to-end proof
    ↓
Task 8
Global verification
```

Each task is independently reviewable after its focused test suite passes. A reviewer should be able to reject a task without invalidating the semantic work of earlier tasks.

No task should modify Step 3 canonical semantics simply to simplify delivery implementation.

---

## 11. Step 5 Exit Criteria

Step 5 is complete only when all of the following are true:

1. A historical `ResearchSnapshot` can be resolved without consulting current canonical state as a substitute for its captured fingerprints.
2. Build-input identity is deterministic and includes the exact canonical member state plus delivery/transformation inputs, while excluding runtime metadata.
3. Step 4 `GateOutcome.PASS` is required before delivery generation.
4. Dataset and Research Note deliveries are produced from the same canonical snapshot but through separate projections.
5. Neither renderer is responsible for semantic research decisions.
6. Unknown and provenance references remain explicit in both delivery forms where applicable.
7. Rebuild with the same declared inputs produces semantically equivalent delivery; the deterministic v1 renderers additionally produce byte-identical payloads.
8. A changed canonical snapshot state produces a different build-input identity.
9. Human edits to delivery artifacts are outside the canonical input path.
10. The audit manifest explains snapshot, exact state, versions, configuration, assumptions, evaluation gate, build identity, and artifact identity without duplicating canonical content.
11. All Step 1–4 tests remain green.
12. Case 001 legacy files are not imported into the generic build implementation.
13. No persistent build/artifact infrastructure has been introduced without demonstrated need.

The result should satisfy:

```text
One Canonical Research State
        ↓
┌───────────────┬──────────────────┐
↓               ↓
Dataset       Research Note
└───────────────┴──────────────────┘
                ↓
         Audit / Manifest
```

and preserve the architectural invariant:

> **Delivery artifacts are projections of canonical research knowledge; they are not independently authored research sources.**
