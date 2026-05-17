# Security Policy

## Supported Versions

Security support applies to the latest maintained Graphix Lab branch. Pre-release
work should still treat dependency alerts and CI security failures as blocking
for release.

## Reporting a Vulnerability

Use GitHub private vulnerability reporting when it is available for the
repository. Otherwise, contact the maintainer privately before opening a public
issue. Do not publish suspected secret leaks, exploitable crashes, or dependency
vulnerabilities publicly until the maintainer confirms the handling plan.

## Dependency Security

Dependabot monitors Python dependencies and GitHub Actions through
`.github/dependabot.yml`. CI also runs a dependency vulnerability audit with:

```powershell
python scripts/run_template_command.py security
```

On Windows, install the development extra inside `.venv` before running the
audit so the local certificate handling helper is available:

```powershell
python -m pip install -e .[dev]
```

## PyPI Publishing

When Graphix Lab is ready for PyPI, prefer PyPI Trusted Publishing from a
dedicated GitHub Actions release workflow and environment. Do not store long
lived PyPI API tokens in the repository.
