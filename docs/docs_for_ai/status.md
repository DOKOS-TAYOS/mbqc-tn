# Status

- Phase: Prompt 05 completed for the live `LabPattern` wrapper; command introspection, summaries, execution, tracing, and visualization behavior remain deferred to later prompts
- Last update: implemented a fluent `LabPattern` wrapper that can wrap raw Graphix patterns or `LabCircuit.compile()` output, performs in-place `standardize()` / `shift_signals()` / `perform_pauli_measurements()` chaining, exposes `copy()` when the runtime provides `Pattern.copy()`, raises clear `GraphixCompatibilityError` messages when pattern APIs are missing, and updates the public API docs plus release notes to explain the mutation semantics
- Next step: Continue with `graphix_lab_vibe_template_codex_pack/prompts/06_command_introspection.md`
- Blockers: Graphix is still not installed in the active `.venv`, so real runtime pattern operations still depend on a future dependency install in this checkout; `LabPattern.commands()`, `summary()`, `explain()`, `resources()`, `run()`, `trace()`, `draw()`, `animate()`, and `compare_backends()` remain intentionally deferred to later prompts; `THIRD_PARTY_LICENSES` also still reflects the pre-Graphix environment
- Tests added: `tests/unit/test_lab_pattern.py` now covers compile-to-pattern wrapping, fluent pattern chaining, `copy()` behavior, and compatibility failures against a fake Graphix runtime; the existing `tests/unit/test_lab_circuit.py` compile test still guards the `LabCircuit -> LabPattern` handoff and `tests/unit/test_public_api.py` still checks the exported wrapper types
- Quality command result: `bin\quality.cmd` passed with `ruff check . --fix`, `ruff format .`, `pytest`, and `pyright`; the in-sandbox run still hit the known Windows temp-directory permission boundary for pytest temp workspaces, but the rerun outside the sandbox completed cleanly with `45 passed` and `0 errors`
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
- [x] `LabPattern` now exposes live fluent wrapper methods around Graphix pattern mutation APIs
- [ ] `THIRD_PARTY_LICENSES` regenerated after installing Graphix Lab runtime dependencies
