"""Tests for startup reconciliation of the three v1 execution crash windows
(brief Step 6): stranded RUNNING attempt without durable success evidence,
complete durable evidence with a missing success event, and a stale run.json.
Also covers fail-fast evidence/schema handling and idempotent re-reconcile.

Each crash window is constructed by direct on-disk mutation after a normal
store session, then reconciled through a fresh store instance over the same
root (mirrors a process restart; store handles are per-instance caches).
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
    InvocationStatus,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.reconciliation import (
    ReconciliationOutcome,
    reconcile_run,
)
from ai_native_workbench.research.runtime.store import (
    EvidenceIntegrityError,
    FileSystemRuntimeStore,
    ProjectionSchemaError,
    RunNotFoundError,
    reduce_events,
)

TS = "2026-09-09T00:00:00+00:00"
RUN_ID = "run-1"
DIGEST = "sha256:" + "d" * 64
EXECUTION_INTERRUPTED = "EXECUTION_INTERRUPTED"


# ---------------------------------------------------------------------------
# Helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def make_store(tmp_path) -> FileSystemRuntimeStore:
    return FileSystemRuntimeStore(tmp_path)


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


def _binding_payload() -> dict:
    return {
        "workflow_identity": "research-workflow",
        "workflow_version": "v1",
        "runtime_configuration_identity": "runtime-config-001",
        "prompts": {},
        "schemas": {},
    }


def run_dir(tmp_path) -> object:
    return tmp_path / "cases" / "case-1" / "runs" / RUN_ID


def read_run_json(tmp_path) -> dict:
    return json.loads((run_dir(tmp_path) / "run.json").read_text(encoding="utf-8"))


def make_created_run():
    from ai_native_workbench.research.runtime.domain.models import (
        CaseBinding,
        RunRecord,
    )

    return RunRecord(
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
    )


def invocation_started_event(invocation_id="inv-1", **kw) -> EventEnvelope:
    return evt(
        EventType.INVOCATION_STARTED,
        f"evt-inv-{invocation_id}",
        invocation_id=invocation_id,
        payload={
            "requested_scope": ["R1"],
            "entry_mode": EntryMode.START.value,
            "execution_binding": _binding_payload(),
        },
        **kw,
    )


def attempt_created_event(attempt_id="att-1", **kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_CREATED,
        **{
            "event_id": f"evt-att-{attempt_id}",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": attempt_id,
            **kw,
        },
    )


def input_bound_event(attempt_id="att-1", binding_id="ib-1", **kw) -> EventEnvelope:
    return evt(
        EventType.INPUT_BOUND,
        f"evt-ib-{binding_id}",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id=attempt_id,
        payload={
            "input_binding_id": binding_id,
            "artifact_ids": [],
            "upstream_attempt_ids": [],
        },
        **kw,
    )


def attempt_started_event(attempt_id="att-1", **kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_STARTED,
        **{
            "event_id": f"evt-att-start-{attempt_id}",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": attempt_id,
            **kw,
        },
    )


def artifact_envelope(artifact_id="art-1") -> ArtifactEnvelope:
    return ArtifactEnvelope(
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
    )


def artifact_committed_event(artifact_id="art-1", attempt_id="att-1", **kw) -> EventEnvelope:
    return evt(
        EventType.ARTIFACT_COMMITTED,
        f"evt-art-{artifact_id}",
        invocation_id="inv-1",
        step_id="R1",
        attempt_id=attempt_id,
        artifact_id=artifact_id,
        payload={"digest": DIGEST},
        **kw,
    )


def attempt_succeeded_event(attempt_id="att-1", **kw) -> EventEnvelope:
    return evt(
        EventType.ATTEMPT_SUCCEEDED,
        **{
            "event_id": f"evt-att-ok-{attempt_id}",
            "invocation_id": "inv-1",
            "step_id": "R1",
            "attempt_id": attempt_id,
            **kw,
        },
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
    """create_run + invocation with attempt att-1 RUNNING (no artifact yet)."""
    store.create_run(make_created_run())
    store.append_event(invocation_started_event())
    store.append_event(attempt_created_event())
    store.append_event(input_bound_event())
    store.append_event(attempt_started_event())


def commit_artifact(store, artifact_id="art-1", attempt_id="att-1") -> None:
    store.save_artifact(artifact_envelope(artifact_id))
    store.append_event(artifact_committed_event(artifact_id, attempt_id))


def complete_run(store) -> None:
    """Run the att-1 cycle to a COMPLETED run (three-terminal-state basis)."""
    start_run(store)
    commit_artifact(store)
    store.append_event(attempt_succeeded_event())
    store.append_event(invocation_completed_event())
    assert store.load_run(RUN_ID).state is RunState.COMPLETED


# ---------------------------------------------------------------------------
# Crash window 1: Attempt RUNNING + no committed Artifact
# ---------------------------------------------------------------------------


def test_reconcile_fails_stranded_attempt_without_evidence(tmp_path):
    start_run(make_store(tmp_path))  # crash: attempt att-1 RUNNING, no artifact
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert isinstance(outcome, ReconciliationOutcome)
    appended = outcome.appended_events
    assert len(appended) == 1
    assert appended[0].event_type is EventType.ATTEMPT_FAILED
    assert appended[0].attempt_id == "att-1"
    assert appended[0].invocation_id == "inv-1"
    assert appended[0].step_id == "R1"
    assert appended[0].payload == {"disposition": EXECUTION_INTERRUPTED}
    projection = outcome.projection
    assert projection.attempts["att-1"].status is AttemptStatus.FAILED
    assert projection.failure_dispositions == {"att-1": EXECUTION_INTERRUPTED}
    # Ruling 12: interruption stays at ATTEMPT level.
    assert projection.invocations["inv-1"].status is InvocationStatus.RUNNING
    assert projection.run.state is RunState.RUNNING
    # The rebuilt projection on disk agrees with the outcome.
    assert read_run_json(tmp_path)["failure_dispositions"] == {
        "att-1": EXECUTION_INTERRUPTED
    }


def test_reconcile_is_idempotent_noop(tmp_path):
    start_run(make_store(tmp_path))
    first = reconcile_run(make_store(tmp_path), RUN_ID)
    assert len(first.appended_events) == 1
    second = reconcile_run(make_store(tmp_path), RUN_ID)
    assert second.appended_events == ()
    assert second.projection == first.projection


def test_reconcile_failed_attempt_retry_without_new_evidence_still_interrupted(
    tmp_path,
):
    """A restarted attempt cannot use a prior round's artifact as success
    evidence: only ARTIFACT_COMMITTED events after its last ATTEMPT_STARTED
    count (retry evidence window)."""
    store = make_store(tmp_path)
    start_run(store)
    commit_artifact(store)  # round 1 evidence
    store.append_event(
        evt(
            EventType.ATTEMPT_FAILED,
            "evt-att-fail-1",
            invocation_id="inv-1",
            step_id="R1",
            attempt_id="att-1",
            payload={"disposition": "EXECUTION_ERROR"},
        )
    )
    store.append_event(attempt_started_event(event_id="evt-restart-1"))  # retry
    assert store.load_run(RUN_ID).state is RunState.RUNNING
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert len(outcome.appended_events) == 1
    assert outcome.appended_events[0].event_type is EventType.ATTEMPT_FAILED
    assert outcome.projection.attempts["att-1"].status is AttemptStatus.FAILED
    assert outcome.projection.failure_dispositions == {
        "att-1": EXECUTION_INTERRUPTED
    }


# ---------------------------------------------------------------------------
# Crash window 2: Artifact committed + missing success event
# ---------------------------------------------------------------------------


def test_reconcile_appends_missing_success_event_from_durable_evidence(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    commit_artifact(store)  # crash: art-1 committed, ATTEMPT_SUCCEEDED lost
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    appended = outcome.appended_events
    assert len(appended) == 1
    assert appended[0].event_type is EventType.ATTEMPT_SUCCEEDED
    assert appended[0].attempt_id == "att-1"
    projection = outcome.projection
    assert projection.attempts["att-1"].status is AttemptStatus.SUCCEEDED
    assert projection.failure_dispositions == {}
    # Invocation/run stay RUNNING: only the missing fact is appended.
    assert projection.invocations["inv-1"].status is InvocationStatus.RUNNING
    assert projection.run.state is RunState.RUNNING
    assert reconcile_run(make_store(tmp_path), RUN_ID).appended_events == ()


def test_reconcile_appends_success_only_for_attempt_with_evidence(tmp_path):
    """Two stranded attempts: att-1 has durable evidence, att-2 does not.
    Missing facts are appended in last-ATTEMPT_STARTED event order."""
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    store.append_event(invocation_started_event())
    store.append_event(attempt_created_event(attempt_id="att-1"))
    store.append_event(input_bound_event(attempt_id="att-1"))
    store.append_event(attempt_started_event(attempt_id="att-1"))
    store.append_event(attempt_created_event(attempt_id="att-2", event_id="evt-att-2"))
    store.append_event(
        input_bound_event(attempt_id="att-2", binding_id="ib-2")
    )
    store.append_event(attempt_started_event(attempt_id="att-2", event_id="evt-as-2"))
    commit_artifact(store, artifact_id="art-1", attempt_id="att-1")
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert [e.event_type.value for e in outcome.appended_events] == [
        "ATTEMPT_SUCCEEDED",
        "ATTEMPT_FAILED",
    ]
    assert outcome.appended_events[0].attempt_id == "att-1"
    assert outcome.appended_events[1].attempt_id == "att-2"
    assert outcome.appended_events[1].payload == {
        "disposition": EXECUTION_INTERRUPTED
    }
    projection = outcome.projection
    assert projection.attempts["att-1"].status is AttemptStatus.SUCCEEDED
    assert projection.attempts["att-2"].status is AttemptStatus.FAILED


def test_reconcile_source_acquisition_commit_is_not_attempt_evidence(tmp_path):
    """A source-acquisition artifact has no attempt lineage and therefore can
    never satisfy a stranded attempt's success evidence."""
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    store.append_event(invocation_started_event())
    source = ArtifactEnvelope(
        artifact_id="src-1",
        run_id=RUN_ID,
        invocation_id="inv-1",
        step_id=None,
        attempt_id=None,
        artifact_schema_id="source-declaration",
        artifact_schema_version="1",
        created_at=TS,
        digest=DIGEST,
        payload={"urls": ["https://example.com/a"]},
    )
    store.save_artifact(source)
    store.append_event(
        evt(
            EventType.ARTIFACT_COMMITTED,
            "evt-art-src-1",
            invocation_id="inv-1",
            artifact_id="src-1",
            payload={"digest": DIGEST},
        )
    )
    store.append_event(attempt_created_event())
    store.append_event(input_bound_event())
    store.append_event(attempt_started_event())
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert len(outcome.appended_events) == 1
    assert outcome.appended_events[0].event_type is EventType.ATTEMPT_FAILED


# ---------------------------------------------------------------------------
# Crash window 3: stale / missing run.json
# ---------------------------------------------------------------------------


def test_reconcile_rebuilds_stale_run_json(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    commit_artifact(store)
    stale = read_run_json(tmp_path)  # snapshot while the run was RUNNING
    store.append_event(attempt_succeeded_event())
    store.append_event(invocation_completed_event())
    assert store.load_run(RUN_ID).state is RunState.COMPLETED
    # Crash: run.json still describes the earlier RUNNING projection.
    (run_dir(tmp_path) / "run.json").write_text(
        json.dumps(stale), encoding="utf-8"
    )
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert outcome.appended_events == ()
    assert outcome.projection.run.state is RunState.COMPLETED
    # The document was rebuilt from events, not patched from the stale copy.
    assert store.load_run(RUN_ID).state is RunState.COMPLETED
    assert read_run_json(tmp_path)["run"]["state"] == "COMPLETED"


def test_reconcile_rebuilds_missing_run_json(tmp_path):
    complete_run(make_store(tmp_path))
    (run_dir(tmp_path) / "run.json").unlink()
    with pytest.raises(RunNotFoundError):
        make_store(tmp_path).load_run(RUN_ID)  # read path requires projection
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert outcome.appended_events == ()
    assert outcome.projection.run.state is RunState.COMPLETED
    assert make_store(tmp_path).load_run(RUN_ID).state is RunState.COMPLETED


def test_reconcile_completed_run_is_noop(tmp_path):
    complete_run(make_store(tmp_path))
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert outcome.appended_events == ()
    assert outcome.projection.run.state is RunState.COMPLETED
    assert outcome.projection.attempts["att-1"].status is AttemptStatus.SUCCEEDED


def test_reconcile_projection_matches_direct_reduction(tmp_path):
    """The reconciled projection is exactly the pure reduction of events."""
    start_run(make_store(tmp_path))
    reconcile_run(make_store(tmp_path), RUN_ID)
    store = make_store(tmp_path)
    assert reconcile_run(store, RUN_ID).projection == reduce_events(
        store.events(RUN_ID)
    )


# ---------------------------------------------------------------------------
# Fail fast: durable evidence and schema integrity
# ---------------------------------------------------------------------------


def test_reconcile_fails_fast_on_missing_evidence_document(tmp_path):
    """A committed event referencing a missing artifact document is an
    integrity failure: never silently dropped, never re-executed."""
    store = make_store(tmp_path)
    start_run(store)
    commit_artifact(store)
    (run_dir(tmp_path) / "artifacts" / "art-1" / "artifact.json").unlink()
    with pytest.raises(EvidenceIntegrityError):
        reconcile_run(make_store(tmp_path), RUN_ID)
    # No events were appended and the projection was not rebuilt.
    assert make_store(tmp_path).events(RUN_ID)[-1].event_type is EventType.ARTIFACT_COMMITTED


def test_reconcile_fails_fast_on_digest_mismatch(tmp_path):
    store = make_store(tmp_path)
    start_run(store)
    commit_artifact(store)
    path = run_dir(tmp_path) / "artifacts" / "art-1" / "artifact.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["artifact"]["digest"] = "sha256:" + "f" * 64
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(EvidenceIntegrityError):
        reconcile_run(make_store(tmp_path), RUN_ID)


def test_reconcile_fails_fast_on_unknown_event_schema(tmp_path):
    start_run(make_store(tmp_path))
    path = run_dir(tmp_path) / "execution.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    last = json.loads(lines[-1])
    last["schema_version"] = 2
    lines[-1] = json.dumps(last)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(EventSchemaError):
        reconcile_run(make_store(tmp_path), RUN_ID)


def test_reconcile_fails_fast_on_unknown_run_json_schema(tmp_path):
    """A run.json from a future schema version is never rebuilt over."""
    complete_run(make_store(tmp_path))
    path = run_dir(tmp_path) / "run.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["runtime_schema_version"] = 2
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ProjectionSchemaError):
        reconcile_run(make_store(tmp_path), RUN_ID)


def test_reconcile_unknown_run_raises(tmp_path):
    with pytest.raises(RunNotFoundError):
        reconcile_run(make_store(tmp_path), "ghost-run")


def test_reconcile_never_calls_an_executor(tmp_path):
    """The crash protocol appends facts only; there is no re-execution path."""
    start_run(make_store(tmp_path))
    outcome = reconcile_run(make_store(tmp_path), RUN_ID)
    assert len(outcome.appended_events) == 1
    assert all(
        e.event_type not in (EventType.ATTEMPT_STARTED, EventType.INVOCATION_STARTED)
        for e in outcome.appended_events
    )


def test_reconcile_contradictory_history_fails_fast(tmp_path):
    """A history the reducer cannot interpret (corruption, manual tampering)
    fails fast instead of being 'reconciled' into a new shape. The tampered
    line is written straight to disk: the append guard is not in play here."""
    store = make_store(tmp_path)
    store.create_run(make_created_run())
    orphan = attempt_succeeded_event()  # success for an attempt never created
    path = run_dir(tmp_path) / "execution.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "event_id": orphan.event_id,
                    "event_type": orphan.event_type.value,
                    "schema_version": orphan.schema_version,
                    "timestamp": orphan.timestamp,
                    "run_id": orphan.run_id,
                    "invocation_id": orphan.invocation_id,
                    "step_id": orphan.step_id,
                    "attempt_id": orphan.attempt_id,
                    "payload": dict(orphan.payload),
                }
            )
            + "\n"
        )
    with pytest.raises(RuntimeContractError):
        reconcile_run(make_store(tmp_path), RUN_ID)
