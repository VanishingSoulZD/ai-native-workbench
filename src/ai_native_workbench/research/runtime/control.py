"""Research Runtime control plane (Task 6, Spec 6.4/15, architecture 6.4).

:class:`ResearchRuntime` is the explicit control surface over the durable
execution state: every action loads the projected Run/Invocation/Attempt/Gate
state, enforces *who may call what* from that state, and drives the
:class:`~orchestrator.Orchestrator`. Illegal actions raise
:class:`ControlError` (a ``RuntimeContractError``) naming the state conflict
— the runtime never guesses and never silently repairs.

Control semantics (Spec 15):

- ``create_run`` freezes the Case binding and creates a CREATED Run.
- ``start`` (CREATED only) opens a START Invocation for the full v1 scope
  (or a bounded ``--until`` prefix, EntryMode UNTIL) and runs it to the
  first stop condition: a pending Gate Barrier, a failure, or bounded
  completion (completion_reason ``BOUNDED_SCOPE``, Spec 6.2/15.5).
- ``resume`` (COMPLETED / NEEDS_REVISION / FAILED, or a RUNNING Run whose
  active invocation holds a failed attempt — the stranded state left by
  crash reconciliation, Ruling 7) opens a new Invocation for the same Run:
  from the next uncompleted node (COMPLETED), from the failing step
  (FAILED), or from the revision target recorded by the rejecting Gate
  (NEEDS_REVISION — entry validated against the workflow, Spec 6.5). A
  stranded RUNNING invocation is first closed durably as FAILED with its
  recorded disposition.
- ``retry`` (RUNNING, Invocation RUNNING, latest Attempt PENDING/FAILED)
  stays within the same Attempt + Invocation (Spec 15.1).
- ``rerun`` (RUNNING, Invocation RUNNING, latest Attempt not RUNNING)
  creates a new Attempt inside the current Invocation and rebuilds the
  downstream lineage (Spec 15.2); downstream checkpoints are invalidated by
  default (Spec 12).
- ``run_from`` (as resume; CREATED/WAITING refused) opens a FROM Invocation
  at an exact-compatible VALID checkpoint boundary of *step_id* (Spec 12.1:
  the entry checkpoint is validated exactly — mismatch is an explicit
  error, never a fuzzy fallback), invalidates the old path's downstream
  checkpoints and rebuilds the downstream lineage with fresh Attempts.
- ``decide_gate`` records the whole-set decision; an APPROVED gate on the
  current lineage resumes progression (the derived WAITING state resolves),
  a REJECTED gate fails the active Invocation with HUMAN_REJECTION so the
  Run derives NEEDS_REVISION (never an automatic re-run, Spec 6.3/15), and
  a decision on a superseded Gate is recorded as a review fact only —
  superseded approvals/rejections never authorize or redirect progression
  (Spec 13.2, Ruling 2).

Every action returns the freshly projected RunRecord (derived by the store
from the authoritative event history, Ruling 10).
"""

import uuid
from pathlib import Path

from .binding import ExecutionConfiguration, ResearchCase, freeze_case_binding
from .checkpoints import invalidate_downstream
from .domain import (
    AttemptStatus,
    EntryMode,
    EventType,
    GateDecision,
    InvocationStatus,
    RevisionTarget,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from .execution import ExecutorRegistry
from .gates.runtime import GateRuntime
from .orchestrator import (
    RUNTIME_CONFIGURATION_IDENTITY,
    Orchestrator,
    TerminalPhaseHook,
)
from .reconciliation import EXECUTION_INTERRUPTED
from .source.acquisition import SourceAcquisitionService
from .store import HUMAN_REJECTION, RuntimeStore, reduce_events
from .workflow import (
    STANDARD_NODE_IDS,
    STANDARD_WORKFLOW_ID,
    STANDARD_WORKFLOW_VERSION,
    StandardResearchWorkflow,
    build_standard_workflow,
    scope_nodes,
    validate_entry_boundary,
)


class ControlError(RuntimeContractError):
    """Raised when a control action is illegal in the projected run state.

    The message always names the conflict (the run state, the attempt
    status, the missing checkpoint, ...); the runtime never silently
    repairs a state the operator did not ask to change.
    """


class ResearchRuntime:
    """The explicit control surface of the Research Runtime (see module docs)."""

    def __init__(
        self,
        store: RuntimeStore,
        *,
        cases_dir: str | Path = "cases",
        workflow: StandardResearchWorkflow | None = None,
        execution_config: ExecutionConfiguration | None = None,
        registry: ExecutorRegistry | None = None,
        acquisition: SourceAcquisitionService | None = None,
        domain_checks: dict | None = None,
        terminal_phase: TerminalPhaseHook | None = None,
    ) -> None:
        self._store = store
        self._workflow = workflow or build_standard_workflow()
        self._config = execution_config or ExecutionConfiguration(
            workflow_identity=STANDARD_WORKFLOW_ID,
            workflow_version=STANDARD_WORKFLOW_VERSION,
            runtime_configuration_identity=RUNTIME_CONFIGURATION_IDENTITY,
        )
        self._gates = GateRuntime(store, self._workflow)
        self._orchestrator = Orchestrator(
            store,
            workflow=self._workflow,
            execution_config=self._config,
            registry=registry,
            gates=self._gates,
            acquisition=acquisition,
            cases_dir=cases_dir,
            domain_checks=domain_checks,
            terminal_phase=terminal_phase,
        )

    # -- run lifecycle --------------------------------------------------------

    def create_run(self, case: ResearchCase) -> RunRecord:
        """Create a CREATED Run freezing the Case binding (Spec 5.1/16.1)."""
        binding = freeze_case_binding(case)
        run = RunRecord(
            run_id=f"run-{uuid.uuid4().hex}",
            case_id=binding.case_id,
            case_binding=binding,
            state=RunState.CREATED,
            cumulative_execution_scope=(),
            current_invocation_id=None,
            completion_reason=None,
        )
        self._store.create_run(run)
        return self._load(run.run_id)

    def start(self, run_id: str, *, until_step: str | None = None) -> RunRecord:
        """Start a CREATED Run: a new Invocation for the (bounded) v1 scope."""
        run = self._load(run_id)
        if run.state is not RunState.CREATED:
            raise ControlError(
                f"run {run_id} is {run.state.value}; start is only legal on "
                "a CREATED run (resume continues a non-CREATED run)."
            )
        full = scope_nodes(self._workflow, STANDARD_NODE_IDS)
        scope = self._bounded_scope(full, until_step)
        mode = EntryMode.UNTIL if until_step is not None else EntryMode.START
        return self._execute_invocation(
            run_id, scope, mode, from_step=None, until_step=until_step
        )

    def resume(self, run_id: str, *, until_step: str | None = None) -> RunRecord:
        """Continue the Run from its current durable state (Spec 15.3).

        On NEEDS_REVISION the entry is the rejecting Gate's validated
        revision target; on FAILED it is the failing step (or the first node
        for an acquisition failure); on COMPLETED it is the next uncompleted
        node. A stranded RUNNING invocation (a failed attempt under a
        RUNNING invocation, Ruling 7) is closed durably first.
        """
        run = self._load(run_id)
        projection = reduce_events(self._store.events(run_id))
        if run.state is RunState.CREATED:
            raise ControlError(
                f"run {run_id} is CREATED; start it before resuming."
            )
        if run.state is RunState.WAITING_FOR_HUMAN:
            raise ControlError(
                f"run {run_id} is WAITING_FOR_HUMAN; decide the pending Gate "
                "first — resume never bypasses a human decision."
            )
        if run.state is RunState.RUNNING:
            entry = self._close_stranded(run, projection)
        else:
            entry = self._resume_entry(run, projection)
        full = scope_nodes(self._workflow, STANDARD_NODE_IDS)
        scope = self._scope_from_entry(full, entry, until_step)
        mode = EntryMode.UNTIL if until_step is not None else EntryMode.RESUME
        self._invalidate_downstream_of(run_id, entry)
        return self._execute_invocation(
            run_id, scope, mode, from_step=None, until_step=until_step, entry_step=entry
        )

    def run_from(self, run_id: str, step_id: str, *, until_step: str | None = None) -> RunRecord:
        """Rebuild the downstream path from *step_id* (Spec 12.1/15.4).

        The entry boundary checkpoint must be exact-compatible and VALID;
        the old path's downstream checkpoints are invalidated and fresh
        Attempts/Gates rebuild the lineage.
        """
        run = self._load(run_id)
        projection = reduce_events(self._store.events(run_id))
        validate_entry_boundary(self._workflow, step_id)
        if run.state is RunState.CREATED:
            raise ControlError(
                f"run {run_id} is CREATED; run_from needs an existing path "
                "with a checkpoint boundary."
            )
        if run.state is RunState.WAITING_FOR_HUMAN:
            raise ControlError(
                f"run {run_id} is WAITING_FOR_HUMAN; decide the pending Gate "
                "before rebuilding a path."
            )
        if run.state is RunState.RUNNING:
            self._close_stranded(run, projection)
        full = scope_nodes(self._workflow, STANDARD_NODE_IDS)
        scope = self._scope_from_entry(full, step_id, until_step)
        self._invalidate_downstream_of(run_id, step_id)
        return self._execute_invocation(
            run_id,
            scope,
            EntryMode.FROM,
            from_step=step_id,
            until_step=until_step,
            entry_step=step_id,
        )

    # -- attempt-level controls -----------------------------------------------

    def retry(self, run_id: str, step_id: str) -> RunRecord:
        """Retry the same Attempt within the current Invocation (Spec 15.1).

        Legal from a PENDING or FAILED attempt; the Attempt and Invocation
        identities never change.
        """
        run = self._load(run_id)
        projection = reduce_events(self._store.events(run_id))
        self._require_running_run(run)
        validate_entry_boundary(self._workflow, step_id)
        invocation = self._active_invocation(run, projection)
        attempt = self._latest_attempt(projection, invocation, step_id)
        if attempt is None:
            raise ControlError(
                f"step {step_id!r} has no attempt in invocation "
                f"{invocation.invocation_id!r}; retry re-executes an "
                "existing attempt."
            )
        if attempt.status is AttemptStatus.RUNNING:
            raise ControlError(
                f"attempt {attempt.attempt_id} is RUNNING; reconcile first — "
                "retry never touches an active attempt."
            )
        if attempt.status is AttemptStatus.SUCCEEDED:
            raise ControlError(
                f"attempt {attempt.attempt_id} succeeded; retry re-executes "
                "only PENDING/FAILED attempts (use rerun for a new lineage)."
            )
        self._orchestrator.retry_attempt(
            run_id, invocation.invocation_id, step_id, attempt
        )
        self._orchestrator.continue_execution(run_id, invocation.invocation_id)
        return self._load(run_id)

    def rerun(self, run_id: str, step_id: str) -> RunRecord:
        """Create a new Attempt for *step_id* inside the current Invocation.

        The old path's downstream checkpoints are invalidated by default
        (Spec 12); the new Attempt rebuilds the artifact lineage.
        """
        run = self._load(run_id)
        projection = reduce_events(self._store.events(run_id))
        self._require_running_run(run)
        validate_entry_boundary(self._workflow, step_id)
        invocation = self._active_invocation(run, projection)
        attempt = self._latest_attempt(projection, invocation, step_id)
        if attempt is None:
            raise ControlError(
                f"step {step_id!r} has no attempt in invocation "
                f"{invocation.invocation_id!r}; rerun replaces an existing "
                "attempt of the current invocation."
            )
        if attempt.status is AttemptStatus.RUNNING:
            raise ControlError(
                f"attempt {attempt.attempt_id} is RUNNING; reconcile first — "
                "rerun never races an active attempt."
            )
        invalidate_downstream(
            self._store, run_id, step_id, workflow=self._workflow.definition
        )
        self._orchestrator.continue_execution(
            run_id, invocation.invocation_id, cut_step=step_id
        )
        return self._load(run_id)

    # -- gate decisions ---------------------------------------------------------

    def decide_gate(
        self,
        run_id: str,
        gate_id: str,
        decision: GateDecision,
        reviewer: str,
        comment: str,
        revision_target: RevisionTarget | None = None,
    ) -> RunRecord:
        """Record a whole-set Gate decision and apply its effect (Spec 13).

        APPROVED on the current lineage resumes progression from the
        barrier; REJECTED fails the active Invocation with HUMAN_REJECTION
        (the Run derives NEEDS_REVISION); decisions on superseded Gates are
        recorded as historical review facts only.
        """
        projection = reduce_events(self._store.events(run_id))
        gate = projection.gates.get(gate_id)
        if gate is None or gate.run_id != run_id:
            raise ControlError(
                f"gate {gate_id!r} is not recorded in run {run_id!r}."
            )
        decided = self._gates.decide(
            gate_id, decision, reviewer, comment, revision_target
        )
        projection = reduce_events(self._store.events(run_id))
        if decided.superseded_by is not None:
            return self._load(run_id)  # review fact on a historical path
        if decision is GateDecision.REJECTED:
            invocation_id = projection.run.current_invocation_id
            if invocation_id is None:
                raise ControlError(
                    f"run {run_id} has no active invocation for the "
                    "rejection to close."
                )
            self._orchestrator.fail_invocation(
                run_id, invocation_id, HUMAN_REJECTION
            )
            return self._load(run_id)
        if projection.run.state is RunState.WAITING_FOR_HUMAN:
            return self._load(run_id)  # another pending Gate still blocks
        invocation_id = projection.run.current_invocation_id
        if invocation_id is None:
            raise ControlError(
                f"run {run_id} has no active invocation to continue."
            )
        self._orchestrator.continue_execution(run_id, invocation_id)
        return self._load(run_id)

    # -- internal: entry/scope computation -------------------------------------

    def _bounded_scope(self, full, until_step: str | None) -> tuple[str, ...]:
        if until_step is None:
            return full
        validate_entry_boundary(self._workflow, until_step)
        if until_step not in full:
            raise ControlError(
                f"until_step {until_step!r} is not part of the v1 workflow "
                f"definition {tuple(full)}."
            )
        return full[: full.index(until_step) + 1]

    def _scope_from_entry(self, full, entry: str, until_step: str | None) -> tuple[str, ...]:
        end = full[-1]
        if until_step is not None:
            validate_entry_boundary(self._workflow, until_step)
            end = until_step
        if full.index(end) < full.index(entry):
            raise ControlError(
                f"until_step {until_step!r} sits upstream of the entry "
                f"{entry!r}; a bounded scope must contain its entry."
            )
        return full[full.index(entry) : full.index(end) + 1]

    def _resume_entry(self, run: RunRecord, projection) -> str:
        if run.state is RunState.NEEDS_REVISION:
            for gate in reversed(list(projection.gates.values())):
                if (
                    gate.superseded_by is None
                    and gate.decision is GateDecision.REJECTED
                    and gate.revision_target is not None
                ):
                    entry = gate.revision_target.entry_step
                    validate_entry_boundary(self._workflow, entry)
                    return entry
            raise ControlError(
                f"run {run.run_id} is NEEDS_REVISION but no non-superseded "
                "REJECTED Gate records a revision target; resume requires "
                "an explicit revision target (Spec 6.5)."
            )
        if run.state is RunState.COMPLETED:
            full = scope_nodes(self._workflow, STANDARD_NODE_IDS)
            remaining = [
                node for node in full if node not in run.cumulative_execution_scope
            ]
            if not remaining:
                raise ControlError(
                    f"run {run.run_id} already completed the v1 scope "
                    f"{tuple(full)}; nothing to resume."
                )
            return remaining[0]
        if run.state is RunState.FAILED:
            for event in reversed(self._store.events(run.run_id)):
                if event.event_type is EventType.ATTEMPT_FAILED:
                    validate_entry_boundary(self._workflow, event.step_id)
                    return event.step_id
            return scope_nodes(self._workflow, STANDARD_NODE_IDS)[0]
        raise ControlError(
            f"run {run.run_id} is {run.state.value}; resume is not legal "
            "from this state."
        )

    def _close_stranded(self, run: RunRecord, projection) -> str:
        """Close a stranded RUNNING invocation; return the failed step."""
        invocation = projection.invocations.get(run.current_invocation_id)
        if invocation is None or invocation.status is not InvocationStatus.RUNNING:
            raise ControlError(
                f"run {run.run_id} is RUNNING without an active invocation."
            )
        for attempt in reversed(list(projection.attempts.values())):
            if attempt.invocation_id != invocation.invocation_id:
                continue
            if attempt.status is AttemptStatus.FAILED:
                disposition = projection.failure_dispositions.get(
                    attempt.attempt_id, EXECUTION_INTERRUPTED
                )
                self._orchestrator.fail_invocation(
                    run.run_id, invocation.invocation_id, disposition
                )
                return attempt.step_id
            raise ControlError(
                f"run {run.run_id} is RUNNING with attempt "
                f"{attempt.attempt_id} {attempt.status.value}; the stranded "
                "state to close is a FAILED attempt (reconcile first, or "
                "use retry/rerun)."
            )
        raise ControlError(
            f"run {run.run_id} is RUNNING with an empty active invocation; "
            "nothing stranded to close."
        )

    def _invalidate_downstream_of(self, run_id: str, entry_step: str) -> None:
        node = self._node(entry_step)
        for predecessor_id in node.depends_on:
            invalidate_downstream(
                self._store,
                run_id,
                predecessor_id,
                workflow=self._workflow.definition,
            )

    def _execute_invocation(
        self,
        run_id: str,
        scope: tuple[str, ...],
        mode: EntryMode,
        *,
        from_step: str | None,
        until_step: str | None,
        entry_step: str | None = None,
    ) -> RunRecord:
        """Open an Invocation, acquire sources, execute to a stop condition."""
        invocation = self._orchestrator.open_invocation(
            run_id, scope, mode, from_step=from_step, until_step=until_step
        )
        run = self._load(run_id)
        result = self._orchestrator.acquire_sources(run)
        if result.blocked:
            return self._load(run_id)
        if entry_step is not None:
            entry = self._orchestrator.entry_context(
                run_id, invocation.invocation_id, entry_step
            )
            self._orchestrator.continue_execution(
                run_id, invocation.invocation_id, cut_step=entry_step, entry=entry
            )
        else:
            self._orchestrator.continue_execution(run_id, invocation.invocation_id)
        return self._load(run_id)

    # -- internal: lookups --------------------------------------------------------

    def _load(self, run_id: str) -> RunRecord:
        return self._store.load_run(run_id)

    def _node(self, step_id: str):
        for node in self._workflow.definition.steps:
            if node.step.id == step_id:
                return node
        raise ControlError(
            f"step {step_id!r} is not part of workflow "
            f"{self._workflow.definition.id!r}."
        )

    def _require_running_run(self, run: RunRecord) -> None:
        if run.state is not RunState.RUNNING:
            raise ControlError(
                f"run {run.run_id} is {run.state.value}; the action requires "
                "a RUNNING run."
            )

    @staticmethod
    def _active_invocation(run: RunRecord, projection):
        invocation = projection.invocations.get(run.current_invocation_id)
        if invocation is None or invocation.status is not InvocationStatus.RUNNING:
            raise ControlError(
                f"run {run.run_id} has no RUNNING invocation for this action "
                f"(current invocation: {run.current_invocation_id!r})."
            )
        return invocation

    @staticmethod
    def _latest_attempt(projection, invocation, step_id: str):
        attempts = [
            attempt
            for attempt in projection.attempts.values()
            if attempt.invocation_id == invocation.invocation_id
            and attempt.step_id == step_id
        ]
        return attempts[-1] if attempts else None
