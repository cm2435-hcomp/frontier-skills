---
name: vscode-desktop
description: Configure and verify VS Code keybindings, settings, extensions, and debugger-visible state.
compatibility: Requires a disposable desktop workspace shared with VS Code and the code CLI when command-line verification is used.
---

Use this for VS Code keybindings, settings, extensions, and debugger-state tasks.

## Keybindings and settings

- A keybinding is a complete object. Match `key`, `command`, and `when`; omitting the context creates a broader and
  structurally different binding.
- The context named by the task normally determines `when`. Terminal bindings commonly use `terminalFocus`; Explorer
  and tree-view find bindings use `listFocus && listSupportsFind`.
- Do not guess a command ID from its visible label. Open Keyboard Shortcuts, search for the row, and read its Command
  and When columns. Removing a default binding through the UI writes a `-command` entry with the matching `when`.
- The running application can rewrite settings files from memory. Change settings through VS Code or close it before
  an exact JSON edit, then reopen and verify through the UI.

## Debugger and extensions

"Visualize the variables" means debugger state, not a plot. Fix syntax errors, set a breakpoint after the final
assignment, start the debugger, and finish while paused with VARIABLES and Locals expanded.

Verify extension identifiers with `code --list-extensions`. IDs are case-sensitive and may not match the marketplace
display name. Read the actual output instead of inferring the ID.

After an edit, parse the JSON and check the complete requested object. After a debugger task, inspect the fresh screen.
After an extension task, rerun the CLI listing. A successful click or valid JSON file alone is not the final state.
