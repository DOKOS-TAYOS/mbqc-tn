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
