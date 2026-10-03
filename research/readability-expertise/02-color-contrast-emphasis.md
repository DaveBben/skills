# Color, contrast and emphasis when reading text and code on screens

Research date: 2026-10-02.

This file answers six questions for one reader.
The reader reads terminal output, code and Markdown on a 27-inch 5K Retina display under macOS.
The tools are iTerm2, VS Code with Catppuccin Mocha, Neovim and Obsidian with the Minimal theme, all in dark mode today.

## How to read the labels

* **Measured:** A controlled study tested the claim; the bullet gives numbers and conditions.
* **Standard:** A published standard or specification states the rule (W3C WCAG, ECMA-48, NO_COLOR).
* **Convention:** Practitioners or vendors recommend it, without a controlled study behind it.
* **[unverified]:** The claim comes from a search snippet or from memory, not from a page I fetched.
* **Terms:** "Positive polarity" means dark text on a light background (light mode). "Negative polarity" means light text on a dark background (dark mode).

## 1. Polarity: light mode against dark mode

### What the measured studies found

* **Buchner & Baumgartner 2007:** Proofreading was better with dark-on-light text than with light-on-dark text across a series of experiments. The advantage held in darkness and in office lighting, and for black/white and blue/yellow pairs. Red text on green could not replace missing luminance contrast. Heart rate, skin conductance and self-reported eyestrain did not differ between conditions. Source: abstract at https://europepmc.org/article/MED/17510822.
* **Buchner & Baumgartner 2007 conditions:** The light display averaged 180.30 cd/m² and the dark display 12.23 cd/m² in Experiment 1. Ambient light ranged from 5 lx to 550 lx. Source: Buchner, Mayr & Brandt 2009, https://www.psychologie.hhu.de/fileadmin/redaktion/Oeffentliche_Medien/Fakultaeten/Mathematisch-Naturwissenschaftliche_Fakultaet/Psychologie/AAP/Publikationen/2009/Buchner_Mayr_Brandt__2009_.pdf.
* **Buchner, Mayr & Brandt 2009:** When the researchers made both polarities equally bright overall, the polarity advantage disappeared. Only overall display luminance mattered, and brighter displays gave better performance. The authors conclude that polarity itself does not affect readability. Source: same PDF as above (Ergonomics 52(7), 882–886).
* **Piepenbrock et al. 2013 (age):** 84 younger adults (18–33, mean 22.6) and 85 older adults (60–85, mean 69.8) took an acuity test and a proofreading task in one polarity each. Screen white was 350 cd/m² and black 1 cd/m². Text was 10-point Helvetica at 50 cm. Dark-on-light gave better acuity in both groups (younger d = 2.17, older d = 0.58). Dark-on-light gave better proofreading in both groups (polarity η² = 0.06, no age interaction). Reading rate and self-reported eyestrain, headache and mood did not differ. Source: https://www.psychologie.hhu.de/fileadmin/redaktion/Oeffentliche_Medien/Fakultaeten/Mathematisch-Naturwissenschaftliche_Fakultaet/Psychologie/AAP/Publikationen/2013/Piepenbrock-2013-Positive_display_polarity_is_.pdf.
* **Piepenbrock et al. 2014 (character size, Human Factors):** 160 analysed participants proofread black-on-white or white-on-black text at 8, 10, 12 and 14 pt. These sizes gave x-heights of 0.22° to 0.34° of visual angle. The light-mode advantage grew linearly as text got smaller (interaction with linear size trend: F(1,158) = 10.61, p = .001). The authors write that light-on-dark "should be avoided", "especially with small font sizes". Source: author manuscript at https://www.psychologie.hhu.de/fileadmin/redaktion/Oeffentliche_Medien/Fakultaeten/Mathematisch-Naturwissenschaftliche_Fakultaet/Psychologie/AAP/Publikationen/in_press/Piepenbrock_Mayr_Buchner_inpress_.pdf.
* **Piepenbrock et al. 2014 (pupil, Ergonomics):** 35 adults aged 20–30 read both polarities in a 0.1 lx room. Mean pupil diameter was 2.09 mm with dark-on-light and 3.65 mm with light-on-dark. Proofreading accuracy (dz = 0.77) and reading rate (dz = 0.68) were higher with dark-on-light. Smaller pupils predicted better accuracy and faster reading in a mixed model. The light from the screen alone changed eye-level illuminance from 2.7 lx to 118.4 lx. Source: author manuscript at https://www.psychologie.hhu.de/fileadmin/redaktion/Oeffentliche_Medien/Fakultaeten/Mathematisch-Naturwissenschaftliche_Fakultaet/Psychologie/AAP/Publikationen/in_press/Piepenbrock-in_press-Smaller_pupil_size_and_better.pdf.
* **Mechanism:** A brighter screen narrows the pupil. A narrower pupil reduces optical aberrations and increases depth of field, so the retinal image of small letters is sharper. Source: the 2014 pupil manuscript above and Dobres et al. 2017, https://jdobr.es/pdf/Dobres-etal-2017-Ambient.pdf.
* **Dobres, Chahine & Reimer 2017:** 34 adults (mean age about 38) made word/non-word decisions on brief glances. Letter heights were 3 mm and 4 mm (14.7 and 19.6 arcmin). Rooms were near 0 lx or 4750 lx. In the dark room, light-on-dark needed 122.3 ms at 3 mm against 84.1 ms for dark-on-light. In the bright room, the polarity difference was not statistically significant (88.7 ms against 86.0 ms at 3 mm). The authors call this a "negative polarity disadvantage" that appears in dark rooms with small text. Source: https://jdobr.es/pdf/Dobres-etal-2017-Ambient.pdf.

### Is the light-mode advantage tied to small text and ambient light?

* **Size:** Yes. The advantage grows as text shrinks (Piepenbrock 2014, Dobres 2017, both above).
* **Ambient light:** Partly. Buchner & Baumgartner found the advantage from 5 lx to 550 lx. Dobres found it only in a near-dark room and not at 4750 lx, which is near outdoor daylight. Typical office lighting (about 500 lx) sits inside the range where the advantage was found. Sources: https://europepmc.org/article/MED/17510822 and https://jdobr.es/pdf/Dobres-etal-2017-Ambient.pdf.
* **Your text size:** On a 27-inch 5K display at the default 2560 × 1440 "looks like" scaling, one point is about 0.233 mm. A 13-point code font with an x-height of 0.52 em at 60 cm gives an x-height of about 0.15°. This is my calculation, not a study. It is below the smallest size Piepenbrock tested (0.22°), so your code text sits where the light-mode advantage was largest. Measure your own font size and viewing distance before relying on this.

### Newer studies on dark mode

* **Sethi & Ziat 2023:** Younger and older adults wrote and searched in both polarities under bright and dim rooms. Light-on-dark raised cognitive load (longer search time, larger pupils) for older adults in a bright room and for younger adults in a dim room. Older adults reported more positive emotion with light mode. Younger adults expressed more interest in dark mode, which the authors read as aesthetic preference. Source: https://europepmc.org/article/MED/36533999.
* **Pathari et al. 2024 (ACHI):** 18 IT students used a smartphone in both modes. Self-reported eye fatigue was lower with dark mode in a 460 lx room (p = 0.004) and did not differ in a 33 lx room. The sample is small. Source: https://www.thinkmind.org/articles/achi_2024_3_150_20069.pdf.
* **Sengsoon & Intaruk 2025:** 30 women aged 18–25 used an iPad for 1 hour per mode at 100% brightness in a 300–500 lx room. Visual-fatigue scores did not differ (18.37 light, 18.87 dark). Dry-eye scores were lower after dark mode (22.73 against 24.40). Both modes raised fatigue over the hour. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC12027292/.
* **Mixed reality 2025:** A video see-through headset at 39 pixels per degree reproduced the light-mode advantage for proofreading and symbol identification. Source: https://europepmc.org/article/MED/39918051.
* **Text colour within dark mode, 2024:** In a light-on-dark reading task under several room lights, red text produced the most measured fatigue and yellow text the least. The abstract gives no effect sizes. Source: https://europepmc.org/article/MED/38894307.

### Astigmatism, halation and cataract

* **Halation claim:** Light text on a dark background is said to "bleed" or glow for people with astigmatism, because the larger pupil passes light through more of the irregular cornea. I found no controlled study that tested this in astigmatic readers. Treat it as **[unverified]** optical reasoning. Source for the claim: https://www.astigmatismofit.com/blog/dark-mode-vs-light-mode-astigmatism.
* **What supports the reasoning:** Light-on-dark text does produce larger pupils (3.65 mm against 2.09 mm), and larger pupils pass more aberration. Source: the 2014 pupil manuscript above.
* **Cloudy ocular media:** Legge et al. 1985 found that readers with cataract-like cloudy media read faster with light-on-dark text. Readers with central-field loss were not affected by polarity. Source: summary in https://www.nngroup.com/articles/dark-mode/.
* **macOS rendering:** iTerm2 draws thinner strokes on Retina displays when the background is darker than the text. This reduces the visual weight of light text on dark. Source: https://iterm2.com/documentation-preferences-profiles-text.html.

### Eye strain and sleep

* **Eye strain:** Controlled studies have not shown dark mode reduces eye strain on desktop displays. Buchner & Baumgartner 2007 and Piepenbrock 2013 found no difference in self-reported eyestrain. The two small 2024–2025 mobile studies found lower fatigue or dry-eye scores with dark mode under room light. Sources: https://europepmc.org/article/MED/17510822, the 2013 PDF above, https://www.thinkmind.org/articles/achi_2024_3_150_20069.pdf, https://pmc.ncbi.nlm.nih.gov/articles/PMC12027292/.
* **Myopia marker:** Aleman, Wang & Schaeffel 2018 found the choroid (the blood-vessel layer behind the retina) thinned by about 16 µm after one hour of reading black-on-white text and thickened by about 10 µm with white-on-black. Choroid thinning is associated with myopia development in animal and human studies. This is a one-hour marker in a small group, not a measured change in myopia. Source: abstract via https://api.openalex.org/works/doi:10.1038/s41598-018-28904-x and summary in https://www.nngroup.com/articles/dark-mode/.
* **Sleep:** I found no controlled study comparing dark mode with light mode on sleep. Schöllhorn et al. 2023 exposed 72 men to display light 4 hours before bedtime. Lower melanopic (blue-weighted) light shortened time to fall asleep and reduced melatonin suppression, in a dose-dependent way. Dark mode lowers total light from the screen, so it plausibly lowers melanopic dose. That last step is inference, not a measured result. Source: https://europepmc.org/article/MED/36854795.

### Recommendations for polarity

* **Use light mode for long reading of small text:** Measured. The advantage appeared in every lab study above and grew as text got smaller. It comes from screen brightness, not from polarity itself.
* **Never pair dark mode with a dark room:** Measured. Dark room plus light-on-dark gave the slowest legibility in Dobres 2017 (122 ms against 84 ms at 3 mm). Light the room.
* **Enlarge text if you keep dark mode:** Measured. The polarity penalty shrinks as text grows (Piepenbrock 2014, Dobres 2017).
* **Keep dark mode if you prefer it and your text is large:** Convention. Preference and mood favoured dark mode for younger adults in Sethi & Ziat 2023, and performance differences shrink with large text and bright rooms.

## 2. Background colour

* **Pure white against off-white:** I found no controlled study that compared #FFFFFF with an off-white or cream background for reading speed or comprehension in readers without dyslexia. Claims that off-white reduces glare come from blogs.
* **Rello & Bigham 2017:** 341 participants (89 with dyslexia) read black text on ten coloured backgrounds online. Peach, orange and yellow gave the shortest reading times. Blue-grey gave the longest, 45–53% longer than peach. The study did not include white or off-white. Participants used their own computers. Source: https://www.cs.cmu.edu/~jbigham/pubs/pdfs/2017/colors.pdf.
* **Li et al. 2025:** 40 students read on light green (RGB 207, 232, 204) or white. Light green lowered rated difficulty and negative mood for Chinese text. Neither background changed reading performance for English text. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC12331638/.
* **Pure black against dark grey:** Google's Material dark theme uses dark grey instead of black. Google's stated reasons are visible shadows and less eye strain for light text, with no study cited. Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/theming/Dark.md.
* **Coloured overlays and Irlen lenses:** Griffiths et al. 2016 reviewed 51 published items (54 data sets) across Irlen, Intuitive, Chromagen and other systems. Most studies had high or uncertain risk of bias. Studies with lower risk of bias showed less benefit. Effects were small or matched placebo. Source: https://europepmc.org/article/MED/27580753 and https://pure.york.ac.uk/portal/en/publications/the-effect-of-coloured-overlays-and-lenses-on-reading-a-systemati/.
* **Overview of reviews:** Suttle, Lawrenson & Conway 2018 appraised four systematic reviews with AMSTAR 2. Three found insufficient good-quality evidence for overlays or lenses. The overview concludes there is "not yet a reliable evidence base" to recommend them. Source: https://openaccess.city.ac.uk/id/eprint/19242/.

### Recommendations for background colour

* **Do not expect a tinted background to improve reading:** Measured. Systematic reviews found no reliable benefit from coloured overlays.
* **Pick white or off-white by comfort:** Convention. No study separates them.
* **Use dark grey instead of pure black in dark mode:** Convention. Catppuccin Mocha's base (#1E1E2E) already does this.

## 3. Contrast

### WCAG 2.x contrast ratio

* **Thresholds:** WCAG 2.2 Success Criterion 1.4.3 (level AA) requires 4.5:1 for normal text and 3:1 for large text. Large text is 18 pt, or 14 pt bold. Source: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html.
* **Enhanced thresholds:** Success Criterion 1.4.6 (level AAA) requires 7:1 for normal text and 4.5:1 for large text. Source: https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html.
* **Rationale:** The 4.5:1 figure assumes a reader with 20/40 acuity needs about 1.5 times the normal 3:1. The 7:1 figure targets 20/80 acuity. Source: the two W3C pages above.
* **Thin fonts:** W3C notes that anti-aliasing and thin strokes lower the real contrast below the computed value. It advises choosing fonts with thicker strokes. Source: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html.
* **Flaw with dark colours:** The APCA documentation states that WCAG 2 "overstates contrast for dark colors to the point that 4.5:1 can be functionally unreadable when one of the colors in a pair is near black." It concludes WCAG 2 contrast "cannot be used for guidance designing 'dark mode'." Source: https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.
* **Worked example:** I computed both metrics with the APCA-W3 0.0.98G constants from https://github.com/Myndex/apca-w3. Black text on #777777 scores 4.69:1 and passes WCAG AA, yet scores Lc 33 in APCA. White text on #777777 scores 4.48:1 and fails WCAG AA, yet scores Lc −76.6. The ratio cannot tell these two cases apart in the direction readers do.

### APCA and WCAG 3

* **Scale:** APCA reports lightness contrast (Lc) from 0 to about ±106. A positive value means dark text on a light background. A negative value means light text on a dark background. Source: https://git.apcacontrast.com/documentation/APCAeasyIntro.html.
* **Body text levels:** Lc 90 is the preferred level for body text no smaller than 18 px at weight 300 or 14 px at weight 400. Lc 75 is the minimum for body text no smaller than 24 px/300, 18 px/400, 16 px/500 or 14 px/700. Lc 60 is the minimum for other content text. Lc 45 is the minimum for headlines. Source: https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.
* **Lookup for small text:** The APCA readability criterion lists Lc 100 for 14 px at weight 400 and Lc 90 for 16 px at weight 400. Source: https://www.readtech.org/ARC/tests/visual-readability-contrast/.
* **Maximum contrast:** APCA suggests Lc 90 as a maximum for text larger than 36 px bold and for large areas of colour. It gives a preliminary dark-mode maximum of Lc −90 for large fonts. Sources: https://www.readtech.org/ARC/tests/bronze-simple-mode/ and https://git.apcacontrast.com/documentation/APCAeasyIntro.html.
* **Status:** The WCAG 3.0 Working Draft of 10 September 2026 does not name APCA. It reads "[contrast measure to be determined]" and says the algorithm "is yet to be determined". APCA is a proposal, not an adopted standard. Source: https://www.w3.org/TR/wcag-3.0/.

### Is too much contrast a problem?

* **Reading speed tolerates lower contrast:** Legge, Rubin & Luebker 1987 measured reading speed against contrast for normal vision. Speed peaked near 350 words per minute for letters from 0.25° to 2°. For 1° letters, a tenfold drop in contrast cut speed by less than half. Results were similar for white-on-black and black-on-white. Source: https://europepmc.org/article/MED/3660667.
* **No measured harm from maximum contrast in normal vision:** I found no controlled study showing that 21:1 text slows reading or raises strain in readers with normal vision. The APCA maximums are design guidance for large text, not study results.
* **People who need lower contrast:** W3C notes that "some people with cognitive disabilities require color combinations or hues that have low contrast" and allows user-adjustable colours. Source: https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html.

### iTerm2 Minimum Contrast

* **What it does:** "It has the effect of shifting text colors that are similar to their background colors closer to black or white. As this setting is increased, more colors are affected and the effect is greater. At 100, all text will be pure black or pure white. Minimum contrast never modifies background colors." Source: https://iterm2.com/documentation-preferences-profiles-colors.html.
* **Why it exists:** Programs choose ANSI colour numbers, but the user's theme decides what those numbers look like. A program cannot know that its blue lands on your dark blue background. Source: same page.
* **Equivalent elsewhere:** Windows Terminal has `adjustIndistinguishableColors` with values `always`, `indexed` and `never`. Source: https://learn.microsoft.com/en-us/windows/terminal/customize-settings/profile-appearance.
* **Value:** No study or vendor gives a recommended value.

### Your current theme

These are my calculations with the WCAG formula and APCA-W3 0.0.98G, using hex values from https://raw.githubusercontent.com/catppuccin/palette/main/palette.json.

| Catppuccin Mocha pair (text on base #1E1E2E) | WCAG 2 ratio | APCA Lc |
|---|---|---|
| Text #CDD6F4 | 11.34:1 | −80.0 |
| Subtext1 #BAC2DE | 9.26:1 | −68.1 |
| Subtext0 #A6ADC8 | 7.37:1 | −56.2 |
| Overlay2 #9399B2 | 5.81:1 | −45.5 |
| Overlay0 #6C7086 | 3.36:1 | −25.8 |
| Red #F38BA8 | 7.08:1 | −54.7 |
| Green #A6E3A1 | 11.03:1 | −78.3 |

* **Main text:** Mocha's text colour passes WCAG AAA (7:1) and APCA's body-text minimum (Lc 75), and sits below APCA's preferred Lc 90.
* **Secondary text:** Subtext0, Overlay2 and the accent colours fall below Lc 60, the APCA minimum for non-body content text. Overlay0 fails WCAG AA for text.

### Recommendations for contrast

* **Keep body text at or above 7:1:** Standard (WCAG 2.2 AAA).
* **Keep any text at or above 4.5:1:** Standard (WCAG 2.2 AA).
* **Check dark-mode pairs with APCA, aiming for Lc 75 or more (absolute value) for body text and Lc 90 for small text:** Convention (proposed method, not adopted).
* **Do not chase 21:1:** Measured. Reading speed changes little across a wide contrast range at normal sizes (Legge 1987).
* **Set iTerm2 Minimum Contrast to the lowest value that makes your unreadable ANSI pairs readable:** Convention. Zero leaves unreadable pairs, and 100 removes all colour.

## 4. Number of colours and syntax highlighting

### Does highlighting help comprehension?

* **Sarkar 2015:** 10 graduate students mentally executed short Python programs, with and without highlighting, under an eye tracker. Highlighted tasks finished faster, by a median of 8.4 s (p = 0.047). Highlighted code needed fewer gaze switches between regions (median 23 fewer). Fixation counts and durations did not change. The time benefit shrank as experience grew (log-normalised r = −0.39, p = 0.033). Source: https://ppig.org/files/2015-PPIG-26th-Sarkar1.pdf.
* **Beelders & du Plessis 2016:** 34 IT students (mean age 21.7) read C# snippets in colour or black-and-white, 17 per group. Fixations, fixation durations and regressions were higher for black-and-white, but not statistically significant. Students rated colour code easier to read. Source: https://pdfs.semanticscholar.org/32f5/b62050bb572a8d8d62981a7095669190016e.pdf.
* **Hannebauer, Hesenius & Gruhn 2018:** About 400 novices in an introductory Java course solved small tasks with and without highlighting. Correctness did not differ. Source: summary at https://academiccomputing.wordpress.com/2018/11/30/code-highlighting-the-lowlights/. The exact count of 390 and the authors' phrase that highlighting "squanders a feedback channel" come from search snippets **[unverified]**. Paper: https://doi.org/10.1007/s10664-017-9579-0.
* **Hakala et al. 2006:** Highlighting did not change the speed of visual search on screen. Source: cited in Sarkar 2015, https://ppig.org/files/2015-PPIG-26th-Sarkar1.pdf.
* **Baecker 1988:** Improved layout and typography of code, including colour, raised correct answers by 11%. Colour was one of several changes. Source: cited in Sarkar 2015, same URL.
* **Summary:** Highlighting gives at most a small speed gain, for less experienced readers, in small studies. No study shows a comprehension gain for experienced programmers.

### Minimal highlighting

* **Prokopov 2025:** Nikita Prokopov's post "I am sorry, but everyone is getting syntax highlighting wrong" (15 October 2025) argues "if everything is highlighted, nothing is highlighted." He advises: "Limit the number of different colors to what you can remember." He advises against colouring keywords, variable uses and function calls. He advises colouring strings and constants, top-level definitions and comments, and making comments prominent instead of dim. He cites no studies. Source: https://tonsky.me/blog/syntax-highlighting/.
* **Alabaster:** Prokopov's theme highlights four classes: strings, statically known constants, comments and global definitions. It leaves keywords plain because "they are usually least important and most obvious part of any program." It has light, dark, background-colour and monochrome variants. Source: https://github.com/tonsky/sublime-scheme-alabaster.

### How many colours can people track?

* **Healey 1996:** 38 observers searched displays for one coloured target among others of equal brightness. Three and five colours gave fast, accurate search (mean response 459–661 ms). Seven colours worked only when chosen with enough colour distance and from distinct named colour categories. Nine colours raised errors to 8.1% and produced slow serial search for some hues. Healey concludes seven equal-brightness colours is about the maximum for rapid identification. This is visual search, not code reading. Source: https://vis.cs.brown.edu/docs/pdf/Healey-1996-CEC.pdf.

### Colour-vision deficiency

* **Prevalence:** Red-green deficiency occurs in about 1 in 12 men and 1 in 200 women of Northern European ancestry. Blue-yellow deficiency occurs in fewer than 1 in 10,000 people. Source: https://medlineplus.gov/genetics/condition/color-vision-deficiency/.
* **Failing pairs:** Protanopia and deuteranopia make red and green indistinguishable. Deuteranomaly makes some greens look redder, and protanomaly makes some reds look greener and dimmer. Tritanopia confuses blue with green, purple with red, and yellow with pink. Source: https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness/types-color-vision-deficiency.
* **Standard:** WCAG 1.4.1 says colour must not be "the only visual means of conveying information." When the user must recognise a specific colour, such as green for valid and red for invalid, "an additional visual indicator will be required regardless of the contrast ratio." Source: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html.

### Recommendations for colours

* **Keep distinct hues in a theme to about five, and at most seven:** Measured (Healey 1996), applied by analogy from visual search to code.
* **Highlight few token classes, such as strings, constants, comments and definitions:** Convention (Prokopov, Alabaster).
* **Do not expect highlighting to improve comprehension for an experienced reader:** Measured (Sarkar 2015, Hannebauer 2018, Beelders 2016).
* **Never encode a difference by red against green alone; add a symbol, word or position:** Standard (WCAG 1.4.1).

## 5. Emphasis

* **All capitals:** Tinker & Paterson (320 readers) found all-capital text read 11.8% slower than lower case. A later Tinker study with 60 students found 9.5% to 19.0% slower over 5–10 minutes and 13.9% slower over 20 minutes. All-capital text takes about 35% more space at the same point size. 90% of 224 readers judged lower case more legible. Source: Tinker, *Legibility of Print* (1963), https://gwern.net/doc/design/typography/1963-tinker-legibilityofprint.pdf.
* **All capitals, the exception:** Arditi & Cho 2007 held point size fixed. Capitals were read faster than mixed case at twice the acuity limit, for both normal and low-vision readers. At ten times the acuity limit the advantage disappeared. Capitals are physically larger at the same point size. Source: https://europepmc.org/article/MED/17675131.
* **Why capitals read slower:** Kevin Larson's review attributes the lower-case advantage to practice, not to word shape. Readers forced to read large amounts of capitals speed up toward lower-case rates. Source: https://learn.microsoft.com/en-us/typography/develop/word-recognition.
* **Italics:** Italic print was read 2.7% slower than roman in one experiment and 4.9% slower over 30 minutes for 96 readers (all differences p < .01). 96% of 224 readers preferred roman. Combined with small type and dim light, the slowdown exceeded 10%. Tinker advises italics only "on those rare occasions when added emphasis is needed." Source: https://gwern.net/doc/design/typography/1963-tinker-legibilityofprint.pdf.
* **Bold:** Paterson & Tinker found no difference in reading speed between boldface and ordinary lower case. 70% of 224 readers preferred ordinary lower case. Tinker concludes bold "may be used for emphasis whenever desired," but not for large amounts of text. Source: same PDF.
* **Mixed forms:** Tinker reports that mixing lower case, italics, capitals and bold within paragraphs "markedly retards speed of reading." Source: same PDF.
* **Underline and too much emphasis:** Lorch, Lorch & Klusewitz 1995 had students read a 4-page text with no underlining, with only target sentences underlined, or with targets plus half the other sentences underlined. Recall of targets improved only in the light condition. Heavy underlining gave the same recall as none. **[unverified]**: from a search snippet. Paper: https://doi.org/10.1006/ceps.1995.1003.
* **Colour as emphasis:** clig.dev advises: "if everything is a different color, then the color means nothing and only makes it harder to read." Source: https://clig.dev/.

### Emphasis in terminals

* **The escape codes:** ECMA-48 defines Select Graphic Rendition parameter 1 as "bold or increased intensity", 2 as "faint, decreased intensity", 3 as "italicized" and 4 as "singly underlined". Source: https://ecma-international.org/wp-content/uploads/ECMA-48_5th_edition_june_1991.pdf.
* **Bold as bright:** Because parameter 1 can mean "increased intensity", terminals may draw bold text in the bright variant of its colour. Windows Terminal's `intenseTextStyle` offers `bold`, `bright`, `all` and `none`, and defaults to `bright`. Alacritty's `draw_bold_text_with_bright_colors` defaults to false. Sources: https://learn.microsoft.com/en-us/windows/terminal/customize-settings/profile-appearance and https://alacritty.org/config-alacritty.html.
* **iTerm2 bold:** "Draw bold text in bold font" uses the bold face. If the font has none, iTerm2 simulates bold by drawing the text twice, one pixel apart. A profile can also set a separate colour for bold text. Sources: https://iterm2.com/documentation-preferences-profiles-text.html and https://iterm2.com/documentation-preferences-profiles-colors.html.
* **iTerm2 italics and faint:** Italics render only if the option is on and "the font you select must have an italic face." Faint text has an opacity setting with a floor of 0.1. Sources: same two iTerm2 pages.
* **tmux:** With `default-terminal` set to `screen` or `screen-*`, tmux disables italics. Setting `default-terminal` to `tmux` enables them. Source: https://raw.githubusercontent.com/wiki/tmux/tmux/FAQ.md.

### Recommendations for emphasis

* **Use bold for emphasis in running text:** Measured (no speed cost, Tinker).
* **Keep italics to short spans:** Measured (2.7–4.9% slower, more under poor conditions).
* **Avoid all capitals for running text:** Measured (about 12–14% slower); short labels at small sizes are the exception (Arditi & Cho 2007).
* **Emphasise a few items per screen, not most of them:** Measured but **[unverified]** (Lorch 1995); also convention (clig.dev, Prokopov).
* **Turn on bold font and turn off bold-as-bright in the terminal, so bold changes weight and colour keeps one meaning:** Convention.

## 6. Semantic colour in terminal output

* **NO_COLOR:** "Command-line software which adds ANSI color to its output by default should check for a NO_COLOR environment variable that, when present and not an empty string (regardless of its value), prevents the addition of ANSI color." User config files and command-line flags override it. It covers colour only, not bold, underline or italic. Source: https://no-color.org/.
* **When to disable colour (clig.dev):** Disable colour when stdout or stderr is not a terminal, checking each stream separately. Disable it when NO_COLOR is set and non-empty, when `TERM` is `dumb`, or when the user passes `--no-color`. Consider an application-specific `MYAPP_NO_COLOR`. clig.dev also lists `FORCE_COLOR` to force colour on. Source: https://clig.dev/.
* **Red for errors:** clig.dev lists "use red to indicate an error" as an intended use, and warns "the eye will be drawn to red text, so use it intentionally and sparingly." It also advises putting the most important information at the end of the output. Source: https://clig.dev/.
* **Red and green together:** Red-for-error and green-for-success is exactly the pair that red-green colour deficiency merges (about 1 in 12 men). WCAG 1.4.1 requires a second cue when meaning depends on recognising a colour. Sources: https://medlineplus.gov/genetics/condition/color-vision-deficiency/ and https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html.
* **Symbols:** clig.dev suggests symbols and emoji where they make output clearer, and warns they can make a program "look cluttered or feel like a toy." Source: https://clig.dev/.
* **Bold headings:** clig.dev: "Bold headings make it much easier to scan." Source: https://clig.dev/.

### Recommendations for terminal output

* **Honour NO_COLOR, `--no-color` and `TERM=dumb`, and drop colour when a stream is not a terminal:** Standard (NO_COLOR) and convention (clig.dev).
* **Use red for errors, sparingly:** Convention (clig.dev).
* **Pair every status colour with a word or symbol, such as "error:", "ok" or ✗/✓:** Standard (WCAG 1.4.1, applied by analogy to terminal output).

## Where findings vary by person

* **Age:** The light-mode acuity advantage was smaller in adults aged 60–85 (d = 0.58) than in adults aged 18–33 (d = 2.17), but present in both. Older adults showed higher cognitive load with dark mode in bright rooms. Sources: Piepenbrock 2013 PDF above and https://europepmc.org/article/MED/36533999.
* **Cloudy ocular media (cataract):** These readers read faster with light-on-dark text (Legge 1985, via https://www.nngroup.com/articles/dark-mode/).
* **Astigmatism:** No controlled polarity study found; the halation claim is **[unverified]**.
* **Myopia:** One-hour choroid changes favour light-on-dark text; long-term effect not measured (Aleman 2018).
* **Colour-vision deficiency:** Red-green pairs fail for about 8% of men; blue-green, purple-red and yellow-pink fail for the rare tritan types.
* **Ambient light:** The dark-mode penalty is largest in a dark room (Dobres 2017). Dark mode reduced self-reported fatigue only in a lit room in one small phone study (Pathari 2024).
* **Dyslexia:** Warm backgrounds read faster than cool ones in one large online study (Rello & Bigham 2017); systematic reviews do not support coloured overlays.
* **Low vision:** WCAG's 4.5:1 and 7:1 targets are built around 20/40 and 20/80 acuity. Capitals help at sizes near the acuity limit (Arditi & Cho 2007).

## Summary table

| Setting | Recommended value or range | Evidence | Source |
|---|---|---|---|
| Polarity for long reading of small text | Dark text on light background | Measured | https://europepmc.org/article/MED/17510822, Piepenbrock 2013/2014 PDFs above, https://jdobr.es/pdf/Dobres-etal-2017-Ambient.pdf |
| Room light when using dark mode | Lit room, not near-dark | Measured | https://jdobr.es/pdf/Dobres-etal-2017-Ambient.pdf |
| Text size when using dark mode | Larger than in light mode | Measured | Piepenbrock 2014 Human Factors manuscript above |
| Dark-mode background | Dark grey (for example #1E1E2E), not #000000 | Convention | https://raw.githubusercontent.com/material-components/material-components-android/master/docs/theming/Dark.md |
| Light-mode background | White or off-white by comfort | Convention (no study found) | — |
| Tinted background or overlay | Not for reading benefit | Measured (systematic reviews) | https://europepmc.org/article/MED/27580753, https://openaccess.city.ac.uk/id/eprint/19242/ |
| Body text contrast, WCAG 2 | ≥ 7:1 (AAA); never below 4.5:1 (AA) | Standard | https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html |
| Body text contrast, APCA | abs(Lc) ≥ 75; ≥ 90 for 14–16 px text | Convention (proposed, not adopted) | https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell |
| Maximum contrast | No need to reach 21:1; speed is flat over a wide range | Measured | https://europepmc.org/article/MED/3660667 |
| iTerm2 Minimum Contrast | Lowest value that fixes unreadable ANSI pairs | Convention | https://iterm2.com/documentation-preferences-profiles-colors.html |
| Distinct syntax colours | About 5, at most 7 | Measured (visual search, by analogy) | https://vis.cs.brown.edu/docs/pdf/Healey-1996-CEC.pdf |
| Token classes to colour | Strings, constants, comments, definitions | Convention | https://tonsky.me/blog/syntax-highlighting/ |
| Red against green as the only cue | Never; add a word or symbol | Standard | https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html |
| Emphasis in prose | Bold | Measured | https://gwern.net/doc/design/typography/1963-tinker-legibilityofprint.pdf |
| Italics | Short spans only | Measured | same |
| All capitals in running text | Avoid | Measured | same, and https://europepmc.org/article/MED/17675131 |
| Amount of emphasis | A few items per screen | Measured [unverified] and convention | https://doi.org/10.1006/ceps.1995.1003, https://clig.dev/ |
| Terminal bold | Bold font on, bold-as-bright off | Convention | https://iterm2.com/documentation-preferences-profiles-text.html |
| CLI colour switches | Honour NO_COLOR, --no-color, TERM=dumb, non-TTY | Standard and convention | https://no-color.org/, https://clig.dev/ |
| CLI error colour | Red, sparingly, with a text label | Convention | https://clig.dev/ |
