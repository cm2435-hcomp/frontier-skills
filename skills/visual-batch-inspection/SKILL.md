---
name: visual-batch-inspection
description: Inspect long videos efficiently with bounded frame sampling and contact sheets before detailed review.
compatibility: Requires ffmpeg and ffprobe in the shell, plus access to the same video files as the desktop application.
---

Use bounded sampling to find relevant intervals before scrubbing frame by frame.

1. Check `command -v ffmpeg` and `command -v ffprobe`. If either is unavailable, keep the failure visible and use the
   desktop application's timeline rather than attempting a large install without evidence it is allowed.
2. Read duration and stream metadata with `ffprobe`.
3. Sample a modest number of evenly spaced frames—usually 12 to 30—scaled to thumbnails and arranged as a labelled
   contact sheet. Keep timestamps visible.
4. Identify candidate intervals from the contact sheet, then inspect only those intervals at higher temporal density.
5. Perform edits in the requested application and review the rendered/exported result there. Sampled source frames do
   not prove that an edit or export succeeded.

Example starting point, adjusted to the video's duration and output directory:

```bash
ffmpeg -i INPUT -vf "fps=1/20,scale=320:-1,tile=5x4" -frames:v 1 contact-sheet.jpg
```

Avoid unbounded frame extraction and avoid loading the whole video into memory.
