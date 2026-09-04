"""Deterministic producer/consumer release boundary."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_release import _is_package_file, build_release  # noqa: E402


def test_release_build_is_deterministic_and_complete(tmp_path: Path) -> None:
    first_descriptor, first_archive = build_release(tmp_path / "first", provenance_commit="test-commit")
    second_descriptor, second_archive = build_release(tmp_path / "second", provenance_commit="test-commit")

    assert first_archive.read_bytes() == second_archive.read_bytes()
    assert first_descriptor.read_bytes() == second_descriptor.read_bytes()
    descriptor = json.loads(first_descriptor.read_text())
    assert descriptor["release_sha256"] == hashlib.sha256(first_archive.read_bytes()).hexdigest()
    assert {entry["name"] for entry in descriptor["skills"]} >= {
        "libreoffice-calc",
        "libreoffice-impress",
        "libreoffice-writer",
        "thunderbird-desktop",
        "vscode-desktop",
    }


def test_release_excludes_python_runtime_cache(tmp_path: Path) -> None:
    source = tmp_path / "scripts" / "inspect.py"
    cache = tmp_path / "scripts" / "__pycache__" / "inspect.cpython-312.pyc"
    source.parent.mkdir(parents=True)
    cache.parent.mkdir(parents=True)
    source.touch()
    cache.touch()

    assert _is_package_file(source)
    assert not _is_package_file(cache)
