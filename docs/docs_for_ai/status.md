# Status

- Phase: Prompt 03 completed for domain models and the initial Graphix Lab public API; Graphix-backed circuit and pattern behavior is still deferred to later prompts
- Last update: added frozen domain dataclasses for commands, summaries, traces, simulations, and backend comparisons; replaced the top-level placeholder metadata API with the Graphix Lab public surface; added lightweight `LabCircuit` and `LabPattern` stubs; and updated the API docs plus library example to match
- Next step: Continue with `graphix_lab_vibe_template_codex_pack/prompts/04_lab_circuit_wrapper.md`
- Blockers: Graphix is still not installed in the active `.venv`, so `graphix_info()` currently raises `GraphixUnavailableError` in this checkout until runtime dependencies are installed; the new wrapper entrypoints are intentionally stubs until Prompt 04 and Prompt 05; `THIRD_PARTY_LICENSES` also still reflects the pre-Graphix environment
- Tests added: `tests/unit/test_public_api.py` now checks the exported Graphix Lab models, immutable report dataclasses, lightweight wrapper stubs, and the clear `from_qiskit` placeholder error; `tests/smoke/test_examples.py` now validates the updated library example output against the new public API
- Quality command result: `bin\quality.cmd` passed with `ruff check . --fix`, `ruff format .`, `pytest`, and `pyright`; the first in-sandbox pytest run hit a Windows temp-directory permission boundary, but the full repo run passed once allowed to use the normal temp location
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
- [x] Initial Graphix Lab public domain models are exported from `graphix_lab`
- [x] Template metadata is no longer part of the public top-level API
- [ ] `THIRD_PARTY_LICENSES` regenerated after installing Graphix Lab runtime dependencies
