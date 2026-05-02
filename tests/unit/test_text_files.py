from __future__ import annotations

from pathlib import Path

from graphix_lab.infrastructure.text_files import iter_text_files


def test_iter_text_files_skips_exact_directory_names(temp_dir: Path) -> None:
    included_file = temp_dir / "README.md"
    included_file.write_text("included", encoding="utf-8")
    skipped_file = temp_dir / ".pytest_cache" / "cache.md"
    skipped_file.parent.mkdir()
    skipped_file.write_text("skipped", encoding="utf-8")

    text_files = iter_text_files(
        workspace_root=temp_dir,
        suffixes=(".md",),
        file_names=(),
        skip_directories=(".pytest_cache",),
    )

    assert text_files == [included_file]


def test_iter_text_files_skips_globbed_directory_names(temp_dir: Path) -> None:
    included_file = temp_dir / "docs" / "guide.md"
    included_file.parent.mkdir()
    included_file.write_text("included", encoding="utf-8")
    skipped_file = temp_dir / "pytest-cache-files-abc123" / "cache.md"
    skipped_file.parent.mkdir()
    skipped_file.write_text("skipped", encoding="utf-8")

    text_files = iter_text_files(
        workspace_root=temp_dir,
        suffixes=(".md",),
        file_names=(),
        skip_directories=(),
        skip_directory_globs=("pytest-cache-files-*",),
    )

    assert text_files == [included_file]


def test_iter_text_files_discovers_explicit_file_names_outside_skipped_directories(
    temp_dir: Path,
) -> None:
    included_file = temp_dir / "LICENSE"
    included_file.write_text("included", encoding="utf-8")
    skipped_file = temp_dir / ".pytest_cache" / "LICENSE"
    skipped_file.parent.mkdir()
    skipped_file.write_text("skipped", encoding="utf-8")

    text_files = iter_text_files(
        workspace_root=temp_dir,
        suffixes=(),
        file_names=("LICENSE",),
        skip_directories=(".pytest_cache",),
    )

    assert text_files == [included_file]
