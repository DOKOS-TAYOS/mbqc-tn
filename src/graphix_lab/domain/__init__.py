"""Domain models for the template package."""

from .errors import (
    GraphixCompatibilityError,
    GraphixLabError,
    GraphixUnavailableError,
    OptionalDependencyError,
    UnsupportedBackendError,
    UnsupportedGateError,
)

__all__ = [
    "GraphixCompatibilityError",
    "GraphixLabError",
    "GraphixUnavailableError",
    "OptionalDependencyError",
    "UnsupportedBackendError",
    "UnsupportedGateError",
]
