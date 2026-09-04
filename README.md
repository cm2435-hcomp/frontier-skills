# Frontier Skills

`frontier-skills` is H's reviewed package registry for browser and desktop agents. It owns skill content and
deterministic releases. HAI owns selection, verification, installation, and model-visible discovery; see the
[filesystem agent skills guide](https://github.com/hcompai/hai/blob/codex/skill-registry-runtime/sagent/docs/agent-skills.md)
for that runtime contract and the complete PR map.

The registry is opt-in while its evaluation gates are open. Publishing a package proves that it is valid and
installable. It does not prove that a model will read it or that it improves a benchmark.

## Repository contract

```text
registry.yaml                  # release inventory, modes, paths, and provenance
skills/<skill-id>/
  SKILL.md                     # model-facing entry point and compatibility declaration
  scripts/                     # optional helpers reached from SKILL.md
audits/                        # source evidence, portability decisions, and runtime receipts
evaluations/                   # matched experiment configs and launchers
scripts/
  validate_registry.py         # package and metadata validation
  build_release.py             # deterministic manifest and archive producer
```

`registry.yaml` is the release inventory. Each entry declares a unique skill ID, prompt description, eligible
execution modes, package path, and provenance:

```yaml
schema_version: 1
source: h/frontier-skills
revision: 2026-09-04.0
skills:
  - name: libreoffice-impress
    description: Inspect, edit, and verify LibreOffice Impress presentations without losing native structure.
    modes: [desktop]
    path: skills/libreoffice-impress
    provenance:
      repository: hcompai/frontier-skills
      license: H-owned original
```

Each package starts with Agent Skills-compatible frontmatter:

```markdown
---
name: libreoffice-impress
description: Inspect, edit, and verify LibreOffice Impress presentations without losing native structure.
compatibility: Requires a disposable desktop workspace shared with LibreOffice Impress and Python 3.
---
```

The name and description must match `registry.yaml`. `compatibility` tells the model what the package requires; it
does not cause the runtime to install dependencies.

## Authoring rules

A package should contain knowledge or a helper that is both reusable and difficult to recover reliably during one
task. Good packages capture exact application semantics, file-format details, safe inspection procedures, and
verification steps tied to observed failures.

Do not add:

- generic advice such as planning, checking work, or trying another route;
- benchmark answers, evaluator details, credentials, or machine-specific secrets;
- claims that browser, desktop, and shell state are shared unless the declared topology proves it;
- setup instructions that silently mutate the runtime before the model chooses to use the package; or
- a helper whose output is treated as proof that a visible application changed.

Write the narrowest package that addresses the evidence. Keep optional references and scripts beside `SKILL.md`, and
link them from the instructions so the model can discover them with normal filesystem tools. Helpers should preserve
the supported application write surface. Read-only inspectors are preferred when direct database or archive writes
could bypass the state the task is meant to exercise.

## Compatibility and modes

Modes select packages by interaction surface:

- `desktop` means the instructions apply to a desktop task;
- `browser` means the instructions apply to a web task.

Scripts always run in the agent's configured shell, which can be on a different host from the browser or desktop.
State every load-bearing runtime requirement in `compatibility`, including required commands, file access, and any
same-workstation assumption. A package should tell the model how to check a requirement and choose another approach
when it is absent.

The first runtime does not support mobile and does not resolve dependencies from compatibility metadata.

## Validate and build

```bash
uv run python scripts/validate_registry.py
uv run pytest -q
uv run python scripts/build_release.py --output dist/release
```

The producer emits:

- `release.tar.gz`, containing its authenticated `release.json` manifest and every declared package file; and
- a detached copy of `release.json` for human inspection. The runtime ignores this copy.

Build the same revision twice before publishing and require identical digests. Never replace assets under an existing
revision. A content change requires a new revision and digest.

## Runtime consumption

HAI selects packages by pinned revision, digest, modes, includes, and excludes. It verifies the complete release,
copies only the selected packages into `<workspace>/.agents/skills`, writes `CATALOG.md`, and advertises the resulting
`SKILL.md` paths to the model. The model reads and executes packages with its existing shell and filesystem tools.

The runtime fails closed on an invalid manifest, mismatched archive digest, unsafe path, unmatched filter, empty
selection, or existing installation. It does not fall back to a moving branch or an unverified local copy.

## Evidence and rollout

Task evidence, compatibility decisions, and runtime probe receipts live under `audits/`. Matched benchmark configs
and launch rules live under `evaluations/`.

Every evaluation report must separate:

1. installation: the selected package was delivered and advertised;
2. use: the trajectory read `SKILL.md`, followed a reference, or ran a helper; and
3. outcome: reward, success, latency, and benchmark errors changed under a matched control.

The current app-specific release is a candidate for the OSWorld three-arm ablation. It is not a production default,
and the later HAI migration remains blocked until the treatment preserves the monolithic prompt's performance and
beats the same slim prompt without skills.
