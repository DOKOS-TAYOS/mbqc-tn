from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

DIRECTORY_PATTERNS: tuple[str, ...] = (
    "__pycache__",
    ".pytest-tmp",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".pyright",
    "build",
    "dist",
    "htmlcov",
    ".hypothesis",
    ".tmp",
    "pytest-cache",
    "pytest-temp",
    "test-artifacts",
)
FILE_PATTERNS: tuple[str, ...] = ("*.log", ".coverage")
DIRECTORY_GLOBS: tuple[str, ...] = ("pytest-cache-files-*",)
PROTECTED_DIRECTORIES: tuple[str, ...] = (".venv", ".git")


@dataclass(frozen=True, slots=True)
class CleanResult:
    removed_paths: tuple[Path, ...]
    planned_paths: tuple[Path, ...]
    failed_paths: tuple[Path, ...]


def _contains_protected_descendant(path: Path) -> bool:
    found_inaccessible_path = False

    def mark_inaccessible(error: OSError) -> None:
        nonlocal found_inaccessible_path
        found_inaccessible_path = True
        del error

    for _, directory_names, _ in os.walk(path, topdown=True, onerror=mark_inaccessible):
        if any(name in PROTECTED_DIRECTORIES for name in directory_names):
            return True
        directory_names[:] = [
            directory_name
            for directory_name in directory_names
            if directory_name not in PROTECTED_DIRECTORIES
        ]
    return found_inaccessible_path


def _matches_cleanup_directory(directory_name: str) -> bool:
    return directory_name in DIRECTORY_PATTERNS or any(
        fnmatch(directory_name, pattern) for pattern in DIRECTORY_GLOBS
    )


def collect_cleanup_paths(root: Path) -> list[Path]:
    candidates: set[Path] = set()

    def ignore_walk_error(error: OSError) -> None:
        del error

    for current_root, directory_names, file_names in os.walk(
        root,
        topdown=True,
        onerror=ignore_walk_error,
    ):
        current_path = Path(current_root)
        directory_names[:] = [
            directory_name
            for directory_name in directory_names
            if directory_name not in PROTECTED_DIRECTORIES
        ]

        for directory_name in tuple(directory_names):
            directory_path = current_path / directory_name
            if not _matches_cleanup_directory(directory_name):
                continue
            if _contains_protected_descendant(directory_path):
                directory_names.remove(directory_name)
                continue
            candidates.add(directory_path)
            directory_names.remove(directory_name)

        for file_name in file_names:
            if any(fnmatch(file_name, pattern) for pattern in FILE_PATTERNS):
                candidates.add(current_path / file_name)

    return sorted(candidates)


def run_clean(root: Path, dry_run: bool = False) -> CleanResult:
    planned_paths = tuple(collect_cleanup_paths(root))
    removed_paths: list[Path] = []
    failed_paths: list[Path] = []

    if dry_run:
        return CleanResult(removed_paths=(), planned_paths=planned_paths, failed_paths=())

    for candidate in planned_paths:
        try:
            if candidate.is_dir():
                shutil.rmtree(candidate, ignore_errors=False)
            elif candidate.exists():
                candidate.unlink()
            removed_paths.append(candidate)
        except OSError:
            failed_paths.append(candidate)

    return CleanResult(
        removed_paths=tuple(removed_paths),
        planned_paths=planned_paths,
        failed_paths=tuple(failed_paths),
    )
