---
name: handing-off
version: "0.3.2"
description: "Use this skill whenever this session's work has to survive into another one, or the user says the context window is filling, full, running out, running low or rotting. Use it on: 'create a handoff', 'make a handoff', 'write a handoff document', 'your context is getting full', 'you are running out of context', 'you are running low on context', 'there's context rot', 'I want to pick this up later', 'summarise this for next time'. A remark about your context is a request for a handoff, not an observation to agree with: write the handoff. Record the dead ends, not just the progress."
license: MIT
compatibility: any-agent
---
# Handing off

Write a handoff document summarizing this session so a fresh agent or human can resume without re-deriving context.

## File Naming and Creation

* **Format:** `docs/agents/handoff/YYYY-MM-DD-NNN-<slug>.md`
* **Date:** Use the current system date.
* **Increment:** `NNN` is zero-padded to three digits and restarts at `001` each day. List the directory and increment the highest number already used today.
* **Slug:** A short kebab-case name derived from the main subject of the session (e.g., `eth-brownie-optimization`, `video-script-draft`, `enclosure-prototype`).
* **Interaction:** Propose the exact file path and wait. Say: `"Proposed filename: <path>. Is that correct? If not, provide the filename to use instead."` Do not write the file until the user confirms or overrides.

## What it carries

Read the most recent existing handoff in that directory, if one exists, and match its style and depth. The document must explicitly include:

* **Active State:** The exact status of the current task list. *If an engineering task is active,* explicitly list which Falsifiable Assertions were checked `[x]` this session, and which remain `[ ]`.
* **What was accomplished:** Concrete deliverables, written content, or code that now works that did not before.
* **Key decisions:** Major choices made, what was ruled out, and why (linking to ADRs if applicable).
* **Dead ends:** What was tried, and what went wrong with each. Name the exact errors, roadblocks, or failure paths.
* **Context a fresh agent needs:** File paths, source URLs, data locations, or credentials. *If a codebase is involved,* include the active `feature/{slug}` or `fix/{slug}` branch name and any pre-existing test failures that belong to the base branch.
* **Where things stand:** The single concrete next step to resume the work.

Name what is unfinished plainly. A handoff that reads as though everything went well is worse than none.

## Communication Constraints
You are writing for another mechanical agent. Adhere strictly to these rules when formatting the file:

* **Zero Filler & Wrap-ups:** Never use introductory acknowledgments, narrative summaries, or closing thoughts.
* **Structure over prose:** Use bulleted lists or tables. Do not write block paragraphs.
* **Zero Analogies:** Explain systems, failures, and data literally. Stick strictly to the code, files, and data.
* **Falsifiability:** Reference exact file names, line numbers, and metric constraints instead of general areas.