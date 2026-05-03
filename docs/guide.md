# Developer Guide

## Core Principles

- Prefer small, well-named modules with one responsibility.
- Treat the library as the product core and the CLI as a thin entrypoint.
- Keep function typing explicit.
- Use tests to define behavior before implementation changes.
- Update human docs and AI docs when architecture or workflow changes.

## Suggested Workflow

1. Activate `.venv`.
2. Install with `python -m pip install -e .[dev]` if the environment is not
   ready yet.
3. Write or update a failing test.
4. Implement the minimal change.
5. Run the smallest relevant test command.
6. Refactor while staying green.
7. Before finishing, run the full quality flow.

## Stable Entry Points

- `bin\quality.cmd` or `./bin/quality.sh`
- `bin\clean.cmd` or `./bin/clean.sh`
- `python scripts/run_template_command.py licenses`

The `bootstrap` wrapper still exists for validating fresh template copies, but
it is not part of the normal day-to-day workflow in this already-bootstrapped
repository.

## Example Scripts

- `examples/one_qubit_rotation.py`
- `examples/bell_like_pattern.py`
- `examples/trace_slider.py`
- `examples/trace_animation.py`
- `examples/backend_comparison.py`
- `examples/qiskit_import.py`
- `examples/library_usage.py`
- `examples/cli_usage.py`

## Documentation Responsibilities

- `README.md`: overview, install steps, and the first example to try
- `docs/quick-start.md`: concise repo-specific setup and run commands
- `docs/api.md`: public API and CLI contract changes
- `docs/graphix_lab/*.md`: Graphix Lab design notes and MVP expectations
- `docs/docs_for_ai/project_ai_instructions.md`: workflow, guardrails, and AI
  handoff rules
- `docs/docs_for_ai/status.md`: current phase, next step, blockers, and recent
  verification results
