# Frontier Skills

`frontier-skills` is H's reviewed package registry for browser and desktop agents. It owns skill content and
deterministic releases. HAI owns selection, verification, installation, and model-visible discovery; see the
[filesystem agent skills guide](https://github.com/hcompai/hai/blob/codex/skill-registry-runtime/sagent/docs/agent-skills.md)
for the runtime contract.

Publishing a package proves that it is valid and installable. It does not prove that a model will use it or that it
improves a benchmark.

## Repository contract

```text
registry.yaml                  # release revision and mode membership
skills/<skill-id>/
  SKILL.md                     # model-facing entry point and compatibility declaration
  scripts/                     # optional helpers reached from SKILL.md
scripts/
  validate_registry.py         # package and metadata validation
  build_release.py             # deterministic manifest and archive producer
```

`registry.yaml` lists each package once:

```yaml
schema_version: 1
revision: 2026-09-04.0
skills:
  - name: web-gmail
    modes: [browser]
```

The package path is always `skills/<name>`. Name, description, and compatibility live in Agent Skills-compatible
`SKILL.md` frontmatter:

```markdown
---
name: web-gmail
description: Drafting emails in Gmail using the web UI.
compatibility: Requires a browser session with Gmail available.
---
```

Compatibility tells the model what the package requires. It does not cause the runtime to install dependencies.

## Authoring rules

A package should contain reusable knowledge or a helper that is difficult to recover reliably during one task. Good
packages capture exact application semantics, file-format details, safe inspection procedures, and verification
steps tied to observed failures.

Do not add generic advice, benchmark answers, evaluator details, credentials, machine-specific secrets, or helpers
that bypass the supported application write surface. Do not claim browser, desktop, and shell state are shared unless
the declared deployment topology guarantees it.

Modes describe the interaction surface. `desktop` applies to desktop tasks and `browser` to web tasks. Helpers always
run in the agent's configured shell, which may be on a different host. Put required commands, file access, and any
same-workstation assumption in `compatibility`.

## Validate and build

```bash
uv run python scripts/validate_registry.py
uv run pytest -q
uv run python scripts/build_release.py --output dist/release
```

The producer emits one `release.tar.gz` containing its authenticated `release.json` manifest and every declared
package file. It also writes a detached `release.json` for human inspection; the runtime ignores that copy.

Builds are deterministic. Never replace assets under an existing revision. A content change requires a new revision
and digest.

## Runtime consumption

HAI selects packages by pinned revision, digest, modes, includes, and excludes. It verifies the complete release,
copies selected packages into `<workspace>/.agents/skills`, writes `CATALOG.md`, and advertises their `SKILL.md` paths
to the model. The model reads and runs packages with its normal filesystem and shell tools.

The runtime fails closed on an invalid manifest, mismatched archive digest, unsafe path, unmatched filter, empty
selection, or existing installation. It does not fall back to a moving branch or an unverified local copy.
