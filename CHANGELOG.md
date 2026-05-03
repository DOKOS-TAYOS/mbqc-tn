# Changelog

All notable changes to this project are documented in this file.

## Unreleased MVP

### Added

- Script examples for the current Graphix Lab workflows: `examples/one_qubit_rotation.py`, `examples/bell_like_pattern.py`, `examples/trace_slider.py`, `examples/backend_comparison.py`, and `examples/qiskit_import.py`.
- Smoke coverage for the new example set, including the optional-Qiskit example's friendly missing-dependency path.
- `from_qiskit(...)` now imports a small supported Qiskit gate subset into a live `LabCircuit`, keeping `qiskit` optional while raising a clear `OptionalDependencyError` when that extra is missing from the active `.venv`.
- The first Qiskit adapter supports `h`, `x`, `y`, `z`, `s`, `rx`, `ry`, `rz`, and `cx` / `cnot`, converts rotation angles into Graphix `pi` units before delegation, and raises `UnsupportedGateError` with the gate name plus instruction index for unsupported instructions.
- Focused unit coverage now exercises the missing-Qiskit path, fake-circuit gate mapping, qubit-index lookup through `find_bit(...)`, `angle_units="pi"` passthrough, and real-Qiskit import smoke tests that auto-skip when Qiskit is not installed.
- `LabPattern.compare_backends(...)` now runs the wrapped Graphix pattern across a selected backend list and returns a typed `BackendComparisonReport` with per-backend success state, elapsed time, result type, error text, and captured warning notes.
- Backend comparison now keeps going after individual backend failures, and explicitly requested unsupported backend names are reported as failed rows instead of aborting the full comparison.
- `BackendComparisonReport.__str__()` now renders a readable plain-text table for notebooks, terminals, and quick inspection.
- Focused unit and integration coverage now exercises detected-backend comparisons, per-backend failure capture, unsupported backend reporting inside comparison runs, and real-Graphix comparison on a small pattern.
- `LabPattern.animate(...)` now returns a headless-safe `TraceAnimationHandle` backed by `matplotlib.widgets.Slider`, so callers can inspect conceptual MBQC trace steps without opening a web UI or relying on notebook-only widgets.
- The slider trace view now reuses the local command-record visualization model, updating the active step title, current command description box, current-node highlight, and measured-versus-pending node styling while keeping callback references alive on the returned handle.
- Focused unit, integration, and smoke coverage now exercise the new animation handle, empty-pattern fallback, real Graphix slider creation, and the new `examples/trace_animation.py` walkthrough.
- `LabPattern.draw(...)` now returns a real headless-safe `matplotlib.figure.Figure`, using a local NetworkX/Matplotlib renderer by default and an explicit `delegate_to_graphix=True` opt-in when callers want to reuse Graphix's own `draw_graph()` path.
- A dedicated visualization service now extracts MBQC graph structure from normalized `CommandRecord` objects, including entanglement edges, measured nodes, `s` / `t` measurement dependencies, explicit `X` / `Z` correction domains, and optional flow overlays when the wrapped Graphix pattern exposes extractable flow metadata.
- Focused unit and integration coverage now exercises visualization-model extraction, correction overlays, opt-in Graphix delegation, and headless figure creation against both fake and real Graphix runtimes.
- `LabPattern.trace()` now returns a standalone syntactic `RunTrace` built from normalized `CommandRecord` objects, with per-step `TraceFrame` snapshots that capture command kind, current nodes, measured nodes, pending nodes, correction notes, and readable descriptions for teaching-oriented inspection.
- The trace builder now uses an explicit post-command convention for measurement frames, so `measured_nodes` already includes the node handled by an `M` command, and `X`/`Z` frames describe correction dependencies from their domains in plain language.
- Focused unit and integration coverage now verify standalone trace generation, readable correction dependency wording, and parity between `LabPattern.trace()` and `run(..., trace=True)`.
- `LabPattern.run()` now delegates small-pattern simulation to the active Graphix runtime, returning a typed `SimulationReport` with backend name, elapsed time, raw result object, result type, requested seed, captured warning notes, and an optional syntactic `RunTrace` payload when `trace=True`.
- A dedicated simulation service now prefers `Pattern.simulate_pattern()` and falls back to `graphix.simulator.PatternSimulator`, while validating built-in backend availability for `statevector`, `densitymatrix`, `tensornetwork`, and `mps` only when the installed Graphix version exposes them.
- Unit coverage now exercises the high-level simulation path, the `PatternSimulator` fallback, unsupported backend errors, and trace-bearing reports, while runtime integration tests verify real Graphix execution for `statevector` plus any optional detected built-in backends.
- `LabPattern.summary()`, `LabPattern.resources()`, and `LabPattern.explain()` now provide structural, teaching-oriented pattern inspection on top of normalized `CommandRecord` data, including detectable inputs/outputs, correction counts, entanglement-edge counts, and concise multi-line explanations without pretending to simulate backend complexity.
- A dedicated summary service now derives `PatternSummary` and `ResourceSummary` objects from Graphix pattern commands, keeping the public wrapper thin while reusing one typed structural analysis path.
- Focused unit tests now cover summary, resource, explanation, and stable string behavior for small compiled patterns through the existing fake Graphix runtime.
- Integration tests that exercise the real Graphix runtime through `graphix_info()` and the public `circuit(...).compile().commands()` flow, so missing or incompatible Graphix installations now fail the quality checks instead of hiding behind fake-only coverage.
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

- The shared `temp_dir` test fixture no longer depends on `pytest`'s own temporary-directory factory; it now probes the system temp root first and falls back to a repo-local `pytest-temp/` workspace only when the full create/write/delete cycle is not usable in the active environment.
- Bootstrap integration tests now ignore unreadable local artifact directories while copying the repository into a temporary workspace, which keeps unrelated local probes from breaking the bootstrap regression suite.
- `LabPattern.shift_signals()` now keeps the wrapped Graphix pattern bound to the real pattern object when Graphix mutates in place but returns its auxiliary signal-map `dict`, instead of accidentally replacing the wrapper target with that dictionary and losing command introspection.
- Real-runtime and fake-runtime tests now cover the `shift_signals()` auxiliary-return shape, so future hardening work catches this Graphix compatibility edge case before it reaches the public API.
- Internal wording now matches the current repo shape more closely, including the `graphix_lab.infrastructure` package description, the small internal export surface at that package root, and a few docs that still spoke as if Graphix Lab were an unbootstrapped template checkout.
- Removed an unused internal public-API placeholder helper from `public_api.py`, and backend detection now reuses the single implementation in `graphix_capabilities.py` instead of maintaining a second copy inside `simulation_service.py`.
- Command-node collection now goes through one shared internal helper for summaries, trace building, and visualization, and `LabPattern` reuses one private summary/resource preparation path instead of repeating that local setup.
- `LabCircuit` now routes repeated single-qubit and rotation delegation through private typed helpers, and Graphix command attribute extraction now reuses one internal fallback path for direct-versus-measurement metadata.
- `compare_backends()` now treats a single backend string as one backend instead of splitting it character by character, visualization now falls back from unusable causal-flow objects to `gflow` when available, and the Qiskit adapter now rejects boolean rotation angles instead of silently treating them as numeric values.
- Wrapped Graphix patterns now reject plain iterables and invalid pattern-like method return values more clearly, and syntactic traces no longer crash when an unexpected `E` command shape carries fewer than two nodes.
- `graphix_lab.cli.main(...)` now accepts full command strings programmatically instead of splitting them character by character, and `LabCircuit` rejects non-integer widths/qubit indices plus boolean rotation angles before those invalid values leak into the Graphix runtime.
- `LabCircuit` now rejects out-of-range qubit indices and `cnot` calls that target the same qubit, and `from_qiskit(...)` now validates `num_qubits` plus `find_bit(...).index` values before delegating into the Graphix runtime.
- `from_qiskit(...)` now rejects malformed Qiskit-like circuit structures with clear `TypeError` messages, including invalid `data` collections, incomplete instruction objects, and broken `find_bit(...)` results that previously leaked raw adapter exceptions.
- The tiny internal `process_runner` wrapper is gone; CLI/tooling subprocess calls now run directly, the bootstrap text-file passthrough was removed, and the `graphix_lab.app` package docstring now reflects the real application-service scope.
- Internal Graphix runtime import and callable resolution logic now goes through one shared helper module, which removes redundant compatibility code without changing the public API or CLI surface.
- Bootstrap scanning, temporary-workspace copying, cleanup rules, git ignores, and Ruff excludes now treat repo-local temp/cache directories more consistently, including `.pytest-tmp`, `.pytest_cache`, `.pyright`, `.hypothesis`, and `pytest-cache-files-*`.
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

- Pytest now disables the cacheprovider plugin in the shared project configuration, which avoids fragile cache-temp creation paths during local and CI runs on restricted Windows/Linux environments.
- Example smoke coverage now includes `examples/trace_animation.py`, `examples/library_usage.py`, and `examples/cli_usage.py`, and the README plus AI/developer guides now list those scripts explicitly.
- `docs/api.md` now documents the real `shift_signals()` wrapper behavior against the current Graphix runtime, including the fact that Graphix returns auxiliary signal-shift data while the Graphix Lab wrapper stays attached to the mutated pattern.
- The `quality` wrapper now runs package-import and CLI-help smoke checks before `pytest` and `pyright`, so local release verification catches editable-install regressions earlier and mirrors the CI release smoke more closely.
- CI now keeps the Windows and Ubuntu core matrix while adding explicit `python -m pip install -e .[dev]` release smoke for package import plus CLI help, and an isolated Ubuntu-only optional-Qiskit subset job that installs `.[qiskit,dev]`.
- Package metadata now uses Graphix Lab-specific keywords and classifiers plus repository and issue URLs, replacing the lingering generic template packaging identity.
- `THIRD_PARTY_LICENSES` has been regenerated after the current runtime dependency install, so the release inventory now reflects the active `.venv` package set, including the Graphix runtime dependencies needed by Graphix Lab.
- The README, quick start, guide, troubleshooting notes, AI fast-path guide, and Graphix Lab design docs now point to the live example scripts and describe the current repository workflow instead of the old template/demo flow.
- `docs/api.md` and `docs/graphix_lab/02_public_api_contract.md` now list the exact top-level exports and document the current `CommandRecord(kind="UNKNOWN")` fallback for Graphix command shapes that Graphix Lab does not name yet.
- `docs/api.md`, `docs/graphix_lab/02_public_api_contract.md`, and `docs/graphix_lab/05_qiskit_frontend.md` now document the live `from_qiskit(...)` behavior, including the supported gate subset, `find_bit(...)` qubit-index convention, angle conversion, and the current lack of measurement/bitstring translation.
- `docs/api.md` and `docs/graphix_lab/02_public_api_contract.md` now document the live `LabPattern.compare_backends(...)` API, including conservative backend selection, per-backend failure reporting, and the intentional lack of numerical-equivalence claims across backend result objects.
- `docs/api.md`, `docs/graphix_lab/00_project_scope.md`, `docs/graphix_lab/02_public_api_contract.md`, and `docs/graphix_lab/04_visualization_trace.md` now document the live slider-inspection API, including `TraceAnimationHandle`, `LabPattern.animate(...)`, the updated example flow, and the local Matplotlib step-highlighting behavior.
- `docs/api.md` now documents the standalone `LabPattern.trace()` API, including its conceptual-only scope, the post-command measurement convention, and the shared syntactic trace path used by `run(..., trace=True)`.
- `docs/api.md` now documents the live `LabPattern.run()` contract, including runtime-detected backend validation, Graphix delegation behavior, seed forwarding through NumPy RNG when available, and the lightweight trace included directly in `SimulationReport`.
- `docs/api.md` now documents the live structural summary/resource/explanation API and explains that detected input/output nodes are best-effort pedagogical inferences from pattern commands rather than deeper Graphix semantic analysis.
- The README and troubleshooting docs now state explicitly that changing `pyproject.toml` requires rerunning `python -m pip install -e .[dev]` inside `.venv` before relying on Graphix runtime features or quality results.
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
