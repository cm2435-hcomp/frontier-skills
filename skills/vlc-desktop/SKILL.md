---
name: vlc-desktop
description: Load media into the existing VLC instance and verify its durable playback state.
compatibility: Requires a desktop workspace where the harness may prelaunch VLC and expose its local HTTP interface.
---

Use this for VLC playback and preference tasks.

## Reuse the existing instance

Inspect the running VLC process before launching another instance. A managed desktop may prelaunch VLC with a local
HTTP interface configured by `http-port` and `http-password` in `~/.config/vlc/vlcrc`. A second instance can fail to
bind that port while the checker continues to observe the idle first process.

Load media into the existing window through Media > Open File. When the local interface is already configured, the
equivalent `in_play` request may load the exact `file://` URI into that same process. Do not expose the interface
outside the local machine or print its password.

Verify the managed instance reports `playing` and that its current input resolves to the requested file. A successful
launch command or a second VLC window is not evidence that the observed instance changed.

For a persisted setting, use VLC's preferences UI or stop the exact process before editing `vlcrc`, then relaunch and
read the value back. A running instance may overwrite an offline edit on exit.
