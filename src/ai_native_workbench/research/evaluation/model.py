"""Immutable contracts for research evaluation."""
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType

from ..canonical import CanonicalRef
from .errors import EvaluationValidationError

class EvaluationTargetType(str, Enum): OBJECT="object"; SNAPSHOT="snapshot"; DELIVERY="delivery"
class EvaluationMode(str, Enum): MECHANICAL="mechanical"; HUMAN_ASSISTED="human_assisted"; HUMAN_REQUIRED="human_required"
class EvaluationResultStatus(str, Enum): PASS="pass"; FAIL="fail"; INCONCLUSIVE="inconclusive"; NOT_APPLICABLE="not_applicable"
class EvaluationRunStatus(str, Enum): CREATED="created"; RUNNING="running"; COMPLETED="completed"; FAILED="failed"
class GateOutcome(str, Enum): PASS="PASS"; REVIEW="REVIEW"; FAIL="FAIL"
class HumanReviewDecision(str, Enum): ACCEPTED="accepted"; REJECTED="rejected"; NEEDS_REVISION="needs_revision"

def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip(): raise EvaluationValidationError(f"{name} must be a non-empty string.")
def _enum(value: object, kind: type[Enum], name: str) -> None:
    if not isinstance(value, kind): raise EvaluationValidationError(f"{name} must be a {kind.__name__}.")
def _freeze(value: object) -> object:
    if isinstance(value, Mapping): return MappingProxyType({k: _freeze(v) for k,v in value.items()})
    if isinstance(value, (list, tuple)): return tuple(_freeze(v) for v in value)
    return value

@dataclass(frozen=True)
class EvaluationRule:
    rule_id: str; name: str; description: str; target_scope: EvaluationTargetType; mode: EvaluationMode; severity: str; version: str
    def __post_init__(self):
        for n in ("rule_id","name","description","version"): _text(getattr(self,n),n)
        _enum(self.target_scope, EvaluationTargetType, "target_scope"); _enum(self.mode, EvaluationMode, "mode")
        if self.severity not in {"informational","warning","critical"}: raise EvaluationValidationError("severity is invalid.")

@dataclass(frozen=True)
class EvaluationResult:
    result_id: str; run_id: str; rule_id: str; target_type: EvaluationTargetType; target_id: str; status: EvaluationResultStatus; finding: str; severity: str|None=None; subject_refs: tuple[CanonicalRef,...]=(); value: int|float|str|None=None; notes: str|None=None
    def __post_init__(self):
        for n in ("result_id","run_id","rule_id","target_id","finding"): _text(getattr(self,n),n)
        _enum(self.target_type, EvaluationTargetType, "target_type"); _enum(self.status, EvaluationResultStatus, "status")
        if self.severity is not None and self.severity not in {"informational","warning","critical"}: raise EvaluationValidationError("severity is invalid.")
        if not isinstance(self.subject_refs, tuple) or not all(isinstance(x, CanonicalRef) for x in self.subject_refs): raise EvaluationValidationError("subject_refs must be a tuple of CanonicalRef values.")
        if isinstance(self.value, bool) or (self.value is not None and not isinstance(self.value,(int,float,str))): raise EvaluationValidationError("value must be an int, float, str, or None.")
        if self.notes is not None and not isinstance(self.notes,str): raise EvaluationValidationError("notes must be a string or None.")

@dataclass(frozen=True)
class EvaluationRun:
    run_id: str; target_type: EvaluationTargetType; target_id: str; evaluation_rule_versions: tuple[str,...]; evaluation_protocol_version: str; configuration: Mapping[str,object]; created_at: str; status: EvaluationRunStatus; results: tuple[EvaluationResult,...]=()
    def __post_init__(self):
        for n in ("run_id","target_id","evaluation_protocol_version","created_at"): _text(getattr(self,n),n)
        _enum(self.target_type, EvaluationTargetType,"target_type"); _enum(self.status, EvaluationRunStatus,"status")
        if not isinstance(self.evaluation_rule_versions,tuple) or not self.evaluation_rule_versions: raise EvaluationValidationError("evaluation_rule_versions must be a non-empty tuple.")
        if len(set(self.evaluation_rule_versions)) != len(self.evaluation_rule_versions) or any(not isinstance(x,str) or x.count("@") != 1 or not all(p.strip() for p in x.split("@")) for x in self.evaluation_rule_versions): raise EvaluationValidationError("evaluation_rule_versions must contain unique rule_id@version keys.")
        if not isinstance(self.configuration,Mapping): raise EvaluationValidationError("configuration must be a mapping.")
        object.__setattr__(self,"configuration",_freeze(self.configuration))
        if not isinstance(self.results,tuple) or not all(isinstance(r,EvaluationResult) and r.run_id == self.run_id for r in self.results): raise EvaluationValidationError("results must match the run.")
        if len({r.result_id for r in self.results}) != len(self.results): raise EvaluationValidationError("result IDs must be unique.")

@dataclass(frozen=True)
class HumanReviewRecord:
    review_id: str; run_id: str; target_type: EvaluationTargetType; target_id: str; reviewer: str; decision: HumanReviewDecision; reviewed_at: str; comment: str
    def __post_init__(self):
        for n in ("review_id","run_id","target_id","reviewer","reviewed_at","comment"): _text(getattr(self,n),n)
        _enum(self.target_type,EvaluationTargetType,"target_type"); _enum(self.decision,HumanReviewDecision,"decision")
