Goal: implement a defensive Graphix capability adapter.

Read first:
- `docs/graphix_lab/03_graphix_integration.md`
- `docs/api.md`
- `docs/architecture.md`

Tasks:
1. Add tests for capability detection when Graphix is installed.
2. Add tests for the error message when Graphix is missing. Use monkeypatching rather than uninstalling dependencies.
3. Implement `src/graphix_lab/domain/errors.py` with at least:
   - `GraphixLabError`
   - `GraphixUnavailableError`
   - `GraphixCompatibilityError`
   - `UnsupportedBackendError`
   - `OptionalDependencyError`
   - `UnsupportedGateError`
4. Implement `src/graphix_lab/infrastructure/graphix_capabilities.py` with a frozen dataclass `GraphixCapabilities`.
5. Detect the installed Graphix version via `importlib.metadata.version("graphix")`.
6. Detect important APIs via `hasattr`, not by assuming one Graphix minor version.
7. Return supported backend names conservatively: include only Graphix built-in names that can be verified or documented in the installed API.
8. Add a small public function, probably `graphix_info()`, exported from `graphix_lab.__init__`.

Do not implement any simulation or wrappers yet. This task is only capability discovery and errors.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.
