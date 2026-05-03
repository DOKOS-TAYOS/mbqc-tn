# Quick Start

Use this guide for the current Graphix Lab repository.

## 1. Create the Environment and Install

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Linux or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

If you want the optional Qiskit example too, use:

```bash
python -m pip install -e .[qiskit,dev]
```

## 2. Run a Couple of Examples

Windows PowerShell:

```powershell
.venv\Scripts\python.exe examples\one_qubit_rotation.py
.venv\Scripts\python.exe examples\backend_comparison.py
```

Linux or macOS:

```bash
.venv/bin/python examples/one_qubit_rotation.py
.venv/bin/python examples/backend_comparison.py
```

Optional example:

- `examples/trace_slider.py` opens a Matplotlib-backed trace viewer.
- `examples/qiskit_import.py` prints a friendly message when `qiskit` is not
  installed yet.

## 3. Run the Quality Flow

Windows PowerShell:

```powershell
bin\quality.cmd
```

Linux or macOS:

```bash
./bin/quality.sh
```

## 4. Keep the Environment Fresh

- If you edit `pyproject.toml`, rerun `python -m pip install -e .[dev]`
  inside `.venv`.
- If dependency changes affect third-party packages, regenerate
  `THIRD_PARTY_LICENSES` with `python scripts/run_template_command.py licenses`.
- When you change public behavior, update `CHANGELOG.md` and
  `docs/docs_for_ai/status.md`.
