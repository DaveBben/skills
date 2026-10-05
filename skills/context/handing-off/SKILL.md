---
name: handing-off
metadata:
  version: "0.5.0"
description: "Use this skill whenever this session's work has to survive into another one, or the user says the context window is filling, full, running out, running low or rotting. Use it on: 'create a handoff', 'make a handoff', 'write a handoff document', 'your context is getting full', 'you are running out of context', 'you are running low on context', 'there's context rot', 'I want to pick this up later', 'summarise this for next time'. A remark about your context is a request for a handoff, not an observation to agree with: write the handoff. Writes one handoff document under `docs/agents/handoff/`."
license: MIT
---
# Handing off

Write a handoff document summarizing this session so a fresh agent or human can resume without re-deriving context.

## File Naming and Creation

* **Format:** `docs/agents/handoff/YYYY-MM-DD-NNN-<slug>.md`
* **Date:** Use the current system date.
* **Increment:** `NNN` is zero-padded to three digits and restarts at `001` each day. List the directory and increment the highest number already used today.
* **Slug:** A short kebab-case name derived from the main subject of the session (e.g., `eth-brownie-optimization`, `video-script-draft`, `enclosure-prototype`).
* **Never committed:** a handoff is private working state. Before writing one inside a git repository, run `git check-ignore -q docs/agents/handoff/x.md`; when that fails, add the line `docs/agents/handoff/` to the file `git rev-parse --git-path info/exclude` prints. Git reads that file but never commits it. Run both commands from the repository root.
* **Interaction:** Propose the exact file path and wait. Say: `"Proposed filename: <path>. Is that correct? If not, provide the filename to use instead."` Do not write the file until the user confirms or overrides.

## Writing for a reader who was not here

The reader did not see this conversation. Text that reads as complete to the writer and as a list of pointers to the reader is the failure to avoid.

* **Resolve every pointer on the page.** No bare test ID, config key, abbreviation, or "the X" without one sentence saying what it is. Write "clinician", not "NP". Write "the browser panel that sends one request per keystroke", not "the panel". A pointer is a name local to this project or this session. Do not define industry-standard terms a working engineer knows: SQLite, fsync, Linux, HTTP.
* **Mechanism before label.** Write what physically happens ("the worker thread sits idle until the HTTP response arrives") before any name for it ("blocking"). A name never stands alone. "Racy at the margin" is a label; "two requests can both read 2, both write 3, and the cap admits one extra call" is the mechanism.
* **Check every connective.** For each "because", "so", "therefore", "which means": confirm the left clause causes the right. When it does not, write two sentences and no connective.
* **One rung at a time.** A claim about the system needs the component sentence, then the platform sentence, then the system sentence. Do not go from a function name to an outage in one sentence.
* **Incident as narrative.** When something broke, write what was built, what it did, and what failed, in that order. Narrative is the shortest explanation of a mechanism.
* **Before and after in the reader's units.** "Clinicians currently recording", not a formula, a variable, or "N".
* **Floor, not ceiling.** No word cap. Every claim carries at least one sentence of mechanism. Length follows from that.
* **Never invent a mechanism.** When the cause is not known, write "cause not established" and what would establish it. A plausible mechanism the evidence does not show is the same defect as a label, with a confident tone added. Every fact comes from the session, the code, or a source you can name. Do not add a rejected alternative nobody considered, a hardware rationale nobody measured, or a language or library the session never named.

Use a list for parallel items. Use a paragraph when the sentences depend on each other, as a mechanism explanation does. No acknowledgments, closing thoughts or analogies.

## What it carries

Read the most recent existing handoff in that directory, if one exists. Carry forward each dead end and open item it lists that this session did not resolve. Include:

* **Active state:** each task in this session's task list and its status: done, in progress or not started.
* **What was accomplished:** Concrete deliverables, written content, or code that now works that did not before.
* **Key decisions:** Major choices made, what was ruled out, and why (linking to ADRs if applicable).
* **Dead ends:** What was tried, and what went wrong with each. Name the exact errors, roadblocks, or failure paths.
* **Context a fresh agent needs:** File paths, source URLs, data locations, and where each credential is stored (the environment variable or vault entry), never the secret value. *If a codebase is involved,* include the current branch name and any pre-existing test failures that belong to the base branch.
* **Where things stand:** The single concrete next step to resume the work.

Name what is unfinished plainly. A handoff that reads as though everything went well is worse than none.
