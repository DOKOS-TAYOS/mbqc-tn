from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
PYTEST_TEMP_ROOT = REPO_ROOT / "pytest-temp"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    from graphix_lab.infrastructure.temporary_workspaces import create_temporary_workspace

    temporary_workspace = create_temporary_workspace(
        prefix="graphix-lab-tests-",
        fallback_root=PYTEST_TEMP_ROOT,
    )
    try:
        yield temporary_workspace.path
    finally:
        temporary_workspace.cleanup(ignore_errors=True)
