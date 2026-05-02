from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from types import ModuleType
from typing import Protocol, cast

from graphix_lab.domain.errors import GraphixCompatibilityError, GraphixUnavailableError


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
