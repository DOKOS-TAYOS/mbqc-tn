# Public API contract

## Top-level functions

```python
from graphix_lab import circuit, from_graphix_pattern, from_qiskit
```

### `circuit(width: int) -> LabCircuit`

Create a wrapper around `graphix.Circuit`.

### `from_graphix_pattern(pattern: object) -> LabPattern`

Wrap an existing Graphix pattern.

### `from_qiskit(qc: object, *, angle_units: str = "radians") -> LabCircuit`

Optional frontend. This function should raise a clear `OptionalDependencyError` when Qiskit is not installed.

## `LabCircuit`

Recommended methods:

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

Graphix rotation methods use angles in units of π. Graphix Lab should make this explicit and optionally convert from radians.

## `LabPattern`

Recommended methods:

```python
.to_graphix() -> object
.copy() -> LabPattern
.standardize() -> LabPattern
.shift_signals() -> LabPattern
.perform_pauli_measurements() -> LabPattern
.commands() -> tuple[CommandRecord, ...]
.summary() -> PatternSummary
.explain() -> str
.resources() -> ResourceSummary
.run(backend: str = "statevector", *, seed: int | None = None, trace: bool = False) -> SimulationReport
.trace() -> RunTrace
.draw(...) -> matplotlib.figure.Figure
.animate(...) -> object
```

Mutating Graphix operations should be wrapped carefully. If a Graphix method mutates in place, document whether the wrapper mutates in place or returns a copy.

## Result objects

Result objects should be typed dataclasses with predictable fields and readable `repr` output.

Avoid returning raw tuples when a named dataclass would be clearer.
