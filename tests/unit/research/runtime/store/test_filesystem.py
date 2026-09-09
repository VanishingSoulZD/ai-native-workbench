"""Tests for the FileSystemRuntimeStore durable layout and read/write APIs.

Covers the brief's verbatim layout and idempotency snippets, run.json /
artifact.json document handling with ``runtime_schema_version=1``, the
commit-read semantics (residue is invisible; committed artifacts are
immutable and digest-checked) and per-instance caching of the event log.
"""

import json
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    ArtifactEnvelope,
    AttemptStatus,
    EntryMode,
    EventEnvelope,
    EventSchemaError,
    EventType,
    GateDecision,
    InvocationStatus,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.store import (
    ArtifactNotFoundError,
    EventConflictError,
    EvidenceIntegrityError,
    FileSystemRuntimeStore,
    ProjectionSchemaError,
    RunAlreadyExistsError,
    RunNotFoundError,
)

TS = "2026-09-09T00:00:00+00:00"
RUN_ID = "run-1"
DIGEST = "sha256:" + "d" * 64


# ---------------------------------------------------------------------------
# Shared fixtures/helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def make_store(tmp_path) -> FileSystemRuntimeStore:
    return FileSystemRuntimeStore(tmp_path)


def make_created_run(**overrides) -> RunRecord:
    """RunRecord matching the domain-test helper shape (case-1/run-1/CREATED)."""
    from ai_native_workbench.research.runtime.domain.models import CaseBinding

    return replace(
        RunRecord(
            run_id=RUN_ID,
            case_id="case-1",
            case_binding=CaseBinding(
                case_id="case-1",
                charter_identity="charter-001",
                charter_digest="sha256:" + "a" * 64,
                source_declaration_identity="urls-001",
                source_declaration_digest="sha256:" + "b" * 64,
            ),
            state=RunState.CREATED,
            cumulative_execution_scope=(),
            current_invocation_id=None,
            completion_reason=None,
        ),
        **overrides,
    )


def _execution_binding_payload() -> dict:
    return {
        "workflow_identity": "research-workflow",
        "workflow_version": "v1",
        "runtime_configuration_identity": "runtime-config-001",
        "prompts": {},
        "schemas": {},
    }


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


def invocation_started_event(**kw) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_STARTED,
        "evt-inv-1",
        invocation_id="inv-1",
        payload={
            "requested_scope": ["R1"],
            "entry_mode": EntryMode.START.value,
            "execution_binding": _execution_binding_payload(),
        },
        **kw,
    )


def attempt_created_event(**kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_CREATED,
        "evt-att-1",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id="att-1",
        **kw,
    )


def input_bound_event(**kw) -> EventEnvelope:
    return evt(
        EventType.INPUT_BOUND,
        "evt-ib-1",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id="att-1",
        payload={
            "input_binding_id": "ib-1",
            "artifact_ids": [],
            "upstream_attempt_ids": [],
        },
        **kw,
    )


def attempt_started_event(**kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_STARTED,
        "evt-att-start-1",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id="att-1",
        **kw,
    )


def artifact_committed_event(artifact_id: str = "art-1", **kw) -> EventEnvelope:
    return evt(
        EventType.ARTIFACT_COMMITTED,
        f"evt-art-{artifact_id}",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id="att-1",
        artifact_id=artifact_id,
        payload={"digest": DIGEST},
        **kw,
    )


def attempt_succeeded_event(**kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_SUCCEEDED,
        "evt-att-ok-1",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id="att-1",
        **kw,
    )


def invocation_completed_event(**kw) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_COMPLETED,
        "evt-inv-done-1",
        invocation_id="inv-1",
        payload={"status": "SUCCEEDED", "completion_reason": "BOUNDED_SCOPE"},
        **kw,
    )


def start_run(store) -> None:
    """create_run + a running invocation with a RUNNING attempt (att-1/R1)."""
    store.create_run(make_created_run())
    store.append_event(invocation_started_event())
    store.append_event(attempt_created_event())
    store.append_event(input_bound_event())
    store.append_event(attempt_started_event())


def make_artifact(artifact_id: str = "art-1", **overrides) -> ArtifactEnvelope:
    return replace(
        ArtifactEnvelope(
            artifact_id=artifact_id,
            run_id=RUN_ID,
            invocation_id="inv-1",
            step_id="R1",
            attempt_id="att-1",
            artifact_schema_id="evidence-set",
            artifact_schema_version="1",
            created_at=TS,
            digest=DIGEST,
            payload={"rows": [{"id": 1}]},
        ),
        **overrides,
    )


def read_run_json(tmp_path) -> dict:
    return json.loads(
        (tmp_path / "cases" / "case-1" / "runs" / RUN_ID / "run.json").read_text(
            encoding="utf-8"
        )
    )


# ---------------------------------------------------------------------------
# Durable layout and runtime_schema_version=1 (brief Step 1 snippet)
# ---------------------------------------------------------------------------


def test_run_layout_is_created(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    assert (tmp_path / "cases" / "case-1" / "runs" / "run-1" / "run.json").exists()
    assert (
        tmp_path / "cases" / "case-1" / "runs" / "run-1" / "execution.jsonl"
    ).exists()


def test_created_documents_declare_runtime_schema_version_1(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    document = read_run_json(tmp_path)
    assert document["runtime_schema_version"] == 1
    assert document["projection_version"] == 1
    lines = (
        tmp_path / "cases" / "case-1" / "runs" / "run-1" / "execution.jsonl"
    ).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["schema_version"] == 1
    assert json.loads(lines[0])["event_type"] == "RUN_CREATED"


def test_create_run_twice_raises_run_already_exists(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    with pytest.raises(RunAlreadyExistsError):
        store.create_run(make_created_run())


def test_create_run_rejects_non_created_state(tmp_path):
    store = make_store(tmp_path)
    running = make_created_run().start()
    with pytest.raises(RuntimeContractError):
        store.create_run(running)
    with pytest.raises(RunNotFoundError):
        store.load_run(RUN_ID)


# ---------------------------------------------------------------------------
# Load / read path
# ---------------------------------------------------------------------------


def test_load_run_returns_created_run(tmp_path):
    store = make_store(tmp_path)
    run = make_created_run()
    store.create_run(run)
    assert store.load_run(RUN_ID) == run


def test_load_run_unknown_run_raises(tmp_path):
    store = make_store(tmp_path)
    with pytest.raises(RunNotFoundError):
        store.load_run("ghost-run")


def test_load_run_rejects_unknown_runtime_schema_version(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    path = tmp_path / "cases" / "case-1" / "runs" / RUN_ID / "run.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["runtime_schema_version"] = 2
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ProjectionSchemaError):
        store.load_run(RUN_ID)


def test_load_run_missing_projection_requires_reconciliation(tmp_path):
    """run.json is a rebuildable projection; without it the read path refuses
    to guess and reconciliation is the repair authority."""
    store = make_store(tmp_path)
    start_run(store)
    (tmp_path / "cases" / "case-1" / "runs" / RUN_ID / "run.json").unlink()
    with pytest.raises(RunNotFoundError):
        store.load_run(RUN_ID)
    # Events themselves remain fully readable.
    assert len(store.events(RUN_ID)) == 5


def test_load_run_reflects_appended_events(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    assert store.load_run(RUN_ID).state is RunState.RUNNING
    assert store.load_run(RUN_ID).current_invocation_id == "inv-1"


# ---------------------------------------------------------------------------
# append_event: idempotency, conflicts, projection refresh
# ---------------------------------------------------------------------------


def test_append_event_and_read_back(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    store.append_event(invocation_started_event())
    store.append_event(attempt_created_event())
    events = store.events(RUN_ID)
    assert len(events) == 3
    assert events[0].event_type is EventType.RUN_CREATED
    assert events[1].event_type is EventType.INVOCATION_STARTED
    assert events[2].event_type is EventType.ATTEMPT_CREATED


def test_append_event_unknown_run_raises(tmp_path):
    store = make_store(tmp_path)
    with pytest.raises(RunNotFoundError):
        store.append_event(invocation_started_event())


def test_duplicate_event_id_is_idempotent(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    event = attempt_created_event()
    store.append_event(event)
    store.append_event(event)
    assert store.events(RUN_ID).count(event) == 1


def test_same_event_id_with_different_payload_is_rejected(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    event = attempt_created_event()
    store.append_event(event)
    with pytest.raises(EventConflictError):
        store.append_event(
            replace(attempt_created_event(), payload={"changed": True})
        )
    assert store.events(RUN_ID).count(event) == 1


def test_duplicate_logical_fact_with_fresh_id_is_rejected(tmp_path):
    """Ruling 11: a new event_id may not re-state a fact history reflects."""
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    second_run_created = evt(
        EventType.RUN_CREATED,
        "evt-rc-2",
        payload={
            "case_id": "case-1",
            "charter_identity": "charter-001",
            "charter_digest": "sha256:" + "a" * 64,
            "source_declaration_identity": "urls-001",
            "source_declaration_digest": "sha256:" + "b" * 64,
        },
    )
    with pytest.raises(EventConflictError):
        store.append_event(second_run_created)
    assert len(store.events(RUN_ID)) == 1


def test_append_event_contradicting_history_is_rejected(tmp_path):
    """An event the reducer cannot interpret (unknown attempt lineage, illegal
    transition, unresolved reference) is rejected before anything is written."""
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    orphan_success = attempt_succeeded_event()  # no ATTEMPT_CREATED for att-1
    with pytest.raises(EventConflictError):
        store.append_event(orphan_success)
    assert store.events(RUN_ID) == (
        store.events(RUN_ID)[0],
    )  # only RUN_CREATED remains
    assert len(store.events(RUN_ID)) == 1


def test_append_event_validates_envelope_schema(tmp_path):
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    with pytest.raises(EventSchemaError):
        store.append_event(attempt_created_event(schema_version=2))
    assert len(store.events(RUN_ID)) == 1


def test_events_survive_store_reopen(tmp_path):
    """The event log is durable: a fresh store instance (process restart)
    reads the same history."""
    store = make_store(tmp_path)
    start_run(store)
    restarted = make_store(tmp_path)
    assert restarted.events(RUN_ID) == store.events(RUN_ID)
    assert restarted.load_run(RUN_ID).state is RunState.RUNNING


# ---------------------------------------------------------------------------
# save_projection
# ---------------------------------------------------------------------------


def test_save_projection_writes_derived_document(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    current = store.load_run(RUN_ID)
    store.save_projection(current)  # given run matches reduced state
    document = read_run_json(tmp_path)
    assert document["run"]["state"] == "RUNNING"
    assert document["attempts"]["att-1"]["status"] == "RUNNING"


def test_save_projection_rejects_run_that_differs_from_events(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    with pytest.raises(RuntimeContractError):
        store.save_projection(make_created_run())  # stale CREATED view
    # run.json unchanged (still reflects the RUNNING state)
    assert read_run_json(tmp_path)["run"]["state"] == "RUNNING"


# ---------------------------------------------------------------------------
# Artifact documents: save/load/commit semantics (Ruling 4)
# ---------------------------------------------------------------------------


def test_save_artifact_creates_artifact_document(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    store.save_artifact(make_artifact())
    path = (
        tmp_path
        / "cases"
        / "case-1"
        / "runs"
        / RUN_ID
        / "artifacts"
        / "art-1"
        / "artifact.json"
    )
    assert path.exists()
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["runtime_schema_version"] == 1
    assert document["artifact"]["digest"] == DIGEST


def test_save_artifact_unknown_run_raises(tmp_path):
    store = make_store(tmp_path)
    with pytest.raises(RunNotFoundError):
        store.save_artifact(make_artifact())


def test_save_artifact_requires_step_attempt_pair(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    with pytest.raises(RuntimeContractError):
        store.save_artifact(make_artifact(step_id="R1", attempt_id=None))


def test_committed_artifact_round_trip(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    artifact = make_artifact()
    store.save_artifact(artifact)
    store.append_event(artifact_committed_event())  # commit fact
    loaded = store.load_artifact("art-1")
    assert loaded == artifact
    assert loaded.payload == {"rows": [{"id": 1}]}
    # The projection records the committed reference.
    document = read_run_json(tmp_path)
    assert document["artifacts"]["art-1"]["digest"] == DIGEST
    assert document["artifacts"]["art-1"]["attempt_id"] == "att-1"


def test_uncommitted_artifact_document_is_invisible(tmp_path):
    """Ruling 4: residue left by a crashed executor is never readable as a
    committed artifact."""
    store = make_store(tmp_path)
    start_run(store)
    residue = make_artifact(artifact_id="res-1")
    document = {
        "runtime_schema_version": 1,
        "artifact": {
            "artifact_id": residue.artifact_id,
            "run_id": residue.run_id,
            "invocation_id": residue.invocation_id,
            "artifact_schema_id": residue.artifact_schema_id,
            "artifact_schema_version": residue.artifact_schema_version,
            "created_at": residue.created_at,
            "step_id": residue.step_id,
            "attempt_id": residue.attempt_id,
            "digest": residue.digest,
            "provenance": list(residue.provenance),
            "payload": residue.payload,
        },
    }
    path = (
        tmp_path
        / "cases"
        / "case-1"
        / "runs"
        / RUN_ID
        / "artifacts"
        / "res-1"
        / "artifact.json"
    )
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ArtifactNotFoundError):
        store.load_artifact("res-1")


def test_missing_artifact_raises_artifact_not_found(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    with pytest.raises(ArtifactNotFoundError):
        store.load_artifact("ghost")


def test_committed_artifact_digest_mismatch_is_integrity_error(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    store.save_artifact(make_artifact(digest="sha256:" + "e" * 64))
    store.append_event(artifact_committed_event())  # event digest is DIGEST
    with pytest.raises(EvidenceIntegrityError):
        store.load_artifact("art-1")


def test_committed_artifact_document_is_immutable(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    store.save_artifact(make_artifact())
    store.append_event(artifact_committed_event())
    with pytest.raises(RuntimeContractError):
        store.save_artifact(make_artifact(payload={"rows": [{"id": 2}]}))
    # The original document is untouched.
    assert store.load_artifact("art-1").payload == {"rows": [{"id": 1}]}


def test_committed_artifact_same_document_resave_is_noop(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    artifact = make_artifact()
    store.save_artifact(artifact)
    store.append_event(artifact_committed_event())
    store.save_artifact(artifact)  # idempotent commit save
    assert store.load_artifact("art-1") == artifact


def test_precommit_artifact_document_may_be_overwritten(tmp_path):
    """Before the commit event the document is residue and may be replaced by
    the executor pipeline; after commit it is immutable."""
    store = make_store(tmp_path)
    start_run(store)
    store.save_artifact(make_artifact(digest=None, payload={"rows": [{"id": 1}]}))
    store.save_artifact(make_artifact(digest=None, payload={"rows": [{"id": 2}]}))
    # Still invisible without the commit event...
    with pytest.raises(ArtifactNotFoundError):
        store.load_artifact("art-1")
    # ...and the committed write completes the digest exactly once.
    committed = make_artifact(payload={"rows": [{"id": 2}]})
    store.save_artifact(committed)
    store.append_event(artifact_committed_event())
    assert store.load_artifact("art-1") == committed


def test_artifact_document_unknown_schema_version_fails_fast(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    store.save_artifact(make_artifact())
    store.append_event(artifact_committed_event())
    path = (
        tmp_path
        / "cases"
        / "case-1"
        / "runs"
        / RUN_ID
        / "artifacts"
        / "art-1"
        / "artifact.json"
    )
    document = json.loads(path.read_text(encoding="utf-8"))
    document["runtime_schema_version"] = 2
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(EvidenceIntegrityError):
        store.load_artifact("art-1")


def test_artifact_digest_is_completed_outside_store(tmp_path):
    """The store never computes digests: digest semantics belong to the
    commit protocol (Task 3); here the envelope arrives already digested."""
    store = make_store(tmp_path)
    start_run(store)
    artifact = make_artifact()  # already carries DIGEST
    store.save_artifact(artifact)
    assert artifact.digest == DIGEST
