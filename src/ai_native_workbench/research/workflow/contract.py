"""Immutable public contracts for reusable research workflow steps."""

from dataclasses import dataclass


class StepValidationError(ValueError):
    """Raised when a workflow step does not satisfy its declared contract."""


@dataclass(frozen=True)
class StepInput:
    name: str
    kind: str


@dataclass(frozen=True)
class StepOutput:
    name: str
    kind: str


@dataclass(frozen=True)
class GateRequirement:
    required: bool
    gate_type: str | None


@dataclass(frozen=True)
class ProvenanceRequirement:
    required: bool
    rules: tuple[str, ...]


@dataclass(frozen=True)
class WorkflowStep:
    id: str
    name: str
    version: str
    purpose: str
    inputs: tuple[StepInput, ...]
    outputs: tuple[StepOutput, ...]
    preconditions: tuple[str, ...]
    method: tuple[str, ...]
    constraints: tuple[str, ...]
    human_gate: GateRequirement
    validation: tuple[str, ...]
    provenance: ProvenanceRequirement


def validate_step_contract(step: WorkflowStep) -> None:
    """Validate structural invariants of a reusable workflow step."""
    for field_name in ("id", "name", "version", "purpose"):
        if not getattr(step, field_name):
            raise StepValidationError(f"WorkflowStep {field_name} must not be empty.")

    if not step.inputs:
        raise StepValidationError("WorkflowStep must declare at least one input.")
    if not step.outputs:
        raise StepValidationError("WorkflowStep must declare at least one output.")
    _validate_artifact_fields("input", step.inputs)
    _validate_artifact_fields("output", step.outputs)
    if len({item.name for item in step.inputs}) != len(step.inputs):
        raise StepValidationError("WorkflowStep input names must be unique.")
    if len({item.name for item in step.outputs}) != len(step.outputs):
        raise StepValidationError("WorkflowStep output names must be unique.")
    if not step.method:
        raise StepValidationError("WorkflowStep must declare a method.")
    if not step.constraints:
        raise StepValidationError("WorkflowStep must declare constraints.")
    if step.human_gate.required and not step.human_gate.gate_type:
        raise StepValidationError("A required human gate must declare its type.")
    if step.provenance.required and not step.provenance.rules:
        raise StepValidationError("Required provenance must declare at least one rule.")


def _validate_artifact_fields(label: str, artifacts: tuple[StepInput, ...] | tuple[StepOutput, ...]) -> None:
    for artifact in artifacts:
        if not artifact.name or not artifact.name.strip():
            raise StepValidationError(f"WorkflowStep {label} names must not be empty.")
        if not artifact.kind or not artifact.kind.strip():
            raise StepValidationError(f"WorkflowStep {label} kinds must not be empty.")
