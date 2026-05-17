# Status

- Phase: Security and release-preparation hardening
- Last update: Dependabot configuration now tracks Python dependencies and GitHub Actions, CI uses read-only repository permissions by default, CI runs a `pip-audit` dependency vulnerability job, and the local CLI exposes `python scripts/run_template_command.py security` for manual audits from `.venv`
- Next step: Continue manual MVP acceptance/release preparation; before PyPI publishing, add a dedicated release workflow using PyPI Trusted Publishing and a protected GitHub environment
- Blockers: No blocker for the core MVP flow; the optional `qiskit` extra is still not installed in the active local `.venv`, so the real-Qiskit tests continue to skip locally and are expected to run through the isolated CI job instead
- Tests added: `tests/unit/test_dependabot_config.py` covers Dependabot configuration, `tests/unit/test_ci_workflow.py` covers CI permission and dependency-audit expectations, and `tests/unit/test_tooling.py` covers the local security audit command plus Ruff security configuration
- Quality command result: On May 17, 2026, security hardening passed `ruff check . --fix`, `ruff format .`, `pytest` (`162 passed`, `2 skipped` for missing optional Qiskit), `pyright` (`0 errors`), and `python scripts/run_template_command.py security` (`No known vulnerabilities found`)
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
- [x] Dependabot tracks Python dependencies and GitHub Actions
- [x] CI runs a dependency vulnerability audit with `pip-audit`
- [x] CI defaults `GITHUB_TOKEN` to read-only repository contents
