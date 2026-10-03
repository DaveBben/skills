# Readability on screens: research brief (2026-10-02)

This brief combines four research files in this folder.
Each claim below has its source in the file named in brackets.

* `01-typography.md`: font, size, line length, line, letter and paragraph spacing, weight.
* `02-color-contrast-emphasis.md`: light and dark mode, background, contrast, number of colors, bold, italic and capitals.
* `03-writing.md`: how people read on screens, sentences, words, punctuation, document structure, AI-text habits.
* `04-markdown-and-tools.md`: exact settings in iTerm2, VS Code, Neovim, Obsidian and Claude Code, and how Markdown renders.

Evidence labels: **measured** means a controlled study with numbers.
**Standard** means WCAG or an official style guide.
**Convention** means designer or vendor practice with no study behind it.

## 1. The answers in one place

| Question | Answer | Evidence |
|---|---|---|
| Font | Any well-made font with a large x-height (0.52 em or more), a marked zero and distinct `I l 1`. Serif or sans makes no difference. Dyslexia fonts do not help. | measured |
| Font size | Size by visual angle: lowercase x-height of at least 0.2°, better 0.25°, at your viewing distance. See the table in section 2. | measured |
| Background | Dark text on a light background reads better for small text and in dim rooms. In dark mode, light the room and enlarge the text. Tinted backgrounds show no benefit. | measured |
| Line length | 55 to 75 characters for prose, 80 to 100 for code. | measured (prose), convention (code) |
| Line spacing | 1.4 to 1.5 for prose, 1.3 to 1.5 for code, the same in every tool. | measured and standard (prose), convention (code) |
| Letter and word spacing | Leave at the font default. Extra spacing helps only readers with dyslexia. | measured |
| Paragraph spacing | A blank line (space, no indent), 0.75 to 1.5 times the font size. | convention |
| Number of colors | About 5 distinct hues, at most 7. Highlighting gives experienced programmers no measured comprehension gain. | measured (visual search, by analogy) |
| Bold and italic | Bold costs no reading speed; italics are 3 to 5% slower; all capitals are 12 to 14% slower. Bold works only when it is rare. | measured |
| Sentences and words | Answer first, one idea per sentence, verb next to its subject, positive statements, common words, one name per thing. | measured and standard |
| Punctuation | Serial comma, a comma after an introductory clause, few semicolons, dashes and parentheses, no exclamation marks. | standard; comma measured |

## 2. Font size for your display

Your display is a 27-inch 5K at 2x scaling.
One macOS point there is 0.233 mm, two-thirds of a print point, so "18 pt" on screen is smaller than 18 pt on paper.
Reading speed holds steady from an x-height of about 0.2° up to 2°, so going larger costs screen space but not speed.

Point size that gives a 0.25° x-height, by viewing distance (computed from the font files and display geometry):

| Distance (eye to screen) | Fira Code | Atkinson Hyperlegible Next or Mono |
|---|---|---|
| 50 cm | 17 pt | 19 pt |
| 60 cm | 21 pt | 23 pt |
| 70 cm | 24 pt | 26 pt |
| 80 cm | 28 pt | 30 pt |

Today VS Code and Obsidian use 16 and iTerm2 uses 18.
At 60 cm, 16 pt Fira Code is 0.19°, just below the point where reading slows.

The size a reader needs grows with age, about a third larger by the late sixties (measured, 645 readers).
People also differ: the critical size ranges from 0.15° to 0.3°.
To find yours, time yourself reading the same passage at three sizes and keep the smallest that is not slower.

## 3. Light or dark mode

Every lab study found dark text on a light background gave better proofreading and acuity.
The cause is screen brightness: a brighter screen shrinks the pupil (2.1 mm against 3.7 mm), which sharpens the image of small letters.
When both modes were made equally bright overall, the difference disappeared.

The gap grows as text gets smaller and the room gets darker.
In a near-dark room, a glance-length word took 122 ms to read in dark mode and 84 ms in light mode.
At daylight levels the difference was not significant.

No controlled study shows dark mode reduces eye strain on a desktop display, and none compares the two modes for sleep.
The claim that dark mode is worse with astigmatism is untested.

If you stay in dark mode, the measured mitigations are a lit room and larger text.
Use dark grey rather than pure black (convention); Catppuccin Mocha's #1E1E2E already does.

## 4. Changes for your tools

Values marked "your size" come from the table in section 2 once you have measured your distance.

### Things that are wrong today

* **VS Code terminal font is missing:** `terminal.integrated.fontFamily` is `"MesloLGS NF"`, which is not installed, so VS Code falls back to another font.
  Set it to `"FiraCode Nerd Font Mono"`.
* **Obsidian shows prose in Fira Code:** the text font is `FiraCode Nerd Font,Atkinson Hyperlegible Next`, and the second font only draws characters the first lacks.
  Put Atkinson Hyperlegible Next first if you want it.
* **iTerm2 grey text fails contrast:** ANSI color 8 (#686868) on your background (#15191F) is 3.2:1, below the 4.5:1 minimum, and Minimum Contrast is 0.
  Lighten color 8 to at least 4.5:1, or raise Minimum Contrast until grey text is readable.
* **Neovim breaks wrapped lines mid-word:** `linebreak` is off.
  Add `vim.o.linebreak = true` to `init.lua`.
* **VS Code Markdown preview has no line-length cap:** lines run the full pane width, well over 100 characters.
  Load a CSS file through `markdown.styles` containing `body { max-width: 70ch; margin: 0 auto; }`.

### Size, spacing and weight

| Tool | Setting | Suggested value |
|---|---|---|
| iTerm2 | Font size | your size |
| iTerm2 | Vertical Spacing | about 1.15, which gives a line height near 1.4 (mapping unverified; check by eye) |
| iTerm2 | Brighten bold text | off, so bold changes weight and color keeps one meaning |
| iTerm2 | Thin strokes | on for dark backgrounds |
| VS Code | `editor.fontSize`, `terminal.integrated.fontSize` | your size |
| VS Code | `editor.lineHeight` | leave unset (1.5 on macOS) |
| VS Code | `terminal.integrated.lineHeight` | 1.15, to match iTerm2 |
| VS Code | `"[markdown]"`: `editor.wordWrap` and `editor.wordWrapColumn` | `"bounded"` and 80 |
| VS Code | `markdown.preview.fontFamily` and `markdown.preview.fontSize` | `"Atkinson Hyperlegible Next"` and your size |
| Obsidian | Font size | your size |
| Obsidian | Minimal line width | widen with the font so lines stay near 65 characters |
| Claude Code | `maxProseWidth` | keep 80 |

Use the Regular or Retina weight of Fira Code, never Light (measured: thin weights slowed search).
Ligatures have no study either way; turn them off for screenshots and screen sharing.

### Colors

Keep syntax themes to about 5 distinct hues.
A minimal theme colors strings, constants, comments and top-level definitions and leaves keywords plain (convention, Prokopov's Alabaster).
Never let red against green be the only signal; pair status colors with a word or symbol (WCAG 1.4.1, about 1 in 12 men cannot tell them apart).
Catppuccin Mocha's main text meets the stricter WCAG 7:1 level.
Its Subtext0, Overlay and accent colors fall below the APCA minimum for body text, so avoid them for text you read at length.

## 5. Writing Markdown that is easy to read

People scan before they read: 79% of test users scanned and 16% read word by word.
On average they read about 20% of a page's words, and each extra 100 words gets about 18% of those words read.
Rewriting a site to be concise, scannable and objective raised measured usability by 124%.

### Structure

* **Answer first:** put the conclusion, decision or blocker in the first sentence.
* **Front-load:** readers see about the first 2 words of each heading, list item and link, so put the information-carrying words there.
* **Descriptive headings:** each heading names what its section covers. Use one `#`, then `##` and `###`; three levels at most, none skipped, none empty.
* **Lists for parallel items:** numbered for steps, bulleted for independent items. Use a paragraph when one point depends on another, because a list item has no room for "because" or "so".
* **Tables for two dimensions only:** three or four short columns. Claude Code tables ignore `maxProseWidth` and stack into `Header: value` lines when the terminal is too narrow.
* **Paragraphs:** one topic, about five sentences at most.
* **Numbers as numerals:** "3 files", not "three files".
* **Link text names the destination:** never "click here".

### Sentences and words

* **One idea per sentence:** split a sentence that makes two claims, and keep the "because", "so" or "unless" when you split.
* **Verb next to its subject:** clauses placed between subject and verb hurt recall more than jargon or passive voice did (measured, 184 readers).
* **Length:** aim for an average of 15 to 20 words and split sentences over 25. These limits come from style guides; no study sets the number.
* **State things positively:** each negation added about 685 ms in a sentence-checking task. Remove double negatives and exceptions to exceptions.
* **Common words:** "use", "help", "is" over "utilize", "assist", "serves as". Judges and lawyers preferred the plain version 80 to 86% of the time.
* **One name per thing:** a new word makes the reader wonder whether it is a new thing.
* **Concrete nouns:** name the file, command, number or error message.
* **Active voice:** name who does the action. The measured benefit is mixed, so do not contort a sentence for it.
* **Readability scores are not targets:** only about half of 36 studies that raised scores raised comprehension.

### Punctuation and emphasis

* **Serial comma:** "A, B, and C" (Google, Microsoft, Chicago).
* **Comma after an introductory clause:** it raised correct parses from 47% to 81% in one study.
* **Few semicolons:** split into two sentences instead (Google, Microsoft, GOV.UK).
* **Few em dashes:** a comma, colon or new sentence first (Microsoft, Chicago).
* **Nothing important in parentheses:** some readers skip them (Google).
* **No exclamation marks or scare quotes:** use code font for literal strings.
* **Bold rarely:** a term at its definition, a run-in heading, a rare key sentence. Never for tone.
* **Italics rarely, all capitals never:** for running text.

### Markdown source

* **One sentence per line (semantic line breaks):** a one-sentence edit becomes a one-line diff, and rendered output does not change.
  The breaks do show in GitHub comments, in Obsidian with "Strict line breaks" off, and in VS Code with `markdown.preview.breaks` on.
* **Tag every code fence with a language:** untagged blocks get no highlighting.
* **Blank lines around headings, lists, tables and code blocks:** some parsers need them.
* **Two list levels at most.**
* **Callouts:** use only GitHub's five types (`NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`), unnested, when a file must render everywhere. The VS Code preview shows them as plain blockquotes.
* **No Nerd Font icons or emoji in shared files or tables:** they show as boxes elsewhere and shift table borders.
* **Lint:** markdownlint rules MD001, MD013, MD022, MD031, MD032, MD040 and MD059 cover most of the above.

### Habits that make AI-written text tiring

Each of these costs the reader something specific (measured or documented in `03-writing.md`, section 7).

* **"Not X, but Y":** makes the reader process a negation of a view they never held. A one-line instruction cut it by 50 to 75%.
* **Bold on every key phrase:** removes the signal bold is supposed to give.
* **Bold-label-colon lists for content that is not a list of terms:** drops the reasoning between points.
* **Groups of three, puffery ("pivotal", "evolving landscape"), "serves as" for "is":** fill reading time with no facts.
* **Padding:** length is rewarded in model training whether or not it helps the reader.
* **Small tables that would read better as a sentence, and headings with nothing under them.**

## 6. Where the research conflicts with your writing rules

Your writing rules (`plugins/SDLC/hooks/writing.md`) ask documents to format lists as `* **Lead:** condition and outcome.`.
Microsoft's style guide accepts that form for term lists.
The research counts it as tiring when every list in a document uses it: bold stops signalling, and Wikipedia's "Signs of AI writing" lists it.
This brief follows your rule in its lists so you can judge the effect.
A narrower rule would keep the bold lead for lists of terms or rules and use plain bullets elsewhere.

The rest of your writing rules match the research: answer first, one thought per sentence, plain words, verbs over nominalizations, no "X, not Y" frames, one name per thing.

## 7. What is not established

* **Code-specific studies:** no controlled study was found on line length, line spacing, letter spacing or ligatures for reading code. Those values are convention.
* **Astigmatism and dark mode:** untested.
* **Dark mode and sleep:** untested; dark mode lowers screen light, which plausibly helps, but that is inference.
* **iTerm2 vertical spacing:** whether 1.15 gives a 1.4 line height is unverified.
* **Unverified sources:** claims marked **[unverified]** in the four files came from search snippets, not fetched pages. They include Lorch 1995 on heavy underlining, Haviland and Clark on given-new order, and Sadoski on concrete words.
