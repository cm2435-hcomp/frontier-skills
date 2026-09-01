---
name: office-artifact-surgery
description: Make narrow office-document edits while preserving application-native structure and verifying the saved artifact.
compatibility: Requires a disposable desktop workspace shared with the office application; Python 3 is needed for optional archive checks.
---

Use this when a Writer, Calc, Impress, or OOXML artifact needs a precise change without rebuilding the document.

- Treat the application-native file as the source of truth. Prefer editing in the office application when the change
  depends on layout, formulas, styles, embedded objects, charts, notes, or application state.
- Use archive/XML surgery only for a narrow, understood property that the application UI cannot reliably express.
  Copy the original first, change the minimum member, and preserve every unrelated member.
- Never replace a workbook, document, or presentation with an offline reconstruction merely because generating one is
  easier. That commonly destroys formulas, themes, relationships, metadata, or evaluator-visible state.
- Save to the exact requested path. Confirm that path exists before declaring success.
- Reopen the saved artifact in its final application. Inspect the changed area and one nearby unchanged area. For
  spreadsheets, also check formulas and displayed values; for slides/documents, inspect rendering and object placement.

For OOXML files, `python scripts/check_ooxml.py PATH` provides a fast structural check. It proves the ZIP package is
readable and key document members exist; it does not prove visual correctness, so still reopen the artifact.
