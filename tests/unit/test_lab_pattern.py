from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum, auto
from types import ModuleType, SimpleNamespace
from typing import ClassVar, cast

import pytest

import graphix_lab.infrastructure.graphix_adapter as graphix_adapter_module
from graphix_lab import CommandRecord, LabPattern, circuit, from_graphix_pattern
from graphix_lab.domain.errors import GraphixCompatibilityError


@dataclass(slots=True)
class FakePattern:
    label: str = "compiled-pattern"
    operations: list[str] = field(default_factory=list)
    copy_calls: int = 0
    compiled_commands: tuple[object, ...] = ()

    def copy(self) -> FakePattern:
        self.copy_calls += 1
        return FakePattern(
            label=f"{self.label}-copy",
            operations=list(self.operations),
            compiled_commands=tuple(self.compiled_commands),
        )

    def standardize(self) -> None:
        self.operations.append("standardize")

    def shift_signals(self) -> None:
        self.operations.append("shift_signals")

    def perform_pauli_measurements(self) -> None:
        self.operations.append("perform_pauli_measurements")

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
class FakeTranspileResult:
    pattern: object


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


def _unwrap_graphix_pattern(lab_pattern: LabPattern) -> FakePattern:
    return cast(FakePattern, lab_pattern.to_graphix())


def _compiled_graphix_commands(lab_pattern: LabPattern) -> tuple[object, ...]:
    return tuple(_unwrap_graphix_pattern(lab_pattern))


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
