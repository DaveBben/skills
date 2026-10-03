# Typography for reading on screen

Scope: terminal output, code and Markdown read on a 27-inch 5K Studio Display (5120 x 2880, 218 ppi, macOS at 2x, 2560 x 1440 points) in iTerm2, VS Code, Neovim and Obsidian.

Evidence labels:
* **measured:** a controlled study, with numbers, and whether it ran on paper or screen.
* **standard:** WCAG or a similar document, with what it was based on.
* **convention:** designer consensus or vendor documentation with no study behind it.
* **[unverified]:** the claim comes from a search snippet or memory, not from a page that was fetched.

Local measurements in this file (x-height, character width, built-in line height, ligature features) were taken from the font files with fontTools on 2026-10-02.
The files came from the system fonts, `~/Library/Fonts`, and these downloads: [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf), [IBM Plex Mono](https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf), [Atkinson Hyperlegible Mono](https://github.com/google/fonts/tree/main/ofl/atkinsonhyperlegiblemono), [Cascadia Code](https://github.com/google/fonts/tree/main/ofl/cascadiacode), [Iosevka (Fontsource build)](https://cdn.jsdelivr.net/fontsource/fonts/iosevka@latest/latin-400-normal.ttf).

## Current setup (read from the machine)

* **iTerm2:** The main profile uses FiraCode Nerd Font Mono at 18 pt, with ligatures on and vertical spacing 1.0.
* **iTerm2 line height:** Vertical spacing 1.0 uses the font's own line height, which is 1.23 em for Fira Code (measured from the font file).
* **VS Code:** The editor uses Fira Code at 16, with ligatures on and no `editor.lineHeight` set.
* **VS Code line height:** With `editor.lineHeight` unset, VS Code on macOS uses 1.5 x font size, so 24 points ([fontInfo.ts](https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/editor/common/config/fontInfo.ts)).
* **VS Code terminal:** The integrated terminal uses MesloLGS NF at 16.
* **Obsidian:** The Minimal theme sets body text in FiraCode Nerd Font (monospace) at 16 px, line height 1.5, line width 40 rem and paragraph spacing 1.75 rem.
* **Obsidian line length:** 40 rem is 640 px, which holds about 65 Fira Code characters at 16 px (Fira Code advance width is 0.615 em).
* **Font smoothing:** `AppleFontSmoothing` is not set, so macOS uses its default.
* **Neovim:** Neovim runs inside iTerm2, so iTerm2's font, size and line spacing apply.

## 1. Font choice

### Serif or sans-serif

* **Serifs alone do not change legibility:** Arditi and Cho built fonts that differed only in serif size (0%, 5%, 10% of cap height) and found no effect of serifs on RSVP or continuous reading speed (measured, lab study) ([Arditi & Cho 2005](https://europepmc.org/abstract/MED/16099015)).
* **Serif spacing effect:** In that study, 5% serifs were slightly more legible at threshold sizes, and the authors attribute the gain to the extra letter spacing that serifs add ([Arditi & Cho 2005](https://europepmc.org/abstract/MED/16099015)).
* **High-ppi screens:** Nielsen Norman Group says screens at 220 ppi or more render serifs well enough that either style is fine for body text (convention, reasoning only; the article cites no study) ([NN/g](https://www.nngroup.com/articles/serif-vs-sans-serif-fonts-hd-screens/)).
* **Low-ppi screens:** The older advice to use sans-serif on screen came from screens that could not render serifs at small sizes (convention) ([NN/g](https://www.nngroup.com/articles/serif-vs-sans-serif-fonts-hd-screens/)).
* **x-height matters more than serifs:** Legge and Bigelow report a screen study in which Verdana (x-height 0.55 of the body size) was the most legible and Times New Roman (0.45) the least at the same point size ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Apply:** Choose by x-height and letter shapes, not by serif or sans-serif, on a 218 ppi display.

### What makes characters easy to tell apart

* **x-height:** A larger x-height makes lowercase text read as larger at the same point size, because the visual angle that predicts reading speed is measured on the x-height (measured) ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Letter spacing:** At small sizes, letter spacing limits reading more than letter size, because neighbouring letters interfere with each other (crowding) (measured, screen RSVP) ([Pelli et al. 2007](https://europepmc.org/abstract/MED/18217835)).
* **Distinct confusable pairs:** The Braille Institute designed Atkinson Hyperlegible to separate B/8, O/0, 1/I/i/l, E/F, p/q, e/b/g/s and g/m/n/r for low-vision readers (convention; the fetched pages describe no formal test) ([Braille Institute](https://www.brailleinstitute.org/freefont/)).
* **Atkinson design detail:** The designer says the font puts a tail on lowercase l and a hook on the numeral 1 so the two differ **[unverified]** ([Dezeen](https://www.dezeen.com/2020/09/11/atkinson-hyperlegible-typeface-applied-design-works/)).
* **rn versus m:** A monospace font puts r and n in two fixed cells, so "rn" cannot close up into "m" (observed in the rendered sample below).
* **Bigelow review:** A 2019 Vision Research review covers typeface-feature legibility research but its abstract gives no ranked list of features ([Bigelow 2019](https://europepmc.org/abstract/MED/31078662)).

### Monospace fonts compared

The table below was measured from the font files.
"x-height" and "width" are fractions of the em; "built-in line height" is the font's ascender + descender + line gap, which a terminal uses at vertical spacing 1.0.
"Zero" and the I/l/1 check come from rendering each font at 80 px and looking at the result.

| Font | x-height | Width | Built-in line height | Zero | I l 1 distinct | Ligatures (`calt`) |
|---|---|---|---|---|---|---|
| JetBrains Mono | 0.550 | 0.600 | 1.32 | dotted | yes | yes |
| Menlo | 0.547 | 0.602 | 1.16 | slashed | yes | no |
| Monaco | 0.545 | 0.600 | 1.33 | slashed | yes | no |
| Fira Code | 0.540 | 0.615 | 1.23 | slashed | yes | yes |
| SF Mono | 0.526 | 0.618 | 1.18 | slashed | yes | no |
| Iosevka (default build) | 0.520 | 0.500 | 1.25 | slashed | yes | yes |
| Cascadia Code | 0.518 | 0.586 | 1.16 | dotted | yes | yes (Cascadia Mono has none) |
| IBM Plex Mono | 0.516 | 0.600 | 1.30 | dotted | yes | no |
| Atkinson Hyperlegible Mono | 0.496 | 0.632 | 1.30 | reverse-slashed | yes | no |
| Berkeley Mono | not measured (commercial) | | | slashed and other styles **[unverified]** | **[unverified]** | yes **[unverified]** |

* **All nine measured fonts separate 0/O and I/l/1:** None of the nine rendered fonts drew two of these characters the same.
* **Atkinson Hyperlegible Mono runs small:** Its x-height is 0.496 against Fira Code's 0.540, so at the same point size its lowercase is 8% shorter.
* **Matching Atkinson to Fira Code:** Atkinson Hyperlegible Mono at 19.6 pt has the same x-height as Fira Code at 18 pt.
* **Atkinson Hyperlegible Next is the same height:** The proportional Next family also has an x-height of 0.496.
* **Atkinson Hyperlegible Mono purpose:** The Braille Institute describes it as "specifically designed to assist coders" where character spacing matters (convention) ([Braille Institute news](https://www.brailleinstitute.org/about-us/news/braille-institute-launches-enhanced-atkinson-hyperlegible-font-to-make-reading-easier/)).
* **JetBrains Mono design claims:** JetBrains says it maximises lowercase height at standard width, dots the zero, separates 1/l/I and gives the comma a different shape from the period (convention) ([JetBrains Mono](https://www.jetbrains.com/lp/mono/)).
* **Iosevka width:** Iosevka is the narrowest at 0.500 em, so it fits 23% more characters per line than Fira Code at the same size, with narrower letters.
* **Iosevka variants:** Iosevka lets you pick each character's shape (zero, l, i and others) through OpenType variants (convention) ([Iosevka](https://github.com/be5invis/Iosevka)).
* **Cascadia variants:** Cascadia Code has ligatures and Cascadia Mono is the same font without them ([Cascadia Code](https://github.com/microsoft/cascadia-code)).
* **No controlled study ranks these fonts:** No study was found that compares reading speed or error rate across programming fonts.
* **Apply:** Choose a font with x-height of at least 0.52, a marked zero and distinct I/l/1, then set the size by x-height (section 2), not by point size.

### Monospace versus proportional for reading

* **Normal readers, paper charts:** Maximum reading speed was 5% faster with Times than with Courier in 50 normally sighted readers (measured, printed MNREAD charts) ([Mansfield, Legge & Bane 1996](https://legge.psych.umn.edu/sites/legge.psych.umn.edu/files/files/media/mansfield96_psychophysics_of_reading_xv-_font_effects_in_normal_and_low_vision.pdf)).
* **Small print favours monospace:** In the same study, Courier gave better reading acuity (0.05 logMAR) and a smaller critical print size (0.06 logMAR), and below the critical print size Times was read up to 50% slower than Courier (measured, paper) ([Mansfield et al. 1996](https://legge.psych.umn.edu/sites/legge.psych.umn.edu/files/files/media/mansfield96_psychophysics_of_reading_xv-_font_effects_in_normal_and_low_vision.pdf)).
* **Low vision favours monospace:** Readers with low vision read 10% faster with Courier than with Times (measured, paper, 42 readers) ([Mansfield et al. 1996](https://legge.psych.umn.edu/sites/legge.psych.umn.edu/files/files/media/mansfield96_psychophysics_of_reading_xv-_font_effects_in_normal_and_low_vision.pdf)).
* **Eye tracking, sentences:** In 32 readers, monospacing raised the number of fixations and shortened each fixation, and total reading time did not change (measured, eye tracking) ([Jarosch et al.](https://zenodo.org/records/18912221)).
* **Dyslexia:** In 48 Spanish readers with dyslexia, Courier gave the shortest fixation durations of 12 fonts, but monospace had no significant effect on reading time (29.6 s vs 31.5 s, p = 0.159) (measured, screen, 14 pt) ([Rello & Baeza-Yates 2013](https://www.changedyslexia.org/publications/pdfs/2013-ASSETS-Good%20Fonts%20for%20Dyslexia.pdf)).
* **No study of code:** No controlled study was found that compares monospace and proportional fonts for reading code.
* **Apply:** Keep monospace for code and terminals, where alignment carries meaning.
* **Apply to Obsidian prose:** Setting prose in a proportional font such as Atkinson Hyperlegible Next may gain up to about 5% maximum speed at comfortable sizes, and the evidence is one paper study and one null result.

### Dyslexia fonts

* **Meta-analysis:** Across 15 studies (91 effect sizes, 688 readers), dyslexia fonts such as OpenDyslexic and Dyslexie had no reliable effect on reading speed or accuracy, g = -0.04, 95% CI [-0.15, 0.07] (measured) ([Azzarello et al. 2026](https://europepmc.org/abstract/MED/42536336)).
* **Dyslexie:** 170 children with dyslexia read Dyslexie no faster or more accurately than Arial, and most preferred Arial (measured) ([Kuster et al. 2018](https://europepmc.org/abstract/MED/29204931)).
* **Dyslexie gain was spacing:** When Times New Roman was given the same extra spacing, Dyslexie and spaced Times did not differ (measured) ([Duranovic et al. 2018](https://europepmc.org/abstract/MED/30094714)).
* **OpenDyslexic:** In 12 children with dyslexia, OpenDyslexic gave no improvement in reading rate or accuracy against Arial and Times New Roman, and no child preferred it (measured, paper) ([Wery & Diliberto 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5629233/)).
* **OpenDyslexic on screen:** OpenDyslexic did not lead to faster reading in 48 readers with dyslexia (measured, screen) ([Rello & Baeza-Yates 2013](https://www.changedyslexia.org/publications/pdfs/2013-ASSETS-Good%20Fonts%20for%20Dyslexia.pdf)).
* **Apply:** Do not switch to a dyslexia font for legibility.

### Programming ligatures

* **No controlled study found:** No study was found that measures reading speed or error rate with and without programming ligatures.
* **Case for:** Fira Code says ligatures save the eye from joining `->`, `<=` or `:=` into one token, and that the file stays plain ASCII (convention) ([Fira Code](https://github.com/tonsky/FiraCode)).
* **Case against:** Butterick says ligatures can be mistaken for real Unicode symbols such as `≠`, and that substitution ignores context, so it will sometimes be wrong (convention) ([Butterick](https://practicaltypography.com/ligatures-in-programming-fonts-hell-no.html)).
* **Butterick's limit:** Butterick accepts private use and objects to ligatures in code shown to others ([Butterick](https://practicaltypography.com/ligatures-in-programming-fonts-hell-no.html)).
* **Apply:** Treat ligatures as preference.
* **Apply when sharing:** Turn ligatures off for screenshots, screen sharing and debugging character-level problems.

## 2. Font size

### Critical print size

* **Critical print size:** Reading speed rises with print size until a critical print size and then stays at its maximum (measured) ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Value:** The consensus critical print size for normally sighted readers is 0.2° of x-height, with a range of 0.15° to 0.3° by person, font and method (measured) ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Fluent range:** Maximum reading speed holds from about 0.2° to 2°, a tenfold range (measured) ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Printed text sits near the limit:** Running text in newspapers and books subtends about 0.23° to 0.24° at 40 cm, just above the critical print size ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Online news sits at the limit:** Online news body text averaged 0.21° ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Spacing sets the limit:** For fluent readers with good correction and light, reading rate is limited by letter spacing (crowding), not by acuity (measured, screen RSVP) ([Pelli et al. 2007](https://europepmc.org/abstract/MED/18217835)).

### Web text size study

* **Bigger read better:** In 104 readers on Wikipedia pages, mean fixation duration fell as size rose up to 18 pt, and comprehension was lower at 10 and 12 pt (measured, screen, eye tracking) ([Rello, Pielot & Marcos 2016](https://pielot.org/2016/01/optimal-font-size-for-web-pages/)).
* **Recommendation from that study:** The authors recommend 18 pt, which they equate with 24 px on desktop displays ([Rello et al. 2016](https://pielot.org/2016/01/optimal-font-size-for-web-pages/)).
* **Limit of that study:** The blog post does not report viewing distance or display, so the result cannot be converted to visual angle.

### Viewing distance

* **Typical range:** OSHA recommends 50 to 100 cm from eye to screen (standard; OSHA gives no study) ([OSHA](https://www.osha.gov/etools/computer-workstations/components/monitors)).
* **Apply:** Measure your own eye-to-screen distance, because the size you need grows in proportion to it.

### How points map to size on this display

* **Points, not pixels:** macOS lays out in points, and on a Retina display each point is backed by 2 x 2 pixels ([Apple](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Explained/Explained.html)).
* **This display:** The Studio Display is 5120 x 2880 at 218 ppi ([Apple](https://www.apple.com/studio-display/specs/)), and this Mac runs it at 2x, which gives 2560 x 1440 points (read from `NSScreen`).
* **Points per inch:** At 2x, one point is 2 pixels, so the screen shows 109 points per inch and one point is 0.233 mm.
* **Not the print point:** A macOS point on this display (0.233 mm) is smaller than a print point (0.353 mm), so "18 pt" here is about two-thirds the size of 18 pt on paper.
* **VS Code and Obsidian units:** VS Code `editor.fontSize` and Obsidian sizes are CSS pixels, and a CSS pixel equals one macOS point at 2x **[unverified]**.
* **Visual angle:** Legge and Bigelow give angle ≈ 0.05° per print point at 40 cm, and the general rule is that angle scales with size divided by distance ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).

Computed x-height visual angle on this display (x-height fraction x point size x 0.233 mm, then angle at the given distance):

| Font and size | x-height (mm) | At 50 cm | At 60 cm | At 70 cm |
|---|---|---|---|---|
| Fira Code 16 pt | 2.02 | 0.23° | 0.19° | 0.17° |
| Fira Code 18 pt | 2.27 | 0.26° | 0.22° | 0.19° |
| Fira Code 20 pt | 2.52 | 0.29° | 0.24° | 0.21° |
| JetBrains Mono 18 pt | 2.31 | 0.27° | 0.22° | 0.19° |
| Atkinson Hyperlegible Mono or Next 18 pt | 2.08 | 0.24° | 0.20° | 0.17° |

* **Current sizes sit at the limit:** Fira Code at 16 pt in VS Code and Obsidian falls below 0.2° beyond about 58 cm.
* **iTerm2 at 18 pt:** Fira Code at 18 pt falls below 0.2° beyond about 65 cm.
* **Size for 0.2°:** Fira Code needs 16.6 pt at 60 cm and 19.4 pt at 70 cm to reach 0.2°.
* **Size for a margin:** Fira Code needs 24.9 pt at 60 cm and 29.1 pt at 70 cm to reach 0.3°, the top of the critical-print-size range.
* **No cost to going larger:** Reading speed does not fall until about 2°, so the cost of a larger size is fewer lines and characters on screen, not slower reading ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Apply:** Set code and terminal text so the x-height is at least 0.25° at your measured distance, which is about 21 to 24 pt Fira Code at 60 to 70 cm.

### Age

* **Critical print size grows with age:** In 645 normally sighted readers aged 8 to 81, critical print size held at 0.08 logMAR to age 23, rose to 0.21 logMAR by 68, and rose to 0.34 logMAR by 81 (measured, MNREAD charts) ([Calabrèse et al. 2016](https://europepmc.org/abstract/MED/27442222)).
* **What that means in size:** 0.13 logMAR is a factor of 1.35, so a 68-year-old needs text 35% larger than a 23-year-old to read at full speed, and an 81-year-old needs it 82% larger.
* **Maximum speed falls:** Maximum reading speed was 200 ± 25 words per minute from 16 to 40 and fell to 175 by 81 (measured) ([Calabrèse et al. 2016](https://europepmc.org/abstract/MED/27442222)).
* **Age groups:** The authors see three groups, with a change after 40 ([Calabrèse et al. 2016](https://europepmc.org/abstract/MED/27442222)).
* **Older-adult studies:** A review of font size for older adults reports recommendations from 14 to 22 pt on mobile devices, and that age correlated with reading speed more than visual acuity did ([review, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9376262/)).
* **Low vision:** The range of print in daily life can fall below the critical print size of people with central-field loss ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Apply:** Expect the size you need to rise slowly after your twenties, by about a third by your late sixties, and re-check when your glasses prescription changes.

## 3. Line length

### Studies on screen

* **Longer lines read faster:** Dyson and Kipping tested 25 to 100 characters per line (10 pt Arial, 48 readers) and found 100 characters per line read faster than 25, with no other significant differences (measured, screen) ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **Scrolling explains part of it:** Part of the speed gain at 100 characters came from less scrolling, but not all of it ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **Medium lines understood better:** Dyson and Haselgrove found 55 characters per line gave better comprehension than 100, with no speed-accuracy trade-off (measured, screen) ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **Preference:** Readers rated 55 characters per line easiest to read, though it was not the fastest ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **No difference at 45, 76 and 132:** Bernard and colleagues found no difference in reading time or efficiency across 45, 76 and 132 characters per line in 20 adults (measured, screen, 12 pt Arial) ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **Upper limit not found:** Dyson says studies have not found the line length beyond which speed stops improving, and that 132 characters may be past it ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **Shaikh and Chaparro:** 20 students read news at 35, 55, 75 and 95 characters per line, read fastest at 95, and showed no difference in comprehension or satisfaction (measured, screen) **[unverified]** ([HFES 2005](https://journals.sagepub.com/doi/10.1177/154193120504900514)).
* **Older readers:** In Dyson and Kipping's column study, the speed advantage of the longer line appeared only in the 18 to 24 age group ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).

### Standards and conventions

* **WCAG 1.4.8 (AAA):** Text blocks should be no wider than 80 characters (40 for CJK) (standard) ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html)).
* **WCAG 1.4.8 basis:** The Understanding document says long lines make readers with reading and vision disabilities lose their place, and cites no study ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html)).
* **45 to 75:** Bringhurst calls 45 to 75 characters satisfactory and 66 ideal for a single printed column in a serif text face (convention, print) ([Bringhurst via webtypography.net](http://webtypography.net/2.1.2)).
* **45 to 90:** Butterick recommends 45 to 90 characters and cites no study (convention) ([Butterick](https://practicaltypography.com/line-length.html)).

### Code versus prose

* **No code study found:** No controlled study was found on line length for reading source code.
* **PEP 8:** Python limits code to 79 characters and comments and docstrings to 72, and allows up to 99 for teams that agree (convention) ([PEP 8](https://peps.python.org/pep-0008/)).
* **PEP 8 reason:** The stated reason is to fit files side by side and in review tools, not reading speed ([PEP 8](https://peps.python.org/pep-0008/)).
* **Why code differs:** Code lines vary in length and indentation, so a code limit caps the longest line, while a prose limit sets the width of every line.
* **Apply to prose:** Keep Markdown and other prose at 55 to 75 characters per line.
* **Apply to code:** Keep code at 80 to 100 characters, and treat this as convention.
* **Apply to Obsidian:** The current 40 rem width gives about 65 characters, which is inside both the studied and conventional ranges.

## 4. Line spacing

### Prose

* **Extremes hurt:** In the 104-reader web study, line spacings of 0.8 and 1.8 showed marginal signs of harming readability, and 1.0 and 1.4 did not (measured, screen) ([Rello et al. 2016](https://pielot.org/2016/01/optimal-font-size-for-web-pages/)).
* **Unit unclear:** The blog post does not define what 1.0 line spacing means in that study.
* **Old screen studies:** Kolers and colleagues found double spacing marginally better than single, and Kruk and Muter found single spacing significantly slower (measured, 1980s screens) ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **No recent studies:** Dyson found no recent studies that varied line spacing in fine steps ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **Low vision:** Extra line spacing did not raise reading speed in readers with macular degeneration **[unverified]** ([Chung 2008](https://onlinelibrary.wiley.com/doi/10.1097/OPX.0b013e31818527ea)).
* **WCAG 1.4.8 (AAA):** Line spacing should be at least 1.5 within paragraphs, for readers with cognitive disabilities who lose track when lines are close (standard; no study cited) ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html)).
* **Butterick:** Line spacing of 120% to 145% of the point size (convention) ([Butterick](https://practicaltypography.com/line-spacing.html)).
* **Apply:** Use 1.4 to 1.5 for prose.

### WCAG 1.4.12 text spacing

* **Values:** Content must still work when a user sets line height to 1.5, paragraph spacing to 2 x font size, letter spacing to 0.12 x font size and word spacing to 0.16 x font size (standard) ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).
* **What it requires:** The criterion does not tell authors to use these values; it requires that content not break when a user applies them ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).
* **Basis:** The Understanding document cites one study, McLeish 2007, on letter spacing for young readers with low vision, in which reading speed rose with spacing up to 0.25 em and levelled off from 0.20 ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).
* **Who chose the numbers:** Wayne Dick analysed the McLeish study and recommended the metrics the Working Group adopted ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).
* **Gap in the basis:** The document gives no study for the 1.5 line height, the 2x paragraph spacing or the 0.16 word spacing ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).
* **Testing:** The values were checked in about 480 languages and scripts for unwanted side effects ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).

### Monospace code

* **No study found:** No controlled study was found on line spacing for reading code.
* **Font defaults:** The built-in line height of the measured monospace fonts runs from 1.16 (Cascadia Code, Menlo) to 1.33 (Monaco) (measured from the font files).
* **VS Code default:** VS Code on macOS uses 1.5 when no line height is set ([fontInfo.ts](https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/editor/common/config/fontInfo.ts)).
* **Your two setups differ:** iTerm2 shows Fira Code at 1.23 and VS Code shows it at 1.5.
* **Apply:** Set code to 1.3 to 1.5, and set iTerm2 and VS Code to the same value so text looks the same in both (convention).
* **iTerm2 setting:** If iTerm2's vertical spacing multiplies the font's built-in 1.23, a value of 1.15 gives about 1.4 **[unverified]**.

## 5. Letter and word spacing

### Readers with dyslexia

* **Zorzi et al. 2012:** In 74 Italian and French children with dyslexia (ages 8 to 14), adding 2.5 pt between letters of 14 pt Times-Roman, with word and line spacing raised to match, halved reading errors (measured, paper) ([Zorzi et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3396504/)).
* **Speed gain:** Speed rose by about 0.3 syllables per second, and in the second experiment from 1.64 to 1.87 syllables per second (measured, paper) ([Zorzi et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3396504/)).
* **Spacing size:** 2.5 pt on 14 pt type is about 0.18 em of extra space.
* **Typical readers:** The 30 reading-level-matched typical readers showed no significant gain (errors p = 0.1; speed 1.87 vs 1.93 syllables per second, p > 0.3) ([Skottun & Skoyles letter](https://pmc.ncbi.nlm.nih.gov/articles/PMC3497831/)).
* **Critique:** Skottun and Skoyles argue the control group was too small to rule out a gain for typical readers, and that the larger gain may come from poor reading, not dyslexia ([letter](https://pmc.ncbi.nlm.nih.gov/articles/PMC3497831/)).
* **Letter spacing needs word spacing:** In 64 children with and 64 without dyslexia, extra letter spacing without matching extra word spacing slowed reading (measured) ([Galliussi et al. 2020](https://europepmc.org/abstract/MED/32172467)).
* **Perea and colleagues:** Extra letter spacing shortened word identification in adults, children and readers with dyslexia, with a larger effect in dyslexia (measured) **[unverified]** ([ERIC](https://eric.ed.gov/?id=EJ978028)).

### Typical adult readers

* **No gain beyond normal spacing:** Reading speed rose with letter spacing up to a critical spacing that was close to the standard spacing of Courier, then stayed flat or fell slightly, at the fovea and in the periphery (measured, screen RSVP, 6 readers) ([Chung 2002](https://europepmc.org/abstract/MED/11923275)).
* **Small gain in fixation time:** Adding 1.0 or 1.5 pt to 14 pt Times New Roman (about 0.07 to 0.11 em) shortened fixations by 7 to 12 ms in 24 Spanish adults (measured, screen, eye tracking) ([Perea & Gomez 2012](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0047568)).
* **No gain in text reading:** Adding 1.2 pt shortened fixations (237 vs 245 ms) but added fixations, so total reading time and comprehension did not change (measured, eye tracking) ([Perea et al. 2016](https://www.cambridge.org/core/journals/spanish-journal-of-psychology/article/abs/does-extra-interletter-spacing-help-text-reading-in-skilled-adult-readers/28F2F94EBC5DA75EF6A6E73110871C8F)).
* **Crowding:** Spacing limits how many letters you take in per fixation, and the critical spacing grows with distance from fixation (measured) ([Pelli et al. 2007](https://europepmc.org/abstract/MED/18217835)).
* **Monospace already spaces wide:** Courier-style fixed widths give more space between narrow letters than proportional fonts, which is why Courier helped at small sizes ([Mansfield et al. 1996](https://legge.psych.umn.edu/sites/legge.psych.umn.edu/files/files/media/mansfield96_psychophysics_of_reading_xv-_font_effects_in_normal_and_low_vision.pdf)).
* **Apply:** Leave letter spacing at the font default for code and prose.
* **Apply for dyslexia:** If a reader has dyslexia, add letter spacing only together with word spacing.

## 6. Space between paragraphs

* **No isolated study:** Dyson's review says paragraph treatment (indent versus extra space) has not been studied on its own on screen ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **Blank lines in a bundle:** One study of instructional screens included blank lines between paragraphs among many changes, so the effect of the blank lines cannot be separated ([Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf)).
* **WCAG 1.4.8 (AAA):** Paragraph spacing should be at least 1.5 times the line spacing (standard; rationale given, no study) ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html)).
* **WCAG 1.4.12 (AA):** Content must survive a user setting paragraph spacing to 2 x font size (standard; no study for this value) ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).
* **Butterick:** Use either a first-line indent or space between paragraphs, and set the space to 50% to 100% of the body size (convention) ([Butterick](https://practicaltypography.com/space-between-paragraphs.html)).
* **Markdown already chooses:** Markdown separates paragraphs with a blank line, so raw Markdown in Neovim and VS Code shows one full line of space and no indent.
* **Obsidian:** The Minimal theme's 1.75 rem paragraph spacing is 1.75 x the 16 px body size.
* **Apply:** Use space, not indents, between paragraphs on screen, at 0.75 to 1.5 x the font size (convention).

## 7. Font weight and rendering

### Thin versus regular

* **Light weights read worse:** In 24 adults searching 12 pt Helvetica Neue text, Ultra-Light and Light gave longer search times, longer fixations and shorter saccades than Regular and Bold (measured, 23-inch 1080p screen at 75 cm) ([Burmistrov et al. 2016](https://www.interux.com/publications/Burmistrov-NordiCHI16.pdf)).
* **Black background:** In the same study, search on a black background was slower than on white ([Burmistrov et al. 2016](https://www.interux.com/publications/Burmistrov-NordiCHI16.pdf)).
* **Weight helps small text only:** Palmén and colleagues summarise earlier work in which extra boldness helped letter recognition at small visual angles and not at large ones ([Palmén et al. 2023](https://thereadabilityconsortium.org/wp-content/uploads/2023/07/How-bold-can-we-be-The-impact-of-adjusting-font-grade-on-readability-in-light-and-dark-polarities-1.pdf)).
* **Fira Code Retina:** Fira Code ships a Retina weight with weight class 450, between Regular (400) and Medium (500) (measured from the font files).
* **Apply:** Use Regular (400) or Retina (450), and avoid Light and thinner weights for reading.

### macOS rendering

* **No subpixel anti-aliasing:** macOS 10.14 Mojave replaced subpixel anti-aliasing with grayscale anti-aliasing ([Michael Tsai](https://mjtsai.com/blog/2018/07/13/macos-10-14-mojave-removes-subpixel-anti-aliasing/)).
* **Retina makes this moot:** Apple says high-resolution displays allow fractional glyph positions and no longer need hinted screen fonts ([Apple](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Explained/Explained.html)).
* **Font smoothing adds weight:** Tonsky says the macOS font smoothing setting now only makes strokes bolder, and recommends turning it off with `defaults -currentHost write -g AppleFontSmoothing -int 0` (convention) ([Tonsky](https://tonsky.me/blog/monitors/)).
* **Integer scaling:** Tonsky recommends integer scaling (2x) over fractional scaling, which blurs text (convention) ([Tonsky](https://tonsky.me/blog/monitors/)).
* **This Mac:** The display already runs at 2x (2560 x 1440 points), so text is not blurred by scaling.
* **Apply:** Try font smoothing off and compare; it is a taste setting with no study.

### Dark mode and apparent weight

* **Light-on-dark looks heavier:** Designers call the effect halation or irradiation, and Palmén and colleagues note it is described in design media but has not been tested as a reading variable ([Palmén et al. 2023](https://thereadabilityconsortium.org/wp-content/uploads/2023/07/How-bold-can-we-be-The-impact-of-adjusting-font-grade-on-readability-in-light-and-dark-polarities-1.pdf)).
* **iTerm2 compensates:** iTerm2 draws anti-aliased text with thinner strokes by default on Retina displays when the background is darker than the text ([iTerm2](https://iterm2.com/documentation-preferences-profiles-text.html)).
* **Grade changes had no measured effect:** In 459 participants, changing font grade (weight without width change) had no detectable effect on paragraph reading at 14 px on a phone, in light or dark mode (measured, screen) ([Palmén et al. 2023](https://thereadabilityconsortium.org/wp-content/uploads/2023/07/How-bold-can-we-be-The-impact-of-adjusting-font-grade-on-readability-in-light-and-dark-polarities-1.pdf)).
* **Light mode read faster:** The same study found dark text on a light background read reliably faster than light on dark (measured, screen) ([Palmén et al. 2023](https://thereadabilityconsortium.org/wp-content/uploads/2023/07/How-bold-can-we-be-The-impact-of-adjusting-font-grade-on-readability-in-light-and-dark-polarities-1.pdf)).
* **Light mode at all ages:** Piepenbrock and colleagues found dark-on-light better for acuity and proofreading in younger and older adults, and more so for small text (measured, screen) ([NN/g summary](https://www.nngroup.com/articles/dark-mode/)).
* **Astigmatism:** People with astigmatism are often said to see more blur around light text on dark backgrounds **[unverified]**.
* **Apply:** If you stay in dark mode, keep iTerm2's thin strokes on and do not use a lighter font weight to compensate, because no study shows a gain.

## Where findings vary by person

* **Age:** Critical print size grows 35% by 68 and 82% by 81 against young adults ([Calabrèse et al. 2016](https://europepmc.org/abstract/MED/27442222)).
* **Low vision:** Monospace (Courier) gave 10% faster reading than Times in low vision ([Mansfield et al. 1996](https://legge.psych.umn.edu/sites/legge.psych.umn.edu/files/files/media/mansfield96_psychophysics_of_reading_xv-_font_effects_in_normal_and_low_vision.pdf)).
* **Low vision and spacing:** The WCAG spacing values come from a study of young readers with low vision ([W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)).
* **Dyslexia:** Extra letter spacing with matching word spacing helped children with dyslexia, and dyslexia fonts did not ([Zorzi et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3396504/), [Azzarello et al. 2026](https://europepmc.org/abstract/MED/42536336)).
* **Astigmatism:** No fetched study measures how astigmatism changes the effect of polarity or weight.
* **Individual critical print size:** Critical print size ranges from 0.15° to 0.3° across people, so the only reliable size is one tested on yourself ([Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/)).
* **Test yourself:** Read the same passage at three sizes at your normal distance, time each, and keep the smallest size that is not slower.

## Summary table

| Setting | Recommended value or range | Evidence | Source |
|---|---|---|---|
| Typeface style | Serif or sans-serif; choose by x-height and distinct letters | measured (no serif effect) | [Arditi & Cho 2005](https://europepmc.org/abstract/MED/16099015) |
| x-height of font | 0.52 em or larger | measured (x-height drives legibility at equal point size) | [Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/) |
| Confusable characters | Marked zero; distinct I, l, 1 | convention | [Braille Institute](https://www.brailleinstitute.org/freefont/), [JetBrains Mono](https://www.jetbrains.com/lp/mono/) |
| Monospace for prose | Acceptable; proportional may be up to about 5% faster | measured (paper charts; one null eye-tracking result) | [Mansfield et al. 1996](https://legge.psych.umn.edu/sites/legge.psych.umn.edu/files/files/media/mansfield96_psychophysics_of_reading_xv-_font_effects_in_normal_and_low_vision.pdf), [Jarosch et al.](https://zenodo.org/records/18912221) |
| Dyslexia fonts | Do not use for legibility | measured (meta-analysis g = -0.04) | [Azzarello et al. 2026](https://europepmc.org/abstract/MED/42536336) |
| Programming ligatures | Preference; off when sharing code | convention | [Fira Code](https://github.com/tonsky/FiraCode), [Butterick](https://practicaltypography.com/ligatures-in-programming-fonts-hell-no.html) |
| Text size | x-height at least 0.2°, aim for 0.25° or more (Fira Code about 21 to 24 pt at 60 to 70 cm on this display) | measured (paper charts and screen RSVP) | [Legge & Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/) |
| Web prose size | 18 pt / 24 px or larger | measured (screen, 104 readers) | [Rello et al. 2016](https://pielot.org/2016/01/optimal-font-size-for-web-pages/) |
| Size after 40 | About a third larger by late 60s | measured (paper charts) | [Calabrèse et al. 2016](https://europepmc.org/abstract/MED/27442222) |
| Prose line length | 55 to 75 characters | measured (55 best comprehension, screen) and convention (45 to 75) | [Dyson 2004](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf), [Bringhurst](http://webtypography.net/2.1.2) |
| Maximum line length | 80 characters | standard (WCAG 1.4.8 AAA, no study cited) | [W3C](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html) |
| Code line length | 80 to 100 characters | convention | [PEP 8](https://peps.python.org/pep-0008/) |
| Prose line spacing | 1.4 to 1.5 | measured (0.8 and 1.8 marginally worse, screen) and standard (WCAG 1.5) | [Rello et al. 2016](https://pielot.org/2016/01/optimal-font-size-for-web-pages/), [W3C](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html) |
| Code line spacing | 1.3 to 1.5, same in every tool | convention | [VS Code source](https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/editor/common/config/fontInfo.ts) |
| Letter spacing, typical adult | Font default | measured (no gain beyond standard spacing) | [Chung 2002](https://europepmc.org/abstract/MED/11923275), [Perea et al. 2016](https://www.cambridge.org/core/journals/spanish-journal-of-psychology/article/abs/does-extra-interletter-spacing-help-text-reading-in-skilled-adult-readers/28F2F94EBC5DA75EF6A6E73110871C8F) |
| Letter spacing, dyslexia | About +0.12 to +0.18 em, with word spacing raised to match | measured (children, paper) | [Zorzi et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3396504/), [Galliussi et al. 2020](https://europepmc.org/abstract/MED/32172467) |
| Text must tolerate | Line 1.5, paragraph 2x, letter 0.12 em, word 0.16 em | standard (WCAG 1.4.12; based on one low-vision letter-spacing study) | [W3C](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html) |
| Paragraph separation | Space, not indent, of 0.75 to 1.5 x font size | convention | [Butterick](https://practicaltypography.com/space-between-paragraphs.html) |
| Font weight | Regular (400) or Retina (450); no Light | measured (screen, 24 readers) | [Burmistrov et al. 2016](https://www.interux.com/publications/Burmistrov-NordiCHI16.pdf) |
| Dark-mode weight | Keep iTerm2 thin strokes; no weight change needed | convention; measured null for grade | [iTerm2](https://iterm2.com/documentation-preferences-profiles-text.html), [Palmén et al. 2023](https://thereadabilityconsortium.org/wp-content/uploads/2023/07/How-bold-can-we-be-The-impact-of-adjusting-font-grade-on-readability-in-light-and-dark-polarities-1.pdf) |
| Font smoothing | Try off; taste setting | convention | [Tonsky](https://tonsky.me/blog/monitors/) |
| Display scaling | Integer 2x (current) | convention | [Tonsky](https://tonsky.me/blog/monitors/) |
