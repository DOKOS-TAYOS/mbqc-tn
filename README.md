# Project Title Pending

Stable Python template for software-oriented projects. It starts as a reusable library with a lightweight CLI, strong quality defaults, and a compact handoff path for both people and AI contributors.

## Official First Run

This template is intentionally incomplete until bootstrap fills in:

- author name
- initial version
- project scope
- license choice
- final distribution and package names

1. Create and activate `.venv`.
2. Install in editable mode with dev tools: `python -m pip install -e .[dev]`
3. Run `bin\bootstrap.cmd` on Windows or `./bin/bootstrap.sh` on Linux/macOS.
4. Let bootstrap finish its automatic editable reinstall.
5. Run `bin\quality.cmd` on Windows or `./bin/quality.sh` on Linux/macOS.

Bootstrap is a one-time step for a fresh copy of the template. After it finishes, treat the repository as the real project codebase and keep using the stable wrappers when you want the safest entrypoint.

This template repository itself is published under MIT. Bootstrap can keep that choice or replace it for the project you create from the template.

## Why the Wrappers Stay Useful

Before bootstrap, the placeholder package is still called `project_name`. After bootstrap, the package name changes. The wrappers in `bin/` stay stable across that rename and prefer the local `.venv` interpreter when it exists.

If you want the raw module entrypoint, use `python -m project_name.cli ...` before bootstrap and the new package name after bootstrap.

## Project Scope

`PROJECT_SCOPE_PENDING`

## What This Template Includes

- `src` layout with a small public API and a CLI entrypoint
- TDD-oriented tests for API, bootstrap, cleanup, CLI, and examples
- stable wrappers for bootstrap, quality, and clean
- documentation for humans plus a short AI fast path
- CI for Windows and Ubuntu with Python 3.11 to 3.13, plus a fresh-copy bootstrap smoke run

## More Docs

- [Documentation index](docs/README.md)
- [Quick start](docs/quick-start.md)
- [Developer guide](docs/guide.md)
- [Architecture](docs/architecture.md)
- [API overview](docs/api.md)
- [AI user guide](docs/docs_for_ai/guide_for_ai_users.md)
- [AI project instructions](docs/docs_for_ai/project_ai_instructions.md)
