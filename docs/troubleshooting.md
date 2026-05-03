# Troubleshooting

## `graphix_lab` Or Graphix Imports Fail

Make sure the active `.venv` is installed in editable mode:

```bash
python -m pip install -e .[dev]
```

If you just changed `pyproject.toml`, rerun that command before debugging the
runtime behavior.

## `qiskit_import.py` Says Qiskit Is Not Installed

That example is optional by design. Install the extra in the active `.venv`:

```bash
python -m pip install -e .[qiskit,dev]
```

## `licenses` Command Fails

Make sure the dev dependencies are installed in `.venv`:

```bash
python -m pip install -e .[dev]
```

The command only lists third-party packages from the active interpreter. If the
output looks wrong, confirm that you are using the intended `.venv`.

## `THIRD_PARTY_LICENSES` Shows `project-name` Or Another Local Alias

That means the active `.venv` still has an older editable install pointing at
this same repository. Recent `licenses` runs ignore repo-local editable aliases
automatically, but you can also clean up the environment and regenerate the
inventory:

```bash
python -m pip uninstall project-name
python scripts/run_template_command.py licenses
```

## `quality` Fails On Pyright

- check that `.venv` exists
- confirm the package imports from `src`
- keep function typing explicit

## Runtime Features Change After Editing `pyproject.toml`

Graphix Lab reads its runtime dependencies from the active `.venv`. If you
changed `pyproject.toml`, reinstall the editable project before debugging
Graphix-specific failures:

```bash
python -m pip install -e .[dev]
```

This refreshes both the Graphix runtime dependency and the local editable
package metadata.

## `bootstrap` Says The Template Was Already Bootstrapped

That is expected for this repository. Keep working in this checkout without
rerunning bootstrap. Only use bootstrap when validating a fresh template copy.

## Cleanup Removed Too Much

The cleanup command should never touch `.venv`. If it does, stop using that
version of the script and add a regression test before changing the cleanup
rules.
