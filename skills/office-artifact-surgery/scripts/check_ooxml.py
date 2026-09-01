"""Check that an OOXML package is readable and contains its expected primary member."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

PRIMARY_MEMBER = {
    ".docx": "word/document.xml",
    ".xlsx": "xl/workbook.xml",
    ".pptx": "ppt/presentation.xml",
}


def main(path_text: str) -> None:
    path = Path(path_text)
    expected = PRIMARY_MEMBER.get(path.suffix.lower())
    if expected is None:
        raise SystemExit(f"unsupported OOXML extension: {path.suffix}")
    with zipfile.ZipFile(path) as package:
        bad_member = package.testzip()
        if bad_member is not None:
            raise SystemExit(f"corrupt ZIP member: {bad_member}")
        if expected not in package.namelist():
            raise SystemExit(f"missing primary OOXML member: {expected}")
    print(f"valid {path.suffix.lower()} package: {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_ooxml.py PATH")
    main(sys.argv[1])
