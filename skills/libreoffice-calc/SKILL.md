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

## Roll-forward and version-bound features

A "next period" or "roll-forward" workbook is a copy of the prior one with its data ranges moved, not a rebuild. Copy
the file, then edit in place so external links (`=[N]Sheet!$A$1` references to other workbooks), charts, conditional
formats, and names survive. A workbook rebuilt from values loses all of them.

Check `soffice --version` before using a feature with a minimum version. Sparklines need 7.4 (Insert > Sparkline);
on 7.3 there is no menu item, no UNO object, and `x14:sparklineGroups` injected into the file is stripped on the next
save. Three structural absences mean the feature does not exist in this build; report that under the runtime's
infeasible reporting contract rather than hand-authoring XML.

## Edit and hand back

If Calc already has the workbook open, save and close it before a programmatic edit. Reopen the edited workbook in
Calc, recalculate it, and save before finishing. Application-created pivots, fields, and formulas may not materialise
until Calc updates them.

If LibreOffice is force-stopped, dismiss Document Recovery on relaunch before opening the target. A recovery copy is
not evidence that the requested file was saved. In the GUI, write into an empty cell without overwrite mode so Calc
does not open the delete-confirmation dialog.

Verify sheet and row counts before inspecting individual values. Check formulas and displayed results separately. A
valid ZIP or successful library save does not prove that Calc retained the requested object.
