"""Executor registry and the DeterministicExecutor fake (Task 4, Steps 1-2).

Dispatch is strategy-based: ExecutorRegistry maps an execution-mode string
(registered by an adapter) to an Executor implementation. Resolution happens
by mode and never by step id, and an unknown mode fails explicitly with
ExecutorResolutionError — resolve never returns None and never falls back to
a default executor. Registrations are authoritative: a duplicate mode is
refused, never silently overwritten.

DeterministicExecutor is the fake executor the synthetic E2E fixture runs
(brief Step 2): for a step declaring exactly one output it derives one
semantically meaningful structured candidate — content ``{"kind": <declared
output kind>, "inputs": <bound artifact ids in order>, "rows": one
{"input_artifact_id": ...} per bound input}``, provenance facts
``input:<artifact id>`` plus ``mode:deterministic``. The executor never sees
input payloads (the derivation is semantic-real, not an echo), and
``execute`` is a pure function of (step, input binding): no Run/Attempt
state is read or written.
"""

from typing import Protocol, runtime_checkable

from ..domain import InputBinding, RuntimeContractError
from ...workflow.contract import WorkflowStep

from .candidate import CandidateOutput

DETERMINISTIC_MODE = "deterministic"
"""Registry mode string for the deterministic fake executor."""

DETERMINISTIC_SCHEMA_VERSION = "1"
"""Schema version the deterministic executor declares for its outputs."""


class ExecutorResolutionError(Exception):
    """Raised when no executor is registered for the requested mode."""


@runtime_checkable
class Executor(Protocol):
    """Structural contract implemented by every execution adapter.

    Executors are registered under a mode string and looked up by mode; the
    Runtime never dispatches on step id (Spec 7.2). The protocol is
    runtime-checkable so duck-typed adapters (e.g. the E2E fake) register
    without subclassing.
    """

    def execute(self, step: WorkflowStep, inputs: InputBinding) -> CandidateOutput: ...


class ExecutorRegistry:
    """Mode -> Executor registry (Spec 7.2 strategy dispatch).

    The registry is deliberately small: register an adapter under the
    execution-mode string its step declares, resolve it at execution time.
    """

    def __init__(self) -> None:
        self._executors: dict[str, Executor] = {}

    def register(self, mode: str, executor: Executor) -> None:
        """Bind *executor* to *mode*.

        Refuses blank modes, objects that do not satisfy the Executor
        protocol, and duplicate modes (the first registration stays
        authoritative).
        """
        if not isinstance(mode, str) or not mode.strip():
            raise RuntimeContractError(
                f"executor mode must be a non-empty string, got {mode!r}."
            )
        if not isinstance(executor, Executor):
            raise RuntimeContractError(
                "only objects implementing execute(step, inputs) can be "
                "registered as executors."
            )
        if mode in self._executors:
            raise RuntimeContractError(
                f"an executor is already registered for mode {mode!r}; "
                "registrations are never silently overwritten."
            )
        self._executors[mode] = executor

    def resolve(self, mode: str) -> Executor:
        """Return the executor registered for *mode*.

        Unknown modes fail explicitly with ExecutorResolutionError; the
        registry never returns None and never falls back to a default
        executor. The dispatch key is the mode string, never a step id.
        """
        try:
            return self._executors[mode]
        except KeyError:
            raise ExecutorResolutionError(
                f"no executor is registered for mode {mode!r}."
            ) from None


class DeterministicExecutor:
    """Derives the synthetic fixture's deterministic candidates (Step 2).

    Register under :data:`DETERMINISTIC_MODE`; the E2E orchestrator runs it
    as its fake executor.
    """

    MODE = DETERMINISTIC_MODE

    def execute(self, step: WorkflowStep, inputs: InputBinding) -> CandidateOutput:
        """Derive the single-output candidate for *inputs* against *step*.

        The binding must name the step being executed (a mismatch would
        commit under the wrong lineage) and the step must declare exactly
        one output (this executor produces one candidate per execution).
        """
        if not isinstance(step, WorkflowStep):
            raise RuntimeContractError("step must be a WorkflowStep.")
        if not isinstance(inputs, InputBinding):
            raise RuntimeContractError("inputs must be an InputBinding.")
        if len(step.outputs) != 1:
            raise RuntimeContractError(
                f"DeterministicExecutor executes steps declaring exactly one "
                f"output; step {step.id!r} declares {len(step.outputs)}."
            )
        if step.id != inputs.step_id:
            raise RuntimeContractError(
                f"input binding {inputs.input_binding_id!r} is bound to step "
                f"{inputs.step_id!r}, not the step being executed ({step.id!r})."
            )
        output = step.outputs[0]
        rows = [
            {"input_artifact_id": artifact_id}
            for artifact_id in inputs.artifact_ids
        ]
        return CandidateOutput(
            content={
                "kind": output.kind,
                "inputs": inputs.artifact_ids,
                "rows": rows,
            },
            schema_identity=output.kind,
            schema_version=DETERMINISTIC_SCHEMA_VERSION,
            provenance=(
                *(f"input:{artifact_id}" for artifact_id in inputs.artifact_ids),
                f"mode:{DETERMINISTIC_MODE}",
            ),
        )
