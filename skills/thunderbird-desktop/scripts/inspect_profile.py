"""Find Thunderbird profiles and report metadata without exposing string preferences or mail."""

from __future__ import annotations

import argparse
import configparser
import json
import re
from pathlib import Path

PREF = re.compile(r'^user_pref\("(?P<name>(?:[^"\\]|\\.)*)",\s*(?P<value>.*)\);$')


def _safe_value(raw: str) -> object:
    if raw == "true":
        return True
    if raw == "false":
        return False
    if re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        return float(raw) if "." in raw else int(raw)
    return "<redacted:string>"


def _preferences(profile: Path, prefixes: tuple[str, ...]) -> dict[str, object]:
    prefs_path = profile / "prefs.js"
    if not prefs_path.is_file():
        return {}
    result = {}
    for line in prefs_path.read_text(errors="replace").splitlines():
        match = PREF.match(line)
        if match and (not prefixes or match.group("name").startswith(prefixes)):
            result[match.group("name")] = _safe_value(match.group("value"))
    return dict(sorted(result.items()))


def inspect(root: Path, prefixes: tuple[str, ...]) -> dict[str, object]:
    ini_path = root / "profiles.ini"
    if not ini_path.is_file():
        raise FileNotFoundError(f"Thunderbird profiles file not found: {ini_path}")
    config = configparser.ConfigParser()
    config.read(ini_path)
    profiles = []
    for section in config.sections():
        if not section.startswith("Profile"):
            continue
        raw_path = Path(config[section]["Path"])
        profile = raw_path if raw_path.is_absolute() else root / raw_path
        mailboxes = []
        for base_name in ("ImapMail", "Mail"):
            base = profile / base_name
            if base.is_dir():
                mailboxes.extend(
                    {
                        "path": str(path.relative_to(profile)),
                        "bytes": path.stat().st_size,
                    }
                    for path in sorted(base.rglob("*"))
                    if path.is_file()
                    and not path.suffix
                    and not path.name.startswith(".")
                )
        profiles.append(
            {
                "section": section,
                "name": config[section].get("Name"),
                "path": str(profile),
                "default": config[section].getboolean("Default", fallback=False),
                "preferences": _preferences(profile, prefixes),
                "mailboxes": mailboxes,
            }
        )
    return {"root": str(root), "profiles": profiles}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.home() / ".thunderbird")
    parser.add_argument("--pref-prefix", action="append", default=[])
    args = parser.parse_args()
    print(json.dumps(inspect(args.root, tuple(args.pref_prefix)), indent=2))


if __name__ == "__main__":
    main()
