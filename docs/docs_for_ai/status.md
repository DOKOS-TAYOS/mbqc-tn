# Status

- Phase: Prompt 04 completed for the live `LabCircuit` wrapper; higher-level `LabPattern` behavior beyond `to_graphix()` is still deferred to later prompts
- Last update: implemented a fluent `LabCircuit` wrapper that lazily creates and delegates to `graphix.Circuit`, supports `h/x/y/z/s/rx/ry/rz/cnot`, compiles through `transpile().pattern` into `LabPattern`, added explicit `pi`/`radians` angle handling, and updated the API docs plus release notes to reflect the live circuit surface
- Next step: Continue with `graphix_lab_vibe_template_codex_pack/prompts/05_lab_pattern_wrapper.md`
- Blockers: Graphix is still not installed in the active `.venv`, so real runtime circuit operations still depend on a future dependency install in this checkout; `LabPattern` methods other than `to_graphix()` remain intentionally deferred until Prompt 05; `THIRD_PARTY_LICENSES` also still reflects the pre-Graphix environment
- Tests added: `tests/unit/test_lab_circuit.py` now covers fluent gate chaining, explicit angle-unit conversion, `to_graphix()`, `compile()`, and unsupported unit errors against a fake Graphix runtime; `tests/unit/test_public_api.py` still checks the exported Graphix Lab models, wrapper types, and the clear `from_qiskit` placeholder error
- Quality command result: `bin\quality.cmd` passed with `ruff check . --fix`, `ruff format .`, `pytest`, and `pyright`; the in-sandbox run still hit the known Windows temp-directory permission boundary for pytest fixtures, but the rerun outside the sandbox completed cleanly with `41 passed` and `0 errors`
- License: MIT

## Checklist

- [x] Library-first package structure exists
- [x] CLI commands exist
- [x] Human documentation baseline exists
- [x] AI documentation baseline exists
- [x] Bootstrap resyncs the editable install
- [x] Bootstrap refuses re-running after template setup is complete
- [x] CI validates a fresh template copy through bootstrap plus quality
- [x] Minimal stable wrappers exist
- [x] Cleanup command protects `.venv`
- [x] Cleanup tolerates inaccessible subtrees conservatively
- [x] Project-specific bootstrap completed
- [x] Third-party license inventory regenerated after the initial bootstrap dependency install
- [x] Graphix Lab planning docs exist under `docs/graphix_lab`
- [x] Graphix Lab AI status addendum exists
- [x] Root docs now point to the Graphix Lab planning set
- [x] `pyproject.toml` declares Graphix Lab runtime and optional dependency metadata
- [x] Graphix capability detection now inspects the installed runtime defensively
- [x] Missing Graphix now raises a clear domain error instead of a raw import failure
- [x] Initial Graphix Lab public domain models are exported from `graphix_lab`
- [x] Template metadata is no longer part of the public top-level API
- [ ] `THIRD_PARTY_LICENSES` regenerated after installing Graphix Lab runtime dependencies
