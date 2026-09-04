"""Regression tests for read-only app inspectors."""

from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path


def _load(relative_path: str):
    path = Path(__file__).parents[1] / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_impress_inspector_walks_grouped_text_and_run_properties(
    tmp_path: Path,
) -> None:
    inspector = _load("skills/libreoffice-impress/scripts/inspect_presentation.py")
    deck = tmp_path / "deck.pptx"
    with zipfile.ZipFile(deck, "w") as package:
        package.writestr(
            "ppt/presentation.xml",
            '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:sldIdLst>'
            '<p:sldId id="1" r:id="rId1"/></p:sldIdLst></p:presentation>',
        )
        package.writestr(
            "ppt/_rels/presentation.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="slide" Target="/ppt/slides/slide1.xml"/></Relationships>',
        )
        package.writestr(
            "ppt/slides/slide1.xml",
            '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:grpSp><p:sp>'
            '<p:nvSpPr><p:cNvPr id="7" name="Grouped Text"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="10" y="20"/><a:ext cx="30" cy="40"/></a:xfrm></p:spPr>'
            '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr strike="sngStrike"/><a:t>Hello</a:t>'
            "</a:r></a:p></p:txBody></p:sp></p:grpSp></p:spTree></p:cSld></p:sld>",
        )

    report = inspector.inspect(deck, {1}, 200)

    shape = report["slides"][0]["shapes"][0]
    assert shape["name"] == "Grouped Text"
    assert shape["geometry_emu"]["top"] == "20"
    assert shape["paragraphs"][0]["runs"][0]["properties"]["strike"] == "sngStrike"


def test_impress_inspector_reports_pictures_end_para_links_notes_and_master_fields(
    tmp_path: Path,
) -> None:
    inspector = _load("skills/libreoffice-impress/scripts/inspect_presentation.py")
    deck = tmp_path / "deck.pptx"
    p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
    a_ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
    r_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    with zipfile.ZipFile(deck, "w") as package:
        package.writestr(
            "ppt/presentation.xml",
            f'<p:presentation xmlns:p="{p_ns}" xmlns:r="{r_ns}">'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId2"/></p:sldMasterIdLst>'
            '<p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>',
        )
        package.writestr(
            "ppt/_rels/presentation.xml.rels",
            f'<Relationships xmlns="{rel_ns}">'
            '<Relationship Id="rId1" Type="slide" Target="slides/slide1.xml"/>'
            '<Relationship Id="rId2" Type="slideMaster" Target="slideMasters/slideMaster1.xml"/></Relationships>',
        )
        package.writestr(
            "ppt/slideMasters/slideMaster1.xml",
            f'<p:sldMaster xmlns:p="{p_ns}" xmlns:a="{a_ns}"><p:cSld><p:spTree><p:sp>'
            '<p:nvSpPr><p:cNvPr id="4" name="Slide Number Placeholder"/><p:cNvSpPr/>'
            '<p:nvPr><p:ph type="sldNum"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:p><a:fld type="slidenum">'
            '<a:rPr><a:solidFill><a:srgbClr val="FF0000"/></a:solidFill></a:rPr><a:t>1</a:t></a:fld>'
            "</a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sldMaster>",
        )
        package.writestr(
            "ppt/slides/_rels/slide1.xml.rels",
            f'<Relationships xmlns="{rel_ns}">'
            '<Relationship Id="rId9" Type="http://x/notesSlide" Target="../notesSlides/notesSlide1.xml"/>'
            "</Relationships>",
        )
        package.writestr(
            "ppt/notesSlides/notesSlide1.xml",
            f'<p:notes xmlns:p="{p_ns}" xmlns:a="{a_ns}"><p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r>'
            "<a:t>speaker note</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>",
        )
        package.writestr(
            "ppt/slides/slide1.xml",
            f'<p:sld xmlns:p="{p_ns}" xmlns:a="{a_ns}" xmlns:r="{r_ns}"><p:cSld><p:spTree>'
            # a cropped photo stored as a blip-filled shape, not a p:pic
            '<p:sp><p:nvSpPr><p:cNvPr id="5" name="Cropped Photo"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:blipFill><a:blip r:embed="rId3"/></a:blipFill></p:spPr></p:sp>'
            # a true picture element
            '<p:pic><p:nvPicPr><p:cNvPr id="6" name="Icon"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>'
            '<p:blipFill><a:blip r:embed="rId4"/></p:blipFill><p:spPr/></p:pic>'
            # text with a whitespace-only run, a hyperlink, a line break, and end-paragraph properties
            '<p:sp><p:nvSpPr><p:cNvPr id="7" name="Body"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr/>'
            '<p:txBody><a:p><a:r><a:rPr u="sng"><a:hlinkClick r:id="rId5"/></a:rPr><a:t>Ref</a:t></a:r>'
            '<a:r><a:rPr/><a:t> </a:t></a:r><a:br/><a:r><a:rPr u="sng"/><a:t>more</a:t></a:r>'
            '<a:endParaRPr u="sng"/></a:p></p:txBody></p:sp>'
            "</p:spTree></p:cSld></p:sld>",
        )

    report = inspector.inspect(deck, set(), 200)

    slide = report["slides"][0]
    by_name = {shape["name"]: shape for shape in slide["shapes"]}
    assert by_name["Cropped Photo"]["picture"] is True
    assert by_name["Cropped Photo"]["kind"] == "sp"
    assert by_name["Icon"]["picture"] is True
    assert by_name["Icon"]["kind"] == "pic"
    assert by_name["Icon"]["image_rid"] == "rId4"
    assert by_name["Body"]["picture"] is False
    paragraph = by_name["Body"]["paragraphs"][0]
    assert paragraph["runs"][0]["hyperlink"] == "rId5"
    assert paragraph["runs"][1]["whitespace_only"] is True
    assert paragraph["line_breaks"] == 1
    assert paragraph["end_paragraph_properties"]["properties"] == {"u": "sng"}
    assert slide["notes"] == ["speaker note"]
    assert slide["notes_slide"] == "ppt/notesSlides/notesSlide1.xml"
    master = report["master_field_placeholders"][0]
    assert master["placeholder"] == "sldNum"
    field_run = master["paragraphs"][0]["runs"][0]
    assert field_run["field"] == "slidenum"
    assert field_run["color"] == "FF0000"


def test_calc_inspector_reports_formula_format_chart_and_pivot(tmp_path: Path) -> None:
    inspector = _load("skills/libreoffice-calc/scripts/inspect_workbook.py")
    workbook = tmp_path / "book.xlsx"
    with zipfile.ZipFile(workbook, "w") as package:
        package.writestr(
            "xl/workbook.xml",
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
            '<sheet name="Data" sheetId="1" r:id="rId1"/></sheets></workbook>',
        )
        package.writestr(
            "xl/_rels/workbook.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="worksheet" Target="worksheets/sheet1.xml"/></Relationships>',
        )
        package.writestr(
            "xl/worksheets/sheet1.xml",
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><dimension ref="A1:A1"/>'
            '<sheetData><row r="1"><c r="A1" s="0"><f>1+1</f><v>2</v></c></row></sheetData></worksheet>',
        )
        package.writestr(
            "xl/styles.xml",
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<cellXfs count="1"><xf numFmtId="9"/></cellXfs></styleSheet>',
        )
        package.writestr(
            "xl/charts/chart1.xml",
            '<c:chartSpace xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart">'
            "<c:chart><c:ser><c:val><c:numRef><c:f>Data!$A$1:$A$2</c:f></c:numRef></c:val></c:ser>"
            "</c:chart></c:chartSpace>",
        )
        package.writestr(
            "xl/pivotTables/pivotTable1.xml",
            '<pivotTableDefinition xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" name="Pivot1"/>',
        )

    report = inspector.inspect(workbook, {"Data"}, 10)

    assert report["sheets"][0]["cells"][0] == {
        "reference": "A1",
        "formula": "1+1",
        "stored_value": "2",
        "number_format": "builtin:9",
    }
    assert report["charts"][0]["range_formulas"] == ["Data!$A$1:$A$2"]
    assert report["pivots"][0]["name"] == "Pivot1"


def test_thunderbird_inspector_redacts_strings_and_lists_mailboxes(
    tmp_path: Path,
) -> None:
    inspector = _load("skills/thunderbird-desktop/scripts/inspect_profile.py")
    root = tmp_path / ".thunderbird"
    profile = root / "profile"
    mailbox = profile / "ImapMail" / "mail.example" / "Inbox"
    mailbox.parent.mkdir(parents=True)
    mailbox.write_text("secret message body")
    (root / "profiles.ini").write_text(
        "[Profile0]\nName=default\nIsRelative=1\nPath=profile\nDefault=1\n"
    )
    (profile / "prefs.js").write_text(
        'user_pref("mail.server.default.applyIncomingFilters", true);\n'
        'user_pref("mail.identity.id1.smtpServer", "secret-account");\n'
    )

    report = inspector.inspect(root, ("mail.",))

    preferences = report["profiles"][0]["preferences"]
    assert preferences["mail.server.default.applyIncomingFilters"] is True
    assert preferences["mail.identity.id1.smtpServer"] == "<redacted:string>"
    assert report["profiles"][0]["mailboxes"] == [
        {"path": "ImapMail/mail.example/Inbox", "bytes": 19}
    ]
