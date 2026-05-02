from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def _load_wrapper_module() -> ModuleType:
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / "scripts" / "run_template_command.py"
    module_spec = importlib.util.spec_from_file_location("run_template_command", module_path)
    assert module_spec is not None
    assert module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def test_wrapper_launcher_prefers_windows_virtual_environment_python(temp_dir: Path) -> None:
    module = _load_wrapper_module()
    preferred_python = temp_dir / ".venv" / "Scripts" / "python.exe"
    preferred_python.parent.mkdir(parents=True)
    preferred_python.write_text("", encoding="utf-8")

    selected_python = module.select_python_executable(temp_dir)

    assert selected_python == preferred_python


def test_wrapper_launcher_builds_module_command(temp_dir: Path) -> None:
    module = _load_wrapper_module()
    preferred_python = temp_dir / ".venv" / "Scripts" / "python.exe"
    preferred_python.parent.mkdir(parents=True)
    preferred_python.write_text("", encoding="utf-8")
    (temp_dir / "pyproject.toml").write_text(
        """
[tool.vibe_template]
package_name = "bootstrap_cli_project"
""".strip(),
        encoding="utf-8",
    )

    command = module.build_command(temp_dir, ["bootstrap"])

    assert command == [str(preferred_python), "-m", "bootstrap_cli_project.cli", "bootstrap"]
