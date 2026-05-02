# Status

- Phase: Prompt 06 completed for Graphix command introspection; summaries, execution, tracing, and visualization behavior remain deferred to later prompts
- Last update: implemented `LabPattern.commands()` on top of a defensive Graphix adapter that iterates compiled patterns, normalizes known `N`/`E`/`M`/`X`/`Z`/`C` commands into stable `CommandRecord` objects, extracts measurement plane and angle from either direct command attributes or nested measurement objects, and falls back to `kind="UNKNOWN"` plus raw `repr` output for unrecognized command objects
- Next step: Continue with `graphix_lab_vibe_template_codex_pack/prompts/07_summary_explain_resources.md`
- Blockers: Graphix is still not installed in the active `.venv`, so real runtime pattern operations still depend on a future dependency install in this checkout; `summary()`, `explain()`, `resources()`, `run()`, `trace()`, `draw()`, `animate()`, and `compare_backends()` remain intentionally deferred to later prompts; `THIRD_PARTY_LICENSES` also still reflects the pre-Graphix environment
- Tests added: `tests/unit/test_lab_pattern.py` now covers one-qubit and two-qubit compiled-pattern command normalization plus the unknown-command fallback, while the existing `tests/unit/test_lab_circuit.py` and `tests/unit/test_public_api.py` regression coverage still guards the `LabCircuit -> LabPattern` handoff and exported wrapper surface
- Quality command result: `bin\quality.cmd` passed with `ruff check . --fix`, `ruff format .`, `pytest`, and `pyright`; the in-sandbox run still hit the known Windows temp-directory permission boundary for pytest temp workspaces, but the rerun outside the sandbox completed cleanly with `48 passed` and `0 pyright errors`
- License: MIT

## Checklist

- [x] Library-first package structure exists
- [x] CLI commands exist
- [x] Human documentation baseline exists
- [x] AI documentation baseline exists
- [x] Bootstrap resyncs the editable install
- [x] Bootstrap refuses re-running after template setup is complete
- [x] CI focuses on the bootstrapped Graphix Lab library checks instead of inherited template-bootstrap smoke
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
- [x] `LabPattern.commands()` now exposes stable command introspection through `CommandRecord`
- [ ] `THIRD_PARTY_LICENSES` regenerated after installing Graphix Lab runtime dependencies
