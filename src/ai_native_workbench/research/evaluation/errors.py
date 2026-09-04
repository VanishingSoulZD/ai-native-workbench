"""Exception types for the evaluation layer."""
class EvaluationError(RuntimeError): pass
class EvaluationValidationError(EvaluationError): pass
class EvaluationExecutionError(EvaluationError): pass
class EvaluationResolutionError(EvaluationError): pass
