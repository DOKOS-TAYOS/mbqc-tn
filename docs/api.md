# API Overview

## Public Python API

Graphix Lab now exposes the initial public domain model and reserved entrypoints
for the upcoming Graphix-backed wrappers.

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

### Reserved wrapper entrypoints

### `circuit(width: int) -> LabCircuit`

Creates a lightweight `LabCircuit` placeholder object today. The Graphix-backed
fluent builder behavior arrives in the next prompt without changing the import
surface.

### `from_graphix_pattern(pattern: object) -> LabPattern`

Wraps a raw pattern object in a lightweight `LabPattern` placeholder. For this
prompt, only `to_graphix()` is live; Graphix operations are still deferred.

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
