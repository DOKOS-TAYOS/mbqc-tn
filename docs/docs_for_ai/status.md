# Status

- Phase: Prompt 16 implemented for review hardening
- Last update: the Prompt 16 review found and fixed a real Graphix compatibility bug where `Pattern.shift_signals()` mutates the pattern in place but returns an auxiliary signal-map `dict`; `LabPattern.shift_signals()` now keeps the wrapper bound to the mutated Graphix pattern instead of replacing it with that dictionary, example smoke coverage now includes the extra `trace_animation`, `library_usage`, and `cli_usage` scripts, and the public docs now describe the real `shift_signals()` behavior
- Next step: No later Codex-pack prompt remains after Prompt 16; move to manual MVP acceptance/release preparation, or write a new follow-up prompt only if you want post-MVP Graphix compatibility or UX refinements
- Blockers: No blocker for the core MVP flow; the optional `qiskit` extra is still not installed in the active local `.venv`, so the real-Qiskit tests continue to skip locally and are expected to run through the isolated CI job instead
- Tests added: `tests/unit/test_lab_pattern.py` now covers the real `shift_signals()` auxiliary-return shape, `tests/integration/test_graphix_runtime_integration.py` now verifies that real Graphix keeps command introspection after `shift_signals()`, and `tests/smoke/test_examples.py` now covers `examples/trace_animation.py`, `examples/library_usage.py`, and `examples/cli_usage.py`
- Quality command result: On May 3, 2026, `bin\quality.cmd` again hit the known sandbox-only Windows temp-directory permission boundary during `pytest`, then passed cleanly outside the sandbox with `ruff check . --fix`, `ruff format .`, package-import smoke, CLI-help smoke, `pytest`, and `pyright`; the final outside-sandbox result was `100 passed`, `2 skipped` (missing optional Qiskit), and `0 pyright errors`
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
- [x] `LabPattern.trace()` now exposes a standalone conceptual `RunTrace`
- [x] `LabPattern.draw()` now returns a headless-safe Matplotlib `Figure` with local command-record visualization plus optional Graphix delegation
- [x] `LabPattern.animate()` now exposes headless-safe slider-based trace inspection through `TraceAnimationHandle`
- [x] `LabPattern.compare_backends()` now exposes typed backend comparison reports with conservative default backend selection and per-backend failure capture
- [x] `LabPattern.shift_signals()` now preserves the wrapped Graphix pattern when the runtime returns auxiliary signal-shift data
- [x] `from_qiskit(...)` now imports the supported Qiskit gate subset with clear optional-dependency and unsupported-gate failures
- [x] Script examples now cover the current public workflows and optional-Qiskit guidance path
- [x] The extra example scripts now have smoke coverage and are listed in the user/AI guides
- [x] The README and Graphix Lab docs now describe the live API and current repository workflow
- [x] `THIRD_PARTY_LICENSES` regenerated after installing Graphix Lab runtime dependencies
