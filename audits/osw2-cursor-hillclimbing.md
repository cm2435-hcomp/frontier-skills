# OSW-2 skill opportunity audit

Source evidence is Antoine's Cursor canvas `canvas-Mn27BE9xcIjXZcFNvKMmziDm`, baseline `5d23eomw`, and the accepted
run `o8z81viw`. Infrastructure, evaluator, reset, serving, payload, and typing-corruption failures are excluded from
skill attribution.

| Task family | Observed behavior | Package |
| --- | --- | --- |
| Writer/Calc/Impress and OOXML | Offline reconstruction destroyed native state; saved artifacts were not reopened | `office-artifact-surgery` |
| Long video inspection | Repeated GUI scrubbing where bounded sampling could locate intervals | `visual-batch-inspection` |
| Application SQLite state | Shell inspection was useful, but direct mutation risked bypassing app invariants | `safe-live-database-inspection` |
| Completion overclaim | Requested criteria were not checked through the final surface | Experimental `completion-verification` |

The completion package is evaluated alone before joining the combined treatment. Generic shell-first behavior is not
included.
