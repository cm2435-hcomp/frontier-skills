---
description: Using cells in Google Sheets (web UI).
name: web-google-sheets
url_pattern: ^https://docs\.google\.com/spreadsheets
---

Always enter edit mode before typing:
* Without `press("Enter")` or `press("F2")`, typing will fail
* Edit mode shows a blinking cursor in the cell

Wait between actions — Google Sheets needs time to register each one.

Navigation: `Tab` moves right, `Enter` moves down.
`F2` enters edit mode at the cursor position. `Enter` enters edit mode and moves to the next cell.
`Escape` cancels an edit without saving; `Enter` confirms and saves.

## Quick reference

| Action | Command sequence |
|---|---|
| Write new value | Click → Enter → Type → Enter |
| Edit existing | Click → F2 → Type → Enter |
| Append text | Click → F2 → End → Type → Enter |
| Clear cell | Click → Backspace/Delete |
| Move right | Tab |
| Move down | Enter |
| Move up | Shift+Enter |
| Cancel edit | Escape |
