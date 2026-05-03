from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from ..domain.commands import CommandRecord, _iter_command_nodes
from ..domain.summaries import PatternSummary, ResourceSummary

_KNOWN_COMMAND_KIND_ORDER: tuple[str, ...] = ("N", "E", "M", "X", "Z", "C", "UNKNOWN")


def build_pattern_summary(
    commands: Sequence[CommandRecord],
    *,
    resources: ResourceSummary | None = None,
) -> PatternSummary:
    resource_summary = resources or build_resource_summary(commands)
    command_kinds = tuple(kind for kind, _ in resource_summary.command_counts)
    return PatternSummary(
        command_count=resource_summary.command_count,
        node_count=resource_summary.node_count,
        input_nodes=resource_summary.input_nodes,
        output_nodes=resource_summary.output_nodes,
        measurement_count=resource_summary.measurement_count,
        command_kinds=command_kinds,
        entanglement_edge_count=resource_summary.edge_count,
        x_correction_count=resource_summary.x_correction_count,
        z_correction_count=resource_summary.z_correction_count,
    )


def build_resource_summary(commands: Sequence[CommandRecord]) -> ResourceSummary:
    ordered_command_counts = _build_command_counts(commands)
    seen_nodes = _collect_seen_nodes(commands)
    prepared_nodes = _collect_nodes_by_kind(commands, command_kind="N")
    measured_nodes = _collect_nodes_by_kind(commands, command_kind="M")

    command_count = len(commands)
    measurement_count = _command_count_for_kind(ordered_command_counts, command_kind="M")
    x_correction_count = _command_count_for_kind(ordered_command_counts, command_kind="X")
    z_correction_count = _command_count_for_kind(ordered_command_counts, command_kind="Z")

    return ResourceSummary(
        command_count=command_count,
        command_counts=ordered_command_counts,
        node_count=len(seen_nodes),
        edge_count=_command_count_for_kind(ordered_command_counts, command_kind="E"),
        measurement_count=measurement_count,
        x_correction_count=x_correction_count,
        z_correction_count=z_correction_count,
        input_nodes=tuple(sorted(seen_nodes - prepared_nodes)),
        output_nodes=tuple(sorted(seen_nodes - measured_nodes)),
    )


def build_pattern_explanation(
    summary: PatternSummary,
    *,
    resources: ResourceSummary | None = None,
) -> str:
    resource_summary = resources or ResourceSummary(
        command_count=summary.command_count,
        command_counts=tuple((kind, 1) for kind in summary.command_kinds),
        node_count=summary.node_count,
        edge_count=summary.entanglement_edge_count,
        measurement_count=summary.measurement_count,
        x_correction_count=summary.x_correction_count,
        z_correction_count=summary.z_correction_count,
        input_nodes=summary.input_nodes,
        output_nodes=summary.output_nodes,
    )
    return "\n".join(
        (
            f"Pattern with {summary.command_count} commands across {summary.node_count} nodes.",
            f"Command kinds: {_format_command_kinds(summary.command_kinds)}.",
            (
                f"Measurements: {summary.measurement_count} | "
                f"entanglement edges: {summary.entanglement_edge_count} | "
                f"X corrections: {summary.x_correction_count} | "
                f"Z corrections: {summary.z_correction_count}."
            ),
            f"Detected input nodes: {_format_nodes(resource_summary.input_nodes)}.",
            f"Detected output nodes: {_format_nodes(resource_summary.output_nodes)}.",
        )
    )


def _build_command_counts(commands: Sequence[CommandRecord]) -> tuple[tuple[str, int], ...]:
    command_counter = Counter(command.kind for command in commands)
    ordered_command_kinds = _ordered_command_kinds(command_counter)
    return tuple(
        (command_kind, command_counter[command_kind]) for command_kind in ordered_command_kinds
    )


def _ordered_command_kinds(command_counter: Counter[str]) -> tuple[str, ...]:
    known_command_kinds = [
        command_kind
        for command_kind in _KNOWN_COMMAND_KIND_ORDER
        if command_counter[command_kind] > 0
    ]
    extra_command_kinds = sorted(
        command_kind
        for command_kind in command_counter
        if command_kind not in _KNOWN_COMMAND_KIND_ORDER
    )
    return (*known_command_kinds, *extra_command_kinds)


def _command_count_for_kind(
    command_counts: Sequence[tuple[str, int]],
    *,
    command_kind: str,
) -> int:
    for seen_command_kind, count in command_counts:
        if seen_command_kind == command_kind:
            return count
    return 0


def _collect_seen_nodes(commands: Sequence[CommandRecord]) -> set[int]:
    seen_nodes: set[int] = set()
    for command in commands:
        seen_nodes.update(_iter_command_nodes(command))
    return seen_nodes


def _collect_nodes_by_kind(
    commands: Sequence[CommandRecord],
    *,
    command_kind: str,
) -> set[int]:
    nodes: set[int] = set()
    for command in commands:
        if command.kind != command_kind:
            continue
        nodes.update(_iter_command_nodes(command))
    return nodes


def _format_command_kinds(command_kinds: Sequence[str]) -> str:
    if not command_kinds:
        return "none"
    return ", ".join(command_kinds)


def _format_nodes(nodes: Sequence[int]) -> str:
    if not nodes:
        return "none detected"
    return ", ".join(str(node) for node in nodes)
