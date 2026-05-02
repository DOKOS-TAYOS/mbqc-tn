# Guide for AI Users

## Fast Path

1. Read `docs/docs_for_ai/status.md` to see whether bootstrap already happened.
2. Read `docs/api.md` for the public API and CLI contract.
3. Read `examples/library_usage.py` and `examples/cli_usage.py` only if you need usage examples.
4. Read `docs/docs_for_ai/project_ai_instructions.md` only before changing code.
5. Use the wrappers in `bin/` to stay aligned with the repo's active `.venv` and package entrypoints.

## What Not to Assume

- internal modules are not public contracts
- placeholder metadata means bootstrap has not finished
- `bootstrap` is not re-runnable once the project identity has been applied
- empty or outdated `THIRD_PARTY_LICENSES` means dependencies were not regenerated yet

## Useful Commands

- `bin\bootstrap.cmd` or `./bin/bootstrap.sh`
- `bin\quality.cmd` or `./bin/quality.sh`
- `bin\clean.cmd --dry-run` or `./bin/clean.sh --dry-run`
