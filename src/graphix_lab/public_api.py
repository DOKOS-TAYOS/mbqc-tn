from __future__ import annotations

from dataclasses import dataclass, field

from .app.circuit_service import (
    apply_cnot_gate,
    apply_rotation_gate,
    apply_single_qubit_gate,
    build_graphix_circuit,
    compile_graphix_circuit,
)
from .app.pattern_service import apply_graphix_pattern_method, copy_graphix_pattern
from .domain.commands import CommandRecord
from .domain.simulation import BackendComparisonReport, SimulationReport
from .domain.summaries import PatternSummary, ResourceSummary
from .domain.traces import RunTrace
from .infrastructure.graphix_adapter import GraphixCircuitProtocol, extract_command_records

_PROMPT_NOT_READY_MESSAGE = (
    "{name} is part of the public Graphix Lab API surface, but its Graphix-backed "
    "behavior is not implemented yet in this checkout."
)


def circuit(width: int) -> LabCircuit:
    return LabCircuit(width=width)


def from_graphix_pattern(pattern: object) -> LabPattern:
    return LabPattern(pattern=pattern)


def from_qiskit(qc: object, *, angle_units: str = "radians") -> LabCircuit:
    del qc, angle_units
    raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="from_qiskit"))


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
        if self.width <= 0:
            raise ValueError("width must be a positive integer.")

    def h(self, q: int) -> LabCircuit:
        apply_single_qubit_gate(self._ensure_graphix_circuit(), "h", q)
        return self

    def x(self, q: int) -> LabCircuit:
        apply_single_qubit_gate(self._ensure_graphix_circuit(), "x", q)
        return self

    def y(self, q: int) -> LabCircuit:
        apply_single_qubit_gate(self._ensure_graphix_circuit(), "y", q)
        return self

    def z(self, q: int) -> LabCircuit:
        apply_single_qubit_gate(self._ensure_graphix_circuit(), "z", q)
        return self

    def s(self, q: int) -> LabCircuit:
        apply_single_qubit_gate(self._ensure_graphix_circuit(), "s", q)
        return self

    def rx(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        apply_rotation_gate(self._ensure_graphix_circuit(), "rx", q, angle, units=units)
        return self

    def ry(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        apply_rotation_gate(self._ensure_graphix_circuit(), "ry", q, angle, units=units)
        return self

    def rz(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        apply_rotation_gate(self._ensure_graphix_circuit(), "rz", q, angle, units=units)
        return self

    def cnot(self, control: int, target: int) -> LabCircuit:
        apply_cnot_gate(self._ensure_graphix_circuit(), control, target)
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
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.summary"))

    def explain(self) -> str:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.explain"))

    def resources(self) -> ResourceSummary:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.resources"))

    def run(
        self,
        backend: str = "statevector",
        *,
        seed: int | None = None,
        trace: bool = False,
    ) -> SimulationReport:
        del backend, seed, trace
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.run"))

    def trace(self) -> RunTrace:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.trace"))

    def draw(self) -> object:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.draw"))

    def animate(self) -> object:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.animate"))

    def compare_backends(self) -> BackendComparisonReport:
        raise NotImplementedError(
            _PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.compare_backends")
        )

    def _apply_graphix_pattern_method(self, method_name: str) -> LabPattern:
        updated_pattern = apply_graphix_pattern_method(self.pattern, method_name)
        object.__setattr__(self, "pattern", updated_pattern)
        return self
