from __future__ import annotations

import math
from dataclasses import dataclass
from types import ModuleType, SimpleNamespace
from typing import cast

import pytest

import graphix_lab.infrastructure.graphix_adapter as graphix_adapter_module
from graphix_lab import LabCircuit, LabPattern, circuit


@dataclass(slots=True)
class FakePattern:
    label: str = "compiled-pattern"


@dataclass(slots=True)
class FakeTranspileResult:
    pattern: object


class FakeGraphixCircuit:
    def __init__(self, width: int) -> None:
        self.width = width
        self.operations: list[tuple[str, tuple[object, ...]]] = []
        self.pattern = FakePattern()
        self.transpile_calls = 0

    def h(self, q: int) -> None:
        self.operations.append(("h", (q,)))

    def x(self, q: int) -> None:
        self.operations.append(("x", (q,)))

    def y(self, q: int) -> None:
        self.operations.append(("y", (q,)))

    def z(self, q: int) -> None:
        self.operations.append(("z", (q,)))

    def s(self, q: int) -> None:
        self.operations.append(("s", (q,)))

    def rx(self, q: int, angle: float) -> None:
        self.operations.append(("rx", (q, angle)))

    def ry(self, q: int, angle: float) -> None:
        self.operations.append(("ry", (q, angle)))

    def rz(self, q: int, angle: float) -> None:
        self.operations.append(("rz", (q, angle)))

    def cnot(self, control: int, target: int) -> None:
        self.operations.append(("cnot", (control, target)))

    def transpile(self) -> FakeTranspileResult:
        self.transpile_calls += 1
        return FakeTranspileResult(pattern=self.pattern)


def _install_fake_graphix(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_graphix = cast(
        ModuleType,
        SimpleNamespace(Circuit=FakeGraphixCircuit, Pattern=FakePattern),
    )

    def fake_import_module(module_name: str) -> ModuleType:
        if module_name == "graphix":
            return fake_graphix
        raise ModuleNotFoundError(name=module_name)

    monkeypatch.setattr(graphix_adapter_module, "import_module", fake_import_module)


def _unwrap_graphix_circuit(lab_circuit: LabCircuit) -> FakeGraphixCircuit:
    return cast(FakeGraphixCircuit, lab_circuit.to_graphix())


def test_circuit_returns_lab_circuit_wrapper_around_graphix_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_circuit = circuit(2)

    assert isinstance(lab_circuit, LabCircuit)
    assert lab_circuit.width == 2
    assert isinstance(lab_circuit.to_graphix(), FakeGraphixCircuit)
    assert _unwrap_graphix_circuit(lab_circuit).width == 2


def test_lab_circuit_gate_methods_chain_and_delegate_to_graphix_circuit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_circuit = circuit(3)

    chained_result = (
        lab_circuit.h(0)
        .x(1)
        .y(2)
        .z(0)
        .s(1)
        .rx(0, 0.5)
        .ry(1, math.pi / 4, units="radians")
        .rz(2, -0.25)
        .cnot(0, 2)
    )

    assert chained_result is lab_circuit
    assert _unwrap_graphix_circuit(lab_circuit).operations == [
        ("h", (0,)),
        ("x", (1,)),
        ("y", (2,)),
        ("z", (0,)),
        ("s", (1,)),
        ("rx", (0, 0.5)),
        ("ry", (1, 0.25)),
        ("rz", (2, -0.25)),
        ("cnot", (0, 2)),
    ]


def test_lab_circuit_compile_wraps_transpiled_graphix_pattern(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    lab_circuit = circuit(1).h(0)

    pattern = lab_circuit.compile()
    graphix_circuit = _unwrap_graphix_circuit(lab_circuit)

    assert isinstance(pattern, LabPattern)
    assert pattern.to_graphix() is graphix_circuit.pattern
    assert graphix_circuit.transpile_calls == 1


def test_lab_circuit_rejects_unsupported_angle_units(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    lab_circuit = circuit(1)

    with pytest.raises(ValueError, match="Unsupported angle units"):
        lab_circuit.rx(0, 90.0, units="degrees")

    assert _unwrap_graphix_circuit(lab_circuit).operations == []
