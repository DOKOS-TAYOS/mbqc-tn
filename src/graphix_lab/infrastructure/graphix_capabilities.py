from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module, metadata
from types import ModuleType

from graphix_lab.domain.errors import GraphixCompatibilityError, GraphixUnavailableError

_GRAPHIX_DISTRIBUTION_NAME = "graphix"
_BACKEND_MODULES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("statevector", "graphix.sim.statevec", ("StatevectorBackend", "StateVectorBackend")),
    ("densitymatrix", "graphix.sim.density_matrix", ("DensityMatrixBackend",)),
    ("tensornetwork", "graphix.sim.tensornet", ("TensorNetworkBackend",)),
    ("mps", "graphix.sim.mps", ("MPSBackend", "MpsBackend")),
)


@dataclass(frozen=True, slots=True)
class GraphixCapabilities:
    version: str
    has_circuit: bool
    has_pattern_simulate_pattern: bool
    has_pattern_draw_graph: bool
    has_pattern_draw_flow: bool
    has_pattern_draw_xzcorrections: bool
    has_pattern_standardize: bool
    has_pattern_shift_signals: bool
    has_pattern_perform_pauli_measurements: bool
    supported_backends: tuple[str, ...]


def graphix_info() -> GraphixCapabilities:
    return detect_graphix_capabilities()


def detect_graphix_capabilities() -> GraphixCapabilities:
    version = _detect_graphix_version()
    graphix_module = _import_graphix_root()
    pattern_type = _load_pattern_type(graphix_module)
    simulator_module = _optional_import("graphix.simulator")

    return GraphixCapabilities(
        version=version,
        has_circuit=hasattr(graphix_module, "Circuit"),
        has_pattern_simulate_pattern=_pattern_has_attr(pattern_type, "simulate_pattern"),
        has_pattern_draw_graph=_pattern_has_attr(pattern_type, "draw_graph"),
        has_pattern_draw_flow=_pattern_has_attr(pattern_type, "draw_flow"),
        has_pattern_draw_xzcorrections=_pattern_has_attr(pattern_type, "draw_xzcorrections"),
        has_pattern_standardize=_pattern_has_attr(pattern_type, "standardize"),
        has_pattern_shift_signals=_pattern_has_attr(pattern_type, "shift_signals"),
        has_pattern_perform_pauli_measurements=_pattern_has_attr(
            pattern_type,
            "perform_pauli_measurements",
        ),
        supported_backends=_detect_supported_backends(graphix_module, simulator_module),
    )


def _detect_graphix_version() -> str:
    try:
        return metadata.version(_GRAPHIX_DISTRIBUTION_NAME)
    except metadata.PackageNotFoundError as error:
        raise GraphixUnavailableError() from error
    except Exception as error:  # pragma: no cover - defensive fallback
        raise GraphixCompatibilityError(
            message="Graphix metadata is present but its version could not be inspected."
        ) from error


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


def _load_pattern_type(graphix_module: ModuleType) -> type[object] | None:
    exported_pattern = getattr(graphix_module, "Pattern", None)
    if isinstance(exported_pattern, type):
        return exported_pattern

    pattern_module = _optional_import("graphix.pattern")
    if pattern_module is None:
        return None

    nested_pattern = getattr(pattern_module, "Pattern", None)
    if isinstance(nested_pattern, type):
        return nested_pattern
    return None


def _pattern_has_attr(pattern_type: type[object] | None, attribute_name: str) -> bool:
    return pattern_type is not None and hasattr(pattern_type, attribute_name)


def _detect_supported_backends(
    graphix_module: ModuleType,
    simulator_module: ModuleType | None,
) -> tuple[str, ...]:
    supported_backends: list[str] = []

    for backend_name, module_name, attribute_names in _BACKEND_MODULES:
        backend_module = _optional_import(module_name)
        search_modules = tuple(
            module
            for module in (backend_module, simulator_module, graphix_module)
            if module is not None
        )
        if any(_module_has_any_attr(module, attribute_names) for module in search_modules):
            supported_backends.append(backend_name)

    return tuple(supported_backends)


def _module_has_any_attr(module: ModuleType, attribute_names: tuple[str, ...]) -> bool:
    return any(hasattr(module, attribute_name) for attribute_name in attribute_names)


def _optional_import(module_name: str) -> ModuleType | None:
    try:
        return import_module(module_name)
    except ModuleNotFoundError:
        return None
    except Exception:  # pragma: no cover - defensive fallback
        return None
