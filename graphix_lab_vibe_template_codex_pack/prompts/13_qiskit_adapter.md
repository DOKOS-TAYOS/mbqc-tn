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
