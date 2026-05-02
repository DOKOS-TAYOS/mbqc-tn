You are working in a repository that must start from `https://github.com/DOKOS-TAYOS/vibe_template`.

Goal: bootstrap the template once into the Graphix Lab project. Do not scaffold a new Python project from scratch.

Tasks:
1. Inspect the existing template docs: `README.md`, `docs/quick-start.md`, `docs/guide.md`, `docs/api.md`, `docs/architecture.md`, `docs/docs_for_ai/project_ai_instructions.md`, and `docs/docs_for_ai/status.md`.
2. Create and activate `.venv` if it does not exist.
3. Install editable dev dependencies with `python -m pip install -e .[dev]`.
4. Run bootstrap non-interactively using the stable wrapper and these values:
   - project title: `Graphix Lab`
   - distribution name: `graphix-lab`
   - package name: `graphix_lab`
   - initial version: `0.1.0`
   - license id: `MIT`
   - project scope: `A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends.`
   - author name: keep the current public author name unless the repository owner asks for a different one.
5. Verify that `src/graphix_lab` was renamed to `src/graphix_lab` and that `pyproject.toml` points to `graphix_lab`.
6. Run the template quality wrapper.
7. Do not re-run bootstrap if `bootstrap_required` is already false.

Preferred Linux/macOS command:

```bash
./bin/bootstrap.sh \
  --project-title "Graphix Lab" \
  --distribution-name "graphix-lab" \
  --package-name "graphix_lab" \
  --author-name "Alejandro Mata Ali" \
  --initial-version "0.1.0" \
  --project-scope "A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends." \
  --license-id MIT
```

Preferred Windows command:

```powershell
bin\bootstrap.cmd `
  --project-title "Graphix Lab" `
  --distribution-name "graphix-lab" `
  --package-name "graphix_lab" `
  --author-name "Alejandro Mata Ali" `
  --initial-version "0.1.0" `
  --project-scope "A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends." `
  --license-id MIT
```


Completion requirements:
- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.

