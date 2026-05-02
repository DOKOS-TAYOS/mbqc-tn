from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path


def iter_text_files(
    workspace_root: Path,
    suffixes: tuple[str, ...],
    file_names: tuple[str, ...],
    skip_directories: tuple[str, ...],
    skip_directory_globs: tuple[str, ...] = (),
) -> list[Path]:
    text_files: list[Path] = []
    for path in workspace_root.rglob("*"):
        if not path.is_file():
            continue
        if _path_has_skipped_directory(
            path=path,
            workspace_root=workspace_root,
            skip_directories=skip_directories,
            skip_directory_globs=skip_directory_globs,
        ):
            continue
        if path.suffix in suffixes or path.name in file_names:
            text_files.append(path)
    return sorted(text_files)


def _path_has_skipped_directory(
    *,
    path: Path,
    workspace_root: Path,
    skip_directories: tuple[str, ...],
    skip_directory_globs: tuple[str, ...],
) -> bool:
    for path_part in path.relative_to(workspace_root).parts:
        if path_part in skip_directories:
            return True
        if any(fnmatch(path_part, pattern) for pattern in skip_directory_globs):
            return True
    return False
