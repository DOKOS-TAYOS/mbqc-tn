# Public API Contract

The public surface is the top-level `graphix_lab` package.

## Top-Level Imports

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

## Constructors

- `circuit(width: int) -> LabCircuit`
- `from_graphix_pattern(pattern: object) -> LabPattern`
- `from_qiskit(qc: object, *, angle_units: str = "radians") -> LabCircuit`
- `graphix_info() -> GraphixCapabilities`

## `LabCircuit`

Current fluent methods:

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

Angle units are explicit:

- `pi` means Graphix-style pi units
- `radians` are converted by dividing by `math.pi`
- any other unit raises `ValueError`

## `LabPattern`

Current wrapped-pattern methods:

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
.draw(...) -> matplotlib.figure.Figure
.animate(...) -> TraceAnimationHandle
.run(...) -> SimulationReport
.compare_backends(...) -> BackendComparisonReport
```

Mutation helpers update the wrapped Graphix pattern and return the same
`LabPattern`.

`commands()` currently gives named adapters for `N`, `E`, `M`, `X`, `Z`, and
`C`. Unrecognized runtime command objects still surface through
`CommandRecord(kind="UNKNOWN", raw=...)` so users can inspect them without
crashing.

## Result Objects

The summary, trace, simulation, and comparison objects are public frozen
dataclasses with readable string forms. They are designed to be script-friendly
and test-friendly rather than notebook-only.
