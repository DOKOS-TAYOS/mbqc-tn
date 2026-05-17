from __future__ import annotations

import subprocess
import sys
import tomllib
from collections.abc import Sequence
from pathlib import Path


def select_python_executable(project_root: Path) -> Path:
    windows_python = project_root / ".venv" / "Scripts" / "python.exe"
    posix_python = project_root / ".venv" / "bin" / "python"

    if windows_python.exists():
        return windows_python
    if posix_python.exists():
        return posix_python
    return Path(sys.executable)


def load_package_name(project_root: Path) -> str:
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return "graphix_lab"

    pyproject_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    tool_data = pyproject_data.get("tool", {})
    template_data = tool_data.get("vibe_template", {})
    package_name = template_data.get("package_name")
    if isinstance(package_name, str) and package_name.strip():
        return package_name
    return "graphix_lab"


def build_command(project_root: Path, args: Sequence[str]) -> list[str]:
    python_executable = select_python_executable(project_root)
    package_name = load_package_name(project_root)
    return [str(python_executable), "-m", f"{package_name}.cli", *args]


def main(argv: Sequence[str] | None = None) -> int:
    project_root = Path(__file__).resolve().parents[1]
    command = build_command(project_root, list(argv) if argv is not None else sys.argv[1:])
    completed_process = subprocess.run(command, check=False, cwd=project_root)  # noqa: S603
    return completed_process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
