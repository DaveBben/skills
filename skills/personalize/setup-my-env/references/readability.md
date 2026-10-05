# Making apps readable

Contents: targets, font size, font choice, line length, light or dark, contrast and color, emphasis, procedure, mistakes.

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
* **Proportional or monospace for prose:** use a proportional font for prose in note apps and Markdown previews, and monospace for code and terminals.
* **Ligatures:** no study either way.
  Leave them as the user has them, and turn them off for screenshots and screen sharing.
* **Programming fonts:** no study ranks them.
  Fira Code and JetBrains Mono both meet the criteria.
* **Font smoothing:** macOS `AppleFontSmoothing` only thickens strokes on Retina displays.
  It is a taste setting with no study.

### Line length

* **Code:** no study exists.
* **Measure width in real text:** a font's average glyph width is wider than its average on running English, because prose is mostly narrow lowercase letters.
  Measure on the user's own notes with fontTools: sum the `hmtx` advances, then divide by the character count and by `unitsPerEm`.
  Atkinson Hyperlegible Next averages 0.436 em per character on the user's notes, against 0.544 em over its glyphs.
* **Width formula:** width in em = characters per line × average advance in em.

### Light or dark

* **Dark mode:** use dark grey rather than pure black.
  If the user keeps dark mode, light the room and enlarge the text.
* **Tinted backgrounds and colored overlays:** systematic reviews find no reliable benefit.

### Contrast and color

* **Maximum contrast is not needed:** reading speed barely changes across a wide contrast range.
* **Fix a failing color:** move its lightness away from the background, keeping hue and saturation, until it reaches 4.6:1.
  `scripts/contrast.py --fix FG BG` does this, and exits with an error when the target cannot be reached.
* **Exempt background-like colors:** ANSI black in a dark theme, and ANSI white and bright white in a light theme, are meant to match the background.
  Leave them, and let the terminal's minimum-contrast setting catch text drawn in them.
* **Syntax highlighting:** it gives at most a small speed gain, for less experienced readers.
  A theme that colors only strings, constants, comments, and top-level definitions fits the 5-hue target.

### Emphasis in the UI

Keep italics to short spans, and avoid all capitals in running text.

## Procedure for any app

* **Check font names:** a missing font family falls back silently, so check the family exists in the font files.
* **Set line height and width** only after you know what the app's units mean (see the mistakes below).
* **Fixed colors:** programs that print fixed 256-color or hex colors ignore the palette and break when the mode changes.
  Shell prompts, status lines, and CLI themes are the usual cases.
  Switch them to ANSI colors 0 to 15, or to an ANSI theme, so they follow the palette.

## Mistakes to avoid

* **Obsidian's rem is the base font size:** Minimal's line width is in rem, and Obsidian sets the rem to `baseFontSize`, not 16 px.
  49 rem at 22 px gave 108 characters per line.
* **Glyph-average width overstates prose width:** using 0.544 em instead of the measured 0.436 em set both the Obsidian and VS Code widths too wide.
* **Minimal needs Obsidian's readable line length:** with `readableLineLength` off, Minimal applies no width at all.
* **VS Code `markdown.styles` loads only from the workspace:** a stylesheet path outside the open folder fails to load.
  Use an extension with `markdown.previewStyles`.
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

Other apps: look for line height as line spacing, leading or vertical spacing; readable width as max width, text width or column; and a minimum-contrast setting.
