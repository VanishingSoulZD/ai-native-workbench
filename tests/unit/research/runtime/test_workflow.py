"""Unit tests for the Standard Research Workflow adapter (Task 5 brief Step 1,
Spec sections 1/7.1, Ruling 5; methodology sections 9/13).

The adapter exposes the formal versioned Standard Research Workflow built on
Workflow Core: definition nodes R1..R5 following the Spec 1 chain
(R1 -> R2 -> R3 -> H2 -> R4 -> H3 -> R5), with H2/H3/H4 carried as Gate
Barrier metadata and never fabricated as Workflow Steps (Spec 7.1). H4 guards
the R6 Evaluate / Snapshot readiness -> R7 Deliver boundary of the full
standard lifecycle (methodology section 9); its position literals name steps
outside the v1 completion boundary, so a v1 scheduler can never raise it.
"""

import pytest

from ai_native_workbench.research.runtime import (
    ExecutionScope,
    RuntimeContractError,
    SNAPSHOT_MARKER,
)
from ai_native_workbench.research.runtime.workflow import (
    EntryBoundaryError,
    GateBarrier,
    STANDARD_WORKFLOW_ID,
    STANDARD_WORKFLOW_VERSION,
    StandardResearchWorkflow,
    build_standard_workflow,
    scope_nodes,
    validate_entry_boundary,
)
from ai_native_workbench.research.workflow import (
    LifecycleStage,
    WorkflowDefinition,
    WorkflowNode,
    WorkflowValidationError,
    execution_order,
    validate_workflow,
)
from ai_native_workbench.research.workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    WorkflowStep,
)

WORKFLOW = build_standard_workflow()

STANDARD_NODE_IDS = ("R1", "R2", "R3", "R4", "R5")

STANDARD_NAMES = {
    "R1": "R1 Discover",
    "R2": "R2 Evidence",
    "R3": "R3 Analyze",
    "R4": "R4 Decide",
    "R5": "R5 Synthesize / Canonicalize",
}


def node_ids(workflow: StandardResearchWorkflow) -> tuple[str, ...]:
    return tuple(node.step.id for node in workflow.definition.steps)


def step_by_id(workflow: StandardResearchWorkflow, step_id: str):
    for node in workflow.definition.steps:
        if node.step.id == step_id:
            return node.step
    raise AssertionError(f"step {step_id!r} not found in the standard workflow")


# ---------------------------------------------------------------------------
# Adapter shape: definition, lifecycle mapping, gate barriers (Ruling 5)
# ---------------------------------------------------------------------------


def test_build_standard_workflow_is_identity_versioned():
    assert STANDARD_WORKFLOW_ID == WORKFLOW.definition.id
    assert STANDARD_WORKFLOW_VERSION == WORKFLOW.definition.version
    assert WORKFLOW.definition.id
    assert WORKFLOW.definition.version


def test_standard_workflow_defines_r1_to_r5_in_chain_order():
    assert node_ids(WORKFLOW) == STANDARD_NODE_IDS
    # Linear Spec 1 chain: each step depends on its immediate predecessor.
    assert step_by_id(WORKFLOW, "R1").id == "R1"
    for step_id in ("R2", "R3", "R4", "R5"):
        node = next(n for n in WORKFLOW.definition.steps if n.step.id == step_id)
        assert node.depends_on == (STANDARD_NODE_IDS[STANDARD_NODE_IDS.index(step_id) - 1],)


def test_standard_workflow_step_names_are_verbatim():
    for step_id, name in STANDARD_NAMES.items():
        assert step_by_id(WORKFLOW, step_id).name == name


def test_standard_workflow_passes_core_validation():
    validate_workflow(WORKFLOW.definition)
    assert execution_order(WORKFLOW.definition) == STANDARD_NODE_IDS


def test_standard_workflow_lifecycle_stages_map_r1_to_r5():
    assert WORKFLOW.definition.lifecycle_stage_map == {
        "R1": LifecycleStage.R1_DISCOVER,
        "R2": LifecycleStage.R2_EVIDENCE,
        "R3": LifecycleStage.R3_ANALYZE,
        "R4": LifecycleStage.R4_DECIDE,
        "R5": LifecycleStage.R5_SYNTHESIZE,
    }


def test_each_standard_step_declares_one_output_and_at_least_one_input():
    # DeterministicExecutor (Task 4) executes steps declaring exactly one
    # output, so the standard v1 steps keep a single-output port.
    for step_id in STANDARD_NODE_IDS:
        step = step_by_id(WORKFLOW, step_id)
        assert len(step.outputs) == 1, f"{step_id} declares one output port"
        assert len(step.inputs) >= 1, f"{step_id} declares at least one input"
        assert step.method and step.constraints and step.validation


def test_gate_barriers_cover_h2_h3_h4_verbatim():
    assert tuple(WORKFLOW.gate_barriers) == ("H2", "H3", "H4")
    expected = {
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
    for gate_id, barrier in expected.items():
        assert WORKFLOW.gate_barriers[gate_id] == barrier
        assert barrier.logical_gate_id == gate_id
        assert barrier.after_step != barrier.before_step


def test_h2_and_h3_barrier_positions_name_in_definition_boundaries():
    # H2 sits between R3 and R4, H3 between R4 and R5: both endpoints are
    # definition nodes of the v1 completion chain.
    for gate_id in ("H2", "H3"):
        barrier = WORKFLOW.gate_barriers[gate_id]
        assert barrier.after_step in node_ids(WORKFLOW)
        assert barrier.before_step in node_ids(WORKFLOW)


def test_h4_barrier_is_metadata_outside_the_v1_definition():
    # H4 guards the R6/Snapshot -> R7 boundary of the full lifecycle; R6/R7
    # are Step 7 scope and never fabricated into the v1 definition.
    barrier = WORKFLOW.gate_barriers["H4"]
    assert barrier.after_step == "R6"
    assert barrier.before_step == "R7"
    assert barrier.after_step not in node_ids(WORKFLOW)
    assert barrier.before_step not in node_ids(WORKFLOW)
    # ... and v1 scoping rules below refuse every barrier id, so H4 cannot be
    # raised by a v1 scheduler.


def test_gate_barriers_are_never_workflow_nodes():
    barrier_ids = set(WORKFLOW.gate_barriers)
    step_ids = set(node_ids(WORKFLOW))
    assert not (barrier_ids & step_ids)


# ---------------------------------------------------------------------------
# scope_nodes: ordered step projection of an ExecutionScope (brief Step 1)
# ---------------------------------------------------------------------------


def test_scope_nodes_returns_full_chain_for_full_scope():
    assert scope_nodes(WORKFLOW, STANDARD_NODE_IDS) == STANDARD_NODE_IDS


def test_scope_nodes_orders_requested_steps_by_execution_order():
    # The scheduler consumes the deterministic topological order, never the
    # caller's request order.
    assert scope_nodes(WORKFLOW, ("R3", "R1", "R5")) == ("R1", "R3", "R5")
    assert scope_nodes(WORKFLOW, ("R5",)) == ("R5",)


def test_scope_nodes_accepts_empty_scope():
    assert scope_nodes(WORKFLOW, ()) == ()


def test_scope_nodes_allows_snapshot_marker_but_never_returns_it():
    scope = STANDARD_NODE_IDS + (SNAPSHOT_MARKER,)
    assert scope_nodes(WORKFLOW, scope) == STANDARD_NODE_IDS
    # A snapshot-only invocation freezes without scheduling workflow steps.
    assert scope_nodes(WORKFLOW, (SNAPSHOT_MARKER,)) == ()


def test_scope_nodes_rejects_unknown_step_ids():
    for entry in ("R6", "R7", "R8", "ghost", ""):
        with pytest.raises(RuntimeContractError) as excinfo:
            scope_nodes(WORKFLOW, ("R1", entry))
        assert entry in str(excinfo.value)


def test_scope_nodes_rejects_gate_barrier_ids():
    for entry in ("H2", "H3", "H4"):
        with pytest.raises(RuntimeContractError) as excinfo:
            scope_nodes(WORKFLOW, ("R1", entry))
        assert entry in str(excinfo.value)


def test_scope_nodes_rejects_non_scope_and_non_workflow():
    with pytest.raises(RuntimeContractError):
        scope_nodes(WORKFLOW, ["R1"])  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        scope_nodes(WORKFLOW, "R1")  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        scope_nodes(object(), ("R1",))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_entry_boundary: syntactic entry legality (brief Step 1)
# ---------------------------------------------------------------------------


def test_entry_boundary_accepts_every_definition_node():
    for step_id in STANDARD_NODE_IDS:
        assert validate_entry_boundary(WORKFLOW, step_id) is None


def test_entry_boundary_rejects_barriers_and_snapshot_marker():
    # Barrier ids and the snapshot marker are never steps, so they are never
    # legal --from/--until entries (Spec 12.1 boundary legality is stateful
    # and belongs to the orchestrator layer).
    for step_id in ("H2", "H3", "H4", SNAPSHOT_MARKER):
        with pytest.raises(EntryBoundaryError) as excinfo:
            validate_entry_boundary(WORKFLOW, step_id)
        assert isinstance(excinfo.value, RuntimeContractError)
        assert step_id in str(excinfo.value)


def test_entry_boundary_rejects_unknown_and_blank_step_ids():
    for step_id in ("R6", "R7", "ghost", ""):
        with pytest.raises(EntryBoundaryError):
            validate_entry_boundary(WORKFLOW, step_id)


def test_entry_boundary_rejects_non_string_entries():
    with pytest.raises(RuntimeContractError):
        validate_entry_boundary(WORKFLOW, None)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        validate_entry_boundary(WORKFLOW, 42)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        validate_entry_boundary(object(), "R1")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Construction-time validation (progress.md: adapter validates at construction)
# ---------------------------------------------------------------------------


def make_step(step_id: str, depends_on: tuple[str, ...] = ()) -> WorkflowNode:
    return WorkflowNode(
        step=WorkflowStep(
            id=step_id,
            name=step_id,
            version="1",
            purpose=f"Execute {step_id}.",
            inputs=(StepInput("input", "value"),),
            outputs=(StepOutput("output", "value"),),
            preconditions=("inputs are bound",),
            method=("perform the declared step method",),
            constraints=("do not change undeclared scope",),
            human_gate=GateRequirement(required=False, gate_type=None),
            validation=("declared output exists",),
            provenance=ProvenanceRequirement(required=False, rules=()),
        ),
        depends_on=depends_on,
    )


def test_adapter_construction_validates_the_definition():
    broken = WorkflowDefinition(
        id=STANDARD_WORKFLOW_ID,
        version=STANDARD_WORKFLOW_VERSION,
        steps=(make_step("R1"), make_step("R2", depends_on=("ghost",))),
        lifecycle_stage_map={"R1": LifecycleStage.R1_DISCOVER},
    )
    with pytest.raises(RuntimeContractError) as excinfo:
        StandardResearchWorkflow(definition=broken, gate_barriers={})
    assert "ghost" in str(excinfo.value)


def test_adapter_construction_rejects_non_definition_and_bad_barriers():
    with pytest.raises(RuntimeContractError):
        StandardResearchWorkflow(definition=object(), gate_barriers={})  # type: ignore[arg-type]
    barrier = GateBarrier(
        logical_gate_id="H2",
        name="H2 Selection Gate",
        after_step="R3",
        before_step="R4",
        description="A durable Runtime Gate Barrier.",
    )
    with pytest.raises(RuntimeContractError):
        StandardResearchWorkflow(
            definition=WORKFLOW.definition, gate_barriers=[barrier]  # type: ignore[arg-type]
        )
    with pytest.raises(RuntimeContractError):
        StandardResearchWorkflow(
            definition=WORKFLOW.definition,
            gate_barriers={"H2": "not-a-barrier"},  # type: ignore[dict-item]
        )


def test_core_validation_error_wrapping_is_preserved():
    # RuntimeContractError is the Runtime boundary; the core failure reason
    # stays readable inside it and is chained as the cause.
    broken = WorkflowDefinition(
        id=STANDARD_WORKFLOW_ID,
        version=STANDARD_WORKFLOW_VERSION,
        steps=(make_step("R1"), make_step("R2", depends_on=("ghost",))),
        lifecycle_stage_map={"R1": LifecycleStage.R1_DISCOVER},
    )
    try:
        validate_workflow(broken)
    except WorkflowValidationError as core_error:
        try:
            StandardResearchWorkflow(definition=broken, gate_barriers={})
        except RuntimeContractError as runtime_error:
            assert isinstance(runtime_error.__cause__, WorkflowValidationError)
            assert str(core_error) in str(runtime_error)
            return
        raise AssertionError("construction must fail for an invalid workflow")
    raise AssertionError("the broken definition must fail core validation")
