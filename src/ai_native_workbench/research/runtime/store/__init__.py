"""Public surface of the durable runtime store (Task 2).

Boundary rule: tests and later tasks import the store through this package,
never through ``ai_native_workbench.research.runtime`` — the runtime package
surface is Task 1 domain contracts only.
"""

from .events import EventConflictError, EventLog, EventLogError
from .filesystem import (
    ArtifactNotFoundError,
    EvidenceIntegrityError,
    FileSystemRuntimeStore,
    RunAlreadyExistsError,
    RunNotFoundError,
    RuntimeStore,
)
from .projection import (
    ArtifactReference,
    BINDING_COMMITTED,
    BINDING_PENDING,
    CanonicalBindingView,
    HUMAN_REJECTION,
    ProjectionSchemaError,
    RunProjection,
    SnapshotBindingView,
    parse_projection,
    reduce_events,
    serialize_projection,
)

__all__ = [
    "ArtifactNotFoundError",
    "ArtifactReference",
    "BINDING_COMMITTED",
    "BINDING_PENDING",
    "CanonicalBindingView",
    "EventConflictError",
    "EventLog",
    "EventLogError",
    "EvidenceIntegrityError",
    "FileSystemRuntimeStore",
    "HUMAN_REJECTION",
    "ProjectionSchemaError",
    "RunAlreadyExistsError",
    "RunNotFoundError",
    "RunProjection",
    "RuntimeStore",
    "SnapshotBindingView",
    "parse_projection",
    "reduce_events",
    "serialize_projection",
]
