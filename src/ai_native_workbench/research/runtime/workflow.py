"""Standard Research Workflow adapter for the Research Runtime v1 (Task 5).

The Runtime consumes the formal, versioned Standard Research Workflow of
Workflow Core (Spec section 7.1); it never embeds ``if step_id == "R1"``
dispatch. This adapter freezes that workflow into a validated
:class:`StandardResearchWorkflow` record: definition nodes R1..R5 follow the
Spec 1 chain ``R1 -> R2 -> R3 -> H2 -> R4 -> H3 -> R5`` and H2/H3/H4 are
carried as :class:`GateBarrier` metadata — durable Runtime control decisions
between workflow regions, never fabricated Workflow Steps (Spec 7.1,
Ruling 5, methodology section 9).

Barrier position semantics are explicit: each barrier names the boundary it
guards as ``after_step``/``before_step`` lifecycle literals. H2 and H3 guard
boundaries inside the v1 completion chain (R3->R4 and R4->R5) while H4 guards
the R6 Evaluate / Snapshot readiness -> R7 Deliver boundary of the full
standard lifecycle — outside the v1 definition, so a v1 scheduler can never
raise it. The v1 completion boundary is R1..R5 plus the Runtime-managed
Snapshot freeze (``SNAPSHOT_MARKER``), which is never a step.

The module exposes the scope/entry projection helpers the Task 6 orchestrator
scheduler consumes: :func:`scope_nodes` maps an ExecutionScope to the ordered
definition node ids to schedule, and :func:`validate_entry_boundary` decides
syntactic entry legality (barriers and the snapshot marker are never legal
entries). Stateful boundary legality (checkpoint compatibility, pending Gate
state) belongs to the orchestrator layer (Spec sections 12.1/13.3).
"""

from collections.abc import Mapping
from dataclasses import dataclass

from ..workflow.composition import (
    LifecycleStage,
    WorkflowDefinition,
    WorkflowNode,
    WorkflowValidationError,
    execution_order,
    validate_workflow,
)
from ..workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    WorkflowStep,
)
from .domain import ExecutionScope, RuntimeContractError, SNAPSHOT_MARKER

STANDARD_WORKFLOW_ID = "research-standard"
"""Workflow identity the Runtime freezes into an Invocation's execution
binding for the Standard Research Workflow (Spec 16.2)."""

STANDARD_WORKFLOW_VERSION = "1.0.0"
"""Version of the Standard Research Workflow definition frozen by this
adapter."""

STANDARD_NODE_IDS = ("R1", "R2", "R3", "R4", "R5")
"""The v1 completion-chain node ids, in definition order (Spec section 1)."""


class EntryBoundaryError(RuntimeContractError):
    """Raised when an entry point is not a legal workflow entry boundary.

    Only definition node ids are legal syntactic entries: Gate Barrier ids
    (H2/H3/H4) and the snapshot marker are never steps, and step ids outside
    the definition (R6/R7/R8 in v1) do not exist as entries. Stateful
    legality (checkpoint compatibility, resolved predecessor Gates) is
    decided by the orchestrator layer, not by this boundary check.
    """


@dataclass(frozen=True)
class GateBarrier:
    """Durable human Gate Barrier metadata (Spec 7.1, methodology section 9).

    A barrier is a control decision between workflow regions, never a
    Workflow Step. Its position is explicit ``after_step``/``before_step``
    lifecycle literals naming the boundary it guards; both are always
    present so every barrier has a documented position. Literals may name
    steps beyond the current definition (H4 names R6/R7, which the v1
    definition does not contain): a barrier only binds execution when a
    scheduler actually walks the region it guards.
    """

    logical_gate_id: str
    name: str
    after_step: str
    before_step: str
    description: str

    def __post_init__(self) -> None:
        for field_name in (
            "logical_gate_id",
            "name",
            "after_step",
            "before_step",
            "description",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeContractError(
                    f"GateBarrier {field_name} must be a non-empty string."
                )
        if self.after_step == self.before_step:
            raise RuntimeContractError(
                f"GateBarrier {self.logical_gate_id!r} must guard a boundary "
                "between two different lifecycle positions "
                f"(after_step == before_step == {self.after_step!r})."
            )


@dataclass(frozen=True)
class StandardResearchWorkflow:
    """The validated, versioned Standard Research Workflow adapter.

    ``definition`` is a Workflow Core graph whose nodes are the workflow
    steps; ``gate_barriers`` maps each logical Gate id (verbatim H2/H3/H4
    tokens) to its barrier metadata. The definition is validated at
    construction (core contract, dependency graph, lifecycle mapping), so
    Runtime paths only ever consume already-valid workflows; a definition
    that fails core validation raises RuntimeContractError wrapping the core
    WorkflowValidationError.
    """

    definition: WorkflowDefinition
    gate_barriers: Mapping[str, GateBarrier]

    def __post_init__(self) -> None:
        if not isinstance(self.definition, WorkflowDefinition):
            raise RuntimeContractError(
                "StandardResearchWorkflow.definition must be a WorkflowDefinition."
            )
        if not isinstance(self.gate_barriers, Mapping):
            raise RuntimeContractError(
                "StandardResearchWorkflow.gate_barriers must be a mapping of "
                "logical gate id -> GateBarrier."
            )
        for gate_id, barrier in self.gate_barriers.items():
            if not isinstance(gate_id, str) or not gate_id.strip():
                raise RuntimeContractError(
                    "gate_barriers keys must be non-empty logical gate id strings."
                )
            if not isinstance(barrier, GateBarrier):
                raise RuntimeContractError(
                    f"gate barrier {gate_id!r} must be a GateBarrier "
                    f"(got {barrier!r})."
                )
            if barrier.logical_gate_id != gate_id:
                raise RuntimeContractError(
                    f"gate barrier key {gate_id!r} does not match its "
                    f"logical_gate_id {barrier.logical_gate_id!r}."
                )
        try:
            validate_workflow(self.definition)
        except WorkflowValidationError as error:
            raise RuntimeContractError(
                f"invalid standard workflow definition: {error}"
            ) from error


def build_standard_workflow() -> StandardResearchWorkflow:
    """Return a freshly validated Standard Research Workflow instance.

    The workflow is immutable constant data (validated at construction); a
    factory keeps construction explicit and gives later layers (Task 6
    execution binding freeze) a single call site for the workflow identity.
    """
    return StandardResearchWorkflow(
        definition=_build_definition(),
        gate_barriers=_build_gate_barriers(),
    )


# ---------------------------------------------------------------------------
# Definition construction
# ---------------------------------------------------------------------------


def _make_node(
    step_id: str,
    name: str,
    purpose: str,
    *,
    depends_on: tuple[str, ...],
    inputs: tuple[StepInput, ...],
    outputs: tuple[StepOutput, ...],
    preconditions: tuple[str, ...],
    method: tuple[str, ...],
    constraints: tuple[str, ...],
    validation: tuple[str, ...],
) -> WorkflowNode:
    return WorkflowNode(
        step=WorkflowStep(
            id=step_id,
            name=name,
            version="1",
            purpose=purpose,
            inputs=inputs,
            outputs=outputs,
            preconditions=preconditions,
            method=method,
            constraints=constraints,
            # Human Gates are workflow-level Gate Barriers (H2/H3/H4), never
            # step attributes; steps themselves require no per-step gate.
            human_gate=GateRequirement(required=False, gate_type=None),
            validation=validation,
            provenance=ProvenanceRequirement(
                required=True,
                rules=("every output artifact records its input lineage",),
            ),
        ),
        depends_on=depends_on,
    )


def _build_definition() -> WorkflowDefinition:
    """The v1 completion chain R1..R5 (architecture sections 14.1-14.5).

    Each step declares exactly one output port (its one committed output
    artifact per attempt round, Ruling 14) and the input ports its region
    consumes from the acquired Source Artifacts and upstream step outputs;
    port names/kind strings are declarations consumed by later binding
    construction, in the Workflow Core convention.
    """
    source_input = StepInput("source_artifacts", "source-artifact")
    steps = (
        _make_node(
            "R1",
            "R1 Discover",
            "Map the research space from the approved charter and the acquired "
            "Source Artifacts: candidate universe, taxonomy / categories, "
            "source map and research hypotheses / plan. R1 creates a working "
            "map, never final selection decisions.",
            depends_on=(),
            inputs=(source_input,),
            outputs=(StepOutput("candidate_universe", "candidate-universe"),),
            preconditions=("approved charter is bound", "source acquisition completed"),
            method=(
                "survey the acquired Source Artifacts against the approved charter",
                "derive the candidate universe, taxonomy, source map and plan",
            ),
            constraints=(
                "create a working map, not final selection decisions",
                "no autonomous source discovery",
            ),
            validation=("the candidate universe and source map are recorded",),
        ),
        _make_node(
            "R2",
            "R2 Evidence",
            "Extract and normalize evidence from the candidate universe and "
            "the acquired Source Artifacts, forming Source Records, Evidence "
            "Candidates and Claim Candidates with provenance intact.",
            depends_on=("R1",),
            inputs=(StepInput("candidate_universe", "candidate-universe"), source_input),
            outputs=(StepOutput("evidence_candidates", "evidence-candidate"),),
            preconditions=("R1 output is committed and bound",),
            method=(
                "extract and normalize evidence from declared sources only",
                "form evidence and claim candidates from the candidate universe",
            ),
            constraints=(
                "preserve provenance of every claim",
                "do not invent sources or claims",
            ),
            validation=("every evidence candidate is traceable to an acquired source",),
        ),
        _make_node(
            "R3",
            "R3 Analyze",
            "Analyze the collected evidence and claims within the research "
            "framework: comparisons, metrics, scores, relationships and "
            "analytical findings.",
            depends_on=("R2",),
            inputs=(StepInput("evidence_candidates", "evidence-candidate"),),
            outputs=(StepOutput("analysis", "analysis"),),
            preconditions=("R2 output is committed and bound",),
            method=(
                "analyze evidence and claims against the research framework",
                "derive comparisons, metrics, relationships and findings",
            ),
            constraints=("keep observation and inference distinguishable",),
            validation=("analysis findings separate observation from inference",),
        ),
        _make_node(
            "R4",
            "R4 Decide",
            "Formulate judgment, decision and recommendation candidates from "
            "evidence and analysis, given the resolved H2 selection decision; "
            "state hypotheses and unknowns explicitly.",
            depends_on=("R3",),
            inputs=(
                StepInput("analysis", "analysis"),
                StepInput("evidence_candidates", "evidence-candidate"),
            ),
            outputs=(StepOutput("judgment_candidates", "judgment-candidate"),),
            preconditions=("R3 output is committed and bound", "H2 is resolved"),
            method=(
                "formulate judgment, decision and recommendation candidates",
                "state hypotheses and unknowns explicitly",
            ),
            constraints=("do not turn unknowns into negative findings",),
            validation=("judgment candidates are present and unknowns explicit",),
        ),
        _make_node(
            "R5",
            "R5 Synthesize / Canonicalize",
            "Synthesize the accepted judgments into canonical candidates and "
            "validate them (schema, provenance, domain rules) against the "
            "Canonical Registry. R5 remains one lifecycle Step; its output "
            "crosses the R5 knowledge-plane boundary on acceptance.",
            depends_on=("R4",),
            inputs=(StepInput("judgment_candidates", "judgment-candidate"),),
            outputs=(StepOutput("canonical_candidates", "canonical-candidate"),),
            preconditions=("R4 output is committed and bound", "H3 is resolved"),
            method=(
                "synthesize accepted judgments into canonical candidates",
                "run schema, provenance and canonical domain validation",
            ),
            constraints=(
                "register only schema- and provenance-valid canonical candidates",
                "canonicalization preserves the working artifact lineage",
            ),
            validation=(
                "canonical candidates passed schema, provenance and domain validation",
            ),
        ),
    )
    return WorkflowDefinition(
        id=STANDARD_WORKFLOW_ID,
        version=STANDARD_WORKFLOW_VERSION,
        steps=steps,
        lifecycle_stage_map={
            "R1": LifecycleStage.R1_DISCOVER,
            "R2": LifecycleStage.R2_EVIDENCE,
            "R3": LifecycleStage.R3_ANALYZE,
            "R4": LifecycleStage.R4_DECIDE,
            "R5": LifecycleStage.R5_SYNTHESIZE,
        },
    )


def _build_gate_barriers() -> dict[str, GateBarrier]:
    """The in-run Gate Barriers, verbatim from methodology section 9."""
    return {
        "H2": GateBarrier(
            logical_gate_id="H2",
            name="H2 Selection Gate",
            after_step="R3",
            before_step="R4",
            description=(
                "H2 is a durable Runtime Gate Barrier between R3 Analyze and "
                "R4 Decide."
            ),
        ),
        "H3": GateBarrier(
            logical_gate_id="H3",
            name="H3 Judgment Gate",
            after_step="R4",
            before_step="R5",
            description=(
                "H3 is a durable Runtime Gate Barrier between R4 Decide and "
                "R5 Synthesize / Canonicalize."
            ),
        ),
        "H4": GateBarrier(
            logical_gate_id="H4",
            name="H4 Final Delivery Gate",
            after_step="R6",
            before_step="R7",
            description=(
                "H4 is a durable Runtime Gate Barrier between R6 Evaluate / "
                "Snapshot readiness and R7 Deliver."
            ),
        ),
    }


# ---------------------------------------------------------------------------
# Scope and entry projection (consumed by the Task 6 orchestrator)
# ---------------------------------------------------------------------------


def _require_adapter(workflow: object, operation: str) -> StandardResearchWorkflow:
    if not isinstance(workflow, StandardResearchWorkflow):
        raise RuntimeContractError(
            f"{operation} requires a StandardResearchWorkflow (got {workflow!r})."
        )
    return workflow


def _node_ids(workflow: StandardResearchWorkflow) -> tuple[str, ...]:
    return tuple(node.step.id for node in workflow.definition.steps)


def scope_nodes(workflow: StandardResearchWorkflow, scope: ExecutionScope) -> tuple[str, ...]:
    """Return the definition node ids of *scope* in deterministic execution
    order, for the Task 6 scheduler.

    Every scope entry must be a definition node id or the SNAPSHOT marker
    (Spec 5.3): Gate Barrier ids are never scheduled steps and unknown ids
    (R6/R7/R8 in v1) cannot be requested, so both raise RuntimeContractError.
    The snapshot marker is never returned — the Snapshot freeze is a
    Runtime-managed operation the orchestrator reads from the requested
    scope verbatim.
    """
    workflow = _require_adapter(workflow, "scope_nodes")
    if not isinstance(scope, tuple):
        raise RuntimeContractError(
            "scope must be an ExecutionScope tuple of step id strings "
            f"(got {scope!r})."
        )
    known = _node_ids(workflow)
    for entry in scope:
        if entry in known or entry == SNAPSHOT_MARKER:
            continue
        if entry in workflow.gate_barriers:
            raise RuntimeContractError(
                f"scope entry {entry!r} is a Gate Barrier, never a scheduled "
                "workflow step; barriers are resolved between steps and "
                "cannot be requested in a scope."
            )
        raise RuntimeContractError(
            f"scope entry {entry!r} is not a step of workflow "
            f"{workflow.definition.id!r} v{workflow.definition.version} "
            f"(steps: {', '.join(known)}; {SNAPSHOT_MARKER!r} is the only "
            "non-step scope entry)."
        )
    requested = set(scope)
    return tuple(
        step_id for step_id in execution_order(workflow.definition) if step_id in requested
    )


def validate_entry_boundary(workflow: StandardResearchWorkflow, step_id: str) -> None:
    """Validate *step_id* as a legal workflow entry boundary.

    Raises EntryBoundaryError (a RuntimeContractError) unless *step_id* names
    a definition node. Barrier ids and the SNAPSHOT marker are never legal
    entries (they are not steps), and ids outside the definition do not exist
    as entries in this workflow version. Stateful legality — checkpoint
    compatibility, resolved predecessor Gates — is the orchestrator's
    decision at scheduling time.
    """
    workflow = _require_adapter(workflow, "validate_entry_boundary")
    if not isinstance(step_id, str):
        raise RuntimeContractError(
            f"an entry step id must be a string (got {step_id!r})."
        )
    known = _node_ids(workflow)
    if step_id in known:
        return None
    if step_id in workflow.gate_barriers:
        raise EntryBoundaryError(
            f"{step_id!r} is a Gate Barrier, never a workflow step; only "
            "definition steps are legal entry boundaries."
        )
    if step_id == SNAPSHOT_MARKER:
        raise EntryBoundaryError(
            "SNAPSHOT is a Runtime-managed freeze marker, never a workflow "
            "step, so it can never be a workflow entry."
        )
    raise EntryBoundaryError(
        f"step {step_id!r} is not part of workflow {workflow.definition.id!r} "
        f"v{workflow.definition.version}; legal entry steps are "
        f"{', '.join(known)}."
    )


__all__ = [
    "EntryBoundaryError",
    "GateBarrier",
    "STANDARD_NODE_IDS",
    "STANDARD_WORKFLOW_ID",
    "STANDARD_WORKFLOW_VERSION",
    "StandardResearchWorkflow",
    "build_standard_workflow",
    "scope_nodes",
    "validate_entry_boundary",
]
