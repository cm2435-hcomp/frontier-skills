# Public skill compatibility audit

The first OSW-2 packages are H-owned rewrites based on observed task failures, not copied public packages. Public
document and media skills were useful evidence for the portable `SKILL.md` shape, but their large Python/Node stacks,
LibreOffice/Poppler assumptions, and sometimes unclear cross-host state made direct vendoring a poor first release.

The ten `web-*` packages are moved from `hcompai/hai` at release base commit `68d6e2ace2`. They are instruction-only,
use the existing authenticated browser surface, add no shell dependency, and remain under H ownership. They do not
launch a second browser or substitute shell HTTP for authenticated browser actions.

| Candidate | Requirements | Decision |
| --- | --- | --- |
| OpenAI/Anthropic office packages | Python/Node packages, LibreOffice, Poppler, shared task files | Rewrite narrowly; use the baked OSW-2 tools and standard library only |
| Generic Playwright/browser packages | Node runtime, browser download, separate browser state | Reject; conflicts with HoloTab's authenticated browser |
| Generic shell-first desktop guidance | Shared desktop files and broad offline reconstruction | Reject; observed to destroy native office state |
| HAI `web-*` packages | Existing browser tools only | Port for live migration compatibility |
