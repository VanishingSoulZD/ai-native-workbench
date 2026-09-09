"""Single-process sequential Research orchestration (Task 6, Spec 7.1).

The Orchestrator is the runtime's execution engine: it resolves Workflow
nodes through the Standard Research Workflow adapter and Workflow Core's
topological order, resolves Executors through :class:`ExecutorRegistry` by
execution-mode string (never by step id), persists lifecycle facts through
the Task 2 store, and stops at Gate Barriers or failures. It contains no
``if step_id == "R1"`` dispatch: the only step-id-keyed data is the
documented execution-spec table below (Ruling 9), and even that only feeds
the registry/pipeline — all execution flows through one generic attempt
protocol.

Attempt protocol (Spec 5.5, Ruling 14)::

    ATTEMPT_CREATED -> INPUT_BOUND -> ATTEMPT_STARTED -> Executor
    -> VALIDATION_COMPLETED -> ACCEPTANCE_RECORDED
    -> ARTIFACT_COMMITTED -> ATTEMPT_SUCCEEDED -> CHECKPOINT_CREATED

Exactly one output artifact (the accepted candidate payload) is committed
per attempt round; acceptance dispositions precede the commit they
authorize. A rejected candidate records its validation/acceptance
dispositions durably, then the attempt fails with disposition
``ACCEPTANCE_REJECTED`` — the Invocation and Run fail with it (ordinary
execution failure is never NEEDS_REVISION, Spec 6.3). Under the human
policy the disposition is ``DEFERRED_TO_HUMAN``: the candidate is committed
and the attempt succeeds, and progression stops at the following Gate
Barrier whose review target is that concrete candidate set.

Gate barriers (Spec 13): before executing a node a barrier guards, the
orchestrator checks the latest non-superseded Gate for the logical gate id.
A pending Gate stops the loop (the Run's WAITING_FOR_HUMAN state is derived
by the reducer); an APPROVED Gate authorizes progression only when its
review target matches the current lineage (the latest successful attempt of
the barrier's upstream step and its committed artifact set) — a mismatch
creates a replacement Gate via :class:`GateRuntime.replace` and stops. H4 is
honored as metadata whose before_step (R7) is beyond the v1 definition, so
a v1 scheduler never raises or fabricates it.

Checkpoints (Spec 12): every successful step boundary records a checkpoint
with the step's CompatibilityIdentity and its committed artifact set.
Entry-boundary validation and downstream invalidation belong to the control
layer (Task 6 ``control.py``).

Task 7 seam (Ruling 10): when an invocation's requested scope reaches the
terminal node of the workflow definition (R5), the orchestrator calls the
optional ``terminal_phase`` hook *after* the terminal attempt's success and
checkpoint, *before* emitting INVOCATION_COMPLETED. The hook receives
``(store, projection, invocation, terminal_attempt)`` and must not emit
INVOCATION_COMPLETED itself; Task 7 supplies the hook implementing canonical
registration (CANONICAL_BINDING_PENDING/COMMITTED) and snapshot binding
(SNAPSHOT_BOUND). Bounded scopes that end before the terminal node never
call the hook.

Disposition vocabulary (documented, kept short and stable):

- ``ACCEPTANCE_REJECTED`` — validation/acceptance rejected the candidate.
- ``EXECUTOR_FAILED`` — the executor raised during execution.
- ``ACQUISITION_FAILED`` — a required declared source could not be acquired
  (invocation completion_reason; per-source details stay in the
  AcquisitionResult, v1 owns no event type for them, Task 5 note).
- ``BOUNDED_SCOPE`` — the requested scope completed (completion_reason).
- ``HUMAN_REJECTION`` / ``EXECUTION_INTERRUPTED`` — projection/reconciliation
  vocabulary (Task 2), reused verbatim.
"""

import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from ..workflow.composition import execution_order
from .artifacts import commit_artifact, persist_input_binding
from .binding import (
    ExecutionBinding,
    ExecutionConfiguration,
    freeze_execution_binding,
    load_research_case,
)
from .checkpoints import create_checkpoint, validate_checkpoint
from .domain import (
    ArtifactEnvelope,
    AttemptRecord,
    AttemptStatus,
    CheckpointRecord,
    CheckpointStatus,
    CompatibilityIdentity,
    EntryMode,
    EventEnvelope,
    EventType,
    GateDecision,
    InputBinding,
    InvocationRecord,
    InvocationStatus,
    ReviewTarget,
    RunRecord,
    RuntimeContractError,
    utc_now,
)
from .execution import (
    DETERMINISTIC_MODE,
    DETERMINISTIC_SCHEMA_VERSION,
    AcceptanceDisposition,
    AcceptancePipeline,
    AcceptancePolicy,
    DeterministicExecutor,
    ExecutorRegistry,
    SchemaSpec,
    ValidationDimension,
)
from .gates.runtime import GateRuntime
from .reconciliation import EXECUTION_INTERRUPTED
from .source.acquisition import AcquisitionResult, SourceAcquisitionService
from .store import HUMAN_REJECTION, RunProjection, RuntimeStore, reduce_events
from .workflow import (
    STANDARD_WORKFLOW_ID,
    STANDARD_WORKFLOW_VERSION,
    StandardResearchWorkflow,
    build_standard_workflow,
    scope_nodes,
)

COMPLETION_BOUNDED_SCOPE = "BOUNDED_SCOPE"
"""Invocation completion_reason of a successfully reached scope boundary."""

COMPLETION_ACQUISITION_FAILED = "ACQUISITION_FAILED"
"""Invocation completion_reason when a required source blocks acquisition."""

DISPOSITION_ACCEPTANCE_REJECTED = "ACCEPTANCE_REJECTED"
"""ATTEMPT_FAILED disposition when validation/acceptance rejected a candidate."""

DISPOSITION_EXECUTOR_FAILED = "EXECUTOR_FAILED"
"""ATTEMPT_FAILED disposition when the executor raised during execution."""

RUNTIME_CONFIGURATION_IDENTITY = "research-runtime-v1"
"""Runtime configuration identity frozen into every execution binding."""

_SOURCE_ARTIFACT_KIND = "source-artifact"
"""Input port kind resolved from the run's attempt-less Source Artifacts."""

TerminalPhaseHook = Callable[
    [RuntimeStore, RunProjection, InvocationRecord, AttemptRecord], None
]
"""Task 7 seam: canonical registration + snapshot before invocation completion."""


@dataclass(frozen=True)
class StepExecutionSpec:
    """The documented execution spec of one Standard Workflow step."""

    mode: str
    policy: AcceptancePolicy


# Documented v1 convention (Ruling 9): the Task 5 adapter's WorkflowStep
# contract carries no execution-metadata section, so the execution spec of
# the Standard Research Workflow lives here as constant data keyed by step
# id. Executor resolution still goes through ExecutorRegistry by mode; the
# table never dispatches execution itself. R1-R3 are automatic working
# artifacts, R4 defers to the H3 human judgment, R5 runs canonical/domain
# acceptance (its domain hook is supplied per runtime instance).
_STANDARD_STEP_SPECS: Mapping[str, StepExecutionSpec] = {
    "R1": StepExecutionSpec(DETERMINISTIC_MODE, AcceptancePolicy.AUTOMATIC),
    "R2": StepExecutionSpec(DETERMINISTIC_MODE, AcceptancePolicy.AUTOMATIC),
    "R3": StepExecutionSpec(DETERMINISTIC_MODE, AcceptancePolicy.AUTOMATIC),
    "R4": StepExecutionSpec(DETERMINISTIC_MODE, AcceptancePolicy.HUMAN),
    "R5": StepExecutionSpec(DETERMINISTIC_MODE, AcceptancePolicy.CANONICAL_DOMAIN),
}

_CANDIDATE_REQUIRED_FIELDS = ("kind", "inputs", "rows")
_CANDIDATE_FIELD_TYPES = {"kind": "string", "inputs": "array", "rows": "array"}


class Orchestrator:
    """The single-process sequential execution engine (see module docstring)."""

    def __init__(
        self,
        store: RuntimeStore,
        *,
        workflow: StandardResearchWorkflow | None = None,
        execution_config: ExecutionConfiguration | None = None,
        registry: ExecutorRegistry | None = None,
        gates: GateRuntime | None = None,
        acquisition: SourceAcquisitionService | None = None,
        cases_dir: str | Path = "cases",
        domain_checks: Mapping[str, object] | None = None,
        terminal_phase: TerminalPhaseHook | None = None,
    ) -> None:
        self._store = store
        self._workflow = workflow or build_standard_workflow()
        self._execution_config = execution_config or ExecutionConfiguration(
            workflow_identity=STANDARD_WORKFLOW_ID,
            workflow_version=STANDARD_WORKFLOW_VERSION,
            runtime_configuration_identity=RUNTIME_CONFIGURATION_IDENTITY,
        )
        self._registry = registry or _default_registry()
        self._gates = gates or GateRuntime(store, self._workflow)
        self._acquisition = acquisition or SourceAcquisitionService(store)
        self._cases_dir = Path(cases_dir)
        self._domain_checks = dict(domain_checks or {})
        self._terminal_phase = terminal_phase

    # -- invocation lifecycle -------------------------------------------------

    def open_invocation(
        self,
        run_id: str,
        scope: tuple[str, ...],
        entry_mode: EntryMode,
        *,
        from_step: str | None = None,
        until_step: str | None = None,
    ) -> InvocationRecord:
        """Durably start an immutable Invocation request (Spec 5.2/16.2).

        The scope entries are validated and ordered through the workflow
        adapter; the execution binding is frozen from this orchestrator's
        execution configuration.
        """
        if not isinstance(entry_mode, EntryMode):
            raise RuntimeContractError(
                f"entry_mode must be an EntryMode (got {entry_mode!r})."
            )
        ordered = scope_nodes(self._workflow, scope)
        if not ordered:
            raise RuntimeContractError("an invocation's requested scope must not be empty.")
        invocation_id = f"inv-{uuid.uuid4().hex}"
        binding = freeze_execution_binding(self._execution_config)
        payload: dict[str, object] = {
            "requested_scope": list(ordered),
            "entry_mode": entry_mode.value,
            "execution_binding": {
                "workflow_identity": binding.workflow_identity,
                "workflow_version": binding.workflow_version,
                "runtime_configuration_identity": binding.runtime_configuration_identity,
                "prompts": dict(binding.prompts),
                "schemas": dict(binding.schemas),
            },
        }
        if from_step is not None:
            payload["from_step"] = from_step
        if until_step is not None:
            payload["until_step"] = until_step
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.INVOCATION_STARTED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation_id,
                payload=payload,
            )
        )
        projection = reduce_events(self._store.events(run_id))
        return projection.invocations[invocation_id]

    def acquire_sources(self, run: RunRecord) -> AcquisitionResult:
        """Acquire the Case's declared sources for the current invocation.

        A required-source failure fails the invocation durably with
        ``ACQUISITION_FAILED`` (nothing is half-committed — the acquisition
        service's required-failure policy commits no partial evidence).
        """
        case = load_research_case(self._cases_dir / run.case_binding.case_id)
        result = self._acquisition.acquire(case, run)
        if result.blocked:
            self.fail_invocation(
                run.run_id, run.current_invocation_id, COMPLETION_ACQUISITION_FAILED
            )
        return result

    def fail_invocation(self, run_id: str, invocation_id: str, reason: str) -> None:
        """Durably close *invocation_id* as FAILED with *reason*."""
        if not isinstance(reason, str) or not reason.strip():
            raise RuntimeContractError("an invocation failure requires a reason.")
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.INVOCATION_COMPLETED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation_id,
                payload={"status": "FAILED", "completion_reason": reason},
            )
        )

    # -- sequential execution -------------------------------------------------

    def continue_execution(
        self,
        run_id: str,
        invocation_id: str,
        *,
        cut_step: str | None = None,
        entry: tuple[tuple[str, ...], tuple[str, ...]] | None = None,
    ) -> None:
        """Execute the invocation's requested scope until a stop condition.

        Stops at a pending Gate Barrier, fails the Invocation on an attempt
        failure, or completes the Invocation when the scope is exhausted.
        ``cut_step`` re-executes from that node onward with fresh attempts
        (rerun/run_from lineage rebuilds); without it the frontier is the
        first node lacking a successful attempt in this invocation. ``entry``
        is the pre-resolved concrete input set of the cut node (an
        exact-compatible checkpoint boundary); only the cut node consumes it.
        """
        projection = reduce_events(self._store.events(run_id))
        invocation = projection.invocations.get(invocation_id)
        if invocation is None:
            raise RuntimeContractError(
                f"invocation {invocation_id!r} is not recorded in run {run_id!r}."
            )
        order = scope_nodes(self._workflow, invocation.requested_scope)
        if cut_step is None:
            cut_step = self._frontier(projection, invocation, order)
            if cut_step is None:
                self._complete_if_running(run_id, invocation_id)
                return
        if cut_step not in order:
            raise RuntimeContractError(
                f"cut step {cut_step!r} is not part of the requested scope of "
                f"invocation {invocation_id!r}."
            )
        for index in range(order.index(cut_step), len(order)):
            projection = reduce_events(self._store.events(run_id))
            invocation = projection.invocations[invocation_id]
            if invocation.status is not InvocationStatus.RUNNING:
                return
            if self._barrier_blocks(projection, run_id, order[index]):
                return
            attempt = self._execute_new_attempt(
                run_id, invocation, order[index], entry=entry
            )
            entry = None
            if attempt.status is AttemptStatus.FAILED:
                projection = reduce_events(self._store.events(run_id))
                disposition = projection.failure_dispositions.get(
                    attempt.attempt_id, DISPOSITION_EXECUTOR_FAILED
                )
                self.fail_invocation(run_id, invocation_id, disposition)
                return
        self._complete_if_running(run_id, invocation_id)

    def entry_context(
        self, run_id: str, invocation_id: str, step_id: str
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Resolve and validate the exact-compatible entry boundary for *step_id*.

        Every predecessor boundary must hold a latest VALID checkpoint whose
        CompatibilityIdentity exactly matches the invocation's execution
        binding (validate_checkpoint: no fuzzy fallback, Spec 12.1). The
        entry artifact set is the union of the predecessor checkpoints'
        concrete artifact ids plus the run's Source Artifacts when the node
        declares source input ports. A first node (no predecessor) resolves
        its inputs normally. Returns the (artifact_ids, upstream_attempt_ids)
        for the entry attempt's input binding.
        """
        projection = reduce_events(self._store.events(run_id))
        invocation = projection.invocations[invocation_id]
        node = self._node(step_id)
        if not node.depends_on:
            return self._resolve_inputs(projection, invocation, node)
        artifact_ids: list[str] = []
        upstream: list[str] = []
        for predecessor_id in node.depends_on:
            checkpoint = self._latest_valid_checkpoint(projection, predecessor_id)
            if checkpoint is None:
                raise RuntimeContractError(
                    f"entry {step_id!r} requires an exact-compatible VALID "
                    f"checkpoint at its {predecessor_id!r} input boundary; "
                    "none is recorded in the run (no fuzzy fallback)."
                )
            validate_checkpoint(
                self._store,
                checkpoint,
                self._checkpoint_identity(
                    invocation.execution_binding,
                    self._node(predecessor_id).step,
                ),
            )
            for artifact_id in checkpoint.artifact_ids:
                if artifact_id not in artifact_ids:
                    artifact_ids.append(artifact_id)
                reference = projection.artifacts[artifact_id]
                if (
                    reference.attempt_id is not None
                    and reference.attempt_id not in upstream
                ):
                    upstream.append(reference.attempt_id)
        for input_port in node.step.inputs:
            if input_port.kind == _SOURCE_ARTIFACT_KIND:
                for artifact_id in self._source_artifact_ids(projection):
                    if artifact_id not in artifact_ids:
                        artifact_ids.append(artifact_id)
        return tuple(artifact_ids), tuple(upstream)

    def retry_attempt(
        self, run_id: str, invocation_id: str, step_id: str, attempt: AttemptRecord
    ) -> AttemptRecord:
        """Re-execute an existing Attempt within its Invocation (Spec 15.1).

        A PENDING attempt receives its durable input binding first; a FAILED
        attempt reuses its recorded binding (INPUT_BOUND precedes the first
        start only). The attempt identity never changes.
        """
        node = self._node(step_id)
        projection = reduce_events(self._store.events(run_id))
        invocation = projection.invocations[invocation_id]
        if attempt.status is AttemptStatus.PENDING:
            artifact_ids, upstream = self._resolve_inputs(
                projection, invocation, node
            )
            persist_input_binding(
                self._store,
                InputBinding(
                    input_binding_id=f"ib-{uuid.uuid4().hex}",
                    run_id=run_id,
                    invocation_id=invocation_id,
                    step_id=step_id,
                    attempt_id=attempt.attempt_id,
                    artifact_ids=artifact_ids,
                    upstream_attempt_ids=upstream,
                ),
            )
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.ATTEMPT_STARTED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation_id,
                step_id=step_id,
                attempt_id=attempt.attempt_id,
                payload={},
            )
        )
        return self._execute_round(run_id, invocation, node, attempt.attempt_id)

    # -- internal: frontier, barriers, inputs ---------------------------------

    def _frontier(
        self, projection: RunProjection, invocation: InvocationRecord, order
    ) -> str | None:
        """Return the next node to execute, or None when the scope is done.

        A FAILED latest attempt means the invocation lost its terminal fact
        to a crash window: it is closed durably with the recorded
        disposition. A PENDING/RUNNING latest attempt blocks progression
        explicitly (reconciliation closes RUNNING attempts; PENDING ones are
        a retry target).
        """
        for step_id in order:
            attempts = self._invocation_attempts(
                projection, invocation.invocation_id, step_id
            )
            if not attempts:
                return step_id
            latest = attempts[-1]
            if latest.status is AttemptStatus.SUCCEEDED:
                continue
            if latest.status is AttemptStatus.FAILED:
                disposition = projection.failure_dispositions.get(
                    latest.attempt_id, EXECUTION_INTERRUPTED
                )
                self.fail_invocation(
                    projection.run.run_id, invocation.invocation_id, disposition
                )
                return None
            raise RuntimeContractError(
                f"attempt {latest.attempt_id} for step {step_id!r} is "
                f"{latest.status.value}; an active attempt blocks progression "
                "(reconcile or retry first)."
            )
        return None

    def _barrier_blocks(self, projection: RunProjection, run_id: str, step_id: str) -> bool:
        """Resolve the Gate Barriers guarding *step_id*; True stops the loop.

        See the module docstring for the approval-validity rules; a REJECTED
        gate whose target still matches the current lineage is a contract
        contradiction (the run would be NEEDS_REVISION): the invocation is
        closed with HUMAN_REJECTION and the contradiction is raised.
        """
        for barrier in self._workflow.gate_barriers.values():
            if barrier.before_step != step_id:
                continue
            upstream = self._latest_successful_attempt(projection, barrier.after_step)
            if upstream is None:
                raise RuntimeContractError(
                    f"barrier {barrier.logical_gate_id!r} guards the boundary "
                    f"after {barrier.after_step!r}, which has no successful "
                    f"attempt in run {run_id!r}."
                )
            artifacts = self._attempt_artifacts(projection, upstream)
            if not artifacts:
                raise RuntimeContractError(
                    f"barrier {barrier.logical_gate_id!r} cannot review "
                    f"{barrier.after_step!r}: its attempt committed no artifacts."
                )
            target = ReviewTarget(
                step_id=upstream.step_id,
                attempt_id=upstream.attempt_id,
                artifact_ids=artifacts,
            )
            gate = self._current_gate(projection, barrier.logical_gate_id)
            if gate is None:
                self._gates.create(run_id, barrier.logical_gate_id, target)
                return True
            if gate.decision is GateDecision.PENDING:
                return True
            if gate.decision is GateDecision.REJECTED:
                if gate.review_target == target:
                    self.fail_invocation(
                        run_id, projection.run.current_invocation_id, HUMAN_REJECTION
                    )
                    raise RuntimeContractError(
                        f"rejected gate {gate.gate_id!r} still matches the "
                        f"current {barrier.after_step!r} lineage; the revision "
                        "entry must re-execute at-or-above the reviewed step."
                    )
                self._gates.replace(gate.gate_id, target, f"gate-{uuid.uuid4().hex}")
                return True
            if gate.review_target == target:
                return False  # APPROVED for the current lineage: proceed
            self._gates.replace(gate.gate_id, target, f"gate-{uuid.uuid4().hex}")
            return True
        return False

    def _resolve_inputs(
        self, projection: RunProjection, invocation: InvocationRecord, node
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Resolve the concrete input artifact set for *node*.

        Every declared input port resolves explicitly: source-artifact
        ports bind the run's attempt-less committed Source Artifacts, every
        other port binds the artifact set of its producing step's latest
        successful attempt (never an implicit "latest artifact").
        """
        artifact_ids: list[str] = []
        upstream: list[str] = []
        seen_artifacts: set[str] = set()
        seen_upstream: set[str] = set()
        for input_port in node.step.inputs:
            if input_port.kind == _SOURCE_ARTIFACT_KIND:
                for artifact_id in self._source_artifact_ids(projection):
                    if artifact_id not in seen_artifacts:
                        artifact_ids.append(artifact_id)
                        seen_artifacts.add(artifact_id)
                continue
            producer = self._producer_for(node, input_port)
            attempt = self._latest_successful_attempt(projection, producer.step.id)
            if attempt is None:
                raise RuntimeContractError(
                    f"step {node.step.id!r} consumes output of "
                    f"{producer.step.id!r}, which has no successful attempt in "
                    f"run {projection.run.run_id!r}; prerequisites are never "
                    "skipped."
                )
            for artifact_id in self._attempt_artifacts(projection, attempt):
                if artifact_id not in seen_artifacts:
                    artifact_ids.append(artifact_id)
                    seen_artifacts.add(artifact_id)
            if attempt.attempt_id not in seen_upstream:
                upstream.append(attempt.attempt_id)
                seen_upstream.add(attempt.attempt_id)
        return tuple(artifact_ids), tuple(upstream)

    def _producer_for(self, node, input_port):
        """The unique workflow node producing the output *input_port* consumes."""
        matches = [
            other
            for other in self._workflow.definition.steps
            if any(
                output.name == input_port.name or output.kind == input_port.kind
                for output in other.step.outputs
            )
        ]
        if len(matches) != 1:
            raise RuntimeContractError(
                f"input port {input_port.name!r} of step {node.step.id!r} "
                f"matches {len(matches)} producer steps; input resolution "
                "requires a unique producer."
            )
        return matches[0]

    # -- internal: attempt protocol -------------------------------------------

    def _execute_new_attempt(
        self,
        run_id: str,
        invocation: InvocationRecord,
        step_id: str,
        *,
        entry: tuple[tuple[str, ...], tuple[str, ...]] | None = None,
    ) -> AttemptRecord:
        node = self._node(step_id)
        attempt_id = f"att-{uuid.uuid4().hex}"
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.ATTEMPT_CREATED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation.invocation_id,
                step_id=step_id,
                attempt_id=attempt_id,
                payload={},
            )
        )
        if entry is None:
            projection = reduce_events(self._store.events(run_id))
            entry = self._resolve_inputs(projection, invocation, node)
        artifact_ids, upstream = entry
        persist_input_binding(
            self._store,
            InputBinding(
                input_binding_id=f"ib-{uuid.uuid4().hex}",
                run_id=run_id,
                invocation_id=invocation.invocation_id,
                step_id=step_id,
                attempt_id=attempt_id,
                artifact_ids=artifact_ids,
                upstream_attempt_ids=upstream,
            ),
        )
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.ATTEMPT_STARTED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation.invocation_id,
                step_id=step_id,
                attempt_id=attempt_id,
                payload={},
            )
        )
        return self._execute_round(run_id, invocation, node, attempt_id)

    def _execute_round(
        self, run_id: str, invocation: InvocationRecord, node, attempt_id: str
    ) -> AttemptRecord:
        """Execute one attempt round: executor, acceptance, commit, terminal."""
        projection = reduce_events(self._store.events(run_id))
        binding = next(
            binding
            for binding in projection.input_bindings.values()
            if binding.attempt_id == attempt_id
        )
        spec = self._spec_for(node.step.id)
        executor = self._registry.resolve(spec.mode)
        try:
            candidate = executor.execute(node.step, binding)
        except Exception:
            self._store.append_event(
                EventEnvelope(
                    event_id=f"evt-{uuid.uuid4().hex}",
                    event_type=EventType.ATTEMPT_FAILED,
                    timestamp=utc_now(),
                    run_id=run_id,
                    invocation_id=invocation.invocation_id,
                    step_id=node.step.id,
                    attempt_id=attempt_id,
                    payload={"disposition": DISPOSITION_EXECUTOR_FAILED},
                )
            )
            projection = reduce_events(self._store.events(run_id))
            return projection.attempts[attempt_id]
        pipeline = self._pipeline_for(node)
        results = {
            ValidationDimension.SCHEMA: pipeline.validate_schema(candidate),
            ValidationDimension.PROVENANCE: pipeline.validate_provenance(candidate),
            ValidationDimension.DOMAIN: pipeline.validate_domain(candidate),
        }
        artifact_id = f"art-{uuid.uuid4().hex}"
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.VALIDATION_COMPLETED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation.invocation_id,
                step_id=node.step.id,
                attempt_id=attempt_id,
                artifact_id=artifact_id,
                payload=_validation_payload(results),
            )
        )
        acceptance = pipeline.accept(candidate, spec.policy)
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.ACCEPTANCE_RECORDED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation.invocation_id,
                step_id=node.step.id,
                attempt_id=attempt_id,
                artifact_id=artifact_id,
                payload=_acceptance_payload(acceptance),
            )
        )
        if acceptance.disposition is AcceptanceDisposition.REJECTED:
            self._store.append_event(
                EventEnvelope(
                    event_id=f"evt-{uuid.uuid4().hex}",
                    event_type=EventType.ATTEMPT_FAILED,
                    timestamp=utc_now(),
                    run_id=run_id,
                    invocation_id=invocation.invocation_id,
                    step_id=node.step.id,
                    attempt_id=attempt_id,
                    payload={"disposition": DISPOSITION_ACCEPTANCE_REJECTED},
                )
            )
            projection = reduce_events(self._store.events(run_id))
            return projection.attempts[attempt_id]
        artifact = ArtifactEnvelope(
            artifact_id=artifact_id,
            run_id=run_id,
            invocation_id=invocation.invocation_id,
            artifact_schema_id=candidate.schema_identity,
            artifact_schema_version=candidate.schema_version,
            created_at=utc_now(),
            step_id=node.step.id,
            attempt_id=attempt_id,
            provenance=candidate.provenance,
        )
        commit_artifact(self._store, artifact, dict(candidate.content))
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.ATTEMPT_SUCCEEDED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation.invocation_id,
                step_id=node.step.id,
                attempt_id=attempt_id,
                payload={},
            )
        )
        create_checkpoint(
            self._store,
            CheckpointRecord(
                checkpoint_id=f"cp-{uuid.uuid4().hex}",
                run_id=run_id,
                step_id=node.step.id,
                artifact_ids=(artifact_id,),
                compatibility=self._checkpoint_identity(
                    invocation.execution_binding, node.step
                ),
                created_at=utc_now(),
            ),
        )
        projection = reduce_events(self._store.events(run_id))
        return projection.attempts[attempt_id]

    # -- internal: completion --------------------------------------------------

    def _complete_if_running(self, run_id: str, invocation_id: str) -> None:
        projection = reduce_events(self._store.events(run_id))
        invocation = projection.invocations[invocation_id]
        if invocation.status is InvocationStatus.RUNNING:
            self._complete_invocation(run_id, projection, invocation)

    def _complete_invocation(
        self, run_id: str, projection: RunProjection, invocation: InvocationRecord
    ) -> None:
        terminal = tuple(execution_order(self._workflow.definition))[-1]
        if self._terminal_phase is not None and terminal in invocation.requested_scope:
            attempts = self._invocation_attempts(
                projection, invocation.invocation_id, terminal
            )
            if attempts and attempts[-1].status is AttemptStatus.SUCCEEDED:
                self._terminal_phase(self._store, projection, invocation, attempts[-1])
        self._store.append_event(
            EventEnvelope(
                event_id=f"evt-{uuid.uuid4().hex}",
                event_type=EventType.INVOCATION_COMPLETED,
                timestamp=utc_now(),
                run_id=run_id,
                invocation_id=invocation.invocation_id,
                payload={
                    "status": "SUCCEEDED",
                    "completion_reason": COMPLETION_BOUNDED_SCOPE,
                },
            )
        )

    # -- internal: lookups ------------------------------------------------------

    def _node(self, step_id: str):
        for node in self._workflow.definition.steps:
            if node.step.id == step_id:
                return node
        raise RuntimeContractError(
            f"step {step_id!r} is not part of workflow "
            f"{self._workflow.definition.id!r}."
        )

    def _spec_for(self, step_id: str) -> StepExecutionSpec:
        spec = _STANDARD_STEP_SPECS.get(step_id)
        if spec is None:
            raise RuntimeContractError(
                f"step {step_id!r} has no execution spec in the standard "
                "workflow table; execution is resolved through the spec table "
                "and the executor registry, never ad hoc."
            )
        return spec

    def _pipeline_for(self, node) -> AcceptancePipeline:
        output = node.step.outputs[0]
        return AcceptancePipeline(
            schema=SchemaSpec(
                identity=output.kind,
                version=DETERMINISTIC_SCHEMA_VERSION,
                required_fields=_CANDIDATE_REQUIRED_FIELDS,
                field_types=dict(_CANDIDATE_FIELD_TYPES),
                constant_fields={"kind": output.kind},
            ),
            provenance_required=True,
            domain_check=self._domain_checks.get(node.step.id),
        )

    def _checkpoint_identity(
        self, binding: ExecutionBinding, step
    ) -> CompatibilityIdentity:
        """The exact CompatibilityIdentity of a step boundary (Spec 12).

        Prompt pairs never apply (the v1 standard workflow declares none);
        the schema pair names the step's single declared output schema.
        """
        output = step.outputs[0]
        return CompatibilityIdentity(
            workflow_identity=binding.workflow_identity,
            workflow_version=binding.workflow_version,
            step_identity=step.id,
            step_version=step.version,
            runtime_configuration_identity=binding.runtime_configuration_identity,
            prompt_identity=None,
            prompt_version=None,
            schema_identity=output.kind,
            schema_version=DETERMINISTIC_SCHEMA_VERSION,
        )

    @staticmethod
    def _invocation_attempts(
        projection: RunProjection, invocation_id: str, step_id: str
    ) -> list[AttemptRecord]:
        return [
            attempt
            for attempt in projection.attempts.values()
            if attempt.invocation_id == invocation_id and attempt.step_id == step_id
        ]

    @staticmethod
    def _latest_valid_checkpoint(projection: RunProjection, step_id: str):
        for checkpoint in reversed(list(projection.checkpoints.values())):
            if (
                checkpoint.step_id == step_id
                and checkpoint.status is CheckpointStatus.VALID
            ):
                return checkpoint
        return None

    @staticmethod
    def _source_artifact_ids(projection: RunProjection) -> tuple[str, ...]:
        return tuple(
            reference.artifact_id
            for reference in projection.artifacts.values()
            if reference.step_id is None and reference.attempt_id is None
        )

    @staticmethod
    def _latest_successful_attempt(
        projection: RunProjection, step_id: str
    ) -> AttemptRecord | None:
        for attempt in reversed(list(projection.attempts.values())):
            if attempt.step_id == step_id and attempt.status is AttemptStatus.SUCCEEDED:
                return attempt
        return None

    @staticmethod
    def _attempt_artifacts(
        projection: RunProjection, attempt: AttemptRecord
    ) -> tuple[str, ...]:
        return tuple(
            reference.artifact_id
            for reference in projection.artifacts.values()
            if reference.attempt_id == attempt.attempt_id
        )

    @staticmethod
    def _current_gate(projection: RunProjection, logical_gate_id: str):
        gates = [
            gate
            for gate in projection.gates.values()
            if gate.logical_gate_id == logical_gate_id
        ]
        if not gates:
            return None
        latest = gates[-1]
        if latest.superseded_by is not None:
            raise RuntimeContractError(
                f"the latest {logical_gate_id!r} gate {latest.gate_id!r} is "
                "superseded without a non-superseded successor; the gate "
                "chain of the run is inconsistent."
            )
        return latest


def _default_registry() -> ExecutorRegistry:
    registry = ExecutorRegistry()
    registry.register(DETERMINISTIC_MODE, DeterministicExecutor())
    return registry


def _validation_payload(results: Mapping[ValidationDimension, object]) -> dict:
    return {
        "validation": {
            dimension.value: {
                "passed": result.passed,
                "evaluated": result.evaluated,
                "reasons": list(result.reasons),
            }
            for dimension, result in results.items()
        }
    }


def _acceptance_payload(acceptance) -> dict:
    return {
        "policy": acceptance.policy.value,
        "disposition": acceptance.disposition.value,
        "validation": {
            dimension.value: {
                "passed": result.passed,
                "evaluated": result.evaluated,
                "reasons": list(result.reasons),
            }
            for dimension, result in acceptance.validation.items()
        },
        "reasons": list(acceptance.reasons),
    }
