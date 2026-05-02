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
