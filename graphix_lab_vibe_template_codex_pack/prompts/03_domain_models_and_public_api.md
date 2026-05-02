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
