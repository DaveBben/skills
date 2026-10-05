# Values applied

The display is a 27-inch 5K at 2x, where 1 point is 0.233 mm, and the user sits 46 to 56 cm away.
Backups of every original file are in `~/Backups/readability-2026-10-02/`.

### iTerm2

* **Profile:** "Dave Profile", GUID `4F0F4EB3-BE9B-4708-A7AE-566A1F3CC9F2`, the default profile.
  "Use Separate Colors for Light and Dark Mode" is on.
* **Font:** `FiraCodeNFM-Reg 20` (Fira Code Nerd Font Mono).
  20 pt gives 0.26° at 56 cm.
* **Vertical Spacing:** 1.14.
  iTerm2 multiplies the font's own line height by this value (`PTYTextView.m`: `lineHeight = ceil(charHeightWithoutSpacing * verticalSpacing)`).
  Fira Code's own line height is 1.23, so the result is 1.40.
* **Brighten bold text:** off, in both modes.
* **Thin strokes:** Retina, dark backgrounds only (value 1).
* **Theme:** Light (Settings, Appearance, Theme, value 0), so the profile uses its light colors while macOS stays dark.
* **Minimum Contrast:** 0.34 dark, 0.54 light.
  Each sits just below the weakest palette color's brightness difference from the background (0.353 and 0.548).
  So the setting leaves the palette alone and lifts only dimmer colors that programs send directly.
* **Light colors:** background `#FAFAFA`, foreground and bold `#101010`, link `#1271D4`.
* **Dark colors:** background `#15191F`, foreground `#DCDCDC`, bold `#FFFFFF`, link `#328EEE`.
  ANSI 1, 4, 5 and 8 in the dark palette were lifted by contrast.py --fix; the rest already passed.
* **How to apply:** use the iTerm2 Python API, with `EnableAPIServer` on, through `uv run --with iterm2 python script.py`.
  The script gets the profile with `iterm2.Profile.async_get(connection, [GUID])`.
  It then calls setters such as `async_set_normal_font`, `async_set_vertical_spacing`, `async_set_ansi_8_color_light`, `async_set_minimum_contrast_dark`, and `async_set_use_bright_bold_light`.
  Set the app theme with `iterm2.preferences.async_set_preference(connection, PreferenceKey.THEME, 0)`.

### Shell and Claude Code

* **Powerlevel10k** (`~/.config/p10k/p10k.zsh`, Pure style): the prompt colors are palette numbers: grey 8, red 1, yellow 3, blue 4, magenta 5, cyan 6, and white 7.
  The snazzy hex colors before them were invisible on white.
* **Claude Code status line** (`~/.claude/scripts/context-bar.sh`): accent `\033[34m`, grey text and empty bar `\033[90m`.
  They replace 256-color codes 74, 245, and 238.
* **Claude Code theme:** `"theme": "light-daltonized"` in `~/.claude/settings.json`.
  Use `dark-daltonized` in dark mode.
  Claude Code's ANSI themes take their colors from the terminal palette instead.
* **Claude Code prose width:** `"maxProseWidth": 80`.
  Tables and code blocks ignore it.
* **zsh plugins:** fast-syntax-highlighting and zsh-autosuggestions already use palette colors.

### VS Code

Settings are in `~/Library/Application Support/Code/User/settings.json`, which VS Code applies on save.

* **Sizes:** `editor.fontSize`, `terminal.integrated.fontSize`, `debug.console.fontSize`, and `chat.fontSize` are 20.
  `markdown.preview.fontSize` is 22, because Atkinson's x-height is 8% shorter than Fira Code's.
* **Fonts:** editor `Fira Code`, terminal `FiraCode Nerd Font Mono`, chat `FiraCode Nerd Font`, and preview `Atkinson Hyperlegible Next`.
* **Line height:** `editor.lineHeight` is unset, so VS Code uses 1.5 on macOS.
  `markdown.preview.lineHeight` is 1.5.
  `terminal.integrated.lineHeight` is 1.14, meant to match iTerm2's 1.40.
  Whether VS Code multiplies the font size or the font's own line height is not established, so measure the line pitch in a screenshot before relying on it.
* **Terminal bold:** `terminal.integrated.drawBoldTextInBrightColors` is false.
  `terminal.integrated.minimumContrastRatio` stays at its default of 4.5.
* **Markdown source:** `"[markdown]": { "editor.wordWrap": "bounded", "editor.wordWrapColumn": 80 }`.
* **Theme:** Alabaster (`tonsky.theme-alabaster`).
  `workbench.preferredLightColorTheme` is Alabaster and `workbench.preferredDarkColorTheme` is Catppuccin Mocha.
  The command "Preferences: Toggle between Light/Dark Themes" switches between them.
  `window.autoDetectColorScheme` is off, so VS Code does not follow macOS.
* Dark theme Catppuccin Mocha is unchecked; check and fix it and its terminal palette before using dark mode.
* **Alabaster fixes** under `editor.tokenColorCustomizations["[Alabaster]"]`: strings `#3D7E23` (was 3.9:1), and punctuation and escapes `#6F6F6F` (was 4.2:1).
* **Alabaster fixes** under `workbench.colorCustomizations["[Alabaster]"]`: `editorLineNumber.foreground` `#6B7268` (was 2.4:1).
  The terminal background, foreground, and 16 ANSI colors are set to the iTerm2 light colors above.
* **Preview:** `markdown.previewStyles` comes from the local extension dave.markdown-readable-width (source ~/projects/vscode-markdown-readable/); tables are centred on a wider rule.

### Obsidian

The vault is `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/notes/`, with settings in `.obsidian/`.
Quit Obsidian before editing these files with `osascript -e 'tell application "Obsidian" to quit'`, then reopen it with `open -a Obsidian`.

* **`appearance.json`:** `cssTheme` `Minimal`, `textFontFamily` `Atkinson Hyperlegible Next`, `monospaceFontFamily` `FiraCode Nerd Font Mono`, `baseFontSize` 22, and `theme` `moonstone` (light).
  Dark mode is `obsidian`.
* **`app.json`:** `readableLineLength` true and `strictLineBreaks` true.
* **Minimal Theme Settings** (`plugins/obsidian-minimal-settings/data.json`): `textNormal` 22, `lineWidth` 29, `lineWidthWide` 36, and `lineHeight` 1.5.
  The color schemes are `minimal-default-light` and `minimal-atom-dark`.
  29 em at 0.436 em per character is about 66 characters, confirmed in a screenshot at 60 to 68.
* **Minimal default light contrast:** body text about 19:1, muted text about 4.6:1, and faint text about 2:1.
  Faint text is used only for placeholders and similar details.
* **Known trade-off:** Fira Code in code blocks fits about 52 characters in the prose column, so long code lines wrap.


### Neovim, not configured

Neovim, not configured: needs `vim.o.linebreak = true`, a light colorscheme that passes contrast, and `pipe_table.wrap = true` in render-markdown.nvim. Configure it only when asked.
