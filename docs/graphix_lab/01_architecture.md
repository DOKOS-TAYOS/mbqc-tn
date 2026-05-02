# Architecture

This project inherits the template's library-first architecture.

## Package layout

After bootstrap, the package is `graphix_lab`.

Recommended layout:

```text
src/graphix_lab/
  __init__.py
  cli.py
  domain/
    commands.py
    summaries.py
    traces.py
    simulation.py
    errors.py
  app/
    circuit_service.py
    pattern_service.py
    summary_service.py
    simulation_service.py
    trace_service.py
    comparison_service.py
  infrastructure/
    graphix_adapter.py
    graphix_capabilities.py
    qiskit_adapter.py
    plotting.py
    graph_layout.py
```

## Layers

### Domain

Stable, typed, mostly immutable data structures. Domain objects should not import heavy optional dependencies unless unavoidable.

Examples:

- `CommandRecord`
- `CommandKind`
- `PatternSummary`
- `ResourceSummary`
- `TraceFrame`
- `RunTrace`
- `SimulationReport`
- `BackendComparisonReport`

### App

Orchestrates workflows while staying independent from presentation details.

Examples:

- compile a `LabCircuit` into a `LabPattern`
- standardize or shift signals
- build command tables
- run simulations through Graphix
- build trace frames
- compare backends

### Infrastructure

Adapters to external libraries and runtime details.

Examples:

- Graphix version/capability detection
- Graphix command extraction
- Qiskit `QuantumCircuit` translation
- Matplotlib plotting
- NetworkX graph layout

### CLI

The CLI should remain thin. It may expose commands such as `info`, `examples`, or `inspect`, but the core product is the library API.

## Dependency direction

```text
cli -> app -> domain
app -> infrastructure -> external libraries
infrastructure -> domain
```

Domain must not import app or infrastructure.

## Public API

The public API should live in `src/graphix_lab/__init__.py` and stay small. Avoid exposing every internal service.
