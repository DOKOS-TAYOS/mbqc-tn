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
