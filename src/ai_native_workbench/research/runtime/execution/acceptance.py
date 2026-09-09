"""Candidate validation and acceptance pipeline (Task 4, brief Steps 3-4).

The pipeline is the pure evaluation layer between an executed Candidate and
the orchestrator's proceed/stop decision. Invariants:

- Purity: AcceptancePipeline holds only the declared schema and hooks; it
  never takes a store, never appends events and never sees Attempt records.
  Recording dispositions (VALIDATION_COMPLETED / ACCEPTANCE_RECORDED) is
  the control layer's job (Task 6); rejection here is a recorded
  disposition, never a deletion — candidates stay intact and reusable
  history.
- The v1 schema seam is minimal by design: SchemaSpec (identity/version,
  required field names, JSON type tokens, exact constants) declares the
  schema the step's output content must conform to. No schema framework
  exists in v1, so pipelines are constructed with the declared schema for
  the step being validated.
- Domain validation is a declared hook ``(content) -> (passed, reasons)``
  — the seam real domain knowledge plugs into. With no hook the domain
  dimension is recorded as explicitly not evaluated (never as a pass), so
  a durable result can never claim a validation ran when it did not;
  canonical/domain acceptance refuses to run without a declared hook.
- Policies are explicit: ``automatic`` (schema, provenance and, when a
  hook is declared, domain gate acceptance; an unevaluated domain is
  acceptable by policy and stays recorded as not evaluated), ``human``
  (mechanical schema + provenance gates only; the human is the domain
  judge, so machine domain failures defer with advisory reasons),
  ``canonical/domain`` (domain gates are canonical and the hook is
  mandatory; structural failures still reject).
- ValidationResult distinguishes an evaluated pass from an evaluated fail
  (structured reasons) and records an unevaluated dimension explicitly;
  AcceptanceResult carries the disposition plus every per-dimension result
  so the orchestrator's proceed/stop decision is mechanical.
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType

from ..domain import RuntimeContractError

from .candidate import CandidateOutput

_SCHEMA_TYPE_TOKENS = ("string", "number", "boolean", "array", "object")
"""The JSON type tokens SchemaSpec field_types may declare."""

_MISSING = object()
"""Sentinel distinguishing an absent constant field from a None constant."""


def _require_text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeContractError(f"{name} must be a non-empty string.")


def _require_field_tuple(value: object, name: str) -> None:
    if not isinstance(value, tuple):
        raise RuntimeContractError(f"{name} must be a tuple of non-empty strings.")
    seen: set[str] = set()
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise RuntimeContractError(f"{name} entries must be non-empty strings.")
        if entry in seen:
            raise RuntimeContractError(f"{name} must not contain duplicates.")
        seen.add(entry)


def _require_reason_tuple(value: object, name: str) -> None:
    if not isinstance(value, tuple):
        raise RuntimeContractError(f"{name} must be a tuple of non-empty strings.")
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise RuntimeContractError(f"{name} entries must be non-empty strings.")


def _matches_token(value: object, token: str) -> bool:
    if token == "string":
        return isinstance(value, str) and bool(value.strip())
    if token == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if token == "boolean":
        return isinstance(value, bool)
    if token == "array":
        return isinstance(value, (list, tuple))
    if token == "object":
        return isinstance(value, Mapping)
    return False


@dataclass(frozen=True)
class SchemaSpec:
    """The v1 schema seam: a minimal declarative content check.

    ``identity``/``version`` name the schema; ``required_fields`` names the
    fields content must carry; ``field_types`` maps a required field to one
    JSON type token (string/number/boolean/array/object); ``constant_fields``
    pins a required field to an exact scalar value. The seam deliberately
    stops here — v1 has no schema framework, and richer semantics are the
    domain hook's job.
    """

    identity: str
    version: str
    required_fields: tuple[str, ...] = ()
    field_types: Mapping[str, str] = field(default_factory=dict)
    constant_fields: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.identity, "identity")
        _require_text(self.version, "version")
        _require_field_tuple(self.required_fields, "required_fields")
        if not isinstance(self.field_types, Mapping):
            raise RuntimeContractError(
                "field_types must be a mapping of required field -> type token."
            )
        frozen_types: dict[str, str] = {}
        for field_name, token in self.field_types.items():
            _require_text(field_name, "field_types key")
            if field_name not in self.required_fields:
                raise RuntimeContractError(
                    f"field_types declares {field_name!r}, which is not a "
                    "required field."
                )
            if token not in _SCHEMA_TYPE_TOKENS:
                raise RuntimeContractError(
                    f"unknown schema type token {token!r} for field "
                    f"{field_name!r}; expected one of {_SCHEMA_TYPE_TOKENS}."
                )
            frozen_types[field_name] = token
        if not isinstance(self.constant_fields, Mapping):
            raise RuntimeContractError(
                "constant_fields must be a mapping of required field -> scalar."
            )
        frozen_constants: dict[str, object] = {}
        for field_name, constant in self.constant_fields.items():
            _require_text(field_name, "constant_fields key")
            if field_name not in self.required_fields:
                raise RuntimeContractError(
                    f"constant_fields declares {field_name!r}, which is not "
                    "a required field."
                )
            if not _is_json_scalar(constant):
                raise RuntimeContractError(
                    f"constant for field {field_name!r} must be a JSON "
                    "scalar, not a nested structure."
                )
            frozen_constants[field_name] = constant
        object.__setattr__(self, "field_types", MappingProxyType(frozen_types))
        object.__setattr__(
            self, "constant_fields", MappingProxyType(frozen_constants)
        )

    def check(self, content: object) -> tuple[bool, tuple[str, ...]]:
        """Check *content* against this schema; returns (passed, reasons)."""
        if not isinstance(content, Mapping):
            return (False, ("schema content must be a JSON object.",))
        reasons: list[str] = []
        for field_name in self.required_fields:
            if field_name not in content:
                reasons.append(f"missing required schema field {field_name!r}.")
                continue
            value = content[field_name]
            token = self.field_types.get(field_name)
            if token is not None and not _matches_token(value, token):
                reasons.append(
                    f"schema field {field_name!r} must be a JSON {token}."
                )
                continue
            declared = self.constant_fields.get(field_name, _MISSING)
            if declared is not _MISSING and value != declared:
                reasons.append(
                    f"schema field {field_name!r} must equal its declared "
                    f"constant {declared!r}."
                )
        return (not reasons, tuple(reasons))


def _is_json_scalar(value: object) -> bool:
    return value is None or isinstance(value, (str, bool, int, float))


class ValidationDimension(str, Enum):
    """The three evaluation dimensions of the acceptance pipeline."""

    SCHEMA = "schema"
    PROVENANCE = "provenance"
    DOMAIN = "domain"


_VALIDATION_DIMENSIONS = (
    ValidationDimension.SCHEMA,
    ValidationDimension.PROVENANCE,
    ValidationDimension.DOMAIN,
)


class AcceptancePolicy(str, Enum):
    """Explicit acceptance policies (brief Step 4)."""

    AUTOMATIC = "automatic"
    HUMAN = "human"
    CANONICAL_DOMAIN = "canonical/domain"


class AcceptanceDisposition(str, Enum):
    """The disposition an acceptance decision records."""

    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    DEFERRED_TO_HUMAN = "DEFERRED_TO_HUMAN"


@dataclass(frozen=True)
class ValidationResult:
    """One dimension's verdict.

    An evaluated validation either passes (``passed=True``, no reasons) or
    fails (``passed=False`` with structured reasons). An unevaluated
    dimension is a distinct, explicit marker — ``evaluated=False`` with no
    pass and no reasons — so a record can never claim a validation ran
    when it did not.
    """

    dimension: ValidationDimension
    passed: bool
    reasons: tuple[str, ...] = ()
    evaluated: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.dimension, ValidationDimension):
            raise RuntimeContractError("dimension must be a ValidationDimension.")
        if not isinstance(self.passed, bool):
            raise RuntimeContractError("passed must be a bool.")
        _require_reason_tuple(self.reasons, "reasons")
        if not isinstance(self.evaluated, bool):
            raise RuntimeContractError("evaluated must be a bool.")
        if not self.evaluated:
            # A not-evaluated result claims no verdict: it can neither pass
            # nor carry failure reasons, so it can never be mistaken for an
            # evaluated pass or an evaluated failure.
            if self.passed or self.reasons:
                raise RuntimeContractError(
                    f"a not-evaluated {self.dimension.value} result cannot "
                    "claim a pass or carry reasons."
                )
            return
        if self.passed and self.reasons:
            raise RuntimeContractError(
                f"a passing {self.dimension.value} validation cannot carry "
                "reasons."
            )
        if not self.passed and not self.reasons:
            raise RuntimeContractError(
                f"a failing {self.dimension.value} validation must carry "
                "reasons."
            )


@dataclass(frozen=True)
class AcceptanceResult:
    """The full disposition record: policy, disposition, every dimension
    result and the reasons behind the decision."""

    disposition: AcceptanceDisposition
    policy: AcceptancePolicy
    validation: Mapping[ValidationDimension, ValidationResult]
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.disposition, AcceptanceDisposition):
            raise RuntimeContractError(
                "disposition must be an AcceptanceDisposition."
            )
        if not isinstance(self.policy, AcceptancePolicy):
            raise RuntimeContractError("policy must be an AcceptancePolicy.")
        if (
            self.disposition is AcceptanceDisposition.DEFERRED_TO_HUMAN
            and self.policy is not AcceptancePolicy.HUMAN
        ):
            raise RuntimeContractError(
                "DEFERRED_TO_HUMAN is produced only under the human policy."
            )
        if not isinstance(self.validation, Mapping):
            raise RuntimeContractError(
                "validation must map each dimension to its ValidationResult."
            )
        frozen: dict[ValidationDimension, ValidationResult] = {}
        for dimension, result in self.validation.items():
            if not isinstance(result, ValidationResult):
                raise RuntimeContractError(
                    "validation values must be ValidationResult records."
                )
            if result.dimension is not dimension:
                raise RuntimeContractError(
                    f"validation key {dimension!r} holds a "
                    f"{result.dimension.value!r} result."
                )
            frozen[dimension] = result
        if set(frozen) != set(_VALIDATION_DIMENSIONS):
            raise RuntimeContractError(
                "validation must evaluate every dimension (schema, "
                "provenance, domain)."
            )
        object.__setattr__(self, "validation", MappingProxyType(frozen))
        _require_reason_tuple(self.reasons, "reasons")


DomainCheck = Callable[[object], tuple[bool, tuple[str, ...]]]


@dataclass(frozen=True)
class AcceptancePipeline:
    """Pure candidate evaluation: declared schema, provenance requirement
    and the optional domain hook. Never touches a store or Attempt state."""

    schema: SchemaSpec
    provenance_required: bool = True
    domain_check: DomainCheck | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.schema, SchemaSpec):
            raise RuntimeContractError("schema must be a SchemaSpec.")
        if not isinstance(self.provenance_required, bool):
            raise RuntimeContractError("provenance_required must be a bool.")
        if self.domain_check is not None and not callable(self.domain_check):
            raise RuntimeContractError("domain_check must be callable or None.")

    # -- dimension validation ----------------------------------------------

    def validate_schema(self, candidate: CandidateOutput) -> ValidationResult:
        """Check the candidate's declared schema identity/version and the
        conformance of its content against the pipeline's SchemaSpec."""
        if not isinstance(candidate, CandidateOutput):
            raise RuntimeContractError("candidate must be a CandidateOutput.")
        if (
            candidate.schema_identity != self.schema.identity
            or candidate.schema_version != self.schema.version
        ):
            return ValidationResult(
                dimension=ValidationDimension.SCHEMA,
                passed=False,
                reasons=(
                    f"candidate declares schema {candidate.schema_identity!r} "
                    f"version {candidate.schema_version!r}, but the pipeline "
                    f"schema is {self.schema.identity!r} version "
                    f"{self.schema.version!r}.",
                ),
            )
        passed, reasons = self.schema.check(candidate.content)
        return ValidationResult(
            dimension=ValidationDimension.SCHEMA,
            passed=passed,
            reasons=reasons,
        )

    def validate_provenance(self, candidate: CandidateOutput) -> ValidationResult:
        """Require provenance facts when the pipeline declares them
        required. Provenance is well-formedness here: real lineage
        coherence is event-derived at the store/binding layer, so the
        dimension gates on requiredness + fact presence only."""
        if not isinstance(candidate, CandidateOutput):
            raise RuntimeContractError("candidate must be a CandidateOutput.")
        if self.provenance_required and not candidate.provenance:
            return ValidationResult(
                dimension=ValidationDimension.PROVENANCE,
                passed=False,
                reasons=(
                    "the pipeline requires provenance facts but the "
                    "candidate carries none.",
                ),
            )
        return ValidationResult(
            dimension=ValidationDimension.PROVENANCE, passed=True
        )

    def validate_domain(self, candidate: CandidateOutput) -> ValidationResult:
        """Run the declared domain hook over the candidate content.

        Without a declared hook the dimension is recorded as explicitly
        not evaluated — ``evaluated=False``, never a pass — so the result
        cannot overstate what was validated (automatic acceptance then
        gates on schema and provenance only; canonical/domain acceptance
        refuses to run, see ``accept``).
        """
        if not isinstance(candidate, CandidateOutput):
            raise RuntimeContractError("candidate must be a CandidateOutput.")
        if self.domain_check is None:
            return ValidationResult(
                dimension=ValidationDimension.DOMAIN,
                passed=False,
                evaluated=False,
            )
        outcome = self.domain_check(candidate.content)
        if (
            not isinstance(outcome, tuple)
            or len(outcome) != 2
            or not isinstance(outcome[0], bool)
            or not isinstance(outcome[1], tuple)
        ):
            raise RuntimeContractError(
                "domain_check must return a (passed: bool, reasons: "
                f"tuple[str, ...]) pair; got {outcome!r}."
            )
        passed, reasons = outcome
        if passed and reasons:
            raise RuntimeContractError(
                "a passing domain check cannot carry reasons."
            )
        if not passed and not reasons:
            raise RuntimeContractError(
                "a failing domain check must carry reasons."
            )
        _require_reason_tuple(reasons, "domain_check reasons")
        return ValidationResult(
            dimension=ValidationDimension.DOMAIN,
            passed=passed,
            reasons=reasons,
        )

    # -- policy application -------------------------------------------------

    def accept(
        self, candidate: CandidateOutput, policy: AcceptancePolicy
    ) -> AcceptanceResult:
        """Evaluate *candidate* under the explicit *policy*.

        automatic: every evaluated gate must pass — schema and provenance
        always gate; the domain hook gates when one is declared, and an
        unevaluated domain is acceptable by policy (recorded as not
        evaluated, never as a domain pass).
        human: mechanical schema/provenance failures reject; everything
        else defers to a human reviewer, with machine domain failures
        riding along as advisory reasons.
        canonical/domain: schema, provenance and the mandatory domain hook
        all gate; a missing hook is a contract error, never a silent pass.
        """
        if not isinstance(policy, AcceptancePolicy):
            raise RuntimeContractError(
                f"policy must be an AcceptancePolicy, got {policy!r}."
            )
        if not isinstance(candidate, CandidateOutput):
            raise RuntimeContractError("candidate must be a CandidateOutput.")
        if (
            policy is AcceptancePolicy.CANONICAL_DOMAIN
            and self.domain_check is None
        ):
            raise RuntimeContractError(
                "canonical/domain acceptance requires a declared domain "
                "check; a vacuous domain verdict cannot be canonical."
            )
        results: dict[ValidationDimension, ValidationResult] = {
            ValidationDimension.SCHEMA: self.validate_schema(candidate),
            ValidationDimension.PROVENANCE: self.validate_provenance(candidate),
            ValidationDimension.DOMAIN: self.validate_domain(candidate),
        }
        if policy is AcceptancePolicy.HUMAN:
            mechanical_failed = (
                not results[ValidationDimension.SCHEMA].passed
                or not results[ValidationDimension.PROVENANCE].passed
            )
            if mechanical_failed:
                return self._rejected(policy, results)
            reasons = ["human review required for the candidate."]
            domain = results[ValidationDimension.DOMAIN]
            if domain.evaluated and not domain.passed:
                reasons.extend(
                    self._reasons(results, only_dimensions=(
                        ValidationDimension.DOMAIN,
                    ))
                )
            return AcceptanceResult(
                disposition=AcceptanceDisposition.DEFERRED_TO_HUMAN,
                policy=policy,
                validation=results,
                reasons=tuple(reasons),
            )
        # automatic and canonical/domain accept only when every evaluated
        # dimension passes. canonical/domain refuses a missing hook above,
        # so its domain dimension is always evaluated; under automatic a
        # hook-less pipeline accepts on schema and provenance, keeping the
        # domain recorded as not evaluated rather than as a domain pass.
        for dimension in _VALIDATION_DIMENSIONS:
            result = results[dimension]
            if result.evaluated and not result.passed:
                return self._rejected(policy, results)
        return AcceptanceResult(
            disposition=AcceptanceDisposition.ACCEPTED,
            policy=policy,
            validation=results,
        )

    @staticmethod
    def _rejected(
        policy: AcceptancePolicy, results: Mapping[ValidationDimension, ValidationResult]
    ) -> AcceptanceResult:
        return AcceptanceResult(
            disposition=AcceptanceDisposition.REJECTED,
            policy=policy,
            validation=results,
            reasons=AcceptancePipeline._reasons(results),
        )

    @staticmethod
    def _reasons(
        results: Mapping[ValidationDimension, ValidationResult],
        *,
        only_dimensions: tuple[ValidationDimension, ...] = _VALIDATION_DIMENSIONS,
    ) -> tuple[str, ...]:
        """Flatten the evaluated failures' reasons, each prefixed with its
        dimension token so the disposition's reasons name the failing
        dimension. Not-evaluated dimensions never appear: they carry no
        reasons and cannot be a cause of rejection."""
        return tuple(
            f"{dimension.value}: {reason}"
            for dimension in only_dimensions
            if results[dimension].evaluated and not results[dimension].passed
            for reason in results[dimension].reasons
        )
