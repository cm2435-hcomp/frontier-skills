"""Validate registry metadata and Agent Skills frontmatter."""

from __future__ import annotations

import re
from pathlib import Path

import frontmatter
import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_registry() -> dict:
    data = yaml.safe_load((ROOT / "registry.yaml").read_text())
    if not isinstance(data, dict):
        raise ValueError("registry.yaml must contain a mapping")
    return data


def validate_registry() -> list[dict]:
    registry = load_registry()
    if registry.get("schema_version") != 1:
        raise ValueError("registry schema must be 1")
    if not isinstance(registry.get("revision"), str) or not registry["revision"]:
        raise ValueError("registry revision must be a non-empty string")
    skills = registry.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ValueError("registry.skills must be a non-empty list")
    names: set[str] = set()
    for entry in skills:
        if not isinstance(entry, dict) or set(entry) != {"name", "modes"}:
            raise ValueError("each registry skill must contain only name and modes")
        name = entry.get("name")
        if not isinstance(name, str) or NAME_PATTERN.fullmatch(name) is None:
            raise ValueError(f"invalid skill name: {name!r}")
        if name in names:
            raise ValueError(f"duplicate skill name: {name}")
        names.add(name)
        modes = entry.get("modes")
        if not isinstance(modes, list) or not modes or set(modes) - {"desktop", "browser"}:
            raise ValueError(f"{name}: modes must be a non-empty desktop/browser subset")
        package = ROOT / "skills" / name
        skill_md = package / "SKILL.md"
        if not skill_md.is_file():
            raise ValueError(f"{name}: missing {skill_md.relative_to(ROOT)}")
        post = frontmatter.load(skill_md)
        if post.metadata.get("name") != name or not post.metadata.get("description"):
            raise ValueError(f"{name}: SKILL.md must declare its matching name and a description")
        if not post.content.strip():
            raise ValueError(f"{name}: SKILL.md body is empty")
        for file_path in package.rglob("*"):
            if file_path.is_symlink():
                raise ValueError(f"{name}: symlinks are not allowed: {file_path.relative_to(ROOT)}")
    return skills


def main() -> None:
    skills = validate_registry()
    print(f"validated {len(skills)} skills")


if __name__ == "__main__":
    main()
