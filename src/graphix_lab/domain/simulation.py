from __future__ import annotations

from dataclasses import dataclass

from .traces import RunTrace


@dataclass(frozen=True, slots=True)
class SimulationReport:
    backend: str
    elapsed_time_seconds: float
    result: object | None
    result_type: str
    seed: int | None = None
    notes: tuple[str, ...] = ()
    trace: RunTrace | None = None


@dataclass(frozen=True, slots=True)
class BackendRunReport:
    backend: str
    success: bool
    elapsed_time_seconds: float
    result_type: str | None = None
    error_message: str | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BackendComparisonReport:
    runs: tuple[BackendRunReport, ...]
