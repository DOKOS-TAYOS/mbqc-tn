from __future__ import annotations

from types import ModuleType

import pytest

import graphix_lab.infrastructure.graphix_runtime as graphix_runtime_module
from graphix_lab.domain.errors import GraphixCompatibilityError, GraphixUnavailableError


class _FakeTarget:
    def standardize(self) -> str:
        return "ok"


def test_require_graphix_callable_returns_existing_callable() -> None:
    graphix_method = graphix_runtime_module.require_graphix_callable(
        _FakeTarget(),
        "standardize",
        feature_name="Pattern.standardize",
    )

    assert graphix_method() == "ok"


def test_require_graphix_callable_raises_default_compatibility_error() -> None:
    with pytest.raises(GraphixCompatibilityError, match=r"Pattern\.standardize") as error_info:
        graphix_runtime_module.require_graphix_callable(
            object(),
            "standardize",
            feature_name="Pattern.standardize",
        )

    assert error_info.value.feature == "Pattern.standardize"


def test_require_graphix_callable_preserves_custom_missing_message() -> None:
    with pytest.raises(GraphixCompatibilityError, match="custom Graphix message") as error_info:
        graphix_runtime_module.require_graphix_callable(
            object(),
            "copy",
            feature_name="Pattern.copy",
            missing_message="custom Graphix message",
        )

    assert error_info.value.feature == "Pattern.copy"


def test_optional_import_module_returns_none_for_missing_module(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_import_module(module_name: str) -> ModuleType:
        raise ModuleNotFoundError(name=module_name)

    monkeypatch.setattr(graphix_runtime_module, "import_module", fake_import_module)

    assert graphix_runtime_module.optional_import_module("graphix.missing") is None


def test_import_graphix_root_raises_graphix_unavailable_when_graphix_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_import_module(module_name: str) -> ModuleType:
        raise ModuleNotFoundError(name=module_name)

    monkeypatch.setattr(graphix_runtime_module, "import_module", fake_import_module)

    with pytest.raises(GraphixUnavailableError, match="Graphix is not installed"):
        graphix_runtime_module.import_graphix_root()


def test_import_graphix_root_raises_compatibility_error_for_missing_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_import_module(module_name: str) -> ModuleType:
        del module_name
        raise ModuleNotFoundError(name="numpy")

    monkeypatch.setattr(graphix_runtime_module, "import_module", fake_import_module)

    with pytest.raises(GraphixCompatibilityError, match="numpy"):
        graphix_runtime_module.import_graphix_root()
