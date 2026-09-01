"""Validate registry metadata and Agent Skills frontmatter."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

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
    if registry.get("schema_version") != 1 or registry.get("source") != "h/frontier-skills":
        raise ValueError("registry identity must be schema 1 and source h/frontier-skills")
    skills = registry.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ValueError("registry.skills must be a non-empty list")
    names: set[str] = set()
    paths: set[str] = set()
    for entry in skills:
        name = entry.get("name")
        path = entry.get("path")
        if not isinstance(name, str) or NAME_PATTERN.fullmatch(name) is None:
            raise ValueError(f"invalid skill name: {name!r}")
        if name in names:
            raise ValueError(f"duplicate skill name: {name}")
        names.add(name)
        if not isinstance(path, str) or not path.startswith("skills/"):
            raise ValueError(f"{name}: path must live under skills/")
        parsed = PurePosixPath(path)
        if parsed.is_absolute() or ".." in parsed.parts or str(parsed) != path or path in paths:
            raise ValueError(f"{name}: unsafe or duplicate path {path!r}")
        paths.add(path)
        modes = entry.get("modes")
        if not isinstance(modes, list) or not modes or set(modes) - {"desktop", "browser"}:
            raise ValueError(f"{name}: modes must be a non-empty desktop/browser subset")
        package = ROOT / path
        skill_md = package / "SKILL.md"
        if not skill_md.is_file():
            raise ValueError(f"{name}: missing {skill_md.relative_to(ROOT)}")
        post = frontmatter.load(skill_md)
        if post.metadata.get("name") != name or post.metadata.get("description") != entry.get("description"):
            raise ValueError(f"{name}: registry and SKILL.md frontmatter disagree")
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
