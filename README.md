# Graphix Lab

Graphix Lab is a small educational usability layer over Graphix for
measurement-based quantum computing experiments. It keeps Graphix in charge of
transpilation, pattern manipulation, and simulation, while adding readable
summaries, conceptual traces, backend comparisons, and Matplotlib-based
inspection tools.

## Project Scope

`A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends.`

## Install

This repository is already bootstrapped as Graphix Lab. Do not rerun
`bootstrap` here.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Linux or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

If you also want the optional Qiskit import example, install:

```bash
python -m pip install -e .[qiskit,dev]
```

After changing runtime dependencies in `pyproject.toml`, rerun the editable
install inside `.venv` before trusting runtime behavior or quality results.
When dependency changes affect third-party packages, regenerate
`THIRD_PARTY_LICENSES` with `python scripts/run_template_command.py licenses`.

## Minimal Example

```python
from graphix_lab import circuit

pattern = circuit(2).h(0).cnot(0, 1).compile().standardize()

print(pattern.summary())
print(pattern.explain())

report = pattern.compare_backends(backends=("statevector",))
print(report)
```

## Example Scripts

- `examples/one_qubit_rotation.py` shows a tiny rotation workflow and prints
  the resulting summary.
- `examples/bell_like_pattern.py` builds a Bell-like circuit, compiles it, and
  prints a small resource overview.
- `examples/trace_slider.py` creates the Matplotlib slider-based trace view
  without requiring a notebook.
- `examples/trace_animation.py` prepares the same trace-inspection handle and
  prints the final frame title for quick terminal verification.
- `examples/backend_comparison.py` runs the same pattern through detected
  Graphix backends and prints the typed comparison report.
- `examples/qiskit_import.py` demonstrates optional Qiskit import and degrades
  gracefully when `qiskit` is not installed.
- `examples/library_usage.py` shows the frozen public data models without
  requiring a Graphix runtime call.
- `examples/cli_usage.py` demonstrates the thin CLI entrypoint through a safe
  `clean --dry-run` invocation.

## Working In This Repository

1. Create or activate `.venv`.
2. Install with `python -m pip install -e .[dev]` if the environment is not
   ready yet.
3. Run `bin\quality.cmd` on Windows or `./bin/quality.sh` on Linux/macOS.
4. Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` when the public
   behavior or workflow changes.

The wrappers in `bin/` stay useful because they prefer the local `.venv`
interpreter and keep the quality flow consistent across Windows and Linux/macOS.

## License

Graphix Lab is distributed under the MIT License. See `LICENSE` for the project
license text.

`THIRD_PARTY_LICENSES` tracks the runtime dependency licenses from the active
`.venv`. Regenerate it with `python scripts/run_template_command.py licenses`
after dependency changes. The license command now ignores repo-local editable
aliases that still point at this checkout, so stale template installs do not
pollute the inventory. The generated table is metadata-based, so a dependency
may still show `UNKNOWN` when the installed package does not publish license
metadata in its distribution.

## Project Documentation

- [Documentation index](docs/README.md)
- [Graphix Lab project docs](docs/graphix_lab/README.md)
- [Quick start](docs/quick-start.md)
- [Developer guide](docs/guide.md)
- [Architecture](docs/architecture.md)
- [API overview](docs/api.md)
- [Release and packaging notes](docs/graphix_lab/07_release_packaging.md)
- [AI user guide](docs/docs_for_ai/guide_for_ai_users.md)
- [AI project instructions](docs/docs_for_ai/project_ai_instructions.md)
- [AI status board](docs/docs_for_ai/status.md)
- [Graphix Lab AI addendum](docs/docs_for_ai/graphix_lab_status_addendum.md)
