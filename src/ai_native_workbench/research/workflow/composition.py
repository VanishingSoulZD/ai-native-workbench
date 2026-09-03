"""Composition and lifecycle metadata for research workflows."""

from dataclasses import dataclass
from enum import Enum
import heapq
from typing import Mapping

from .contract import WorkflowStep, StepValidationError, validate_step_contract


class LifecycleStage(str, Enum):
    R0_DEFINE = "R0_DEFINE"
    R1_DISCOVER = "R1_DISCOVER"
    R2_EVIDENCE = "R2_EVIDENCE"
    R3_ANALYZE = "R3_ANALYZE"
    R4_DECIDE = "R4_DECIDE"
    R5_SYNTHESIZE = "R5_SYNTHESIZE"
    R6_EVALUATE = "R6_EVALUATE"
    R7_DELIVER = "R7_DELIVER"
    R8_ARCHIVE_UPDATE = "R8_ARCHIVE_UPDATE"


class WorkflowValidationError(ValueError):
    """Raised when a workflow graph or its steps are invalid."""


@dataclass(frozen=True)
class WorkflowNode:
    step: WorkflowStep
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkflowDefinition:
    id: str
    version: str
    steps: tuple[WorkflowNode, ...]
    lifecycle_stage_map: Mapping[str, LifecycleStage]


def validate_workflow(workflow: WorkflowDefinition) -> None:
    """Validate a workflow's step contracts, references, and dependency graph."""
    if not workflow.id:
        raise WorkflowValidationError("Workflow id must not be empty.")
    if not workflow.version:
        raise WorkflowValidationError("Workflow version must not be empty.")

    step_ids = tuple(node.step.id for node in workflow.steps)
    if len(set(step_ids)) != len(step_ids):
        raise WorkflowValidationError("Workflow step ids must be unique.")
    known_step_ids = set(step_ids)
    for node in workflow.steps:
        try:
            validate_step_contract(node.step)
        except StepValidationError as error:
            raise WorkflowValidationError(str(error)) from error
        unresolved = set(node.depends_on) - known_step_ids
        if unresolved:
            raise WorkflowValidationError(f"Unknown dependencies: {sorted(unresolved)}.")
    unknown_metadata = set(workflow.lifecycle_stage_map) - known_step_ids
    if unknown_metadata:
        raise WorkflowValidationError(f"Lifecycle metadata references unknown steps: {sorted(unknown_metadata)}.")
    _topological_order(workflow, validate=False)


def execution_order(workflow: WorkflowDefinition) -> tuple[str, ...]:
    """Return the workflow's deterministic, lexicographic topological order."""
    validate_workflow(workflow)
    return _topological_order(workflow, validate=False)


def _topological_order(workflow: WorkflowDefinition, *, validate: bool) -> tuple[str, ...]:
    if validate:
        validate_workflow(workflow)
    dependents: dict[str, list[str]] = {node.step.id: [] for node in workflow.steps}
    in_degree: dict[str, int] = {node.step.id: len(node.depends_on) for node in workflow.steps}
    for node in workflow.steps:
        for dependency in node.depends_on:
            dependents[dependency].append(node.step.id)

    ready = [step_id for step_id, degree in in_degree.items() if degree == 0]
    heapq.heapify(ready)
    ordered: list[str] = []
    while ready:
        step_id = heapq.heappop(ready)
        ordered.append(step_id)
        for dependent in dependents[step_id]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                heapq.heappush(ready, dependent)
    if len(ordered) != len(workflow.steps):
        raise WorkflowValidationError("Workflow dependencies must be acyclic.")
    return tuple(ordered)
