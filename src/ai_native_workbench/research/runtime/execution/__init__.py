"""Public execution surface of the Research Runtime (Task 4).

Mode-based executor strategy dispatch (ExecutorRegistry + Executor
protocol + the DeterministicExecutor fake for the synthetic E2E fixture),
CandidateOutput, the pure schema/provenance/domain acceptance pipeline with
explicit policies, and the isolated DeepSeek adapter boundary. Records are
frozen and keyword-constructed; evaluation never touches a store, events or
Attempt state (recording dispositions is the Task 6 control layer's job).
"""

from .acceptance import (
    AcceptanceDisposition,
    AcceptancePipeline,
    AcceptancePolicy,
    AcceptanceResult,
    SchemaSpec,
    ValidationDimension,
    ValidationResult,
)
from .candidate import CandidateOutput
from .llm import (
    DEEPSEEK_API_KEY_ENV,
    DEEPSEEK_ENDPOINT,
    DEEPSEEK_MODEL,
    DEEPSEEK_PROVIDER,
    CompletionRequest,
    CompletionResult,
    DeepSeekAPIError,
    DeepSeekClient,
    DeepSeekConfigurationError,
    DeepSeekError,
    DeepSeekResponseError,
    DeepSeekTimeoutError,
    DeepSeekTransport,
    DeepSeekTransportError,
    UrllibTransport,
)
from .registry import (
    DETERMINISTIC_MODE,
    DETERMINISTIC_SCHEMA_VERSION,
    DeterministicExecutor,
    Executor,
    ExecutorRegistry,
    ExecutorResolutionError,
)

__all__ = [
    "AcceptanceDisposition",
    "AcceptancePipeline",
    "AcceptancePolicy",
    "AcceptanceResult",
    "CandidateOutput",
    "CompletionRequest",
    "CompletionResult",
    "DEEPSEEK_API_KEY_ENV",
    "DEEPSEEK_ENDPOINT",
    "DEEPSEEK_MODEL",
    "DEEPSEEK_PROVIDER",
    "DETERMINISTIC_MODE",
    "DETERMINISTIC_SCHEMA_VERSION",
    "DeepSeekAPIError",
    "DeepSeekClient",
    "DeepSeekConfigurationError",
    "DeepSeekError",
    "DeepSeekResponseError",
    "DeepSeekTimeoutError",
    "DeepSeekTransport",
    "DeepSeekTransportError",
    "DeterministicExecutor",
    "Executor",
    "ExecutorRegistry",
    "ExecutorResolutionError",
    "SchemaSpec",
    "UrllibTransport",
    "ValidationDimension",
    "ValidationResult",
]
