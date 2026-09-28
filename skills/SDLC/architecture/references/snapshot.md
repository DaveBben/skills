# Write an architecture snapshot

Load this whenever the `architecture` skill writes the system's shape: the capture path, and section 6 of the plan reference. A snapshot is one Markdown file, `docs/architecture/snapshots/<YYYY-MM-DD>.md`, that lets a reader who has never opened the code explain how the system works and predict what a change would do. It is dated, and never edited after its commit. A later snapshot replaces it, and `AGENTS.md` points at the latest one. On a day that already has a snapshot, edit that day's file.

Write it by the writing rules. The reader is a person, or an agent about to change the code. Its test is the reconstruction test: from the file alone, the reader can follow each key flow through the system, say what fails and what the person using it sees, and name the file to change.

## Sources

* **Read the code, not the docs.** Take each fact from the code, the schema, a config file, a test, a spike's findings or an ADR (architecture decision record), and name the file. A README or an older snapshot is a claim to check.
* **Read the stores' schemas** even when another repository owns them: the tables and columns this system reads and writes, the key, the constraints, and the grants of the account this system connects as.
* **Read every current decision.** ADRs under `docs/adr/`, or the repository's own decision log. Skip each one with a `Superseded by:` line, and each one the code no longer follows.
* **Write "unknown" where nothing read settles a fact,** and list it under Open questions. Never fill a cell from what is plausible.
* **Cite a test as an enforcer only after reading its assertions.** A test whose name matches the rule but asserts something narrower is not the rule's enforcer; name what it does cover.
* **Follow each write to its commit.** For every file, store or message a unit of work touches, state whether it happens before or after the commit, and what a failure between the two leaves behind.
* **Refute before committing.** Hand the draft to a fresh subagent told to disprove each claim against the code (every test ID, number, path, link and failure row), and fix or delete each claim it refutes.

## The summary the user owns

`docs/architecture/summary.md` is one page, at most about 40 lines, that the user writes in their own words and only the user edits. It is not dated. Writing it is how the user keeps their own model of the system. Draft it once, from the numbers, the decisions and the failure table, headed `DRAFT: rewrite this in your own words, then delete this line`, and ask the user to rewrite it. Never edit it after that. When a decision or a snapshot contradicts it, say so in chat, quoting the line.

```text
Purpose:      <one sentence: who uses this and what they get>
Qualities:    <the three that matter most, ranked, each with its number: "1. a task appears within 15 minutes of the lab arriving">
Tradeoffs:    <three to five lines: "<chosen> over <rejected>, accepting <the cost>">
Constraints:  <each hard limit nobody may break: a law, a contract, a platform>
Risks:        <the three most likely ways the system fails: what the person using it sees, and the outside system or crossing involved>
```

When a smaller choice has alternatives and the ranked qualities pick one, the qualities settle it (see `SKILL.md`, section 5).

## Sections, in this order

Leave out a section with nothing to say. Add a section for any mechanism a reader needs that this list lacks. Sections 1 to 7 are the part a person reads, and stay under about 100 lines together. Head section 8 onward with "Reference: read when changing that part".

1. **Header:** the date, the commit read (hash and subject) or "planned, not yet built", and one line saying the file is never edited, and that `AGENTS.md` points at the latest snapshot and at `docs/architecture/summary.md`.
2. **Changed since the previous snapshot:** one line per process, store, module, flow, owner, failure row or decision added, removed or changed, with the story that changed it. On the first snapshot, write "First snapshot."
3. **What the system does:** one paragraph a person could say aloud. Name who uses the output and what they see, the one unit of work, and each outside system it depends on. Then the numbers the system is held to (load, response time, downtime, accuracy), each with its source, and what a spike or a log measured.
4. **The system and what it talks to:** one Mermaid `flowchart` with the system as one box, and each kind of person and each outside system around it, each arrow labelled by what crosses it.
5. **Processes and stores:** one Mermaid `flowchart` of each process, each store and each outside system, grouped by machine, with each arrow labelled by what crosses it and pointing from the side that starts the exchange. Leave modules out. Keep it to about 10 boxes; past that, group processes that share a machine and a job into one box, and say which.
6. **Key flows, end to end:** three to five flows, one per main thing a person gets from the system; a system with one flow has one. Each is the numbered path of one unit of work (a request, a night's batch, an upload), from what starts it to what the person sees. Each step names the function that does it, the store it reads or writes, and any time, count or limit that governs it. Follow the numbered path with a Mermaid `sequenceDiagram` of the same steps. A reader repeats these to someone else, so write the mechanism, never a label for it.
7. **Who owns what:** a table with one row per process, store and outside system: the team or person who owns it, and how to reach them. Take each from `CODEOWNERS`, the tracker or the code host, and write "unknown" where none says. A question only that owner can answer goes to them.
8. **The core logic:** one section per piece of logic a reader cannot guess from the step names, headed by what it is (the classifier, the pricing rule, the sync algorithm). Write its inputs, where each input comes from, how the output is computed, what makes it change, what it was measured at, and its known limits.
9. **Storage:** a table with one row per store: where it lives, which repository owns its schema, what this system reads, and what it writes. Then, for each store this system writes, the shape of one record, what makes a record unique, what the database enforces and what only the code enforces, how the data grows, what deletes it, and how it is backed up. When the account this system connects as lacks a privilege (UPDATE, DELETE, CREATE), write which behaviours depend on that.
10. **Rules and their enforcers:** a table of each rule the code keeps across modules (one transaction per unit, an item processed once, a cap), each with the test ID, contract or constraint that fails when the rule breaks. A rule with no enforcer says "none".
11. **When something fails:** a table with one row per failure: what fails, what the code does, and what the person using the system sees. Cover every crossing to another process, machine or outside system, and each overlap or partial run. Mark each row derived from the code and never observed as "not observed live".
12. **Code map:** a table with one row per module: the one thing it owns, and the change a reader would make there. Then one sentence stating which module may import which, and the file that enforces it.
13. **Deploy and operate:** a table with a row per process: the machine, the copies, and what starts it. Then the commands that build, ship and run it once by hand, and where its logs go.
14. **Who else can reach each crossing:** a table with a row per crossing to another machine or a store: how the callee checks the caller, and who else can reach it. Write "unknown" where the code does not show it.
15. **Open questions:** each "unknown", as one question and the person or system that can answer it.
16. **Current decisions:** one line per decision the code on this commit follows, grouped under the section it shapes, written as a tradeoff: "<chosen> over <rejected>: <the reason>, accepting <the cost>". Take each part from the decision itself, and end the line with a link to the ADR file or to the heading anchor in the decision log. Leave out superseded ones.
17. **Drift found:** each doc, comment or decision this snapshot contradicts, with the file. It tells the next session what to fix.

## Links and form

* **Link where the reader acts.** Link a decision beside the sentence it explains, as well as in Current decisions. Write file and function names in backticks so a reader can search for them.
* **Tables for parallel facts, paragraphs for mechanism.** A store, a failure or a module is a row. A step that depends on the step before it is a sentence.
* **No length cap.** A section is as long as its mechanism needs and no longer. Snapshots of small systems run to about 200 lines, of which sections 1 to 7 are the part most readers need.
* **Commit it on its own branch with a pull request,** together with the `AGENTS.md` pointer change and any summary draft, so they land together.
