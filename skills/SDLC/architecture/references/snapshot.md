# Write an architecture snapshot

Load this whenever the `architecture` skill writes the system's shape: the capture path, and section 6 of the plan reference. A snapshot is one Markdown file, `docs/architecture/snapshots/<YYYY-MM-DD>.md`, that lets a reader who has never opened the code explain how the system works and predict what a change would do. It is dated, and never edited after its commit. A later snapshot replaces it, and `AGENTS.md` points at the latest one. On a day that already has a snapshot, edit that day's file.

Write it by the writing rules. The reader is a person, or an agent about to change the code. Its test is the reconstruction test: from the file alone, the reader can follow one unit of work through the system, say what fails and what the person using it sees, and name the file to change.

## Sources

* **Read the code, not the docs.** Take each fact from the code, the schema, a config file, a test, a spike's findings or an ADR (architecture decision record), and name the file. A README or an older snapshot is a claim to check.
* **Read the stores' schemas** even when another repository owns them: the tables and columns this system reads and writes, the key, the constraints, and the grants of the account this system connects as.
* **Read every current decision.** ADRs under `docs/adr/`, or the repository's own decision log. Skip each one with a `Superseded by:` line, and each one the code no longer follows.
* **Write "unknown" where nothing read settles a fact,** and list it under Open questions. Never fill a cell from what is plausible.
* **Cite a test as an enforcer only after reading its assertions.** A test whose name matches the rule but asserts something narrower is not the rule's enforcer; name what it does cover.
* **Follow each write to its commit.** For every file, store or message a unit of work touches, state whether it happens before or after the commit, and what a failure between the two leaves behind.
* **Refute before committing.** Hand the draft to a fresh subagent told to disprove each claim against the code (every test ID, number, path, link and failure row), and fix or delete each claim it refutes.

## Sections, in this order

Leave out a section with nothing to say. Add a section for any mechanism a reader needs that this list lacks.

1. **Header:** the date, the commit read (hash and subject) or "planned, not yet built", and one line saying the file is never edited and `AGENTS.md` points at the latest snapshot.
2. **What the system does:** one paragraph a person could say aloud. Name who uses the output and what they see, the one unit of work, and each outside system it depends on. Then the numbers the system is held to (load, response time, downtime, accuracy), each with its source, and what a spike or a log measured.
3. **Context diagram:** one Mermaid `flowchart`. Draw each process, each store and each outside system, grouped by machine, with each arrow labelled by what crosses it and pointing from the side that starts the exchange. Leave modules out of it.
4. **One unit, end to end:** the numbered path of one unit of work (a request, a night's batch, an upload), from what starts it to what the person sees. Each step names the function that does it, the store it reads or writes, and any time, count or limit that governs it. This section is the one a reader repeats to someone else, so write the mechanism, never a label for it.
5. **The core logic:** one section per piece of logic a reader cannot guess from the step names, headed by what it is (the classifier, the pricing rule, the sync algorithm). Write its inputs, where each input comes from, how the output is computed, what makes it change, what it was measured at, and its known limits.
6. **Storage:** a table with one row per store: where it lives, which repository owns its schema, what this system reads, and what it writes. Then, for each store this system writes, the shape of one record, what makes a record unique, what the database enforces and what only the code enforces, how the data grows, what deletes it, and how it is backed up. When the account this system connects as lacks a privilege (UPDATE, DELETE, CREATE), write which behaviours depend on that.
7. **Rules and their enforcers:** a table of each rule the code keeps across modules (one transaction per unit, an item processed once, a cap), each with the test ID, contract or constraint that fails when the rule breaks. A rule with no enforcer says "none".
8. **When something fails:** a table with one row per failure: what fails, what the code does, and what the person using the system sees. Cover every crossing to another process, machine or outside system, and each overlap or partial run. Mark each row derived from the code and never observed as "not observed live".
9. **Code map:** a table with one row per module: the one thing it owns, and the change a reader would make there. Then one sentence stating which module may import which, and the file that enforces it.
10. **Deploy and operate:** a table with a row per process: the machine, the copies, and what starts it. Then the commands that build, ship and run it once by hand, and where its logs go.
11. **Who else can reach each crossing:** a table with a row per crossing to another machine or a store: how the callee checks the caller, and who else can reach it. Write "unknown" where the code does not show it.
12. **Open questions:** each "unknown", as one question and the person or system that can answer it.
13. **Current decisions:** one line per decision the code on this commit follows, grouped under the section it shapes, written as a tradeoff: "<chosen> over <rejected>: <the reason>, accepting <the cost>". Take each part from the decision itself, and end the line with a link to the ADR file or to the heading anchor in the decision log. Leave out superseded ones.
14. **Drift found:** each doc, comment or decision this snapshot contradicts, with the file. It tells the next session what to fix.

## Links and form

* **Link where the reader acts.** Link a decision beside the sentence it explains, as well as in Current decisions. Write file and function names in backticks so a reader can search for them.
* **Tables for parallel facts, paragraphs for mechanism.** A store, a failure or a module is a row. A step that depends on the step before it is a sentence.
* **No length cap.** A section is as long as its mechanism needs and no longer. Snapshots of small systems run to about 200 lines.
* **Commit it on its own branch with a pull request,** together with the `AGENTS.md` pointer change, so the snapshot and the pointer land together.
