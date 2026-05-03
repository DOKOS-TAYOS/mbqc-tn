from __future__ import annotations

import warnings
from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum, auto
from types import ModuleType, SimpleNamespace
from typing import Any, ClassVar, cast

import matplotlib

matplotlib.use("Agg")
import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib.colors import to_hex
from matplotlib.figure import Figure

import graphix_lab.infrastructure.graphix_runtime as graphix_runtime_module
from graphix_lab import (
    BackendComparisonReport,
    CommandRecord,
    LabPattern,
    PatternSummary,
    ResourceSummary,
    RunTrace,
    SimulationReport,
    TraceAnimationHandle,
    circuit,
    from_graphix_pattern,
)
from graphix_lab.app.simulation_service import build_syntactic_trace
from graphix_lab.app.visualization_service import (
    _NODE_FILL_CURRENT,
    _NODE_FILL_MEASURED,
    build_visualization_model,
)
from graphix_lab.domain.errors import GraphixCompatibilityError, UnsupportedBackendError


@dataclass(slots=True)
class FakePattern:
    label: str = "compiled-pattern"
    operations: list[str] = field(default_factory=list)
    copy_calls: int = 0
    compiled_commands: tuple[object, ...] = ()
    last_simulation_backend: str | None = None
    simulation_backends: list[str] = field(default_factory=list)
    last_rng_sample: int | None = None

    def copy(self) -> FakePattern:
        self.copy_calls += 1
        return FakePattern(
            label=f"{self.label}-copy",
            operations=list(self.operations),
            compiled_commands=tuple(self.compiled_commands),
        )

    def standardize(self) -> None:
        self.operations.append("standardize")

    def shift_signals(self) -> dict[int, set[int]]:
        self.operations.append("shift_signals")
        return {}

    def perform_pauli_measurements(self) -> None:
        self.operations.append("perform_pauli_measurements")

    def simulate_pattern(
        self,
        backend: str = "statevector",
        input_state: object | None = None,
        rng: np.random.Generator | None = None,
        **kwargs: object,
    ) -> object:
        del input_state, kwargs
        self.last_simulation_backend = backend
        self.simulation_backends.append(backend)
        if rng is None:
            warnings.warn(
                "Default random-number generator is used. Results may not be reproducible.",
                UserWarning,
                stacklevel=2,
            )
            self.last_rng_sample = None
        else:
            self.last_rng_sample = int(rng.integers(0, 10_000))
        return FakeSimulationResult(backend=backend, rng_sample=self.last_rng_sample)

    def __iter__(self) -> Iterator[object]:
        return iter(self.compiled_commands)


@dataclass(slots=True)
class FakePatternWithoutCopy:
    operations: list[str] = field(default_factory=list)

    def standardize(self) -> None:
        self.operations.append("standardize")

    def shift_signals(self) -> None:
        self.operations.append("shift_signals")

    def perform_pauli_measurements(self) -> None:
        self.operations.append("perform_pauli_measurements")


@dataclass(slots=True)
class FakePatternWithoutStandardize:
    operations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FakePatternReturningInvalidPatternLike:
    compiled_commands: tuple[object, ...] = ()

    def standardize(self) -> StrangeIterablePatternLike:
        return StrangeIterablePatternLike()


@dataclass(slots=True)
class StrangeIterablePatternLike:
    payload: tuple[object, ...] = ()

    def __iter__(self) -> Iterator[object]:
        return iter(self.payload)

    def copy(self) -> None:
        return None

    def standardize(self) -> None:
        return None

    def shift_signals(self) -> None:
        return None


@dataclass(slots=True)
class FakePatternWithoutSimulate:
    compiled_commands: tuple[object, ...] = ()

    def copy(self) -> FakePatternWithoutSimulate:
        return FakePatternWithoutSimulate(compiled_commands=tuple(self.compiled_commands))

    def standardize(self) -> None:
        return None

    def shift_signals(self) -> dict[int, set[int]]:
        return {}

    def perform_pauli_measurements(self) -> None:
        return None

    def __iter__(self) -> Iterator[object]:
        return iter(self.compiled_commands)


@dataclass(slots=True)
class FakePatternWithBackendOutcomes(FakePattern):
    failing_backends: frozenset[str] = frozenset()
    warnings_by_backend: dict[str, str] = field(default_factory=dict)

    def simulate_pattern(
        self,
        backend: str = "statevector",
        input_state: object | None = None,
        rng: np.random.Generator | None = None,
        **kwargs: object,
    ) -> object:
        del input_state, kwargs
        self.last_simulation_backend = backend
        self.simulation_backends.append(backend)
        warning_message = self.warnings_by_backend.get(backend)
        if warning_message is not None:
            warnings.warn(warning_message, UserWarning, stacklevel=2)
        if backend in self.failing_backends:
            raise RuntimeError(f"{backend} backend failed")
        return super(FakePatternWithBackendOutcomes, self).simulate_pattern(
            backend=backend, rng=rng
        )


@dataclass(frozen=True, slots=True)
class FakeFlow:
    correction_function: dict[int, set[int]]


@dataclass(slots=True)
class FakePatternWithFlow(FakePattern):
    flow_correction_function: dict[int, set[int]] = field(default_factory=dict)

    def extract_causal_flow(self) -> FakeFlow:
        return FakeFlow(correction_function=self.flow_correction_function)


@dataclass(frozen=True, slots=True)
class FakeFlowWithoutCorrectionFunction:
    label: str = "missing-correction-function"


@dataclass(slots=True)
class FakePatternWithBrokenCausalFlowAndWorkingGFlow(FakePattern):
    gflow_correction_function: dict[int, set[int]] = field(default_factory=dict)

    def extract_causal_flow(self) -> FakeFlowWithoutCorrectionFunction:
        return FakeFlowWithoutCorrectionFunction()

    def extract_gflow(self) -> FakeFlow:
        return FakeFlow(correction_function=self.gflow_correction_function)


@dataclass(slots=True)
class FakePatternWithDrawGraph(FakePattern):
    draw_graph_calls: list[bool] = field(default_factory=list)

    def draw_graph(self, flow_from_pattern: bool = True, **kwargs: object) -> None:
        del kwargs
        self.draw_graph_calls.append(flow_from_pattern)
        plt.figure()


@dataclass(slots=True)
class FakeTranspileResult:
    pattern: object


@dataclass(frozen=True, slots=True)
class FakeSimulationResult:
    backend: str
    rng_sample: int | None = None


class FakeCommandKind(Enum):
    N = auto()
    E = auto()
    M = auto()
    X = auto()
    Z = auto()
    C = auto()


class FakePlane(Enum):
    XY = auto()
    YZ = auto()
    XZ = auto()


@dataclass(frozen=True, slots=True)
class FakeMeasurement:
    angle: float
    plane: FakePlane


@dataclass(frozen=True, slots=True)
class FakeNCommand:
    node: int
    kind: ClassVar[FakeCommandKind] = FakeCommandKind.N


@dataclass(frozen=True, slots=True)
class FakeECommand:
    nodes: tuple[int, int]
    kind: ClassVar[FakeCommandKind] = FakeCommandKind.E


@dataclass(frozen=True, slots=True)
class FakeMeasurementCommand:
    node: int
    measurement: FakeMeasurement
    s_domain: set[int] = field(default_factory=set)
    t_domain: set[int] = field(default_factory=set)
    kind: ClassVar[FakeCommandKind] = FakeCommandKind.M


@dataclass(frozen=True, slots=True)
class FakeDirectMeasurementCommand:
    node: int
    angle: float
    plane: FakePlane
    s_domain: set[int] = field(default_factory=set)
    t_domain: set[int] = field(default_factory=set)
    kind: ClassVar[FakeCommandKind] = FakeCommandKind.M


@dataclass(frozen=True, slots=True)
class FakeXCommand:
    node: int
    domain: set[int] = field(default_factory=set)
    kind: ClassVar[FakeCommandKind] = FakeCommandKind.X


@dataclass(frozen=True, slots=True)
class FakeZCommand:
    node: int
    domain: set[int] = field(default_factory=set)
    kind: ClassVar[FakeCommandKind] = FakeCommandKind.Z


@dataclass(frozen=True, slots=True)
class FakeClifford:
    label: str


@dataclass(frozen=True, slots=True)
class FakeCCommand:
    node: int
    clifford: FakeClifford
    kind: ClassVar[FakeCommandKind] = FakeCommandKind.C


@dataclass(frozen=True, slots=True)
class FakeUnknownCommand:
    payload: str


class FakeGraphixCircuit:
    def __init__(self, width: int) -> None:
        self.width = width
        self.pattern = FakePattern(compiled_commands=_build_compiled_commands(width))

    def h(self, q: int) -> None:
        del q

    def cnot(self, control: int, target: int) -> None:
        del control, target

    def transpile(self) -> FakeTranspileResult:
        return FakeTranspileResult(pattern=self.pattern)


class FakePatternSimulator:
    last_backend: ClassVar[str | None] = None
    last_rng_sample: ClassVar[int | None] = None

    def __init__(self, pattern: object, backend: str = "statevector", **kwargs: object) -> None:
        del pattern, kwargs
        self.selected_backend = backend
        self.backend = SimpleNamespace(state=None)

    def run(
        self,
        input_state: object | None = None,
        rng: np.random.Generator | None = None,
        **kwargs: object,
    ) -> None:
        del input_state, kwargs
        FakePatternSimulator.last_backend = self.selected_backend
        if rng is None:
            warnings.warn(
                "Default random-number generator is used. Results may not be reproducible.",
                UserWarning,
                stacklevel=2,
            )
            FakePatternSimulator.last_rng_sample = None
        else:
            FakePatternSimulator.last_rng_sample = int(rng.integers(0, 10_000))
        self.backend.state = FakeSimulationResult(
            backend=self.selected_backend,
            rng_sample=FakePatternSimulator.last_rng_sample,
        )


def _build_compiled_commands(width: int) -> tuple[object, ...]:
    if width == 1:
        return (
            FakeNCommand(node=1),
            FakeMeasurementCommand(
                node=0,
                measurement=FakeMeasurement(angle=0.5, plane=FakePlane.XY),
                s_domain={1},
            ),
            FakeXCommand(node=1, domain={0}),
        )
    if width == 2:
        return (
            FakeNCommand(node=2),
            FakeECommand(nodes=(0, 2)),
            FakeDirectMeasurementCommand(
                node=0,
                angle=-0.25,
                plane=FakePlane.XZ,
                t_domain={2},
            ),
            FakeZCommand(node=2, domain={0, 1}),
            FakeCCommand(node=2, clifford=FakeClifford(label="H")),
        )
    return ()


def _install_fake_graphix(
    monkeypatch: pytest.MonkeyPatch,
    *,
    supported_backends: tuple[str, ...] = ("statevector",),
) -> None:
    fake_graphix = cast(
        ModuleType,
        SimpleNamespace(Circuit=FakeGraphixCircuit, Pattern=FakePattern),
    )
    fake_simulator_module = cast(
        ModuleType,
        SimpleNamespace(PatternSimulator=FakePatternSimulator),
    )
    fake_modules: dict[str, ModuleType] = {
        "graphix": fake_graphix,
        "graphix.simulator": fake_simulator_module,
    }
    backend_modules: dict[str, tuple[str, ModuleType]] = {
        "statevector": (
            "graphix.sim.statevec",
            cast(ModuleType, SimpleNamespace(StatevectorBackend=object)),
        ),
        "densitymatrix": (
            "graphix.sim.density_matrix",
            cast(ModuleType, SimpleNamespace(DensityMatrixBackend=object)),
        ),
        "tensornetwork": (
            "graphix.sim.tensornet",
            cast(ModuleType, SimpleNamespace(TensorNetworkBackend=object)),
        ),
        "mps": (
            "graphix.sim.mps",
            cast(ModuleType, SimpleNamespace(MPSBackend=object)),
        ),
    }
    for backend in supported_backends:
        module_name, module = backend_modules[backend]
        fake_modules[module_name] = module

    def fake_import_module(module_name: str) -> ModuleType:
        if module_name in fake_modules:
            return fake_modules[module_name]
        raise ModuleNotFoundError(name=module_name)

    monkeypatch.setattr(graphix_runtime_module, "import_module", fake_import_module)


def _unwrap_graphix_pattern(lab_pattern: LabPattern) -> FakePattern:
    return cast(FakePattern, lab_pattern.to_graphix())


def _compiled_graphix_commands(lab_pattern: LabPattern) -> tuple[object, ...]:
    return tuple(_unwrap_graphix_pattern(lab_pattern))


def _expected_rng_sample(seed: int) -> int:
    return int(np.random.default_rng(seed).integers(0, 10_000))


def test_lab_pattern_wraps_compiled_graphix_pattern_and_supports_chaining(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(2).h(0).cnot(0, 1).compile()

    chained_result = lab_pattern.standardize().shift_signals().perform_pauli_measurements()

    assert isinstance(lab_pattern, LabPattern)
    assert chained_result is lab_pattern
    assert _unwrap_graphix_pattern(lab_pattern).operations == [
        "standardize",
        "shift_signals",
        "perform_pauli_measurements",
    ]


def test_lab_pattern_shift_signals_keeps_wrapped_pattern_when_graphix_returns_signal_map() -> None:
    graphix_pattern = FakePattern(
        compiled_commands=(
            FakeNCommand(node=2),
            FakeECommand(nodes=(0, 2)),
            FakeMeasurementCommand(
                node=0,
                measurement=FakeMeasurement(angle=0.5, plane=FakePlane.XY),
                s_domain={2},
            ),
            FakeXCommand(node=2, domain={0}),
        )
    )
    lab_pattern = from_graphix_pattern(graphix_pattern)

    shifted_pattern = lab_pattern.shift_signals()

    assert shifted_pattern is lab_pattern
    assert shifted_pattern.to_graphix() is graphix_pattern
    assert shifted_pattern.commands() == (
        CommandRecord(
            index=0,
            kind="N",
            node=2,
            nodes=(2,),
            raw=repr(graphix_pattern.compiled_commands[0]),
        ),
        CommandRecord(
            index=1,
            kind="E",
            nodes=(0, 2),
            raw=repr(graphix_pattern.compiled_commands[1]),
        ),
        CommandRecord(
            index=2,
            kind="M",
            node=0,
            nodes=(0,),
            angle=0.5,
            plane="XY",
            s_domain=(2,),
            raw=repr(graphix_pattern.compiled_commands[2]),
        ),
        CommandRecord(
            index=3,
            kind="X",
            node=2,
            nodes=(2,),
            domain=(0,),
            raw=repr(graphix_pattern.compiled_commands[3]),
        ),
    )


def test_lab_pattern_copy_wraps_graphix_copy_result() -> None:
    graphix_pattern = FakePattern(label="source")
    lab_pattern = from_graphix_pattern(graphix_pattern)

    copied_pattern = lab_pattern.copy()

    assert isinstance(copied_pattern, LabPattern)
    assert copied_pattern is not lab_pattern
    assert graphix_pattern.copy_calls == 1
    assert copied_pattern.to_graphix() is not graphix_pattern
    assert _unwrap_graphix_pattern(copied_pattern).label == "source-copy"


def test_lab_pattern_copy_raises_clear_error_when_graphix_copy_is_unavailable() -> None:
    lab_pattern = from_graphix_pattern(FakePatternWithoutCopy())

    with pytest.raises(GraphixCompatibilityError, match=r"Pattern\.copy"):
        lab_pattern.copy()


def test_lab_pattern_raises_clear_error_when_graphix_method_is_missing() -> None:
    lab_pattern = from_graphix_pattern(FakePatternWithoutStandardize())

    with pytest.raises(GraphixCompatibilityError, match=r"Pattern\.standardize"):
        lab_pattern.standardize()


def test_lab_pattern_commands_reject_plain_iterables_that_are_not_graphix_patterns() -> None:
    lab_pattern = from_graphix_pattern("abc")

    with pytest.raises(
        GraphixCompatibilityError,
        match=r"could not iterate over to inspect its command sequence",
    ):
        lab_pattern.commands()


def test_lab_pattern_standardize_rejects_invalid_pattern_like_return_values() -> None:
    lab_pattern = from_graphix_pattern(FakePatternReturningInvalidPatternLike())

    with pytest.raises(GraphixCompatibilityError, match=r"Pattern\.standardize"):
        lab_pattern.standardize()


def test_lab_pattern_commands_normalize_one_qubit_compiled_pattern(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(1).h(0).compile()
    graphix_commands = _compiled_graphix_commands(lab_pattern)

    assert lab_pattern.commands() == (
        CommandRecord(
            index=0,
            kind="N",
            node=1,
            nodes=(1,),
            raw=repr(graphix_commands[0]),
        ),
        CommandRecord(
            index=1,
            kind="M",
            node=0,
            nodes=(0,),
            angle=0.5,
            plane="XY",
            s_domain=(1,),
            raw=repr(graphix_commands[1]),
        ),
        CommandRecord(
            index=2,
            kind="X",
            node=1,
            nodes=(1,),
            domain=(0,),
            raw=repr(graphix_commands[2]),
        ),
    )


def test_lab_pattern_commands_normalize_two_qubit_compiled_pattern(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(2).h(0).cnot(0, 1).compile()
    graphix_commands = _compiled_graphix_commands(lab_pattern)

    assert lab_pattern.commands() == (
        CommandRecord(
            index=0,
            kind="N",
            node=2,
            nodes=(2,),
            raw=repr(graphix_commands[0]),
        ),
        CommandRecord(
            index=1,
            kind="E",
            nodes=(0, 2),
            raw=repr(graphix_commands[1]),
        ),
        CommandRecord(
            index=2,
            kind="M",
            node=0,
            nodes=(0,),
            angle=-0.25,
            plane="XZ",
            t_domain=(2,),
            raw=repr(graphix_commands[2]),
        ),
        CommandRecord(
            index=3,
            kind="Z",
            node=2,
            nodes=(2,),
            domain=(0, 1),
            raw=repr(graphix_commands[3]),
        ),
        CommandRecord(
            index=4,
            kind="C",
            node=2,
            nodes=(2,),
            raw=repr(graphix_commands[4]),
        ),
    )


def test_lab_pattern_commands_fall_back_for_unknown_graphix_command_objects() -> None:
    unknown_command = FakeUnknownCommand(payload="opaque")
    lab_pattern = from_graphix_pattern(FakePattern(compiled_commands=(unknown_command,)))

    commands = lab_pattern.commands()

    assert len(commands) == 1
    assert commands[0].index == 0
    assert commands[0].kind == "UNKNOWN"
    assert commands[0].raw == repr(unknown_command)


def test_lab_pattern_summary_reports_structural_counts_for_one_qubit_pattern(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(1).h(0).compile()
    summary = lab_pattern.summary()

    assert summary == PatternSummary(
        command_count=3,
        node_count=2,
        input_nodes=(0,),
        output_nodes=(1,),
        measurement_count=1,
        command_kinds=("N", "M", "X"),
        entanglement_edge_count=0,
        x_correction_count=1,
        z_correction_count=0,
    )
    assert str(summary) == (
        "PatternSummary(commands=3, kinds=(N, M, X), nodes=2, measurements=1, "
        "entanglement_edges=0, x_corrections=1, z_corrections=0, inputs=(0,), "
        "outputs=(1,))"
    )


def test_lab_pattern_resources_report_detectable_inputs_outputs_and_corrections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(2).h(0).cnot(0, 1).compile()

    assert lab_pattern.resources() == ResourceSummary(
        command_count=5,
        command_counts=(("N", 1), ("E", 1), ("M", 1), ("Z", 1), ("C", 1)),
        node_count=2,
        edge_count=1,
        measurement_count=1,
        x_correction_count=0,
        z_correction_count=1,
        input_nodes=(0,),
        output_nodes=(2,),
    )


def test_lab_pattern_explain_returns_concise_structural_description(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(2).h(0).cnot(0, 1).compile()

    assert lab_pattern.explain() == (
        "Pattern with 5 commands across 2 nodes.\n"
        "Command kinds: N, E, M, Z, C.\n"
        "Measurements: 1 | entanglement edges: 1 | X corrections: 0 | Z corrections: 1.\n"
        "Detected input nodes: 0.\n"
        "Detected output nodes: 2."
    )


def test_lab_pattern_trace_builds_a_standalone_syntactic_trace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(1).h(0).compile()

    trace = lab_pattern.trace()

    assert isinstance(trace, RunTrace)
    assert len(trace.frames) == 3
    assert trace.frames[0].step == 0
    assert trace.frames[0].command_kind == "N"
    assert trace.frames[0].node == 1
    assert trace.frames[0].nodes == (1,)
    assert trace.frames[0].measured_nodes == frozenset()
    assert trace.frames[0].active_nodes == frozenset({1})
    assert trace.frames[0].pending_nodes == frozenset({0, 1})
    assert trace.frames[0].corrections == ()
    assert trace.frames[0].description == "Prepare node 1."

    assert trace.frames[1].step == 1
    assert trace.frames[1].command_kind == "M"
    assert trace.frames[1].node == 0
    assert trace.frames[1].measured_nodes == frozenset({0})
    assert trace.frames[1].active_nodes == frozenset({1})
    assert trace.frames[1].pending_nodes == frozenset({1})
    assert trace.frames[1].description == (
        "Measure node 0 in plane XY at angle 0.5. "
        "This frame reflects the conceptual command state after applying the measurement."
    )

    assert trace.frames[2].step == 2
    assert trace.frames[2].command_kind == "X"
    assert trace.frames[2].corrections == (
        "X correction on node 1 depends on the measurement outcome of node 0.",
    )
    assert trace.frames[2].description == (
        "Apply the X byproduct correction on node 1, conditioned on the measurement "
        "outcome of node 0."
    )


def test_lab_pattern_trace_reports_multi_node_correction_dependencies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(2).h(0).cnot(0, 1).compile()

    trace = lab_pattern.trace()

    assert trace.frames[3].command_kind == "Z"
    assert trace.frames[3].corrections == (
        "Z correction on node 2 depends on measurement outcomes of nodes 0, 1.",
    )
    assert trace.frames[3].description == (
        "Apply the Z byproduct correction on node 2, conditioned on measurement "
        "outcomes of nodes 0, 1."
    )


def test_build_visualization_model_extracts_nodes_edges_and_dependencies() -> None:
    commands = (
        CommandRecord(index=0, kind="N", node=2, nodes=(2,), raw="N(2)"),
        CommandRecord(index=1, kind="E", nodes=(0, 2), raw="E(0,2)"),
        CommandRecord(
            index=2,
            kind="M",
            node=0,
            nodes=(0,),
            plane="XY",
            s_domain=(2,),
            t_domain=(3,),
            raw="M(0)",
        ),
        CommandRecord(index=3, kind="X", node=2, nodes=(2,), domain=(0,), raw="X(2)"),
        CommandRecord(index=4, kind="Z", node=3, nodes=(3,), domain=(0, 2), raw="Z(3)"),
    )

    model = build_visualization_model(commands)

    assert model.nodes == (0, 2, 3)
    assert model.edges == ((0, 2),)
    assert model.measured_nodes == frozenset({0})
    assert model.input_nodes == (0, 3)
    assert model.output_nodes == (2, 3)
    assert {(edge.source, edge.target, edge.label) for edge in model.correction_dependencies} == {
        (2, 0, "s"),
        (3, 0, "t"),
        (0, 2, "X"),
        (0, 3, "Z"),
        (2, 3, "Z"),
    }


def test_build_visualization_model_adds_optional_flow_dependencies() -> None:
    commands = (
        CommandRecord(index=0, kind="N", node=2, nodes=(2,), raw="N(2)"),
        CommandRecord(index=1, kind="E", nodes=(0, 2), raw="E(0,2)"),
        CommandRecord(index=2, kind="M", node=0, nodes=(0,), plane="XY", raw="M(0)"),
    )
    graphix_pattern = FakePatternWithFlow(
        compiled_commands=commands,
        flow_correction_function={0: {2}},
    )

    model = build_visualization_model(commands, pattern=graphix_pattern, show_flow=True)

    assert model.flow_dependencies == ((0, 2),)


def test_build_visualization_model_falls_back_to_gflow_when_causal_flow_is_not_usable() -> None:
    commands = (
        CommandRecord(index=0, kind="N", node=2, nodes=(2,), raw="N(2)"),
        CommandRecord(index=1, kind="E", nodes=(0, 2), raw="E(0,2)"),
        CommandRecord(index=2, kind="M", node=0, nodes=(0,), plane="XY", raw="M(0)"),
    )
    graphix_pattern = FakePatternWithBrokenCausalFlowAndWorkingGFlow(
        compiled_commands=commands,
        gflow_correction_function={0: {2}},
    )

    model = build_visualization_model(commands, pattern=graphix_pattern, show_flow=True)

    assert model.flow_dependencies == ((0, 2),)


def test_trace_and_visualization_collect_all_related_command_nodes() -> None:
    command = CommandRecord(
        index=0,
        kind="X",
        node=5,
        nodes=(1, 2),
        s_domain=(3,),
        t_domain=(4,),
        domain=(6,),
        raw="X(5)",
    )

    trace = build_syntactic_trace((command,))
    model = build_visualization_model((command,))

    assert trace.frames[0].pending_nodes == frozenset({1, 2, 3, 4, 5, 6})
    assert model.nodes == (1, 2, 3, 4, 5, 6)


def test_build_syntactic_trace_gracefully_handles_malformed_entanglement_commands() -> None:
    trace = build_syntactic_trace((CommandRecord(index=0, kind="E", nodes=(1,), raw="E(1)"),))

    assert trace.frames[0].command_kind == "E"
    assert trace.frames[0].label == "E"
    assert trace.frames[0].description == "E(1)"


def test_lab_pattern_draw_returns_headless_matplotlib_figure() -> None:
    lab_pattern = from_graphix_pattern(
        FakePattern(
            compiled_commands=(
                FakeNCommand(node=2),
                FakeECommand(nodes=(0, 2)),
                FakeMeasurementCommand(
                    node=0,
                    measurement=FakeMeasurement(angle=0.5, plane=FakePlane.XY),
                    s_domain={2},
                ),
                FakeXCommand(node=2, domain={0}),
            )
        )
    )

    figure = lab_pattern.draw(show_flow=False, show_corrections=True, layout="shell")
    figure_without_corrections = lab_pattern.draw(
        show_flow=False,
        show_corrections=False,
        layout="shell",
    )

    assert isinstance(figure, Figure)
    assert len(figure.axes) == 1
    assert {"0", "2", "s", "X"}.issubset({text.get_text() for text in figure.axes[0].texts})
    assert "s" not in {text.get_text() for text in figure_without_corrections.axes[0].texts}
    assert "X" not in {text.get_text() for text in figure_without_corrections.axes[0].texts}

    plt.close(figure)
    plt.close(figure_without_corrections)


def test_lab_pattern_draw_can_delegate_to_graphix_renderer() -> None:
    graphix_pattern = FakePatternWithDrawGraph(
        compiled_commands=(
            FakeNCommand(node=2),
            FakeECommand(nodes=(0, 2)),
            FakeMeasurementCommand(
                node=0,
                measurement=FakeMeasurement(angle=0.5, plane=FakePlane.XY),
            ),
        )
    )
    lab_pattern = from_graphix_pattern(graphix_pattern)

    figure = lab_pattern.draw(show_flow=False, delegate_to_graphix=True)

    assert isinstance(figure, Figure)
    assert graphix_pattern.draw_graph_calls == [False]

    plt.close(figure)


def test_lab_pattern_animate_returns_slider_handle_and_updates_trace_view() -> None:
    lab_pattern = from_graphix_pattern(
        FakePattern(
            compiled_commands=(
                FakeNCommand(node=2),
                FakeECommand(nodes=(0, 2)),
                FakeMeasurementCommand(
                    node=0,
                    measurement=FakeMeasurement(angle=0.5, plane=FakePlane.XY),
                    s_domain={2},
                ),
                FakeXCommand(node=2, domain={0}),
            )
        )
    )

    handle = lab_pattern.animate(show_flow=False, show_corrections=True, layout="shell")

    assert isinstance(handle, TraceAnimationHandle)
    assert isinstance(handle.figure, Figure)
    assert handle.trace == lab_pattern.trace()
    assert handle.slider.valmin == 0
    assert handle.slider.valmax == len(handle.trace.frames) - 1
    assert callable(handle.update)
    assert "Step 0 of 3" in handle.graph_axes.get_title()
    assert "Prepare node 2." in handle.description_text.get_text()

    handle.slider.set_val(3)

    node_collection = next(
        collection
        for collection in handle.graph_axes.collections
        if isinstance(collection, PathCollection)
    )
    facecolors = {to_hex(color).lower() for color in cast(Any, node_collection).get_facecolors()}

    assert "Step 3 of 3" in handle.graph_axes.get_title()
    assert "Apply the X byproduct correction on node 2" in handle.description_text.get_text()
    assert _NODE_FILL_CURRENT.lower() in facecolors
    assert _NODE_FILL_MEASURED.lower() in facecolors

    plt.close(handle.figure)


def test_lab_pattern_animate_gracefully_handles_empty_patterns() -> None:
    lab_pattern = from_graphix_pattern(FakePattern(compiled_commands=()))

    handle = lab_pattern.animate(show_flow=False)

    assert isinstance(handle, TraceAnimationHandle)
    assert handle.trace.frames == ()
    assert "No trace frames are available" in handle.graph_axes.get_title()
    assert "No MBQC commands were available to visualize." in {
        text.get_text() for text in handle.graph_axes.texts
    }

    plt.close(handle.figure)


def test_lab_pattern_run_returns_simulation_report_from_pattern_simulate_pattern(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    FakePatternSimulator.last_backend = None
    FakePatternSimulator.last_rng_sample = None

    lab_pattern = circuit(1).h(0).compile()

    report = lab_pattern.run(backend="statevector", seed=123)

    assert isinstance(report, SimulationReport)
    assert report.backend == "statevector"
    assert report.seed == 123
    assert report.elapsed_time_seconds >= 0.0
    assert report.result_type == "FakeSimulationResult"
    assert report.notes == ()
    assert report.trace is None
    assert report.result == FakeSimulationResult(
        backend="statevector",
        rng_sample=_expected_rng_sample(123),
    )
    assert _unwrap_graphix_pattern(lab_pattern).last_simulation_backend == "statevector"
    assert FakePatternSimulator.last_backend is None


def test_lab_pattern_run_falls_back_to_pattern_simulator_and_builds_trace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)
    FakePatternSimulator.last_backend = None
    FakePatternSimulator.last_rng_sample = None

    lab_pattern = from_graphix_pattern(
        FakePatternWithoutSimulate(compiled_commands=_build_compiled_commands(1))
    )

    report = lab_pattern.run(backend="statevector", seed=123, trace=True)

    assert report.result == FakeSimulationResult(
        backend="statevector",
        rng_sample=_expected_rng_sample(123),
    )
    assert report.result_type == "FakeSimulationResult"
    assert FakePatternSimulator.last_backend == "statevector"
    assert FakePatternSimulator.last_rng_sample == _expected_rng_sample(123)
    assert report.trace is not None
    assert report.trace == lab_pattern.trace()


def test_lab_pattern_compare_backends_uses_detected_supported_backends(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch, supported_backends=("statevector", "densitymatrix"))

    lab_pattern = circuit(1).h(0).compile()

    report = lab_pattern.compare_backends(seed=123)

    assert isinstance(report, BackendComparisonReport)
    assert tuple(run.backend for run in report.runs) == ("statevector", "densitymatrix")
    assert all(run.success for run in report.runs)
    assert all(run.error_message is None for run in report.runs)
    assert all(run.result_type == "FakeSimulationResult" for run in report.runs)
    assert all(run.notes == () for run in report.runs)
    assert _unwrap_graphix_pattern(lab_pattern).simulation_backends == [
        "statevector",
        "densitymatrix",
    ]


def test_lab_pattern_compare_backends_records_failures_without_aborting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch, supported_backends=("statevector", "densitymatrix"))
    lab_pattern = from_graphix_pattern(
        FakePatternWithBackendOutcomes(
            failing_backends=frozenset({"densitymatrix"}),
            warnings_by_backend={"densitymatrix": "densitymatrix warning"},
        )
    )

    report = lab_pattern.compare_backends(
        backends=("densitymatrix", "mps", "statevector"),
        seed=123,
    )

    assert tuple(run.backend for run in report.runs) == ("densitymatrix", "mps", "statevector")
    assert report.runs[0].success is False
    assert report.runs[0].result_type is None
    assert report.runs[0].error_message == "densitymatrix backend failed"
    assert report.runs[0].notes == ("densitymatrix warning",)
    assert report.runs[1].success is False
    assert report.runs[1].error_message is not None
    assert "Supported backends: statevector, densitymatrix" in report.runs[1].error_message
    assert report.runs[2].success is True
    assert report.runs[2].result_type == "FakeSimulationResult"


def test_lab_pattern_compare_backends_accepts_a_single_backend_string(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch, supported_backends=("statevector", "densitymatrix"))

    lab_pattern = circuit(1).h(0).compile()

    report = lab_pattern.compare_backends(backends="statevector", seed=123)

    assert tuple(run.backend for run in report.runs) == ("statevector",)
    assert report.runs[0].success is True
    assert _unwrap_graphix_pattern(lab_pattern).simulation_backends == ["statevector"]


def test_lab_pattern_run_raises_clear_error_for_unsupported_backends(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_graphix(monkeypatch)

    lab_pattern = circuit(1).h(0).compile()

    with pytest.raises(UnsupportedBackendError, match="Supported backends: statevector"):
        lab_pattern.run(backend="densitymatrix")
