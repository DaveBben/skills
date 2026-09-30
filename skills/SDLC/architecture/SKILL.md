---
name: architecture
description: "Use this skill when a choice costs more than a day to reverse, when a system's shape must be decided or mapped, when a decision or an accepted risk must be recorded, when an idea must be tried, compared or tested with throwaway code before it is built for real, or when work is asked for in a repository with no application yet. Use it on: 'how should this be structured', 'should I use X or Y', 'let's build this' in an empty repo, 'note this decision', 'record the why', 'write an ADR', 'snapshot the architecture', 'do a spike', 'let's prove this works first', 'try a few approaches and see', 'test whether X improves Y', 'find the best model for this', 'experiment with', 'prototype', 'mock this up', 'a demo', 'is X feasible', 'see how this would fit or integrate', 'what would it take to move to X', 'template project'. Load it before asking what the user means. Runs spikes, maps the system, records decisions with the user's reasons."
license: MIT
metadata:
  version: "4.0.0"
---
# Architecture

Decide architecture in this order: prove each unknown with a spike, take a broad starting shape, record each decision, prove the shape with a walking skeleton (the thinnest end-to-end version a real person can use, built first), and change it by refactoring as stories teach more.

## Where things are written

* **The shape:** a snapshot, a dated Markdown file under `docs/architecture/snapshots/` describing the system's processes, stores and flows, with one `Architecture:` line in `AGENTS.md` pointing at the latest. The user owns a one-page summary, `docs/architecture/summary.md`.
* **Each decision:** an ADR (architecture decision record), one Markdown file under `docs/adr/` saying what was decided, why, and what it gave up.
* **Each rule:** a test or a dependency contract, which the `guardrails` skill writes.
* **The feature:** the feature header is the epic's description on the tracker that the `Backlog:` line of `AGENTS.md` names, and the feature's slug is the epic's key. When a feature is open, write to it `Decided:` (one ADR path per line) and `Deferred:` (one open item per line, with what will force it). With no feature header, ask the user for the outcome in one sentence and the steps a person takes.

Subagents write the ADRs, the snapshots and the spikes, each from a brief under this skill's `references/`. Pass a subagent its brief's full path without reading the brief yourself. Read any other file under `references/` only at the step that names it. To continue a subagent after asking the user, resume it where the harness allows (Claude Code's SendMessage), else launch a fresh one with its brief and what it returned. Where the harness cannot launch a subagent, read the brief and do its task yourself.

## Asking

Everything here is agreed with the user. Look up any fact the code, the data or the tracker holds, and use it. Put a fact only a named person knows on the epic for that person. Ask one question per message. A set of drafts for the user to correct (the Numbers, the Map tables, an ADR's three answers) goes in one message. Open each message with one line naming the repository and the feature, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion).

## Pick the path

* **Record a decision already made:** read `references/record-decision.md`, nothing else.
* **Decide one open item:** read `references/plan-numbers.md` and draft only the numbers the item turns on, then `references/plan-decide.md` for that item alone.
* **Find something out by building throwaway code:** "Run a spike" below.
* **Capture the current architecture:** "Write a snapshot" below on a new branch of its own, then open a pull request for that branch, then stop.
* **Plan a system:** read `references/plan-crossings.md`; each step names the next.
* **A new application:** decide the repositories first (how many, each name and directory; on the feature header's `Repositories:` line as `new: <name>`, or in chat until a tracker exists), run `git init -b main` in the first (`scaffold.sh` keeps that repository), and record that decision by `references/record-decision.md`. Then read `references/plan-crossings.md`; the Decide step sends you on to stand up each repository.

## Run a spike

A spike answers one question with the smallest throwaway code inside a timebox, records what it learned, and deletes the code. Frame it with the user in one message before any code:

* **The question,** as an outcome that can fail: "the library streams partial results under 200 ms", not "look into the library". Refuse a spike with no failing condition.
* **The finish line:** the signal that answers it.
* **The timebox:** a wall-clock limit or a number of attempts, proposed for the user to correct. When it runs out, the outcome is inconclusive.
* **Throwaway:** tell the user the code is deleted once the findings are written.

Then launch a fresh general-purpose subagent (in Claude Code, the Agent tool with `subagent_type: general-purpose`) with the full path of `references/spike.md`, the question, the finish line, the timebox, the repository, and the epic's key or "no epic". When it returns a missing credential's name, ask the user for it once and continue the subagent with the answer. Frame each second unknown it returns with the user as a spike of its own. When it resolves, state the verdict and the finding that settles it, and put its decision table to the user to mark each row `record`, `drop` or `defer`. Record each `record` row by `references/record-decision.md`, and add each `defer` row to the findings' open questions. A finding that contradicts a decided ADR gets a new ADR naming the old one on `Supersedes:`, by the same file.

## Write a snapshot

Launch a fresh general-purpose subagent (in Claude Code, the Agent tool with `subagent_type: general-purpose`) with the full path of `references/snapshot.md`, the repository, the latest snapshot `AGENTS.md` points at or "none", and the checkout and branch to commit in. It writes and commits the snapshot, points `AGENTS.md` at it, drafts the summary when there is none, and returns what it found; relay its `Settles:`, `Drift:` and `Questions:` lines. When it returns a snapshot of built code unrefuted, launch a fresh refuting subagent (in Claude Code, the `SDLC:refute` agent) told to disprove each claim in the snapshot against the code, and continue the writer with what it refutes, to fix or delete. When it drafted the summary, ask the user to rewrite it in their own words. Quote to the user each summary line it reports contradicted.
