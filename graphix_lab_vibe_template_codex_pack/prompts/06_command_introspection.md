Goal: normalize Graphix pattern commands into stable `CommandRecord` objects.

Tasks:
1. Add tests using one-qubit and two-qubit compiled patterns.
2. Implement a Graphix command adapter in `infrastructure/graphix_adapter.py`.
3. Extract command records defensively from Graphix command objects.
4. Support known command kinds: `N`, `E`, `M`, `X`, `Z`, `C`.
5. Include fallback records for unknown command objects with `kind="UNKNOWN"` and a raw `repr`.
6. `CommandRecord` should include at least:
   - `index`
   - `kind`
   - `node`
   - `nodes`
   - `angle`
   - `plane`
   - `s_domain`
   - `t_domain`
   - `domain`
   - `raw`
7. Implement `LabPattern.commands() -> tuple[CommandRecord, ...]`.
8. Avoid depending on private Graphix attributes without fallback. If a private-looking attribute is unavoidable, isolate it in the adapter and test it.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.
