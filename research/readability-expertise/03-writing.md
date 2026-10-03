# Writing for screens: sentences, words, punctuation and structure

This brief covers what the evidence says about writing text that is easy to read on a screen.
The target documents are Markdown files that a developer and their AI agents write: READMEs, research briefs, design notes, plans, skill instruction files and chat answers shown in a terminal.

## How to read this brief

* **Evidence labels:** Each recommendation carries one label.
  **measured** means a controlled study or usability test with numbers.
  **standard** means an official style guide says so, and the guide is named.
  **convention** means common practice with no study or official guide behind it.
* **Unverified claims:** A claim marked **[unverified]** comes from a search-result snippet, not from a page I fetched and read.
* **Second-hand claims:** Some numbers come from a fetched page that cites an older source I could not open. Those are marked "second-hand".

## The strongest findings

* **People scan before they read:** In NN/g's 1997 tests, 79% of users scanned each new page and 16% read word by word ([NN/g](https://www.nngroup.com/articles/how-users-read-on-the-web/)).
  A log study of 45,237 page views found people read about 20% of the words on an average page ([NN/g](https://www.nngroup.com/articles/how-little-do-users-read/)).
* **Scannable, concise, plain text tests better:** Rewriting a site to be concise, scannable and objective raised measured usability by 124% in a 51-user study ([NN/g](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/)).
* **Experts prefer plain language too:** 1,462 judges and lawyers in four US states preferred the plain version of legal paragraphs by 80% to 86% ([Kimble, "Writing for Dollars, Writing to Please"](https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf)).
* **Structure inside a sentence matters more than its length:** In contracts, clauses nested inside other clauses hurt recall more than jargon or passive voice did, across 184 participants ([Martínez, Mollica and Gibson 2022](https://scholarship.law.tamu.edu/facscholar/2400/)).
* **Readability scores do not measure what helps readers:** Klare reviewed 36 studies that tried to raise comprehension by raising readability scores, and only about half succeeded ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
* **Bullets can hide reasoning:** The Columbia Accident Investigation Board called NASA's use of slides in place of technical papers "an illustration of the problematic methods of technical communication" ([Tufte](https://www.edwardtufte.com/notebook/columbia-accident-investigation-board-the-boeing-powerpoint-slide/)).
* **AI text has measurable tics:** "Not X, but Y" constructions, bold on every key phrase, em dashes, groups of three and stock words such as "delve" appear in LLM output at rates above human baselines ([Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing); [Kobak et al.](https://arxiv.org/abs/2406.07016); [Boggia 2026](https://arxiv.org/abs/2607.21498)).

## 1. How people read on screens

### Scanning patterns

* **F-pattern:** Readers read across the top, read across a second, shorter line lower down, then scan down the left edge ([NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)).
  NN/g first reported it in 2006 and confirmed it with 47 participants in later eye-tracking studies ([NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)).
* **When the F-pattern happens:** It happens when the text has no bold, bullets or subheadings, the reader wants to finish fast, and the reader is not committed to reading everything ([NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)).
  NN/g treats the F-pattern as a failure mode, because readers who scan this way miss content on the right and lower down ([NN/g](https://www.nngroup.com/articles/layer-cake-pattern-scanning/)).
* **Layer-cake pattern:** Readers fix their eyes mostly on headings and subheadings and dip into body text only where a heading matches their need ([NN/g](https://www.nngroup.com/articles/layer-cake-pattern-scanning/)).
  NN/g calls it "by far the most effective way to scan pages" ([NN/g](https://www.nngroup.com/articles/layer-cake-pattern-scanning/)).
  This pattern only works when the page has headings that describe their sections.
* **Other patterns:** NN/g also names a spotted pattern (hunting for one thing), a commitment pattern (reading almost everything, when motivated) and marking and bypassing patterns ([NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)).

### How much people read

* **About 20% of words:** Weinreich and colleagues logged 25 users' normal browsing, 45,237 page views after cleaning ([NN/g](https://www.nngroup.com/articles/how-little-do-users-read/)).
  Users spent about 25 seconds plus 4.4 seconds per 100 words on a page, which means they read at most 28% of the words and about 20% on average ([NN/g](https://www.nngroup.com/articles/how-little-do-users-read/)).
  Each 100 extra words on a page gets about 18% of those words read ([NN/g](https://www.nngroup.com/articles/how-little-do-users-read/)).
* **Attention stays near the top:** In a 2018 study of 120 participants and over 130,000 fixations, 57% of viewing time went to the first screenful and 74% to the first two screenfuls ([NN/g](https://www.nngroup.com/articles/scrolling-and-attention/)).
* **Screens cost some comprehension for expository text:** A meta-analysis of 54 studies and about 171,000 readers found a small advantage for paper over screen, Hedges' g = −0.21 ([TUM summary of Delgado et al. 2018](https://www.edtech.tum.de/dont-throw-away-your-printed-books-why-reading-performance-is-better-on-paper-than-on-screens/)).
  The gap appeared for expository and informational texts and under time pressure, and not for narrative texts ([TUM](https://www.edtech.tum.de/dont-throw-away-your-printed-books-why-reading-performance-is-better-on-paper-than-on-screens/)).
  READMEs, briefs and plans are expository, so this gap applies to them.

### Concise, scannable, objective

* **The 1997 rewrite study:** NN/g tested five versions of a travel site with 51 experienced web users ([NN/g](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/)).
  Measured usability rose 58% for the concise version, 47% for the scannable version, 27% for the objective (non-promotional) version and 124% for the version that combined all three ([NN/g](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/)).
  Usability combined task time, errors, memory, sitemap time and satisfaction ([NN/g](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/)).
* **Scannable means specific things:** NN/g lists highlighted keywords, meaningful subheadings, bulleted lists, one idea per paragraph, the inverted pyramid, and half the word count of print writing ([NN/g](https://www.nngroup.com/articles/how-users-read-on-the-web/)).

### Front-loading and the inverted pyramid

* **The first two words carry the load:** When scanning a list, users see about the first 2 words or 11 characters of each item ([NN/g](https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/)).
  Label: **measured**.
* **Front-load headings, links and sentences:** NN/g, GOV.UK and Microsoft all tell writers to put the information-carrying words first ([NN/g](https://www.nngroup.com/articles/layer-cake-pattern-scanning/); [GOV.UK clear structure](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/); [Microsoft Top 10 tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)).
  Label: **standard** (GOV.UK, Microsoft), backed by NN/g eye-tracking.
* **Inverted pyramid:** Put the conclusion first and supporting detail after it in falling order of importance ([NN/g](https://www.nngroup.com/articles/inverted-pyramid/)).
  A reader who stops at any point still has the main point ([NN/g](https://www.nngroup.com/articles/inverted-pyramid/)).
  NN/g's inverted-pyramid article cites no numbers of its own, so the support comes from the reading-depth data above.
  Label: **standard** (GOV.UK: "Put the most important information first", [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/)).
* **Bottom line up front:** US Army Regulation 25-50, paragraph 1-38, requires "putting the main point at the beginning of the correspondence (bottom line up front)" and says Army writing must be "understood by the reader in a single rapid reading" ([AR 25-50, mirror at armywriter.com](https://www.armywriter.com/AR25-50.pdf)).
  Label: **standard** (AR 25-50).

## 2. Sentence length and structure

### Sentence length

* **The guidance varies between 15 and 25 words:**
  US Army AR 25-50 sets an average of about 15 words ([AR 25-50](https://www.armywriter.com/AR25-50.pdf)).
  Martin Cutts's *Oxford Guide to Plain English* says to make the average 15 to 20 words over the whole document (second-hand, quoted at [strainindex](https://strainindex.wordpress.com/2008/07/28/the-average-sentence-length/)).
  GOV.UK says to split sentences over 25 words ([GOV.UK clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)).
  Label: **standard**.
* **The US Federal Plain Language Guidelines give no number:** The 2011 guidelines say "Express only one idea in each sentence" and "Write short sentences" but set no word count ([Federal Plain Language Guidelines 2011, section III.b.1](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  I searched the full text and found no "20 words" rule, so attributions of a 20-word average to these guidelines are not supported by the 2011 text.
* **The American Press Institute figures are second-hand:** Writing coach Ann Wylie reports that readers understood 100% of stories with average sentences of 8 words or fewer, 90% at 14 words and under 10% at 43 words, from a study of 410 newspapers ([Wylie](https://www.wyliecomm.com/how-long-should-a-sentence-be/)).
  The page gives no year, author or method, and I could not find the original report.
  Treat these numbers as unconfirmed.
* **A difficulty table from the press associations:** Jyoti Sanyal cites a table that rates 8 words as "very easy", 14 as "fairly easy", 17 as "standard", 21 as "fairly difficult" and 29 or more as "very difficult" (second-hand, at [strainindex](https://strainindex.wordpress.com/2008/07/28/the-average-sentence-length/)).
  This matches the scale Rudolf Flesch published, but I did not see the original ([Flesch, archive.org listing](https://archive.org/details/artofplaintalk0000rudo_p5q2)) **[unverified]**.
* **Length is a symptom:** Redish writes that "long sentences are not a problem just because they are long" and that length goes with other features that make sentences hard ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  Her example: "He is the defendant. He is fifteen years old. He is in his teens. Someone says he stole from the store." reads worse than "The defendant is a fifteen-year old teenager who is accused of shoplifting." ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
* **Nesting costs more than length:** Martínez, Mollica and Gibson compared contract excerpts with and without jargon, center-embedded clauses, passive voice and odd capitalization ([Martínez et al. 2022](https://scholarship.law.tamu.edu/facscholar/2400/)).
  Across 184 participants, each feature lowered recall and comprehension, and center-embedded clauses lowered recall the most ([Martínez et al. 2022](https://scholarship.law.tamu.edu/facscholar/2400/)).
  A center-embedded clause is one placed between a subject and its verb, so the reader holds the subject in memory until the verb arrives.
  Label: **measured**.

### One idea per sentence

* **Split compound ideas:** The Federal guidelines say long sentences with dependent clauses and exceptions lose "the main point in a forest of words" ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  Label: **standard** (Federal Plain Language Guidelines).
* **Keep the relations when you split:** In the Charrows' jury-instruction study, revised instructions raised comprehension but often scored worse on readability formulas, because the revisers added words that showed how the facts related ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  Splitting a sentence helps only when the connecting words ("because", "so", "if") survive the split.
  Label: **measured** (Charrow and Charrow 1979, reported by Redish).

### Subject, verb and word order

* **Put the verb next to its subject:** Gopen and Swan's first principle is "Follow a grammatical subject as soon as possible with its verb" ([Gopen and Swan 1990](https://www.gatsby.ucl.ac.uk/~pel/misc/gopen_swan.pdf)).
  The center-embedding result above is the measured support for this rule.
* **Old information first, new information last:** Gopen and Swan say to place "old information" (already stated) at the start of a sentence for linkage, and the new point you want stressed at the end ([Gopen and Swan 1990](https://www.gatsby.ucl.ac.uk/~pel/misc/gopen_swan.pdf)).
  They also say to "Articulate the action of every clause or sentence in its verb" ([Gopen and Swan 1990](https://www.gatsby.ucl.ac.uk/~pel/misc/gopen_swan.pdf)).
  Label: **convention** (a widely taught model, not a style-guide rule).
* **Given-new evidence:** Haviland and Clark (1974) found that a sentence took less time to understand when its given information had a direct antecedent in the previous sentence than when the reader had to infer the link ([ScienceDirect listing](https://www.sciencedirect.com/science/article/pii/S0022537174800034)) **[unverified]**.
  Label: **measured**.
* **Main idea before exceptions:** The Federal guidelines say to place the main idea before exceptions and conditions ([FPLG 2011, section III.b.4](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  Label: **standard**.

### Active and passive voice

* **The style guides agree:** Google, GOV.UK, the Federal guidelines and AR 25-50 all tell writers to prefer active voice ([Google voice](https://developers.google.com/style/voice); [GOV.UK clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/); [digital.gov](https://digital.gov/guides/plain-language/writing); [AR 25-50](https://www.armywriter.com/AR25-50.pdf)).
  The stated reason is that passive voice hides who does the action ([Google voice](https://developers.google.com/style/voice)).
  Label: **standard**.
* **Passive is allowed when the actor does not matter:** Google allows it to stress the object ("The file is saved"), to play down the subject, and when readers do not need to know the actor ([Google voice](https://developers.google.com/style/voice)).
  Label: **standard** (Google).
* **The measured effect is real but small and depends on context:** Ferreira (2003) found listeners misassigned who-did-what more often in passives, and most often in implausible passives ([review in Frontiers in Psychology 2024](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1323700/full)).
  Later work argues these errors arise when recalling the sentence, not during first reading ([ERIC record for the 2018 replication](https://eric.ed.gov/?id=EJ1187701)) **[unverified]**.
  Balling (2018) changed passives to actives and nominalizations to verbs in four authentic texts and found no difference in eye-tracking with 27 readers ([CBS abstract](https://research.cbs.dk/en/publications/no-effect-of-writing-advice-on-reading-comprehension/)).
  Balling concluded that what matters is how a change supports cohesion and coherence ([CBS abstract](https://research.cbs.dk/en/publications/no-effect-of-writing-advice-on-reading-comprehension/)).
  Label for "prefer active": **standard**, with mixed **measured** support.

### Nominalizations

* **What they are:** A nominalization is a verb turned into a noun that then needs a second, weak verb, such as "make a decision" for "decide" ([digital.gov](https://digital.gov/guides/plain-language/writing)).
  Endings such as -ment, -tion, -sion and -ance flag them ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
* **Evidence:** Spyridakis and Isakson (1998) found that turning nominalizations back into verbs helped native English readers recall the important information, and may not help non-native readers ([ERIC](https://eric.ed.gov/?id=EJ569911)).
  Balling (2018) found no effect in her eye-tracking test ([CBS](https://research.cbs.dk/en/publications/no-effect-of-writing-advice-on-reading-comprehension/)).
  Label: **standard** (Federal guidelines), with mixed **measured** support.

### Negatives and double negatives

* **Negatives take longer:** In Clark and Chase's 1972 experiment, 12 participants checked sentences against pictures ([Clark and Chase 1972](https://web.stanford.edu/~clark/1970s/Clark.Chase.comparing.72.pdf)).
  A negative sentence added an estimated 685 ms to a base time of 1,763 ms ([Clark and Chase 1972](https://web.stanford.edu/~clark/1970s/Clark.Chase.comparing.72.pdf)).
  Label: **measured**.
* **Context lowers the cost:** When a negative answers a question that set it up, such as "Which one isn't peeled?", the extra step disappears ([PMC8660742](https://pmc.ncbi.nlm.nih.gov/articles/PMC8660742/)).
  A negative that denies something the reader never thought costs more than one that answers an expectation.
* **Double negatives:** The Federal guidelines say two negatives require "a mental switch from no to yes", quoting Flesch ([FPLG 2011, section III.b.3](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  They list rewrites: "no fewer than" to "at least", "is not … unless" to "is … only if" ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  They treat an exception to an exception as a double negative ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  Hidden negatives include "unless", "fail to", "except", "other than" and words starting with un- and dis- ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  Label: **standard** (Federal guidelines), with **measured** support for the cost of single negatives.

### Garden-path sentences

* **What they are:** A garden-path sentence is grammatical but leads the reader to a wrong first parse, as in "The horse raced past the barn fell" ([Wikipedia](https://en.wikipedia.org/wiki/Garden-path_sentence)).
  Readers parse word by word and must go back and re-read when the parse fails ([Wikipedia](https://en.wikipedia.org/wiki/Garden-path_sentence)).
* **Fixes:** Keep the relative pronoun ("The horse that was raced…") and use punctuation at clause boundaries ([Wikipedia](https://en.wikipedia.org/wiki/Garden-path_sentence)).
* **A comma after an introductory clause helps:** In an ERP study of 26 readers, sentences with an early comma were judged correctly 81% of the time against 47% without it ([PMC5023661](https://pmc.ncbi.nlm.nih.gov/articles/PMC5023661/)).
  Hill and Murray (2000) found the effect of punctuation on garden paths is large in some structures and absent in others ([Edinburgh listing](https://www.research.ed.ac.uk/en/publications/chapter-22-commas-and-spaces-effects-of-punctuation-on-eye-moveme/)) **[unverified]**.
  Label: **measured**.
* **Developer text has its own garden paths:** Words that are both noun and verb ("build", "test", "run", "log", "cache") create them, as in "Test results cache the build".
  Label: **convention** (my example; no study of developer text found).

## 3. Word choice

### Plain language

* **The rule:** GOV.UK makes plain English mandatory and says to use short, common words, such as "buy" for "purchase" and "help" for "assist" ([GOV.UK clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)).
  The US Plain Writing Act of 2010 requires plain language for public federal content ([digital.gov](https://digital.gov/guides/plain-language)).
  Label: **standard** (GOV.UK, US federal).
* **Experts prefer it:** Kimble's 1987 survey sent six pairs of legal paragraphs, one plain and one traditional, to Michigan judges and lawyers without mentioning plain English ([Kimble](https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf)).
  Across Michigan, Florida, Louisiana and Texas, 1,462 judges and lawyers chose the plain versions by margins of 80% to 86% ([Kimble](https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf)).
  Label: **measured**.
* **Experts judge plain writers more competent:** Benson and Kessler gave 10 California appellate judges and 33 research attorneys plain and legalese versions of brief passages ([Kimble](https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf)).
  They rated the legalese versions "substantively weaker and less persuasive" and guessed that the plain writers came from more prestigious firms ([Kimble](https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf)).
  Label: **measured**.
* **Plain text saves expert time:** 262 naval officers who read a plain business memo answered more questions correctly, read it in 17% to 23% less time, and half as many felt the need to re-read ([Kimble](https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf)).
  Label: **measured**.
* **Lawyers understand plain contracts better:** In two experiments with over 100 lawyers each, recall rose from about 45% for legalese to over 50% for plain versions, and lawyers rated the plain versions higher in quality ([MIT News on Martínez et al., PNAS 2023](https://news.mit.edu/2023/new-study-lawyers-legalese-0529)).
  Label: **measured**.
* **Educated readers prefer plain English most:** Trudeau (2012) found 80% of people preferred the plain version, and the preference rose with education and the complexity of the issue ([GDS blog](https://gds.blog.gov.uk/2014/02/17/guest-post-clarity-is-king-the-evidence-that-reveals-the-desperate-need-to-re-think-the-way-we-write/)).
  97% preferred "among other things" over "inter alia" ([GDS blog](https://gds.blog.gov.uk/2014/02/17/guest-post-clarity-is-king-the-evidence-that-reveals-the-desperate-need-to-re-think-the-way-we-write/)).
  Label: **measured**.

### Jargon

* **Define it or drop it:** GOV.UK says to use specialist terms only when needed and to explain them on first use ([GOV.UK clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)).
  GOV.UK and the Federal guidelines both say to spell out abbreviations on first use ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/); [FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  Label: **standard**.
* **Defining jargon does not remove its cost:** Bullock and colleagues (2019, N = 650) found jargon lowered reported processing fluency even when definitions were given ([ResearchGate listing](https://www.researchgate.net/publication/334738666_Jargon_as_a_barrier_to_effective_science_communication_Evidence_from_metacognition)) **[unverified]**.
  Label: **measured**.
* **Jargon is not the main cost in expert text:** In the contracts study, nesting hurt recall more than low-frequency jargon ([Martínez et al. 2022](https://scholarship.law.tamu.edu/facscholar/2400/)).
  For a developer audience, terms such as "commit" or "endpoint" are ordinary words; terms invented inside one project are the jargon. Label: **convention**.

### Consistent terminology

* **One name per thing:** The Federal guidelines say to use the same term for the same concept throughout, because a new word "may cause the reader to wonder if you are referring to the same group" ([FPLG 2011, section III.a.2.iv](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  They add: "Don't feel that you need to use synonyms to make your writing more interesting" ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  Label: **standard**.
* **Why it matters:** The given-new research suggests a reader who meets a new word must infer that it links back, which takes extra time (Haviland and Clark 1974, [ScienceDirect listing](https://www.sciencedirect.com/science/article/pii/S0022537174800034)) **[unverified]**.

### Concrete words

* **Concrete text is understood and remembered better:** Sadoski, Goetz and Fritz (1993) found concreteness was the variable most related to comprehensibility and recall of sentences and texts ([reference listing](https://www.scirp.org/reference/referencespapers?referenceid=2258530)) **[unverified]**.
  Label: **measured**.
* **Developer form:** Name the file, the command, the number and the error message instead of "the configuration", "the issue" or "performance".
  Label: **convention**, supported by the measured concreteness effect.

### Readability formulas

* **What they count:** Flesch Reading Ease is 206.835 − 1.015 × (words per sentence) − 84.6 × (syllables per word) ([Wikipedia](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)).
  Flesch-Kincaid Grade Level is 0.39 × (words per sentence) + 11.8 × (syllables per word) − 15.59, built for the US Navy in 1975 ([Wikipedia](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)).
  Gunning Fog (1952) is 0.4 × (words per sentence + 100 × share of words with three or more syllables) ([Wikipedia](https://en.wikipedia.org/wiki/Gunning_fog_index)).
  All three count only sentence length and word length.
* **What they miss:** Redish lists content, organization, headings, tables, lists, layout, grammar, and whether readers know the words ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  "I wave my hand" and "I waive my rights" get the same Flesch score ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  Fog counts "interesting" as complex and short rare words as easy ([Wikipedia](https://en.wikipedia.org/wiki/Gunning_fog_index)).
* **They break on lists and Markdown:** Formulas count a sentence from period to period, so a bulleted list without periods scores as one long sentence ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  Code spans, file paths and URLs in developer Markdown will also distort syllable and word counts.
* **They were built for children:** Grade-level formulas were calibrated on school texts, and the acceptance threshold was that 50% of children answered 50% of questions correctly ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
* **Writing to the score does not work:** Klare reviewed 36 studies that tried to raise comprehension by raising readability scores, and only about half succeeded ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  Klare compared writing to the formula to "lighting a match under a thermometer" to warm a room ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  The Government of Canada says rewriting to a lower grade score does not raise understanding, and the 2023 ISO plain language standard excludes formulas ([Our Languages blog](https://our-languages.canada.ca/en/blogue-blog/readability-formulas-eng)).
* **What they are good for:** A poor score is a warning sign that sentences or words are too long ([Redish 2000](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
  Label: **measured** (Klare's review) and **standard** (ISO 24495-1 excludes them, per the Canadian page).

## 4. Punctuation

No controlled study I found tests semicolons, parentheses, exclamation marks or quotation marks for comprehension.
The comma is the exception, through the garden-path work above.
The rest of this section is **standard** guidance.

* **Semicolons:**
  Google says "If possible, avoid using semicolons" and allows them between closely related clauses, before "therefore" and similar words, and in lists of long items ([Google](https://developers.google.com/style/semicolons)).
  Microsoft says sentences with semicolons "are often complex" and suggests breaking them into sentences or a list ([Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/semicolons)).
  GOV.UK says "Do not use semicolons as they are often mis-read" ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
  GOV.UK gives no study for "often mis-read".
* **Em dashes:**
  Google allows an em dash for a break or interruption, with no spaces ([Google](https://developers.google.com/style/dashes)).
  Microsoft allows them but warns that, like colons, semicolons and parentheses, they hurt readability when overused "by interrupting the flow of the text and making sentences overly long and complex" ([Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/dashes-hyphens/emes)).
  The Chicago Manual of Style's Q&A says "Because dashes are so flexible, they tend to be overused. When in doubt, edit them out." ([CMOS Q&A](https://www.chicagomanualofstyle.org/qanda/data/faq/topics/HyphensEnDashesEmDashes/faq0181.html)).
  Google says to use a colon or a period, not a dash, between an item and its description ([Google](https://developers.google.com/style/dashes)).
* **Parentheses:**
  Google says "Don't put important information in parentheses" because "some readers ignore anything that appears in parentheses" ([Google](https://developers.google.com/style/parentheses)).
  Google says to keep a parenthetical short or make it a separate sentence ([Google](https://developers.google.com/style/parentheses)).
  GOV.UK says not to use brackets for optional plurals such as "file(s)" ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
* **Serial (Oxford) comma:**
  Google, Microsoft, Chicago and APA use it; AP and the New York Times do not ([Google](https://developers.google.com/style/commas); [Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/commas); [Wikipedia: Serial comma](https://en.wikipedia.org/wiki/Serial_comma)).
  Google's reason is that it avoids "potentially changing the meaning of the sentence" ([Google](https://developers.google.com/style/commas)).
  A missing serial comma in a Maine overtime law led to O'Connor v. Oakhurst Dairy, settled for $5 million in 2017 ([Wikipedia](https://en.wikipedia.org/wiki/Serial_comma)).
  The serial comma can also create ambiguity, as in "my mother, Mother Teresa, and the pope" ([Wikipedia](https://en.wikipedia.org/wiki/Serial_comma)).
  Microsoft suggests a bulleted list when a series has more than three items or long items ([Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/commas)).
* **Colons:**
  Google says a colon "indicates that closely-related information follows" and that the text before a colon that introduces a list must be a complete sentence ([Google](https://developers.google.com/style/colons)).
  Google lowercases the first word after a colon in most cases ([Google](https://developers.google.com/style/colons)).
  Microsoft says not to end headings with a period or colon ([Microsoft Top 10 tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)).
* **Exclamation marks:**
  Google says never to use them in concept and reference docs, because they "can appear unprofessional, alarming, or translate poorly" ([Google](https://developers.google.com/style/exclamation-points)).
  Microsoft says "Use exclamation points sparingly. Save them for when they count." ([Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/exclamation-points)).
* **Quotation marks:**
  Google uses straight quotes everywhere in developer docs, because code requires them ([Google](https://developers.google.com/style/quotation-marks)).
  Google says not to use scare quotes and not to combine quotation marks with code font ([Google](https://developers.google.com/style/quotation-marks)).
  GOV.UK uses double quotes only for direct quotations ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
* **Ampersands:** GOV.UK says use "and" rather than "&" ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
  Microsoft says not to use "&" or "+" in headings ([Microsoft headings](https://learn.microsoft.com/en-us/style-guide/scannable-content/headings)).

## 5. Document structure

### Headings

* **Descriptive beats clever:** NN/g says a subheading should describe "all topics in the section, and only topics in the section", lead with the important words, and be clear rather than clever ([NN/g layer-cake](https://www.nngroup.com/articles/layer-cake-pattern-scanning/)).
  GOV.UK says to avoid generic headings such as "Introduction" ([GOV.UK clear structure](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/)).
  Google says to use descriptive headings because they help navigation ([Google headings](https://developers.google.com/style/headings)).
  Label: **standard**, backed by NN/g eye-tracking.
* **How many levels:** The Federal guidelines say to limit levels to three or fewer, because readers lose track of where they are with more ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  GOV.UK uses H1 for the page title and H2 to H4 for content ([GOV.UK clear structure](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/)).
  Microsoft says "One heading level is usually plenty for a page or two of content", and to skip second-level headings when a section lacks two distinct topics ([Microsoft headings](https://learn.microsoft.com/en-us/style-guide/scannable-content/headings)).
  Google says not to skip levels and to use one H1 per page ([Google headings](https://developers.google.com/style/headings)).
  Label: **standard**.
* **No empty headings:** Google says headings must be followed by content ([Google headings](https://developers.google.com/style/headings)).
  Microsoft says two headings in a row "might indicate a problem with organization", and not to add filler to separate them ([Microsoft headings](https://learn.microsoft.com/en-us/style-guide/scannable-content/headings)).
  Label: **standard**.
* **Form:** Google and Microsoft use sentence case and no end punctuation in headings ([Google headings](https://developers.google.com/style/headings); [Microsoft Top 10 tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)).
  Google starts task headings with a bare verb ("Create an instance") and conceptual headings with a noun phrase ([Google headings](https://developers.google.com/style/headings)).
  Label: **standard**.
* **Question headings are disputed:** The Federal guidelines call question headings "the most useful type of heading" when you know the reader's questions ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  GOV.UK says not to use them, because they are hard to front-load ([GOV.UK clear structure](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/)).

### Summary first

* **Open with the answer:** GOV.UK puts a summary at the top and says not to repeat it in the first paragraph ([GOV.UK clear structure](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/)).
  NN/g found summaries at the top let readers decide quickly whether the article is relevant ([NN/g long-form formatting](https://www.nngroup.com/articles/formatting-long-form-content/)).
  NN/g's F-pattern advice is to put the most important points in the first two paragraphs ([NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)).
  Label: **standard** (GOV.UK, AR 25-50), supported by **measured** reading-depth data.

### Paragraphs

* **Length:** The Federal guidelines cite a limit of 150 words in three to eight sentences, and never more than 250 words ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  GOV.UK sets no more than 5 sentences ([GOV.UK clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)).
  AR 25-50 sets no more than 10 lines ([AR 25-50](https://www.armywriter.com/AR25-50.pdf)).
  NN/g says one idea per paragraph ([NN/g](https://www.nngroup.com/articles/how-users-read-on-the-web/)).
  Label: **standard**.
* **One topic per paragraph:** The Federal guidelines say to cover only one topic in each paragraph and allow an occasional one-sentence paragraph ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  Label: **standard**.

### Lists versus paragraphs

* **Lists help scanning:** The scannable version in NN/g's 1997 test, which used bulleted lists, scored 47% higher ([NN/g](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/)).
  Label: **measured**.
* **When to use which list:** Google uses numbered lists for sequences, bulleted lists for non-sequential items and description lists for terms with explanations ([Google lists](https://developers.google.com/style/lists)).
  Google says a single item is not a list ([Google lists](https://developers.google.com/style/lists)).
  Microsoft sets at least two and, if possible, no more than seven items ([Microsoft lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists)).
  Both require parallel structure, such as every item starting with a verb ([Google lists](https://developers.google.com/style/lists); [Microsoft lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists)).
  Google says to introduce a list with a complete sentence ([Google lists](https://developers.google.com/style/lists)).
  Label: **standard**.
* **Lists hide reasoning:** The Columbia Accident Investigation Board was "surprised to receive similar presentation slides from NASA officials in place of technical reports" and called this "an illustration of the problematic methods of technical communication at NASA" ([Tufte](https://www.edwardtufte.com/notebook/columbia-accident-investigation-board-the-boeing-powerpoint-slide/)).
  Tufte's analysis of the Boeing slide shows the key uncertainty buried at a low bullet level ([Tufte](https://www.edwardtufte.com/notebook/columbia-accident-investigation-board-the-boeing-powerpoint-slide/)).
  Tufte argues that bullet outlines leave out the narrative between points and so hide the causal links ([search summary of *The Cognitive Style of PowerPoint*](https://www.edwardtufte.com/notebook/new-edition-of-the-cognitive-style-of-powerpoint/)) **[unverified]**.
  Jeff Bezos banned slides at Amazon in 2004, writing that "the narrative structure of a good memo forces better thought and better understanding of what's more important than what, and how things are related" ([Slab blog](https://slab.com/blog/jeff-bezos-writing-management-strategy/)) **[unverified]**.
  Label: **convention**, supported by one accident-board finding.
* **Resolution:** Use a list for parallel, independent items and steps.
  Use a paragraph when each point depends on the one before, because the words "because", "so" and "unless" carry the logic and a list has no place for them.
  Label: **convention**, consistent with Google, Microsoft and the CAIB finding.

### Tables

* **Use a table for comparisons with two dimensions:** The Federal guidelines say to use tables "to make complex material easier to understand", and show if-then tables for rules with several conditions ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
  digital.gov says to use tables "to make complex relationships clear" ([digital.gov design](https://digital.gov/guides/plain-language/design)).
  Label: **standard**.
* **Do not use a table for one dimension:** Wikipedia lists small tables that "could be better represented as prose" as a sign of AI writing ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  Microsoft offers a term list as the alternative for a set of terms and definitions ([Microsoft lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists)).
  Label: **convention**.

### Chunking

* **Small units with white space:** NN/g recommends short paragraphs separated by white space, clear visual hierarchy, contrasting headings and lists ([NN/g chunking](https://www.nngroup.com/articles/chunking/)).
  NN/g warns that Miller's "seven plus or minus two" is often misapplied to content ([NN/g chunking](https://www.nngroup.com/articles/chunking/)).
  Label: **standard** (NN/g guidance).

### Link text

* **Describe the destination:** Google says link text should be short, unique and descriptive, and should never be "click here", "this document" or "this article" ([Google link text](https://developers.google.com/style/link-text)).
  Screen-reader users jump from link to link without the words between ([Google link text](https://developers.google.com/style/link-text)).
  NN/g says people mostly look at the first 2 words of a link ([NN/g writing links](https://www.nngroup.com/articles/writing-links/)).
  Label: **standard** (Google), backed by NN/g eye-tracking.

### Numbers

* **NN/g: always numerals online:** Write "23", not "twenty-three", even at the start of a sentence, because numerals attract fixations while users scan ([NN/g](https://www.nngroup.com/articles/web-writing-show-numbers-as-numerals/)).
  Exceptions are vague amounts ("thousands") and numbers in the billions ("24 billion") ([NN/g](https://www.nngroup.com/articles/web-writing-show-numbers-as-numerals/)).
  Label: **measured** (eye-tracking observation, no effect size given).
* **The style guides differ:** Google spells out zero to nine except for versions, technical quantities, steps and mixed sets ([Google numbers](https://developers.google.com/style/numbers)).
  GOV.UK uses numerals for everything except "one" ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
  For technical Markdown, Google's own exceptions cover most numbers, so numerals are the default in practice.

## 6. Bold and italics inside prose

* **Google:** Bold is for UI elements and run-in headings only ([Google text formatting](https://developers.google.com/style/text-formatting)).
  Italics are for introducing or defining terms, and for emphasis when needed, but "usually, your words can carry the emphasis without adding italics" ([Google text formatting](https://developers.google.com/style/text-formatting)).
  Label: **standard** (Google).
* **Microsoft:** Italic is allowed "sparingly for emphasis", and for the first mention of a new term that is defined right away ([Microsoft formatting](https://learn.microsoft.com/en-us/style-guide/text-formatting/formatting-common-text-elements)).
  Bold is used for the term in a term list, which Microsoft calls an exception to "the general guideline of using italic for emphasis" ([Microsoft lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists)).
  Label: **standard** (Microsoft).
* **GOV.UK:** "Only use bold to indicate interface elements in text that are explicitly telling the user what to do" and "Do not use italics" ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
  Label: **standard** (GOV.UK).
* **NN/g:** NN/g recommends bolding important words to help scanning ([NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)).
  It also says to bold "selectively and sparingly", to keep highlighted text to no more than 30% of an article, and not to bold "to strengthen your tone, as it can slow down scanning and cause confusion" ([NN/g long-form formatting](https://www.nngroup.com/articles/formatting-long-form-content/)).
  The 30% cap comes from a qualitative usability study, not an experiment.
* **Why less bold works better:** Martin Fowler writes that "the more a writer uses typographical emphasis, the less power it has" and keeps bold for headings, a new term at the point it is explained, and a rare key sentence ([Fowler](https://martinfowler.com/bliki/ExcessiveBold.html)).
  Label: **convention**.
* **All capitals and underline:** digital.gov says all capitals make text harder to read, and that readers expect underlined text online to be a link ([digital.gov design](https://digital.gov/guides/plain-language/design)).
  Label: **standard**.
* **Summary:** Bold works as a signal only when it is rare.
  The official guides limit bold to UI labels, run-in headings and defined terms, and use italics, if anything, for emphasis.

## 7. Patterns that make AI-generated text tiring to read

### What the evidence shows LLMs do

* **Stock vocabulary:** Kobak and colleagues tracked over 15 million PubMed abstracts from 2010 to 2024 and found an abrupt rise in style words after LLMs appeared ([Kobak et al.](https://arxiv.org/abs/2406.07016)).
  They estimate at least 13.5% of 2024 abstracts were processed with LLMs, up to 40% in some subsets ([Kobak et al.](https://arxiv.org/abs/2406.07016)).
  Juzek and Ward found 21 such words, including "delve", "intricate" and "underscore", and found evidence consistent with RLHF (training on human preference ratings) causing the overuse ([Juzek and Ward](https://arxiv.org/abs/2412.11385)).
* **The words change by model generation:** Wikipedia lists "delve", "tapestry", "testament" and "pivotal" for GPT-4 (2023 to mid-2024), and "enhance", "highlighting" and "showcasing" from mid-2025 ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  A list of banned words goes out of date as models change.
* **Avoiding "is" and "has":** LLMs replace "is" with "serves as", "marks" or "functions as", and "has" with "features", "offers" or "boasts" ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  Wikipedia cites a study that found use of "is" and "are" in academic writing fell over 10% in 2023 (Geng and Trotta, [arXiv 2404.08627](https://arxiv.org/abs/2404.08627), as reported by [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
* **"Not X, but Y":** LLMs overuse "It's not X, it's Y", "not only X but also Y" and "no X, no Y, just Z" ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  Boggia (2026) measured this figure, called epanorthosis, at about twice the human rate in speech-like text, and at human rates in journalism and encyclopedic prose ([Boggia](https://arxiv.org/abs/2607.21498)).
  Boggia traces it to promotional training text and preference tuning, and found a one-line instruction cut it by 50% to 75% ([Boggia](https://arxiv.org/abs/2607.21498)).
* **Groups of three:** LLMs overuse "adjective, adjective, adjective" and "phrase, phrase, and phrase" to make a thin analysis look complete ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
* **Bold everywhere:** LLMs bold every instance of chosen phrases "in a 'key takeaways' fashion", a habit Wikipedia traces to READMEs, how-tos, slide decks and listicles ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
* **Inline-header lists:** LLMs write lists where each item starts with a bold label, then a colon, then the text ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  This format is close to Microsoft's term list, which is standard for terms and definitions ([Microsoft lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists)).
  The problem is using it for content that is not a set of terms.
* **Em dashes:** LLM output uses em dashes more often than non-professional human writing of the same genre, often to punch up a clause ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  Wikipedia reports a July 2026 Economist study finding that among current models only Claude used em dashes more than professional writers ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), citing [The Economist](https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing)) **[unverified]**.
* **Heading habits:** LLMs repeat the title as the first heading, use title case, add headings with no text under them, skip heading levels, overuse top-level headings, and add horizontal rules between sections ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
* **Tables for small data:** LLMs make small tables that would read better as a sentence ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
* **Puffery and vague analysis:** LLMs add claims of significance ("pivotal moment", "evolving landscape"), participle phrases that comment on meaning ("highlighting", "ensuring", "contributing to"), and vague attributions ("experts argue") ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
* **Chat residue:** Text written as correspondence ends up in documents, such as "In this section, we will discuss…" or offers to help further ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
* **Length:** Singhal and colleagues found that much of the reward gain in RLHF came from longer responses, and that a reward based on length alone reproduced most of the gain ([Singhal et al.](https://arxiv.org/abs/2310.03716)).
  Training therefore pushes models toward longer answers whether or not length helps the reader.

### Why these patterns tire readers

* **Generic text carries less information:** Wikipedia's explanation is that LLMs predict the most likely next words and so "regress to the mean", replacing specific facts with generic, positive descriptions ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  The reader spends the same reading time and gets fewer facts; the concreteness research above predicts lower comprehension and recall for such text.
* **"Not X, but Y" makes the reader process a negation:** Each construction adds a negated clause, and negation added about 685 ms per sentence in Clark and Chase's task ([Clark and Chase 1972](https://web.stanford.edu/~clark/1970s/Clark.Chase.comparing.72.pdf)).
  The cost is highest when the reader never held the denied view, because the negation answers no expectation ([PMC8660742](https://pmc.ncbi.nlm.nih.gov/articles/PMC8660742/)).
* **Bold on every phrase removes the signal:** Bold helps scanning only when it marks a few points ([NN/g](https://www.nngroup.com/articles/formatting-long-form-content/); [Fowler](https://martinfowler.com/bliki/ExcessiveBold.html)).
  Bolding for tone "can slow down scanning and cause confusion" ([NN/g](https://www.nngroup.com/articles/formatting-long-form-content/)).
* **Lists of labelled fragments drop the logic:** A list item has no room for "because" or "so", which is the CAIB and Tufte objection to bullet outlines ([Tufte](https://www.edwardtufte.com/notebook/columbia-accident-investigation-board-the-boeing-powerpoint-slide/)).
* **Em dashes interrupt:** Microsoft says overused dashes interrupt the flow and make sentences long and complex ([Microsoft](https://learn.microsoft.com/en-us/style-guide/punctuation/dashes-hyphens/emes)).
* **Length costs reading depth:** Each extra 100 words on a page gets about 18% of those words read ([NN/g](https://www.nngroup.com/articles/how-little-do-users-read/)).
  Padding pushes the useful sentences below the first screenful, where attention drops ([NN/g](https://www.nngroup.com/articles/scrolling-and-attention/)).
* **Synonym cycling breaks reference:** Changing the name of a thing to vary the prose makes the reader ask whether it is the same thing ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf)).
* **Caveat from Wikipedia:** The page says these patterns are "only potential signs of a problem, not the problem itself" and asks editors not to just remove the signs ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  Removing em dashes from an empty paragraph leaves an empty paragraph; the fix is specific content.

## Where the sources disagree

* **Italics:** Google and Microsoft allow italics for emphasis; GOV.UK bans italics ([Google](https://developers.google.com/style/text-formatting); [Microsoft](https://learn.microsoft.com/en-us/style-guide/text-formatting/formatting-common-text-elements); [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
* **Bold for key words:** NN/g recommends bolding key words; Google and GOV.UK restrict bold to UI elements and run-in headings ([NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/); [Google](https://developers.google.com/style/text-formatting); [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
* **Question headings:** The Federal guidelines favour them; GOV.UK forbids them ([FPLG 2011](https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf); [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/)).
* **Numbers under 10:** NN/g and GOV.UK use numerals; Google spells out zero to nine outside technical contexts ([NN/g](https://www.nngroup.com/articles/web-writing-show-numbers-as-numerals/); [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/); [Google](https://developers.google.com/style/numbers)).
* **Serial comma:** Google, Microsoft and Chicago use it; AP and the New York Times do not ([Wikipedia](https://en.wikipedia.org/wiki/Serial_comma)).
* **Passive voice and nominalizations:** Every guide says to avoid them, but Balling's eye-tracking test found no effect in authentic texts ([CBS](https://research.cbs.dk/en/publications/no-effect-of-writing-advice-on-reading-comprehension/)).
* **Sentence length limits:** 15, 15 to 20, and 25 words are all in use, and no fetched controlled study sets a threshold ([AR 25-50](https://www.armywriter.com/AR25-50.pdf); [strainindex](https://strainindex.wordpress.com/2008/07/28/the-average-sentence-length/); [GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)).

## Open questions for this project

* **Terminal rendering:** I found no study of how Markdown renders in a terminal, or of how readers scan chat answers there.
  Test this by rendering sample answers in the terminal the developer uses and checking whether bold, tables and nested lists display.
* **AI readers:** Skill instruction files are read by models as well as people.
  None of the sources here test how models follow instructions written in each style; a separate brief should cover that.

## Checklist

* **Put the answer first:** State the conclusion, decision or blocker in the first sentence or paragraph. **standard** (GOV.UK, AR 25-50), with **measured** reading-depth support from NN/g.
* **Front-load every heading, list item, link and sentence:** Place the information-carrying words in the first two words. **measured** (NN/g eye-tracking: about 2 words or 11 characters seen).
* **Write descriptive headings:** Make each heading describe all and only what its section covers, with no clever or generic labels. **standard** (Google, GOV.UK), backed by NN/g layer-cake findings.
* **Keep heading depth to three levels:** Use H1 once, do not skip levels, and do not stack headings with no text between them. **standard** (Federal Plain Language Guidelines, Google, Microsoft).
* **Express one idea per sentence:** Split a sentence when it carries two claims, and keep the connecting word ("because", "so", "unless") when you split. **standard** (Federal Plain Language Guidelines), with **measured** support from Charrow and Charrow.
* **Keep the average sentence near 15 to 20 words:** Split sentences over 25 words. **standard** (AR 25-50, Cutts, GOV.UK); no controlled study sets the number.
* **Place the verb next to its subject:** Move clauses that sit between subject and verb to the end or into their own sentence. **measured** (Martínez et al. 2022: center-embedding hurt recall most).
* **Start with known information and end with the new point:** Link each sentence back through its opening words. **convention** (Gopen and Swan), with **measured** support from given-new research **[unverified]**.
* **Prefer active voice:** Name who does the action, and use passive only when the actor does not matter. **standard** (Google, GOV.UK, AR 25-50); **measured** evidence is mixed.
* **Use verbs instead of nouns made from verbs:** Write "decide", not "make a decision". **standard** (Federal Plain Language Guidelines); **measured** evidence is mixed.
* **State things positively:** Remove double negatives and exceptions to exceptions, and use a negative only to answer an expectation the reader holds. **measured** (Clark and Chase: about 685 ms per negation) and **standard** (Federal Plain Language Guidelines).
* **Avoid garden paths:** Keep "that" in relative clauses, put a comma after an introductory clause, and avoid noun-verb words that invite a wrong parse. **measured** (comma: 81% vs 47% correct).
* **Use short common words:** Choose "use", "buy", "help" and "is" over "utilize", "purchase", "assist" and "serves as". **standard** (GOV.UK), with **measured** support from expert-preference studies (80% to 86%).
* **Define each project-specific term once:** Say what a local name means on first use, and spell out abbreviations. **standard** (GOV.UK, Federal Plain Language Guidelines).
* **Keep one name per thing:** Do not swap synonyms for variety. **standard** (Federal Plain Language Guidelines).
* **Name concrete things:** Give the file, command, number or error message instead of an abstract noun. **measured** (Sadoski et al. 1993 **[unverified]**) and **convention**.
* **Ignore readability scores as targets:** Use a poor score only as a warning sign, and test with real readers instead. **measured** (Klare's review of 36 studies) and **standard** (ISO 24495-1 excludes formulas).
* **Avoid semicolons:** Split into two sentences or a list. **standard** (Google, Microsoft, GOV.UK).
* **Limit em dashes:** Use a comma, colon, parentheses or a new sentence first, and use no more than one dash pair per paragraph. **standard** (Microsoft, Chicago Q&A: "When in doubt, edit them out"); the per-paragraph limit is **convention**.
* **Keep important facts out of parentheses:** Put them in the main sentence. **standard** (Google).
* **Use the serial comma:** Put a comma before "and" or "or" in a series of three or more. **standard** (Google, Microsoft, Chicago).
* **Drop exclamation marks and scare quotes:** Use periods, and use code font for literal strings. **standard** (Google, Microsoft).
* **Use a list only for parallel items or steps:** Use a numbered list for sequences, a bulleted list for independent items, and a paragraph when points depend on each other. **standard** (Google, Microsoft) and **convention** (CAIB, Tufte).
* **Use a table only for two-dimensional data:** Write a sentence instead of a two-row table. **standard** (Federal Plain Language Guidelines) and **convention** (Wikipedia AI signs).
* **Keep paragraphs to one topic and about five sentences:** Use an occasional one-sentence paragraph when it helps. **standard** (GOV.UK, Federal Plain Language Guidelines, AR 25-50).
* **Write link text that names the destination:** Never write "click here" or "this document". **standard** (Google), with **measured** support from NN/g.
* **Write numbers as numerals:** Use digits for counts, versions, sizes and steps. **measured** (NN/g eye-tracking) and **standard** (GOV.UK, Google's technical exceptions).
* **Reserve bold:** Bold UI labels, run-in headings and a term at its definition, and nothing for tone. **standard** (Google, GOV.UK, Microsoft) and **measured** (NN/g usability study).
* **Use italics rarely:** Italicize a new term at its definition, and let the words carry emphasis. **standard** (Google, Microsoft).
* **Cut LLM stock patterns at the source:** Replace "not X, but Y", groups of three, "serves as", puffery and chat residue with the specific fact they stand in for. **measured** (Boggia 2026; Kobak et al.; Juzek and Ward) and **convention** (Wikipedia).
* **Cut length that carries no fact:** Each extra 100 words gets about 18% of those words read. **measured** (NN/g, Weinreich et al.).

## Sources

* NN/g, F-shaped pattern: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
* NN/g, layer-cake pattern: https://www.nngroup.com/articles/layer-cake-pattern-scanning/
* NN/g, how little users read: https://www.nngroup.com/articles/how-little-do-users-read/
* NN/g, how users read on the web: https://www.nngroup.com/articles/how-users-read-on-the-web/
* NN/g, concise, scannable and objective: https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/
* NN/g, inverted pyramid: https://www.nngroup.com/articles/inverted-pyramid/
* NN/g, first 2 words: https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/
* NN/g, scrolling and attention: https://www.nngroup.com/articles/scrolling-and-attention/
* NN/g, formatting long-form content: https://www.nngroup.com/articles/formatting-long-form-content/
* NN/g, chunking: https://www.nngroup.com/articles/chunking/
* NN/g, writing links: https://www.nngroup.com/articles/writing-links/
* NN/g, numbers as numerals: https://www.nngroup.com/articles/web-writing-show-numbers-as-numerals/
* Federal Plain Language Guidelines 2011: https://ies.ed.gov/ncee/rel/regions/central/pdf/CE5.3.2-Federal-Plain-Language-Guidelines.pdf
* digital.gov plain language: https://digital.gov/guides/plain-language/writing and https://digital.gov/guides/plain-language/design
* GOV.UK clear language: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
* GOV.UK clear structure: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/
* GOV.UK A to Z style guide: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
* GDS blog, Clarity is King: https://gds.blog.gov.uk/2014/02/17/guest-post-clarity-is-king-the-evidence-that-reveals-the-desperate-need-to-re-think-the-way-we-write/
* Google developer documentation style guide: https://developers.google.com/style/ (pages: semicolons, dashes, parentheses, commas, colons, exclamation-points, quotation-marks, text-formatting, headings, lists, link-text, numbers, voice)
* Microsoft Writing Style Guide: https://learn.microsoft.com/en-us/style-guide/ (pages: top-10-tips-style-voice, punctuation/semicolons, punctuation/dashes-hyphens/emes, punctuation/commas, punctuation/exclamation-points, text-formatting/formatting-common-text-elements, scannable-content/headings, scannable-content/lists)
* Chicago Manual of Style Q&A on em dashes: https://www.chicagomanualofstyle.org/qanda/data/faq/topics/HyphensEnDashesEmDashes/faq0181.html
* US Army AR 25-50 (mirror): https://www.armywriter.com/AR25-50.pdf
* Kimble, Writing for Dollars, Writing to Please: https://www.editorsoftware.com/wp-content/uploads/2021/03/kimble-writing-for-dollars-plain-english.pdf
* Martínez, Mollica and Gibson 2022: https://scholarship.law.tamu.edu/facscholar/2400/
* MIT News on Martínez et al. 2023: https://news.mit.edu/2023/new-study-lawyers-legalese-0529
* Redish 2000, readability formulas: https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf
* Government of Canada, readability formulas: https://our-languages.canada.ca/en/blogue-blog/readability-formulas-eng
* Wikipedia, Flesch-Kincaid: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
* Wikipedia, Gunning fog index: https://en.wikipedia.org/wiki/Gunning_fog_index
* Wikipedia, garden-path sentence: https://en.wikipedia.org/wiki/Garden-path_sentence
* Wikipedia, serial comma: https://en.wikipedia.org/wiki/Serial_comma
* Wikipedia, Signs of AI writing: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
* Gopen and Swan 1990: https://www.gatsby.ucl.ac.uk/~pel/misc/gopen_swan.pdf
* Clark and Chase 1972: https://web.stanford.edu/~clark/1970s/Clark.Chase.comparing.72.pdf
* Negation in context: https://pmc.ncbi.nlm.nih.gov/articles/PMC8660742/
* Commas and garden paths, ERP study: https://pmc.ncbi.nlm.nih.gov/articles/PMC5023661/
* Passive comprehension review: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1323700/full
* Balling 2018: https://research.cbs.dk/en/publications/no-effect-of-writing-advice-on-reading-comprehension/
* Spyridakis and Isakson 1998: https://eric.ed.gov/?id=EJ569911
* Delgado et al. 2018, via TUM: https://www.edtech.tum.de/dont-throw-away-your-printed-books-why-reading-performance-is-better-on-paper-than-on-screens/
* Tufte on the CAIB slide: https://www.edwardtufte.com/notebook/columbia-accident-investigation-board-the-boeing-powerpoint-slide/
* Fowler, Excessive Bold: https://martinfowler.com/bliki/ExcessiveBold.html
* Kobak et al.: https://arxiv.org/abs/2406.07016
* Juzek and Ward: https://arxiv.org/abs/2412.11385
* Boggia 2026: https://arxiv.org/abs/2607.21498
* Singhal et al.: https://arxiv.org/abs/2310.03716
* Wylie on sentence length: https://www.wyliecomm.com/how-long-should-a-sentence-be/
* Strainindex on average sentence length: https://strainindex.wordpress.com/2008/07/28/the-average-sentence-length/
