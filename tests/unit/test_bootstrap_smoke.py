from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _load_bootstrap_smoke_module() -> ModuleType:
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / "scripts" / "bootstrap_smoke.py"
    module_spec = importlib.util.spec_from_file_location("bootstrap_smoke", module_path)
    assert module_spec is not None
    assert module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    sys.modules["bootstrap_smoke"] = module
    module_spec.loader.exec_module(module)
    return module


def test_copy_template_workspace_skips_local_artifacts(temp_dir: Path) -> None:
    module = _load_bootstrap_smoke_module()
    source_root = temp_dir / "source"
    workspace_root = temp_dir / "workspace"
    (source_root / ".git").mkdir(parents=True)
    (source_root / ".venv").mkdir()
    (source_root / "test-artifacts").mkdir()
    (source_root / "src").mkdir()
    (source_root / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (source_root / ".venv" / "marker.txt").write_text("venv\n", encoding="utf-8")
    (source_root / "test-artifacts" / "marker.txt").write_text("artifact\n", encoding="utf-8")
    (source_root / "src" / "kept.py").write_text("print('kept')\n", encoding="utf-8")

    module.copy_template_workspace(source_root, workspace_root)

    assert (workspace_root / "src" / "kept.py").exists()
    assert not (workspace_root / ".git").exists()
    assert not (workspace_root / ".venv").exists()
    assert not (workspace_root / "test-artifacts").exists()


def test_build_smoke_commands_use_workspace_python_and_noninteractive_bootstrap(
    temp_dir: Path,
) -> None:
    module = _load_bootstrap_smoke_module()
    workspace_root = temp_dir / "workspace"
    config = module.SmokeTestConfig(
        project_title="CI Template Smoke",
        distribution_name="ci-template-smoke",
        package_name="ci_template_smoke",
        author_name="CI Smoke",
        initial_version="0.1.0",
        project_scope="Fresh template smoke validation.",
        license_id="MIT",
    )

    commands = module.build_smoke_commands(workspace_root, config)
    workspace_python = module.build_workspace_python(workspace_root)

    assert commands[0] == [sys.executable, "-m", "venv", str(workspace_root / ".venv")]
    assert commands[1] == [str(workspace_python), "-m", "pip", "install", "--upgrade", "pip"]
    assert commands[2] == [str(workspace_python), "-m", "pip", "install", "-e", ".[dev]"]
    assert commands[3] == [
        str(workspace_python),
        str(workspace_root / "scripts" / "run_template_command.py"),
        "bootstrap",
        "--project-title",
        "CI Template Smoke",
        "--distribution-name",
        "ci-template-smoke",
        "--package-name",
        "ci_template_smoke",
        "--author-name",
        "CI Smoke",
        "--initial-version",
        "0.1.0",
        "--project-scope",
        "Fresh template smoke validation.",
        "--license-id",
        "MIT",
    ]
    assert commands[4] == [
        str(workspace_python),
        str(workspace_root / "scripts" / "run_template_command.py"),
        "quality",
    ]
