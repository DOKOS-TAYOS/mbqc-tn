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
