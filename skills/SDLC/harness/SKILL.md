---
name: harness
version: "0.4.0"
description: "Fire when a repository gives an agent no deterministic feedback: no formatter, linter, type check, custom rules, architectural contracts, or commit gate, or when those exist but nothing feeds their output back to the agent. Fire on: 'set this repo up for my AI agent', 'bootstrap this repo', 'initialize a repo', 'set up guardrails', 'we have no linting or rules', 'the agent keeps making the same mistake'. Not for making a change; that is `agile`."
license: MIT
compatibility: any-agent
---
# Repository harness

Build the checks that reach the agent without a human carrying them. Every correction a human makes by hand is a rule nobody has written yet.

Language agnostic. This skill names each slot and the test a filled slot must pass. Identify the language, pick the tool yourself, and say which you picked.

It does not decide what the system should be. Discovery, specs and design belong to `agile`.

```text
SURVEY        language, package manager, harness, slots already filled
  |
SLOTS         one tool per slot, each watched failing once
  |
CONTRACTS     allowed dependency directions, executed
  |
RULES         this codebase's own anti-patterns, executed
  |
LOOP          three layers wired to harness events
  |
GUARDS        hard blocks, denied paths, pre-approved commands
  |
INSTRUCTIONS  root, nested, path-scoped
  |
GATE          commit hook and CI running the same list
```

* **Classify the repository** to determine whether enforcement scope is a decision:
  * *Greenfield:* No code, or code you will discard. Every rule applies from the first commit and nothing needs grandfathering.
  * *Brownfield:* Code that predates the rules. Existing code violates every rule you add.
* **The branch is not project age.** A two-week-old repo with a thousand lines and no linter is brownfield.
* **Halt before writing anything** if a change is in flight: an open `feature/` or `fix/` branch with slices merged into it, or an uncommitted spec or design document for a change underway. Cleanups rewrite the tree and will collide. Offer the config-only subset now with cleanups deferred, or finishing the slice first.
* **Resume at the first missing output** when a repository is part-way through this skill.

## What never bends

* **The failure message is the prompt.** Every check states what is forbidden and what to do instead. `rule R2011 violated` has thrown away its value.
* **Watch every check fail once.** Introduce the violation, confirm the non-zero exit and the message, remove it. A check nobody has seen fail is a check you do not know works.
* **Feedback arrives on the developer's machine**, at the moment of the edit. CI is the backstop and never the first place a rule fires.
* **Silencing a check is not passing it.** Disabling a rule, loosening a config, weakening an assertion, or skipping a test to reach green is not a fix. This sentence goes into the instructions file verbatim.
* **A blocking check needs an escape.** Wire the loop safety before the checks, or an unfixable error traps the agent.

## How to talk with the user

Do not announce steps. You are a dry, highly mechanical agent. Strictly adhere to these output rules:

* **Zero Filler & Wrap-ups:** Never use introductory acknowledgments. Stop generating text the moment the factual answer is complete.
* **Order by risk:** Inverted pyramid. The core answer or hard blocker goes in the first sentence.
* **Structure over prose:** Bulleted lists or tables for sequences, never block paragraphs.
* **Zero Analogies:** Explain the mechanism literally.
* **One question per turn.** Surface what you found and let the user disposition it. Never decide a tool swap on their behalf.
* **Config goes to disk, not into the chat.** Name the file and the one line in it the user would argue with.

## Survey

* **Record the language, package manager, harness, and which slots already have a tool.** State it in one table before proposing anything.
* **Name every conflict before changing it:** two tools covering one slot, two package managers, a manifest with no lockfile, or config in a file the new tool will not read.
* **Propose the migration; never perform it.** Replacing a working toolchain is the user's decision. On greenfield, take all of it.

## Slots

Load `references/toolchain.md` now, before writing any config. It carries the slot table, the placement rule in seconds, the fallbacks for slots with no tool, and the settings whose defaults are wrong for an agent.

* **Take the tool's defaults** except for the settings that reference names explicitly. Each of those has a silent failure mode.
* **Delegate the mechanical work** to subagents where the harness allows it, in parallel where it divides: the lint cleanup, landing rules on existing code, deriving the dependency graph, any bulk rewrite a new rule forces. Pick the cheapest model per job and say which. Where subagents are unavailable, warn the user that a cleanup runs inline and holds the session.

## Contracts

The only check that sees a dependency reverse. A single-file linter and a type checker both have no opinion about the shape of the package, and the cost of the wrong shape arrives months later, long after every test still passes.

* **Greenfield:** Ask the user for the modules, what each owns, and which way dependencies run. It is theirs to draw. Where nothing is settled, say so, fill the language-level slots now, and encode contracts after the first change through `agile` has drawn the shape.
* **Brownfield:** Derive the current dependency graph, render it as a diagram, and ask which edges they did not expect. Those are the ones nobody chose, and they become the first contracts. Never encode the whole current graph; that makes the mess permanent.
* **One contract per allowed-dependency line.** Everything not listed is forbidden, and the config says so explicitly.
* **Write each contract's name as the rule in plain English**, so a broken build prints the sentence that stopped being true.
* **The contracts are the record.** Do not create a separate architecture document to describe them; two sources of truth drift, and the prose one is never the one that fails the build.

## Rules

The deposit location for a correction a static check can express. One rule per file, in `.semgrep/` unless the project already has a pattern engine.

* **Brownfield only.** Greenfield has nothing yet to violate a rule.
* **Offer the anti-pattern sweep and the rules as one decision.** Apart they produce nothing.
* **Ask the agent what anti-patterns this codebase uses**, put the list to the user, then encode the practices already visible in the code and those anti-patterns as their inverse.
* **Show each rule with one real violation it catches** before adding it. A rule with no current violation is a preference; say so and let the user choose.
* **Scope with the engine's path filters**, never with exemptions written into the pattern.

## Loop

Where the harness is Claude Code, load `references/claude-harness.md` now and write the files it carries. Another harness wires the same three layers to whatever events it exposes. Where it exposes none, say so plainly: the checks still run at commit time and in CI, and feedback arrives a turn later instead of immediately.

* **Three layers, each a subset of one command list**, so what is fixed at edit time is never rediscovered at commit time.
* **Auto-fix everything mechanically fixable and silence it.** Surface only what needs a decision.
* **Count the retries per session.** Increment on each block, clear on a pass, give up after three, then let the turn end and say so.
* **Re-verify after each fix**, rather than checking once and standing down.
* **Skip when nothing relevant changed.**
* **Fail open when the tool itself breaks.** Distinguish "the checker found problems" from "the checker could not run", or a missing dependency phantom-blocks every edit.
* **Scope to this repository.** A session can hold other working directories and these rules do not apply there.

## Guards

* **Hard blocks: two entries, and justify a third.** A rule earns a slot only when violating it is never correct and the harness cannot catch it afterwards. Blocking the flag that skips the commit gate qualifies. Blocking a package manager the project does not use is blocklist creep.
* **Deny reads and writes outright** for secrets files, the lockfile, and the version control directory. These are not style rules and do not belong in a linter.
* **Say plainly that the deny list stops accidents and is not a security boundary.** Anything pre-approved that executes code can read any file the user can.
* **Pre-approve every verification command** the agent needs to check its own work. A check the agent must ask permission to run is a check it stops running.
* **Report environment readiness at session start**, naming the command that fixes each problem. "Environment is not ready" tells the agent nothing it can act on.
* **Offer an isolated container** where the harness supports one, so a permissive agent session has a bounded blast radius. Keep credentials out of environment variables, which are readable by every child process and by anyone inspecting the container.

## Instructions

Three scopes. Put each rule in the narrowest one that still loads when it is needed.

| Scope | Loads | Holds |
|---|---|---|
| Root instructions file | every session | anything true for the whole conversation |
| Nested instructions file | a file in that directory is touched | conventions for one module |
| Path-scoped rule file | a matching path is touched | instructions tied to a file type |

* **Create the root file if the repo has none**, even empty with a heading, and say where it is. The change loop appends to it.
* **Cap the root file at 100 lines.** Every line costs context on every turn, and a bloated file makes the agent ignore the rules that matter. Anything longer belongs in a nested or path-scoped file.
* **Alias the other conventional filenames to it** with a symlink, so every tool reads one file.
* **Record where a future correction goes.** State the routing in the root file: a static check into the rules directory, a dependency direction into the contracts, a file-specific instruction into a path-scoped rule, anything conversational into the root file itself.
* **Offer an answer-length rule for the root file:** give the finding, what it means, and the question, then stop; name a document or diff just written rather than reproducing it. Ask before adding it. That file is the user's.
* **Never path-scope an instruction that governs the conversation.** Path frontmatter loads it only when a matching file is touched.

## Gate

* **Commit hook and CI run the same command list**, so "passes locally" and "passes in CI" are the same contract.
* **Pin every hook version.** An unpinned hook makes the gate non-reproducible.
* **Run each CI check as its own step**, install from the lockfile, and run the full supported runtime matrix without stopping at the first failure.
* **Scope the dependency audit to lockfile changes.** It needs the network, and a registry outage must not block a pure code commit. Give the user the command that skips one hook, and state that skipping the whole gate is never the answer.
* **Wire automated dependency updates** so the lockfile and CI pins do not rot.

## Landing rules on existing code

Brownfield, and only where rules were accepted. Put the choice to the user:

* **Scope enforcement to files authored from here on.** The rules land today and the backlog stays where it is.
* **Clean up in a subagent, as its own change**, running in proportion to the size of the codebase.

Either is a real answer. Adding rules and leaving them red is not. The same choice applies to a failing test suite: quarantine the pre-existing failures or fix them before the suite enters the gate.
