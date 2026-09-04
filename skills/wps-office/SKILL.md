---
name: wps-office
description: Author and verify WPS Presentation, Spreadsheets, and Writer documents inside WPS rather than through file surgery.
compatibility: Requires a desktop workspace with WPS Office installed and the target document on the same filesystem.
---

Use this when the task names WPS Office or the document is opened in WPS Presentation, WPS Spreadsheets, or WPS
Writer. LibreOffice and Microsoft Office semantics do not transfer; the `libreoffice-*` packages do not cover WPS.

## The deliverable is the application's object

When the task names the application, the result is judged as that application's own object, not as a file that
happens to open. Create and edit it through the WPS UI, then reopen it in WPS and inspect the object there. A file
that passes a library round trip or a PDF render can still be missing the object WPS expects.

- WPS loads python-pptx and openpyxl output only partially. Tables, transitions, shape effects, equations, formulas,
  and charts written by those libraries can render blank, drop, or lose cached values. Fewer slides or empty
  content after opening a generated file means the format was not accepted; rebuild in WPS.
- Do not run a WPS Spreadsheets file through LibreOffice to recalculate or resave. The structure and cached values
  it writes are not what WPS produces.
- Equations are inserted through Insert > Equation. Hand-written OMML is not a WPS equation object even when the
  markup is valid.
- 3D effects live under Format Shape > 3D Format and 3D Rotation. Apply them to the selected shapes in WPS instead of
  rebuilding geometry in XML.
- A transition such as Morph counts only if WPS plays it. Run the slide show and watch the transition; the XML
  element being present does not prove WPS honours it.

## File handoff

WPS keeps the open document in memory and writes that buffer back on save. Before any edit outside WPS, find the
exact WPS process, save, and close it. After the edit, reopen the file in WPS so it loads the new state, and leave
it open if the task expects the document to remain open.

## Verify in WPS

Open the finished document in WPS and check the object the task names: the table renders, the formula shows a value
and recalculates, the chart draws, the equation is selectable as an equation, the transition plays. Counting slides,
sheets, or cells in the file is not that check.
