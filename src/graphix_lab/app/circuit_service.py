from __future__ import annotations

import math
from typing import SupportsFloat, SupportsIndex, TypeAlias

from graphix_lab.infrastructure.graphix_adapter import (
    GraphixCircuitProtocol,
    create_graphix_circuit,
    extract_pattern_from_transpile_result,
)
from graphix_lab.infrastructure.graphix_runtime import require_graphix_callable

AngleLike: TypeAlias = float | int | str | SupportsFloat | SupportsIndex


def build_graphix_circuit(width: int) -> GraphixCircuitProtocol:
    return create_graphix_circuit(width)


def apply_single_qubit_gate(
    graphix_circuit: GraphixCircuitProtocol,
    gate_name: str,
    qubit: int,
) -> None:
    validated_qubit = _validate_qubit_index_in_width(
        qubit,
        width=graphix_circuit.width,
        argument_name="qubit",
    )
    _call_graphix_gate(graphix_circuit, gate_name, validated_qubit)


def apply_rotation_gate(
    graphix_circuit: GraphixCircuitProtocol,
    gate_name: str,
    qubit: int,
    angle: AngleLike,
    *,
    units: str = "pi",
) -> None:
    validated_qubit = _validate_qubit_index_in_width(
        qubit,
        width=graphix_circuit.width,
        argument_name="qubit",
    )
    graphix_angle = normalize_angle(angle, units=units)
    _call_graphix_gate(graphix_circuit, gate_name, validated_qubit, graphix_angle)


def apply_cnot_gate(
    graphix_circuit: GraphixCircuitProtocol,
    control: int,
    target: int,
) -> None:
    validated_control, validated_target = _validate_cnot_operands(
        control,
        target,
        width=graphix_circuit.width,
    )
    _call_graphix_gate(graphix_circuit, "cnot", validated_control, validated_target)


def compile_graphix_circuit(graphix_circuit: GraphixCircuitProtocol) -> object:
    transpile_method = require_graphix_callable(
        graphix_circuit,
        "transpile",
        feature_name="Circuit.transpile",
    )
    transpile_result = transpile_method()
    return extract_pattern_from_transpile_result(transpile_result)


def normalize_angle(angle: AngleLike, *, units: str = "pi") -> float:
    normalized_units = units.strip().lower()
    numeric_angle = _coerce_real_angle(angle)

    if normalized_units == "pi":
        return numeric_angle
    if normalized_units == "radians":
        return numeric_angle / math.pi

    raise ValueError(f"Unsupported angle units {units!r}. Supported units are 'pi' and 'radians'.")


def _validate_positive_circuit_width(width: object, *, argument_name: str = "width") -> int:
    if isinstance(width, bool) or not isinstance(width, int) or width <= 0:
        raise ValueError(f"{argument_name} must be a positive integer.")
    return width


def _validate_qubit_index(index: object, *, argument_name: str) -> int:
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError(f"{argument_name} must be an integer qubit index.")
    return index


def _validate_qubit_index_in_width(
    index: object,
    *,
    width: object,
    argument_name: str,
) -> int:
    validated_width = _validate_positive_circuit_width(width)
    validated_index = _validate_qubit_index(index, argument_name=argument_name)
    if validated_index < 0 or validated_index >= validated_width:
        raise ValueError(
            f"{argument_name} must be between 0 and {validated_width - 1} "
            f"for a circuit of width {validated_width}."
        )
    return validated_index


def _validate_cnot_operands(
    control: object,
    target: object,
    *,
    width: object,
) -> tuple[int, int]:
    validated_control = _validate_qubit_index_in_width(
        control,
        width=width,
        argument_name="control",
    )
    validated_target = _validate_qubit_index_in_width(
        target,
        width=width,
        argument_name="target",
    )
    if validated_control == validated_target:
        raise ValueError("control and target must refer to different qubits.")
    return (validated_control, validated_target)


def _coerce_real_angle(angle: AngleLike) -> float:
    if isinstance(angle, bool):
        raise TypeError("angle must be a real number, not bool.")
    return float(angle)


def _call_graphix_gate(
    graphix_circuit: GraphixCircuitProtocol,
    gate_name: str,
    *args: int | float,
) -> None:
    graphix_gate = require_graphix_callable(
        graphix_circuit,
        gate_name,
        feature_name=f"Circuit.{gate_name}",
    )
    graphix_gate(*args)
