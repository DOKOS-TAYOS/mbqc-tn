# API Overview

## Public Python API

```python
from graphix_lab import (
    BackendComparisonReport,
    BackendRunReport,
    CommandRecord,
    GraphixCapabilities,
    LabCircuit,
    LabPattern,
    PatternSummary,
    ResourceSummary,
    RunTrace,
    SimulationReport,
    TraceAnimationHandle,
    TraceFrame,
    circuit,
    from_graphix_pattern,
    from_qiskit,
    graphix_info,
)
```

Everything else should be treated as internal implementation detail.

## Frozen Public Data Models

The public report and trace objects are frozen dataclasses with typed fields:

- `CommandRecord`
- `PatternSummary`
- `ResourceSummary`
- `TraceFrame`
- `RunTrace`
- `SimulationReport`
- `BackendRunReport`
- `BackendComparisonReport`
- `TraceAnimationHandle`
- `GraphixCapabilities`

They are intended to be easy to print, compare, and pass between examples,
tests, and teaching notebooks later on.

## Top-Level Functions

### `circuit(width: int) -> LabCircuit`

Creates a live `LabCircuit` wrapper around `graphix.Circuit`.

- `width` must be a positive integer.
- The underlying Graphix circuit is created lazily the first time a gate is
  applied.

### `from_graphix_pattern(pattern: object) -> LabPattern`

Wraps an existing Graphix pattern object by reference.

### `from_qiskit(qc: object, *, angle_units: str = "radians") -> LabCircuit`

Imports a supported subset of Qiskit gates into a live `LabCircuit`.

- `qiskit` remains optional.
- If `qiskit` is missing from the active `.venv`, Graphix Lab raises
  `OptionalDependencyError`.
- Supported instructions are `h`, `x`, `y`, `z`, `s`, `rx`, `ry`, `rz`, and
  `cx` / `cnot`.
- Unsupported instructions raise `UnsupportedGateError` with the gate name and
  zero-based instruction index.
- Qubit numbering follows `QuantumCircuit.find_bit(...)`.

### `graphix_info() -> GraphixCapabilities`

Returns a snapshot of the active Graphix runtime capabilities.

## `LabCircuit`

`LabCircuit` is a small fluent wrapper. It mutates the underlying Graphix
circuit and returns `self` from its gate methods.

```python
.h(q: int) -> LabCircuit
.x(q: int) -> LabCircuit
.y(q: int) -> LabCircuit
.z(q: int) -> LabCircuit
.s(q: int) -> LabCircuit
.rx(q: int, angle: float, *, units: str = "pi") -> LabCircuit
.ry(q: int, angle: float, *, units: str = "pi") -> LabCircuit
.rz(q: int, angle: float, *, units: str = "pi") -> LabCircuit
.cnot(control: int, target: int) -> LabCircuit
.compile() -> LabPattern
.to_graphix() -> object
```

Angle handling is explicit:

- `units="pi"` passes the numeric value through as Graphix-style pi units.
- `units="radians"` converts by dividing by `math.pi`.
- Any other value raises `ValueError`.

## `LabPattern`

`LabPattern` wraps a Graphix pattern object and exposes the current educational
inspection surface:

```python
.to_graphix() -> object
.copy() -> LabPattern
.standardize() -> LabPattern
.shift_signals() -> LabPattern
.perform_pauli_measurements() -> LabPattern
.commands() -> tuple[CommandRecord, ...]
.summary() -> PatternSummary
.resources() -> ResourceSummary
.explain() -> str
.trace() -> RunTrace
.draw(
    *,
    show_flow: bool = True,
    show_corrections: bool = True,
    layout: str = "auto",
    ax: matplotlib.axes.Axes | None = None,
    delegate_to_graphix: bool = False,
) -> matplotlib.figure.Figure
.animate(
    *,
    show_flow: bool = True,
    show_corrections: bool = True,
    layout: str = "auto",
) -> TraceAnimationHandle
.run(
    backend: str = "statevector",
    *,
    seed: int | None = None,
    trace: bool = False,
) -> SimulationReport
.compare_backends(
    backends: collections.abc.Sequence[str] | None = None,
    *,
    seed: int | None = None,
) -> BackendComparisonReport
```

### Mutation Semantics

- `standardize()`, `shift_signals()`, and `perform_pauli_measurements()` update
  the wrapped Graphix pattern and return the same `LabPattern`.
- If Graphix returns a replacement pattern object instead of mutating in place,
  Graphix Lab keeps the wrapper aligned to that replacement.
- If Graphix returns auxiliary data while still mutating in place, as the real
  `Pattern.shift_signals()` currently does, Graphix Lab keeps the wrapper bound
  to the mutated pattern instead of replacing it with that auxiliary value.
- `copy()` requires runtime support for `Pattern.copy()`. When it is missing,
  Graphix Lab raises `GraphixCompatibilityError`.

### Command Normalization

`commands()` normalizes Graphix command objects into `CommandRecord` values with
these fields:

- `index`
- `kind`
- `node`
- `nodes`
- `angle`
- `plane`
- `s_domain`
- `t_domain`
- `domain`
- `raw`

The adapter currently recognizes `N`, `E`, `M`, `X`, `Z`, and `C` commands.
Unknown command objects are still returned as records with `kind="UNKNOWN"` and
their raw `repr(...)`. This matters in practice after some Graphix rewrites,
such as `shift_signals()`, because newer command shapes may not yet have a
named Graphix Lab adapter.

### Summaries And Explanations

- `summary()` returns the compact `PatternSummary` view.
- `resources()` returns the fuller `ResourceSummary`.
- `explain()` formats the same structural information into a readable,
  teaching-oriented multi-line string.

Input and output nodes are inferred conservatively from the normalized command
stream. These values are useful for quick inspection, but they are not a
replacement for deeper Graphix semantic analyses.

### Trace And Visualization

- `trace()` returns a standalone conceptual `RunTrace`.
- Each `TraceFrame` represents the state immediately after its command.
- `draw()` returns a headless-safe Matplotlib `Figure`.
- `animate()` returns a `TraceAnimationHandle` that keeps the figure, slider,
  description text, trace, and update callback alive for interactive use.

By default, the local renderer uses normalized `CommandRecord` objects with
NetworkX and Matplotlib. `delegate_to_graphix=True` opts into Graphix's own
drawer when that runtime path is available.

### Simulation

`run()` delegates execution to the active Graphix runtime.

- Graphix Lab prefers `Pattern.simulate_pattern()` when available.
- It falls back to `graphix.simulator.PatternSimulator` when needed.
- Backend names are validated against the detected Graphix runtime support.
- Unsupported names raise `UnsupportedBackendError`.
- When `trace=True`, the returned `SimulationReport` includes the same light
  conceptual trace model used by `.trace()`.

### Backend Comparison

`compare_backends()` runs the same wrapped pattern across a backend list and
returns `BackendComparisonReport`.

- If `backends=None`, Graphix Lab uses the detected supported backend order.
- Individual backend failures are recorded without aborting the whole report.
- `str(report)` renders a readable plain-text table for terminals and examples.

## Public CLI

- `bootstrap`
- `quality`
- `test`
- `clean`
- `licenses`

### CLI Notes

- `bootstrap` is only for fresh template copies, not for this already
  bootstrapped repository.
- `quality` runs Ruff, pytest, and pyright through the active interpreter.
- `test` runs pytest through the active interpreter.
- `clean` removes caches and temporary artifacts while staying conservative
  around `.venv`, `.git`, and inaccessible subtrees.
- `licenses` regenerates `THIRD_PARTY_LICENSES` from the active interpreter.
