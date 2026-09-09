"""Tests for the Task 3 Artifact commit protocol and durable Input Bindings
(Spec 5.5/9.4/11.2, Ruling 4/14).

Covers the brief Step 4/5 assertions: payload digesting over canonical JSON,
the commit order (payload -> digest -> committed evidence document ->
ARTIFACT_COMMITTED event), idempotent replay when a crash falls between the
document write and the event append, exactly one committed artifact per
attempt round (Ruling 14), and that only committed Artifacts are eligible
for an Input Binding — residue written straight into a run's artifacts
directory is never readable as a committed artifact (Ruling 4).
"""

import hashlib
import json
from dataclasses import replace

import pytest

from ai_native_workbench.research.runtime import (
    ArtifactEnvelope,
    CaseBinding,
    EntryMode,
    EventEnvelope,
    EventType,
    InputBinding,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.artifacts import (
    ArtifactNotCommittedError,
    commit_artifact,
    persist_input_binding,
)
from ai_native_workbench.research.runtime.store import (
    ArtifactNotFoundError,
    FileSystemRuntimeStore,
    RunNotFoundError,
    reduce_events,
)

CASE_ID = "case-1"
CASE_ID_2 = "case-2"
RUN_ID = "run-1"
RUN_ID_2 = "run-2"
INVOCATION_ID = "inv-1"
INVOCATION_ID_2 = "inv-2"
STEP_ID = "R1"
STEP_ID_2 = "R2"
ATTEMPT_ID = "att-1"
TS = "2026-09-09T08:00:00+00:00"

PAYLOAD = {"kind": "evidence-set", "items": [{"id": "s-1", "url": "https://e.com"}]}
PAYLOAD_UNICODE = {"note": "批准的执行证据"}
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


def invocation_started_event(run_id: str = RUN_ID, invocation_id: str = INVOCATION_ID, **kw):
    return evt(
        EventType.INVOCATION_STARTED,
        f"evt-{run_id}-inv-1",
        run_id=run_id,
        invocation_id=invocation_id,
        payload={
            "requested_scope": ["R1"],
            "entry_mode": EntryMode.START.value,
            "execution_binding": _execution_binding_payload(),
        },
        **kw,
    )


def attempt_created_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
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
    attempt_id: str = ATTEMPT_ID,
    **kw,
):
    return evt(
        EventType.INPUT_BOUND,
        f"evt-{run_id}-{attempt_id}-bound",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        payload={
            "input_binding_id": f"ib-{attempt_id}",
            "artifact_ids": [],
            "upstream_attempt_ids": [],
        },
        **kw,
    )


def attempt_started_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
    event_id: str | None = None,
    **kw,
):
    return evt(
        EventType.ATTEMPT_STARTED,
        event_id or f"evt-{run_id}-{attempt_id}-started",
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
    attempt_id: str = ATTEMPT_ID,
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


def attempt_failed_event(
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
    **kw,
):
    return evt(
        EventType.ATTEMPT_FAILED,
        f"evt-{run_id}-{attempt_id}-failed",
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        payload={"disposition": "EXECUTION_INTERRUPTED"},
        **kw,
    )


def invocation_completed_event(run_id: str = RUN_ID, invocation_id: str = INVOCATION_ID, **kw):
    return evt(
        EventType.INVOCATION_COMPLETED,
        f"evt-{run_id}-inv-done",
        run_id=run_id,
        invocation_id=invocation_id,
        payload={"status": "SUCCEEDED", "completion_reason": "BOUNDED_SCOPE"},
        **kw,
    )


def build_running_attempt(
    store,
    *,
    run_id: str = RUN_ID,
    case_id: str = CASE_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID,
    attempt_id: str = ATTEMPT_ID,
) -> None:
    """create_run + started Invocation + RUNNING attempt with an empty Input
    Binding (the natural first-step flow)."""
    store.create_run(make_run_record(run_id=run_id, case_id=case_id))
    store.append_event(
        invocation_started_event(run_id=run_id, invocation_id=invocation_id)
    )
    store.append_event(
        attempt_created_event(
            run_id=run_id, invocation_id=invocation_id, step_id=step_id,
            attempt_id=attempt_id,
        )
    )
    store.append_event(
        input_bound_event(
            run_id=run_id, invocation_id=invocation_id, step_id=step_id,
            attempt_id=attempt_id,
        )
    )
    store.append_event(
        attempt_started_event(
            run_id=run_id, invocation_id=invocation_id, step_id=step_id,
            attempt_id=attempt_id,
        )
    )


def make_artifact(artifact_id: str = "art-1", **overrides) -> ArtifactEnvelope:
    """An uncommitted (digest-free) envelope; commit_artifact adds the payload."""
    defaults = dict(
        artifact_id=artifact_id,
        run_id=RUN_ID,
        invocation_id=INVOCATION_ID,
        artifact_schema_id="evidence-set",
        artifact_schema_version="1",
        created_at=TS,
        step_id=STEP_ID,
        attempt_id=ATTEMPT_ID,
    )
    defaults.update(overrides)
    return ArtifactEnvelope(**defaults)


def make_binding(
    input_binding_id: str = "ib-2",
    run_id: str = RUN_ID,
    invocation_id: str = INVOCATION_ID,
    step_id: str = STEP_ID_2,
    attempt_id: str = "att-2",
    **overrides,
) -> InputBinding:
    defaults = dict(
        input_binding_id=input_binding_id,
        run_id=run_id,
        invocation_id=invocation_id,
        step_id=step_id,
        attempt_id=attempt_id,
        artifact_ids=(),
        upstream_attempt_ids=(),
    )
    defaults.update(overrides)
    return InputBinding(**defaults)


def reference_payload_digest(payload: object) -> str:
    """Independent reference digest pinning the documented canonical-JSON
    scheme (sha256 over sort_keys/compact/ensure_ascii=False dumps)."""
    text = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def commit_events(store, run_id: str = RUN_ID) -> tuple:
    return tuple(
        event
        for event in store.events(run_id)
        if event.event_type is EventType.ARTIFACT_COMMITTED
    )


def input_bound_events(store, run_id: str = RUN_ID) -> tuple:
    return tuple(
        event
        for event in store.events(run_id)
        if event.event_type is EventType.INPUT_BOUND
    )


# ---------------------------------------------------------------------------
# commit_artifact: the commit protocol (brief Step 5 order)
# ---------------------------------------------------------------------------


def test_commit_artifact_records_durable_evidence_in_order(tmp_path):
    """payload -> digest -> committed document -> ARTIFACT_COMMITTED event."""
    store = make_store(tmp_path)
    build_running_attempt(store)
    artifact = make_artifact("art-1")

    committed = commit_artifact(store, artifact, PAYLOAD)

    digest = reference_payload_digest(PAYLOAD)
    expected = replace(artifact, payload=PAYLOAD).with_digest(digest)
    assert committed.digest == digest
    assert committed.payload == PAYLOAD
    assert committed == expected
    assert store.load_artifact("art-1") == committed

    events = store.events(RUN_ID)
    commit = commit_events(store)[0]
    assert commit.payload == {"digest": digest}
    assert commit.invocation_id == INVOCATION_ID
    assert commit.step_id == STEP_ID
    assert commit.attempt_id == ATTEMPT_ID
    assert commit.event_id
    # run.json projection is rebuilt from events: artifact reference + record.
    projection = reduce_events(events)
    assert projection.artifacts["art-1"].digest == digest
    assert projection.artifacts["art-1"].committed_at == commit.timestamp
    assert projection.run.run_id == RUN_ID


def test_commit_artifact_digest_is_canonical_and_deterministic(tmp_path):
    # The same payload commits under two artifact ids (each in its own run,
    # since Ruling 14 allows one commit per attempt round).
    store = make_store(tmp_path)
    build_running_attempt(store)
    first = commit_artifact(store, make_artifact("art-1"), PAYLOAD_UNICODE)
    store = FileSystemRuntimeStore(tmp_path / "second-run")
    build_running_attempt(
        store, run_id=RUN_ID_2, case_id=CASE_ID_2,
        invocation_id=INVOCATION_ID_2, attempt_id="att-x",
    )
    second = commit_artifact(
        store, make_artifact("art-2", run_id=RUN_ID_2, invocation_id=INVOCATION_ID_2,
                             attempt_id="att-x"), PAYLOAD_UNICODE,
    )
    assert first.digest == second.digest == reference_payload_digest(PAYLOAD_UNICODE)
    assert first.digest.startswith("sha256:")
    assert len(first.digest) == len("sha256:") + 64
    # ensure_ascii=False is part of the scheme: an escaped digest must differ.
    ascii_escaped = json.dumps(PAYLOAD_UNICODE, ensure_ascii=True)
    assert first.digest != "sha256:" + hashlib.sha256(
        ascii_escaped.encode("utf-8")
    ).hexdigest()


def test_commit_artifact_rejects_non_jsonable_payload(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact(), object())  # type: ignore[arg-type]
    assert commit_events(store) == ()


def test_commit_artifact_requires_an_envelope(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, object(), PAYLOAD)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, None, PAYLOAD)  # type: ignore[arg-type]


def test_commit_artifact_refuses_an_already_digested_envelope(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact(digest=COMMIT_DIGEST), PAYLOAD)
    assert commit_events(store) == ()


def test_commit_artifact_unknown_run_fails(tmp_path):
    store = make_store(tmp_path)
    with pytest.raises(RunNotFoundError):
        commit_artifact(store, make_artifact(), PAYLOAD)


def test_commit_artifact_requires_a_running_invocation(tmp_path):
    # No invocation yet: the run is still CREATED.
    store = make_store(tmp_path)
    store.create_run(make_run_record())
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact(), PAYLOAD)
    # A completed invocation may not commit either.
    store = FileSystemRuntimeStore(tmp_path / "second")
    build_running_attempt(store)
    store.append_event(attempt_succeeded_event())
    store.append_event(invocation_completed_event())
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact("art-2"), PAYLOAD)
    assert commit_events(store) == ()


def test_commit_artifact_requires_a_running_attempt_with_matching_lineage(tmp_path):
    # The attempt was created but never started (PENDING, no durable binding).
    store = make_store(tmp_path)
    store.create_run(make_run_record())
    store.append_event(invocation_started_event())
    store.append_event(attempt_created_event())
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact(), PAYLOAD)
    # The envelope names a different step than the running attempt belongs to.
    store = FileSystemRuntimeStore(tmp_path / "second")
    build_running_attempt(store)
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact(step_id=STEP_ID_2, attempt_id="att-x"), PAYLOAD)
    assert commit_events(store) == ()


def test_source_acquisition_artifact_commits_without_step_or_attempt(tmp_path):
    """Spec 9: source-acquisition artifacts bind to the Invocation only."""
    store = make_store(tmp_path)
    store.create_run(make_run_record())
    store.append_event(invocation_started_event())
    envelope = make_artifact(step_id=None, attempt_id=None)
    committed = commit_artifact(store, envelope, PAYLOAD)
    assert committed.digest == reference_payload_digest(PAYLOAD)
    commit = commit_events(store)[0]
    assert commit.step_id is None
    assert commit.attempt_id is None
    assert reduce_events(store.events(RUN_ID)).artifacts["art-1"].step_id is None


def test_attempt_round_commits_exactly_one_artifact(tmp_path):
    """Ruling 14: one committed artifact per attempt round."""
    store = make_store(tmp_path)
    build_running_attempt(store)
    commit_artifact(store, make_artifact("art-1"), PAYLOAD)
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact("art-2"), PAYLOAD)
    assert len(commit_events(store)) == 1
    assert "art-2" not in reduce_events(store.events(RUN_ID)).artifacts


def test_retry_round_may_commit_again(tmp_path):
    """ATTEMPT_FAILED -> ATTEMPT_STARTED opens a fresh round (Ruling 14)."""
    store = make_store(tmp_path)
    build_running_attempt(store)
    commit_artifact(store, make_artifact("art-1"), PAYLOAD)
    store.append_event(attempt_failed_event())
    # A fresh ATTEMPT_STARTED id: the retry round is a new fact.
    store.append_event(attempt_started_event(event_id="evt-run-1-att-1-retry"))
    second = commit_artifact(store, make_artifact("art-2"), PAYLOAD)
    assert second.digest == reference_payload_digest(PAYLOAD)
    assert len(commit_events(store)) == 2
    projection = reduce_events(store.events(RUN_ID))
    assert projection.attempts[ATTEMPT_ID].status.value == "RUNNING"
    assert "art-1" in projection.artifacts
    assert "art-2" in projection.artifacts


def test_commit_artifact_replay_is_idempotent(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    artifact = make_artifact("art-1")
    first = commit_artifact(store, artifact, PAYLOAD)
    replay = commit_artifact(store, artifact, PAYLOAD)
    assert replay == first
    assert len(commit_events(store)) == 1
    # A fresh store instance (process restart) replays identically.
    reopened = make_store(tmp_path)
    assert commit_artifact(reopened, artifact, PAYLOAD) == first
    assert len(commit_events(reopened)) == 1
    assert reopened.load_artifact("art-1") == first


def test_commit_artifact_recovers_from_crash_between_document_and_event(tmp_path):
    """Ruling 4 residue: document written, commit event lost — a retry of the
    commit heals it without duplicating evidence."""
    store = make_store(tmp_path)
    build_running_attempt(store)
    artifact = make_artifact("art-1")
    digest = reference_payload_digest(PAYLOAD)
    # What the crashed executor left behind: only the document, no event.
    residue = replace(artifact, payload=PAYLOAD).with_digest(digest)
    store.save_artifact(residue)
    with pytest.raises(ArtifactNotFoundError):
        store.load_artifact("art-1")

    committed = commit_artifact(store, artifact, PAYLOAD)
    assert committed == residue
    assert len(commit_events(store)) == 1
    assert store.load_artifact("art-1") == residue


def test_commit_replay_rejects_different_payload_or_envelope(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    artifact = make_artifact("art-1")
    commit_artifact(store, artifact, PAYLOAD)
    # A different payload can never commit under the same artifact id.
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, artifact, {"kind": "other"})
    # The same payload with a different envelope is not the recorded artifact.
    with pytest.raises(RuntimeContractError):
        commit_artifact(store, make_artifact(created_at="2026-09-09T09:00:00+00:00"), PAYLOAD)
    assert len(commit_events(store)) == 1


# ---------------------------------------------------------------------------
# persist_input_binding: only committed artifacts are eligible (Ruling 4)
# ---------------------------------------------------------------------------


def test_persist_input_binding_records_the_durable_binding(tmp_path):
    """R1 commits art-1; R2's attempt binds to it before ATTEMPT_STARTED
    (Spec 5.5: INPUT_BOUND must precede the first start)."""
    store = make_store(tmp_path)
    build_running_attempt(store)
    commit_artifact(store, make_artifact("art-1"), PAYLOAD)
    store.append_event(attempt_succeeded_event())
    store.append_event(attempt_created_event(step_id=STEP_ID_2, attempt_id="att-2"))
    binding = make_binding(artifact_ids=("art-1",), upstream_attempt_ids=(ATTEMPT_ID,))

    persist_input_binding(store, binding)
    persist_input_binding(store, binding)  # idempotent replay is a no-op

    bound_events = input_bound_events(store)
    assert len(bound_events) == 2
    bound = bound_events[1]
    assert bound.payload == {
        "input_binding_id": "ib-2",
        "artifact_ids": ("art-1",),
        "upstream_attempt_ids": ("att-1",),
    }
    assert bound.invocation_id == INVOCATION_ID
    assert bound.step_id == STEP_ID_2
    assert bound.attempt_id == "att-2"
    # Ordering proof: the attempt may only start after the binding is durable.
    store.append_event(attempt_started_event(step_id=STEP_ID_2, attempt_id="att-2"))
    projection = reduce_events(store.events(RUN_ID))
    assert projection.input_bindings["ib-2"] == binding
    assert projection.attempts["att-2"].input_binding_id == "ib-2"
    assert projection.attempts["att-2"].status.value == "RUNNING"
    # Durability: a fresh store instance reduces the same history.
    reopened = make_store(tmp_path)
    assert reduce_events(reopened.events(RUN_ID)).input_bindings["ib-2"] == binding


def test_uncommitted_residue_cannot_be_used_as_step_input(tmp_path):
    """Ruling 4: residue written straight into the artifacts directory (a
    crashed executor's leftovers) is neither readable nor bindable."""
    store = make_store(tmp_path)
    build_running_attempt(store)
    store.append_event(attempt_succeeded_event())
    store.append_event(attempt_created_event(step_id=STEP_ID_2, attempt_id="att-2"))
    residue = make_artifact("art-residue", step_id=STEP_ID_2, attempt_id="att-2")
    store.save_artifact(residue.with_digest(COMMIT_DIGEST))
    with pytest.raises(ArtifactNotFoundError):
        store.load_artifact("art-residue")
    binding = make_binding(artifact_ids=("art-residue",))
    with pytest.raises(ArtifactNotCommittedError):
        persist_input_binding(store, binding)
    assert len(input_bound_events(store)) == 1


def test_persist_input_binding_refuses_a_cross_run_committed_artifact(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    store.append_event(attempt_succeeded_event())
    store.append_event(attempt_created_event(step_id=STEP_ID_2, attempt_id="att-2"))
    # A second run commits art-x under the same store.
    build_running_attempt(
        store, run_id=RUN_ID_2, case_id=CASE_ID_2,
        invocation_id=INVOCATION_ID_2, attempt_id="att-x",
    )
    commit_artifact(
        store,
        make_artifact("art-x", run_id=RUN_ID_2, invocation_id=INVOCATION_ID_2, attempt_id="att-x"),
        PAYLOAD,
    )
    binding = make_binding(artifact_ids=("art-x",))
    with pytest.raises(ArtifactNotCommittedError):
        persist_input_binding(store, binding)
    assert len(input_bound_events(store)) == 1


def test_persist_input_binding_requires_a_pending_attempt(tmp_path):
    store = make_store(tmp_path)
    # The attempt is already RUNNING (bound and started by the builder).
    build_running_attempt(store)
    with pytest.raises(RuntimeContractError):
        persist_input_binding(store, make_binding(step_id=STEP_ID, attempt_id=ATTEMPT_ID))
    # An attempt that was never created.
    with pytest.raises(RuntimeContractError):
        persist_input_binding(store, make_binding(attempt_id="att-ghost"))
    # A second binding for an already bound attempt (fresh id) is rejected.
    store.append_event(attempt_created_event(step_id=STEP_ID_2, attempt_id="att-2"))
    persist_input_binding(store, make_binding())
    with pytest.raises(RuntimeContractError):
        persist_input_binding(store, make_binding(input_binding_id="ib-other"))
    assert len(input_bound_events(store)) == 2


def test_persist_input_binding_requires_matching_lineage_and_run(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    store.append_event(attempt_created_event(step_id=STEP_ID_2, attempt_id="att-2"))
    # A binding that names a run this store has never created is explicit.
    with pytest.raises(RunNotFoundError):
        persist_input_binding(store, make_binding(run_id=RUN_ID_2))
    with pytest.raises(RuntimeContractError):
        persist_input_binding(store, make_binding(invocation_id="inv-other"))
    with pytest.raises(RuntimeContractError):
        persist_input_binding(store, make_binding(step_id=STEP_ID))
    with pytest.raises(RuntimeContractError):
        persist_input_binding(store, make_binding(attempt_id="att-other"))
    with pytest.raises(RuntimeContractError):
        persist_input_binding(store, object())  # type: ignore[arg-type]
    assert len(input_bound_events(store)) == 1


def test_persist_input_binding_refuses_unknown_upstream_attempts(tmp_path):
    store = make_store(tmp_path)
    build_running_attempt(store)
    commit_artifact(store, make_artifact("art-1"), PAYLOAD)
    store.append_event(attempt_succeeded_event())
    store.append_event(attempt_created_event(step_id=STEP_ID_2, attempt_id="att-2"))
    with pytest.raises(RuntimeContractError):
        persist_input_binding(
            store, make_binding(artifact_ids=("art-1",), upstream_attempt_ids=("att-ghost",))
        )
    assert len(input_bound_events(store)) == 1


def test_persist_input_binding_binds_no_artifacts_for_a_first_step(tmp_path):
    """A step may legitimately have no upstream artifacts (Spec 5.5)."""
    store = make_store(tmp_path)
    build_running_attempt(store)
    store.append_event(attempt_created_event(step_id=STEP_ID_2, attempt_id="att-2"))
    persist_input_binding(store, make_binding())
    projection = reduce_events(store.events(RUN_ID))
    assert projection.input_bindings["ib-2"].artifact_ids == ()
    assert projection.input_bindings["ib-2"].upstream_attempt_ids == ()


def test_persist_input_binding_unknown_run_fails(tmp_path):
    store = make_store(tmp_path)
    with pytest.raises(RunNotFoundError):
        persist_input_binding(store, make_binding())
