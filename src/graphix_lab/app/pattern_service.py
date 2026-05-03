from __future__ import annotations

from graphix_lab.domain.errors import GraphixCompatibilityError
from graphix_lab.infrastructure.graphix_adapter import _is_graphix_pattern_like
from graphix_lab.infrastructure.graphix_runtime import require_graphix_callable


def copy_graphix_pattern(pattern: object) -> object:
    graphix_copy = require_graphix_callable(
        pattern,
        "copy",
        feature_name="Pattern.copy",
        missing_message=(
            "The installed Graphix runtime does not expose Pattern.copy() on pattern objects. "
            "LabPattern mutates the wrapped Graphix pattern in place, so create a Graphix-side "
            "copy before wrapping if you need isolation."
        ),
    )
    copied_pattern = graphix_copy()
    if copied_pattern is None:
        raise GraphixCompatibilityError(
            feature="Pattern.copy",
            message=(
                "The installed Graphix runtime exposed Pattern.copy(), but it did not return a "
                "copied pattern object."
            ),
        )
    return copied_pattern


def apply_graphix_pattern_method(pattern: object, method_name: str) -> object:
    feature_name = f"Pattern.{method_name}"
    graphix_method = require_graphix_callable(
        pattern,
        method_name,
        feature_name=feature_name,
        missing_message=_build_missing_pattern_method_message(feature_name),
    )
    method_result = graphix_method()
    return _coerce_pattern_method_result(
        pattern,
        method_name=method_name,
        feature_name=feature_name,
        method_result=method_result,
    )


def _build_missing_pattern_method_message(feature_name: str) -> str:
    return f"The installed Graphix runtime does not expose {feature_name}() on pattern objects."


def _coerce_pattern_method_result(
    pattern: object,
    *,
    method_name: str,
    feature_name: str,
    method_result: object | None,
) -> object:
    if method_result is None:
        return pattern
    if _is_pattern_like(method_result) or isinstance(method_result, type(pattern)):
        return method_result
    if method_name == "shift_signals" and isinstance(method_result, dict):
        return pattern
    raise GraphixCompatibilityError(
        feature=feature_name,
        message=(
            f"The installed Graphix runtime exposed {feature_name}(), but it returned "
            f"{type(method_result).__name__} instead of mutating in place or returning a "
            "pattern object."
        ),
    )


def _is_pattern_like(value: object) -> bool:
    return _is_graphix_pattern_like(value)
