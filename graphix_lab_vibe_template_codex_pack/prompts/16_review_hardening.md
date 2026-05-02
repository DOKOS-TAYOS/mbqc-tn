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
