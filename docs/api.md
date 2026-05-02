# API Overview

## Public Python API

Graphix Lab now exposes its public domain model plus the first live Graphix
wrapper entrypoints.

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
    TraceFrame,
    circuit,
    from_graphix_pattern,
    from_qiskit,
    graphix_info,
)
```

### Stable domain models

- `CommandRecord`
- `PatternSummary`
- `ResourceSummary`
- `TraceFrame`
- `RunTrace`
- `SimulationReport`
- `BackendRunReport`
- `BackendComparisonReport`

All of these are frozen dataclasses with typed fields so later prompts can build
command summaries, traces, simulation reports, and backend comparisons on top
of a stable contract.

### Wrapper entrypoints

### `circuit(width: int) -> LabCircuit`

Creates a `LabCircuit` fluent wrapper that delegates gate construction to
`graphix.Circuit`.

Supported methods in this prompt:

- `.h(q)`
- `.x(q)`
- `.y(q)`
- `.z(q)`
- `.s(q)`
- `.rx(q, angle, units="pi")`
- `.ry(q, angle, units="pi")`
- `.rz(q, angle, units="pi")`
- `.cnot(control, target)`
- `.compile()`
- `.to_graphix()`

Rotation angles are explicit:

- `units="pi"` passes the numeric value through as Graphix Lab's public
  pi-scaled convention.
- `units="radians"` converts the numeric angle by dividing by `math.pi` before
  delegating.
- Any other unit raises a clear `ValueError`.

`compile()` wraps `circuit.transpile().pattern` in `LabPattern`, and
`to_graphix()` returns the wrapped Graphix circuit object.

### `from_graphix_pattern(pattern: object) -> LabPattern`

Wraps a raw Graphix pattern object in `LabPattern`. In this prompt,
`to_graphix()` remains the only live pattern method; higher-level pattern
operations arrive later.

### `from_qiskit(qc: object, *, angle_units: str = "radians") -> LabCircuit`

Reserved public entrypoint for the later Qiskit adapter. It currently raises a
clear `NotImplementedError` instead of pretending the adapter exists.

### `graphix_info() -> GraphixCapabilities`

Returns a `GraphixCapabilities` snapshot for the active Graphix runtime.

If Graphix is not installed in the active `.venv`, this function raises a clear
domain error instead of failing with a raw import error.

## Public CLI

- `bootstrap`
- `quality`
- `test`
- `clean`
- `licenses`

### CLI behavior notes

- `bootstrap` is for a fresh template copy only. Once `bootstrap_required` becomes `False`, the command exits with an error instead of prompting again.
- `quality` runs Ruff, pytest, and pyright through the active interpreter, which keeps `.venv` resolution consistent on Windows and Linux.
- `test` runs pytest through the active interpreter.
- `clean` removes caches and temporary artifacts, but stays conservative around `.venv`, `.git`, and inaccessible subtrees.
- `licenses` regenerates `THIRD_PARTY_LICENSES` from the active interpreter and excludes the local template package.

Treat everything outside `src/graphix_lab/__init__.py` and the CLI subcommands as internal implementation detail.
