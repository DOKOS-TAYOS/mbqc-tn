You are reviewing a branch of Graphix Lab, a library built from `DOKOS-TAYOS/vibe_template` as a usability layer over Graphix.

Review checklist:
1. Confirm the repository was bootstrapped once and imports as `graphix_lab`.
2. Confirm the public API is small and documented in `docs/api.md`.
3. Confirm Graphix is delegated to for MBQC semantics.
4. Confirm optional dependencies, especially Qiskit, are not imported by the core package at import time.
5. Confirm visualization uses Matplotlib/NetworkX and does not require a display in tests.
6. Confirm domain objects do not import Graphix/Qiskit/Matplotlib/NetworkX unnecessarily.
7. Confirm all meaningful changes update tests, `CHANGELOG.md`, and `docs/docs_for_ai/status.md`.
8. Run the full quality command.
9. Report exact failures instead of saying the branch is ready.

Output format:

```text
Status: PASS | FAIL
Summary:
Files inspected:
Tests run:
Failures/blockers:
Risks:
Recommended next step:
```
