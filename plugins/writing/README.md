# writing

Skills for writing text people read on a screen.

| Skill | Fires on |
|---|---|
| `markdown-files` | writing or editing any `.md` file a person reads: "write a README", "write this up", "put this in a doc", "write a brief", "clean up this doc", "make this easier to read" |

## `markdown-files`

Sets the rules for a Markdown file: conclusion first, descriptive headings, short paragraphs, 1 idea per sentence, plain punctuation, rare bold, 1 sentence per source line, and a list of patterns to remove.
It replaces the writing rules that SDLC's hooks used to print into every session.
A skill loads only when a Markdown file is being written, so a session that writes no document pays nothing for the rules.

### Evidence

These results were measured in studies:

* People scan: 79% of test users scanned a page, and 16% read word by word ([NN/g](https://www.nngroup.com/articles/how-users-read-on-the-web/)).
* People read about 20% of a page's words, and each extra 100 words gets about 18% of those words read (45,237 page views, [NN/g](https://www.nngroup.com/articles/how-little-do-users-read/)).
* Rewriting a site to be concise, scannable, and objective raised measured usability by 124% (51 users, [NN/g](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/)).
* When scanning a list, readers see about the first 2 words of each item ([NN/g](https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/)).
* A clause between a subject and its verb hurt recall more than jargon or passive voice did (184 readers, [Martínez, Mollica and Gibson 2022](https://scholarship.law.tamu.edu/facscholar/2400/)).
* Each negation added about 685 ms to checking a sentence ([Clark and Chase 1972](https://web.stanford.edu/~clark/1970s/Clark.Chase.comparing.72.pdf)).
* Judges and lawyers preferred the plain version of legal text 80 to 86% of the time (1,462 readers, [Kimble](https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf)).
* A comma after an introductory clause raised correct readings from 47% to 81% (26 readers, [PMC5023661](https://pmc.ncbi.nlm.nih.gov/articles/PMC5023661/)).
* Bold costs no reading speed. Italics cost 3 to 5% and all capitals 12 to 14% ([Tinker, *Legibility of Print*](https://gwern.net/doc/design/typography/1963-tinker-legibilityofprint.pdf)).
* Raising readability-formula scores raised comprehension in only about half of 36 studies, so the skill sets no formula target ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).

These rules come from style guides or common practice, with no study behind them:

* Sentence length: AR 25-50 sets an average of about 15 words, Cutts's *Oxford Guide to Plain English* sets 15 to 20, and [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/) says to split sentences over 25.
* Paragraphs of at most 5 sentences, conclusion first, and descriptive headings: [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/) and the [US Federal Plain Language Guidelines](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf).
* Semicolons: [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/) bans them, and [Google](https://developers.google.com/style/semicolons) and [Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/semicolons) discourage them. The skill follows GOV.UK.
* Em dashes: [Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/dashes-hyphens/emes) and [Chicago](https://www.chicagomanualofstyle.org/qanda/data/faq/topics/HyphensEnDashesEmDashes/faq0181.html) warn against overuse. The limit of 1 per paragraph is convention.
* Other punctuation: parentheses ([Google](https://developers.google.com/style/parentheses)), the serial comma ([Google](https://developers.google.com/style/commas), Microsoft, and Chicago use it, and AP does not), colons ([Google](https://developers.google.com/style/colons)), exclamation marks ([Google](https://developers.google.com/style/exclamation-points)), quotation marks ([Google](https://developers.google.com/style/quotation-marks)), and ampersands ([GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
* Bold and italics: [Google](https://developers.google.com/style/text-formatting) and [NN/g](https://www.nngroup.com/articles/formatting-long-form-content/).
* Active voice and verbs over nouns made from verbs: every style guide asks for them, but an eye-tracking test of real texts found no effect ([Balling 2018](https://research.cbs.dk/en/publications/no-effect-of-writing-advice-on-reading-comprehension/)).
* 1 sentence per source line: [sembr.org](https://sembr.org/). Table, heading, and fence rules: [markdownlint](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) and the [GFM spec](https://github.github.com/gfm/).

The patterns to remove come from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and measured overuse in model output ([Kobak et al.](https://arxiv.org/abs/2406.07016), [Boggia 2026](https://arxiv.org/abs/2607.21498)).
