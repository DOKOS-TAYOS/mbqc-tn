from __future__ import annotations

from collections.abc import Sequence
from importlib import import_module
from typing import TYPE_CHECKING, Protocol, SupportsFloat, TypeGuard, cast

from ..app.circuit_service import (
    _validate_positive_circuit_width,
    _validate_qubit_index_in_width,
    normalize_angle,
)
from ..domain.errors import OptionalDependencyError, UnsupportedGateError

if TYPE_CHECKING:
    from ..public_api import LabCircuit

_SUPPORTED_SINGLE_QUBIT_GATES = frozenset({"h", "s", "x", "y", "z"})
_SUPPORTED_ROTATION_GATES = frozenset({"rx", "ry", "rz"})
_SUPPORTED_CONTROLLED_GATES = frozenset({"cx", "cnot"})


class QiskitBitLocationProtocol(Protocol):
    index: int


class QiskitOperationProtocol(Protocol):
    name: str
    params: Sequence[object]


class QiskitCircuitInstructionProtocol(Protocol):
    operation: QiskitOperationProtocol
    qubits: Sequence[object]
    params: Sequence[object]


class QiskitCircuitProtocol(Protocol):
    num_qubits: int
    data: Sequence[QiskitCircuitInstructionProtocol]

    def find_bit(self, bit: object) -> QiskitBitLocationProtocol: ...


def convert_qiskit_circuit(
    qc: object,
    *,
    angle_units: str = "radians",
) -> LabCircuit:
    _require_qiskit()

    from ..public_api import LabCircuit

    qiskit_circuit = _coerce_qiskit_circuit(qc)
    circuit_width = _validate_positive_circuit_width(
        qiskit_circuit.num_qubits,
        argument_name="num_qubits",
    )
    instruction_data = _coerce_instruction_data(qiskit_circuit.data)
    lab_circuit = LabCircuit(width=circuit_width)

    for gate_index, raw_instruction in enumerate(instruction_data):
        circuit_instruction, instruction_qubits = _coerce_circuit_instruction(
            raw_instruction,
            gate_index=gate_index,
        )
        gate_name = _read_gate_name(circuit_instruction)
        qubit_indices = _read_qubit_indices(
            qiskit_circuit,
            instruction_qubits,
            circuit_width=circuit_width,
            gate_index=gate_index,
        )

        if gate_name in _SUPPORTED_SINGLE_QUBIT_GATES:
            _apply_single_qubit_gate(
                lab_circuit,
                gate_name,
                qubit_indices,
                gate_index=gate_index,
            )
            continue
        if gate_name in _SUPPORTED_ROTATION_GATES:
            _apply_rotation_gate(
                lab_circuit,
                gate_name,
                circuit_instruction,
                qubit_indices,
                gate_index=gate_index,
                angle_units=angle_units,
            )
            continue
        if gate_name in _SUPPORTED_CONTROLLED_GATES:
            _apply_cnot_gate(
                lab_circuit,
                gate_name,
                qubit_indices,
                gate_index=gate_index,
            )
            continue

        raise UnsupportedGateError(gate_name, gate_index=gate_index)

    return lab_circuit


def _coerce_qiskit_circuit(qc: object) -> QiskitCircuitProtocol:
    if (
        not hasattr(qc, "num_qubits")
        or not hasattr(qc, "data")
        or not callable(getattr(qc, "find_bit", None))
    ):
        raise TypeError(
            "from_qiskit() expects a Qiskit-like circuit object with num_qubits, data, and "
            "find_bit()."
        )
    return cast(QiskitCircuitProtocol, qc)


def _coerce_instruction_data(data: object) -> tuple[object, ...]:
    if not _is_nonstring_sequence(data):
        raise TypeError(
            "from_qiskit() expects circuit.data to be a sequence of Qiskit-like instructions."
        )
    return tuple(cast(Sequence[object], data))


def _coerce_circuit_instruction(
    circuit_instruction: object,
    *,
    gate_index: int,
) -> tuple[QiskitCircuitInstructionProtocol, tuple[object, ...]]:
    if not hasattr(circuit_instruction, "operation"):
        raise TypeError(
            f"from_qiskit() expects instruction at index {gate_index} to expose an "
            "operation attribute."
        )
    if not hasattr(circuit_instruction, "qubits"):
        raise TypeError(
            f"from_qiskit() expects instruction at index {gate_index} to expose a qubits attribute."
        )

    validated_instruction = cast(QiskitCircuitInstructionProtocol, circuit_instruction)
    instruction_qubits = validated_instruction.qubits
    if not _is_nonstring_sequence(instruction_qubits):
        raise TypeError(
            f"from_qiskit() expects instruction at index {gate_index} to expose qubits as a "
            "sequence."
        )

    return validated_instruction, tuple(cast(Sequence[object], instruction_qubits))


def _require_qiskit() -> None:
    try:
        import_module("qiskit")
    except ModuleNotFoundError as error:
        if error.name == "qiskit":
            raise OptionalDependencyError("qiskit", feature="from_qiskit()") from error
        raise OptionalDependencyError(
            "qiskit",
            feature="from_qiskit()",
            message=(
                "Qiskit appears to be installed, but importing it failed because a required "
                f"dependency could not be loaded: {error.name!r}."
            ),
        ) from error
    except Exception as error:  # pragma: no cover - defensive fallback
        raise OptionalDependencyError(
            "qiskit",
            feature="from_qiskit()",
            message=(
                "Qiskit is installed but could not be imported cleanly in the active environment."
            ),
        ) from error


def _read_gate_name(circuit_instruction: QiskitCircuitInstructionProtocol) -> str:
    gate_name = getattr(circuit_instruction.operation, "name", "")
    return str(gate_name).strip().lower()


def _read_qubit_indices(
    qc: QiskitCircuitProtocol,
    qubits: Sequence[object],
    *,
    circuit_width: int,
    gate_index: int,
) -> tuple[int, ...]:
    return tuple(
        _read_qubit_index(
            qc,
            qubit,
            circuit_width=circuit_width,
            gate_index=gate_index,
        )
        for qubit in qubits
    )


def _read_qubit_index(
    qc: QiskitCircuitProtocol,
    qubit: object,
    *,
    circuit_width: int,
    gate_index: int,
) -> int:
    try:
        bit_location = qc.find_bit(qubit)
    except Exception as error:
        raise TypeError(
            "from_qiskit() expects find_bit() to resolve each qubit operand; "
            f"instruction index {gate_index} could not be resolved."
        ) from error

    if not hasattr(bit_location, "index"):
        raise TypeError(
            "from_qiskit() expects find_bit() to return an object with .index for "
            f"instruction index {gate_index}."
        )

    return _validate_qubit_index_in_width(
        bit_location.index,
        width=circuit_width,
        argument_name="find_bit(...).index",
    )


def _apply_single_qubit_gate(
    lab_circuit: LabCircuit,
    gate_name: str,
    qubit_indices: Sequence[int],
    *,
    gate_index: int,
) -> None:
    qubit_index = _require_qubit_arity(
        gate_name,
        qubit_indices,
        expected_arity=1,
        gate_index=gate_index,
    )
    getattr(lab_circuit, gate_name)(qubit_index)


def _apply_rotation_gate(
    lab_circuit: LabCircuit,
    gate_name: str,
    circuit_instruction: QiskitCircuitInstructionProtocol,
    qubit_indices: Sequence[int],
    *,
    gate_index: int,
    angle_units: str,
) -> None:
    qubit_index = _require_qubit_arity(
        gate_name,
        qubit_indices,
        expected_arity=1,
        gate_index=gate_index,
    )
    params = _read_instruction_params(circuit_instruction)
    if len(params) != 1:
        raise UnsupportedGateError(
            gate_name,
            gate_index=gate_index,
            message=(
                f"Gate {gate_name!r} at instruction index {gate_index} must provide exactly one "
                "rotation angle."
            ),
        )

    try:
        numeric_angle = _coerce_angle_parameter(
            params[0],
            gate_name=gate_name,
            gate_index=gate_index,
        )
        graphix_angle = normalize_angle(numeric_angle, units=angle_units)
    except ValueError:
        raise
    except (TypeError, OverflowError) as error:
        raise UnsupportedGateError(
            gate_name,
            gate_index=gate_index,
            message=(
                f"Gate {gate_name!r} at instruction index {gate_index} must provide a numeric "
                "rotation angle."
            ),
        ) from error

    getattr(lab_circuit, gate_name)(qubit_index, graphix_angle, units="pi")


def _coerce_angle_parameter(
    parameter: object,
    *,
    gate_name: str,
    gate_index: int,
) -> float:
    if isinstance(parameter, bool):
        raise UnsupportedGateError(
            gate_name,
            gate_index=gate_index,
            message=(
                f"Gate {gate_name!r} at instruction index {gate_index} must provide a numeric "
                "rotation angle."
            ),
        )
    if not _is_float_like(parameter):
        raise UnsupportedGateError(
            gate_name,
            gate_index=gate_index,
            message=(
                f"Gate {gate_name!r} at instruction index {gate_index} must provide a numeric "
                "rotation angle."
            ),
        )
    return float(parameter)


def _apply_cnot_gate(
    lab_circuit: LabCircuit,
    gate_name: str,
    qubit_indices: Sequence[int],
    *,
    gate_index: int,
) -> None:
    control, target = _require_qubit_pair(gate_name, qubit_indices, gate_index=gate_index)
    lab_circuit.cnot(control, target)


def _read_instruction_params(
    circuit_instruction: QiskitCircuitInstructionProtocol,
) -> tuple[object, ...]:
    if _is_nonstring_sequence(circuit_instruction.params):
        return tuple(circuit_instruction.params)

    operation_params = getattr(circuit_instruction.operation, "params", ())
    if _is_nonstring_sequence(operation_params):
        return tuple(operation_params)
    return ()


def _is_nonstring_sequence(value: object) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _is_float_like(value: object) -> TypeGuard[SupportsFloat | str]:
    return not isinstance(value, bool) and (
        isinstance(value, (int, float, str)) or hasattr(value, "__float__")
    )


def _require_qubit_arity(
    gate_name: str,
    qubit_indices: Sequence[int],
    *,
    expected_arity: int,
    gate_index: int,
) -> int:
    if len(qubit_indices) != expected_arity:
        raise UnsupportedGateError(
            gate_name,
            gate_index=gate_index,
            message=(
                f"Gate {gate_name!r} at instruction index {gate_index} expected "
                f"{expected_arity} qubit operand(s), but received {len(qubit_indices)}."
            ),
        )
    return qubit_indices[0]


def _require_qubit_pair(
    gate_name: str,
    qubit_indices: Sequence[int],
    *,
    gate_index: int,
) -> tuple[int, int]:
    if len(qubit_indices) != 2:
        raise UnsupportedGateError(
            gate_name,
            gate_index=gate_index,
            message=(
                f"Gate {gate_name!r} at instruction index {gate_index} expected 2 qubit "
                f"operands, but received {len(qubit_indices)}."
            ),
        )
    return (qubit_indices[0], qubit_indices[1])
