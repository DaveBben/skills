---
name: handing-off
metadata:
  version: "0.8.0"
description: "Use this skill whenever this session's work must survive into another, or the user says the context window is filling, full, running low or rotting. Use it on: 'handoff', 'create a handoff', 'your context is getting full', 'you are running out of context', 'context rot', 'I want to pick this up later', 'summarise this for next time'. A remark about your context is a request for a handoff: write it. Writes one handoff document under `.claude/agents/handoff/` or `.agents/handoff/`. Not for picking up from a handoff; that is `story`."
license: MIT
---
# Handing off

Write a handoff document summarizing this session so a fresh agent or human can resume without re-deriving context.

## File name and location

* **Directory:** `.claude/agents/handoff/` when the project root (the repository root inside git, otherwise the working directory) already holds a `.claude/` folder, otherwise `.agents/handoff/`. Choose it without asking, and create it when missing.
* **Format:** `<directory>/YYYY-MM-DD-HHMMSS-mmm.md`, the current local date and time to the millisecond, e.g. `.agents/handoff/2026-10-07-080714-995.md`. macOS `date` has no milliseconds; `python3 -c 'from datetime import datetime; print(datetime.now().strftime("%Y-%m-%d-%H%M%S-%f")[:-3])'` works everywhere Python does.
* **Never committed:** inside a git repository, run `git check-ignore -q <directory>/x.md` from the repository root before writing; when that fails, add the line `<directory>/` to the file `git rev-parse --git-path info/exclude` prints.
* **Interaction:** write the file without asking, then tell the user its path.

## Writing for a reader who was not here

The reader did not see this conversation. The failure to avoid is text that reads as complete to the writer and as a list of pointers to the reader.

* **Resolve every pointer on the page.** A pointer is a name local to this project or this session: a bare test ID, config key, abbreviation, or "the X". Give each one sentence saying what it is: "the browser panel that sends one request per keystroke", not "the panel". A term in `docs/glossary.md`, the user's confirmed domain terms, needs no definition. Define a term this session coined and mark it unconfirmed. Do not define industry-standard terms such as SQLite, fsync or HTTP.
* **Mechanism before label.** Write what physically happens before any name for it, and never a name alone. "Racy at the margin" is a label; "two requests can both read 2, both write 3, and the cap admits one extra call" is the mechanism.
* **Check every connective.** For each "because", "so", "therefore" or "which means", confirm the left clause causes the right. When it does not, write two sentences and no connective.
* **One rung at a time.** A claim about the system needs the component sentence, then the platform sentence, then the system sentence. Do not go from a function name to an outage in one sentence.
* **Incident as narrative.** When something broke, write what was built, what it did, and what failed, in that order.
* **Before and after in the reader's units.** "Clinicians currently recording", not a formula, a variable, or "N".
* **Floor, not ceiling.** No word cap. Every claim carries at least one sentence of mechanism. Length follows from that.
* **Never invent a mechanism.** When the cause is not known, write "cause not established" and what would establish it. Every fact comes from the session, the code, or a source you can name. Do not add a rejected alternative nobody considered, a hardware rationale nobody measured, or a language or library the session never named.

Use a list for parallel items. Use a paragraph when the sentences depend on each other, as a mechanism explanation does. No acknowledgments, closing thoughts or analogies.

## What it carries

Read the most recent existing handoff in that directory, if one exists. Carry forward each dead end and open item it lists that this session did not resolve. Include:

* **Active state:** each task in this session's task list and its status: done, in progress or not started.
* **Destination,** when there is one: the issue, story or spec whose acceptance criteria define done, by link or path, never copied. With a story, the next session resumes it by the `story` skill.
* **What was accomplished:** each deliverable, and code that now works that did not before, with the test or command that shows it, where one does.
* **Key decisions:** each choice made, what was ruled out, and why, linking any ADR.
* **Dead ends:** what was tried, and the exact error or failure each hit.
* **Context a fresh agent needs:** file paths, source URLs, data locations, and where each credential is stored (the environment variable or vault entry), never the secret value. In a codebase, the current branch and any test failures that belong to the base branch.
* **Open questions:** each decision still open. Copy word for word each `Needs research:` line, a question the user is researching that a story waits on.
* **Where things stand:** the single concrete next step to resume the work. Mid test-first work, it names the failing test and the command that runs it.

Name what is unfinished plainly; never write a handoff that reads as though everything went well.
