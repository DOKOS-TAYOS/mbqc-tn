# Template bootstrap values

Use this file when bootstrapping `DOKOS-TAYOS/vibe_template` into the Graphix Lab project.

## Values

```text
project_title: Graphix Lab
distribution_name: graphix-lab
package_name: graphix_lab
initial_version: 0.1.0
license_id: MIT
project_scope: A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends.
```

Set `author_name` to the public author or organization name you want in `pyproject.toml` and `LICENSE`.

## Linux/macOS command

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
./bin/bootstrap.sh \
  --project-title "Graphix Lab" \
  --distribution-name "graphix-lab" \
  --package-name "graphix_lab" \
  --author-name "Alejandro Mata Ali" \
  --initial-version "0.1.0" \
  --project-scope "A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends." \
  --license-id MIT
./bin/quality.sh
```

## Windows PowerShell command

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
bin\bootstrap.cmd `
  --project-title "Graphix Lab" `
  --distribution-name "graphix-lab" `
  --package-name "graphix_lab" `
  --author-name "Alejandro Mata Ali" `
  --initial-version "0.1.0" `
  --project-scope "A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends." `
  --license-id MIT
bin\quality.cmd
```

## Rules

- Run bootstrap once only.
- After bootstrap, use `graphix_lab` as the package import path.
- Keep the `bin/` wrappers as the preferred quality/test entrypoints.
- Keep the project MIT unless there is an explicit reason to change it.
