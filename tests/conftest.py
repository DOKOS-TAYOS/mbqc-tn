from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture
def temp_dir(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    yield tmp_path_factory.mktemp("vibe-template")
