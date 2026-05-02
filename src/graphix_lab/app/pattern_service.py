from __future__ import annotations

from collections.abc import Callable
from typing import cast

from graphix_lab.domain.errors import GraphixCompatibilityError


def copy_graphix_pattern(pattern: object) -> object:
    graphix_copy = _require_graphix_pattern_method(
        pattern,
        "copy",
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
    graphix_method = _require_graphix_pattern_method(pattern, method_name)
    updated_pattern = graphix_method()
    if updated_pattern is None:
        return pattern
    return updated_pattern


def _require_graphix_pattern_method(
    pattern: object,
    method_name: str,
    *,
    missing_message: str | None = None,
) -> Callable[[], object]:
    graphix_method = getattr(pattern, method_name, None)
    if callable(graphix_method):
        return cast(Callable[[], object], graphix_method)

    feature_name = f"Pattern.{method_name}"
    raise GraphixCompatibilityError(
        feature=feature_name,
        message=missing_message
        or (f"The installed Graphix runtime does not expose {feature_name}() on pattern objects."),
    )
