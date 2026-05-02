from __future__ import annotations

from dataclasses import FrozenInstanceError, is_dataclass

import pytest

from graphix_lab import (
    BackendComparisonReport,
    BackendRunReport,
    CommandRecord,
    GraphixCapabilities,
    LabCircuit,
    LabPattern,
    PatternSummary,
    ResourceSummary,
    RunTrace,
    SimulationReport,
    TraceFrame,
    circuit,
    from_graphix_pattern,
    from_qiskit,
    graphix_info,
)
from graphix_lab import __all__ as public_names


def test_public_api_exports_graphix_lab_models_and_entrypoints() -> None:
    assert GraphixCapabilities.__name__ in public_names
    assert set(public_names) == {
        "BackendComparisonReport",
        "BackendRunReport",
        "CommandRecord",
        "GraphixCapabilities",
        "LabCircuit",
        "LabPattern",
        "PatternSummary",
        "ResourceSummary",
        "RunTrace",
        "SimulationReport",
        "TraceFrame",
        "circuit",
        "from_graphix_pattern",
        "from_qiskit",
        "graphix_info",
    }
    assert "TemplateMetadata" not in public_names
    assert "get_template_metadata" not in public_names
    assert callable(graphix_info)


def test_public_api_domain_models_are_frozen_dataclasses() -> None:
    command = CommandRecord(
        index=0,
        kind="N",
        node=1,
        nodes=(1,),
        angle=None,
        plane=None,
        s_domain=(),
        t_domain=(),
        domain=(),
        raw="N(1)",
    )
    summary = PatternSummary(
        command_count=3,
        node_count=2,
        input_nodes=(0,),
        output_nodes=(1,),
        measurement_count=1,
        command_kinds=("N", "E", "M"),
    )
    resources = ResourceSummary(
        command_count=3,
        command_counts=(("N", 1), ("E", 1), ("M", 1)),
        node_count=2,
        edge_count=1,
        measurement_count=1,
        x_correction_count=0,
        z_correction_count=0,
        input_nodes=(0,),
        output_nodes=(1,),
    )
    frame = TraceFrame(
        step=0,
        command_kind="N",
        label="Prepare node 1",
        node=1,
        nodes=(1,),
        measured_nodes=frozenset(),
        active_nodes=frozenset({1}),
        pending_nodes=frozenset({1}),
        corrections=(),
        description="Preparation step",
    )
    trace = RunTrace(frames=(frame,))
    report = SimulationReport(
        backend="statevector",
        elapsed_time_seconds=0.125,
        result=None,
        result_type="NoneType",
        seed=123,
        notes=("seed accepted",),
        trace=trace,
    )
    backend_run = BackendRunReport(
        backend="statevector",
        success=True,
        elapsed_time_seconds=0.125,
        result_type="Statevector",
        error_message=None,
        notes=("available",),
    )
    comparison = BackendComparisonReport(runs=(backend_run,))

    for value in (
        command,
        summary,
        resources,
        frame,
        trace,
        report,
        backend_run,
        comparison,
    ):
        assert is_dataclass(value)

    with pytest.raises(FrozenInstanceError):
        command.kind = "E"  # type: ignore[misc]

    assert "PatternSummary" in str(summary)
    assert comparison.runs == (backend_run,)


def test_public_api_exposes_public_wrapper_types() -> None:
    lab_circuit = circuit(2)
    pattern = object()
    lab_pattern = from_graphix_pattern(pattern)

    assert isinstance(lab_circuit, LabCircuit)
    assert lab_circuit.width == 2
    assert isinstance(lab_pattern, LabPattern)
    assert lab_pattern.to_graphix() is pattern


def test_from_qiskit_stub_raises_clear_not_implemented_error() -> None:
    with pytest.raises(NotImplementedError, match="from_qiskit"):
        from_qiskit(object())
