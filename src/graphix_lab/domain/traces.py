from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.widgets import Slider


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


@dataclass(frozen=True, slots=True)
class TraceAnimationHandle:
    figure: Figure
    graph_axes: Axes
    slider_axes: Axes
    slider: Slider
    trace: RunTrace
    description_text: Text
    update: Callable[[int], None]
