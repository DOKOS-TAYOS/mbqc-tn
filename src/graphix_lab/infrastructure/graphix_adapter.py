from __future__ import annotations

from collections.abc import Callable, Iterable
from importlib import import_module
from types import ModuleType
from typing import Protocol, cast, runtime_checkable

from graphix_lab.domain.commands import CommandRecord
from graphix_lab.domain.errors import GraphixCompatibilityError, GraphixUnavailableError

_KNOWN_COMMAND_KINDS = frozenset({"N", "E", "M", "X", "Z", "C"})


class GraphixCircuitProtocol(Protocol):
    width: int

    def h(self, q: int) -> object: ...

    def x(self, q: int) -> object: ...

    def y(self, q: int) -> object: ...

    def z(self, q: int) -> object: ...

    def s(self, q: int) -> object: ...

    def rx(self, q: int, angle: float) -> object: ...

    def ry(self, q: int, angle: float) -> object: ...

    def rz(self, q: int, angle: float) -> object: ...

    def cnot(self, control: int, target: int) -> object: ...

    def transpile(self) -> object: ...


@runtime_checkable
class SupportsIntProtocol(Protocol):
    def __int__(self) -> int: ...


@runtime_checkable
class SupportsFloatProtocol(Protocol):
    def __float__(self) -> float: ...


def create_graphix_circuit(width: int) -> GraphixCircuitProtocol:
    circuit_factory = load_graphix_circuit_class()
    graphix_circuit = circuit_factory(width)
    return cast(GraphixCircuitProtocol, graphix_circuit)


def load_graphix_circuit_class() -> Callable[[int], GraphixCircuitProtocol]:
    graphix_module = _import_graphix_root()
    circuit_class = getattr(graphix_module, "Circuit", None)
    if not callable(circuit_class):
        raise GraphixCompatibilityError(feature="Circuit")
    return cast(Callable[[int], GraphixCircuitProtocol], circuit_class)


def extract_pattern_from_transpile_result(transpile_result: object) -> object:
    pattern = getattr(transpile_result, "pattern", None)
    if pattern is not None:
        return pattern
    raise GraphixCompatibilityError(
        feature="Circuit.transpile().pattern",
        message=(
            "The installed Graphix runtime returned an unexpected transpile result. "
            "Expected an object with a 'pattern' attribute."
        ),
    )


def extract_command_records(pattern: object) -> tuple[CommandRecord, ...]:
    graphix_commands = _iter_pattern_commands(pattern)
    return tuple(
        _extract_command_record(index=index, graphix_command=graphix_command)
        for index, graphix_command in enumerate(graphix_commands)
    )


def _iter_pattern_commands(pattern: object) -> tuple[object, ...]:
    if not isinstance(pattern, Iterable):
        raise GraphixCompatibilityError(
            feature="Pattern.__iter__",
            message=(
                "The installed Graphix runtime returned a pattern object that Graphix Lab could "
                "not iterate over to inspect its command sequence."
            ),
        )

    try:
        return tuple(pattern)
    except TypeError as error:
        raise GraphixCompatibilityError(
            feature="Pattern.__iter__",
            message=(
                "The installed Graphix runtime returned a pattern object that Graphix Lab could "
                "not iterate over to inspect its command sequence."
            ),
        ) from error


def _extract_command_record(index: int, graphix_command: object) -> CommandRecord:
    command_kind = _normalize_command_kind(graphix_command)
    if command_kind not in _KNOWN_COMMAND_KINDS:
        return CommandRecord(index=index, kind="UNKNOWN", raw=repr(graphix_command))

    node = _extract_node(graphix_command)
    return CommandRecord(
        index=index,
        kind=command_kind,
        node=node,
        nodes=_extract_nodes(graphix_command, command_kind=command_kind, node=node),
        angle=_extract_angle(graphix_command),
        plane=_extract_plane(graphix_command),
        s_domain=_extract_domain(graphix_command, attribute_name="s_domain"),
        t_domain=_extract_domain(graphix_command, attribute_name="t_domain"),
        domain=_extract_domain(graphix_command, attribute_name="domain"),
        raw=repr(graphix_command),
    )


def _normalize_command_kind(graphix_command: object) -> str:
    kind_value = getattr(graphix_command, "kind", None)
    if kind_name := _normalize_kind_value(kind_value):
        return kind_name

    class_name = type(graphix_command).__name__.upper()
    if class_name in _KNOWN_COMMAND_KINDS:
        return class_name
    return "UNKNOWN"


def _normalize_kind_value(kind_value: object) -> str | None:
    enum_name = getattr(kind_value, "name", None)
    if isinstance(enum_name, str):
        return enum_name.upper()
    if not isinstance(kind_value, str):
        return None

    normalized_kind = kind_value.strip().upper()
    if "." in normalized_kind:
        normalized_kind = normalized_kind.rsplit(".", maxsplit=1)[-1]
    return normalized_kind or None


def _extract_node(graphix_command: object) -> int | None:
    node_value = getattr(graphix_command, "node", None)
    return _coerce_int(node_value)


def _extract_nodes(
    graphix_command: object,
    *,
    command_kind: str,
    node: int | None,
) -> tuple[int, ...]:
    if command_kind == "E":
        node_values = getattr(graphix_command, "nodes", ())
        return _coerce_int_tuple(node_values, sort_values=False)
    if node is None:
        return ()
    return (node,)


def _extract_angle(graphix_command: object) -> float | None:
    angle_value = getattr(graphix_command, "angle", None)
    if angle_value is None:
        angle_value = _extract_measurement_attribute(graphix_command, attribute_name="angle")
    return _coerce_float(angle_value)


def _extract_plane(graphix_command: object) -> str | None:
    plane_value = getattr(graphix_command, "plane", None)
    if plane_value is None:
        plane_value = _extract_measurement_attribute(graphix_command, attribute_name="plane")
    if plane_value is None:
        return None
    plane_name = getattr(plane_value, "name", None)
    if isinstance(plane_name, str):
        return plane_name
    return str(plane_value)


def _extract_measurement_attribute(
    graphix_command: object,
    *,
    attribute_name: str,
) -> object | None:
    measurement = getattr(graphix_command, "measurement", None)
    if measurement is None:
        return None

    attribute_value = getattr(measurement, attribute_name, None)
    if attribute_value is not None:
        return attribute_value

    to_bloch = getattr(measurement, "to_bloch", None)
    if not callable(to_bloch):
        return None

    bloch_measurement = to_bloch()
    return getattr(bloch_measurement, attribute_name, None)


def _extract_domain(graphix_command: object, *, attribute_name: str) -> tuple[int, ...]:
    return _coerce_int_tuple(getattr(graphix_command, attribute_name, ()), sort_values=True)


def _coerce_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    if not isinstance(value, SupportsIntProtocol):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _coerce_int_tuple(values: object, *, sort_values: bool) -> tuple[int, ...]:
    if values is None:
        return ()

    if isinstance(values, (set, frozenset)):
        coerced_values = [_coerce_int(value) for value in values]
        valid_values = [value for value in coerced_values if value is not None]
        return tuple(sorted(valid_values))

    if isinstance(values, (list, tuple)):
        coerced_values = [_coerce_int(value) for value in values]
        valid_values = [value for value in coerced_values if value is not None]
        return tuple(sorted(valid_values) if sort_values else valid_values)

    coerced_value = _coerce_int(values)
    if coerced_value is None:
        return ()
    return (coerced_value,)


def _coerce_float(value: object) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    if isinstance(value, SupportsFloatProtocol):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
    if isinstance(value, SupportsIntProtocol):
        try:
            return float(int(value))
        except (TypeError, ValueError):
            return None
    return None


def _import_graphix_root() -> ModuleType:
    try:
        return import_module("graphix")
    except ModuleNotFoundError as error:
        if error.name == "graphix":
            raise GraphixUnavailableError() from error
        raise GraphixCompatibilityError(
            message=(
                "Graphix appears to be installed, but importing it failed because a required "
                f"dependency could not be loaded: {error.name!r}."
            )
        ) from error
    except Exception as error:  # pragma: no cover - defensive fallback
        raise GraphixCompatibilityError(
            message="Graphix is installed but could not be imported cleanly."
        ) from error
