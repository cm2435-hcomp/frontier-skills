---
name: libreoffice-impress
description: Inspect, edit, and verify LibreOffice Impress presentations without losing native structure.
compatibility: Requires a disposable desktop workspace shared with LibreOffice Impress and Python 3 for the read-only inspector.
---

Use this for a presentation opened or intended for LibreOffice Impress. Do not assume these details apply to WPS
Presentation or Microsoft PowerPoint.

## Inspect the actual object

For a `.pptx`, run `python scripts/inspect_presentation.py FILE --slide N` before choosing the object to change. The
report walks text and pictures inside groups and shows shape geometry, placeholders, paragraphs, bullets, runs,
end-of-paragraph properties, hyperlinks, notes, and the master's field placeholders without resaving the deck.

- The title and body placeholder are separate shapes. "The content" means the body placeholder.
- "First textbox" means the text shape with the smallest `top`, including text nested inside groups. It does not mean
  the first shape in archive order.
- "A note" on a slide means the speaker notes (`notes_slide` in the report; View > Notes in Impress), never a text
  box on the canvas. Verify that the on-slide shape count is unchanged after adding one.
- "The picture" is any element carrying `a:blip`: a `p:pic`, or a `p:sp` whose `spPr` has a `blipFill`. The report
  marks both as `picture: true`. Libraries that only count `p:pic` miss cropped or shaped photos. When several match,
  small repeated blips are usually bullet icons and the large one is the photo.
- Formatting is stored per run and is read per run. Set every named attribute on every run of the target text,
  including runs the report marks `whitespace_only`, and on each paragraph's `a:endParaRPr`. Preserve attributes and
  the `a:hlinkClick` child the task did not mention; rewriting `a:rPr` without it removes the link.
- Slide number, date, and footer fields inherit from the master's `sldNum`, `dt`, and `ftr` placeholders (listed under
  `master_field_placeholders`). Format them in View > Master Slide, or patch the master, every layout, and every
  slide; per-slide copies alone do not change what Impress shows.
- Strike-through is `strike="sngStrike"` on the run's `a:rPr`. The value `sng` is invalid even if a library accepts it.
- Bullet existing text by replacing `<a:buNone/>` with the requested bullet property on that paragraph. Do not add a
  second paragraph. A paragraph ending in `:` is normally a heading, not the first list item.
- An instruction phrased as a question about the open deck still expects the deck to be changed.

## Exact LibreOffice values

Named colors refer to LibreOffice's installed palette, not CSS names. Read the current machine's value from
`/usr/lib/libreoffice/share/palette/standard.soc`. Known Standard palette values include Green `00A933`, Gold
`FFBF00`, Orange `FF8000`, Blue `2A6099`, Lime `81D41A`, and Dark Red 2 `C9211E`.

Text typed through LibreOffice AutoCorrect may use typographic quotes. Inspect a nearby run or the saved XML instead
of normalising apostrophes or whitespace.

If LibreOffice is force-stopped, dismiss Document Recovery on relaunch before opening the target. A recovery copy is
not evidence that the requested file was saved.

## Edit and hand back

If Impress already has the deck open, save and close it before a programmatic edit. Reopen the edited file in Impress
before finishing. A stale open buffer can overwrite the disk edit when it is saved. Patch the narrowest XML member
when unrelated shapes must remain byte-stable; a library resave may rewrite the full package.

After editing, rerun the inspector on the changed slide, confirm slide and shape counts, reopen the deck, and inspect
the changed object plus one nearby unchanged object. The inspector proves structure, not rendering or animation.
