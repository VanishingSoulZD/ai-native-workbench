from dataclasses import fields

import pytest

from ai_native_workbench.research.workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    StepValidationError,
    WorkflowStep,
    validate_step_contract,
)


def make_valid_step(**overrides: object) -> WorkflowStep:
    values: dict[str, object] = {
        "id": "collect_evidence",
        "name": "Collect Evidence",
        "version": "1.0.0",
        "purpose": "Collect relevant evidence.",
        "inputs": (StepInput("research_question", "ResearchQuestion"),),
        "outputs": (StepOutput("evidence_set", "EvidenceSet"),),
        "preconditions": ("scope is approved",),
        "method": ("collect declared sources",),
        "constraints": ("do not change scope",),
        "human_gate": GateRequirement(required=False, gate_type=None),
        "validation": ("evidence set exists",),
        "provenance": ProvenanceRequirement(required=False, rules=()),
    }
    values.update(overrides)
    return WorkflowStep(**values)  # type: ignore[arg-type]


def test_workflow_package_imports():
    import ai_native_workbench.research.workflow as workflow

    assert workflow is not None


def test_valid_step_contract_is_accepted():
    validate_step_contract(make_valid_step())


@pytest.mark.parametrize("field", ["id", "name", "version", "purpose"])
def test_empty_identity_is_rejected(field: str):
    with pytest.raises(StepValidationError):
        validate_step_contract(make_valid_step(**{field: ""}))


@pytest.mark.parametrize("field", ["inputs", "outputs"])
def test_empty_inputs_or_outputs_are_rejected(field: str):
    with pytest.raises(StepValidationError):
        validate_step_contract(make_valid_step(**{field: ()}))


def test_duplicate_input_names_are_rejected():
    with pytest.raises(StepValidationError):
        validate_step_contract(make_valid_step(inputs=(StepInput("x", "a"), StepInput("x", "b"))))


def test_duplicate_output_names_are_rejected():
    with pytest.raises(StepValidationError):
        validate_step_contract(make_valid_step(outputs=(StepOutput("x", "a"), StepOutput("x", "b"))))


def test_required_gate_without_type_is_rejected():
    with pytest.raises(StepValidationError):
        validate_step_contract(make_valid_step(human_gate=GateRequirement(True, None)))


def test_required_provenance_without_rules_is_rejected():
    with pytest.raises(StepValidationError):
        validate_step_contract(make_valid_step(provenance=ProvenanceRequirement(True, ())))


def test_workflow_step_exposes_no_prompt_model_or_runtime_field():
    field_names = {field.name for field in fields(WorkflowStep)}

    assert not field_names.intersection({"prompt", "model", "tool", "agent", "runtime", "executor"})
