# Status

- Phase: Prompt 02 completed for the Graphix capability adapter; wrapper and pattern implementations have not started yet
- Last update: added typed Graphix domain errors, implemented defensive runtime capability discovery in `src/graphix_lab/infrastructure/graphix_capabilities.py`, exported public `graphix_info()`, and added unit coverage for installed and missing Graphix runtime detection
- Next step: Continue with `graphix_lab_vibe_template_codex_pack/prompts/03_domain_models_and_public_api.md`
- Blockers: Graphix is still not installed in the active `.venv`, so `graphix_info()` currently raises `GraphixUnavailableError` in this checkout until runtime dependencies are installed; `THIRD_PARTY_LICENSES` also still reflects the pre-Graphix environment
- Tests added: `tests/unit/test_graphix_capabilities.py` covers capability discovery with monkeypatched Graphix modules and the clear missing-dependency error path; `tests/unit/test_public_api.py` now checks that `graphix_info` is exported
- Quality command result: `bin\quality.cmd` passed with `ruff check . --fix`, `ruff format .`, `pytest`, and `pyright`
- License: MIT

## Checklist

- [x] Library-first package structure exists
- [x] CLI commands exist
- [x] Human documentation baseline exists
- [x] AI documentation baseline exists
- [x] Bootstrap resyncs the editable install
- [x] Bootstrap refuses re-running after template setup is complete
- [x] CI validates a fresh template copy through bootstrap plus quality
- [x] Minimal stable wrappers exist
- [x] Cleanup command protects `.venv`
- [x] Cleanup tolerates inaccessible subtrees conservatively
- [x] Project-specific bootstrap completed
- [x] Third-party license inventory regenerated after the initial bootstrap dependency install
- [x] Graphix Lab planning docs exist under `docs/graphix_lab`
- [x] Graphix Lab AI status addendum exists
- [x] Root docs now point to the Graphix Lab planning set
- [x] `pyproject.toml` declares Graphix Lab runtime and optional dependency metadata
- [x] Graphix capability detection now inspects the installed runtime defensively
- [x] Missing Graphix now raises a clear domain error instead of a raw import failure
- [ ] `THIRD_PARTY_LICENSES` regenerated after installing Graphix Lab runtime dependencies
