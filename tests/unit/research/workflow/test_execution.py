from ai_native_workbench.research.workflow.execution import WorkflowExecutionContext, WorkflowRunner


class EchoExecutor:
    def __init__(self):
        self.calls: list[str] = []
        self.contexts = []

    def execute(self, step, context):
        self.calls.append(step.id)
        self.contexts.append(context)
        return {output.name: f"{step.id}:{output.name}" for output in step.outputs}


def test_runner_executes_in_dependency_order(workflow):
    executor = EchoExecutor()
    result = WorkflowRunner(workflow, executor).run(WorkflowExecutionContext("case", {}))
    assert executor.calls == ["define", "collect", "synthesize"]
    assert result.status == "succeeded"


def test_runner_passes_prior_outputs_in_context(workflow):
    executor = EchoExecutor()
    WorkflowRunner(workflow, executor).run(WorkflowExecutionContext("case", {"request": "value"}))
    assert executor.contexts[1].inputs == {"request": "value"}
    assert executor.contexts[1].step_outputs == {"define": {"output": "define:output"}}


def test_required_gate_blocks_before_step_execution(workflow_with_required_gate):
    executor = EchoExecutor()
    result = WorkflowRunner(workflow_with_required_gate, executor).run(WorkflowExecutionContext("case", {}))
    assert result.status == "blocked"
    assert result.blocked_step_id == "select"
    assert executor.calls == ["define"]


def test_approved_gate_allows_execution(workflow_with_required_gate):
    executor = EchoExecutor()
    result = WorkflowRunner(workflow_with_required_gate, executor).run(WorkflowExecutionContext("case", {}, approved_gates=frozenset({"select"})))
    assert result.status == "succeeded"
    assert executor.calls == ["define", "select"]


def test_executor_failure_returns_failed_result_and_stops_downstream(workflow):
    class FailingExecutor(EchoExecutor):
        def execute(self, step, context):
            if step.id == "collect":
                raise RuntimeError("source unavailable")
            return super().execute(step, context)

    executor = FailingExecutor()
    result = WorkflowRunner(workflow, executor).run(WorkflowExecutionContext("case", {}))
    assert result.status == "failed"
    assert result.steps[-1].step_id == "collect"
    assert result.steps[-1].status == "failed"
    assert "source unavailable" in result.steps[-1].error
    assert "synthesize" not in executor.calls


def test_success_requires_every_step_to_succeed(workflow):
    executor = EchoExecutor()
    result = WorkflowRunner(workflow, executor).run(WorkflowExecutionContext("case", {}))
    assert result.status == "succeeded"
    assert all(step.status == "succeeded" for step in result.steps)


def test_executor_missing_declared_output_fails_the_step(workflow):
    class MissingOutputExecutor:
        def execute(self, step, context):
            return {}

    result = WorkflowRunner(workflow, MissingOutputExecutor()).run(WorkflowExecutionContext("case", {}))

    assert result.status == "failed"
    assert result.steps[-1].status == "failed"
    assert "missing declared outputs" in result.steps[-1].error


def test_executor_undeclared_output_fails_the_step(workflow):
    class UndeclaredOutputExecutor:
        def execute(self, step, context):
            return {"output": "declared", "extra": "undeclared"}

    result = WorkflowRunner(workflow, UndeclaredOutputExecutor()).run(WorkflowExecutionContext("case", {}))

    assert result.status == "failed"
    assert result.steps[-1].status == "failed"
    assert "undeclared outputs" in result.steps[-1].error
