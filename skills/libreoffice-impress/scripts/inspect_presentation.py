"""Report presentation structure without modifying the OOXML package."""

from __future__ import annotations

import argparse
import json
import posixpath
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
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


def _properties(props: ET.Element | None) -> dict[str, object] | None:
    if props is None:
        return None
    output: dict[str, object] = {"properties": dict(sorted(props.attrib.items()))}
    colour = props.find("a:solidFill/a:srgbClr", NS)
    if colour is not None:
        output["color"] = colour.attrib.get("val")
    link = props.find("a:hlinkClick", NS)
    if link is not None:
        output["hyperlink"] = link.attrib.get(RID)
    return output


RUN_TAGS = (f"{{{NS['a']}}}r", f"{{{NS['a']}}}fld")


def _run(run: ET.Element, max_text: int) -> dict[str, object]:
    """A text run or a field run (slide number, date); both carry `a:rPr`."""
    text = "".join(node.text or "" for node in run.findall("a:t", NS))[:max_text]
    output: dict[str, object] = {"text": text, "whitespace_only": text.strip() == ""}
    if run.tag.endswith("}fld"):
        output["field"] = run.attrib.get("type")
    output.update(_properties(run.find("a:rPr", NS)) or {})
    return output


def _paragraph(paragraph: ET.Element, max_text: int) -> dict[str, object]:
    props = paragraph.find("a:pPr", NS)
    bullet = None
    if props is not None:
        bullet_node = next(
            (child for child in props if child.tag.rsplit("}", 1)[-1].startswith("bu")),
            None,
        )
        if bullet_node is not None:
            bullet = {"type": bullet_node.tag.rsplit("}", 1)[-1], **bullet_node.attrib}
    runs = [_run(run, max_text) for run in paragraph if run.tag in RUN_TAGS]
    return {
        "text": "".join(node.text or "" for node in paragraph.findall(".//a:t", NS))[
            :max_text
        ],
        "level": None if props is None else props.attrib.get("lvl", "0"),
        "bullet": bullet,
        "runs": runs,
        "line_breaks": len(paragraph.findall("a:br", NS)),
        "end_paragraph_properties": _properties(paragraph.find("a:endParaRPr", NS)),
    }


def _shape(shape: ET.Element, max_text: int) -> dict[str, object]:
    kind = shape.tag.rsplit("}", 1)[-1]
    identity = shape.find("p:nvSpPr/p:cNvPr", NS)
    if identity is None:
        identity = shape.find("p:nvPicPr/p:cNvPr", NS)
    placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
    if placeholder is None:
        placeholder = shape.find("p:nvPicPr/p:nvPr/p:ph", NS)
    blip = shape.find("p:blipFill/a:blip", NS)
    if blip is None:
        blip = shape.find("p:spPr/a:blipFill/a:blip", NS)
    transform = shape.find("p:spPr/a:xfrm", NS)
    geometry = None
    if transform is not None:
        offset = transform.find("a:off", NS)
        extent = transform.find("a:ext", NS)
        geometry = {
            "left": None if offset is None else offset.attrib.get("x"),
            "top": None if offset is None else offset.attrib.get("y"),
            "width": None if extent is None else extent.attrib.get("cx"),
            "height": None if extent is None else extent.attrib.get("cy"),
        }
    return {
        "id": None if identity is None else identity.attrib.get("id"),
        "name": None if identity is None else identity.attrib.get("name"),
        "kind": kind,
        "placeholder": None
        if placeholder is None
        else placeholder.attrib.get("type", "body"),
        "picture": blip is not None,
        "image_rid": None if blip is None else blip.attrib.get(f"{{{NS['r']}}}embed"),
        "geometry_emu": geometry,
        "paragraphs": [
            _paragraph(p, max_text) for p in shape.findall("p:txBody/a:p", NS)
        ],
    }


def _shapes(root: ET.Element, max_text: int) -> list[dict[str, object]]:
    """Every text shape and picture in document order, including those nested in groups."""
    return [
        _shape(node, max_text)
        for node in root.iter()
        if node.tag in (f"{{{NS['p']}}}sp", f"{{{NS['p']}}}pic")
    ]


FIELD_PLACEHOLDERS = ("sldNum", "dt", "ftr")


def _master_fields(
    package: zipfile.ZipFile,
    presentation: ET.Element,
    relationships: dict[str, tuple[str, str]],
    max_text: int,
) -> list[dict[str, object]]:
    """Slide number, date, and footer placeholders on each master; slides inherit their formatting."""
    reports = []
    for node in presentation.findall("p:sldMasterIdLst/p:sldMasterId", NS):
        master_path = relationships[node.attrib[RID]][0]
        master = ET.fromstring(package.read(master_path))
        for shape in _shapes(master, max_text):
            if shape["placeholder"] in FIELD_PLACEHOLDERS:
                reports.append({"master": master_path, **shape})
    return reports


def inspect(path: Path, selected_slides: set[int], max_text: int) -> dict[str, object]:
    with zipfile.ZipFile(path) as package:
        presentation_path = "ppt/presentation.xml"
        presentation = ET.fromstring(package.read(presentation_path))
        relationships = _rels(package, presentation_path)
        slide_paths = [
            relationships[node.attrib[RID]][0]
            for node in presentation.findall("p:sldIdLst/p:sldId", NS)
        ]
        master_fields = _master_fields(package, presentation, relationships, max_text)
        slides = []
        for number, slide_path in enumerate(slide_paths, 1):
            if selected_slides and number not in selected_slides:
                continue
            root = ET.fromstring(package.read(slide_path))
            slide_rels = _rels(package, slide_path)
            notes_paths = [
                target
                for target, kind in slide_rels.values()
                if kind.endswith("/notesSlide")
            ]
            notes = []
            for notes_path in notes_paths:
                notes_root = ET.fromstring(package.read(notes_path))
                notes.extend(
                    node.text or "" for node in notes_root.findall(".//a:t", NS)
                )
            slides.append(
                {
                    "number": number,
                    "path": slide_path,
                    "shapes": _shapes(root, max_text),
                    "notes": notes,
                    "notes_slide": notes_paths[0] if notes_paths else None,
                }
            )
    return {
        "path": str(path),
        "slide_count": len(slide_paths),
        "master_field_placeholders": master_fields,
        "slides": slides,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--slide", action="append", type=int, default=[])
    parser.add_argument("--max-text", type=int, default=200)
    args = parser.parse_args()
    if args.max_text < 1:
        parser.error("--max-text must be positive")
    print(
        json.dumps(
            inspect(args.path, set(args.slide), args.max_text),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
