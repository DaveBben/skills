---
name: setup-my-env
description: "Use this skill whenever the user wants an app, terminal, editor, shell prompt, note app or system setting configured for them, above all to make text easier to read: font, font size, line spacing, line length, light or dark mode, theme, colors or contrast. Use it on: 'set up my environment', 'set up my new Mac', 'make my terminal readable', 'configure VS Code for readability', 'make Obsidian easier to read', 'set up this app like my others', 'the colors look off in light mode', 'what font size should I use', 'is this theme readable'. Load it before changing an app's fonts, sizes, spacing, theme, or colors."
license: MIT
compatibility: "Any agent. The recorded settings are macOS paths; the scripts need python3, fontTools for font measurements, and uv for the iTerm2 Python API."
metadata:
  version: "0.1.0"
---

# Set up my env

Configure the user's apps to the same targets as the rest of their setup, and carry those targets to apps not yet configured.

## Before changing anything

* **Back up:** copy every file you will change into `~/Backups/<topic>-<YYYY-MM-DD>/` and tell the user the path.
* **Find the real settings store:** read where the app keeps its settings and whether the running app overwrites that file when it saves or quits. When it does, change the setting through the app's API or quit the app first.
* **One app at a time:** finish an app, ask the user for a screenshot, check it, then start the next app.
* **Verify by reading back:** after a change, read the stored value back from the file or the app, and measure the result in a screenshot where a number can be measured, such as characters per line.

## Readability

Read `references/readability.md` before you choose a font, size, line spacing, line length, theme or color.
It holds the targets and the formulas behind them, a procedure that works for any app, the values already applied to iTerm2, zsh, Claude Code, VS Code and Obsidian, and the mistakes to avoid.

`scripts/contrast.py` prints the WCAG contrast ratio of two colors and moves a color's lightness, keeping its hue, until it reaches a target ratio.
Run `python3 scripts/contrast.py --help` for usage.
