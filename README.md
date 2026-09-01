# Frontier Skills

H-owned, reviewed Agent Skills packages for browser and desktop agents.

Packages are selected by mode and skill-id globs, then published as immutable `release.json` and
`release.tar.gz` assets. The runtime verifies the complete release before copying only the selected packages into
the agent's shell workspace.

Validate and build a release with:

```bash
uv run python scripts/validate_registry.py
uv run python scripts/build_release.py --output dist/release
```

Skills must describe their real runtime requirements in `compatibility`. A package may guide browser or desktop
actions, but its scripts always run in the agent's configured shell. Do not imply shared cookies, processes, or files
unless the runtime topology proves that boundary.
