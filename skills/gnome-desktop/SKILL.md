---
name: gnome-desktop
description: Change GNOME desktop settings only when the required device and visible state exist.
compatibility: Requires a GNOME desktop session with access to its real device and settings state.
---

Use this for GNOME settings and operating-system state exposed through the desktop.

## Prove the backing state exists

Before changing a hardware-backed setting, inspect the real device inventory. Power, Bluetooth, display, audio, and
network controls cannot produce a truthful visible result when the corresponding device or service is absent.

Changing a stored setting is not enough when the task asks to show a resulting state. Verify both the persisted value
and the visible effect. Do not create a mock service, fake device entry, or placeholder UI to imitate missing
hardware. If the required backing resource is structurally absent, treat the request as infeasible under the runtime's
own reporting contract.

Use GNOME's supported settings UI when provenance matters. If a direct settings command is allowed, read the value
back from the same schema and confirm the desktop reflects it before finishing.

## Exact locations

- GNOME Terminal profiles are UUIDs. List them with `gsettings get org.gnome.Terminal.ProfilesList list`, then write
  under `org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:<uuid>/`. The path `:default/` is
  not a profile. Check a window size change by opening a new terminal and running `stty size`.
- "Default application for videos" means every MIME type in the category, not a hand-typed list. Take the set from
  the application's `.desktop` `MimeType=` line and `/usr/share/mime/video`, run `xdg-mime default` over all of it,
  and confirm with `xdg-mime query default` on the same set. Settings > Default Applications > Video does the same
  through the UI.
- When counting or summarising files in a project tree, exclude dependency directories such as `node_modules` unless
  the task includes them.
- A user created inside an SSH `ChrootDirectory` jail also needs its `/etc/passwd` home directory to exist on the
  host, or `su -` and host logins fail.
