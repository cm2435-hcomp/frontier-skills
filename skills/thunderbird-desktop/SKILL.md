---
name: thunderbird-desktop
description: Inspect and change Thunderbird preferences, profiles, mailboxes, and exports through supported surfaces.
compatibility: Requires a disposable desktop workspace shared with Thunderbird and Python 3 for the redacted profile inspector.
---

Use this for Thunderbird settings, account, mailbox, filter, and message-export tasks.

Run `python scripts/inspect_profile.py` to find profiles, preference names and primitive values, and mailbox paths. The
inspector redacts every string preference and never reads message bodies.

## Preferences and accounts

- Thunderbird persists preferences under the active profile's `prefs.js`, but the running application owns that
  state and may rewrite an offline edit.
- Change a live preference through Settings > General > Config Editor (`about:config`) and then re-read the persisted
  preference. Do not invent a preference key from the visible label.
- Applying incoming filters to subfolders uses `mail.server.default.applyIncomingFilters = true` together with
  `mail.imap.use_status_for_biff = false`; creating a periodic filter is a different behavior.
- The account wizard supports IMAP and POP3 incoming servers. A hand-written account block in `prefs.js` is not proof
  that Thunderbird loaded the account.

## Mailboxes and exports

Thunderbird IMAP folders are mbox files under the active profile's `ImapMail/` tree. Python's standard-library
`mailbox` module can inspect a disposable copy when shell inspection is useful. Do not mutate the live mbox.

When exporting messages, use the decoded `Subject` exactly for each `.eml` filename unless the task supplies another
name. Do not slugify, lowercase, or replace punctuation. Prefer File > Save As from Thunderbird when application
provenance matters.

After a change, verify it in Thunderbird and then inspect the freshly persisted profile state. A shell edit alone is
not evidence that the running application accepted it.
