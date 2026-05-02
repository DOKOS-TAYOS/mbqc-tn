from __future__ import annotations

from collections.abc import Iterable


class GraphixLabError(Exception):
    """Base error for Graphix Lab domain failures."""


class GraphixUnavailableError(GraphixLabError):
    """Raised when Graphix is not available in the active environment."""

    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message
            or (
                "Graphix is not installed in the active environment. "
                "Install the project dependencies inside .venv before using Graphix Lab runtime "
                "features."
            )
        )


class GraphixCompatibilityError(GraphixLabError):
    """Raised when the installed Graphix API is incompatible with Graphix Lab."""

    def __init__(self, feature: str | None = None, message: str | None = None) -> None:
        self.feature = feature
        detail = message or "The installed Graphix version is incompatible with Graphix Lab."
        if feature is not None and message is None:
            detail = f"{detail} Missing or incompatible API: {feature}."
        super().__init__(detail)


class UnsupportedBackendError(GraphixLabError):
    """Raised when a requested simulation backend is not supported."""

    def __init__(self, backend: str, supported_backends: Iterable[str] = ()) -> None:
        self.backend = backend
        self.supported_backends = tuple(supported_backends)

        if self.supported_backends:
            supported_display = ", ".join(self.supported_backends)
            message = (
                f"Backend {backend!r} is not supported by the installed Graphix runtime. "
                f"Supported backends: {supported_display}."
            )
        else:
            message = (
                f"Backend {backend!r} is not supported by the installed Graphix runtime, and "
                "no compatible built-in backends were detected."
            )

        super().__init__(message)


class OptionalDependencyError(GraphixLabError):
    """Raised when an optional dependency required by a feature is missing."""

    def __init__(
        self,
        dependency: str,
        feature: str | None = None,
        message: str | None = None,
    ) -> None:
        self.dependency = dependency
        self.feature = feature

        if message is None:
            feature_detail = f" for {feature}" if feature is not None else ""
            message = (
                f"Optional dependency {dependency!r} is required{feature_detail}. "
                f"Install {dependency!r} in the active environment and try again."
            )

        super().__init__(message)


class UnsupportedGateError(GraphixLabError):
    """Raised when an input circuit contains a gate Graphix Lab does not handle."""

    def __init__(
        self,
        gate_name: str,
        gate_index: int | None = None,
        message: str | None = None,
    ) -> None:
        self.gate_name = gate_name
        self.gate_index = gate_index

        if message is None:
            if gate_index is None:
                message = f"Gate {gate_name!r} is not supported by Graphix Lab."
            else:
                message = (
                    f"Gate {gate_name!r} at instruction index {gate_index} is not supported by "
                    "Graphix Lab."
                )

        super().__init__(message)
