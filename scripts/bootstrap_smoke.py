from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Final

IGNORE_PATTERNS: Final[tuple[str, ...]] = (
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".pyright",
    ".hypothesis",
    ".tmp",
    "build",
    "dist",
    "htmlcov",
    "*.egg-info",
    "test-artifacts",
    "pytest-cache",
    "pytest-temp",
    "pytest-cache-files-*",
)


@dataclass(frozen=True, slots=True)
class SmokeTestConfig:
    project_title: str
    distribution_name: str
    package_name: str
    author_name: str
    initial_version: str
    project_scope: str
    license_id: str


def build_workspace_python(workspace_root: Path) -> Path:
    if sys.platform == "win32":
        return workspace_root / ".venv" / "Scripts" / "python.exe"
    return workspace_root / ".venv" / "bin" / "python"


def copy_template_workspace(source_root: Path, workspace_root: Path) -> None:
    if workspace_root.exists():
        shutil.rmtree(workspace_root, ignore_errors=False)
    workspace_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source_root,
        workspace_root,
        ignore=shutil.ignore_patterns(*IGNORE_PATTERNS),
    )


def build_smoke_commands(workspace_root: Path, config: SmokeTestConfig) -> list[list[str]]:
    workspace_python = build_workspace_python(workspace_root)
    launcher_script = workspace_root / "scripts" / "run_template_command.py"
    return [
        [sys.executable, "-m", "venv", str(workspace_root / ".venv")],
        [str(workspace_python), "-m", "pip", "install", "--upgrade", "pip"],
        [str(workspace_python), "-m", "pip", "install", "-e", ".[dev]"],
        [
            str(workspace_python),
            str(launcher_script),
            "bootstrap",
            "--project-title",
            config.project_title,
            "--distribution-name",
            config.distribution_name,
            "--package-name",
            config.package_name,
            "--author-name",
            config.author_name,
            "--initial-version",
            config.initial_version,
            "--project-scope",
            config.project_scope,
            "--license-id",
            config.license_id,
        ],
        [
            str(workspace_python),
            str(launcher_script),
            "quality",
        ],
    ]


def run_smoke(source_root: Path, workspace_root: Path, config: SmokeTestConfig) -> int:
    copy_template_workspace(source_root, workspace_root)
    commands = build_smoke_commands(workspace_root, config)
    for command in commands:
        print(f"Running: {' '.join(command)}")
        completed_process = subprocess.run(command, check=False, cwd=workspace_root)
        if completed_process.returncode != 0:
            return completed_process.returncode
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a fresh template copy, bootstrap it, and run quality checks."
    )
    parser.add_argument(
        "--workspace-root",
        default=str(Path(tempfile.gettempdir()) / "vibe-template-smoke"),
    )
    parser.add_argument("--project-title", default="CI Template Smoke")
    parser.add_argument("--distribution-name", default="ci-template-smoke")
    parser.add_argument("--package-name", default="ci_template_smoke")
    parser.add_argument("--author-name", default="CI Smoke")
    parser.add_argument("--initial-version", default="0.1.0")
    parser.add_argument("--project-scope", default="Fresh template smoke validation.")
    parser.add_argument("--license-id", default="MIT")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    source_root = Path(__file__).resolve().parents[1]
    workspace_root = Path(args.workspace_root).resolve()
    config = SmokeTestConfig(
        project_title=args.project_title,
        distribution_name=args.distribution_name,
        package_name=args.package_name,
        author_name=args.author_name,
        initial_version=args.initial_version,
        project_scope=args.project_scope,
        license_id=args.license_id,
    )
    return run_smoke(source_root, workspace_root, config)


if __name__ == "__main__":
    raise SystemExit(main())
