from ai_native_workbench.research.workflow import (
    GateRequirement,
    LifecycleStage,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    WorkflowDefinition,
    WorkflowExecutionContext,
    WorkflowNode,
    WorkflowRunner,
    WorkflowStep,
)


class SyntheticCaseExecutor:
    def __init__(self):
        self.calls: list[str] = []

    def execute(self, step, context):
        self.calls.append(step.id)
        return {output.name: f"{context.case_id}:{step.id}" for output in step.outputs}


def make_step(step_id: str, depends_on: tuple[str, ...] = ()) -> WorkflowNode:
    return WorkflowNode(
        step=WorkflowStep(
            id=step_id,
            name=step_id.replace("_", " ").title(),
            version="1.0.0",
            purpose="Support a tool-adoption research question.",
            inputs=(StepInput("research_request", "text"),),
            outputs=(StepOutput("result", "text"),),
            preconditions=("research request is available",),
            method=("perform the declared research operation",),
            constraints=("do not change the research scope",),
            human_gate=GateRequirement(False, None),
            validation=("result exists",),
            provenance=ProvenanceRequirement(False, ()),
        ),
        depends_on=depends_on,
    )


def test_new_case_executes_through_the_shared_workflow_interfaces():
    workflow = WorkflowDefinition(
        id="project-management-adoption-v1",
        version="1.0.0",
        steps=(
            make_step("frame_question"),
            make_step("collect_evidence", ("frame_question",)),
            make_step("synthesize_answer", ("collect_evidence",)),
        ),
        lifecycle_stage_map={
            "frame_question": LifecycleStage.R0_DEFINE,
            "collect_evidence": LifecycleStage.R2_EVIDENCE,
            "synthesize_answer": LifecycleStage.R5_SYNTHESIZE,
        },
    )
    executor = SyntheticCaseExecutor()
    context = WorkflowExecutionContext(
        case_id="small-team-project-management-tool",
        inputs={"research_request": "Should a small team adopt a new project-management tool?"},
    )

    result = WorkflowRunner(workflow, executor).run(context)

    assert context.case_id == "small-team-project-management-tool"
    assert executor.calls == ["frame_question", "collect_evidence", "synthesize_answer"]
    assert result.status == "succeeded"
    assert [step.step_id for step in result.steps] == executor.calls
