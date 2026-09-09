"""Tests for CandidateOutput and the Candidate/Validation/Acceptance pipeline
(Task 4, brief Steps 3-4; acceptance coverage lives here per the brief).

Invariants under test:

- Candidate/Validation/Acceptance are a pure evaluation layer producing
  dispositions: they never take a store, never append events and never see
  Attempt records, so Attempt status semantics (PENDING/RUNNING/FAILED/
  SUCCEEDED) are untouched by any validation or acceptance outcome.
- Schema, provenance and domain failures produce explicit REJECTED
  dispositions under the automatic policy and so prevent Step completion
  (the orchestrator commits only ACCEPTED/DEFERRED candidates).
- Rejection is a recorded disposition, never a deletion: a rejected
  candidate stays intact and remains reusable history.
- Acceptance policies are explicit: automatic, human, canonical/domain.
- ValidationResult distinguishes an evaluated pass from an evaluated fail
  (structured reasons) and records an unevaluated dimension explicitly;
  AcceptanceResult carries the disposition plus per-dimension results so
  the orchestrator's proceed/stop decision is mechanical.
- The not-evaluated disposition is representable and honest: no result can
  claim a validation ran (passed) when it did not, so durable acceptance
  evidence never overstates what was validated.
"""

import pytest
from dataclasses import FrozenInstanceError

from ai_native_workbench.research.runtime.domain import (
    AttemptRecord,
    AttemptStatus,
    InputBinding,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.execution import (
    AcceptanceDisposition,
    AcceptancePipeline,
    AcceptancePolicy,
    AcceptanceResult,
    CandidateOutput,
    DeterministicExecutor,
    SchemaSpec,
    ValidationDimension,
    ValidationResult,
)
from ai_native_workbench.research.workflow.contract import (
    GateRequirement,
    ProvenanceRequirement,
    StepInput,
    StepOutput,
    WorkflowStep,
)

SCHEMA_IDENTITY = "evidence-set"
SCHEMA_VERSION = "1"
STEP_ID = "R1"
RUN_ID = "run-1"
INVOCATION_ID = "inv-1"
ATTEMPT_ID = "att-1"

GOOD_CONTENT = {
    "kind": "evidence-set",
    "inputs": ["art-1", "art-2"],
    "rows": [
        {"input_artifact_id": "art-1"},
        {"input_artifact_id": "art-2"},
    ],
}
GOOD_PROVENANCE = ("input:art-1", "input:art-2", "mode:deterministic")


# ---------------------------------------------------------------------------
# Shared fixtures/helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def make_schema(**overrides) -> SchemaSpec:
    defaults = dict(
        identity=SCHEMA_IDENTITY,
        version=SCHEMA_VERSION,
        required_fields=("kind", "inputs", "rows"),
        field_types={"kind": "string", "inputs": "array", "rows": "array"},
        constant_fields={"kind": "evidence-set"},
    )
    defaults.update(overrides)
    return SchemaSpec(**defaults)


def make_candidate(**overrides) -> CandidateOutput:
    defaults = dict(
        content=dict(GOOD_CONTENT),
        schema_identity=SCHEMA_IDENTITY,
        schema_version=SCHEMA_VERSION,
        provenance=GOOD_PROVENANCE,
    )
    defaults.update(overrides)
    return CandidateOutput(**defaults)


def make_pipeline(**overrides) -> AcceptancePipeline:
    defaults = dict(
        schema=make_schema(),
        provenance_required=True,
        domain_check=None,
    )
    defaults.update(overrides)
    return AcceptancePipeline(**defaults)


def make_attempt(status: AttemptStatus = AttemptStatus.RUNNING) -> AttemptRecord:
    return AttemptRecord(
        attempt_id=ATTEMPT_ID,
        run_id=RUN_ID,
        invocation_id=INVOCATION_ID,
        step_id=STEP_ID,
        status=status,
        input_binding_id="ib-1",
    )


def evidence_domain_check(content: object):
    """Synthetic fixture domain rule: every derived row cites a bound input.

    Rows are semantic units; a row deriving from an input that the content
    does not list as consumed is a domain violation. Returns
    (passed, reasons) per the declared-check contract.
    """
    reasons: list[str] = []
    if not isinstance(content, dict) and not hasattr(content, "get"):
        return (False, ("content must be a JSON object for the evidence domain rule.",))
    inputs = content.get("inputs") or ()
    rows = content.get("rows") or ()
    if not isinstance(inputs, (list, tuple)) or not isinstance(rows, (list, tuple)):
        return (False, ("domain content must declare inputs and rows arrays.",))
    for index, row in enumerate(rows):
        if not isinstance(row, dict) and not hasattr(row, "get"):
            reasons.append(f"derived row {index} must be a JSON object.")
            continue
        input_id = row.get("input_artifact_id")
        if not isinstance(input_id, str) or not input_id:
            reasons.append(f"derived row {index} must carry a string input_artifact_id.")
        elif input_id not in inputs:
            reasons.append(
                f"derived row {index} cites unknown input {input_id!r}."
            )
    return (not reasons, tuple(reasons))


def make_step() -> WorkflowStep:
    return WorkflowStep(
        id=STEP_ID,
        name=f"Synthetic {STEP_ID}",
        version="1",
        purpose="synthetic workflow step for acceptance pipeline tests",
        inputs=(StepInput(name="sources", kind="evidence-set"),),
        outputs=(StepOutput(name="output", kind=SCHEMA_IDENTITY),),
        preconditions=(),
        method=("deterministic",),
        constraints=("none",),
        human_gate=GateRequirement(required=False, gate_type=None),
        validation=(),
        provenance=ProvenanceRequirement(required=True, rules=("input lineage",)),
    )


# ---------------------------------------------------------------------------
# CandidateOutput record (frozen, JSON-able, keyword-constructed)
# ---------------------------------------------------------------------------


def test_candidate_output_record_is_frozen_and_immutable():
    candidate = make_candidate()
    with pytest.raises(TypeError):
        candidate.content["kind"] = "tampered"  # type: ignore[index]
    with pytest.raises(FrozenInstanceError):
        candidate.schema_identity = "other"


def test_candidate_output_deeply_freezes_content():
    candidate = make_candidate()
    # Content stays a dict subclass — JSON-serializable exactly as stored,
    # so artifact-commit digests can canonicalize it — but every mutator
    # refuses writes: a deep freeze, not a plain mutable copy.
    assert isinstance(candidate.content, dict)
    assert candidate.content["rows"] == (
        {"input_artifact_id": "art-1"},
        {"input_artifact_id": "art-2"},
    )
    nested = candidate.content["rows"][0]
    with pytest.raises(TypeError):
        nested["input_artifact_id"] = "tampered"  # type: ignore[index]
    with pytest.raises(TypeError):
        candidate.content["inputs"] = ("art-9",)  # type: ignore[index]


def test_candidate_output_refuses_non_mapping_content():
    with pytest.raises(RuntimeContractError):
        CandidateOutput(content="not a mapping", schema_identity="s", schema_version="1")
    with pytest.raises(RuntimeContractError):
        CandidateOutput(content=["list"], schema_identity="s", schema_version="1")


def test_candidate_output_refuses_non_json_serializable_content():
    with pytest.raises(RuntimeContractError):
        CandidateOutput(
            content={"kind": {"bad-key": object()}},
            schema_identity="s",
            schema_version="1",
        )
    with pytest.raises(RuntimeContractError):
        CandidateOutput(
            content={"kind": 1.5, "nan": float("nan")},
            schema_identity="s",
            schema_version="1",
        )
    with pytest.raises(RuntimeContractError):
        CandidateOutput(
            content={"kind": 1, 3: "non-string key"},
            schema_identity="s",
            schema_version="1",
        )


def test_candidate_output_refuses_blank_identities_and_bad_provenance():
    with pytest.raises(RuntimeContractError):
        CandidateOutput(content={"kind": "x"}, schema_identity="", schema_version="1")
    with pytest.raises(RuntimeContractError):
        CandidateOutput(content={"kind": "x"}, schema_identity="s", schema_version="  ")
    with pytest.raises(RuntimeContractError):
        CandidateOutput(
            content={"kind": "x"},
            schema_identity="s",
            schema_version="1",
            provenance=("input:art-1", "input:art-1"),
        )
    with pytest.raises(RuntimeContractError):
        CandidateOutput(
            content={"kind": "x"},
            schema_identity="s",
            schema_version="1",
            provenance=(1,),  # type: ignore[list-item]
        )


def test_candidate_output_allows_empty_provenance():
    candidate = CandidateOutput(
        content={"kind": "x"},
        schema_identity="s",
        schema_version="1",
        provenance=(),
    )
    assert candidate.provenance == ()


# ---------------------------------------------------------------------------
# SchemaSpec record (the v1 schema seam: no schema framework)
# ---------------------------------------------------------------------------


def test_schema_spec_validates_conforming_content():
    assert make_schema().check(GOOD_CONTENT) == (True, ())


def test_schema_spec_detects_missing_required_fields():
    passed, reasons = make_schema().check({"kind": "evidence-set"})
    assert passed is False
    assert any("inputs" in reason for reason in reasons)
    assert any("rows" in reason for reason in reasons)


def test_schema_spec_detects_type_mismatches_and_empty_strings():
    spec = make_schema()
    passed, reasons = spec.check(
        {"kind": "evidence-set", "inputs": "not-an-array", "rows": {}}
    )
    assert passed is False
    assert any("inputs" in reason and "array" in reason for reason in reasons)
    assert any("rows" in reason and "array" in reason for reason in reasons)
    passed, reasons = spec.check({"kind": "", "inputs": [], "rows": []})
    assert passed is False
    assert any("kind" in reason for reason in reasons)
    # A non-empty array is fine even when the tuple is empty (no inputs).
    passed, reasons = spec.check({"kind": "evidence-set", "inputs": [], "rows": ()})
    assert passed is True


def test_schema_spec_detects_constant_field_violations():
    passed, reasons = make_schema().check(
        {"kind": "claim-set", "inputs": [], "rows": []}
    )
    assert passed is False
    assert any("kind" in reason for reason in reasons)


def test_schema_spec_requires_json_object_content():
    passed, reasons = make_schema().check(["not", "an", "object"])
    assert passed is False
    assert reasons


def test_schema_spec_rejects_malformed_declarations():
    with pytest.raises(RuntimeContractError):
        SchemaSpec(identity="", version="1")
    with pytest.raises(RuntimeContractError):
        SchemaSpec(identity="s", version="1", required_fields=("kind", "kind"))
    with pytest.raises(RuntimeContractError):
        SchemaSpec(
            identity="s",
            version="1",
            required_fields=("kind",),
            field_types={"kind": "regex"},  # unknown type token
        )
    with pytest.raises(RuntimeContractError):
        SchemaSpec(
            identity="s",
            version="1",
            field_types={"kind": "string"},  # token without required entry
        )
    with pytest.raises(RuntimeContractError):
        SchemaSpec(
            identity="s",
            version="1",
            constant_fields={"kind": "evidence-set"},  # constant without required entry
        )
    with pytest.raises(RuntimeContractError):
        SchemaSpec(
            identity="s",
            version="1",
            required_fields=("kind",),
            constant_fields={"kind": {"nested": "mapping"}},
        )
    with pytest.raises(RuntimeContractError):
        SchemaSpec(identity="s", version="1", required_fields=("kind",), field_types=[])


# ---------------------------------------------------------------------------
# ValidationResult record
# ---------------------------------------------------------------------------


def _ok_result(dimension=ValidationDimension.SCHEMA) -> ValidationResult:
    return ValidationResult(dimension=dimension, passed=True)


def test_validation_result_requires_reasons_when_failed_only():
    with pytest.raises(RuntimeContractError):
        ValidationResult(dimension=ValidationDimension.SCHEMA, passed=False)
    with pytest.raises(RuntimeContractError):
        ValidationResult(
            dimension=ValidationDimension.SCHEMA,
            passed=True,
            reasons=("no reason for pass",),
        )
    ok = ValidationResult(dimension=ValidationDimension.SCHEMA, passed=True)
    assert ok.reasons == ()
    assert ok.evaluated is True
    failed = ValidationResult(
        dimension=ValidationDimension.SCHEMA,
        passed=False,
        reasons=("missing field",),
    )
    assert failed.passed is False
    assert failed.evaluated is True


def test_validation_result_records_not_evaluated_distinctly():
    """A not-evaluated marker is representable and is neither a pass nor an
    evaluated failure: the record layer can always tell "checked and
    passed" apart from "not evaluated"."""
    marker = ValidationResult(
        dimension=ValidationDimension.DOMAIN, passed=False, evaluated=False
    )
    assert marker.dimension is ValidationDimension.DOMAIN
    assert marker.passed is False
    assert marker.reasons == ()
    assert marker.evaluated is False
    assert marker != _ok_result(ValidationDimension.DOMAIN)
    assert marker != ValidationResult(
        dimension=ValidationDimension.DOMAIN,
        passed=False,
        reasons=("a real evaluated failure",),
    )


def test_validation_result_not_evaluated_cannot_claim_a_pass_or_reasons():
    with pytest.raises(RuntimeContractError):
        # The vacuous-pass lie: claiming a pass without an evaluation.
        ValidationResult(
            dimension=ValidationDimension.DOMAIN, passed=True, evaluated=False
        )
    with pytest.raises(RuntimeContractError):
        # Reasons belong to evaluated failures; a marker carries none.
        ValidationResult(
            dimension=ValidationDimension.DOMAIN,
            passed=False,
            reasons=("not really a failure",),
            evaluated=False,
        )
    with pytest.raises(RuntimeContractError):
        ValidationResult(
            dimension=ValidationDimension.DOMAIN,
            passed=False,
            evaluated="yes",  # type: ignore[arg-type]
        )


def test_validation_result_rejects_malformed_fields():
    with pytest.raises(RuntimeContractError):
        ValidationResult(dimension="schema", passed=True)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        ValidationResult(  # passed must be a real bool
            dimension=ValidationDimension.SCHEMA,
            passed="yes",  # type: ignore[arg-type]
        )
    with pytest.raises(RuntimeContractError):
        ValidationResult(
            dimension=ValidationDimension.SCHEMA,
            passed=False,
            reasons=("",),  # type: ignore[list-item]
        )


# ---------------------------------------------------------------------------
# AcceptancePipeline: validate_schema
# ---------------------------------------------------------------------------


def test_validate_schema_passes_conforming_candidate():
    result = make_pipeline().validate_schema(make_candidate())
    assert result.dimension is ValidationDimension.SCHEMA
    assert result.passed is True
    assert result.reasons == ()


def test_validate_schema_rejects_declared_identity_mismatch():
    candidate = make_candidate(schema_identity="claim-set", schema_version="2")
    result = make_pipeline().validate_schema(candidate)
    assert result.passed is False
    assert any("claim-set" in reason for reason in result.reasons)
    assert any("evidence-set" in reason for reason in result.reasons)


def test_validate_schema_rejects_content_violations():
    candidate = make_candidate(content={"kind": "claim-set", "inputs": [], "rows": []})
    result = make_pipeline().validate_schema(candidate)
    assert result.passed is False
    assert any("kind" in reason for reason in result.reasons)


def test_validate_schema_requires_a_candidate():
    pipeline = make_pipeline()
    with pytest.raises(RuntimeContractError):
        pipeline.validate_schema(object())  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        pipeline.validate_schema(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# AcceptancePipeline: validate_provenance
# ---------------------------------------------------------------------------


def test_validate_provenance_requires_facts_when_required():
    pipeline = make_pipeline(provenance_required=True)
    assert pipeline.validate_provenance(make_candidate()).passed is True
    bare = make_candidate(provenance=())
    result = pipeline.validate_provenance(bare)
    assert result.passed is False
    assert any("provenance" in reason for reason in result.reasons)
    # A provenance dimension result never modifies Attempt state.
    attempt = make_attempt()
    assert attempt.status is AttemptStatus.RUNNING


def test_validate_provenance_is_optional_when_not_required():
    pipeline = make_pipeline(provenance_required=False)
    assert pipeline.validate_provenance(make_candidate(provenance=())).passed is True


# ---------------------------------------------------------------------------
# AcceptancePipeline: validate_domain
# ---------------------------------------------------------------------------


def test_validate_domain_passes_and_fails_with_declared_hook():
    pipeline = make_pipeline(domain_check=evidence_domain_check)
    ok = pipeline.validate_domain(make_candidate())
    assert ok.passed is True
    assert ok.evaluated is True
    incoherent = make_candidate(
        content={
            "kind": "evidence-set",
            "inputs": ["art-1"],
            "rows": [{"input_artifact_id": "art-ghost"}],
        }
    )
    result = pipeline.validate_domain(incoherent)
    assert result.passed is False
    assert result.evaluated is True
    assert any("art-ghost" in reason for reason in result.reasons)


def test_validate_domain_without_declared_hook_records_not_evaluated():
    """A pipeline with no declared domain rule records the dimension as not
    evaluated — never as a pass — so the result cannot be mistaken for a
    checked-and-passed verdict.

    Automatic acceptance over such a pipeline gates on schema and
    provenance only; canonical/domain acceptance refuses to run without a
    declared domain check.
    """
    result = make_pipeline(domain_check=None).validate_domain(make_candidate())
    assert result.dimension is ValidationDimension.DOMAIN
    assert result.passed is False
    assert result.reasons == ()
    assert result.evaluated is False


def test_validate_domain_refuses_malformed_hook_results():
    def broken(content: object):
        return "not-a-pair"  # type: ignore[return-value]

    pipeline = make_pipeline(domain_check=broken)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        pipeline.validate_domain(make_candidate())


def test_validate_domain_requires_a_candidate():
    pipeline = make_pipeline(domain_check=evidence_domain_check)
    with pytest.raises(RuntimeContractError):
        pipeline.validate_domain(object())  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# AcceptancePipeline: accept() and explicit policies (brief Step 4)
# ---------------------------------------------------------------------------


def test_accept_automatic_accepts_when_all_dimensions_pass():
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        make_candidate(), AcceptancePolicy.AUTOMATIC
    )
    assert result.disposition is AcceptanceDisposition.ACCEPTED
    assert result.policy is AcceptancePolicy.AUTOMATIC
    assert set(result.validation) == {
        ValidationDimension.SCHEMA,
        ValidationDimension.PROVENANCE,
        ValidationDimension.DOMAIN,
    }
    assert all(item.passed for item in result.validation.values())
    assert all(item.evaluated for item in result.validation.values())
    assert result.reasons == ()


def test_accept_automatic_accepts_without_a_domain_hook_recording_not_evaluated():
    """Automatic acceptance over a hook-less pipeline gates on schema and
    provenance only: the unevaluated domain is acceptable by policy, and the
    disposition record keeps it as not evaluated — never as a domain pass."""
    result = make_pipeline(domain_check=None).accept(
        make_candidate(), AcceptancePolicy.AUTOMATIC
    )
    assert result.disposition is AcceptanceDisposition.ACCEPTED
    domain = result.validation[ValidationDimension.DOMAIN]
    assert domain.evaluated is False
    assert domain.passed is False
    assert domain.reasons == ()
    assert result.validation[ValidationDimension.SCHEMA].evaluated is True
    assert result.validation[ValidationDimension.SCHEMA].passed is True
    assert result.validation[ValidationDimension.PROVENANCE].evaluated is True
    assert result.validation[ValidationDimension.PROVENANCE].passed is True
    assert result.reasons == ()


def test_accept_automatic_rejects_on_schema_failure():
    candidate = make_candidate(content={"kind": "claim-set", "inputs": [], "rows": []})
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        candidate, AcceptancePolicy.AUTOMATIC
    )
    assert result.disposition is AcceptanceDisposition.REJECTED
    assert result.validation[ValidationDimension.SCHEMA].passed is False
    assert any("schema" in reason for reason in result.reasons)
    # The candidate itself is untouched: rejection is a recorded disposition.
    assert candidate.schema_identity == SCHEMA_IDENTITY


def test_accept_automatic_rejects_on_provenance_failure():
    candidate = make_candidate(provenance=())
    result = make_pipeline().accept(candidate, AcceptancePolicy.AUTOMATIC)
    assert result.disposition is AcceptanceDisposition.REJECTED
    assert any("provenance" in reason for reason in result.reasons)


def test_accept_automatic_rejects_on_domain_failure():
    candidate = make_candidate(
        content={
            "kind": "evidence-set",
            "inputs": ["art-1"],
            "rows": [{"input_artifact_id": "art-ghost"}],
        }
    )
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        candidate, AcceptancePolicy.AUTOMATIC
    )
    assert result.disposition is AcceptanceDisposition.REJECTED
    assert result.validation[ValidationDimension.DOMAIN].passed is False
    assert result.validation[ValidationDimension.DOMAIN].evaluated is True
    assert any("domain" in reason for reason in result.reasons)
    assert any("art-ghost" in reason for reason in result.reasons)


def test_accept_automatic_rejection_names_only_evaluated_failures():
    """A rejection never lists an unevaluated dimension as a cause: the
    hook-less domain stays not-evaluated while schema reasons explain the
    rejection."""
    candidate = make_candidate(content={"kind": "claim-set", "inputs": [], "rows": []})
    result = make_pipeline(domain_check=None).accept(
        candidate, AcceptancePolicy.AUTOMATIC
    )
    assert result.disposition is AcceptanceDisposition.REJECTED
    assert result.validation[ValidationDimension.SCHEMA].passed is False
    domain = result.validation[ValidationDimension.DOMAIN]
    assert domain.evaluated is False
    assert domain.passed is False
    assert any("schema" in reason for reason in result.reasons)
    assert not any(reason.startswith("domain:") for reason in result.reasons)


def test_accept_rejected_candidate_remains_durable_history():
    """Rejected candidates are never deleted or rewritten; the same candidate
    stays reusable — a human-policy pipeline may still review it."""
    candidate = make_candidate(provenance=())
    first = make_pipeline().accept(candidate, AcceptancePolicy.AUTOMATIC)
    assert first.disposition is AcceptanceDisposition.REJECTED
    # No mutation, no deletion: the candidate is still the identical record.
    assert candidate.provenance == ()
    assert first.validation[ValidationDimension.PROVENANCE].reasons
    # Re-evaluation is deterministic: the disposition is repeatable.
    second = make_pipeline().accept(candidate, AcceptancePolicy.AUTOMATIC)
    assert second == first


def test_accept_human_defers_when_mechanical_gates_pass():
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        make_candidate(), AcceptancePolicy.HUMAN
    )
    assert result.disposition is AcceptanceDisposition.DEFERRED_TO_HUMAN
    assert any("human" in reason for reason in result.reasons)


def test_accept_human_rejects_mechanically_invalid_candidates():
    """Schema/provenance failures prevent forwarding to a human review."""
    bad_schema = make_candidate(content={"kind": "claim-set", "inputs": [], "rows": []})
    result = make_pipeline().accept(bad_schema, AcceptancePolicy.HUMAN)
    assert result.disposition is AcceptanceDisposition.REJECTED
    assert any("schema" in reason for reason in result.reasons)
    bare = make_candidate(provenance=())
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        bare, AcceptancePolicy.HUMAN
    )
    assert result.disposition is AcceptanceDisposition.REJECTED
    assert any("provenance" in reason for reason in result.reasons)


def test_accept_human_defers_on_domain_failure_with_advisory_reasons():
    """Under the human policy the human is the domain judge: a machine domain
    failure defers the decision and rides along as advisory context."""
    candidate = make_candidate(
        content={
            "kind": "evidence-set",
            "inputs": ["art-1"],
            "rows": [{"input_artifact_id": "art-ghost"}],
        }
    )
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        candidate, AcceptancePolicy.HUMAN
    )
    assert result.disposition is AcceptanceDisposition.DEFERRED_TO_HUMAN
    assert result.validation[ValidationDimension.DOMAIN].passed is False
    assert result.validation[ValidationDimension.DOMAIN].evaluated is True
    assert any("art-ghost" in reason for reason in result.reasons)


def test_accept_human_without_a_domain_hook_defers_without_domain_claims():
    """The machine records no domain verdict under the human policy either:
    the candidate defers to the human reviewer and the domain dimension
    stays not-evaluated — no fabricated pass rides into the record."""
    result = make_pipeline(domain_check=None).accept(
        make_candidate(), AcceptancePolicy.HUMAN
    )
    assert result.disposition is AcceptanceDisposition.DEFERRED_TO_HUMAN
    domain = result.validation[ValidationDimension.DOMAIN]
    assert domain.evaluated is False
    assert domain.passed is False
    assert domain.reasons == ()
    assert any("human" in reason for reason in result.reasons)
    assert not any(reason.startswith("domain:") for reason in result.reasons)


def test_accept_canonical_domain_requires_a_declared_domain_check():
    pipeline = make_pipeline(domain_check=None)
    with pytest.raises(RuntimeContractError) as excinfo:
        pipeline.accept(make_candidate(), AcceptancePolicy.CANONICAL_DOMAIN)
    assert "canonical/domain" in str(excinfo.value)


def test_accept_canonical_domain_accepts_when_domain_gates_pass():
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        make_candidate(), AcceptancePolicy.CANONICAL_DOMAIN
    )
    assert result.disposition is AcceptanceDisposition.ACCEPTED


def test_accept_canonical_domain_rejects_on_domain_failure():
    candidate = make_candidate(
        content={
            "kind": "evidence-set",
            "inputs": ["art-1"],
            "rows": [{"input_artifact_id": "art-ghost"}],
        }
    )
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        candidate, AcceptancePolicy.CANONICAL_DOMAIN
    )
    assert result.disposition is AcceptanceDisposition.REJECTED
    assert any("domain" in reason for reason in result.reasons)


def test_accept_canonical_domain_still_rejects_structural_failures():
    candidate = make_candidate(schema_identity="claim-set", schema_version="2")
    result = make_pipeline(domain_check=evidence_domain_check).accept(
        candidate, AcceptancePolicy.CANONICAL_DOMAIN
    )
    assert result.disposition is AcceptanceDisposition.REJECTED


def test_accept_rejects_unknown_policy_and_non_candidates():
    pipeline = make_pipeline()
    with pytest.raises(RuntimeContractError):
        pipeline.accept(make_candidate(), "automatic")  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        pipeline.accept(object(), AcceptancePolicy.AUTOMATIC)  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        pipeline.accept(None, None)  # type: ignore[arg-type]


def test_acceptance_pipeline_is_pure_repeatable_and_attempt_neutral():
    """The pipeline never touches a store or Attempt records: the same inputs
    yield the same dispositions, forever, across fresh instances."""
    pipeline = make_pipeline(domain_check=evidence_domain_check)
    attempt = make_attempt()
    candidate = make_candidate()
    first = pipeline.accept(candidate, AcceptancePolicy.AUTOMATIC)
    second = pipeline.accept(candidate, AcceptancePolicy.AUTOMATIC)
    assert first == second
    assert first == AcceptanceResult(
        disposition=AcceptanceDisposition.ACCEPTED,
        policy=AcceptancePolicy.AUTOMATIC,
        validation={
            ValidationDimension.SCHEMA: _ok_result(),
            ValidationDimension.PROVENANCE: _ok_result(
                ValidationDimension.PROVENANCE
            ),
            ValidationDimension.DOMAIN: _ok_result(ValidationDimension.DOMAIN),
        },
        reasons=(),
    )
    # Attempt semantics are untouched by the evaluation layer.
    assert attempt.status is AttemptStatus.RUNNING
    assert attempt == make_attempt()
    # The candidate produced by the deterministic executor passes the same
    # schema/domain rules the fixture declares (semantic-real, not echo).
    binding = InputBinding(
        input_binding_id="ib-1",
        run_id=RUN_ID,
        invocation_id=INVOCATION_ID,
        step_id=STEP_ID,
        attempt_id=ATTEMPT_ID,
        artifact_ids=("art-1", "art-2"),
        upstream_attempt_ids=(),
    )
    executed = DeterministicExecutor().execute(make_step(), binding)
    assert make_pipeline(domain_check=evidence_domain_check).accept(
        executed, AcceptancePolicy.AUTOMATIC
    ).disposition is AcceptanceDisposition.ACCEPTED


# ---------------------------------------------------------------------------
# AcceptanceResult / AcceptancePolicy records
# ---------------------------------------------------------------------------


def test_acceptance_result_rejects_malformed_records():
    def full(**overrides) -> dict:
        values = {
            ValidationDimension.SCHEMA: _ok_result(),
            ValidationDimension.PROVENANCE: _ok_result(),
            ValidationDimension.DOMAIN: _ok_result(),
        }
        values.update(overrides)
        return values

    with pytest.raises(RuntimeContractError):
        # DEFERRED_TO_HUMAN is legal only under the human policy.
        AcceptanceResult(
            disposition=AcceptanceDisposition.DEFERRED_TO_HUMAN,
            policy=AcceptancePolicy.AUTOMATIC,
            validation=full(),
        )
    with pytest.raises(RuntimeContractError):
        AcceptanceResult(  # all three dimensions must be evaluated
            disposition=AcceptanceDisposition.ACCEPTED,
            policy=AcceptancePolicy.AUTOMATIC,
            validation={},
        )
    with pytest.raises(RuntimeContractError):
        # A result whose dimension does not match its key is contradictory.
        AcceptanceResult(
            disposition=AcceptanceDisposition.ACCEPTED,
            policy=AcceptancePolicy.AUTOMATIC,
            validation=full(
                **{
                    ValidationDimension.SCHEMA: _ok_result(
                        ValidationDimension.PROVENANCE
                    )
                }
            ),
        )
    with pytest.raises(RuntimeContractError):
        AcceptanceResult(  # values must be ValidationResult records
            disposition=AcceptanceDisposition.ACCEPTED,
            policy=AcceptancePolicy.AUTOMATIC,
            validation=full(
                **{ValidationDimension.SCHEMA: "passed"}  # type: ignore[dict-item]
            ),
        )
    with pytest.raises(RuntimeContractError):
        AcceptanceResult(  # policies and dispositions are explicit enums
            disposition="ACCEPTED",  # type: ignore[arg-type]
            policy=AcceptancePolicy.AUTOMATIC,
            validation=full(),
        )


def test_acceptance_policy_tokens_are_explicit():
    assert AcceptancePolicy.AUTOMATIC.value == "automatic"
    assert AcceptancePolicy.HUMAN.value == "human"
    assert AcceptancePolicy.CANONICAL_DOMAIN.value == "canonical/domain"
    assert AcceptanceDisposition.ACCEPTED.value == "ACCEPTED"
    assert AcceptanceDisposition.REJECTED.value == "REJECTED"
    assert AcceptanceDisposition.DEFERRED_TO_HUMAN.value == "DEFERRED_TO_HUMAN"
    assert ValidationDimension.SCHEMA.value == "schema"
    assert ValidationDimension.PROVENANCE.value == "provenance"
    assert ValidationDimension.DOMAIN.value == "domain"
