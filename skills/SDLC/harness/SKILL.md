---
name: harness
description: "Use this skill whenever the user wants a repository or environment prepared for an AI agent or for Claude, or when a repo gives an agent no feedback of its own: no formatter, linter, type check, custom rules, architectural contracts or commit gate, or nothing routes their output back to the agent. Use it on: 'setup harness in this repo', 'set up guardrails', 'add hooks for the agent', 'wire the linter to claude', 'set up the commit gate', 'configure checks for my ai agent', 'the agent keeps ignoring the linter'. Use it on the complaint underneath: 'we have no linting or rules', 'every PR is a style argument', or the agent repeats a mistake a human keeps correcting by hand. Use it when `orient` hands off. Produces one tool per slot, the hooks that run them, a deny list, and a commit gate and CI that call one check command. Do not use it to write AGENTS.md, or on 'setup claude in this repo' or 'get this repo ready for agents'; those are `orient`. Do not use it to make a code change; that is `execute`."
license: MIT
compatibility: any-agent
metadata:
  version: "0.15.0"
---
# Repository harness

Identify the language, pick the tool, and name the pick.

Decide nothing about what the system should be. Framing and slicing belong to `feature`, and building belongs to `execute`.

```text
SURVEY        language, package manager, agent harness, slots already filled
  |
SLOTS         one tool per slot, each watched failing once
  |
CONTRACTS     allowed dependency directions, executed
  |
RULES         this codebase's own anti-patterns, executed
  |
LOOP          three layers wired to agent-harness events
  |
GUARDS        hard blocks, denied paths, pre-approved commands
  |
INSTRUCTIONS  root, nested, path-scoped
  |
GATE          commit hook and CI running the same list
```

* **Classify the repository** to determine whether enforcement scope is a decision:
  * *Greenfield:* No code, or code to be discarded.
  * *Brownfield:* Code that predates the rules.
* **The branch is not project age.** A two-week-old repo with a thousand lines and no linter is brownfield.
* **Halt before writing anything** if a change is in flight: an open `feature/{slug}` branch, or a `docs/features/{slug}/feature.md` (or the per-change spec `AGENTS.md` names instead) whose feature header still lists unshipped stories. Cleanups rewrite the tree and will collide. Offer the config-only subset now with cleanups deferred, or finishing the story first.
* **Resume at the first missing output** when a repository is part-way through this skill.

## What never bends

* **The failure message is the prompt.** Every check states what is forbidden and what to do instead, never a bare rule identifier such as `rule R2011 violated`.
* **Watch every check fail once.** Introduce the violation, confirm the non-zero exit and the message, remove it.
* **Feedback arrives on the developer's machine**, at the moment of the edit. CI is the backstop and never the first place a rule fires.
* **Silencing a check is not passing it.** Disabling a rule, loosening a config, weakening an assertion, or skipping a test to reach green is not a fix. This sentence goes into `AGENTS.md` verbatim.
* **A blocking check needs an escape.** Wire the loop safety before the checks.

## Survey

* **Record the language, package manager, agent harness, and which slots already have a tool.** State it in one table before proposing anything, one row per slot:

  ```text
  | Slot | Tool now | Fires | Proposed |
  |---|---|---|---|
  | fast_fix | none | - | <tool> |
  | types | <tool> | manual only | wire to turn end |
  ```

* **Name every conflict before changing it:** two tools covering one slot, two package managers, a manifest with no lockfile, or config in a file the new tool will not read. Where a newer tool subsumes an older one, say which rules the older carries that the newer does not.
* **Propose the migration; never perform it.** Replacing a working toolchain is the user's decision. On greenfield, take all of it.

## Slots

Load `references/toolchain.md` now, before writing any config.

* **Config goes to disk, not into the chat.** Name the file and the one line in it the user would argue with.
* **Take the tool's defaults** except for the settings that reference names explicitly. Each of those has a silent failure mode.
* **Delegate the mechanical work** to subagents where the agent harness allows it, in parallel where it divides: the lint cleanup, landing rules on existing code, deriving the dependency graph, any bulk rewrite a new rule forces. Pick the cheapest model per job and say which. Where subagents are unavailable, warn the user that a cleanup runs inline and holds the session.

## Contracts

* **Greenfield:** Ask the user for the modules, what each owns, and which way dependencies run. It is theirs to draw. Where nothing is settled, say so, fill the language-level slots now, and encode contracts after the first change through `execute` has drawn the shape.
* **Brownfield:** Derive the current dependency graph, render it as a diagram, and ask which edges they did not expect. Those are the ones nobody chose, and they become the first contracts. Never encode the whole current graph.
* **One contract per allowed-dependency line.** Everything not listed is forbidden, and the config says so explicitly.
* **Write each contract's name as the rule in plain English**, so a broken build prints the sentence that stopped being true.
* **Name the shape when it has a name.** When the user's modules match a known pattern (hexagonal, layered, MVI), record the name and its one defining rule in `AGENTS.md`.
* **The contracts are the record.** Never write a separate architecture document to describe them.

## Rules

Write each rule with the `make-rule` skill.

* **Brownfield only.**
* **Offer the anti-pattern sweep and the rules as one decision.**
* **Ask the agent what anti-patterns this codebase uses**, put the list to the user, then encode the practices already visible in the code and those anti-patterns as their inverse.
* **Show each rule with one real violation it catches** before adding it. A rule with no current violation is a preference; say so and let the user choose.

## Loop

Where the agent harness is Claude Code, load `references/claude-harness.md` now and write the files it carries. Another agent harness wires the same three layers to whatever events it exposes. Where it exposes none, say so plainly: the checks still run at commit time and in CI, and feedback arrives a turn later instead of immediately.

* **Three layers, each a subset of one command list.**
* **Auto-fix everything mechanically fixable and silence it.** Surface only what needs a decision.
* **Count the retries per session.** Increment on each block, clear on a pass, give up after three, then let the turn end and say so.
* **Re-verify after each fix**, rather than checking once and standing down.
* **Skip when nothing relevant changed.**
* **Fail open when the tool itself breaks.** Distinguish "the checker found problems" from "the checker could not run", or a missing dependency phantom-blocks every edit.
* **Scope to this repository.** A session can hold other working directories and these rules do not apply there.

## Guards

* **Hard blocks: two entries, and justify a third.** A rule earns a slot only when violating it is never correct and the harness cannot catch it afterwards. Blocking the flag that skips the commit gate qualifies. Blocking a package manager the project does not use is blocklist creep.
* **Block edits to accepted tests.** While `execute` has a red commit recorded, refuse any edit to a file that commit touched, at edit time. An instruction to leave tests alone is not a substitute for the guard.
* **Deny agent edits to the feature acceptance tests for good.** The `execute` loop keeps the user's acceptance test for a whole feature in a `feature-acceptance` directory inside the test tree. Deny edits, writes and deletes there permanently, for the agent and every subagent.
* **Deny reads and writes outright** for secrets files, the lockfile, and the version control directory. These are not style rules and do not belong in a linter.
* **Say plainly that the deny list stops accidents and is not a security boundary.** Anything pre-approved that executes code can read any file the user can.
* **Pre-approve every verification command** the agent needs to check its own work.
* **Report environment readiness at session start**, naming the command that fixes each problem.
* **Offer an isolated container** where the agent harness supports one. Keep credentials out of environment variables, which are readable by every child process and by anyone inspecting the container.

## Instructions

Three scopes. Put each rule in the narrowest one that still loads when it is needed.

| Scope | Loads | Holds |
|---|---|---|
| `AGENTS.md` | every session | anything true for the whole conversation |
| Nested instructions file | a file in that directory is touched | conventions for one module |
| Path-scoped rule file | a matching path is touched | instructions tied to a file type |

* **Create `AGENTS.md` if the repo has none** by running the `orient` skill, which writes it in five sections and symlinks `CLAUDE.md` to it. The check command goes under its Operational Commands; the rules below go under its Critical Constraints.
* **Cap `AGENTS.md` at 100 lines.** Anything longer belongs in a nested or path-scoped file.
* **Alias the other conventional filenames to it** with a symlink, so every tool reads one file. `orient` makes `CLAUDE.md`; add any other name the repository carries.
* **Record where a future correction goes.** State the routing in `AGENTS.md`: a static check into the rules directory, a dependency direction into the contracts, a file-specific instruction into a path-scoped rule, anything conversational into `AGENTS.md` itself. The `make-rule` skill applies this routing to each new rule.
* **Offer a decision rule for `AGENTS.md`,** verbatim. Ask before adding it.

  ```text
  # Decisions are the user's
  Before choosing between alternatives the user has not seen, put the choice and
  its tradeoff to them and wait. When the choice is expensive or irreversible,
  accepts a hazard without a test, or rejects an alternative, record it as an ADR
  before the code that depends on it: docs/adr/<slug>/<decision>.md for one
  change, docs/adr/architecture/<decision>.md for the whole repository.
  At the end of every piece of work, list every choice made without the user,
  one line each: what was chosen, why, and the tradeoff.
  ```
* **Offer an answer-length rule for `AGENTS.md`:** give the finding, what it means, and the question, then stop; name a document or diff just written rather than reproducing it. Ask before adding it. That file is the user's.
* **Never path-scope an instruction that governs the conversation.** Path frontmatter loads it only when a matching file is touched.

## Gate

* **Commit one check command** that runs the canonical gate in order and stops at the first failure: a script named `check` at the repository root, or the equivalent target where the project already has a task runner. Commit hook, CI and the agent all call that one command. Name it in `AGENTS.md`.
* **Pin every hook version.**
* **Wire automated dependency updates** so the lockfile and CI pins do not rot.
* **Gate on mutation over the diff in CI.** The `execute` loop's floor check halts when this slot is missing; a missing `e2e` slot becomes that loop's first story.

## Landing rules on existing code

Brownfield, and only where rules were accepted. Put the choice to the user:

* **Scope enforcement to files authored from here on.** The rules land today and the backlog stays where it is.
* **Clean up in a subagent, as its own change**, running in proportion to the size of the codebase.

Either is a real answer. Adding rules and leaving them red is not. The same choice applies to a failing test suite: quarantine the pre-existing failures or fix them before the suite enters the gate.
