# Visualization and trace specification

## Goals

Visualization should help users understand an MBQC pattern. It does not need to expose internal tensor data.

## Static visualization

Use Matplotlib and NetworkX. Return the created `matplotlib.figure.Figure` so callers can save or customize it.

Recommended visual encodings:

- input nodes
- output nodes
- measured nodes
- pending nodes
- current command node
- entanglement edges
- correction dependencies
- optional flow/gflow arrows if Graphix exposes them

## Graphix visualization fallback

If Graphix provides a drawing method such as `draw_graph`, `draw_flow`, or `draw_xzcorrections`, Graphix Lab may delegate to it. If unavailable, it should fall back to a NetworkX graph built from command records.

## Trace model

A syntactic trace is sufficient for MVP.

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

## Slider animation

Use `matplotlib.widgets.Slider` for interactive inspection.

The animation helper should:

- create a static figure
- update node/edge labels when the slider changes
- not require Jupyter-specific APIs
- work in normal Matplotlib backends when possible
- degrade gracefully when no graph can be extracted

Return a small handle object that keeps references to the figure, axes, slider, and callback state to avoid garbage collection.
