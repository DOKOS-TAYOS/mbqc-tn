from __future__ import annotations

import matplotlib
import pytest

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from graphix_lab import (
    BackendComparisonReport,
    CommandRecord,
    GraphixCapabilities,
    LabPattern,
    SimulationReport,
    TraceAnimationHandle,
    circuit,
    graphix_info,
)


def test_graphix_info_reports_real_runtime_capabilities() -> None:
    capabilities = graphix_info()

    assert isinstance(capabilities, GraphixCapabilities)
    assert capabilities.version.startswith("0.3.")
    assert capabilities.has_circuit is True
    assert capabilities.has_pattern_standardize is True
    assert capabilities.has_pattern_shift_signals is True
    assert capabilities.has_pattern_perform_pauli_measurements is True


def test_real_graphix_compile_and_command_introspection_work_together() -> None:
    lab_pattern = circuit(2).h(0).cnot(0, 1).compile()
    graphix_pattern = lab_pattern.to_graphix()
    commands = lab_pattern.commands()

    assert isinstance(lab_pattern, LabPattern)
    assert type(graphix_pattern).__module__.startswith("graphix")
    assert isinstance(commands, tuple)
    assert commands
    assert all(isinstance(command, CommandRecord) for command in commands)
    assert [command.index for command in commands] == list(range(len(commands)))
    assert all(command.raw for command in commands)
    assert all(command.kind != "UNKNOWN" for command in commands)
    assert {"N", "E", "M"}.issubset({command.kind for command in commands})


def test_real_graphix_shift_signals_preserves_command_introspection() -> None:
    lab_pattern = circuit(2).h(0).cnot(0, 1).compile().copy()

    shifted_pattern = lab_pattern.shift_signals()
    commands = shifted_pattern.commands()

    assert shifted_pattern is lab_pattern
    assert type(shifted_pattern.to_graphix()).__module__.startswith("graphix")
    assert commands
    assert {"N", "E", "M"}.issubset({command.kind for command in commands})


def test_real_graphix_run_returns_simulation_report_for_statevector() -> None:
    lab_pattern = circuit(1).h(0).compile()
    standalone_trace = lab_pattern.trace()

    report = lab_pattern.run(backend="statevector", seed=123, trace=True)

    assert isinstance(report, SimulationReport)
    assert report.backend == "statevector"
    assert report.seed == 123
    assert report.elapsed_time_seconds >= 0.0
    assert report.result is not None
    assert report.result_type == type(report.result).__name__
    assert type(report.result).__module__.startswith("graphix")
    assert report.trace is not None
    assert report.trace == standalone_trace
    assert len(report.trace.frames) == len(lab_pattern.commands())
    assert [frame.step for frame in report.trace.frames] == list(range(len(report.trace.frames)))
    assert any(frame.command_kind == "M" for frame in report.trace.frames)


def test_real_graphix_run_supports_optional_detected_backends() -> None:
    optional_backends = tuple(
        backend
        for backend in ("densitymatrix", "tensornetwork", "mps")
        if backend in graphix_info().supported_backends
    )
    if not optional_backends:
        pytest.skip("No optional Graphix simulation backends detected in this environment.")

    for backend in optional_backends:
        report = circuit(1).h(0).compile().run(backend=backend, seed=123)

        assert report.backend == backend
        assert report.elapsed_time_seconds >= 0.0
        assert report.result is not None
        assert report.result_type == type(report.result).__name__
        assert type(report.result).__module__.startswith("graphix")


def test_real_graphix_compare_backends_reports_a_supported_backend() -> None:
    supported_backends = graphix_info().supported_backends
    if not supported_backends:
        pytest.skip("No Graphix simulation backends detected in this environment.")

    report = (
        circuit(1)
        .h(0)
        .compile()
        .compare_backends(
            backends=supported_backends[:1],
            seed=123,
        )
    )

    assert isinstance(report, BackendComparisonReport)
    assert len(report.runs) == 1
    assert report.runs[0].backend == supported_backends[0]
    assert report.runs[0].success is True
    assert report.runs[0].elapsed_time_seconds >= 0.0
    assert report.runs[0].result_type is not None
    assert report.runs[0].error_message is None


def test_real_graphix_draw_returns_headless_matplotlib_figure() -> None:
    figure = circuit(2).h(0).cnot(0, 1).compile().draw(show_flow=False)

    assert isinstance(figure, Figure)
    assert len(figure.axes) == 1

    plt.close(figure)


def test_real_graphix_animate_returns_headless_slider_handle() -> None:
    handle = circuit(2).h(0).cnot(0, 1).compile().animate(show_flow=False)

    assert isinstance(handle, TraceAnimationHandle)
    assert isinstance(handle.figure, Figure)
    assert len(handle.trace.frames) > 0
    assert len(handle.figure.axes) == 2

    plt.close(handle.figure)
