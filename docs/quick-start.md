# Quick Start

Use this document only for the first start of a new project created from the template.

## 1. Create the Environment and Install the Template

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

## 2. Bootstrap the Project Identity

Windows PowerShell:

```powershell
bin\bootstrap.cmd
```

Linux or macOS:

```bash
./bin/bootstrap.sh
```

Bootstrap asks for the project identity fields and then runs `pip install -e .[dev]` again automatically so the renamed package is ready without extra manual steps. Run it only once per fresh copy of the template.

## 3. Verify the Base

Windows PowerShell:

```powershell
bin\quality.cmd
```

Linux or macOS:

```bash
./bin/quality.sh
```

## 4. Start Building

- keep the public API minimal
- add tests before behavior changes
- update `CHANGELOG.md`
- update `docs/docs_for_ai/status.md`
