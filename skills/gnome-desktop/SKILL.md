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
