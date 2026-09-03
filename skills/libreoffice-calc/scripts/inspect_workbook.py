"""Report workbook formulas and generated objects without modifying the OOXML package."""

from __future__ import annotations

import argparse
import json
import posixpath
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
}
RID = f"{{{NS['r']}}}id"


def _rels(package: zipfile.ZipFile, owner: str) -> dict[str, tuple[str, str]]:
    directory, name = posixpath.split(owner)
    rels_path = posixpath.join(directory, "_rels", f"{name}.rels")
    if rels_path not in package.namelist():
        return {}
    root = ET.fromstring(package.read(rels_path))
    result = {}
    for rel in root.findall("pr:Relationship", NS):
        raw_target = rel.attrib["Target"]
        target = (
            raw_target.lstrip("/")
            if raw_target.startswith("/")
            else posixpath.normpath(posixpath.join(directory, raw_target))
        )
        result[rel.attrib["Id"]] = (target, rel.attrib.get("Type", ""))
    return result


def _shared_strings(package: zipfile.ZipFile) -> list[str]:
    path = "xl/sharedStrings.xml"
    if path not in package.namelist():
        return []
    root = ET.fromstring(package.read(path))
    return [
        "".join(node.text or "" for node in item.findall(".//m:t", NS))
        for item in root.findall("m:si", NS)
    ]


def _number_formats(package: zipfile.ZipFile) -> dict[int, str]:
    path = "xl/styles.xml"
    if path not in package.namelist():
        return {}
    root = ET.fromstring(package.read(path))
    custom = {
        int(node.attrib["numFmtId"]): node.attrib["formatCode"]
        for node in root.findall("m:numFmts/m:numFmt", NS)
    }
    formats = {}
    for index, node in enumerate(root.findall("m:cellXfs/m:xf", NS)):
        format_id = int(node.attrib.get("numFmtId", "0"))
        formats[index] = custom.get(format_id, f"builtin:{format_id}")
    return formats


def _cell(
    cell: ET.Element, strings: list[str], formats: dict[int, str]
) -> dict[str, object]:
    value_node = cell.find("m:v", NS)
    value = None if value_node is None else value_node.text
    if cell.attrib.get("t") == "s" and value is not None:
        index = int(value)
        value = (
            strings[index]
            if index < len(strings)
            else f"<missing shared string {index}>"
        )
    formula = cell.find("m:f", NS)
    style = int(cell.attrib.get("s", "0"))
    return {
        "reference": cell.attrib.get("r"),
        "formula": None if formula is None else formula.text,
        "stored_value": value,
        "number_format": formats.get(style),
    }


def inspect(path: Path, selected_sheets: set[str], max_cells: int) -> dict[str, object]:
    with zipfile.ZipFile(path) as package:
        workbook_path = "xl/workbook.xml"
        workbook = ET.fromstring(package.read(workbook_path))
        relationships = _rels(package, workbook_path)
        strings = _shared_strings(package)
        formats = _number_formats(package)
        sheets = []
        for sheet in workbook.findall("m:sheets/m:sheet", NS):
            name = sheet.attrib["name"]
            if selected_sheets and name not in selected_sheets:
                continue
            sheet_path = relationships[sheet.attrib[RID]][0]
            root = ET.fromstring(package.read(sheet_path))
            cells = [
                _cell(cell, strings, formats) for cell in root.findall(".//m:c", NS)
            ]
            sheets.append(
                {
                    "name": name,
                    "path": sheet_path,
                    "dimension": None
                    if root.find("m:dimension", NS) is None
                    else root.find("m:dimension", NS).attrib.get("ref"),
                    "cells": cells[:max_cells],
                    "cells_truncated": len(cells) > max_cells,
                }
            )
        names = [
            {"name": node.attrib.get("name"), "formula": node.text}
            for node in workbook.findall("m:definedNames/m:definedName", NS)
        ]
        charts = []
        for chart_path in sorted(
            name
            for name in package.namelist()
            if name.startswith("xl/charts/chart") and name.endswith(".xml")
        ):
            chart = ET.fromstring(package.read(chart_path))
            charts.append(
                {
                    "path": chart_path,
                    "range_formulas": [
                        node.text for node in chart.findall(".//c:f", NS)
                    ],
                }
            )
        pivots = []
        for pivot_path in sorted(
            name
            for name in package.namelist()
            if name.startswith("xl/pivotTables/pivotTable") and name.endswith(".xml")
        ):
            pivot = ET.fromstring(package.read(pivot_path))
            pivots.append({"path": pivot_path, "name": pivot.attrib.get("name")})
    return {
        "path": str(path),
        "sheet_count": len(workbook.findall("m:sheets/m:sheet", NS)),
        "sheets": sheets,
        "defined_names": names,
        "charts": charts,
        "pivots": pivots,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--sheet", action="append", default=[])
    parser.add_argument("--max-cells", type=int, default=500)
    args = parser.parse_args()
    if args.max_cells < 1:
        parser.error("--max-cells must be positive")
    print(
        json.dumps(
            inspect(args.path, set(args.sheet), args.max_cells),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
