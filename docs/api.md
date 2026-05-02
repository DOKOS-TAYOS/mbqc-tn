# API Overview

## Public Python API

Graphix Lab now exposes its public domain model plus live Graphix wrapper
entrypoints for circuits and patterns.

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

Wraps a raw Graphix pattern object in `LabPattern` by reference.

Available live pattern methods in this prompt:

- `.to_graphix()`
- `.copy()`
- `.standardize()`
- `.shift_signals()`
- `.perform_pauli_measurements()`
- `.commands()`

Mutation semantics are explicit:

- `standardize()`, `shift_signals()`, and `perform_pauli_measurements()`
  mutate the wrapped Graphix pattern and return the same `LabPattern` wrapper
  for fluent chaining.
- If a Graphix runtime method returns a replacement pattern object instead of
  mutating in place, Graphix Lab keeps the wrapper aligned to that replacement
  and still returns `self`.
- `copy()` is only available when the active Graphix runtime exposes
  `Pattern.copy()`. If that method is missing, Graphix Lab raises
  `GraphixCompatibilityError` with a clear message explaining that the wrapper
  otherwise works in place.

If an installed Graphix version does not expose one of the required pattern
methods, Graphix Lab raises `GraphixCompatibilityError` instead of failing with
an unhelpful attribute error.

`commands()` iterates over the wrapped Graphix pattern and normalizes each
command into a stable `CommandRecord` with:

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
For measurement commands, Graphix Lab reads angle and plane information
defensively from either direct command attributes or nested measurement objects.
If Graphix exposes an unrecognized command object, Graphix Lab still returns a
record with `kind="UNKNOWN"` and the raw `repr` so callers can inspect it
without crashing.

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
