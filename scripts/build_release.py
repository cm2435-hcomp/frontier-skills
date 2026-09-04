"""Build deterministic skill release assets."""

from __future__ import annotations

import argparse
import gzip
import io
import json
import tarfile
from pathlib import Path

import frontmatter

from validate_registry import ROOT, load_registry, validate_registry


def build_release(output: Path) -> tuple[Path, Path]:
    entries = validate_registry()
    registry = load_registry()
    release_skills: list[dict] = []
    archive_files: list[tuple[str, bytes, bool]] = []
    for entry in entries:
        package = ROOT / entry["path"]
        file_entries: list[dict] = []
        for file_path in sorted(path for path in package.rglob("*") if path.is_file()):
            relative = file_path.relative_to(package).as_posix()
            content = file_path.read_bytes()
            executable = bool(file_path.stat().st_mode & 0o111)
            file_entries.append(
                {
                    "path": relative,
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
                "files": file_entries,
            }
        )

    descriptor = {
        "schema_version": 2,
        "source": registry["source"],
        "revision": registry["revision"],
        "skills": release_skills,
    }
    descriptor_bytes = (json.dumps(descriptor, indent=2, sort_keys=True) + "\n").encode()
    archive_files.append(("release.json", descriptor_bytes, False))

    output.mkdir(parents=True, exist_ok=True)
    descriptor_path = output / "release.json"
    descriptor_path.write_bytes(descriptor_bytes)
    archive_path = output / "release.tar.gz"
    archive_path.write_bytes(_archive_bytes(archive_files))
    return descriptor_path, archive_path


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    descriptor, archive = build_release(args.output)
    print(descriptor)
    print(archive)


if __name__ == "__main__":
    main()
