from __future__ import annotations

import logging
import warnings
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import cast

import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from matplotlib.widgets import Slider

from ..domain.commands import CommandRecord, _collect_command_related_nodes
from ..domain.traces import TraceAnimationHandle, TraceFrame
from .simulation_service import build_syntactic_trace
from .summary_service import build_resource_summary

_SUPPORTED_LAYOUTS = frozenset({"auto", "circular", "kamada_kawai", "shell", "spring"})
_NODE_BORDER_COLOR = "#264653"
_ENTANGLEMENT_EDGE_COLOR = "#A0AAB4"
_FLOW_EDGE_COLOR = "#4C6A92"
_NODE_FILL_DEFAULT = "#D9D9D9"
_NODE_FILL_CURRENT = "#E9C46A"
_NODE_FILL_INPUT = "#7AA6C2"
_NODE_FILL_OUTPUT = "#69B3A2"
_NODE_FILL_MEASURED = "#F4A261"
_NODE_FILL_INPUT_OUTPUT = "#8EC8B6"
_ANIMATION_TEXT_BACKGROUND = "#F7F3E9"
_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source: int
    target: int
    label: str


@dataclass(frozen=True, slots=True)
class VisualizationModel:
    nodes: tuple[int, ...]
    edges: tuple[tuple[int, int], ...]
    measured_nodes: frozenset[int]
    input_nodes: tuple[int, ...]
    output_nodes: tuple[int, ...]
    correction_dependencies: tuple[DependencyEdge, ...]
    flow_dependencies: tuple[tuple[int, int], ...]


def draw_graphix_pattern(
    pattern: object,
    commands: Sequence[CommandRecord],
    *,
    show_flow: bool = True,
    show_corrections: bool = True,
    layout: str = "auto",
    ax: Axes | None = None,
    delegate_to_graphix: bool = False,
) -> Figure:
    if delegate_to_graphix and ax is None:
        delegated_figure = _delegate_draw_to_graphix(pattern, show_flow=show_flow)
        if delegated_figure is not None:
            return delegated_figure

    model = build_visualization_model(commands, pattern=pattern, show_flow=show_flow)
    return draw_visualization_model(
        model,
        show_corrections=show_corrections,
        layout=layout,
        ax=ax,
    )


def build_visualization_model(
    commands: Sequence[CommandRecord],
    *,
    pattern: object | None = None,
    show_flow: bool = True,
) -> VisualizationModel:
    all_nodes: set[int] = set()
    graph_edges: set[tuple[int, int]] = set()
    measured_nodes: set[int] = set()
    correction_dependencies: list[DependencyEdge] = []
    seen_dependencies: set[tuple[int, int, str]] = set()

    for command in commands:
        all_nodes.update(_collect_command_related_nodes(command))

        if command.kind == "E" and len(command.nodes) == 2:
            left_node, right_node = command.nodes
            graph_edges.add(_normalize_edge(left_node, right_node))

        if command.kind == "M" and command.node is not None:
            measured_nodes.add(command.node)
            for source_node in command.s_domain:
                _append_dependency(
                    correction_dependencies,
                    seen_dependencies,
                    source=source_node,
                    target=command.node,
                    label="s",
                )
            for source_node in command.t_domain:
                _append_dependency(
                    correction_dependencies,
                    seen_dependencies,
                    source=source_node,
                    target=command.node,
                    label="t",
                )

        if command.kind in {"X", "Z"} and command.node is not None:
            for source_node in command.domain:
                _append_dependency(
                    correction_dependencies,
                    seen_dependencies,
                    source=source_node,
                    target=command.node,
                    label=command.kind,
                )

    resource_summary = build_resource_summary(commands)
    if show_flow and pattern is not None:
        flow_dependencies = _extract_flow_dependencies(pattern)
    else:
        flow_dependencies = ()
    all_nodes.update(node for edge in flow_dependencies for node in edge)

    return VisualizationModel(
        nodes=tuple(sorted(all_nodes)),
        edges=tuple(sorted(graph_edges)),
        measured_nodes=frozenset(measured_nodes),
        input_nodes=resource_summary.input_nodes,
        output_nodes=resource_summary.output_nodes,
        correction_dependencies=tuple(
            sorted(correction_dependencies, key=lambda edge: (edge.source, edge.target, edge.label))
        ),
        flow_dependencies=tuple(sorted(flow_dependencies)),
    )


def animate_graphix_pattern_trace(
    pattern: object,
    commands: Sequence[CommandRecord],
    *,
    show_flow: bool = True,
    show_corrections: bool = True,
    layout: str = "auto",
) -> TraceAnimationHandle:
    trace = build_syntactic_trace(commands)
    model = build_visualization_model(commands, pattern=pattern, show_flow=show_flow)
    graph = _build_graph(model)
    positions = _resolve_layout_positions(graph, layout) if model.nodes else {}

    figure, graph_axes = plt.subplots(figsize=(8.2, 6.4))
    figure.subplots_adjust(bottom=0.22)
    slider_axes = figure.add_axes((0.18, 0.08, 0.64, 0.05))
    graph_axes.set_axis_off()

    node_collection = _draw_animation_graph(
        graph_axes,
        graph=graph,
        positions=positions,
        model=model,
        show_corrections=show_corrections,
    )
    description_text = graph_axes.text(
        0.02,
        0.02,
        "",
        transform=graph_axes.transAxes,
        ha="left",
        va="bottom",
        fontsize=9.5,
        wrap=True,
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": _ANIMATION_TEXT_BACKGROUND,
            "edgecolor": _NODE_BORDER_COLOR,
        },
    )

    frame_count = len(trace.frames)
    slider_max = max(frame_count - 1, 1)
    slider = Slider(
        ax=slider_axes,
        label="Step",
        valmin=0,
        valmax=slider_max,
        valinit=0,
        valstep=1,
        valfmt="%0.0f",
    )

    if frame_count <= 1:
        slider_axes.set_visible(False)

    def render_frame(frame_index: int) -> None:
        if frame_count == 0:
            graph_axes.set_title("Graphix Lab Trace Inspection | No trace frames are available")
            description_text.set_text(
                "No commands were recorded, so there is no step-by-step trace to inspect."
            )
            figure.canvas.draw_idle()
            return

        frame = trace.frames[frame_index]
        graph_axes.set_title(_build_animation_title(frame, last_index=frame_count - 1))
        if node_collection is not None:
            node_collection.set_facecolor(_frame_node_colors(model, frame))
            node_collection.set_sizes(_frame_node_sizes(model.nodes, frame))
            node_collection.set_linewidth(_frame_node_linewidths(model.nodes, frame))
        description_text.set_text(_build_animation_description(frame))
        figure.canvas.draw_idle()

    def on_slider_change(raw_value: float) -> None:
        render_frame(_clamp_frame_index(raw_value, frame_count))

    slider.on_changed(on_slider_change)

    def update(frame_index: int) -> None:
        clamped_index = _clamp_frame_index(frame_index, frame_count)
        if frame_count == 0:
            render_frame(clamped_index)
            return
        if round(slider.val) != clamped_index:
            slider.set_val(clamped_index)
            return
        render_frame(clamped_index)

    render_frame(0)

    return TraceAnimationHandle(
        figure=figure,
        graph_axes=graph_axes,
        slider_axes=slider_axes,
        slider=slider,
        trace=trace,
        description_text=description_text,
        update=update,
    )


def draw_visualization_model(
    model: VisualizationModel,
    *,
    show_corrections: bool = True,
    layout: str = "auto",
    ax: Axes | None = None,
) -> Figure:
    graph = _build_graph(model)

    if ax is None:
        figure, axes = plt.subplots(figsize=(7.5, 5.5))
    else:
        figure = cast(Figure, ax.figure)
        axes = ax
        axes.clear()

    axes.set_axis_off()
    axes.set_title("Graphix Lab MBQC Pattern")

    if not model.nodes:
        axes.text(
            0.5,
            0.5,
            "No MBQC commands were available to visualize.",
            ha="center",
            va="center",
            transform=axes.transAxes,
        )
        return figure

    positions = _resolve_layout_positions(graph, layout)

    nx.draw_networkx_edges(
        graph,
        positions,
        ax=axes,
        edge_color=_ENTANGLEMENT_EDGE_COLOR,
        width=1.8,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=axes,
        node_color=[
            _node_fill_color(
                node,
                measured_nodes=model.measured_nodes,
                input_nodes=model.input_nodes,
                output_nodes=model.output_nodes,
            )
            for node in model.nodes
        ],
        edgecolors=_NODE_BORDER_COLOR,
        linewidths=1.2,
        node_size=[780 if node in model.measured_nodes else 690 for node in model.nodes],
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        labels={node: str(node) for node in model.nodes},
        font_size=10,
        font_weight="bold",
        ax=axes,
    )

    if show_corrections:
        for dependency in model.correction_dependencies:
            _draw_dependency(
                axes,
                positions=positions,
                source=dependency.source,
                target=dependency.target,
                label=dependency.label,
            )

    for source_node, target_node in model.flow_dependencies:
        _draw_dependency(
            axes,
            positions=positions,
            source=source_node,
            target=target_node,
            label="flow",
            color=_FLOW_EDGE_COLOR,
            radius=0.05,
            draw_label=False,
            linestyle="-.",
        )

    return figure


def _build_graph(model: VisualizationModel) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(model.nodes)
    graph.add_edges_from(model.edges)
    return graph


def _draw_animation_graph(
    axes: Axes,
    *,
    graph: nx.Graph,
    positions: dict[int, tuple[float, float]],
    model: VisualizationModel,
    show_corrections: bool,
) -> PathCollection | None:
    axes.set_title("Graphix Lab Trace Inspection")

    if not model.nodes:
        axes.text(
            0.5,
            0.5,
            "No MBQC commands were available to visualize.",
            ha="center",
            va="center",
            transform=axes.transAxes,
        )
        return None

    nx.draw_networkx_edges(
        graph,
        positions,
        ax=axes,
        edge_color=_ENTANGLEMENT_EDGE_COLOR,
        width=1.8,
    )
    node_collection = cast(
        PathCollection,
        nx.draw_networkx_nodes(
            graph,
            positions,
            ax=axes,
            node_color=[
                _node_fill_color(
                    node,
                    measured_nodes=model.measured_nodes,
                    input_nodes=model.input_nodes,
                    output_nodes=model.output_nodes,
                )
                for node in model.nodes
            ],
            edgecolors=_NODE_BORDER_COLOR,
            linewidths=1.2,
            node_size=690,
        ),
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        labels={node: str(node) for node in model.nodes},
        font_size=10,
        font_weight="bold",
        ax=axes,
    )

    if show_corrections:
        for dependency in model.correction_dependencies:
            _draw_dependency(
                axes,
                positions=positions,
                source=dependency.source,
                target=dependency.target,
                label=dependency.label,
            )

    for source_node, target_node in model.flow_dependencies:
        _draw_dependency(
            axes,
            positions=positions,
            source=source_node,
            target=target_node,
            label="flow",
            color=_FLOW_EDGE_COLOR,
            radius=0.05,
            draw_label=False,
            linestyle="-.",
        )

    return node_collection


def _append_dependency(
    dependencies: list[DependencyEdge],
    seen_dependencies: set[tuple[int, int, str]],
    *,
    source: int,
    target: int,
    label: str,
) -> None:
    dependency_key = (source, target, label)
    if dependency_key in seen_dependencies:
        return
    seen_dependencies.add(dependency_key)
    dependencies.append(DependencyEdge(source=source, target=target, label=label))


def _normalize_edge(left_node: int, right_node: int) -> tuple[int, int]:
    if left_node <= right_node:
        return (left_node, right_node)
    return (right_node, left_node)


def _extract_flow_dependencies(pattern: object) -> tuple[tuple[int, int], ...]:
    for method_name in ("extract_causal_flow", "extract_gflow"):
        extract_flow = getattr(pattern, method_name, None)
        if not callable(extract_flow):
            continue
        try:
            flow = extract_flow()
        except Exception:
            _LOGGER.debug("Skipping unusable %s flow extraction.", method_name, exc_info=True)
            continue
        correction_function = getattr(flow, "correction_function", None)
        if not isinstance(correction_function, Mapping):
            continue
        return _coerce_flow_edges(correction_function)
    return ()


def _coerce_flow_edges(correction_function: object) -> tuple[tuple[int, int], ...]:
    if not isinstance(correction_function, Mapping):
        return ()

    flow_edges: set[tuple[int, int]] = set()
    for source_node, corrected_nodes in correction_function.items():
        if not isinstance(source_node, int):
            continue
        if not isinstance(corrected_nodes, Sequence | set | frozenset):
            continue
        for target_node in corrected_nodes:
            if isinstance(target_node, int):
                flow_edges.add((source_node, target_node))
    return tuple(sorted(flow_edges))


def _resolve_layout_positions(graph: nx.Graph, layout: str) -> dict[int, tuple[float, float]]:
    if layout not in _SUPPORTED_LAYOUTS:
        supported_layouts = ", ".join(sorted(_SUPPORTED_LAYOUTS))
        raise ValueError(f"Unsupported layout '{layout}'. Supported layouts: {supported_layouts}.")

    if layout == "auto":
        layout = "shell" if graph.number_of_nodes() <= 4 else "spring"

    if layout == "circular":
        raw_positions = nx.circular_layout(graph)
    elif layout == "kamada_kawai":
        raw_positions = nx.kamada_kawai_layout(graph)
    elif layout == "shell":
        raw_positions = nx.shell_layout(graph)
    else:
        raw_positions = nx.spring_layout(graph, seed=17)

    return {
        node: (float(position[0]), float(position[1])) for node, position in raw_positions.items()
    }


def _node_fill_color(
    node: int,
    *,
    measured_nodes: frozenset[int],
    input_nodes: tuple[int, ...],
    output_nodes: tuple[int, ...],
) -> str:
    input_node_set = set(input_nodes)
    output_node_set = set(output_nodes)
    if node in measured_nodes:
        return _NODE_FILL_MEASURED
    if node in input_node_set and node in output_node_set:
        return _NODE_FILL_INPUT_OUTPUT
    if node in input_node_set:
        return _NODE_FILL_INPUT
    if node in output_node_set:
        return _NODE_FILL_OUTPUT
    return _NODE_FILL_DEFAULT


def _build_animation_title(frame: TraceFrame, *, last_index: int) -> str:
    return f"Graphix Lab Trace Inspection | Step {frame.step} of {last_index} | {frame.label}"


def _build_animation_description(frame: TraceFrame) -> str:
    description_lines = [frame.label, frame.description]
    if frame.corrections:
        description_lines.append("Notes: " + " ".join(frame.corrections))
    return "\n".join(description_lines)


def _clamp_frame_index(value: float | int, frame_count: int) -> int:
    if frame_count <= 0:
        return 0
    return max(0, min(frame_count - 1, round(float(value))))


def _frame_node_colors(model: VisualizationModel, frame: TraceFrame) -> list[str]:
    current_nodes = _frame_current_nodes(frame)
    colors: list[str] = []
    for node in model.nodes:
        if node in current_nodes:
            colors.append(_NODE_FILL_CURRENT)
            continue
        if node in frame.measured_nodes:
            colors.append(_NODE_FILL_MEASURED)
            continue
        if node in frame.pending_nodes:
            colors.append(
                _node_fill_color(
                    node,
                    measured_nodes=frozenset(),
                    input_nodes=model.input_nodes,
                    output_nodes=model.output_nodes,
                )
            )
            continue
        colors.append(_NODE_FILL_DEFAULT)
    return colors


def _frame_node_sizes(nodes: tuple[int, ...], frame: TraceFrame) -> list[float]:
    current_nodes = _frame_current_nodes(frame)
    sizes: list[float] = []
    for node in nodes:
        if node in current_nodes:
            sizes.append(860.0)
            continue
        if node in frame.measured_nodes:
            sizes.append(780.0)
            continue
        sizes.append(690.0)
    return sizes


def _frame_node_linewidths(nodes: tuple[int, ...], frame: TraceFrame) -> list[float]:
    current_nodes = _frame_current_nodes(frame)
    linewidths: list[float] = []
    for node in nodes:
        if node in current_nodes:
            linewidths.append(2.4)
            continue
        if node in frame.measured_nodes:
            linewidths.append(1.5)
            continue
        linewidths.append(1.2)
    return linewidths


def _frame_current_nodes(frame: TraceFrame) -> frozenset[int]:
    current_nodes = set(frame.nodes)
    if frame.node is not None:
        current_nodes.add(frame.node)
    return frozenset(current_nodes)


def _draw_dependency(
    axes: Axes,
    *,
    positions: dict[int, tuple[float, float]],
    source: int,
    target: int,
    label: str,
    color: str | None = None,
    radius: float | None = None,
    draw_label: bool = True,
    linestyle: str = "--",
) -> None:
    if source not in positions or target not in positions:
        return

    edge_color = color or _dependency_color(label)
    edge_radius = radius if radius is not None else _dependency_radius(label)
    source_position = positions[source]
    target_position = positions[target]
    arrow = FancyArrowPatch(
        posA=source_position,
        posB=target_position,
        arrowstyle="-|>",
        mutation_scale=13,
        linewidth=1.4,
        color=edge_color,
        linestyle=linestyle,
        shrinkA=18,
        shrinkB=18,
        connectionstyle=f"arc3,rad={edge_radius}",
    )
    axes.add_patch(arrow)

    if not draw_label:
        return

    midpoint_x = (source_position[0] + target_position[0]) / 2
    midpoint_y = (source_position[1] + target_position[1]) / 2
    axes.text(
        midpoint_x,
        midpoint_y + (0.06 if edge_radius >= 0 else -0.06),
        label,
        color=edge_color,
        fontsize=9,
        fontweight="bold",
        ha="center",
        va="center",
    )


def _dependency_color(label: str) -> str:
    if label == "s":
        return "#E76F51"
    if label == "t":
        return "#D62828"
    if label == "X":
        return "#2A9D8F"
    if label == "Z":
        return "#577590"
    return _FLOW_EDGE_COLOR


def _dependency_radius(label: str) -> float:
    if label in {"s", "Z"}:
        return 0.18
    if label in {"t", "X"}:
        return -0.18
    return 0.08


def _delegate_draw_to_graphix(pattern: object, *, show_flow: bool) -> Figure | None:
    draw_graph = getattr(pattern, "draw_graph", None)
    if not callable(draw_graph):
        return None

    existing_figure_numbers = set(plt.get_fignums())
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="FigureCanvas.*non-interactive.*",
            category=UserWarning,
        )
        try:
            draw_graph(flow_from_pattern=show_flow)
        except Exception:
            return None

    new_figure_numbers = [
        figure_number
        for figure_number in plt.get_fignums()
        if figure_number not in existing_figure_numbers
    ]
    if new_figure_numbers:
        return cast(Figure, plt.figure(new_figure_numbers[-1]))
    if plt.get_fignums():
        return cast(Figure, plt.gcf())
    return None
