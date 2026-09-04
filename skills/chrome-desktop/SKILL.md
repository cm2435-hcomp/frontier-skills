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

## When the address is the result

When the task's output is a URL (the current address, a bookmark, a link typed into another document), navigate to
the page and copy the settled address bar after redirects and trailing-slash changes. Never type a URL from memory
or from a search snippet. A site that shows a shortened domain, as Google Maps does in its website field, is not
showing the full URL; open it and copy the address. Bookmark the specific page you landed on, not the site root.

If a results page is bot-walled and the task still needs a filtered URL, take the parameter names from a real URL
of that site, never from a guess.

## Preferences and cloud state

Chrome persists preferences in its profile's `Preferences` and `Local State` files. A running process may rewrite an
offline edit from memory. Prefer the browser UI; otherwise close the exact process, make the narrow edit, relaunch,
and read the stored value back.

A key you cannot find in `Preferences` is not evidence that the setting is missing, and a key you write that Chrome
does not know is silently ignored. To learn a key, snapshot `Preferences`, toggle the setting in the UI, stop the
exact process, and diff. Known values:

- Do Not Track is on `chrome://settings/cookies` ("Send a Do Not Track request") and is stored top level as
  `enable_do_not_track`; it is not under `webkit.webprefs`.
- Startup behaviour is `session.restore_on_startup`: 1 continue where you left off, 4 open specific pages (reads
  `session.startup_urls`), 5 open the New Tab page. A stale `startup_urls` list is harmless unless the value is 4.
- Clear on close moved in Chrome 118. It is under Site settings > Additional content settings > On-device site data
  (`chrome://settings/content/siteData`), stored as `profile.default_content_setting_values.cookies = 4`. Search
  Settings for "on-device" or "site data", not "delete".
- To remove one site's data durably, first close every tab of that site; an open page re-sets its cookies within
  seconds. Then delete each matching entry (apex, `www`, subdomains) on `chrome://settings/content/all`, re-search to
  confirm zero entries, and do not revisit the site before finishing.

Cloud documents and account state are not interchangeable with local files. Use the signed-in browser when the task
names a cloud resource, and verify the resulting URL or visible account state before finishing.
