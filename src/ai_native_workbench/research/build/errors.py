class BuildError(RuntimeError): pass
class BuildValidationError(BuildError): pass
class BuildPreconditionError(BuildError): pass
class BuildExecutionError(BuildError): pass
