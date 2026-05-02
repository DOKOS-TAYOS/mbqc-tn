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
