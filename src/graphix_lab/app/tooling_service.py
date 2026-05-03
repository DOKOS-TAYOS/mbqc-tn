from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname


@dataclass(frozen=True, slots=True)
class CommandExecutionResult:
    command: tuple[str, ...]
    returncode: int


def _build_module_command(module_name: str, *args: str) -> list[str]:
    return [sys.executable, "-m", module_name, *args]


def build_import_smoke_command(package_name: str) -> list[str]:
    return [
        sys.executable,
        "-c",
        f"import {package_name}; print({package_name}.__all__)",
    ]


def build_cli_help_command(package_name: str) -> list[str]:
    return [
        sys.executable,
        "-m",
        f"{package_name}.cli",
        "--help",
    ]


def build_quality_commands(project_root: Path, include_format_fix: bool = True) -> list[list[str]]:
    package_name = load_package_name(project_root)
    commands: list[list[str]] = [_build_module_command("ruff", "check", ".")]
    if include_format_fix:
        commands[0].append("--fix")
        commands.append(_build_module_command("ruff", "format", "."))
    else:
        commands.append(_build_module_command("ruff", "format", ".", "--check"))
    commands.extend(
        [
            build_import_smoke_command(package_name),
            build_cli_help_command(package_name),
            _build_module_command("pytest"),
            _build_module_command("pyright"),
        ]
    )
    return commands


def build_test_command() -> list[str]:
    return _build_module_command("pytest")


def build_bootstrap_resync_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-e",
        ".[dev]",
    ]


def load_distribution_name(project_root: Path) -> str:
    pyproject_data = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject_data["project"]["name"])


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


def _normalize_path_for_comparison(path: Path) -> str:
    return os.path.normcase(str(path.resolve()))


def _path_from_file_url(file_url: str) -> Path | None:
    parsed_url = urlparse(file_url)
    if parsed_url.scheme != "file":
        return None

    raw_path = parsed_url.path
    if parsed_url.netloc:
        raw_path = f"//{parsed_url.netloc}{parsed_url.path}"

    return Path(url2pathname(unquote(raw_path)))


def _distribution_points_to_project_root(
    direct_url_text: str,
    normalized_project_root: str,
) -> bool:
    try:
        direct_url_data = json.loads(direct_url_text)
    except json.JSONDecodeError:
        return False

    dir_info = direct_url_data.get("dir_info")
    if not isinstance(dir_info, dict) or dir_info.get("editable") is not True:
        return False

    distribution_url = direct_url_data.get("url")
    if not isinstance(distribution_url, str):
        return False

    distribution_path = _path_from_file_url(distribution_url)
    if distribution_path is None:
        return False

    return _normalize_path_for_comparison(distribution_path) == normalized_project_root


def _repo_local_editable_distribution_names(
    project_root: Path,
    distribution_name: str,
) -> list[str]:
    ignored_names = {distribution_name}
    normalized_project_root = _normalize_path_for_comparison(project_root)

    for distribution in metadata.distributions():
        try:
            direct_url_text = distribution.read_text("direct_url.json")
        except FileNotFoundError:
            direct_url_text = None

        if not direct_url_text or not _distribution_points_to_project_root(
            direct_url_text,
            normalized_project_root,
        ):
            continue

        editable_name = distribution.metadata["Name"]
        if isinstance(editable_name, str) and editable_name.strip():
            ignored_names.add(editable_name.strip())

    return sorted(ignored_names)


def build_license_command(
    output_file: Path,
    project_root: Path,
    distribution_name: str,
) -> list[str]:
    ignored_packages = _repo_local_editable_distribution_names(
        project_root=project_root,
        distribution_name=distribution_name,
    )

    return [
        sys.executable,
        "-m",
        "piplicenses",
        "--python",
        sys.executable,
        "--format=markdown",
        "--with-urls",
        "--ignore-packages",
        *ignored_packages,
        "--output-file",
        str(output_file),
    ]


def run_commands(commands: list[list[str]], root: Path) -> list[CommandExecutionResult]:
    results: list[CommandExecutionResult] = []
    for command in commands:
        completed_process = subprocess.run(command, check=False, cwd=root)
        results.append(
            CommandExecutionResult(
                command=tuple(command),
                returncode=completed_process.returncode,
            )
        )
        if completed_process.returncode != 0:
            break
    return results
