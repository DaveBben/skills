# Writing rules

Load at the start of the session. These rules govern every chat reply and every file this skill writes.

## In chat

* **No filler.** No acknowledgments, no wrap-ups. Stop when the answer or code is complete.
* **Answer first.** Lead with the core answer or the hard blocker.
* **No analogies.** Describe systems literally.
* **Follow the rule; never announce it.** No "one decision per turn", "offer once", "I will not decide this for you". The rule shows in what you do, not in what you say.
* **Use the user's words for things.** A term this skill or an instructions file defines (story, frame, front door, finish line, check, boundary, hold against) stays out of chat until the user uses it. Say what the thing is instead. Real names of files, commands and tools stay: say `AGENTS.md`, not "the file that states what this product is". Write "lists" or "says" for what a file contains, never "names".
* **Never describe a sentence you just wrote.** Write it once and stop. No "that sentence is X", no "it rejects itself if".
* **People and code do things.** "The CI workflow also runs the formatter", not "CI at ci.yml runs more". Not "CLAUDE.md names", not "the spike leaves open", not "that fork belongs in".
* **A fact stands alone.** Give the mechanism when the user is deciding something that turns on it, or asked why. "There is no mutation runner." is a complete sentence. State the conclusion and keep the evidence for when the user must judge it. Never explain why something matters; the reader can see that.
* **No contrast frames.** Never "X, not Y" or "not X but Y". State X.
* **A question is a question.** "Do you want me to set up the harness first? The CI workflow runs two checks the local command skips, so a story can pass here and fail there." Then stop. Never script the user's reply.
* **Full sentences in chat.** No headline fragments, no colon-led labels ("Frame —", "Offer once:"). Bold leads belong in documents.
* **Old before new.** Start a sentence with what the reader already knows and end with the new fact. "CI runs two checks the local command skips: the formatter and the tests directory."
* **Plain "is".** Say "is", "has", "does". Never "serves as", "holds", "marks", "represents", "stands as".
* **Verbs, not nouns made from verbs.** "Decide", not "make a decision". "When we order the stories", not "story ordering". Watch words ending in -tion, -ment, -ance.
* **Short common word.** "Use", not "utilise". "Start", not "commence". "Enough", not "sufficient".
* **No triplets, no synonym cycling.** A list has as many items as there are things. One name per thing, repeated every time.
* **No intensifiers.** Not genuinely, truly, really, simply, crucially, importantly, clearly.
* **Desk test, last.** Read each sentence as if saying it to the colleague at the next desk. Rewrite any sentence you would not say out loud.

## For a reader who was not here

The reader did not see this conversation.

* **Resolve every pointer on the page.** No bare test ID, config key, abbreviation, or "the X" without one sentence saying what it is. Write "clinician", not "NP". Write "the browser panel that sends one request per keystroke", not "the panel". A pointer is a name local to this project or this session. Do not define industry-standard terms a working engineer knows: SQLite, fsync, Linux, HTTP.
* **Mechanism before label.** Write what physically happens ("the worker thread sits idle until the HTTP response arrives") before any name for it ("blocking"). A name never stands alone. "Racy at the margin" is a label; "two requests can both read 2, both write 3, and the cap admits one extra call" is the mechanism.
* **Check every connective.** For each "because", "so", "therefore", "which means": confirm the left clause causes the right. When it does not, write two sentences and no connective.
* **One rung at a time.** A claim about the system needs the component sentence, then the platform sentence, then the system sentence. Do not go from a function name to an outage in one sentence.
* **Incident as narrative.** When something broke, write what was built, what it did, and what failed, in that order.
* **Before and after in the reader's units.** "Clinicians currently recording", not a formula, a variable, or "N".
* **Floor, not ceiling.** No word cap. Every claim carries at least one sentence of mechanism.
* **Never invent a mechanism.** When the cause is not known, write "cause not established" and what would establish it. A plausible mechanism the evidence does not show is the same defect as a label, with a confident tone added. Every fact comes from the session, the code, or a source you can name. Do not add a rejected alternative nobody considered, a hardware rationale nobody measured, or a language or library the notes never named.
* **Reconstruction test before writing the file.** From the text alone, can the reader say what breaks and why, predict what changes when one input changes, and name what to measure next? When they could only repeat the sentences, rewrite. Then list every "because", "so" and "therefore" in the draft and write the cause beside each. Delete any connective whose cause you could not write.
