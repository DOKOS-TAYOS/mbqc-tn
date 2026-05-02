# Developer Guide

## Core Principles

- Prefer small, well-named modules with one responsibility.
- Treat the library as the product core and the CLI as a thin entrypoint.
- Keep imports relative inside the package so bootstrap renaming stays safe.
- Use tests to define behavior before implementation changes.
- Update human docs and AI docs when architecture or workflow changes.

## Suggested Workflow

1. Activate `.venv`.
2. Install with `python -m pip install -e .[dev]` if the environment is not ready yet.
3. Run bootstrap once for a fresh project and then treat the result as the real codebase.
4. Write or update a failing test.
5. Implement the minimal change.
6. Run the smallest relevant test command.
7. Refactor while staying green.
8. Before finishing, run the full quality flow.

## Stable Entry Points

- `bin\bootstrap.cmd` or `./bin/bootstrap.sh`
- `bin\quality.cmd` or `./bin/quality.sh`
- `bin\clean.cmd` or `./bin/clean.sh`

Use direct `python -m <package>.cli ...` commands when you specifically want the module-level entrypoint after bootstrap.

## Documentation Responsibilities

- `README.md`: overview and first-run expectations
- `docs/quick-start.md`: exact commands for a fresh project
- `docs/api.md`: public API and CLI contract changes
- `docs/architecture.md`: layer or data-flow changes
- `docs/docs_for_ai/project_ai_instructions.md`: workflow, guardrails, and AI handoff rules
- `docs/docs_for_ai/status.md`: current phase, next step, blockers
