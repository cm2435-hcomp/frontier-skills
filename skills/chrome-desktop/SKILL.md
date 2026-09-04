---
name: chrome-desktop
description: Operate and verify the existing Chrome session, profile state, URLs, and browser preferences.
compatibility: Requires a desktop workspace with an existing Chrome session and its profile on the same filesystem.
---

Use this for Chrome process, profile, preference, account-state, and active-URL tasks. General web navigation does not
need this skill.

## Preserve the live session

- Inspect the existing Chrome process before starting another one. When the runtime exposes a debugging endpoint,
  preserve its configured port and verify the endpoint after any restart.
- Never kill Chrome by a broad process-name pattern. Identify the exact process first so the command does not also
  terminate the shell or an unrelated browser session.
- Open a requested URL in the existing browser session. The active address can be part of the required final state,
  even when the page itself fails to load.
- Keep signed-in state unless the task explicitly asks to remove it. Clear cookies only to resolve a proven site loop,
  and scope the change as narrowly as the browser permits.

## Preferences and cloud state

Chrome persists preferences in its profile's `Preferences` and `Local State` files. A running process may rewrite an
offline edit from memory. Prefer the browser UI; otherwise close the exact process, make the narrow edit, relaunch,
and read the stored value back.

Cloud documents and account state are not interchangeable with local files. Use the signed-in browser when the task
names a cloud resource, and verify the resulting URL or visible account state before finishing.
