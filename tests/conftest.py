import pytest

from ai_native_workbench.research.workflow.contract import GateRequirement, ProvenanceRequirement, StepInput, StepOutput, WorkflowStep
from ai_native_workbench.research.workflow.composition import LifecycleStage, WorkflowDefinition, WorkflowNode


def make_step(step_id: str, *, gate_required: bool = False, gate_type: str | None = None, depends_on: tuple[str, ...] = ()) -> WorkflowNode:
    step = WorkflowStep(id=step_id, name=step_id.replace("_", " ").title(), version="1.0.0", purpose=f"Execute {step_id}.", inputs=(StepInput("input", "value"),), outputs=(StepOutput("output", "value"),), preconditions=("preconditions are satisfied",), method=("perform the declared step method",), constraints=("do not change undeclared scope",), human_gate=GateRequirement(required=gate_required, gate_type=gate_type), validation=("declared output exists",), provenance=ProvenanceRequirement(required=False, rules=()))
    return WorkflowNode(step=step, depends_on=depends_on)


@pytest.fixture
def workflow():
    return WorkflowDefinition(id="research-basic-v1", version="1.0.0", steps=(make_step("define"), make_step("collect", depends_on=("define",)), make_step("synthesize", depends_on=("collect",))), lifecycle_stage_map={"define": LifecycleStage.R0_DEFINE, "collect": LifecycleStage.R2_EVIDENCE, "synthesize": LifecycleStage.R5_SYNTHESIZE})


@pytest.fixture
def workflow_with_required_gate():
    return WorkflowDefinition(id="research-gated-v1", version="1.0.0", steps=(make_step("define"), make_step("select", gate_required=True, gate_type="H2_POPULATION_SELECTION", depends_on=("define",))), lifecycle_stage_map={"define": LifecycleStage.R0_DEFINE, "select": LifecycleStage.R4_DECIDE})
