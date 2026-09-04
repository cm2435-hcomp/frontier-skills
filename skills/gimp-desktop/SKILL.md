---
name: gimp-desktop
description: Edit images in GIMP so the live image window carries the result, and recognise what GIMP 2.10 cannot do.
compatibility: Requires a desktop workspace with GIMP 2.10 and the target image on the same filesystem.
---

Use this for tasks that name GIMP or start with an image already open in GIMP.

## The open image is the deliverable

GIMP is often launched on the target image before the task begins and can take 20 seconds or more to appear. Check
for the process or take a fresh screenshot before choosing a route; do not start a second instance.

GIMP never reloads a file that changed on disk. An edit made with Pillow, ImageMagick, or a script is invisible to
the image already open in GIMP, and the open image is what a later export or save produces. Either make the edit
inside GIMP, or after a scripted edit close the stale image (Ctrl+W, Discard) and reopen the edited file so it is the
active image.

Before finishing, leave the edited image open with the image window focused. Close the Script-Fu and Python-Fu
consoles and any dialog, wait for the status bar to clear after an export, then click the canvas so the image window
owns keyboard input. A correct file on disk with a console dialog in front of it is not the finished state. Prefer
menu and shortcut edits (Colors, Layer > Transparency > Add Alpha Channel, Select by Color, Delete) over the console
when the operation is available there.

## What GIMP 2.10 cannot do

- Export is raster only. The Export dialog's file-type list is exhaustive, and the SVG plug-in is import only. An
  SVG wrapping a PNG, or a conversion by another tool, is not a GIMP export.
- Image > Scale Image interpolates existing pixels. Nothing in GIMP 2.10 adds resolution or detail, and JPEG size
  grows with pixel count, so "increase resolution without growing the file" cannot be met by crushing quality.
- A still image carries no audio unless data was embedded. Triage in a few steps (segment parse, bytes after the
  end marker, `exiftool`, `binwalk`, `steghide`/`outguess` with an empty passphrase). If all are clean, the subject
  does not exist. Do not brute-force passphrases or build tools from source.

When the task requires a capability that is structurally absent, stop and report it under the runtime's infeasible
reporting contract instead of shipping a lookalike.
