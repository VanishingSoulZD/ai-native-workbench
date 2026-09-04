"""Exception types for the canonical knowledge domain."""


class CanonicalError(Exception):
    """Base exception for canonical knowledge operations."""


class CanonicalValidationError(CanonicalError):
    """Raised when canonical data violates an intrinsic contract."""


class RegistryError(CanonicalError):
    """Base exception for canonical registry operations."""


class ResolutionError(RegistryError):
    """Raised when a canonical reference cannot be resolved."""


class IntegrityError(CanonicalError):
    """Raised when canonical state violates integrity rules."""


class SnapshotError(CanonicalError):
    """Raised when snapshot operations fail."""
