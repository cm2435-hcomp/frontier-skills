# Runtime probe receipts

All probes use release `2026-09-01.1` with archive digest
`dbc158c7c4f27c0297ec06c21de7e82e78d2f89ca1d7d13d19c4a5531bad93fd`.

| Date | Runtime | Selection | Result | Install time | Bytes | Notes |
| --- | --- | --- | --- | ---: | ---: | --- |
| 2026-09-01 | `LocalCodeSandbox` in a temporary workspace | Three OSW-2 task skills | Pass | 0.039 s | 7,236 | Selected order matched the manifest and `CATALOG.md` was readable. |
| 2026-09-01 | `PureDockerCodeSandbox` in a fresh container | `office-artifact-surgery` | Pass | 1.313 s | 3,364 | The advertised `SKILL.md` was readable inside `/workspace`; no host bind mount was used. |
| 2026-09-01 | OSW-2 Sky preflight, task 009 | `completion-verification` | Blocked before task setup | n/a | n/a | Sky job `19664` failed because the submitting shell did not provide a coordinator identity credential. No VM, model call, or benchmark trial ran. This is launch authentication, not a registry result. |

The local and Docker probes also consumed the release from the temporary public mirror at
`cm2435-hcomp/frontier-skills`. The logical source remains `h/frontier-skills`; production should use the
`hcompai/frontier-skills` release URL once the organisation repository exists.

## Still required

- remote sandbox and OSW-2 co-location proof after coordinator credentials are available;
- browser isolated-state probe;
- the isolated completion-verification control/treatment gate;
- the combined OSW-2 slice and matched full-suite runs.

Do not use these local receipts as rollout gates. They prove packaging and ordinary-shell readability only.
