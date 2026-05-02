# Project AI Instructions

## Mission

Use this template to build software projects with a stable Python core, minimal public APIs, explicit typing, and low-friction maintenance.

## Required Workflow

1. Read `docs/docs_for_ai/status.md` before making changes.
2. Bootstrap a fresh template copy before long-term development.
3. Keep the library layer as the center of the system.
4. Add or update tests before changing behavior.
5. Update `CHANGELOG.md` for meaningful changes.
6. Update these AI docs when workflow, architecture, or constraints change.

## Non-Negotiable Rules

- Always include typing in function definitions.
- Keep the public API as small as possible.
- Use TDD for behavior changes.
- Update `CHANGELOG.md` when adding, fixing, or changing something meaningful.
- Do not remove `.venv` or clean it as part of project cleanup.
- Prefer Windows-safe commands, but keep Linux support where practical.
- Prefer the stable wrappers in `bin/` so commands keep using the repo's active `.venv` and package entrypoints.
- Treat `bootstrap` as a one-time setup command. If it already ran, do not try to re-run it.
- Treat `docs/api.md` and the example scripts as contract documentation.

## Completion Checklist

Before claiming a Python task is complete:

1. Run `ruff check . --fix`
2. Run `ruff format .`
3. Run `pytest`
4. Run `pyright`
5. Update `docs/docs_for_ai/status.md`
6. Update `CHANGELOG.md`

## AI Handoff Checklist

- current status updated
- next step named clearly
- blockers captured
- tests added for new behavior
- docs synchronized with code
