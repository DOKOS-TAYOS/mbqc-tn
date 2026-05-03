from __future__ import annotations

import math
from dataclasses import dataclass
from types import ModuleType, SimpleNamespace
from typing import ClassVar, cast

import pytest

import graphix_lab.infrastructure.graphix_runtime as graphix_runtime_module
import graphix_lab.infrastructure.qiskit_adapter as qiskit_adapter_module
from graphix_lab import LabCircuit, from_qiskit
from graphix_lab.domain.errors import UnsupportedGateError


@dataclass(slots=True)
class FakePattern:
    label: str = "compiled-pattern"


@dataclass(slots=True)
class FakeTranspileResult:
    pattern: object


class FakeGraphixCircuit:
    instances: ClassVar[list[FakeGraphixCircuit]] = []

    def __init__(self, width: int) -> None:
        self.width = width
        self.operations: list[tuple[str, tuple[object, ...]]] = []
        self.pattern = FakePattern()
        self.transpile_calls = 0
        type(self).instances.append(self)

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
    FakeGraphixCircuit.instances.clear()
    fake_graphix = cast(
        ModuleType,
        SimpleNamespace(Circuit=FakeGraphixCircuit, Pattern=FakePattern),
    )

    def fake_import_module(module_name: str) -> ModuleType:
        if module_name == "graphix":
            return fake_graphix
        raise ModuleNotFoundError(name=module_name)

    monkeypatch.setattr(graphix_runtime_module, "import_module", fake_import_module)


def _install_fake_qiskit(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_qiskit = cast(ModuleType, SimpleNamespace(__name__="qiskit"))

    def fake_import_module(module_name: str) -> ModuleType:
        if module_name == "qiskit":
            return fake_qiskit
        raise ModuleNotFoundError(name=module_name)

    monkeypatch.setattr(qiskit_adapter_module, "import_module", fake_import_module)


def _unwrap_graphix_circuit(lab_circuit: LabCircuit) -> FakeGraphixCircuit:
    return cast(FakeGraphixCircuit, lab_circuit.to_graphix())


def _assert_no_graphix_operations_recorded() -> None:
    assert all(not circuit.operations for circuit in FakeGraphixCircuit.instances)


@dataclass(frozen=True, slots=True)
class FakeQubit:
    label: str


@dataclass(frozen=True, slots=True)
class FakeOperation:
    name: str
    params: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class FakeCircuitInstruction:
    operation: FakeOperation
    qubits: tuple[FakeQubit, ...]
    clbits: tuple[object, ...] = ()

    @property
    def params(self) -> tuple[object, ...]:
        return self.operation.params


@dataclass(frozen=True, slots=True)
class FakeBitLocation:
    index: object


class FakeQuantumCircuit:
    def __init__(
        self,
        *,
        num_qubits: object,
        data: object,
        bit_index_by_qubit: dict[FakeQubit, object],
    ) -> None:
        self.num_qubits = num_qubits
        self.data = data
        self._bit_index_by_qubit = dict(bit_index_by_qubit)

    def find_bit(self, bit: object) -> FakeBitLocation:
        return FakeBitLocation(index=self._bit_index_by_qubit[cast(FakeQubit, bit)])


def test_convert_qiskit_circuit_maps_supported_gate_subset_to_lab_circuit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")
    q1 = FakeQubit("q1")
    q2 = FakeQubit("q2")
    qc = FakeQuantumCircuit(
        num_qubits=3,
        data=(
            FakeCircuitInstruction(FakeOperation("h"), (q0,)),
            FakeCircuitInstruction(FakeOperation("x"), (q1,)),
            FakeCircuitInstruction(FakeOperation("y"), (q2,)),
            FakeCircuitInstruction(FakeOperation("z"), (q0,)),
            FakeCircuitInstruction(FakeOperation("s"), (q1,)),
            FakeCircuitInstruction(FakeOperation("rx", (math.pi / 2,)), (q0,)),
            FakeCircuitInstruction(FakeOperation("ry", (math.pi / 4,)), (q1,)),
            FakeCircuitInstruction(FakeOperation("rz", (-math.pi / 2,)), (q2,)),
            FakeCircuitInstruction(FakeOperation("cx"), (q0, q2)),
        ),
        bit_index_by_qubit={q0: 0, q1: 1, q2: 2},
    )

    lab_circuit = qiskit_adapter_module.convert_qiskit_circuit(qc)

    assert isinstance(lab_circuit, LabCircuit)
    assert lab_circuit.width == 3
    assert _unwrap_graphix_circuit(lab_circuit).operations == [
        ("h", (0,)),
        ("x", (1,)),
        ("y", (2,)),
        ("z", (0,)),
        ("s", (1,)),
        ("rx", (0, 0.5)),
        ("ry", (1, 0.25)),
        ("rz", (2, -0.5)),
        ("cnot", (0, 2)),
    ]


def test_convert_qiskit_circuit_can_accept_graphix_pi_units_directly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")
    qc = FakeQuantumCircuit(
        num_qubits=1,
        data=(FakeCircuitInstruction(FakeOperation("rx", (0.75,)), (q0,)),),
        bit_index_by_qubit={q0: 0},
    )

    lab_circuit = qiskit_adapter_module.convert_qiskit_circuit(qc, angle_units="pi")

    assert _unwrap_graphix_circuit(lab_circuit).operations == [("rx", (0, 0.75))]


def test_convert_qiskit_circuit_uses_find_bit_for_qubit_indices(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    control = FakeQubit("control")
    target = FakeQubit("target")
    qc = FakeQuantumCircuit(
        num_qubits=2,
        data=(
            FakeCircuitInstruction(FakeOperation("h"), (control,)),
            FakeCircuitInstruction(FakeOperation("cx"), (control, target)),
        ),
        bit_index_by_qubit={control: 1, target: 0},
    )

    lab_circuit = qiskit_adapter_module.convert_qiskit_circuit(qc)

    assert _unwrap_graphix_circuit(lab_circuit).operations == [
        ("h", (1,)),
        ("cnot", (1, 0)),
    ]


def test_convert_qiskit_circuit_raises_unsupported_gate_error_with_gate_name_and_index(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")
    qc = FakeQuantumCircuit(
        num_qubits=1,
        data=(
            FakeCircuitInstruction(FakeOperation("h"), (q0,)),
            FakeCircuitInstruction(FakeOperation("measure"), (q0,)),
        ),
        bit_index_by_qubit={q0: 0},
    )

    with pytest.raises(UnsupportedGateError, match="measure"):
        qiskit_adapter_module.convert_qiskit_circuit(qc)

    try:
        qiskit_adapter_module.convert_qiskit_circuit(qc)
    except UnsupportedGateError as error:
        assert error.gate_name == "measure"
        assert error.gate_index == 1
    else:  # pragma: no cover - defensive guard for the explicit attribute assertions
        pytest.fail("Expected UnsupportedGateError for unsupported Qiskit instruction.")


def test_convert_qiskit_circuit_rejects_boolean_rotation_angles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")
    qc = FakeQuantumCircuit(
        num_qubits=1,
        data=(FakeCircuitInstruction(FakeOperation("rx", (True,)), (q0,)),),
        bit_index_by_qubit={q0: 0},
    )

    with pytest.raises(UnsupportedGateError, match="rotation angle"):
        qiskit_adapter_module.convert_qiskit_circuit(qc)


@pytest.mark.parametrize("num_qubits", [True, "2", 0, -1])
def test_convert_qiskit_circuit_rejects_invalid_num_qubits(
    monkeypatch: pytest.MonkeyPatch,
    num_qubits: object,
) -> None:
    _install_fake_qiskit(monkeypatch)
    qc = FakeQuantumCircuit(
        num_qubits=num_qubits,
        data=(),
        bit_index_by_qubit={},
    )

    with pytest.raises(ValueError, match="num_qubits must be a positive integer"):
        qiskit_adapter_module.convert_qiskit_circuit(qc)


@pytest.mark.parametrize(
    ("bit_index", "expected_exception", "message_fragment"),
    [
        (True, TypeError, "integer qubit index"),
        (-1, ValueError, "between 0 and 1"),
        (2, ValueError, "between 0 and 1"),
    ],
)
def test_convert_qiskit_circuit_rejects_invalid_find_bit_indices(
    monkeypatch: pytest.MonkeyPatch,
    bit_index: object,
    expected_exception: type[Exception],
    message_fragment: str,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")
    qc = FakeQuantumCircuit(
        num_qubits=2,
        data=(FakeCircuitInstruction(FakeOperation("h"), (q0,)),),
        bit_index_by_qubit={q0: bit_index},
    )

    with pytest.raises(expected_exception, match=message_fragment):
        qiskit_adapter_module.convert_qiskit_circuit(qc)


def test_convert_qiskit_circuit_rejects_controlled_gate_with_identical_qubit_indices(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    control = FakeQubit("control")
    target = FakeQubit("target")
    qc = FakeQuantumCircuit(
        num_qubits=2,
        data=(FakeCircuitInstruction(FakeOperation("cx"), (control, target)),),
        bit_index_by_qubit={control: 0, target: 0},
    )

    with pytest.raises(ValueError, match="control and target must refer to different qubits"):
        qiskit_adapter_module.convert_qiskit_circuit(qc)


@pytest.mark.parametrize("data", ["abc", 123])
def test_convert_qiskit_circuit_rejects_malformed_instruction_data_collection(
    monkeypatch: pytest.MonkeyPatch,
    data: object,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    qc = SimpleNamespace(
        num_qubits=1,
        data=data,
        find_bit=lambda _bit: FakeBitLocation(index=0),
    )

    with pytest.raises(TypeError, match=r"data.*sequence"):
        qiskit_adapter_module.convert_qiskit_circuit(qc)

    _assert_no_graphix_operations_recorded()


@pytest.mark.parametrize(
    ("instruction", "message_fragment"),
    [
        (SimpleNamespace(qubits=(FakeQubit("q0"),)), "instruction at index 0.*operation"),
        (SimpleNamespace(operation=FakeOperation("h")), "instruction at index 0.*qubits"),
        (
            SimpleNamespace(operation=FakeOperation("h"), qubits=123),
            "instruction at index 0.*qubits.*sequence",
        ),
    ],
)
def test_convert_qiskit_circuit_rejects_malformed_instruction_shape(
    monkeypatch: pytest.MonkeyPatch,
    instruction: object,
    message_fragment: str,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")
    qc = FakeQuantumCircuit(
        num_qubits=1,
        data=(instruction,),
        bit_index_by_qubit={q0: 0},
    )

    with pytest.raises(TypeError, match=message_fragment):
        qiskit_adapter_module.convert_qiskit_circuit(qc)

    _assert_no_graphix_operations_recorded()


def test_convert_qiskit_circuit_rejects_find_bit_without_index(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")

    class MissingIndexQuantumCircuit(FakeQuantumCircuit):
        def find_bit(self, bit: object) -> FakeBitLocation:
            del bit
            return cast(FakeBitLocation, object())

    qc = MissingIndexQuantumCircuit(
        num_qubits=1,
        data=(FakeCircuitInstruction(FakeOperation("h"), (q0,)),),
        bit_index_by_qubit={q0: 0},
    )

    with pytest.raises(TypeError, match=r"find_bit\(\).*\.index"):
        qiskit_adapter_module.convert_qiskit_circuit(qc)

    _assert_no_graphix_operations_recorded()


def test_convert_qiskit_circuit_rejects_find_bit_errors_with_clear_wrapper_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    _install_fake_qiskit(monkeypatch)
    q0 = FakeQubit("q0")

    class ErroringFindBitQuantumCircuit(FakeQuantumCircuit):
        def find_bit(self, bit: object) -> FakeBitLocation:
            raise KeyError(bit)

    qc = ErroringFindBitQuantumCircuit(
        num_qubits=1,
        data=(FakeCircuitInstruction(FakeOperation("h"), (q0,)),),
        bit_index_by_qubit={q0: 0},
    )

    with pytest.raises(TypeError, match=r"find_bit\(\).*instruction index 0"):
        qiskit_adapter_module.convert_qiskit_circuit(qc)

    _assert_no_graphix_operations_recorded()


def test_from_qiskit_imports_supported_qiskit_subset_when_qiskit_is_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    qiskit = pytest.importorskip("qiskit")
    _install_fake_graphix(monkeypatch)
    qc = qiskit.QuantumCircuit(2)
    qc.h(0)
    qc.rx(math.pi / 2, 0)
    qc.cx(0, 1)

    lab_circuit = from_qiskit(qc)

    assert _unwrap_graphix_circuit(lab_circuit).operations == [
        ("h", (0,)),
        ("rx", (0, 0.5)),
        ("cnot", (0, 1)),
    ]


def test_from_qiskit_rejects_unsupported_qiskit_instruction_when_qiskit_is_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    qiskit = pytest.importorskip("qiskit")
    _install_fake_graphix(monkeypatch)
    qc = qiskit.QuantumCircuit(1, 1)
    qc.measure(0, 0)

    with pytest.raises(UnsupportedGateError, match="measure"):
        from_qiskit(qc)
