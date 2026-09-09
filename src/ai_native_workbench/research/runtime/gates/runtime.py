"""Human Gate Runtime (Task 6, Spec section 13).

A Gate is an immutable review fact, never a state machine of its own:
``GateDecision`` stays PENDING/APPROVED/REJECTED and supersession is an
immutable *relationship* between records (Spec 13.2) — there is no
INVALIDATED Gate state. ``GateRuntime`` persists those facts through the
Task 2 store (GATE_CREATED / GATE_DECIDED / GATE_SUPERSEDED); the store's
reduce-before-append guard is the authoritative backstop, and every call
pre-validates so contract violations raise RuntimeContractError instead of
the store's append-time EventConflictError.

- ``create`` binds a Gate to a concrete Artifact/Candidate Set
  (``ReviewTarget``, Spec 13.1): every artifact must already be committed
  to the Gate's own run, the reviewed Attempt must exist and match the
  target's step. The Gate id is emitter-chosen (Ruling 11).
- ``decide`` records the whole-set APPROVE/REJECT on a still-PENDING gate.
  REJECT without a validated ``RevisionTarget`` raises RuntimeContractError
  (the brief's verbatim contract). When this runtime was constructed with
  the ``StandardResearchWorkflow``, the revision entry boundary is
  validated against the workflow dependency graph: the entry step must be
  an ancestor-or-self of the rejecting barrier's ``before_step`` — an entry
  downstream of what must be revised is refused (Spec 6.5/13.3).
- ``replace`` records the supersession relationship for a new execution
  path: the new Gate carries ``supersedes`` (persisted on GATE_CREATED),
  the prior Gate is marked ``superseded_by`` (GATE_SUPERSEDED), and the new
  Gate inherits the prior gate's logical identity. A Gate can be superseded
  exactly once; a superseded Gate stays writable as a review fact but never
  authorizes progression (that authority check lives in the control layer).

Gate resolution: ``decide``/``replace`` take only a ``gate_id``, so the
runtime resolves the owning Run from its instance directory (gates it
created/replaced in this process) and, when the store is filesystem-backed,
by scanning the durable event logs under the store root — a fresh instance
mirrors a process restart and still resolves gates recorded before it.
"""

import uuid
from pathlib import Path

from ..domain import (
    EventEnvelope,
    EventType,
    GateDecision,
    GateRecord,
    ReviewTarget,
    RevisionTarget,
    RuntimeContractError,
    utc_now,
)
from ..store import EventLog, RunNotFoundError, RuntimeStore, reduce_events
from ..workflow import StandardResearchWorkflow, validate_entry_boundary

_PENDING = GateDecision.PENDING


def _require_text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeContractError(f"{name} must be a non-empty string.")
    return value


class GateRuntime:
    """Durable Human Gate review facts (see module docstring)."""

    def __init__(
        self, store: RuntimeStore, workflow: StandardResearchWorkflow | None = None
    ) -> None:
        self._store = store
        self._workflow = workflow
        self._gate_runs: dict[str, str] = {}

    # -- public surface ------------------------------------------------------

    def create(
        self, run_id: str, logical_gate_id: str, target: ReviewTarget
    ) -> GateRecord:
        """Create a PENDING Gate reviewing the concrete *target* set."""
        _require_text(run_id, "run_id")
        _require_text(logical_gate_id, "logical_gate_id")
        self._require_review_target(target, run_id)
        events = self._events_of(run_id)
        projection = reduce_events(events)
        self._require_active_run(projection.run.state, run_id)
        gate_id = f"gate-{uuid.uuid4().hex}"
        gate = GateRecord(
            gate_id=gate_id,
            run_id=run_id,
            logical_gate_id=logical_gate_id,
            review_target=target,
            decision=_PENDING,
            created_at=utc_now(),
        )
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.GATE_CREATED,
                timestamp=gate.created_at,
                run_id=run_id,
                gate_id=gate_id,
                payload={
                    "logical_gate_id": logical_gate_id,
                    "review_target": {
                        "step_id": target.step_id,
                        "attempt_id": target.attempt_id,
                        "artifact_ids": list(target.artifact_ids),
                    },
                },
            )
        )
        self._gate_runs[gate_id] = run_id
        return gate

    def decide(
        self,
        gate_id: str,
        decision: GateDecision,
        reviewer: str,
        comment: str,
        revision_target: RevisionTarget | None = None,
    ) -> GateRecord:
        """Record the whole-set decision on a still-PENDING Gate.

        REJECTED requires a validated RevisionTarget (the brief's verbatim
        contract); APPROVED refuses one. When the workflow is known the
        revision entry boundary is validated against the barrier's revision
        boundary (ancestor-or-self of the barrier's ``before_step``).
        """
        _require_text(gate_id, "gate_id")
        _require_text(reviewer, "reviewer")
        _require_text(comment, "comment")
        if decision not in (GateDecision.APPROVED, GateDecision.REJECTED):
            raise RuntimeContractError(
                f"gate {gate_id} decision must be APPROVED or REJECTED "
                f"(got {decision.value!r}); PENDING is not a decision."
            )
        if revision_target is None:
            if decision is GateDecision.REJECTED:
                raise RuntimeContractError(
                    f"gate {gate_id} is REJECTED without a revision target; "
                    "a rejection must name the minimum re-execution boundary "
                    "(Spec 6.5)."
                )
        elif decision is not GateDecision.REJECTED:
            raise RuntimeContractError(
                f"gate {gate_id} decision {decision.value} cannot carry a "
                "revision target; only REJECTED gates request revision."
            )
        run_id = self._resolve_run(gate_id)
        projection = reduce_events(self._events_of(run_id))
        gate = projection.gates.get(gate_id)
        if gate is None:
            raise RuntimeContractError(
                f"gate {gate_id!r} is not recorded in run {run_id!r}."
            )
        if revision_target is not None:
            self._validate_revision_boundary(gate, revision_target)
        decided = gate.decide(
            decision, reviewer, utc_now(), comment=comment,
            revision_target=revision_target,
        )
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.GATE_DECIDED,
                timestamp=decided.decided_at,
                run_id=run_id,
                gate_id=gate_id,
                payload=self._decision_payload(decided),
            )
        )
        return decided

    def replace(
        self, prior_gate_id: str, target: ReviewTarget, gate_id: str
    ) -> GateRecord:
        """Create the replacement Gate of a new execution path (Spec 13.2).

        Persists both relationship facts: the new Gate carries ``supersedes``
        (its GATE_CREATED payload) and the prior Gate is marked
        ``superseded_by`` (GATE_SUPERSEDED). The new Gate inherits the prior
        gate's logical identity; its decision starts PENDING.
        """
        _require_text(prior_gate_id, "prior_gate_id")
        _require_text(gate_id, "gate_id")
        if gate_id == prior_gate_id:
            raise RuntimeContractError(
                f"gate {gate_id} cannot supersede itself."
            )
        run_id = self._resolve_run(prior_gate_id)
        projection = reduce_events(self._events_of(run_id))
        prior = projection.gates.get(prior_gate_id)
        if prior is None:
            raise RuntimeContractError(
                f"prior gate {prior_gate_id!r} is not recorded in run "
                f"{run_id!r}."
            )
        if prior.superseded_by is not None:
            raise RuntimeContractError(
                f"gate {prior_gate_id} is already superseded by "
                f"{prior.superseded_by!r}; a gate is superseded exactly once."
            )
        if gate_id in projection.gates:
            raise RuntimeContractError(
                f"gate id {gate_id!r} is already recorded in run {run_id!r}."
            )
        self._require_review_target(target, run_id)
        self._require_active_run(projection.run.state, run_id)
        replacement = GateRecord(
            gate_id=gate_id,
            run_id=run_id,
            logical_gate_id=prior.logical_gate_id,
            review_target=target,
            decision=_PENDING,
            created_at=utc_now(),
            supersedes=prior_gate_id,
        )
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.GATE_CREATED,
                timestamp=replacement.created_at,
                run_id=run_id,
                gate_id=gate_id,
                payload={
                    "logical_gate_id": prior.logical_gate_id,
                    "review_target": {
                        "step_id": target.step_id,
                        "attempt_id": target.attempt_id,
                        "artifact_ids": list(target.artifact_ids),
                    },
                    "supersedes": prior_gate_id,
                },
            )
        )
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.GATE_SUPERSEDED,
                timestamp=utc_now(),
                run_id=run_id,
                gate_id=prior_gate_id,
                payload={"superseded_by": gate_id},
            )
        )
        self._gate_runs[gate_id] = run_id
        return replacement

    # -- internal helpers ----------------------------------------------------

    def _events_of(self, run_id: str):
        try:
            return self._store.events(run_id)
        except RunNotFoundError as error:
            raise RuntimeContractError(
                f"run {run_id!r} does not exist in the store."
            ) from error

    @staticmethod
    def _require_active_run(state, run_id: str) -> None:
        from ..domain import RunState  # local import keeps the top clean

        if state not in (RunState.RUNNING, RunState.WAITING_FOR_HUMAN):
            raise RuntimeContractError(
                f"run {run_id} is {state.value}; gates are created only on "
                "an active (RUNNING or WAITING_FOR_HUMAN) run."
            )

    def _require_review_target(self, target: object, run_id: str) -> None:
        if not isinstance(target, ReviewTarget):
            raise RuntimeContractError(
                "a gate binds to a concrete ReviewTarget "
                f"(got {target!r})."
            )
        projection = reduce_events(self._events_of(run_id))
        for artifact_id in target.artifact_ids:
            if artifact_id not in projection.artifacts:
                raise RuntimeContractError(
                    f"gate review target names artifact {artifact_id!r}, "
                    "which is not a committed artifact of run "
                    f"{run_id!r}; gates bind to concrete committed "
                    "Candidate Sets only (Spec 13.1)."
                )
        attempt = projection.attempts.get(target.attempt_id)
        if attempt is None:
            raise RuntimeContractError(
                f"gate review target names attempt {target.attempt_id!r}, "
                f"which was never created in run {run_id!r}."
            )
        if attempt.step_id != target.step_id:
            raise RuntimeContractError(
                f"gate review target step {target.step_id!r} does not match "
                f"the reviewed attempt's step {attempt.step_id!r}."
            )

    def _validate_revision_boundary(
        self, gate: GateRecord, revision_target: RevisionTarget
    ) -> None:
        """Refuse a revision entry downstream of the barrier's boundary."""
        if self._workflow is None:
            return
        validate_entry_boundary(self._workflow, revision_target.entry_step)
        barrier = self._workflow.gate_barriers.get(gate.logical_gate_id)
        if barrier is None:
            return
        node_ids = tuple(
            node.step.id for node in self._workflow.definition.steps
        )
        if barrier.before_step not in node_ids:
            return  # the barrier guards a boundary outside this definition
        if not _is_ancestor_or_self(
            self._workflow, revision_target.entry_step, barrier.before_step
        ):
            raise RuntimeContractError(
                f"revision entry step {revision_target.entry_step!r} sits "
                f"downstream of the {gate.logical_gate_id} revision boundary "
                f"({barrier.before_step!r}); the entry must be an "
                "ancestor-or-self of the barrier's downstream step "
                "(Spec 6.5)."
            )

    @staticmethod
    def _decision_payload(gate: GateRecord) -> dict:
        payload: dict = {
            "decision": gate.decision.value,
            "reviewer": gate.reviewer,
            "decided_at": gate.decided_at,
            "comment": gate.comment,
        }
        if gate.revision_target is not None:
            payload["revision_target"] = {
                "entry_step": gate.revision_target.entry_step,
                "reason": gate.revision_target.reason,
            }
        return payload

    def _resolve_run(self, gate_id: str) -> str:
        """Resolve the owning Run of *gate_id* (instance memory + store scan)."""
        known = self._gate_runs.get(gate_id)
        if known is not None:
            return known
        root = getattr(self._store, "root", None)
        if root is not None:
            found: list[str] = []
            for log_path in sorted(Path(root).glob("cases/*/runs/*/execution.jsonl")):
                run_id = log_path.parent.name
                log = EventLog(log_path, run_id)
                if any(event.gate_id == gate_id for event in log.events):
                    found.append(run_id)
            if len(found) == 1:
                self._gate_runs[gate_id] = found[0]
                return found[0]
            if len(found) > 1:
                raise RuntimeContractError(
                    f"gate {gate_id!r} is recorded under multiple runs "
                    f"{found}; gate ids are runtime-wide identities."
                )
        raise RuntimeContractError(
            f"gate {gate_id!r} is not known to this gate runtime; load the "
            "run projection to resolve its gates first."
        )


def _is_ancestor_or_self(
    workflow: StandardResearchWorkflow, candidate: str, target: str
) -> bool:
    """True when *candidate* is an ancestor-or-self of *target* over the
    workflow's dependency edges."""
    if candidate == target:
        return True
    dependencies: dict[str, tuple[str, ...]] = {
        node.step.id: node.depends_on for node in workflow.definition.steps
    }
    frontier = list(dependencies.get(target, ()))
    visited: set[str] = set()
    while frontier:
        node = frontier.pop()
        if node in visited:
            continue
        visited.add(node)
        if node == candidate:
            return True
        frontier.extend(dependencies.get(node, ()))
    return False
