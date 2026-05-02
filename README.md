# Graphix Lab

Graphix Lab is a small educational usability layer over Graphix for measurement-based quantum computing experiments. It aims to wrap Graphix circuits and patterns with readable summaries, command introspection, simulation reports, conceptual traces, and Matplotlib/NetworkX visualizations.

Graphix Lab does not replace Graphix. It delegates MBQC transpilation, pattern manipulation, flow and gflow logic, and simulation backends to Graphix while this repository focuses on usability, diagnostics, and teaching-friendly APIs.

## Intended MVP Flow

The planned user-facing workflow for the MVP looks like this:

```python
from graphix_lab import circuit

lab = (
    circuit(2)
    .h(0)
    .cnot(0, 1)
    .compile()
    .standardize()
    .shift_signals()
)

print(lab.summary())
fig = lab.draw()
report = lab.run(backend="statevector", seed=123, trace=True)
```

## Working In This Repository

This repository has already been bootstrapped as Graphix Lab. Do not rerun `bootstrap` here.

1. Create and activate `.venv`.
2. Install in editable mode with dev tools: `python -m pip install -e .[dev]`
3. Run `bin\quality.cmd` on Windows or `./bin/quality.sh` on Linux/macOS.
4. After installing or changing runtime dependencies, regenerate `THIRD_PARTY_LICENSES` with `python scripts/run_template_command.py licenses`.

The wrappers in `bin/` stay useful because they prefer the local `.venv` interpreter and keep the quality flow consistent across Windows and Linux/macOS.

## Project Scope

`A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends.`

## Project Documentation

- [Documentation index](docs/README.md)
- [Graphix Lab project docs](docs/graphix_lab/README.md)
- [Quick start](docs/quick-start.md)
- [Developer guide](docs/guide.md)
- [Architecture](docs/architecture.md)
- [API overview](docs/api.md)
- [AI user guide](docs/docs_for_ai/guide_for_ai_users.md)
- [AI project instructions](docs/docs_for_ai/project_ai_instructions.md)
- [AI status board](docs/docs_for_ai/status.md)
- [Graphix Lab AI addendum](docs/docs_for_ai/graphix_lab_status_addendum.md)
