---
name: libreoffice-calc
description: Create and verify real LibreOffice Calc formulas, charts, formatting rules, and pivot tables.
compatibility: Requires a disposable desktop workspace shared with LibreOffice Calc and Python 3 for the read-only inspector.
---

Use this for a spreadsheet opened or intended for LibreOffice Calc. Do not substitute a table that looks right for
an application object the task names.

## Inspect first

Run `python scripts/inspect_workbook.py FILE --sheet NAME` before editing and again after saving. It reports formulas,
stored values, number formats, chart range formulas, pivot definitions, names, and sheet counts without resaving the
workbook.

- A calculation is a live formula. A pasted result is not equivalent.
- A percentage cell stores the fraction. For example, `=(C12-B12)/B12` may store `-0.0546`; multiplying by 100 and
  also applying a percentage format is wrong.
- Conditional formatting is a rule, not a static cell fill.
- A chart should normally be one series over one contiguous data range with one category range. A series per cell is
  a different chart structure even if the pixels look similar.

## Real Calc pivots

`openpyxl` cannot create a new LibreOffice pivot table. A hand-built summary grid is not a pivot object.

In Calc, select the complete source range including headers, then use Data > Pivot Table > Insert or Edit. Put the
grouping column in Row Fields and the measure in Data Fields. Double-click the measure to change Sum to Count. Choose
the destination the task names. If a drag does not register, use one mouse-down, several move steps, and one mouse-up
instead of jumping directly from source to destination.

When the task asks for Calc's produced layout, preserve its generated labels and ordering, including `Count - FIELD`,
ascending labels, `Total Result`, and the blank row between blocks where present.

## Edit and hand back

If Calc already has the workbook open, save and close it before a programmatic edit. Reopen the edited workbook in
Calc, recalculate it, and save before finishing. Application-created pivots, fields, and formulas may not materialise
until Calc updates them.

Verify sheet and row counts before inspecting individual values. Check formulas and displayed results separately. A
valid ZIP or successful library save does not prove that Calc retained the requested object.
