from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PatternSummary:
    command_count: int
    node_count: int
    input_nodes: tuple[int, ...] = ()
    output_nodes: tuple[int, ...] = ()
    measurement_count: int = 0
    command_kinds: tuple[str, ...] = ()
    entanglement_edge_count: int = 0
    x_correction_count: int = 0
    z_correction_count: int = 0

    def __str__(self) -> str:
        return (
            "PatternSummary("
            f"commands={self.command_count}, "
            f"kinds={_format_command_kinds(self.command_kinds)}, "
            f"nodes={self.node_count}, "
            f"measurements={self.measurement_count}, "
            f"entanglement_edges={self.entanglement_edge_count}, "
            f"x_corrections={self.x_correction_count}, "
            f"z_corrections={self.z_correction_count}, "
            f"inputs={self.input_nodes}, "
            f"outputs={self.output_nodes}"
            ")"
        )


@dataclass(frozen=True, slots=True)
class ResourceSummary:
    command_count: int
    command_counts: tuple[tuple[str, int], ...]
    node_count: int
    edge_count: int
    measurement_count: int
    x_correction_count: int
    z_correction_count: int
    input_nodes: tuple[int, ...] = ()
    output_nodes: tuple[int, ...] = ()

    def __str__(self) -> str:
        return (
            "ResourceSummary("
            f"commands={self.command_count}, "
            f"command_counts={self.command_counts}, "
            f"nodes={self.node_count}, "
            f"edges={self.edge_count}, "
            f"measurements={self.measurement_count}, "
            f"x_corrections={self.x_correction_count}, "
            f"z_corrections={self.z_correction_count}, "
            f"inputs={self.input_nodes}, "
            f"outputs={self.output_nodes}"
            ")"
        )


def _format_command_kinds(command_kinds: tuple[str, ...]) -> str:
    if not command_kinds:
        return "()"
    return "(" + ", ".join(command_kinds) + ")"
