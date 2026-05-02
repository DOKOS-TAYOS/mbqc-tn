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
