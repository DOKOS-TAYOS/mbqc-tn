# Release and packaging

## License

Graphix Lab code should be MIT. Graphix itself is an Apache-2.0 dependency. Do not copy Graphix source code into this repository.

## Dependencies

Core dependencies should stay small:

```toml
dependencies = [
  "graphix>=0.3.5,<0.4",
  "matplotlib>=3.8",
  "networkx>=3.2",
  "numpy>=1.26",
]
```

Optional extras:

```toml
[project.optional-dependencies]
qiskit = ["qiskit>=2,<3"]
examples = ["jupyter>=1.1"]
dev = [
  "pip-licenses>=5.0.0",
  "pyright>=1.1.408",
  "pytest>=8.4.2",
  "ruff>=0.11.11",
]
```

Adjust versions if tests prove a different compatibility range.

## Distribution

Suggested package metadata:

- distribution name: `graphix-lab`
- import package: `graphix_lab`
- license: MIT
- Python: `>=3.11`
- development status: pre-alpha until MVP is validated
- repository metadata should point at `https://github.com/DOKOS-TAYOS/mbqc-tn`
- keywords and classifiers should describe MBQC / Graphix usage instead of the
  old generic template identity

## Third-party licenses

After the Graphix Lab runtime dependencies are installed, regenerate `THIRD_PARTY_LICENSES` from the repository root:

```powershell
python scripts/run_template_command.py licenses
```

If you prefer the direct module entrypoint, run the same command through the activated project interpreter:

```bash
python -m graphix_lab.cli licenses
```

There is currently no dedicated `bin/licenses` wrapper in this repository.

## Release smoke checks

Before tagging or publishing, confirm the editable install, package import, and
CLI entrypoint from the active `.venv`:

```powershell
python -m pip install -e .[dev]
python -c "import graphix_lab; print(graphix_lab.__all__)"
python -m graphix_lab.cli --help
```

The `quality` wrapper now includes the package-import and CLI-help smoke checks
before `pytest` and `pyright`, so local release verification stays aligned with
CI.

## CI expectations

- Keep both `windows-latest` and `ubuntu-latest` in the main test matrix.
- Keep optional Qiskit coverage isolated in its own job so the core matrix can
  still pass without the extra installed.

## Do not publish until

- public API docs match implementation
- examples run
- Graphix compatibility checks pass
- `THIRD_PARTY_LICENSES` is regenerated
- `CHANGELOG.md` is updated
- package import and CLI smoke tests pass
