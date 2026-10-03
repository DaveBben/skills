# Making apps readable

This file holds the targets, a procedure for any app, the values applied on 2026-10-02, and the mistakes made that day.
Each target is labelled **measured** (a controlled study), **standard** (WCAG or a style guide), or **convention** (designer practice, no study).

## Targets

| Setting | Target | Evidence |
|---|---|---|
| Font size | Lowercase x-height of at least 0.2° of visual angle, aiming for 0.25° | measured |
| Font choice | Large x-height, a marked zero, and distinct `I`, `l`, and `1` | measured (x-height), convention (shapes) |
| Weight | Regular, or Fira Code's Retina weight (450), never Light or thinner | measured |
| Line height | 1.4 to 1.5 for prose, 1.3 to 1.5 for code, matched across tools | measured and standard (prose), convention (code) |
| Prose line length | About 55 characters per line, within 45 to 75 | measured (55), convention (range) |
| Code line length | 80 to 100 characters | convention |
| Letter and word spacing | Font default | measured |
| Paragraph spacing | A blank line, 0.75 to 1.5 times the font size, no indent | convention |
| Polarity | Dark text on a light background | measured |
| Text contrast | At least 4.5:1 for every text color, 7:1 for body text | standard (WCAG 2.2 AA and AAA) |
| Syntax colors | About 5 distinct hues, at most 7 | measured (visual search, applied by analogy) |
| Status colors | Never red against green alone; add a word or symbol | standard (WCAG 1.4.1) |
| Bold in terminals | Bold changes weight only, with bold-as-bright off | convention |

### Font size

* **Why visual angle:** reading speed rises with text size until the x-height reaches about 0.2°, then stays flat up to about 2°.
  The threshold varies by person from 0.15° to 0.3°, and it grows with age, about a third larger by the late sixties.
  Going larger costs screen space, not reading speed.
* **Formula:** point size = tan(target angle) × viewing distance in mm ÷ (x-height in em × mm per point).
* **mm per point:** on macOS, a point is 1 pixel at 1x and 2 pixels at 2x.
  On a 218 ppi 5K display at 2x, 1 point is 25.4 ÷ 109 = 0.233 mm.
* **Distance:** ask the user, and use the far end of their range.
* **x-height:** read it from the font file with fontTools as `OS/2.sxHeight ÷ head.unitsPerEm`.
  A font with a smaller x-height needs a larger point size: multiply by the ratio of the 2 x-heights.
* **Fonts measured so far:** JetBrains Mono 0.550, Menlo 0.547, Monaco 0.545, Fira Code 0.540, SF Mono 0.526, Iosevka 0.520, Cascadia Code 0.518, IBM Plex Mono 0.516, and Atkinson Hyperlegible Mono and Next 0.496.
* **Self-test:** when the user doubts a size, have them time the same passage at 3 sizes.
  Keep the smallest size that is not slower.

### Font choice

* **Serif or sans:** no measured difference.
  Choose by x-height and letter shapes.
* **Dyslexia fonts:** a meta-analysis of 15 studies found no reliable effect.
  Do not recommend them for legibility.
* **Dyslexia and spacing:** extra letter spacing helped children with dyslexia only when word spacing was raised with it.
  It does not help typical adult readers.
* **Proportional or monospace for prose:** proportional fonts read up to about 5% faster in 1 paper study, with a null eye-tracking result.
  Monospace read better below the critical size and for readers with low vision.
  Use a proportional font for prose in note apps and Markdown previews, and monospace for code and terminals.
* **Ligatures:** no study either way.
  Leave them as the user has them, and turn them off for screenshots and screen sharing.
* **Programming fonts:** no study ranks them.
  Fira Code and JetBrains Mono both meet the criteria.
* **Font smoothing:** macOS `AppleFontSmoothing` only thickens strokes on Retina displays.
  It is a taste setting with no study.

### Line length

* **Prose:** 55 characters per line gave the best comprehension on screen, and readers rated it easiest.
  100 characters read fastest, partly from less scrolling.
* **Code:** no study exists.
* **Measure width in real text:** a font's average glyph width is wider than its average on running English, because prose is mostly narrow lowercase letters.
  Measure on the user's own notes with fontTools: sum the `hmtx` advances, then divide by the character count and by `unitsPerEm`.
  Atkinson Hyperlegible Next averages 0.436 em per character on the user's notes, against 0.544 em over its glyphs.
* **Width formula:** width in em = characters per line × average advance in em.

### Light or dark

* **Mechanism:** a brighter screen shrinks the pupil (2.1 mm against 3.7 mm), which sharpens small letters.
  When both modes are made equally bright overall, the difference disappears.
* **When it matters most:** small text and dark rooms.
  In a near-dark room, dark mode took 122 ms to read a glanced word, against 84 ms for light mode.
  At daylight levels, the difference was not significant.
* **Dark mode:** no controlled study shows less eye strain on a desktop display, and none compares the modes for sleep.
  If the user keeps dark mode, light the room, enlarge the text, and use dark grey rather than pure black.
* **Tinted backgrounds and colored overlays:** systematic reviews find no reliable benefit.

### Contrast and color

* **WCAG 2 thresholds:** 4.5:1 for any text, and 7:1 for enhanced contrast.
  Maximum contrast is not needed, because reading speed barely changes across a wide contrast range.
* **APCA:** a proposed replacement for the WCAG 2 ratio, not yet adopted, that scores lightness contrast as Lc from 0 to about 106.
  Its sign shows polarity, so compare absolute values.
  Aim for an absolute Lc of 75 or more for body text and 90 for small text.
  Use it as a second check on dark themes, where WCAG 2 overstates contrast.
* **Fix a failing color:** move its lightness away from the background, keeping hue and saturation, until it reaches 4.6:1.
  `scripts/contrast.py --fix FG BG` does this, and exits with an error when the target cannot be reached.
* **Exempt background-like colors:** ANSI black in a dark theme, and ANSI white and bright white in a light theme, are meant to match the background.
  Leave them, and let the terminal's minimum-contrast setting catch text drawn in them.
* **Syntax highlighting:** it gives at most a small speed gain, for less experienced readers.
  A theme that colors only strings, constants, comments, and top-level definitions fits the 5-hue target.

### Emphasis in the UI

* **Bold:** no reading-speed cost.
* **Italics:** 3 to 5% slower, so keep them to short spans.
* **All capitals:** 12 to 14% slower in running text.

## Procedure for any app

1. **Read the current settings.**
   Find the settings file or store, and note the font, size, line height, wrap width, theme, and colors.
2. **Back up** every file you will touch.
3. **Learn how the app saves.**
   An app that holds settings in memory overwrites edits made while it runs.
   Use its API (iTerm2), edit while it is quit (Obsidian), or edit a file it watches (VS Code `settings.json`).
4. **Check font names.**
   Read family names from the font files with fontTools, and confirm the configured family is installed.
   A missing font falls back silently.
5. **Check font lists.**
   In a CSS font list, the first installed font draws every glyph it has.
   A second font only fills glyphs the first lacks.
6. **Set the size** from the formula and the user's distance.
7. **Set line height and width.**
   Find out what the app's units mean before using them (see the mistakes below).
8. **Check every text color's contrast** against the actual background, in both light and dark variants.
   Fix failures by lightness.
9. **Hunt fixed colors.**
   Programs that print fixed 256-color or hex colors ignore the terminal palette and break when the mode changes.
   Shell prompts, status lines, and CLI themes are the usual cases.
   Switch them to ANSI colors 0 to 15, or to an ANSI theme, so they follow the palette.
10. **Verify.**
    Read stored values back, then ask for a screenshot.
    Measure characters per line, line pitch, and colors in it.

## Values applied on 2026-10-02

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
  It was Minimal (value 5).
* **Minimum Contrast:** 0.34 dark, 0.54 light.
  Each sits just below the weakest palette color's brightness difference from the background (0.353 and 0.548).
  So the setting leaves the palette alone and lifts only dimmer colors that programs send directly.
* **Light colors:** background `#FAFAFA`, foreground and bold `#101010`, link `#1271D4`.
  ANSI 0 to 15: `#14191E`, `#B43C2A`, `#008500`, `#757400`, `#2744C7`, `#B73CB5`, `#007E80`, `#C7C7C7`, `#686868`, `#CE3D38`, `#13823E`, `#797400`, `#5961E7`, `#BE2CBE`, `#007D7F`, `#FFFFFF`.
* **Dark colors:** background `#15191F`, foreground `#DCDCDC`, bold `#FFFFFF`, link `#328EEE`.
  ANSI 0 to 15: `#14191E`, `#D55D4B`, `#00C200`, `#C7C400`, `#667CE1`, `#C755C5`, `#00C5C7`, `#C7C7C7`, `#838383`, `#DD7975`, `#58E790`, `#ECE100`, `#A7ABF2`, `#E17EE1`, `#60FDFF`, `#FFFFFF`.
  ANSI 1, 4, 5, and 8 were fixed. The rest were already at 4.5:1 or more.
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
* **Dark theme not checked:** Catppuccin Mocha's main text is 11.3:1, but Overlay0 is 3.4:1, and Subtext0, Overlay2, and the accent colors fall below APCA Lc 60.
  Check and fix it, and give its terminal a dark palette, before using dark mode.
* **Alabaster fixes** under `editor.tokenColorCustomizations["[Alabaster]"]`: strings `#3D7E23` (was 3.9:1), and punctuation and escapes `#6F6F6F` (was 4.2:1).
* **Alabaster fixes** under `workbench.colorCustomizations["[Alabaster]"]`: `editorLineNumber.foreground` `#6B7268` (was 2.4:1).
  The terminal background, foreground, and 16 ANSI colors are set to the iTerm2 light colors above.
* **Light Modern fix**, kept in case of a switch back: under `editor.tokenColorCustomizations["[Light Modern]"]`, the regex group scopes are `#811F3F` instead of `#D16969` (3.5:1).
* **Light theme candidates:** Catppuccin Latte failed, with 14 syntax colors below 4.5:1.
  Light Modern had 1 failure, and Alabaster had 3 plus its line numbers.
* **Preview line length:** a local extension, `dave.markdown-readable-width`, with its source in `~/projects/vscode-markdown-readable/`.
  It contributes `markdown.previewStyles` with `body { max-width: 28.5em; margin: 0 auto; }`, about 65 characters.
  Tables get `width: max-content; min-width: 100%; max-width: calc(100vw - 52px); margin-left: 50%; transform: translateX(-50%);`.
  Without that rule, a table wider than the text column runs off to the right and looks off-center.
  Rebuild it with `npx @vscode/vsce package --allow-missing-repository --skip-license`.
  Install it with `code --install-extension <file>.vsix --force`.

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

The user chose to skip Neovim on 2026-10-02.
Neovim runs inside iTerm2, so the font, size, and line height already apply.

* **Mid-word wrapping:** `~/.config/nvim/init.lua` (kickstart.nvim) sets `breakindent` but not `linebreak`, so wrapped lines break mid-word.
  Add `vim.o.linebreak = true`.
* **Colors:** the colorscheme is `tokyonight-night`, a dark truecolor scheme.
  It paints its own background, so it ignores the iTerm2 light palette and Minimum Contrast's fixes.
  Choose a light scheme that passes the contrast check, or one that uses the terminal palette.
* **Rendered Markdown:** render-markdown.nvim renders headings, tables, and callouts in place.
  The lazy.nvim spec is `{ 'MeanderingProgrammer/render-markdown.nvim', dependencies = { 'nvim-treesitter/nvim-treesitter', 'nvim-mini/mini.icons' }, opts = {} }`.
  Set `pipe_table.wrap = true` so wide tables fit the window.

## Mistakes to avoid

* **Obsidian's rem is the base font size:** Minimal's line width is in rem, and Obsidian sets the rem to `baseFontSize`, not 16 px.
  49 rem at 22 px gave 108 characters per line.
* **Glyph-average width overstates prose width:** using 0.544 em instead of the measured 0.436 em set both the Obsidian and VS Code widths too wide.
* **Minimal needs Obsidian's readable line length:** with `readableLineLength` off, Minimal applies no width at all.
* **VS Code `markdown.styles` loads only from the workspace:** a stylesheet path outside the open folder fails to load.
  Use an extension with `markdown.previewStyles`.
* **Running apps overwrite config:** iTerm2 and Obsidian rewrite their settings from memory.
  Do not edit their files while they run.
* **iTerm2 Minimum Contrast is not WCAG:** it compares brightness as 0.30 R + 0.59 G + 0.11 B, on 0 to 1 values.
  It pushes text toward black or white until the difference reaches the setting.
  Fix the palette by WCAG first, then set Minimum Contrast as a backup.
* **iTerm2 Python API enum bug:** `async_set_thin_strokes` cannot serialize its own enum.
  Pass `iterm2.ThinStrokes.<NAME>.value`.
* **Colors that look muddy in light mode** are fixed colors made for a dark background, darkened by Minimum Contrast.
  Switch the program to palette colors or to its light theme.
* **Light variants of dark themes often fail contrast:** check before switching.
  Prefer a light theme built for contrast, or fix it with color overrides.
* **Built-in views ignore the readable width:** Obsidian's release notes ran 108 characters.
  Check line length on one of the user's own notes.

## Other apps

For an app not covered above, run the procedure and look for these settings by name:

* **Font family, size, and weight.**
* **Line height:** called line spacing, leading, or vertical spacing.
  Find out whether it multiplies the font size or the font's own line height.
* **Readable width:** called max width, readable line length, text width, or column.
* **Theme and appearance:** whether the app follows the system or can be forced light.
* **Minimum contrast:** iTerm2, VS Code's terminal, and Windows Terminal (`adjustIndistinguishableColors`) have one.
* **Bold rendering:** bold as bright color, and synthetic bold.
* **Fixed colors in config:** hex or 256-color codes in the app's own theme files.
