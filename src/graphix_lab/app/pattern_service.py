from __future__ import annotations

from graphix_lab.domain.errors import GraphixCompatibilityError
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
    updated_pattern = graphix_method()
    if updated_pattern is None:
        return pattern
    return updated_pattern


def _build_missing_pattern_method_message(feature_name: str) -> str:
    return f"The installed Graphix runtime does not expose {feature_name}() on pattern objects."
