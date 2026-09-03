from dataclasses import replace

import pytest

from ai_native_workbench.research.workflow.composition import (
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


def make_node(step_id: str, depends_on: tuple[str, ...] = ()) -> WorkflowNode:
    return WorkflowNode(
        step=WorkflowStep(step_id, step_id, "1.0.0", "purpose", (StepInput("input", "value"),),
                          (StepOutput("output", "value"),), (), ("method",), ("constraint",),
                          GateRequirement(False, None), ("validation",),
                          ProvenanceRequirement(False, ())),
        depends_on=depends_on,
    )


def make_workflow(*nodes: WorkflowNode, stage_map=None) -> WorkflowDefinition:
    return WorkflowDefinition("workflow", "1.0.0", nodes, stage_map or {})


def test_explicit_dependencies_are_resolved():
    validate_workflow(make_workflow(make_node("define"), make_node("collect", ("define",))))


def test_missing_dependency_is_rejected():
    with pytest.raises(WorkflowValidationError):
        validate_workflow(make_workflow(make_node("collect", ("missing",))))


def test_duplicate_step_id_is_rejected():
    with pytest.raises(WorkflowValidationError):
        validate_workflow(make_workflow(make_node("same"), make_node("same")))


def test_cycle_is_rejected():
    with pytest.raises(WorkflowValidationError):
        validate_workflow(make_workflow(make_node("a", ("b",)), make_node("b", ("a",))))


def test_step_contracts_are_revalidated_inside_workflow_validation():
    invalid = replace(make_node("invalid").step, method=())
    with pytest.raises(WorkflowValidationError):
        validate_workflow(make_workflow(WorkflowNode(invalid)))


def test_topological_order_is_deterministic():
    workflow = make_workflow(make_node("zeta"), make_node("alpha"), make_node("beta"))
    assert execution_order(workflow) == ("alpha", "beta", "zeta")


def test_lifecycle_stage_is_optional_metadata():
    validate_workflow(make_workflow(make_node("define")))


def test_multiple_steps_may_share_one_lifecycle_stage():
    validate_workflow(make_workflow(make_node("a"), make_node("b"), stage_map={
        "a": LifecycleStage.R2_EVIDENCE, "b": LifecycleStage.R2_EVIDENCE,
    }))


def test_workflow_does_not_require_all_r0_to_r8_nodes():
    workflow = make_workflow(make_node("define"), stage_map={"define": LifecycleStage.R0_DEFINE})
    validate_workflow(workflow)
