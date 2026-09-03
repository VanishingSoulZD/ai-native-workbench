"""Lightweight executor boundary and runner for declared workflows."""

from dataclasses import dataclass, field
from typing import Mapping, Protocol

from .composition import WorkflowDefinition, execution_order, validate_workflow
from .contract import WorkflowStep


class StepExecutor(Protocol):
    def execute(self, step: WorkflowStep, context: "WorkflowExecutionContext") -> Mapping[str, object]: ...


class WorkflowExecutionError(RuntimeError):
    """Raised for invalid execution operations outside normal run results."""


@dataclass(frozen=True)
class WorkflowExecutionContext:
    case_id: str
    inputs: Mapping[str, object]
    step_outputs: Mapping[str, Mapping[str, object]] = field(default_factory=dict)
    approved_gates: frozenset[str] = frozenset()


@dataclass(frozen=True)
class StepExecutionResult:
    step_id: str
    status: str
    outputs: Mapping[str, object]
    error: str | None = None


@dataclass(frozen=True)
class WorkflowRunResult:
    status: str
    steps: tuple[StepExecutionResult, ...]
    blocked_step_id: str | None = None


class WorkflowRunner:
    """Run a validated workflow through a supplied executor implementation."""

    def __init__(self, workflow: WorkflowDefinition, executor: StepExecutor) -> None:
        self._workflow = workflow
        self._executor = executor

    def run(self, context: WorkflowExecutionContext) -> WorkflowRunResult:
        validate_workflow(self._workflow)
        nodes = {node.step.id: node for node in self._workflow.steps}
        current_context = context
        results: list[StepExecutionResult] = []

        for step_id in execution_order(self._workflow):
            node = nodes[step_id]
            if node.step.human_gate.required and step_id not in current_context.approved_gates:
                return WorkflowRunResult("blocked", tuple(results), blocked_step_id=step_id)
            try:
                outputs = self._executor.execute(node.step, current_context)
            except Exception as error:
                results.append(StepExecutionResult(step_id, "failed", {}, str(error)))
                return WorkflowRunResult("failed", tuple(results))

            recorded_outputs = dict(outputs)
            results.append(StepExecutionResult(step_id, "succeeded", recorded_outputs))
            next_outputs = dict(current_context.step_outputs)
            next_outputs[step_id] = recorded_outputs
            current_context = WorkflowExecutionContext(
                case_id=current_context.case_id,
                inputs=current_context.inputs,
                step_outputs=next_outputs,
                approved_gates=current_context.approved_gates,
            )
        return WorkflowRunResult("succeeded", tuple(results))
