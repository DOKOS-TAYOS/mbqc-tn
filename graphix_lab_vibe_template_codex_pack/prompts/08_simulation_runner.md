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
