Goal: add project-specific Graphix Lab documentation and dependency metadata while preserving the `vibe_template` structure.

Tasks:
1. Copy or recreate the project docs under `docs/graphix_lab/`:
   - `README.md`
   - `00_project_scope.md`
   - `01_architecture.md`
   - `02_public_api_contract.md`
   - `03_graphix_integration.md`
   - `04_visualization_trace.md`
   - `05_qiskit_frontend.md`
   - `06_testing_validation.md`
   - `07_release_packaging.md`
   - `08_roadmap.md`
   - `09_template_integration.md`
2. Add `docs/docs_for_ai/graphix_lab_status_addendum.md`.
3. Update `docs/README.md` to link to `docs/graphix_lab/README.md`.
4. Merge the Graphix Lab addendum into the root `README.md`, replacing template-only language where appropriate but preserving useful first-run/quality information.
5. Update `pyproject.toml` dependencies:
   - core: `graphix>=0.3.5,<0.4`, `matplotlib>=3.8`, `networkx>=3.2`, `numpy>=1.26`
   - optional `qiskit`: `qiskit>=2,<3`
   - optional `examples`: `jupyter>=1.1`
   - preserve existing `dev` dependencies
6. Do not add GPU/CUDA/MPI dependencies.
7. Update `THIRD_PARTY_LICENSES` if dependency installation is available; otherwise note that it must be regenerated.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.
