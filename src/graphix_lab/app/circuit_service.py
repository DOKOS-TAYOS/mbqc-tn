from __future__ import annotations

import math

from graphix_lab.infrastructure.graphix_adapter import (
    GraphixCircuitProtocol,
    create_graphix_circuit,
    extract_pattern_from_transpile_result,
)
from graphix_lab.infrastructure.graphix_runtime import require_graphix_callable


def build_graphix_circuit(width: int) -> GraphixCircuitProtocol:
    return create_graphix_circuit(width)


def apply_single_qubit_gate(
    graphix_circuit: GraphixCircuitProtocol,
    gate_name: str,
    qubit: int,
) -> None:
    _call_graphix_gate(graphix_circuit, gate_name, qubit)


def apply_rotation_gate(
    graphix_circuit: GraphixCircuitProtocol,
    gate_name: str,
    qubit: int,
    angle: float,
    *,
    units: str = "pi",
) -> None:
    graphix_angle = normalize_angle(angle, units=units)
    _call_graphix_gate(graphix_circuit, gate_name, qubit, graphix_angle)


def apply_cnot_gate(
    graphix_circuit: GraphixCircuitProtocol,
    control: int,
    target: int,
) -> None:
    _call_graphix_gate(graphix_circuit, "cnot", control, target)


def compile_graphix_circuit(graphix_circuit: GraphixCircuitProtocol) -> object:
    transpile_method = require_graphix_callable(
        graphix_circuit,
        "transpile",
        feature_name="Circuit.transpile",
    )
    transpile_result = transpile_method()
    return extract_pattern_from_transpile_result(transpile_result)


def normalize_angle(angle: float, *, units: str = "pi") -> float:
    normalized_units = units.strip().lower()
    numeric_angle = float(angle)

    if normalized_units == "pi":
        return numeric_angle
    if normalized_units == "radians":
        return numeric_angle / math.pi

    raise ValueError(f"Unsupported angle units {units!r}. Supported units are 'pi' and 'radians'.")


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
