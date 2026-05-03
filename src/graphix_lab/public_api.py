from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .app.circuit_service import (
    _validate_positive_circuit_width,
    apply_cnot_gate,
    apply_rotation_gate,
    apply_single_qubit_gate,
    build_graphix_circuit,
    compile_graphix_circuit,
)
from .app.pattern_service import apply_graphix_pattern_method, copy_graphix_pattern
from .app.simulation_service import (
    compare_graphix_backends,
    run_graphix_pattern,
    trace_graphix_pattern,
)
from .app.summary_service import (
    build_pattern_explanation,
    build_pattern_summary,
    build_resource_summary,
)
from .app.visualization_service import animate_graphix_pattern_trace, draw_graphix_pattern
from .domain.commands import CommandRecord
from .domain.simulation import BackendComparisonReport, SimulationReport
from .domain.summaries import PatternSummary, ResourceSummary
from .domain.traces import RunTrace, TraceAnimationHandle
from .infrastructure.graphix_adapter import GraphixCircuitProtocol, extract_command_records
from .infrastructure.qiskit_adapter import convert_qiskit_circuit


def circuit(width: int) -> LabCircuit:
    return LabCircuit(width=width)


def from_graphix_pattern(pattern: object) -> LabPattern:
    return LabPattern(pattern=pattern)


def from_qiskit(qc: object, *, angle_units: str = "radians") -> LabCircuit:
    return convert_qiskit_circuit(qc, angle_units=angle_units)


@dataclass(frozen=True, slots=True)
class LabCircuit:
    width: int
    _graphix_circuit: GraphixCircuitProtocol | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "width", _validate_positive_circuit_width(self.width))

    def h(self, q: int) -> LabCircuit:
        return self._apply_single_qubit_gate("h", q)

    def x(self, q: int) -> LabCircuit:
        return self._apply_single_qubit_gate("x", q)

    def y(self, q: int) -> LabCircuit:
        return self._apply_single_qubit_gate("y", q)

    def z(self, q: int) -> LabCircuit:
        return self._apply_single_qubit_gate("z", q)

    def s(self, q: int) -> LabCircuit:
        return self._apply_single_qubit_gate("s", q)

    def rx(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        return self._apply_rotation_gate("rx", q, angle, units=units)

    def ry(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        return self._apply_rotation_gate("ry", q, angle, units=units)

    def rz(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        return self._apply_rotation_gate("rz", q, angle, units=units)

    def cnot(self, control: int, target: int) -> LabCircuit:
        apply_cnot_gate(self._ensure_graphix_circuit(), control, target)
        return self

    def _apply_single_qubit_gate(self, gate_name: str, q: int) -> LabCircuit:
        apply_single_qubit_gate(self._ensure_graphix_circuit(), gate_name, q)
        return self

    def _apply_rotation_gate(
        self,
        gate_name: str,
        q: int,
        angle: float,
        *,
        units: str = "pi",
    ) -> LabCircuit:
        apply_rotation_gate(self._ensure_graphix_circuit(), gate_name, q, angle, units=units)
        return self

    def compile(self) -> LabPattern:
        pattern = compile_graphix_circuit(self._ensure_graphix_circuit())
        return LabPattern(pattern=pattern)

    def to_graphix(self) -> object:
        return self._ensure_graphix_circuit()

    def _ensure_graphix_circuit(self) -> GraphixCircuitProtocol:
        if self._graphix_circuit is None:
            object.__setattr__(self, "_graphix_circuit", build_graphix_circuit(self.width))
        graphix_circuit = self._graphix_circuit
        if graphix_circuit is None:  # pragma: no cover - defensive safeguard
            raise RuntimeError("Graphix circuit initialization failed unexpectedly.")
        return graphix_circuit


@dataclass(frozen=True, slots=True)
class LabPattern:
    pattern: object

    def to_graphix(self) -> object:
        return self.pattern

    def copy(self) -> LabPattern:
        copied_pattern = copy_graphix_pattern(self.pattern)
        return LabPattern(pattern=copied_pattern)

    def standardize(self) -> LabPattern:
        return self._apply_graphix_pattern_method("standardize")

    def shift_signals(self) -> LabPattern:
        return self._apply_graphix_pattern_method("shift_signals")

    def perform_pauli_measurements(self) -> LabPattern:
        return self._apply_graphix_pattern_method("perform_pauli_measurements")

    def commands(self) -> tuple[CommandRecord, ...]:
        return extract_command_records(self.pattern)

    def summary(self) -> PatternSummary:
        commands, resources = self._commands_and_resources()
        return build_pattern_summary(commands, resources=resources)

    def explain(self) -> str:
        commands, resources = self._commands_and_resources()
        summary = build_pattern_summary(commands, resources=resources)
        return build_pattern_explanation(summary, resources=resources)

    def resources(self) -> ResourceSummary:
        _, resources = self._commands_and_resources()
        return resources

    def run(
        self,
        backend: str = "statevector",
        *,
        seed: int | None = None,
        trace: bool = False,
    ) -> SimulationReport:
        return run_graphix_pattern(
            self.pattern,
            backend=backend,
            seed=seed,
            trace=trace,
        )

    def trace(self) -> RunTrace:
        return trace_graphix_pattern(self.pattern)

    def draw(
        self,
        *,
        show_flow: bool = True,
        show_corrections: bool = True,
        layout: str = "auto",
        ax: Axes | None = None,
        delegate_to_graphix: bool = False,
    ) -> Figure:
        commands = self.commands()
        return draw_graphix_pattern(
            self.pattern,
            commands,
            show_flow=show_flow,
            show_corrections=show_corrections,
            layout=layout,
            ax=ax,
            delegate_to_graphix=delegate_to_graphix,
        )

    def animate(
        self,
        *,
        show_flow: bool = True,
        show_corrections: bool = True,
        layout: str = "auto",
    ) -> TraceAnimationHandle:
        commands = self.commands()
        return animate_graphix_pattern_trace(
            self.pattern,
            commands,
            show_flow=show_flow,
            show_corrections=show_corrections,
            layout=layout,
        )

    def compare_backends(
        self,
        backends: str | Sequence[str] | None = None,
        *,
        seed: int | None = None,
    ) -> BackendComparisonReport:
        return compare_graphix_backends(
            self.pattern,
            backends=backends,
            seed=seed,
        )

    def _apply_graphix_pattern_method(self, method_name: str) -> LabPattern:
        updated_pattern = apply_graphix_pattern_method(self.pattern, method_name)
        object.__setattr__(self, "pattern", updated_pattern)
        return self

    def _commands_and_resources(self) -> tuple[tuple[CommandRecord, ...], ResourceSummary]:
        commands = self.commands()
        return commands, build_resource_summary(commands)
