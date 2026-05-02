# All Codex prompts consolidated


## 00_template_bootstrap.md

You are working in a repository that must start from `https://github.com/DOKOS-TAYOS/vibe_template`.

Goal: bootstrap the template once into the Graphix Lab project. Do not scaffold a new Python project from scratch.

Tasks:
1. Inspect the existing template docs: `README.md`, `docs/quick-start.md`, `docs/guide.md`, `docs/api.md`, `docs/architecture.md`, `docs/docs_for_ai/project_ai_instructions.md`, and `docs/docs_for_ai/status.md`.
2. Create and activate `.venv` if it does not exist.
3. Install editable dev dependencies with `python -m pip install -e .[dev]`.
4. Run bootstrap non-interactively using the stable wrapper and these values:
   - project title: `Graphix Lab`
   - distribution name: `graphix-lab`
   - package name: `graphix_lab`
   - initial version: `0.1.0`
   - license id: `MIT`
   - project scope: `A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends.`
   - author name: keep the current public author name unless the repository owner asks for a different one.
5. Verify that `src/graphix_lab` was renamed to `src/graphix_lab` and that `pyproject.toml` points to `graphix_lab`.
6. Run the template quality wrapper.
7. Do not re-run bootstrap if `bootstrap_required` is already false.

Preferred Linux/macOS command:

```bash
./bin/bootstrap.sh \
  --project-title "Graphix Lab" \
  --distribution-name "graphix-lab" \
  --package-name "graphix_lab" \
  --author-name "Alejandro Mata Ali" \
  --initial-version "0.1.0" \
  --project-scope "A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends." \
  --license-id MIT
```

Preferred Windows command:

```powershell
bin\bootstrap.cmd `
  --project-title "Graphix Lab" `
  --distribution-name "graphix-lab" `
  --package-name "graphix_lab" `
  --author-name "Alejandro Mata Ali" `
  --initial-version "0.1.0" `
  --project-scope "A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends." `
  --license-id MIT
```


Completion requirements:
- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 01_project_docs_and_dependencies.md

Goal: add project-specific Graphix Lab documentation and dependency metadata while preserving the `vibe_template` structure.

Tasks:
1. Copy or recreate the project docs under `docs/graphix_lab/`:
   - `README.md`
   - `00_project_scope.md`
   - `01_architecture.md`
   - `02_public_api_contract.md`
   - `03_graphix_integration.md`
   - `04_visualization_trace.md`
   - `05_qiskit_frontend.md`
   - `06_testing_validation.md`
   - `07_release_packaging.md`
   - `08_roadmap.md`
   - `09_template_integration.md`
2. Add `docs/docs_for_ai/graphix_lab_status_addendum.md`.
3. Update `docs/README.md` to link to `docs/graphix_lab/README.md`.
4. Merge the Graphix Lab addendum into the root `README.md`, replacing template-only language where appropriate but preserving useful first-run/quality information.
5. Update `pyproject.toml` dependencies:
   - core: `graphix>=0.3.5,<0.4`, `matplotlib>=3.8`, `networkx>=3.2`, `numpy>=1.26`
   - optional `qiskit`: `qiskit>=2,<3`
   - optional `examples`: `jupyter>=1.1`
   - preserve existing `dev` dependencies
6. Do not add GPU/CUDA/MPI dependencies.
7. Update `THIRD_PARTY_LICENSES` if dependency installation is available; otherwise note that it must be regenerated.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 02_graphix_capability_adapter.md

Goal: implement a defensive Graphix capability adapter.

Read first:
- `docs/graphix_lab/03_graphix_integration.md`
- `docs/api.md`
- `docs/architecture.md`

Tasks:
1. Add tests for capability detection when Graphix is installed.
2. Add tests for the error message when Graphix is missing. Use monkeypatching rather than uninstalling dependencies.
3. Implement `src/graphix_lab/domain/errors.py` with at least:
   - `GraphixLabError`
   - `GraphixUnavailableError`
   - `GraphixCompatibilityError`
   - `UnsupportedBackendError`
   - `OptionalDependencyError`
   - `UnsupportedGateError`
4. Implement `src/graphix_lab/infrastructure/graphix_capabilities.py` with a frozen dataclass `GraphixCapabilities`.
5. Detect the installed Graphix version via `importlib.metadata.version("graphix")`.
6. Detect important APIs via `hasattr`, not by assuming one Graphix minor version.
7. Return supported backend names conservatively: include only Graphix built-in names that can be verified or documented in the installed API.
8. Add a small public function, probably `graphix_info()`, exported from `graphix_lab.__init__`.

Do not implement any simulation or wrappers yet. This task is only capability discovery and errors.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 03_domain_models_and_public_api.md

Goal: replace the template placeholder public API with the initial Graphix Lab domain model and public exports.

Tasks:
1. Add tests that import the intended public API from `graphix_lab`.
2. Remove or deprecate the template-only `TemplateMetadata` public API from `__init__.py`, unless tests still require it. If removed, update docs/tests accordingly.
3. Implement typed frozen dataclasses:
   - `CommandRecord`
   - `PatternSummary`
   - `ResourceSummary`
   - `TraceFrame`
   - `RunTrace`
   - `SimulationReport`
   - `BackendRunReport`
   - `BackendComparisonReport`
4. Keep domain modules dependency-light. Domain modules should not import Graphix, Qiskit, Matplotlib, or NetworkX.
5. Export only the stable public names from `graphix_lab.__init__`.
6. Keep the CLI working after the public API change.
7. Update `docs/api.md` with the new public API contract.

Do not implement Graphix wrappers yet except for harmless stubs if needed by imports.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 04_lab_circuit_wrapper.md

Goal: implement `LabCircuit` as a fluent wrapper around `graphix.Circuit`.

Tasks:
1. Add tests for `graphix_lab.circuit(width)` returning a `LabCircuit`.
2. Add tests for chaining `.h`, `.x`, `.y`, `.z`, `.s`, `.rx`, `.ry`, `.rz`, and `.cnot`.
3. Implement `LabCircuit` in the app/domain split that best fits the existing architecture.
4. Internally delegate to `graphix.Circuit`.
5. Implement `.to_graphix()` returning the wrapped Graphix circuit.
6. Implement `.compile()` returning a `LabPattern` wrapper around `circuit.transpile().pattern`.
7. Make angle units explicit:
   - default `units="pi"` should pass through to Graphix
   - `units="radians"` should divide by `math.pi`
   - unsupported units should raise a clear `ValueError` or domain-specific error
8. Do not add Qiskit support in this prompt.
9. Update `docs/api.md` and examples if needed.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 05_lab_pattern_wrapper.md

Goal: implement `LabPattern` as a wrapper around a Graphix pattern.

Tasks:
1. Add tests that compile a small `LabCircuit` into `LabPattern`.
2. Add `from_graphix_pattern(pattern)` top-level function.
3. Implement `LabPattern.to_graphix()`.
4. Implement wrapper methods:
   - `.copy()` if a safe copy path exists; otherwise document mutating behavior clearly
   - `.standardize()`
   - `.shift_signals()`
   - `.perform_pauli_measurements()`
5. For Graphix methods that may not exist in some versions, use `hasattr` and raise `GraphixCompatibilityError` with a clear message.
6. Decide and document mutation semantics. Preferred: methods mutate the underlying Graphix pattern and return `self` for fluent use, unless a reliable Graphix copy mechanism exists.
7. Add tests for method chaining.
8. Update `docs/api.md`.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 06_command_introspection.md

Goal: normalize Graphix pattern commands into stable `CommandRecord` objects.

Tasks:
1. Add tests using one-qubit and two-qubit compiled patterns.
2. Implement a Graphix command adapter in `infrastructure/graphix_adapter.py`.
3. Extract command records defensively from Graphix command objects.
4. Support known command kinds: `N`, `E`, `M`, `X`, `Z`, `C`.
5. Include fallback records for unknown command objects with `kind="UNKNOWN"` and a raw `repr`.
6. `CommandRecord` should include at least:
   - `index`
   - `kind`
   - `node`
   - `nodes`
   - `angle`
   - `plane`
   - `s_domain`
   - `t_domain`
   - `domain`
   - `raw`
7. Implement `LabPattern.commands() -> tuple[CommandRecord, ...]`.
8. Avoid depending on private Graphix attributes without fallback. If a private-looking attribute is unavoidable, isolate it in the adapter and test it.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 07_summary_explain_resources.md

Goal: implement readable summaries, resource estimates, and explanations.

Tasks:
1. Add tests for `.summary()`, `.resources()`, and `.explain()` on small patterns.
2. Implement `ResourceSummary` with at least:
   - number of commands
   - command counts by kind
   - number of nodes seen
   - number of entanglement edges
   - number of measurements
   - number of X corrections
   - number of Z corrections
   - input nodes if detectable
   - output nodes if detectable
3. Implement `PatternSummary` with readable fields and a stable string representation.
4. Implement `LabPattern.summary()` returning `PatternSummary`.
5. Implement `LabPattern.resources()` returning `ResourceSummary`.
6. Implement `LabPattern.explain()` returning a concise human-readable multi-line string.
7. Do not overpromise physical simulation complexity. Summaries are structural and pedagogical.
8. Update `docs/api.md`.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 08_simulation_runner.md

Goal: implement a Graphix-delegated simulation runner and `SimulationReport`.

Tasks:
1. Add tests for `LabPattern.run(backend="statevector", seed=123)` on a small pattern.
2. Add tests for clear errors on unsupported backends.
3. Implement `LabPattern.run(...)` by delegating to Graphix:
   - prefer `pattern.simulate_pattern(backend=...)` if available
   - otherwise use `graphix.simulator.PatternSimulator` if available
4. Support at least `statevector` when Graphix supports it.
5. Support `densitymatrix`, `tensornetwork`, and `mps` only if the installed Graphix version supports them and tests can run or skip cleanly.
6. Use NumPy random generator seeding if Graphix accepts an RNG path. If Graphix's high-level method does not accept RNG, document/report that the seed could not be applied.
7. Return `SimulationReport` with:
   - backend
   - elapsed time
   - raw result object
   - result type string
   - seed
   - warnings or notes
   - optional `RunTrace` if `trace=True`
8. Do not implement shots unless there is a clear Graphix-supported semantics. Prefer one simulation run for MVP.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 09_syntactic_trace.md

Goal: implement a syntactic MBQC command trace independent of Graphix simulator internals.

Tasks:
1. Add tests for `LabPattern.trace()` on a small pattern.
2. Implement `RunTrace` construction from `CommandRecord` objects.
3. Each `TraceFrame` should capture:
   - step index
   - command kind
   - current node or nodes
   - measured nodes so far
   - pending nodes
   - active correction notes
   - readable description
4. For `M` commands, mark the node as measured after the frame or during the frame consistently and document the convention.
5. For `X` and `Z` commands, add correction dependency descriptions from domains.
6. Do not claim that this trace is the exact internal Graphix simulation trajectory. It is a conceptual/syntactic trace of the command list.
7. Integrate `trace=True` in `LabPattern.run(...)` if not already done.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 10_static_visualization.md

Goal: implement static MBQC visualization using Matplotlib and NetworkX, with Graphix fallback/delegation where useful.

Tasks:
1. Add tests using a non-interactive Matplotlib backend.
2. Implement graph extraction from `CommandRecord` objects:
   - nodes from all command records
   - edges from `E` records
   - measured nodes from `M` records
   - correction dependencies from `X`, `Z`, and measurement domains when available
3. Implement `LabPattern.draw(...)` returning a Matplotlib `Figure`.
4. Allow options such as:
   - `show_flow: bool = True`
   - `show_corrections: bool = True`
   - `layout: str = "auto"`
   - `ax: matplotlib.axes.Axes | None = None`
5. If Graphix exposes a suitable draw method and the caller requests delegation, allow delegating. Otherwise, use the local NetworkX/Matplotlib renderer.
6. Do not require a display server.
7. Update visualization docs.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 11_matplotlib_slider.md

Goal: implement a Matplotlib slider for conceptual trace inspection.

Tasks:
1. Add tests that create the slider handle without opening a GUI.
2. Implement a small handle dataclass, for example `TraceAnimationHandle`, containing figure, axes, slider, trace, and update callback references.
3. Implement `RunTrace.animate(...)` or `LabPattern.animate(...)` using `matplotlib.widgets.Slider`.
4. The slider should update:
   - title or step label
   - highlighted current node(s)
   - measured/pending node styling
   - a text box with the current command description
5. Keep the implementation simple and robust. Do not introduce a web GUI or notebook-only dependency.
6. Ensure references are retained so callbacks are not garbage-collected.
7. Update docs and examples.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 12_backend_comparison.md

Goal: implement backend comparison reports for available Graphix backends.

Tasks:
1. Add tests for comparing at least one supported backend on a small pattern.
2. Implement `LabPattern.compare_backends(backends: Sequence[str] | None = None, ...)`.
3. Default to a conservative backend list from Graphix capabilities.
4. For each backend, capture:
   - backend name
   - success/failure
   - elapsed time
   - result type
   - error message if failed
   - warnings/notes
5. Return `BackendComparisonReport`.
6. Do not attempt to compute numerical equivalence unless there is a clear, tested conversion to comparable state data.
7. Add a readable table/string method for reports.
8. Update docs.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 13_qiskit_adapter.md

Goal: implement optional Qiskit import for a small gate subset.

Tasks:
1. Add tests guarded with `pytest.importorskip("qiskit")`.
2. Add tests for missing Qiskit using monkeypatching/import isolation and ensure `OptionalDependencyError` is clear.
3. Implement `from_qiskit(qc, *, angle_units="radians") -> LabCircuit`.
4. Support only:
   - `h`
   - `x`
   - `y`
   - `z`
   - `s`
   - `rx`
   - `ry`
   - `rz`
   - `cx` / `cnot`
5. Convert radians to Graphix π units for rotations by dividing by `math.pi`.
6. Raise `UnsupportedGateError` for unsupported instructions with gate name and instruction index.
7. Document qubit ordering and bitstring convention limitations.
8. Keep Qiskit as an optional dependency only.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 14_examples_and_docs.md

Goal: add educational examples and synchronize docs with the implemented API.

Tasks:
1. Add simple example scripts under `examples/`:
   - `one_qubit_rotation.py`
   - `bell_like_pattern.py`
   - `trace_slider.py`
   - `backend_comparison.py`
   - `qiskit_import.py` if Qiskit extra is available
2. Ensure examples can be run as scripts.
3. Add tests or smoke checks for examples where practical.
4. Update root `README.md` with a minimal example and installation instructions.
5. Update `docs/api.md` to match the current public API exactly.
6. Update `docs/graphix_lab/` docs where implementation differs from the original plan.
7. Avoid notebooks until the script examples are stable.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 15_ci_packaging_release.md

Goal: harden CI, packaging metadata, and release readiness while preserving the template wrappers.

Tasks:
1. Inspect existing `.github/workflows` from the template.
2. Preserve Windows and Ubuntu coverage unless there is a strong reason to change it.
3. Ensure tests run with core dependencies installed.
4. Add optional Qiskit tests only if the workflow can keep them isolated or skipped when unavailable.
5. Confirm `python -m pip install -e .[dev]` works.
6. Confirm package import works:
   - `python -c "import graphix_lab; print(graphix_lab.__all__)"`
7. Confirm the CLI still works or update CLI tests/docs.
8. Regenerate `THIRD_PARTY_LICENSES` if possible.
9. Update `CHANGELOG.md` with an unreleased MVP section.
10. Do not publish to PyPI in this prompt.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## 16_review_hardening.md

Goal: review and harden the current Graphix Lab implementation before accepting the MVP.

Tasks:
1. Read the project docs and compare them with the actual public API.
2. Run the full quality flow.
3. Look for accidental reimplementation of Graphix internals. Replace with delegation where appropriate.
4. Look for private Graphix attribute assumptions. Isolate or guard them.
5. Look for optional dependencies imported at module import time. Move them into adapters.
6. Check error messages for clarity.
7. Check that `docs/docs_for_ai/status.md` names the true next step and blockers.
8. Check that examples match the current implementation.
9. Produce a concise review summary with:
   - pass/fail status
   - files changed
   - tests run
   - remaining risks
   - recommended next prompt

Do not add new features during this review unless needed to fix a correctness or packaging problem.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.


## MASTER_SEQUENCE.md

# Master sequence for Codex

Use these prompts in order. Stop after any prompt that fails quality checks and fix the failure before continuing.

## Sprint 0

1. `00_template_bootstrap.md`
2. `01_project_docs_and_dependencies.md`

## Sprint 1: minimum useful library

3. `02_graphix_capability_adapter.md`
4. `03_domain_models_and_public_api.md`
5. `04_lab_circuit_wrapper.md`
6. `05_lab_pattern_wrapper.md`
7. `06_command_introspection.md`
8. `07_summary_explain_resources.md`
9. `08_simulation_runner.md`

At this point, there should be a useful non-visual MVP.

## Sprint 2: teaching and visualization

10. `09_syntactic_trace.md`
11. `10_static_visualization.md`
12. `11_matplotlib_slider.md`

At this point, there should be an educational MVP.

## Sprint 3: optional extras

13. `12_backend_comparison.md`
14. `13_qiskit_adapter.md`
15. `14_examples_and_docs.md`
16. `15_ci_packaging_release.md`
17. `16_review_hardening.md`

## Review

Use `REVIEW_PROMPT.md` before accepting or merging an MVP branch.


## REVIEW_PROMPT.md

You are reviewing a branch of Graphix Lab, a library built from `DOKOS-TAYOS/vibe_template` as a usability layer over Graphix.

Review checklist:
1. Confirm the repository was bootstrapped once and imports as `graphix_lab`.
2. Confirm the public API is small and documented in `docs/api.md`.
3. Confirm Graphix is delegated to for MBQC semantics.
4. Confirm optional dependencies, especially Qiskit, are not imported by the core package at import time.
5. Confirm visualization uses Matplotlib/NetworkX and does not require a display in tests.
6. Confirm domain objects do not import Graphix/Qiskit/Matplotlib/NetworkX unnecessarily.
7. Confirm all meaningful changes update tests, `CHANGELOG.md`, and `docs/docs_for_ai/status.md`.
8. Run the full quality command.
9. Report exact failures instead of saying the branch is ready.

Output format:

```text
Status: PASS | FAIL
Summary:
Files inspected:
Tests run:
Failures/blockers:
Risks:
Recommended next step:
```
