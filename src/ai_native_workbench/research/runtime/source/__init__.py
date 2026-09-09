"""Public surface of the Source Acquisition capability (Task 5).

Boundary rule (mirroring the runtime store package): the service and its
records live in :mod:`ai_native_workbench.research.runtime.source.acquisition`
and are re-exported here so later tasks (orchestration, the synthetic case
runner) import one thin package surface.
"""

from .acquisition import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    AcquisitionError,
    AcquisitionResult,
    FetchError,
    FetchResult,
    Fetcher,
    HttpFetcher,
    SourceAcquisitionService,
    SourceDeclaration,
    SourceDeclarationError,
    SourceState,
    SourceStatus,
    parse_source_declarations,
)

__all__ = [
    "DEFAULT_MAX_BYTES",
    "DEFAULT_TIMEOUT_SECONDS",
    "AcquisitionError",
    "AcquisitionResult",
    "FetchError",
    "FetchResult",
    "Fetcher",
    "HttpFetcher",
    "SourceAcquisitionService",
    "SourceDeclaration",
    "SourceDeclarationError",
    "SourceState",
    "SourceStatus",
    "parse_source_declarations",
]
