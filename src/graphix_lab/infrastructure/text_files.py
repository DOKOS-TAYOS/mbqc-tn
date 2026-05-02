from __future__ import annotations

from pathlib import Path


def iter_text_files(
    workspace_root: Path,
    suffixes: tuple[str, ...],
    file_names: tuple[str, ...],
    skip_directories: tuple[str, ...],
) -> list[Path]:
    text_files: list[Path] = []
    for path in workspace_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_directories for part in path.relative_to(workspace_root).parts):
            continue
        if path.suffix in suffixes or path.name in file_names:
            text_files.append(path)
    return sorted(text_files)
