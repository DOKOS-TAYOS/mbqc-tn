# Architecture

Graphix Lab keeps a library-first shape, with the public Python API as the main
product and the CLI as a thin helper layer.

## Current Package Layout

```text
src/graphix_lab/
  __init__.py
  public_api.py
  cli.py
  domain/
    commands.py
    errors.py
    simulation.py
    summaries.py
    traces.py
  app/
    bootstrap_service.py
    circuit_service.py
    clean_service.py
    pattern_service.py
    simulation_service.py
    summary_service.py
    tooling_service.py
    visualization_service.py
  infrastructure/
    graphix_adapter.py
    graphix_capabilities.py
    graphix_runtime.py
    qiskit_adapter.py
    text_files.py
```

## Layer Responsibilities

### Domain

Stable, typed data structures and domain errors.

Examples:

- `CommandRecord`
- `PatternSummary`
- `ResourceSummary`
- `TraceFrame`
- `RunTrace`
- `SimulationReport`
- `BackendRunReport`
- `BackendComparisonReport`

### App

Small orchestration services used by the public API and CLI.

Examples:

- build or compile a `LabCircuit`
- mutate or copy a wrapped Graphix pattern
- derive summaries from normalized commands
- run simulations or backend comparisons
- build figures and trace-slider handles

### Infrastructure

Adapters for Graphix, optional Qiskit, and a few repo/tooling details.

Examples:

- Graphix runtime and capability detection
- Graphix command normalization
- Qiskit `QuantumCircuit` translation
- text-file helpers used by the CLI/tooling path

### Public API And CLI

- `public_api.py` exposes the small educational library surface.
- `cli.py` stays thin and delegates real work to services.

## Dependency Direction

```text
cli -> app
public_api -> app
public_api -> domain
public_api -> infrastructure
app -> infrastructure
infrastructure -> domain
```

Domain code should stay free of Graphix and Qiskit runtime imports.
