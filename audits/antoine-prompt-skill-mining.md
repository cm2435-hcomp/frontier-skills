# Antoine Prompt Skill Mining

## Decision

Create evidence-backed application packages for LibreOffice Impress, Calc, Writer, Thunderbird, and VS Code. Add
small extraction packages for Chrome, VLC, and GNOME so the evaluated prompt has no application-specific procedure.
Keep universal agent behavior in the base prompt and keep evaluator contracts out of the registry.

The primary evidence is HAI PR #13201 at commit `64d5106b15b014f5e5bbef46a77a6004e610f3d0`. Its run completed
360 of 361 OSWorld tasks with 277 successes, a 76.9% success rate. The best old hybrid run had 258 successes. Because
the PR changed a prompt bundle, only the task-level failure analysis is used to select package content.

The target runtime is HAI's `osworld_light_desktop_apps` image: Debian 13 with Python 3, LibreOffice, Thunderbird,
and VS Code installed by the image build. Those application packages are not version-pinned in the Dockerfile, so
the packages rely on the recorded interfaces and persisted formats rather than claiming compatibility with an exact
application version. A future image lockfile or digest should be recorded alongside evaluation results.

## Included

| Package | Failure evidence | Portable content |
| --- | --- | --- |
| `libreoffice-impress` | 7/7 analyzed failures regraded from 0 to 1 after correcting one constant or target | Standard palette source, `sngStrike`, grouped text, placeholder and bullet semantics |
| `libreoffice-writer` | 4/5 analyzed failures prompt-flippable | Exact case and table transformations, whitespace and paragraph preservation |
| `libreoffice-calc` | 2/3 pivot failures prompt-flippable | Real pivot object creation, formulas, percentages, chart range structure |
| `thunderbird-desktop` | 2/3 failures prompt-flippable | Live preferences, mbox location, decoded-subject export names |
| `vscode-desktop` | 4/6 failures prompt-flippable | Whole keybinding objects, context discovery, debugger and extension state |
| `chrome-desktop` | Prompt extraction only | Existing session, profile persistence, active URL, and cloud-account state |
| `vlc-desktop` | One concrete regression plus prompt extraction | Managed instance and local playback-state verification |
| `gnome-desktop` | Prompt extraction only | Device-backed setting checks and honest infeasibility |

HAI PR #13157 supplies the CUA Gym task-profile evidence. Open PR #13217 supplies supporting failure classes at head
`09ded27d048f4e8a987cdd1a1b2ba913b6cb7b9b`: 24 library-artifact failures, 23 wrong-target failures, and 5 stale
application-buffer failures. It is not treated as an uplift result because it combines prompt, harness, tool, and
desktop-image changes.

## Excluded

| Finding | Destination | Reason |
| --- | --- | --- |
| Exact output paths, literal values, missing-value honesty | Base prompt | Always applicable; retrieval would make a core invariant optional |
| Stale open buffers | One base-prompt sentence plus exact app procedures | Cross-application risk, with recovery differing by application |
| Named terminal or application provenance | Benchmark or product contract | Whether method is graded cannot be inferred from application behavior |
| Evaluator Ctrl+S, cache paths, active URL checks, infeasible marker | Benchmark prompt or harness | Private evaluator behavior is not portable product knowledge |
| GIMP export focus | Deferred | One concrete regression and no procedure in the evaluated prompt to extract |
| Additional Chrome content from PR #13222 | Deferred | The prompt iteration has not completed a suite evaluation |
| ALE application skills | Deferred | PR #13154 found GUI interaction in only 2/99 tasks |
| Generic completion verification | Removed | Installed 8/8, read 0/8, and changed success by 0 tasks |

## Content Rule

A package includes only exact application semantics, a short procedure the model repeatedly got wrong, or a bounded
read-only helper that exposes durable application state. It does not restate tool schemas, wrap standard commands, or
contain benchmark task IDs, evaluator logic, credentials, or claims about lookalike applications.
