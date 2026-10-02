---
name: markdown-files
description: "Use this skill whenever you write or edit a Markdown file a person will read: a README, a research brief, a design doc, a plan, notes, an ADR, a SKILL.md, AGENTS.md, or any other .md file. Use it on: 'write a README', 'write this up', 'put this in a doc', 'write a brief', 'save this as markdown', 'clean up this doc', 'make this easier to read'. Load it before writing the first line. Sets the structure, sentence, punctuation, emphasis, and Markdown-source rules that make a file easy to scan on a screen, in a terminal, in an editor preview, and in Obsidian."
license: MIT
compatibility: any-agent
metadata:
  version: "0.1.0"
---

# Markdown files

Readers scan before they read.
In eye-tracking tests, 79% of readers scanned a page, and 16% read it word by word.
In a log study of 45,237 page views, people read about 20% of a page's words.
Each extra 100 words got about 18% of those words read.
Write so that a reader who reads only the headings and the first paragraph still gets the point.

## Structure

* **Conclusion first:** put the conclusion, decision, or answer in the first paragraph.
  Put the supporting detail after it.
* **Front-load:** put the words that carry the information first in every heading, list item, link, and sentence.
  When scanning a list, readers see about the first 2 words of each item.
* **Headings:** use 1 `#` title, then `##` and `###`.
  Skip no level, and leave no heading without text under it.
  Make each heading name what its section covers, in sentence case, with no end punctuation.
  Do not repeat the title as the first heading, and use no bold line as a heading.
* **Section breaks:** separate sections with headings, not horizontal rules.
* **Paragraphs:** keep a paragraph to 1 topic and at most 5 sentences.
* **Lists:** use a numbered list for steps and a bulleted list for parallel items.
  Start every item in a list the same way, such as with a verb.
  Introduce a list with a complete sentence, and write no list of 1 item.
  Nest at most 2 levels, and use 1 bullet marker per file.
* **List or paragraph:** use a paragraph when one point depends on another.
  A list item has no room for the "because" or "so" that links it to the next.
* **Rule lists:** format a list of rules or terms as `* **Lead:** text.`
  Use plain bullets for every other list.
* **Tables:** use a table only for data with 2 dimensions, in at most 4 short columns.
  Put sentence-length comparisons, long paths, and URLs in a list instead, because they wrap badly in cells.
  Give every row the same number of cells, and write a `|` inside a cell as `\|`, even inside code.
  Terminal renderers wrap wide tables or stack them into `Header: value` lines.
* **Callouts:** use at most 2 per file.
  When the file must render everywhere, use only GitHub's `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, and `CAUTION`, unnested.
* **Numbers:** write numbers as numerals: "3 files", "2 levels".
* **Links:** make link text name the destination.
  Never write "click here" or "this document".
* **Length:** cut every sentence that carries no fact.

## Sentences and words

* **One idea per sentence:** split a sentence that makes 2 claims.
  Keep the "because", "so", or "unless" when you split it.
* **Verb next to its subject:** move a clause that sits between a subject and its verb.
  Put it at the end of the sentence or in a sentence of its own.
* **Main idea before exceptions:** state the rule first, then its conditions and exceptions.
* **Positive statements:** state what is true, with no double negatives or exceptions to exceptions.
  Use a negative only to answer something the reader expects.
* **Sentence length:** aim for an average of 15 to 20 words, and split sentences over 25.
* **Common words:** write "use", "help", "is", and "has" over "utilize", "assist", "serves as", and "features".
* **Verbs over nouns made from verbs:** write "decide", not "make a decision".
* **One name per thing:** call a thing by the same name every time.
  A new word makes the reader ask whether it is a new thing.
* **Defined terms:** define each name local to the project the first time it appears.
  Spell out each abbreviation on first use.
* **Concrete nouns:** name the file, command, number, or error message.
* **Active voice:** name who does the action, unless the actor does not matter.
  The measured benefit is small, so do not bend a sentence to get it.
* **No garden paths:** keep "that" in relative clauses.
  Do not open a sentence with a word that reads as noun or verb, such as "test", "build", "run", "log", or "cache", when the wrong reading fits.
* **No formula targets:** do not rewrite to raise a readability score.
  Raising scores raised comprehension in only about half of the studies that tried it.

## Punctuation

* **Serial comma:** put a comma before "and" or "or" in a series of 3 or more: "tests, docs, and config".
  Without it, the last 2 items can read as a pair.
* **Introductory comma:** put a comma after an introductory clause: "When the test fails, the hook blocks the commit."
  In 1 study, correct readings rose from 47% to 81% with the comma.
* **Semicolons:** do not use them.
  Split the clauses into 2 sentences, or the items into a list.
* **Em dashes:** use a comma, a colon, or a new sentence first.
  Allow at most 1 dash or dash pair per paragraph, with no spaces around it.
* **Parentheses:** keep important facts out of them, because some readers skip them.
  Keep a parenthetical to a few words, or make it its own sentence.
  Write "files", not "file(s)".
* **Colons:** make the text before a colon that introduces a list a complete sentence.
  Lowercase the word after a colon unless it is a proper noun or code.
* **Item and description:** separate a list item's lead from its description with a colon or a period, not a dash.
* **Exclamation marks:** do not use them.
* **Quotation marks:** use straight quotes, and only for a direct quotation or exact text the reader will see.
  Use no scare quotes.
  Put commands, file names, keys, and literal strings in code font, never in quotes, and never both.
* **Ampersands:** write "and", not "&" or "+", in headings too.

## Emphasis

* **Bold:** bold only a term where it is defined, the lead of a rule or term in a list, or 1 key sentence.
  Never bold for tone, because bold works only when it is rare.
* **Italics:** use them only for a new term at its definition, never for emphasis.
  Italic text reads 3 to 5% slower than roman.
* **Capitals:** write no all-caps prose.
  All-caps text reads 12 to 14% slower.

## Markdown source

* **One sentence per line:** a 1-sentence edit then changes 1 line in a diff.
  In a list item, put each further sentence on its own line, indented to the item's text.
  A single line break renders as a space on GitHub pages and in most previews.
  It renders as a line break in GitHub comments, in Obsidian with "Strict line breaks" off, and in VS Code with `markdown.preview.breaks` on.
* **Hard line breaks:** end the line with a backslash, not 2 trailing spaces.
* **Code fences:** tag every fence with a language, such as `bash`, `json`, or `text`.
* **Blank lines:** put a blank line before and after every heading, list, table, and code block.
* **Nesting:** indent nested list items 2 spaces.
* **No emoji or Nerd Font icons:** a reader whose font lacks them sees empty boxes.
* **Lint:** when markdownlint is available, run it.
  Its rules MD001, MD013, MD022, MD031, MD032, MD040, and MD059 check most of the rules above.

## Patterns to remove

These habits fill reading time without adding facts.
Replace each one with the specific fact it stands in for.

* **"Not X, but Y" and "X, not Y":** the reader must process a negation of a view they never held.
* **Bold on every key phrase:** bold stops signalling anything.
* **Bold-label lists for content that is not a list of rules or terms:** they drop the reasoning between points.
* **Groups of three:** "fast, reliable, and scalable" when only 1 claim is true.
* **Inflated words:** "pivotal", "delve", "tapestry", "evolving landscape", and "serves as".
* **Comment-on-meaning phrases:** a trailing "highlighting its importance" or "ensuring consistency".
* **Vague attributions:** "experts argue" or "studies show" with no source.
* **Small tables that read better as a sentence.**
* **Chat residue:** "In this section we will", "Let me know if", and closing summaries that repeat the opening.
