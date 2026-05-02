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

    def __str__(self) -> str:
        return (
            "PatternSummary("
            f"commands={self.command_count}, "
            f"nodes={self.node_count}, "
            f"measurements={self.measurement_count}"
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
            f"nodes={self.node_count}, "
            f"edges={self.edge_count}, "
            f"measurements={self.measurement_count}"
            ")"
        )
