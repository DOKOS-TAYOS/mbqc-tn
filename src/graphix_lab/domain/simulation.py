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

    def __str__(self) -> str:
        if not self.runs:
            return "Backend comparison: no backends were selected."

        rows = [
            ("backend", "status", "elapsed_s", "result_type", "notes", "error"),
        ]
        for run in self.runs:
            rows.append(
                (
                    run.backend,
                    "success" if run.success else "failed",
                    f"{run.elapsed_time_seconds:.6f}",
                    run.result_type or "-",
                    "; ".join(run.notes) if run.notes else "-",
                    run.error_message or "-",
                )
            )

        column_widths = [max(len(row[index]) for row in rows) for index in range(len(rows[0]))]
        formatted_rows = [
            "  ".join(value.ljust(column_widths[index]) for index, value in enumerate(row))
            for row in rows
        ]
        return "\n".join(("Backend comparison", *formatted_rows))
