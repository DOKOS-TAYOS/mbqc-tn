# Changelog

All notable changes to this project are documented in this file.

## Unreleased

### Added

- `LabPattern.commands()` now returns stable `CommandRecord` tuples by normalizing Graphix pattern commands through a defensive adapter that supports the known `N`, `E`, `M`, `X`, `Z`, and `C` command kinds, preserves raw `repr` output, and falls back to `kind="UNKNOWN"` for unrecognized command objects.
- A Graphix-backed `LabPattern` wrapper that keeps a live Graphix pattern reference, supports fluent `standardize()`, `shift_signals()`, and `perform_pauli_measurements()` mutation helpers, exposes `copy()` when the runtime provides `Pattern.copy()`, and raises clear `GraphixCompatibilityError` messages when a pattern API is missing.
- Focused unit coverage for the live `LabPattern` wrapper, including compile-to-pattern flow, method chaining, copy semantics, and compatibility failures against a fake Graphix runtime.
- A Graphix-backed `LabCircuit` fluent wrapper that chains `h`, `x`, `y`, `z`, `s`, `rx`, `ry`, `rz`, and `cnot`, exposes `to_graphix()`, and compiles through `circuit.transpile().pattern` into `LabPattern`.
- Explicit angle-unit handling for `LabCircuit` rotations, with public `pi` units by default, `radians` conversion support, and clear errors for unsupported units.
- Focused unit coverage for the new circuit wrapper using a fake Graphix runtime, so the public API stays testable even when Graphix is missing from the active `.venv`.
- The public `graphix_lab` package now exports frozen Graphix Lab domain models for commands, summaries, traces, simulations, and backend comparisons, plus lightweight `LabCircuit` and `LabPattern` wrapper stubs that reserve the long-term import surface without pulling in Graphix yet.
- A defensive Graphix capability adapter with typed domain errors, a frozen `GraphixCapabilities` dataclass, and a public `graphix_info()` entrypoint for inspecting the active Graphix runtime.
- Graphix Lab planning documents under `docs/graphix_lab/`, covering scope, architecture, public API, Graphix integration, visualization, Qiskit, testing, packaging, roadmap, and template integration.
- `docs/docs_for_ai/graphix_lab_status_addendum.md` so future handoffs keep Graphix-specific phase, blocker, and quality context next to the main AI status board.
- Python software template with `src` layout, CLI entrypoint, and bootstrap flow.
- Cleanup and quality wrappers plus test and license CLI commands.
- Human documentation, AI documentation, examples, and CI defaults.
- TDD-oriented tests for bootstrap, cleanup, CLI, public API, and examples.
- A reusable `scripts/bootstrap_smoke.py` helper that creates a fresh template copy, bootstraps it non-interactively, and runs the full quality flow.
- The copied repository is now bootstrapped as Graphix Lab with a local `.venv` dev environment and regenerated `THIRD_PARTY_LICENSES`.
- Targeted unit tests now cover Graphix capability discovery with a monkeypatched installed runtime and the clear error path when Graphix is missing.

### Fixed

- Bootstrap now wraps long generated `scope_summary` values in `template_metadata.py`, which keeps post-bootstrap Ruff runs green for verbose project descriptions.
- Bootstrap no longer rewrites `THIRD_PARTY_LICENSES` as plain text during identity replacement; the inventory now changes only when the explicit license-generation step runs.
- `THIRD_PARTY_LICENSES` generation now stays compact and uses the active project interpreter instead of expanding full license texts or scanning unrelated global packages.
- Bootstrap now re-syncs the editable install after renaming the package, so the new project state is immediately usable.
- Bootstrap now refuses to run again once the template has already been configured, including dry-run calls.
- Bootstrap no longer rewrites unrelated `MIT` text while changing the project license, which keeps `THIRD_PARTY_LICENSES` stable for a public MIT template.
- Bootstrap no longer rewrites its own internal `bootstrap_required` replacement rules after the first project bootstrap, which keeps fresh-copy smoke validation working on already-bootstrapped copies.
- The license inventory now excludes the local template package and no longer ships `example.invalid` placeholder URLs.
- The wrapper launcher now reads the current package name from `pyproject.toml`, so `bin/bootstrap`, `bin/quality`, and `bin/clean` still work after the template package is renamed.
- Non-interactive bootstrap now derives `package_name` from `distribution_name` automatically, and the exported template metadata flips `bootstrap_required` to `False` after bootstrap.
- `clean` now avoids deleting temporary parent directories when that would also wipe a nested `.venv`.
- `clean` now walks directories conservatively, skips inaccessible subtrees, and no longer relies on fragile recursive globbing.
- Automated tests no longer depend on repo-local `test-artifacts`, which avoids the Windows permission issues seen in temporary workspaces.
- Bootstrap-facing tests and example assertions now stay valid after a fresh-copy smoke bootstrap, instead of assuming the repo is always still in template state.

### Changed

- CI no longer runs the inherited template-bootstrap smoke job or ships the dedicated `scripts/bootstrap_smoke.py` helper, because this repository is now a bootstrapped Graphix Lab library rather than a reusable fresh-template source.
- `docs/api.md` now documents the live `LabPattern.commands()` behavior, including how command kinds, measurement metadata, correction domains, and unknown-command fallbacks are exposed through `CommandRecord`.
- `docs/api.md` now documents the live `LabPattern` wrapper semantics, including in-place mutation behavior, fluent chaining, and runtime-dependent `copy()` support.
- `docs/api.md` now documents the live `LabCircuit` wrapper behavior instead of describing the circuit entrypoint as a future stub.
- The placeholder `TemplateMetadata` top-level API has been retired in favor of the Graphix Lab public surface, and `docs/api.md` plus `examples/library_usage.py` now reflect the new domain-model-first contract.
- The public API docs and regression tests now include the new `graphix_info()` runtime inspection entrypoint.
- The root README and documentation index now frame the repository as Graphix Lab and point readers to the new project-specific planning docs instead of template-only guidance.
- Runtime dependency metadata now declares Graphix, Matplotlib, NetworkX, and NumPy as core dependencies, plus optional `qiskit` and `examples` extras, while preserving the existing `dev` tooling set.
- Release and AI status docs now note that `THIRD_PARTY_LICENSES` must be regenerated after the new runtime dependencies are installed in `.venv`.
- The project identity now uses the Graphix Lab bootstrap values: title `Graphix Lab`, distribution `graphix-lab`, package `graphix_lab`, version `0.1.0`, and the Graphix usability-layer project scope.
- The template footprint is leaner by default: removed `CITATION.cff`, removed `docs/features.md`, and reduced `bin/` wrappers to bootstrap, quality, and clean.
- The recommended first-run flow now uses stable wrappers in `bin/`, which keep working across the bootstrap package rename and prefer the local `.venv`.
- The public CLI now focuses on `bootstrap`, `quality`, `test`, `clean`, and `licenses`; the old `demo` command was removed in favor of real examples built on safe commands.
- AI documentation was compacted to three files, and the human docs were tightened to reduce overlap between the README, quick start, and guide.
- The redundant `scripts/clean.py` helper was removed, and `hatchling` no longer ships as a direct dev dependency in the template environment.
- `quality` and `test` now invoke tools through `sys.executable -m ...`, which keeps interpreter selection consistent across Windows and Linux.
- Pytest returned to its default cache naming while Ruff cleanup rules were updated for the standard `.pytest_cache` directory.
- CI now includes a dedicated fresh-copy template smoke job on Windows and Ubuntu, using Python 3.12 to validate the real bootstrap-plus-quality flow end to end.
- The template repository now ships with a real MIT license and `Alejandro Mata Ali` as the template author, while still leaving bootstrap in charge of project-specific identity.
