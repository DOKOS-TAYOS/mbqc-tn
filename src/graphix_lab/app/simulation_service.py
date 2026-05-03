from __future__ import annotations

import inspect
import time
import warnings
from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np

from ..domain.commands import CommandRecord, _collect_command_related_nodes
from ..domain.errors import GraphixCompatibilityError, UnsupportedBackendError
from ..domain.simulation import BackendComparisonReport, BackendRunReport, SimulationReport
from ..domain.traces import RunTrace, TraceFrame
from ..infrastructure.graphix_adapter import extract_command_records
from ..infrastructure.graphix_capabilities import _detect_supported_backends
from ..infrastructure.graphix_runtime import import_graphix_root, optional_import_module


@dataclass(frozen=True, slots=True)
class _BackendAttempt:
    elapsed_time_seconds: float
    result: object | None
    notes: tuple[str, ...]
    error: Exception | None = None


def run_graphix_pattern(
    pattern: object,
    *,
    backend: str,
    seed: int | None = None,
    trace: bool = False,
) -> SimulationReport:
    supported_backends = _runtime_supported_backends()
    if backend not in supported_backends:
        raise UnsupportedBackendError(backend, supported_backends)

    trace_report = trace_graphix_pattern(pattern) if trace else None
    attempt = _attempt_graphix_backend_run(
        pattern,
        backend=backend,
        seed=seed,
    )
    if attempt.error is not None:
        raise attempt.error

    return SimulationReport(
        backend=backend,
        elapsed_time_seconds=attempt.elapsed_time_seconds,
        result=attempt.result,
        result_type=type(attempt.result).__name__ if attempt.result is not None else "NoneType",
        seed=seed,
        notes=attempt.notes,
        trace=trace_report,
    )


def compare_graphix_backends(
    pattern: object,
    *,
    backends: str | Sequence[str] | None = None,
    seed: int | None = None,
) -> BackendComparisonReport:
    supported_backends = _runtime_supported_backends()
    selected_backends = _normalize_requested_backends(
        backends,
        supported_backends=supported_backends,
    )
    runs = tuple(
        _compare_backend_run(
            pattern,
            backend=backend,
            seed=seed,
            supported_backends=supported_backends,
        )
        for backend in selected_backends
    )
    return BackendComparisonReport(runs=runs)


def _runtime_supported_backends() -> tuple[str, ...]:
    graphix_module = import_graphix_root()
    simulator_module = optional_import_module("graphix.simulator")
    return _detect_supported_backends(graphix_module, simulator_module)


def _normalize_requested_backends(
    backends: str | Sequence[str] | None,
    *,
    supported_backends: Sequence[str],
) -> tuple[str, ...]:
    if backends is None:
        return tuple(supported_backends)
    if isinstance(backends, str):
        return (backends,)
    return tuple(backends)


def trace_graphix_pattern(pattern: object) -> RunTrace:
    return build_syntactic_trace(extract_command_records(pattern))


def build_syntactic_trace(commands: Sequence[CommandRecord]) -> RunTrace:
    all_nodes = _collect_trace_nodes(commands)
    seen_nodes: set[int] = set()
    measured_nodes: set[int] = set()
    frames: list[TraceFrame] = []

    for command in commands:
        seen_nodes.update(command.nodes)
        frame_measured_nodes = set(measured_nodes)
        if command.kind == "M" and command.node is not None:
            frame_measured_nodes.add(command.node)

        # Frames represent the conceptual state immediately after each command,
        # so measurement frames already include their node in measured_nodes.
        active_nodes = frozenset(seen_nodes - frame_measured_nodes)
        frames.append(
            TraceFrame(
                step=command.index,
                command_kind=command.kind,
                label=_build_trace_label(command),
                node=command.node,
                nodes=command.nodes,
                measured_nodes=frozenset(frame_measured_nodes),
                active_nodes=active_nodes,
                pending_nodes=frozenset(all_nodes - frame_measured_nodes),
                corrections=_build_trace_corrections(command),
                description=_build_trace_description(command),
            )
        )
        measured_nodes = frame_measured_nodes

    return RunTrace(frames=tuple(frames))


def _run_graphix_simulation(
    pattern: object,
    *,
    backend: str,
    rng: np.random.Generator | None,
    seed: int | None,
    notes: list[str],
) -> object | None:
    simulate_pattern = getattr(pattern, "simulate_pattern", None)
    if callable(simulate_pattern):
        return _run_via_pattern_method(
            simulate_pattern,
            backend=backend,
            rng=rng,
            seed=seed,
            notes=notes,
        )

    return _run_via_pattern_simulator(
        pattern,
        backend=backend,
        rng=rng,
        seed=seed,
        notes=notes,
    )


def _compare_backend_run(
    pattern: object,
    *,
    backend: str,
    seed: int | None,
    supported_backends: Sequence[str],
) -> BackendRunReport:
    if backend not in supported_backends:
        error = UnsupportedBackendError(backend, supported_backends)
        return BackendRunReport(
            backend=backend,
            success=False,
            elapsed_time_seconds=0.0,
            result_type=None,
            error_message=str(error),
            notes=(),
        )

    attempt = _attempt_graphix_backend_run(
        pattern,
        backend=backend,
        seed=seed,
    )
    if attempt.error is not None:
        return BackendRunReport(
            backend=backend,
            success=False,
            elapsed_time_seconds=attempt.elapsed_time_seconds,
            result_type=None,
            error_message=str(attempt.error),
            notes=attempt.notes,
        )

    return BackendRunReport(
        backend=backend,
        success=True,
        elapsed_time_seconds=attempt.elapsed_time_seconds,
        result_type=type(attempt.result).__name__ if attempt.result is not None else "NoneType",
        error_message=None,
        notes=attempt.notes,
    )


def _attempt_graphix_backend_run(
    pattern: object,
    *,
    backend: str,
    seed: int | None,
) -> _BackendAttempt:
    notes: list[str] = []
    rng = np.random.default_rng(seed) if seed is not None else None
    result: object | None = None
    error: Exception | None = None

    start_time = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        try:
            result = _run_graphix_simulation(
                pattern,
                backend=backend,
                rng=rng,
                seed=seed,
                notes=notes,
            )
        except Exception as caught_error:  # pragma: no cover - exercised via caller behavior
            error = caught_error
    elapsed_time_seconds = time.perf_counter() - start_time

    notes.extend(_warning_messages(caught_warnings))
    return _BackendAttempt(
        elapsed_time_seconds=elapsed_time_seconds,
        result=result,
        notes=tuple(notes),
        error=error,
    )


def _run_via_pattern_method(
    simulate_pattern: Callable[..., object],
    *,
    backend: str,
    rng: np.random.Generator | None,
    seed: int | None,
    notes: list[str],
) -> object:
    simulation_kwargs: dict[str, object] = {"backend": backend}
    if rng is not None:
        if _callable_accepts_keyword(simulate_pattern, "rng"):
            simulation_kwargs["rng"] = rng
        else:
            notes.append(_build_seed_unsupported_note(seed, call_target="Pattern.simulate_pattern"))

    return simulate_pattern(**simulation_kwargs)


def _run_via_pattern_simulator(
    pattern: object,
    *,
    backend: str,
    rng: np.random.Generator | None,
    seed: int | None,
    notes: list[str],
) -> object | None:
    simulator_module = optional_import_module("graphix.simulator")
    simulator_type = getattr(simulator_module, "PatternSimulator", None)
    if not callable(simulator_type):
        raise GraphixCompatibilityError(
            feature="Pattern.simulate_pattern / graphix.simulator.PatternSimulator",
            message=(
                "The installed Graphix runtime does not expose Pattern.simulate_pattern() on "
                "pattern objects, and graphix.simulator.PatternSimulator is unavailable."
            ),
        )

    simulator = simulator_type(pattern, backend=backend)
    run_method = getattr(simulator, "run", None)
    if not callable(run_method):
        raise GraphixCompatibilityError(
            feature="PatternSimulator.run",
            message=(
                "The installed Graphix runtime exposed graphix.simulator.PatternSimulator, but "
                "the simulator instance does not provide a callable run() method."
            ),
        )

    run_kwargs: dict[str, object] = {}
    if rng is not None:
        if _callable_accepts_keyword(run_method, "rng"):
            run_kwargs["rng"] = rng
        else:
            notes.append(_build_seed_unsupported_note(seed, call_target="PatternSimulator.run"))

    run_method(**run_kwargs)

    backend_instance = getattr(simulator, "backend", None)
    if backend_instance is None or not hasattr(backend_instance, "state"):
        raise GraphixCompatibilityError(
            feature="PatternSimulator.backend.state",
            message=(
                "The installed Graphix runtime completed a PatternSimulator run, but Graphix "
                "Lab could not read the resulting backend state."
            ),
        )
    return backend_instance.state


def _callable_accepts_keyword(target: Callable[..., object], keyword: str) -> bool:
    try:
        signature = inspect.signature(target)
    except (TypeError, ValueError):
        return False

    for parameter in signature.parameters.values():
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            return True
        if parameter.name == keyword:
            return True
    return False


def _warning_messages(caught_warnings: Sequence[warnings.WarningMessage]) -> list[str]:
    messages: list[str] = []
    for warning_message in caught_warnings:
        message = str(warning_message.message).strip()
        if message:
            messages.append(message)
    return messages


def _build_seed_unsupported_note(seed: int | None, *, call_target: str) -> str:
    return (
        f"Seed {seed} could not be applied because the installed Graphix runtime does not "
        f"accept an rng keyword through {call_target}()."
    )


def _collect_trace_nodes(commands: Sequence[CommandRecord]) -> set[int]:
    nodes: set[int] = set()
    for command in commands:
        nodes.update(_collect_command_related_nodes(command))
    return nodes


def _build_trace_label(command: CommandRecord) -> str:
    if command.kind == "N" and command.node is not None:
        return f"Prepare node {command.node}"
    if command.kind == "E" and len(command.nodes) == 2:
        left_node, right_node = command.nodes
        return f"Entangle nodes {left_node} and {right_node}"
    if command.kind == "M" and command.node is not None:
        return f"Measure node {command.node}"
    if command.kind in {"X", "Z"} and command.node is not None:
        return f"Apply {command.kind} correction on node {command.node}"
    if command.kind == "C" and command.node is not None:
        return f"Apply Clifford on node {command.node}"
    if command.node is not None:
        return f"{command.kind} on node {command.node}"
    return command.kind


def _build_trace_corrections(command: CommandRecord) -> tuple[str, ...]:
    if command.kind not in {"X", "Z"} or command.node is None:
        return ()
    if not command.domain:
        return (
            f"{command.kind} correction on node {command.node} has no explicit "
            "measurement dependencies.",
        )
    dependency_subject = _format_dependency_subject(command.domain)
    return (f"{command.kind} correction on node {command.node} depends on {dependency_subject}.",)


def _build_trace_description(command: CommandRecord) -> str:
    if command.kind == "M":
        plane_text = command.plane or "unknown plane"
        angle_text = command.angle if command.angle is not None else "unknown angle"
        return (
            f"Measure node {command.node} in plane {plane_text} at angle {angle_text}. "
            "This frame reflects the conceptual command state after applying the measurement."
        )
    if command.kind == "E" and len(command.nodes) == 2:
        left_node, right_node = command.nodes
        return f"Create an entanglement edge between nodes {left_node} and {right_node}."
    if command.kind == "N" and command.node is not None:
        return f"Prepare node {command.node}."
    if command.kind in {"X", "Z"} and command.node is not None:
        if not command.domain:
            return (
                f"Apply the {command.kind} byproduct correction on node {command.node} "
                "with no explicit measurement dependency."
            )
        dependency_subject = _format_dependency_subject(command.domain)
        return (
            f"Apply the {command.kind} byproduct correction on node {command.node}, "
            f"conditioned on {dependency_subject}."
        )
    if command.kind == "C" and command.node is not None:
        return f"Apply a local Clifford operation on node {command.node}."
    return command.raw


def _format_dependency_subject(domain: tuple[int, ...]) -> str:
    domain_text = ", ".join(str(node) for node in domain)
    if len(domain) == 1:
        return f"the measurement outcome of node {domain_text}"
    return f"measurement outcomes of nodes {domain_text}"
