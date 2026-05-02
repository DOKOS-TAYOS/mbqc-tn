# Master sequence for Codex

Use these prompts in order. Stop after any prompt that fails quality checks and fix the failure before continuing.

## Sprint 0

1. `00_template_bootstrap.md`
2. `01_project_docs_and_dependencies.md`

## Sprint 1: minimum useful library

3. `02_graphix_capability_adapter.md`
4. `03_domain_models_and_public_api.md`
5. `04_lab_circuit_wrapper.md`
6. `05_lab_pattern_wrapper.md`
7. `06_command_introspection.md`
8. `07_summary_explain_resources.md`
9. `08_simulation_runner.md`

At this point, there should be a useful non-visual MVP.

## Sprint 2: teaching and visualization

10. `09_syntactic_trace.md`
11. `10_static_visualization.md`
12. `11_matplotlib_slider.md`

At this point, there should be an educational MVP.

## Sprint 3: optional extras

13. `12_backend_comparison.md`
14. `13_qiskit_adapter.md`
15. `14_examples_and_docs.md`
16. `15_ci_packaging_release.md`
17. `16_review_hardening.md`

## Review

Use `REVIEW_PROMPT.md` before accepting or merging an MVP branch.
