from __future__ import annotations

from dataclasses import dataclass, field
from types import ModuleType, SimpleNamespace
from typing import cast

import pytest

import graphix_lab.infrastructure.graphix_adapter as graphix_adapter_module
from graphix_lab import LabPattern, circuit, from_graphix_pattern
from graphix_lab.domain.errors import GraphixCompatibilityError


@dataclass(slots=True)
class FakePattern:
    label: str = "compiled-pattern"
    operations: list[str] = field(default_factory=list)
    copy_calls: int = 0

    def copy(self) -> FakePattern:
        self.copy_calls += 1
        return FakePattern(
            label=f"{self.label}-copy",
            operations=list(self.operations),
        )

    def standardize(self) -> None:
        self.operations.append("standardize")

    def shift_signals(self) -> None:
        self.operations.append("shift_signals")

    def perform_pauli_measurements(self) -> None:
        self.operations.append("perform_pauli_measurements")


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


class FakeGraphixCircuit:
    def __init__(self, width: int) -> None:
        self.width = width
        self.pattern = FakePattern()

    def h(self, q: int) -> None:
        del q

    def cnot(self, control: int, target: int) -> None:
        del control, target

    def transpile(self) -> FakeTranspileResult:
        return FakeTranspileResult(pattern=self.pattern)


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
