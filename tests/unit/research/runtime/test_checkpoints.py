"""Tests for Checkpoint persistence, exact validation and downstream
invalidation (Spec 12, Task 3).

Covers the brief Step 6/7 assertions: a Checkpoint stores only committed
Artifact references plus exact compatibility metadata (never serialized
process state), reuse requires exact compatibility on every dimension,
validation re-checks the durable evidence (missing documents and digest
tampering fail as EvidenceIntegrityError), and invalidating a rerun Step
history is append-only: CHECKPOINT_INVALIDATED events are recorded, prior
records are never deleted or rewritten, and already invalidated checkpoints
are left untouched.
"""

import json
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    ArtifactEnvelope,
    CaseBinding,
    CheckpointRecord,
    CompatibilityIdentity,
    EntryMode,
    EventEnvelope,
    EventType,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.artifacts import (
    ArtifactNotCommittedError,
    commit_artifact,
)
from ai_native_workbench.research.runtime.checkpoints import (
    create_checkpoint,
    invalidate_downstream,
    validate_checkpoint,
)
from ai_native_workbench.research.runtime.store import (
    EvidenceIntegrityError,
    FileSystemRuntimeStore,
    RunNotFoundError,
    reduce_events,
)
from ai_native_workbench.research.workflow.composition import (
    LifecycleStage,
    WorkflowDefinition,
    WorkflowNode,
)
from ai_native_workbench.research.workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    WorkflowStep,
)

CASE_ID = "case-1"
CASE_ID_2 = "case-2"
RUN_ID = "run-1"
RUN_ID_2 = "run-2"
INVOCATION_ID = "inv-1"
INVOCATION_ID_2 = "inv-2"
STEP_ID = "R1"
TS = "2026-09-09T08:00:00+00:00"

STEP_PAYLOAD = {"kind": "evidence-set", "rows": [{"step": "R"}]}
COMMIT_DIGEST = "sha256:" + "d" * 64


# ---------------------------------------------------------------------------
# Shared fixtures/helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def make_store(tmp_path) -> FileSystemRuntimeStore:
    return FileSystemRuntimeStore(tmp_path)


def _case_binding(case_id: str) -> CaseBinding:
    return CaseBinding(
        case_id=case_id,
        charter_identity="charter-001",
        charter_digest="sha256:" + "a" * 64,
        source_declaration_identity="urls-001",
        source_declaration_digest="sha256:" + "b" * 64,
    )


def make_run_record(run_id: str = RUN_ID, case_id: str = CASE_ID, **overrides) -> RunRecord:
    defaults = dict(
        run_id=run_id,
        case_id=case_id,
        case_binding=_case_binding(case_id),
        state=RunState.CREATED,
        cumulative_execution_scope=(),
        current_invocation_id=None,
        completion_reason=None,
    )
    defaults.update(overrides)
    return RunRecord(**defaults)


def evt(kind: EventType, event_id: str, **overrides) -> EventEnvelope:
    return replace(
        EventEnvelope(
            event_id=event_id,
            event_type=kind,
            timestamp=TS,
            run_id=RUN_ID,
            payload={},
        ),
        **overrides,
    )


def invocation_started_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    payload: dict | None = None,
    **kw,
):
    if payload is None:
        payload = {
            "requested_scope": ["R1"],
            "entry_mode": EntryMode.START.value,
            "execution_binding": {
                "workflow_identity": "research-workflow",
                "workflow_version": "v1",
                "runtime_configuration_identity": "runtime-config-001",
                "prompts": {},
                "schemas": {},
            },
        }
    return evt(
        EventType.INVOCATION_STARTED,
        f"evt-{run_id}-inv-1",
        run_id=run_id,
        invocation_id=invocation_id,
        payload=payload,
        **kw,
    )


def attempt_created_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = "att-1",
    **kw,
):
    return evt(
        EventType.ATTEMPT_CREATED,
        f"evt-{run_id}-{attempt_id}-created",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        **kw,
    )


def input_bound_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = "att-1",
    payload: dict | None = None,
    **kw,
):
    if payload is None:
        payload = {
            "input_binding_id": f"ib-{attempt_id}",
            "artifact_ids": [],
            "upstream_attempt_ids": [],
        }
    return evt(
        EventType.INPUT_BOUND,
        f"evt-{run_id}-{attempt_id}-bound",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        payload=payload,
        **kw,
    )


def attempt_started_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = "att-1",
    **kw,
):
    return evt(
        EventType.ATTEMPT_STARTED,
        f"evt-{run_id}-{attempt_id}-started",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        **kw,
    )


def attempt_succeeded_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = "att-1",
    **kw,
):
    return evt(
        EventType.ATTEMPT_SUCCEEDED,
        f"evt-{run_id}-{attempt_id}-succeeded",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        **kw,
    )


def invalidated_event(checkpoint: CheckpointRecord, **kw):
    return evt(
        EventType.CHECKPOINT_INVALIDATED,
        f"evt-{checkpoint.run_id}-{checkpoint.checkpoint_id}-invalidated",
        run_id=checkpoint.run_id,
        step_id=checkpoint.step_id,
        payload={"checkpoint_id": checkpoint.checkpoint_id},
        **kw,
    )


def make_artifact(artifact_id: str = "art-1", **overrides) -> ArtifactEnvelope:
    defaults = dict(
        artifact_id=artifact_id,
        run_id=RUN_ID,
        invocation_id=INVOCATION_ID,
        artifact_schema_id="evidence-set",
        artifact_schema_version="1",
        created_at=TS,
        step_id="R1",
        attempt_id="att-1",
    )
    defaults.update(overrides)
    return ArtifactEnvelope(**defaults)


def make_compat(step_id: str = STEP_ID, **overrides) -> CompatibilityIdentity:
    defaults = dict(
        workflow_identity="research-standard",
        workflow_version="1.0.0",
        step_identity=step_id,
        step_version="1",
        runtime_configuration_identity="runtime-config-001",
    )
    defaults.update(overrides)
    return CompatibilityIdentity(**defaults)


def make_checkpoint(checkpoint_id: str, **overrides) -> CheckpointRecord:
    defaults = dict(
        checkpoint_id=checkpoint_id,
        run_id=RUN_ID,
        step_id=STEP_ID,
        artifact_ids=("art-1",),
        compatibility=make_compat(),
        created_at=TS,
    )
    defaults.update(overrides)
    return CheckpointRecord(**defaults)


def start_invocation(
    store,
    *,
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    scope: tuple = ("R1",),
) -> None:
    store.create_run(make_run_record(run_id=run_id))
    store.append_event(
        invocation_started_event(
            run_id=run_id,
            invocation_id=invocation_id,
            payload={
                "requested_scope": list(scope),
                "entry_mode": EntryMode.START.value,
                "execution_binding": {
                    "workflow_identity": "research-workflow",
                    "workflow_version": "v1",
                    "runtime_configuration_identity": "runtime-config-001",
                    "prompts": {},
                    "schemas": {},
                },
            },
        )
    )


def run_successful_step(
    store,
    *,
    step_id: str,
    attempt_id: str,
    artifact_id: str,
    previous_artifact_id: str | None = None,
) -> None:
    """Execute one step to ATTEMPT_SUCCEEDED and commit its output artifact."""
    store.append_event(attempt_created_event(step_id=step_id, attempt_id=attempt_id))
    artifacts = [previous_artifact_id] if previous_artifact_id else []
    store.append_event(
        input_bound_event(
            step_id=step_id,
            attempt_id=attempt_id,
            payload={
                "input_binding_id": f"ib-{attempt_id}",
                "artifact_ids": artifacts,
                "upstream_attempt_ids": [],
            },
        )
    )
    store.append_event(attempt_started_event(step_id=step_id, attempt_id=attempt_id))
    commit_artifact(
        store,
        make_artifact(artifact_id, step_id=step_id, attempt_id=attempt_id),
        STEP_PAYLOAD,
    )
    store.append_event(attempt_succeeded_event(step_id=step_id, attempt_id=attempt_id))


def execute_chain(store, steps: tuple = ("R1", "R2", "R3", "R4")) -> tuple:
    """Execute *steps* sequentially, committing one artifact per step and
    returning the committed artifact ids in order."""
    start_invocation(store, scope=steps)
    accumulated = []
    for index, step_id in enumerate(steps):
        attempt_id = f"att-{index + 1}"
        artifact_id = f"art-{index + 1}"
        run_successful_step(
            store,
            step_id=step_id,
            attempt_id=attempt_id,
            artifact_id=artifact_id,
            previous_artifact_id=accumulated[-1] if accumulated else None,
        )
        accumulated.append(artifact_id)
    return tuple(accumulated)


def build_checkpointed_chain(
    store, steps: tuple = ("R1", "R2", "R3", "R4")
) -> tuple:
    """execute_chain plus one VALID checkpoint per step, created after each
    step's success; returns the created checkpoint records in order."""
    artifacts = execute_chain(store, steps=steps)
    checkpoints = []
    for index, step_id in enumerate(steps):
        checkpoint = make_checkpoint(
            f"cp-{index + 1}",
            step_id=step_id,
            artifact_ids=artifacts[: index + 1],
            compatibility=make_compat(step_id=step_id),
        )
        create_checkpoint(store, checkpoint)
        checkpoints.append(checkpoint)
    return tuple(checkpoints)


def make_step(step_id: str) -> WorkflowStep:
    return WorkflowStep(
        id=step_id,
        name=f"Synthetic {step_id}",
        version="1",
        purpose="synthetic workflow step for checkpoint invalidation tests",
        inputs=(StepInput(name="sources", kind="evidence-set"),),
        outputs=(StepOutput(name="output", kind="evidence-set"),),
        preconditions=(),
        method=("execute",),
        constraints=("none",),
        human_gate=GateRequirement(required=False, gate_type=None),
        validation=(),
        provenance=ProvenanceRequirement(required=False, rules=()),
    )


def make_chain_workflow() -> WorkflowDefinition:
    """R1 -> R2 -> R3 chain plus an independent R4 (edges R1:(), R2:(R1,),
    R3:(R2,), R4:())."""
    nodes = tuple(
        WorkflowNode(step=make_step(step_id), depends_on=depends_on)
        for step_id, depends_on in (
            ("R1", ()),
            ("R2", ("R1",)),
            ("R3", ("R2",)),
            ("R4", ()),
        )
    )
    stages = {step_id: LifecycleStage.R1_DISCOVER for step_id in ("R1", "R2", "R3", "R4")}
    return WorkflowDefinition(
        id="research-standard",
        version="1.0.0",
        steps=nodes,
        lifecycle_stage_map=stages,
    )


def checkpoint_events(store, run_id: str = RUN_ID) -> tuple:
    return tuple(
        event
        for event in store.events(run_id)
        if event.event_type is EventType.CHECKPOINT_CREATED
    )


def invalidated_events(store, run_id: str = RUN_ID) -> tuple:
    return tuple(
        event
        for event in store.events(run_id)
        if event.event_type is EventType.CHECKPOINT_INVALIDATED
    )


# ---------------------------------------------------------------------------
# create_checkpoint (brief Step 7)
# ---------------------------------------------------------------------------


def test_create_checkpoint_persists_exact_event_and_record(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint(
        "cp-1",
        step_id="R1",
        artifact_ids=("art-1",),
        compatibility=make_compat(
            step_id="R1",
            prompt_identity="prompt-r1",
            prompt_version="1",
            schema_identity="schema-r1",
            schema_version="1",
        ),
    )
    result = create_checkpoint(store, checkpoint)
    assert result == checkpoint

    created = checkpoint_events(store)[0]
    # The event carries only the input-context facts — never process state.
    assert set(created.payload) == {"checkpoint_id", "artifact_ids", "compatibility"}
    assert created.payload["checkpoint_id"] == "cp-1"
    assert created.payload["artifact_ids"] == ("art-1",)
    assert created.payload["compatibility"] == {
        "workflow_identity": "research-standard",
        "workflow_version": "1.0.0",
        "step_identity": "R1",
        "step_version": "1",
        "runtime_configuration_identity": "runtime-config-001",
        "prompt_identity": "prompt-r1",
        "prompt_version": "1",
        "schema_identity": "schema-r1",
        "schema_version": "1",
    }
    assert created.step_id == "R1"
    assert created.invocation_id is None
    assert created.attempt_id is None
    assert created.artifact_id is None
    # The event timestamp is the checkpoint's own created_at, so the reduced
    # record equals the record the caller persisted (created_at round-trips).
    assert created.timestamp == checkpoint.created_at
    projection = reduce_events(store.events(RUN_ID))
    assert projection.checkpoints["cp-1"] == checkpoint
    assert projection.checkpoints["cp-1"].status.value == "VALID"


def test_create_checkpoint_omits_not_applicable_compatibility_pairs(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", step_id="R1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    created = checkpoint_events(store)[0]
    assert set(created.payload["compatibility"]) == {
        "workflow_identity",
        "workflow_version",
        "step_identity",
        "step_version",
        "runtime_configuration_identity",
    }
    assert reduce_events(store.events(RUN_ID)).checkpoints["cp-1"] == checkpoint


def test_create_checkpoint_rejects_uncommitted_artifact(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    with pytest.raises(ArtifactNotCommittedError):
        create_checkpoint(store, make_checkpoint("cp-x", artifact_ids=("art-ghost",)))
    # Ruling 4 residue: a document without its commit event is not an input.
    store.save_artifact(make_artifact("art-residue").with_digest(COMMIT_DIGEST))
    with pytest.raises(ArtifactNotCommittedError):
        create_checkpoint(store, make_checkpoint("cp-x", artifact_ids=("art-residue",)))
    assert checkpoint_events(store) == ()


def test_create_checkpoint_rejects_cross_run_artifact(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    # A second run commits art-x under the same store.
    start_invocation(store, run_id=RUN_ID_2, invocation_id=INVOCATION_ID_2)
    store.append_event(
        attempt_created_event(
            run_id=RUN_ID_2, invocation_id=INVOCATION_ID_2, attempt_id="att-x"
        )
    )
    store.append_event(
        input_bound_event(
            run_id=RUN_ID_2, invocation_id=INVOCATION_ID_2, attempt_id="att-x"
        )
    )
    store.append_event(
        attempt_started_event(
            run_id=RUN_ID_2, invocation_id=INVOCATION_ID_2, attempt_id="att-x"
        )
    )
    commit_artifact(
        store,
        make_artifact(
            "art-x",
            run_id=RUN_ID_2,
            invocation_id=INVOCATION_ID_2,
            step_id="R1",
            attempt_id="att-x",
        ),
        STEP_PAYLOAD,
    )
    with pytest.raises(ArtifactNotCommittedError):
        create_checkpoint(
            store, make_checkpoint("cp-x", run_id=RUN_ID, artifact_ids=("art-x",))
        )
    assert checkpoint_events(store) == ()


def test_create_checkpoint_rejects_duplicate_checkpoint_id(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    with pytest.raises(RuntimeContractError):
        create_checkpoint(store, checkpoint)
    assert len(checkpoint_events(store)) == 1


def test_create_checkpoint_unknown_run_fails(tmp_path):
    store = make_store(tmp_path)
    with pytest.raises(RunNotFoundError):
        create_checkpoint(store, make_checkpoint("cp-1"))


def test_create_checkpoint_requires_a_checkpoint_record(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    with pytest.raises(RuntimeContractError):
        create_checkpoint(store, object())  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        create_checkpoint(store, None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_checkpoint
# ---------------------------------------------------------------------------


def test_validate_checkpoint_happy_path(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    assert validate_checkpoint(store, checkpoint, checkpoint.compatibility) is None
    # Durability: a fresh store instance validates the same record again.
    reopened = make_store(tmp_path)
    recorded = reduce_events(reopened.events(RUN_ID)).checkpoints["cp-1"]
    assert validate_checkpoint(reopened, recorded, checkpoint.compatibility) is None


def test_validate_checkpoint_requires_exact_compatibility(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    drifted = make_compat(step_id="R1", workflow_version="1.1.0")
    with pytest.raises(RuntimeContractError) as excinfo:
        validate_checkpoint(store, checkpoint, drifted)
    assert "workflow_version" in str(excinfo.value)
    # A present-vs-absent prompt pair is a mismatch on the pair dimension.
    with_prompt = make_compat(step_id="R1", prompt_identity="prompt-r1", prompt_version="1")
    with pytest.raises(RuntimeContractError) as excinfo:
        validate_checkpoint(store, checkpoint, with_prompt)
    assert "prompt_identity" in str(excinfo.value)


def test_validate_checkpoint_refuses_invalidated_records(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    store.append_event(invalidated_event(checkpoint))
    recorded = reduce_events(store.events(RUN_ID)).checkpoints["cp-1"]
    assert recorded.status.value == "INVALIDATED"
    # A stale VALID copy no longer matches the recorded history.
    with pytest.raises(RuntimeContractError):
        validate_checkpoint(store, checkpoint, checkpoint.compatibility)
    # The recorded INVALIDATED record itself is refused for reuse.
    with pytest.raises(RuntimeContractError):
        validate_checkpoint(store, recorded, recorded.compatibility)


def test_validate_checkpoint_forged_record_fails(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    forged = replace(checkpoint, artifact_ids=("art-1", "art-other"))
    with pytest.raises(RuntimeContractError):
        validate_checkpoint(store, forged, checkpoint.compatibility)


def test_validate_checkpoint_unknown_checkpoint_fails(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    with pytest.raises(RuntimeContractError):
        validate_checkpoint(
            store, make_checkpoint("cp-ghost", artifact_ids=("art-1",)), make_compat()
        )


def test_validate_checkpoint_missing_artifact_document_fails(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    document = (
        store.root / "cases" / CASE_ID / "runs" / RUN_ID
        / "artifacts" / "art-1" / "artifact.json"
    )
    document.unlink()
    with pytest.raises(EvidenceIntegrityError):
        validate_checkpoint(store, checkpoint, checkpoint.compatibility)


def test_validate_checkpoint_digest_tamper_fails(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    document = (
        store.root / "cases" / CASE_ID / "runs" / RUN_ID
        / "artifacts" / "art-1" / "artifact.json"
    )
    content = json.loads(document.read_text(encoding="utf-8"))
    content["artifact"]["digest"] = "sha256:" + "0" * 64
    document.write_text(json.dumps(content), encoding="utf-8")
    with pytest.raises(EvidenceIntegrityError):
        validate_checkpoint(store, checkpoint, checkpoint.compatibility)


def test_validate_checkpoint_requires_records_and_expected(tmp_path):
    store = make_store(tmp_path)
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    with pytest.raises(RuntimeContractError):
        validate_checkpoint(store, object(), checkpoint.compatibility)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        validate_checkpoint(store, checkpoint, object())  # type: ignore[arg-type]
    with pytest.raises(RunNotFoundError):
        validate_checkpoint(store, replace(checkpoint, run_id=RUN_ID_2), make_compat())


# ---------------------------------------------------------------------------
# invalidate_downstream
# ---------------------------------------------------------------------------


def test_invalidate_downstream_invalidates_only_transitive_dependents(tmp_path):
    """Rerunning R1 invalidates the R2/R3 checkpoints but leaves R1's own and
    the independent R4 checkpoint VALID (Spec 12)."""
    store = make_store(tmp_path)
    workflow = make_chain_workflow()
    build_checkpointed_chain(store)

    invalidated_steps = invalidate_downstream(store, RUN_ID, "R1", workflow=workflow)

    assert invalidated_steps == ("R2", "R3")
    events = invalidated_events(store)
    assert len(events) == 2
    assert {event.payload["checkpoint_id"] for event in events} == {"cp-2", "cp-3"}
    by_checkpoint = {event.payload["checkpoint_id"]: event for event in events}
    assert by_checkpoint["cp-2"].step_id == "R2"
    assert by_checkpoint["cp-3"].step_id == "R3"
    # Invalidation is historical: records stay, only the status flag turns.
    projection = reduce_events(store.events(RUN_ID))
    assert projection.checkpoints["cp-1"].status.value == "VALID"
    assert projection.checkpoints["cp-2"].status.value == "INVALIDATED"
    assert projection.checkpoints["cp-3"].status.value == "INVALIDATED"
    assert projection.checkpoints["cp-4"].status.value == "VALID"
    # The rerun step's own checkpoint is not downstream of itself, and an
    # independent step (R4) has no dependents at all.
    assert invalidate_downstream(store, RUN_ID, "R1", workflow=workflow) == ()
    assert invalidate_downstream(store, RUN_ID, "R4", workflow=workflow) == ()
    assert len(invalidated_events(store)) == 2


def test_invalidate_downstream_noop_without_downstream_checkpoints(tmp_path):
    store = make_store(tmp_path)
    workflow = make_chain_workflow()
    execute_chain(store, steps=("R1",))
    checkpoint = make_checkpoint("cp-1", artifact_ids=("art-1",))
    create_checkpoint(store, checkpoint)
    assert invalidate_downstream(store, RUN_ID, "R1", workflow=workflow) == ()
    assert invalidated_events(store) == ()
    assert reduce_events(store.events(RUN_ID)).checkpoints["cp-1"].status.value == "VALID"


def test_invalidate_downstream_invalidates_each_step_once_with_many_checkpoints(tmp_path):
    store = make_store(tmp_path)
    workflow = make_chain_workflow()
    build_checkpointed_chain(store)
    second = make_checkpoint(
        "cp-2b",
        step_id="R2",
        artifact_ids=("art-1", "art-2"),
        compatibility=make_compat(step_id="R2"),
    )
    create_checkpoint(store, second)

    assert invalidate_downstream(store, RUN_ID, "R1", workflow=workflow) == ("R2", "R3")
    events = invalidated_events(store)
    assert {event.payload["checkpoint_id"] for event in events} == {"cp-2", "cp-2b", "cp-3"}
    projection = reduce_events(store.events(RUN_ID))
    assert projection.checkpoints["cp-2"].status.value == "INVALIDATED"
    assert projection.checkpoints["cp-2b"].status.value == "INVALIDATED"
    assert projection.checkpoints["cp-3"].status.value == "INVALIDATED"
    assert projection.checkpoints["cp-1"].status.value == "VALID"
    assert projection.checkpoints["cp-4"].status.value == "VALID"


def test_invalidate_downstream_skips_already_invalidated_checkpoints(tmp_path):
    store = make_store(tmp_path)
    workflow = make_chain_workflow()
    (cp_1, cp_2, cp_3, cp_4) = build_checkpointed_chain(store)
    store.append_event(invalidated_event(cp_2))

    assert invalidate_downstream(store, RUN_ID, "R1", workflow=workflow) == ("R3",)
    events = invalidated_events(store)
    assert len(events) == 2
    assert events[1].payload == {"checkpoint_id": "cp-3"}
    projection = reduce_events(store.events(RUN_ID))
    assert projection.checkpoints["cp-2"].status.value == "INVALIDATED"
    assert projection.checkpoints["cp-3"].status.value == "INVALIDATED"


def test_invalidate_downstream_unknown_step_or_run_fails(tmp_path):
    store = make_store(tmp_path)
    workflow = make_chain_workflow()
    build_checkpointed_chain(store)
    with pytest.raises(RuntimeContractError):
        invalidate_downstream(store, RUN_ID, "R9", workflow=workflow)
    with pytest.raises(RunNotFoundError):
        invalidate_downstream(store, "run-ghost", "R1", workflow=workflow)
    with pytest.raises(RuntimeContractError):
        invalidate_downstream(store, RUN_ID, "R1", workflow=object())  # type: ignore[arg-type]


def test_invalidate_downstream_is_idempotent(tmp_path):
    store = make_store(tmp_path)
    workflow = make_chain_workflow()
    build_checkpointed_chain(store)
    assert invalidate_downstream(store, RUN_ID, "R1", workflow=workflow) == ("R2", "R3")
    assert invalidate_downstream(store, RUN_ID, "R1", workflow=workflow) == ()
    assert len(invalidated_events(store)) == 2


def test_invalidate_downstream_requires_keyword_only_workflow(tmp_path):
    store = make_store(tmp_path)
    workflow = make_chain_workflow()
    build_checkpointed_chain(store)
    with pytest.raises(TypeError):
        invalidate_downstream(store, RUN_ID, "R1", workflow)  # type: ignore[call-arg]
