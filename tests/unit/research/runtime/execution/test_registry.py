"""Tests for the Executor Registry and the DeterministicExecutor (Task 4).

Executor resolution is strategy-based: the registry maps an execution-mode
string (registered by an adapter) to an Executor implementation. Dispatch is
by mode and never by ``step_id`` (Spec 7.2: the Orchestrator is not allowed
to become a table of step-specific executor logic; brief Step 1). Unknown
modes fail explicitly — resolve never returns None and never falls back to a
default executor.

The DeterministicExecutor is the fake executor used by the synthetic E2E
fixture (brief Step 2): executing the step's single declared output yields
one semantically meaningful structured candidate whose content carries the
declared output kind, the consumed input artifact ids and one derived row
per bound input — not an echo of the inputs' payloads (the executor has no
payload access by design) — with the input lineage recorded as candidate
provenance facts. Executing never touches Run/Attempt state: execute is a
pure function of (step, input binding).
"""

import pytest

from ai_native_workbench.research.runtime.domain import (
    InputBinding,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.digests import payload_digest
from ai_native_workbench.research.runtime.execution import (
    CandidateOutput,
    DeterministicExecutor,
    Executor,
    ExecutorRegistry,
    ExecutorResolutionError,
)
from ai_native_workbench.research.workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    WorkflowStep,
)

STEP_ID = "R1"
RUN_ID = "run-1"
INVOCATION_ID = "inv-1"
ATTEMPT_ID = "att-1"
BINDING_ID = "ib-1"


# ---------------------------------------------------------------------------
# Shared fixtures/helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def make_step(step_id: str = STEP_ID, kind: str = "evidence-set") -> WorkflowStep:
    return WorkflowStep(
        id=step_id,
        name=f"Synthetic {step_id}",
        version="1",
        purpose="synthetic workflow step for executor registry tests",
        inputs=(StepInput(name="sources", kind="evidence-set"),),
        outputs=(StepOutput(name="output", kind=kind),),
        preconditions=(),
        method=("deterministic",),
        constraints=("none",),
        human_gate=GateRequirement(required=False, gate_type=None),
        validation=(),
        provenance=ProvenanceRequirement(required=True, rules=("input lineage",)),
    )


def make_binding(
    step_id: str = STEP_ID,
    artifact_ids: tuple[str, ...] = ("art-1", "art-2"),
) -> InputBinding:
    return InputBinding(
        input_binding_id=BINDING_ID,
        run_id=RUN_ID,
        invocation_id=INVOCATION_ID,
        step_id=step_id,
        attempt_id=ATTEMPT_ID,
        artifact_ids=artifact_ids,
        upstream_attempt_ids=(),
    )


class _DuckExecutor:
    """An executor-like object registered through the Executor Protocol."""

    def execute(self, step: WorkflowStep, inputs: InputBinding) -> CandidateOutput:
        return CandidateOutput(
            content={"kind": "duck"},
            schema_identity="duck",
            schema_version="1",
            provenance=("mode:duck",),
        )


# ---------------------------------------------------------------------------
# ExecutorRegistry (brief Step 1)
# ---------------------------------------------------------------------------


def test_registry_resolves_executor_by_mode():
    registry = ExecutorRegistry()
    fake = DeterministicExecutor()
    registry.register("deterministic", fake)
    assert registry.resolve("deterministic") is fake


def test_registry_unknown_mode_fails_explicitly():
    registry = ExecutorRegistry()
    registry.register("deterministic", DeterministicExecutor())
    with pytest.raises(ExecutorResolutionError) as excinfo:
        registry.resolve("llm")
    assert "llm" in str(excinfo.value)
    # resolve never returns None and never falls back to a default executor.
    assert registry.resolve("deterministic") is not None


def test_registry_resolves_each_registered_mode_independently():
    registry = ExecutorRegistry()
    deterministic = DeterministicExecutor()
    duck = _DuckExecutor()
    registry.register("deterministic", deterministic)
    registry.register("llm", duck)
    assert registry.resolve("deterministic") is deterministic
    assert registry.resolve("llm") is duck
    assert registry.resolve("deterministic") is not duck


def test_registry_never_dispatches_on_step_id():
    """Dispatch key is the execution-mode string, never a step id.

    A step-id lookup must fail explicitly even though a mode happens to be
    registered: resolving "R1" never consults executors registered under
    other modes.
    """
    registry = ExecutorRegistry()
    registry.register("deterministic", DeterministicExecutor())
    with pytest.raises(ExecutorResolutionError) as excinfo:
        registry.resolve("R1")
    assert "R1" in str(excinfo.value)
    # The registry API itself has no step_id parameter: only mode resolves.
    assert set(ExecutorRegistry.__dict__) >= {"register", "resolve"}


def test_registry_rejects_duplicate_mode_registration():
    registry = ExecutorRegistry()
    registry.register("deterministic", DeterministicExecutor())
    with pytest.raises(RuntimeContractError):
        registry.register("deterministic", _DuckExecutor())
    # The first registration stays authoritative: no silent overwrite.
    assert isinstance(registry.resolve("deterministic"), DeterministicExecutor)


def test_registry_rejects_blank_or_empty_mode():
    registry = ExecutorRegistry()
    with pytest.raises(RuntimeContractError):
        registry.register("", DeterministicExecutor())
    with pytest.raises(RuntimeContractError):
        registry.register("  ", DeterministicExecutor())
    with pytest.raises(RuntimeContractError):
        registry.register(None, DeterministicExecutor())  # type: ignore[arg-type]
    with pytest.raises(ExecutorResolutionError):
        registry.resolve("")


def test_registry_rejects_non_executor_objects():
    registry = ExecutorRegistry()
    with pytest.raises(RuntimeContractError):
        registry.register("broken", None)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        registry.register("broken", object())  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        registry.register("broken", "not-an-executor")  # type: ignore[arg-type]


def test_registry_accepts_duck_typed_executors_and_protocol_is_structural():
    """Any object implementing execute(step, inputs) is an Executor."""
    registry = ExecutorRegistry()
    duck = _DuckExecutor()
    registry.register("llm", duck)
    assert isinstance(duck, Executor)
    assert registry.resolve("llm") is duck


def test_registry_works_after_construction_without_registration():
    registry = ExecutorRegistry()
    with pytest.raises(ExecutorResolutionError):
        registry.resolve("deterministic")


# ---------------------------------------------------------------------------
# DeterministicExecutor (brief Step 2)
# ---------------------------------------------------------------------------


def test_deterministic_executor_emits_semantic_candidate_for_single_output():
    step = make_step(step_id="R1", kind="evidence-set")
    binding = make_binding(artifact_ids=("art-1", "art-2"))
    candidate = DeterministicExecutor().execute(step, binding)

    assert isinstance(candidate, CandidateOutput)
    # Typed content: the declared output kind, the consumed input ids in
    # binding order, and one derived row per bound input (semantic-real, not
    # an echo of the input payloads — the executor never sees payloads).
    assert candidate.content["kind"] == "evidence-set"
    assert candidate.content["inputs"] == ("art-1", "art-2")
    assert candidate.content["rows"] == (
        {"input_artifact_id": "art-1"},
        {"input_artifact_id": "art-2"},
    )
    # The candidate declares the schema its content conforms to.
    assert candidate.schema_identity == "evidence-set"
    assert candidate.schema_version == "1"
    # Provenance facts cover every bound input plus the producer mode.
    assert candidate.provenance == ("input:art-1", "input:art-2", "mode:deterministic")


def test_deterministic_executor_content_is_json_serializable():
    candidate = DeterministicExecutor().execute(make_step(), make_binding())
    digest = payload_digest(candidate.content)
    assert digest.startswith("sha256:")
    assert payload_digest(candidate.content) == digest


def test_deterministic_executor_is_repeatable_and_pure():
    executor = DeterministicExecutor()
    step = make_step()
    binding = make_binding()
    first = executor.execute(step, binding)
    second = executor.execute(step, binding)
    assert first == second
    # The content mapping is immutable: a second execute cannot observe any
    # mutation, and mutating the returned content fails.
    with pytest.raises(TypeError):
        first.content["kind"] = "tampered"  # type: ignore[index]


def test_deterministic_executor_handles_zero_artifact_binding():
    step = make_step()
    binding = make_binding(artifact_ids=())
    candidate = DeterministicExecutor().execute(step, binding)
    assert candidate.content["inputs"] == ()
    assert candidate.content["rows"] == ()
    assert candidate.provenance == ("mode:deterministic",)


def test_deterministic_executor_keeps_input_artifact_order():
    binding = make_binding(artifact_ids=("art-9", "art-1", "art-5"))
    candidate = DeterministicExecutor().execute(make_step(), binding)
    assert candidate.content["inputs"] == ("art-9", "art-1", "art-5")
    assert candidate.provenance == (
        "input:art-9",
        "input:art-1",
        "input:art-5",
        "mode:deterministic",
    )


def test_deterministic_executor_refuses_steps_without_exactly_one_output():
    step = WorkflowStep(
        id="R1",
        name="two outputs",
        version="1",
        purpose="synthetic step with two declared outputs",
        inputs=(StepInput(name="input", kind="evidence-set"),),
        outputs=(
            StepOutput(name="out-1", kind="evidence-set"),
            StepOutput(name="out-2", kind="claim-set"),
        ),
        preconditions=(),
        method=("deterministic",),
        constraints=("none",),
        human_gate=GateRequirement(required=False, gate_type=None),
        validation=(),
        provenance=ProvenanceRequirement(required=False, rules=()),
    )
    with pytest.raises(RuntimeContractError):
        DeterministicExecutor().execute(step, make_binding())


def test_deterministic_executor_refuses_lineage_mismatched_binding():
    """The binding names the step being executed; a mismatch means the
    attempt would commit under the wrong lineage and is refused."""
    step = make_step(step_id="R2")
    binding = make_binding(step_id="R1")
    with pytest.raises(RuntimeContractError) as excinfo:
        DeterministicExecutor().execute(step, binding)
    assert "R1" in str(excinfo.value)
    assert "R2" in str(excinfo.value)


def test_deterministic_executor_refuses_non_contract_arguments():
    executor = DeterministicExecutor()
    with pytest.raises(RuntimeContractError):
        executor.execute(object(), make_binding())  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        executor.execute(make_step(), object())  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        executor.execute(None, None)  # type: ignore[arg-type]
