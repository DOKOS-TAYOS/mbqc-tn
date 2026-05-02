from __future__ import annotations

from types import ModuleType

import pytest

import graphix_lab.infrastructure.graphix_capabilities as graphix_capabilities_module
from graphix_lab import graphix_info
from graphix_lab.domain.errors import GraphixUnavailableError
from graphix_lab.infrastructure.graphix_capabilities import GraphixCapabilities


def _set_module_attr(module: ModuleType, attribute_name: str, value: object) -> None:
    setattr(module, attribute_name, value)


def _build_fake_graphix_modules() -> dict[str, ModuleType]:
    fake_graphix = ModuleType("graphix")
    fake_pattern_module = ModuleType("graphix.pattern")
    fake_simulator_module = ModuleType("graphix.simulator")
    fake_statevector_module = ModuleType("graphix.sim.statevec")
    fake_density_matrix_module = ModuleType("graphix.sim.density_matrix")
    fake_tensor_network_module = ModuleType("graphix.sim.tensornet")

    class FakeCircuit:
        pass

    class FakePattern:
        def simulate_pattern(self) -> None:
            return None

        def draw_graph(self) -> None:
            return None

        def draw_flow(self) -> None:
            return None

        def standardize(self) -> None:
            return None

        def shift_signals(self) -> None:
            return None

        def perform_pauli_measurements(self) -> None:
            return None

    class FakePatternSimulator:
        pass

    class FakeStatevectorBackend:
        pass

    class FakeDensityMatrixBackend:
        pass

    class FakeTensorNetworkBackend:
        pass

    _set_module_attr(fake_graphix, "Circuit", FakeCircuit)
    _set_module_attr(fake_graphix, "Pattern", FakePattern)
    _set_module_attr(fake_pattern_module, "Pattern", FakePattern)
    _set_module_attr(fake_simulator_module, "PatternSimulator", FakePatternSimulator)
    _set_module_attr(fake_statevector_module, "StatevectorBackend", FakeStatevectorBackend)
    _set_module_attr(fake_density_matrix_module, "DensityMatrixBackend", FakeDensityMatrixBackend)
    _set_module_attr(fake_tensor_network_module, "TensorNetworkBackend", FakeTensorNetworkBackend)

    return {
        "graphix": fake_graphix,
        "graphix.pattern": fake_pattern_module,
        "graphix.simulator": fake_simulator_module,
        "graphix.sim.statevec": fake_statevector_module,
        "graphix.sim.density_matrix": fake_density_matrix_module,
        "graphix.sim.tensornet": fake_tensor_network_module,
    }


def test_graphix_info_reports_detected_capabilities_when_graphix_is_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_modules = _build_fake_graphix_modules()

    def fake_version(distribution_name: str) -> str:
        assert distribution_name == "graphix"
        return "0.3.5"

    def fake_import_module(module_name: str) -> ModuleType:
        if module_name in fake_modules:
            return fake_modules[module_name]
        raise ModuleNotFoundError(module_name)

    monkeypatch.setattr(graphix_capabilities_module.metadata, "version", fake_version)
    monkeypatch.setattr(graphix_capabilities_module, "import_module", fake_import_module)

    assert graphix_info() == GraphixCapabilities(
        version="0.3.5",
        has_circuit=True,
        has_pattern_simulate_pattern=True,
        has_pattern_draw_graph=True,
        has_pattern_draw_flow=True,
        has_pattern_draw_xzcorrections=False,
        has_pattern_standardize=True,
        has_pattern_shift_signals=True,
        has_pattern_perform_pauli_measurements=True,
        supported_backends=("statevector", "densitymatrix", "tensornetwork"),
    )


def test_graphix_info_raises_clear_error_when_graphix_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_version(_: str) -> str:
        raise graphix_capabilities_module.metadata.PackageNotFoundError

    monkeypatch.setattr(graphix_capabilities_module.metadata, "version", fake_version)

    with pytest.raises(
        GraphixUnavailableError,
        match="Graphix is not installed in the active environment",
    ):
        graphix_info()
