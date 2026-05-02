# Suggested `pyproject.toml` dependency patch

Apply after bootstrap and after checking that the project imports as `graphix_lab`.

## Core dependencies

```toml
dependencies = [
  "graphix>=0.3.5,<0.4",
  "matplotlib>=3.8",
  "networkx>=3.2",
  "numpy>=1.26",
]
```

## Optional dependencies

Preserve the existing `dev` extra from the template. Add optional extras carefully:

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

## Notes

- Do not add Qiskit as a core dependency.
- Do not add CUDA/GPU dependencies in the MVP.
- Keep the template's Hatch build backend.
- Keep `requires-python = ">=3.11"` unless tests prove a change is necessary.
- Regenerate `THIRD_PARTY_LICENSES` after dependency installation.
