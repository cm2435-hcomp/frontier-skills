"""Deterministic producer/consumer release boundary."""

from __future__ import annotations

import io
import json
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_release import build_release  # noqa: E402


def test_release_build_is_deterministic_and_complete(tmp_path: Path) -> None:
    first_descriptor, first_archive = build_release(tmp_path / "first")
    second_descriptor, second_archive = build_release(tmp_path / "second")

    assert first_archive.read_bytes() == second_archive.read_bytes()
    assert first_descriptor.read_bytes() == second_descriptor.read_bytes()
    descriptor = json.loads(first_descriptor.read_text())
    assert descriptor["schema_version"] == 2
    with tarfile.open(fileobj=io.BytesIO(first_archive.read_bytes()), mode="r:gz") as archive:
        embedded = archive.extractfile("release.json")
        assert embedded is not None
        assert embedded.read() == first_descriptor.read_bytes()
    assert {entry["name"] for entry in descriptor["skills"]} >= {
        "completion-verification",
        "office-artifact-surgery",
        "safe-live-database-inspection",
        "visual-batch-inspection",
    }
