from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TraceFrame:
    step: int
    command_kind: str
    label: str
    node: int | None
    nodes: tuple[int, ...]
    measured_nodes: frozenset[int]
    active_nodes: frozenset[int]
    pending_nodes: frozenset[int]
    corrections: tuple[str, ...]
    description: str


@dataclass(frozen=True, slots=True)
class RunTrace:
    frames: tuple[TraceFrame, ...] = ()
