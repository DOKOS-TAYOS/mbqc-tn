# Status

- Phase: Prompt 01 completed for Graphix Lab docs and dependency metadata; implementation prompts have not started yet
- Last update: added the `docs/graphix_lab/` planning set, added `docs/docs_for_ai/graphix_lab_status_addendum.md`, rewrote the root README and docs index around Graphix Lab, and declared the Graphix, Matplotlib, NetworkX, NumPy, Qiskit, and examples dependency metadata in `pyproject.toml`
- Next step: Continue with `graphix_lab_vibe_template_codex_pack/prompts/02_graphix_capability_adapter.md`
- Blockers: `THIRD_PARTY_LICENSES` still reflects the pre-Graphix environment and must be regenerated after installing the new runtime dependencies in `.venv`
- Tests added: None; updated `tests/unit/test_template_footprint.py` so the footprint check expects the new AI addendum file
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
- [ ] `THIRD_PARTY_LICENSES` regenerated after installing Graphix Lab runtime dependencies
