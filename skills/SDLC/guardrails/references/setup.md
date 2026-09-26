# Set up the checks

Loaded by the `guardrails` skill when a repository's automated checks must be set up or repaired. The rules under "What never bends" in SKILL.md apply to every step here.

Identify the language, pick the tool, and name the pick.

Decide nothing about what the system should be. Framing and slicing belong to `define-work`, the system's shape to `architecture`, and building to `deliver`.

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
* **Halt before a cleanup that rewrites files an open `story/{slug}/` branch touches.** Stories run in parallel, so a branch is usually open. Compare the cleanup's files with each open branch's diff against main. On an overlap, offer the config-only subset now with that cleanup deferred, or finishing the story first.
* **Resume at the first missing output** when a repository is part-way through this skill.


## Survey

* **Record the language, package manager, agent harness, and which slots already have a tool.** State it in one table before proposing anything, one row per slot:

  ```text
  | Slot | Tool now | Fires | Proposed |
  |---|---|---|---|
  | fast_fix | none | - | <tool> |
  | types | <tool> | manual only | wire to turn end |
  ```

* **Name every conflict before changing it:** two tools covering one slot, two package managers, a manifest with no lockfile, or config in a file the new tool will not read. Where a newer tool subsumes an older one, say which rules the older carries that the newer does not.
* **Propose the migration; never perform it.** On greenfield, take all of it.

## Slots

Load `references/toolchain.md` now, before writing any config. SKILL.md lists it.

* **Config goes to disk, not into the chat.** Name the file and the one line in it the user would argue with.
* **Take the tool's defaults** except for the settings that reference names explicitly. Each of those has a silent failure mode.
* **Delegate the mechanical work** to subagents where the agent harness allows it, in parallel where it divides: the lint cleanup, landing rules on existing code, deriving the dependency graph, any bulk rewrite a new rule forces. Pick the cheapest model per job and say which. Where subagents are unavailable, warn the user that a cleanup runs inline and holds the session.

## Contracts

* **Read the shape from `AGENTS.md`.** The `architecture` skill writes the modules, what each owns, and the flows between them into the Architecture block of `AGENTS.md`. Write one contract per flow that stays inside one process, and delete that flow's row from the Flows table in the same commit. When that block does not exist yet, say so, fill the language-level slots now, and encode contracts after `architecture` has drawn the shape. Never ask the user to draw the modules here.
* **Brownfield with no Architecture block:** Derive the current dependency graph, render it as a diagram, and ask which edges they did not expect. Those are the ones nobody chose, and they become the first contracts. Never encode the whole current graph.
* **One contract per allowed-dependency line.** Everything not listed is forbidden, and the config says so explicitly.
* **Write each contract's name as the rule in plain English**, so a broken build prints the sentence that stopped being true.
* **Name the shape when it has a name.** When the user's modules match a known pattern (hexagonal, layered, MVI), record the name and its one defining rule in `AGENTS.md`.
* **The contracts are the record.** Never write a separate architecture document to describe them.

## Rules

Write each rule by `references/rules.md`.

* **Brownfield only.**
* **Offer the anti-pattern sweep and the rules as one decision.**
* **Ask the agent what anti-patterns this codebase uses**, put the list to the user, then encode the practices already visible in the code and those anti-patterns as their inverse.
* **Show each rule with one real violation it catches** before adding it. A rule with no current violation is a preference; say so and let the user choose.

## Loop

Where the agent harness is Claude Code, load `references/claude-guardrails.md` now and write the files it carries; for one rule, write only its entry. Another agent harness wires the same three layers to whatever events it exposes. Where it exposes none, say so plainly: the checks still run at commit time and in CI, and feedback arrives a turn later instead of immediately.

* **Three layers, each a subset of one command list.**
* **Auto-fix everything mechanically fixable and silence it.** Surface only what needs a decision.
* **Count the retries per session.** Increment on each block, clear on a pass, give up after three, then let the turn end and say so.
* **Re-verify after each fix**, rather than checking once and standing down.
* **Skip when nothing relevant changed.**
* **Fail open when the tool itself breaks.** Distinguish "the checker found problems" from "the checker could not run", or a missing dependency phantom-blocks every edit.
* **Scope to this repository.** A session can hold other working directories and these rules do not apply there.

## Guards

* **Hard blocks: two entries, and justify a third.** A rule earns a slot only when violating it is never correct and the harness cannot catch it afterwards. Blocking the flag that skips the commit gate qualifies. Blocking a package manager the project does not use is blocklist creep.
* **Block edits to accepted tests.** While `deliver` has a red commit recorded, refuse any edit to a file that commit touched, at edit time. An instruction to leave tests alone is not a substitute for the guard.
* **Deny agent edits to the feature acceptance tests for good.** The `deliver` loop keeps the user's acceptance test for a whole feature in a `feature-acceptance` directory inside the test tree. Deny edits, writes and deletes there permanently, for the agent and every subagent.
* **Deny reads and writes outright** for secrets files, the lockfile, and the version control directory.
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
* **Record where a future correction goes.** State the routing in `AGENTS.md`: a static check into the rules directory, a dependency direction into the contracts, a file-specific instruction into a path-scoped rule, anything conversational into `AGENTS.md` itself. `references/rules.md` applies this routing to each new rule.
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
* **Offer an answer-length rule for `AGENTS.md`:** give the finding, what it means, and the question, then stop; name a document or diff just written rather than reproducing it. Ask before adding it.
* **Never path-scope an instruction that governs the conversation.** Path frontmatter loads it only when a matching file is touched.

## Gate

* **Commit the check command** that runs `references/toolchain.md`'s canonical gate in order and stops at the first failure. Name it in `AGENTS.md`.
* **Ask the user for a time limit on the whole test run** and write it in `AGENTS.md`. The `tests` slot fails past it, so a suite that grows with every story is noticed before it drifts out of the commit gate.
* **Pin every hook version.**
* **Wire automated dependency updates** so the lockfile and CI pins do not rot.
* **Gate on mutation over the diff in CI.** The `deliver` loop offers this skill when this slot is missing and continues with mutations applied by hand when the user declines. When the `e2e` slot is missing, that loop's first story adds the runner.

## Landing rules on existing code

Brownfield, and only where rules were accepted. Put the choice to the user:

* **Scope enforcement to files authored from here on.** The rules land today and the backlog stays where it is.
* **Clean up in a subagent, as its own change**, running in proportion to the size of the codebase.

Either is a real answer. Adding rules and leaving them red is not. The same choice applies to a failing test suite: quarantine the pre-existing failures or fix them before the suite enters the gate.
