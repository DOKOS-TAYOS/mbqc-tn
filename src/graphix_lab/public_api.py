from __future__ import annotations

from dataclasses import dataclass

from .domain.commands import CommandRecord
from .domain.simulation import BackendComparisonReport, SimulationReport
from .domain.summaries import PatternSummary, ResourceSummary
from .domain.traces import RunTrace

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

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("width must be a positive integer.")

    def h(self, q: int) -> LabCircuit:
        del q
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.h"))

    def x(self, q: int) -> LabCircuit:
        del q
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.x"))

    def y(self, q: int) -> LabCircuit:
        del q
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.y"))

    def z(self, q: int) -> LabCircuit:
        del q
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.z"))

    def s(self, q: int) -> LabCircuit:
        del q
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.s"))

    def rx(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        del q, angle, units
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.rx"))

    def ry(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        del q, angle, units
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.ry"))

    def rz(self, q: int, angle: float, *, units: str = "pi") -> LabCircuit:
        del q, angle, units
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.rz"))

    def cnot(self, control: int, target: int) -> LabCircuit:
        del control, target
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.cnot"))

    def compile(self) -> LabPattern:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.compile"))

    def to_graphix(self) -> object:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabCircuit.to_graphix"))


@dataclass(frozen=True, slots=True)
class LabPattern:
    pattern: object

    def to_graphix(self) -> object:
        return self.pattern

    def copy(self) -> LabPattern:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.copy"))

    def standardize(self) -> LabPattern:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.standardize"))

    def shift_signals(self) -> LabPattern:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.shift_signals"))

    def perform_pauli_measurements(self) -> LabPattern:
        raise NotImplementedError(
            _PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.perform_pauli_measurements")
        )

    def commands(self) -> tuple[CommandRecord, ...]:
        raise NotImplementedError(_PROMPT_NOT_READY_MESSAGE.format(name="LabPattern.commands"))

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
