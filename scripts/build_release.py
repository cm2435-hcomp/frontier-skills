"""Build deterministic skill release assets."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

import frontmatter

from validate_registry import ROOT, load_registry, validate_registry


def build_release(output: Path, *, provenance_commit: str | None = None) -> tuple[Path, Path]:
    entries = validate_registry()
    registry = load_registry()
    commit = provenance_commit or _git_commit()
    release_skills: list[dict] = []
    archive_files: list[tuple[str, bytes, bool]] = []
    for entry in entries:
        package = ROOT / entry["path"]
        file_entries: list[dict] = []
        for file_path in sorted(path for path in package.rglob("*") if _is_package_file(path)):
            relative = file_path.relative_to(package).as_posix()
            content = file_path.read_bytes()
            executable = bool(file_path.stat().st_mode & 0o111)
            file_entries.append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "size": len(content),
                    "executable": executable,
                }
            )
            archive_files.append((f"{entry['path']}/{relative}", content, executable))
        post = frontmatter.load(package / "SKILL.md")
        release_skills.append(
            {
                "name": entry["name"],
                "description": entry["description"],
                "compatibility": post.metadata.get("compatibility"),
                "modes": entry["modes"],
                "path": entry["path"],
                "sha256": package_sha256(file_entries),
                "files": file_entries,
            }
        )

    output.mkdir(parents=True, exist_ok=True)
    archive_path = output / "release.tar.gz"
    archive_bytes = _archive_bytes(archive_files)
    archive_path.write_bytes(archive_bytes)
    descriptor = {
        "schema_version": 1,
        "source": registry["source"],
        "revision": registry["revision"],
        "release_sha256": hashlib.sha256(archive_bytes).hexdigest(),
        "provenance": {"repository": "hcompai/frontier-skills", "commit": commit},
        "skills": release_skills,
    }
    descriptor_path = output / "release.json"
    descriptor_path.write_text(json.dumps(descriptor, indent=2, sort_keys=True) + "\n")
    return descriptor_path, archive_path


def package_sha256(files: list[dict]) -> str:
    digest = hashlib.sha256()
    for item in sorted(files, key=lambda value: value["path"]):
        digest.update(
            f"{item['path']}\0{item['sha256']}\0{item['size']}\0{int(item['executable'])}\n".encode()
        )
    return digest.hexdigest()


def _is_package_file(path: Path) -> bool:
    return path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"


def _archive_bytes(files: list[tuple[str, bytes, bool]]) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.GNU_FORMAT) as archive:
            for path, content, executable in sorted(files):
                info = tarfile.TarInfo(path)
                info.size = len(content)
                info.mode = 0o755 if executable else 0o644
                info.mtime = 0
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                archive.addfile(info, io.BytesIO(content))
    return buffer.getvalue()


def _git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    descriptor, archive = build_release(args.output)
    print(descriptor)
    print(archive)


if __name__ == "__main__":
    main()
