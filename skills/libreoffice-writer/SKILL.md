---
name: libreoffice-writer
description: Make exact LibreOffice Writer transformations while preserving untouched text and structure.
compatibility: Requires a disposable desktop workspace shared with LibreOffice Writer.
---

Use this for a document opened or intended for LibreOffice Writer. Prefer Writer's own command when the request names
a Writer transformation because the command's semantics define the expected document structure.

## Exact transformations

- "Convert to lowercase" means select the complete requested range and use Format > Text > lowercase. It changes all
  selected characters, including sentence capitals; changing only the first character or paragraph is incomplete.
- "Convert text to table" means select the source text, then Table > Convert > Text to Table with the stated separator.
  Keep every non-separator character exactly, including repeated spaces and non-breaking spaces.
- When fixing selected list entries, already-correct entries remain unchanged and the paragraph count stays constant.
- Preserve trailing spaces, non-breaking spaces, punctuation, and typographic quotes unless the task explicitly asks
  to normalise them.

## File handoff

If Writer already has the document open, save and close it before a programmatic edit. Reopen the edited file in
Writer before finishing. A stale document window can overwrite the disk edit when it is saved.

Use direct document or XML editing only when it can preserve the untouched structure. A markdown or pandoc round trip
is not structure-preserving. If conversion is required and the task does not name another converter, use LibreOffice
and inspect the converted result in Writer.

Text typed through LibreOffice AutoCorrect may use typographic quotes. Inspect the saved document rather than
normalising apostrophes or whitespace. If LibreOffice is force-stopped, dismiss Document Recovery on relaunch before
opening the target.

Verify the transformed range, one adjacent unchanged range, paragraph count, and exact whitespace from the saved
document. A successful save or a visually similar PDF is not evidence that the Writer structure is correct.
