from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from types import ModuleType
from typing import cast

from graphix_lab.domain.errors import GraphixCompatibilityError, GraphixUnavailableError


def import_graphix_root() -> ModuleType:
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


def optional_import_module(module_name: str) -> ModuleType | None:
    try:
        return import_module(module_name)
    except ModuleNotFoundError:
        return None
    except Exception:  # pragma: no cover - defensive fallback
        return None


def require_graphix_callable(
    target: object,
    attribute_name: str,
    *,
    feature_name: str,
    missing_message: str | None = None,
) -> Callable[..., object]:
    graphix_method = getattr(target, attribute_name, None)
    if callable(graphix_method):
        return cast(Callable[..., object], graphix_method)

    raise GraphixCompatibilityError(
        feature=feature_name,
        message=missing_message,
    )
