# Agent instructions for Graphix Lab

This repository starts from `DOKOS-TAYOS/vibe_template`. Treat the template conventions as binding unless a task explicitly changes them.

## Must-read files before code changes

1. `docs/docs_for_ai/status.md`
2. `docs/docs_for_ai/project_ai_instructions.md`
3. `docs/api.md`
4. `docs/architecture.md`
5. `docs/graphix_lab/` project-specific docs, if already present

## Project mission

Build a small, typed, tested Python library that makes Graphix easier to use for MBQC education and experimentation. Graphix Lab is a wrapper and usability layer, not a replacement for Graphix.

## Non-negotiable rules

- Do not reimplement Graphix core MBQC simulation, flow finding, pattern generation, or tensor-network backends.
- Prefer public Graphix APIs and capability checks over private assumptions.
- Keep the public API intentionally small.
- Write or update tests before changing behavior.
- Use typed dataclasses for stable domain objects.
- Keep CLI functionality thin and secondary to the library API.
- Use Matplotlib and NetworkX for visualization.
- Do not add GPU, MPI, CUDA-Q, or cuQuantum support in the MVP.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` after meaningful changes.

## Architecture mapping

- `domain`: immutable records and public result types such as `CommandRecord`, `PatternSummary`, `TraceFrame`, `RunTrace`, `SimulationReport`, `BackendComparison`.
- `app`: orchestration services such as pattern compilation, command summarization, simulation execution, trace construction, backend comparison.
- `infrastructure`: adapters to Graphix, Qiskit, Matplotlib, NetworkX, and packaging/version discovery.
- `cli.py`: thin presentation layer for a few helpful commands only.

## Quality commands

Use the template wrappers when possible. The template currently exposes `bootstrap`, `quality`, and `clean` wrappers; use `python -m pytest` for focused test runs:

```bash
./bin/quality.sh
python -m pytest
```

On Windows:

```powershell
bin\quality.cmd
python -m pytest
```

If wrappers are unavailable, run:

```bash
ruff check . --fix
ruff format .
pytest
pyright
```
