# Visualization And Trace Specification

## Goals

Visualization should help users understand an MBQC pattern without exposing
internal tensor data.

## Static Visualization

`LabPattern.draw(...)` currently returns a headless-safe
`matplotlib.figure.Figure`.

The local renderer builds its graph from normalized `CommandRecord` objects and
can highlight:

- input and output nodes
- measured nodes
- entanglement edges from `E` commands
- dependency arrows from `s_domain`, `t_domain`, and explicit `X` / `Z`
  correction domains
- optional flow overlays when the wrapped Graphix pattern exposes extractable
  flow or gflow data

`delegate_to_graphix=True` is an explicit opt-in when callers want to try
Graphix's own `draw_graph()` path first.

## Trace Model

A lightweight syntactic trace is enough for the MVP.

```python
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
```

```python
@dataclass(frozen=True, slots=True)
class RunTrace:
    frames: tuple[TraceFrame, ...]
```

Each frame describes the state immediately after its command.

## Slider Animation

`LabPattern.animate(...)` currently returns `TraceAnimationHandle`.

That handle keeps the figure, graph axes, slider axes, slider widget,
description text, generated trace, and update callback alive so interactive
Matplotlib state is not lost.

The current script example is `examples/trace_slider.py`.

The animation helper should:

- create a static figure
- update the title and description when the slider changes
- highlight the current command node or nodes
- restyle measured versus pending nodes
- avoid Jupyter-specific APIs
- stay compatible with headless test runs
- degrade gracefully when no graph can be extracted
