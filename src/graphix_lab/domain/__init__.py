"""Domain models for the Graphix Lab public API."""

from .commands import CommandRecord
from .errors import (
    GraphixCompatibilityError,
    GraphixLabError,
    GraphixUnavailableError,
    OptionalDependencyError,
    UnsupportedBackendError,
    UnsupportedGateError,
)
from .simulation import BackendComparisonReport, BackendRunReport, SimulationReport
from .summaries import PatternSummary, ResourceSummary
from .traces import RunTrace, TraceAnimationHandle, TraceFrame

__all__ = [
    "BackendComparisonReport",
    "BackendRunReport",
    "CommandRecord",
    "GraphixCompatibilityError",
    "GraphixLabError",
    "GraphixUnavailableError",
    "OptionalDependencyError",
    "PatternSummary",
    "ResourceSummary",
    "RunTrace",
    "SimulationReport",
    "TraceAnimationHandle",
    "TraceFrame",
    "UnsupportedBackendError",
    "UnsupportedGateError",
]
