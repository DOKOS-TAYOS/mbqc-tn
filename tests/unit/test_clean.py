from __future__ import annotations

import os
from os import PathLike
from pathlib import Path

import pytest

from project_name.app.clean_service import collect_cleanup_paths, run_clean


def test_collect_cleanup_paths_ignores_virtual_environment(temp_dir: Path) -> None:
    cache_dir = temp_dir / ".pytest_cache"
    cache_dir.mkdir()
    venv_cache = temp_dir / ".venv" / ".pytest_cache"
    venv_cache.mkdir(parents=True)
    log_file = temp_dir / "service.log"
    log_file.write_text("log", encoding="utf-8")

    cleanup_paths = collect_cleanup_paths(temp_dir)

    assert cache_dir in cleanup_paths
    assert log_file in cleanup_paths
    assert venv_cache not in cleanup_paths


def test_collect_cleanup_paths_removes_nested_python_caches(temp_dir: Path) -> None:
    pycache_dir = temp_dir / "src" / "project_name" / "__pycache__"
    pycache_dir.mkdir(parents=True)

    cleanup_paths = collect_cleanup_paths(temp_dir)

    assert pycache_dir in cleanup_paths


def test_collect_cleanup_paths_matches_generated_pytest_cache_directories(temp_dir: Path) -> None:
    generated_cache_dir = temp_dir / "pytest-cache-files-abc123"
    generated_cache_dir.mkdir()

    cleanup_paths = collect_cleanup_paths(temp_dir)

    assert generated_cache_dir in cleanup_paths


def test_collect_cleanup_paths_skips_directories_that_contain_nested_virtual_environments(
    temp_dir: Path,
) -> None:
    artifact_dir = temp_dir / "test-artifacts"
    nested_venv = artifact_dir / ".venv" / "Scripts"
    nested_venv.mkdir(parents=True)

    cleanup_paths = collect_cleanup_paths(temp_dir)

    assert artifact_dir not in cleanup_paths


def test_collect_cleanup_paths_skips_permission_denied_subtrees(
    temp_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    artifact_dir = temp_dir / "test-artifacts"
    artifact_dir.mkdir()
    accessible_cache_dir = temp_dir / ".pytest_cache"
    accessible_cache_dir.mkdir()
    original_scandir = os.scandir

    def patched_scandir(path: str | PathLike[str]) -> object:
        if Path(path) == artifact_dir:
            raise PermissionError(f"blocked: {path}")
        return original_scandir(path)

    monkeypatch.setattr(os, "scandir", patched_scandir)

    cleanup_paths = collect_cleanup_paths(temp_dir)

    assert accessible_cache_dir in cleanup_paths
    assert artifact_dir not in cleanup_paths


def test_run_clean_reports_permission_errors_and_continues(
    temp_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache_dir = temp_dir / ".pytest_cache"
    cache_dir.mkdir()
    log_file = temp_dir / "service.log"
    log_file.write_text("log", encoding="utf-8")

    def failing_rmtree(path: Path, ignore_errors: bool = False) -> None:
        del ignore_errors
        raise PermissionError(f"blocked: {path}")

    monkeypatch.setattr("project_name.app.clean_service.shutil.rmtree", failing_rmtree)

    result = run_clean(temp_dir)

    assert cache_dir in result.failed_paths
    assert log_file in result.removed_paths
