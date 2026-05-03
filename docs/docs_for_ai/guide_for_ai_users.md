# Guide for AI Users

## Fast Path

1. Read `docs/docs_for_ai/status.md` for the current prompt, blockers, and last
   verification result.
2. Read `docs/api.md` for the public API and CLI contract.
3. Read `examples/one_qubit_rotation.py`, `examples/bell_like_pattern.py`,
   `examples/trace_slider.py`, `examples/trace_animation.py`,
   `examples/backend_comparison.py`, `examples/library_usage.py`, and
   `examples/cli_usage.py` for concrete usage. Read
   `examples/qiskit_import.py` only when working on the optional Qiskit
   frontend.
4. Read `docs/docs_for_ai/project_ai_instructions.md` before changing code.
5. Use the wrappers in `bin/` to stay aligned with the repo's active `.venv`
   and package entrypoints.

## What Not To Assume

- internal modules are not public contracts
- `qiskit` is optional and may be missing from the active `.venv`
- changing `pyproject.toml` requires reinstalling the editable package in
  `.venv`
- `THIRD_PARTY_LICENSES` may lag behind runtime dependency changes until the
  explicit license-generation command is run

## Useful Commands

- `bin\quality.cmd` or `./bin/quality.sh`
- `bin\clean.cmd --dry-run` or `./bin/clean.sh --dry-run`
- `python scripts/run_template_command.py licenses`
