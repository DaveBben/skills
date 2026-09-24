---
name: make-rule
description: "Use this skill whenever a rule for code or for the agent is to be added, or existing instructions are to be turned into checks. Use it on: 'add a rule', 'make this a rule', 'always do X', 'never do Y', 'add this to CLAUDE.md', 'add this to AGENTS.md', 'the agent keeps making this mistake', 'enforce this convention', 'ban this pattern', 'stop people calling X directly', 'write a semgrep rule', 'custom lint rule', 'add static analysis', 'catch SQL injection automatically', 'which of these instructions could be lint rules', 'audit CLAUDE.md'. Use it when `harness` fills its rules slot, and when a review asks which check would have caught a bug. Puts each rule in the first place that holds: a check that fails deterministically (a linter setting, a Semgrep rule, a type check), then a path-scoped agent rule file, then one line in AGENTS.md. Do not use it to choose the toolchain or wire checks to editor and commit events (`harness`), or to write AGENTS.md itself (`orient`)."
license: MIT
compatibility: any-agent
metadata:
  version: "2.0.0"
---
# Make Rule

A rule a program checks is followed every time. A rule an agent reads is followed when the agent remembers it. Put every rule as far up this ladder as it will go.

| Rung | Where the rule lives | Use when |
| --- | --- | --- |
| 1. Deterministic | A linter setting, a Semgrep rule, a type check, a dependency contract, a test | A program can decide pass or fail from the code, the config or the command alone |
| 2. Scoped agent rule | A rule file the agent loads only for matching paths (`.claude/rules/*.md` with `paths:`, `.cursor/rules/*.mdc` with `globs:`, `.github/instructions/*.instructions.md` with `applyTo:`), or a nested `AGENTS.md` in one module's directory | It needs judgment, and it applies to some paths, one kind of file or one module |
| 3. Agent instructions | One line in `AGENTS.md` | It needs judgment, and it applies everywhere |

Use the rule-file format of the agent this repository already configures. When the repository configures none, and the agent in use has no path-scoped format, the rule goes to rung 3.

## Add one rule

1. **Restate the rule as something a stranger could check.** "Keep the API clean" is not a rule yet. Ask what a violation looks like, and ask for one real example from this codebase.
2. **Try rung 1, cheapest first.** Stop at the first that holds.
   * **The language or framework already prevents it:** a compiler flag, a stricter type-checker setting, a framework default. Turn it on.
   * **The project's linter ships the rule:** ESLint, Ruff, golangci-lint, Clippy, RuboCop, Checkstyle, SwiftLint. Search that linter's rule list before writing anything. Enable the rule in the existing config at error severity, with the options the rule needs.
   * **The rule is about which module may import which:** it is a dependency contract. Hand it to `harness`, which owns contracts.
   * **The rule is about what the agent runs, not the code it writes:** "never force-push", "never edit the migrations directory". It is a hook or a deny-list entry in the agent's settings. Hand it to `harness`, which owns both.
   * **The rule is a pattern over source that no shipped rule matches:** write a Semgrep rule. Load [references/semgrep.md](references/semgrep.md) now. It covers installing the engine, what a pattern can and cannot see, writing the rule, proving it fires, and landing it on code that already breaks it.
   * **The rule is a fact about behaviour:** "every endpoint returns JSON errors". It is a test, not a lint rule. Say which test would hold it.
3. **Fall to rung 2** when no program can decide it but the rule applies only to some paths, such as "components in `src/ui/` take props, never read the store". Write one rule file per topic, with the path glob in its frontmatter and the rule as one imperative sentence plus the reason. Check how the format matches globs. Claude Code uses gitignore rules, so `"*.py"` matches only files at the root, and the file needs `"**/*.py"` as well. Touch one matching file and one non-matching file to confirm the rule loads for the first only.
4. **Fall to rung 3** only when the rule needs judgment and applies everywhere, such as "ask before adding a dependency". Add one line under the constraints section `AGENTS.md` already has. When `AGENTS.md` does not exist, offer `orient` first.
5. **Show the user the rung, the file, the exact text or config, and one real violation it catches** before writing it. A rule with no current violation is a preference, and the user decides whether to take it.

Every rung-1 rule prints a message the agent reads when it fails. Write that message as the fix: what is forbidden, what to use instead, and the replacement's real name and path.

## Audit the instruction files

Read every file that tells a person or an agent what to do: `AGENTS.md`, `CLAUDE.md` at every level, `CONTRIBUTING.md`, `.claude/rules/`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.github/instructions/`, and any review checklist. Classify each instruction line by the ladder.

* **Rung 1 candidates** name code, a file, a command or a config value: "never call the HTTP client directly, use `httpGet`", "no `any` in exported types", "every query goes through the repository layer", "run the formatter before committing".
* **Already enforced:** the line restates something a check this repository runs already fails on. Run the check with one violation to confirm, then delete the line.
* **Rung 2 candidates** in a global file: the line only makes sense for some paths.
* **Stays where it is:** the line needs judgment and applies everywhere, such as "keep functions small" or "prefer composition".

Search the codebase for a real violation of each rung-1 candidate. Report before changing anything:

```text
| # | File:line | Instruction | Move to | Mechanism | Violations today |
|---|-----------|-------------|---------|-----------|------------------|
| 1 | CLAUDE.md:14 | "never use fetch directly" | rung 1 | Semgrep rule no-raw-fetch | 3 (src/api/user.ts:22, ...) |
| 2 | AGENTS.md:31 | "no default exports" | rung 1 | ESLint import/no-default-export | 0 |
| 3 | CLAUDE.md:40 | "UI components never read the store" | rung 2 | .claude/rules/ui.md, paths: src/ui/** | - |
| 4 | AGENTS.md:9 | "run prettier first" | delete | already failed by the format check | - |
```

The user cuts rows by number, and a row not cut is accepted. Convert each accepted row with the steps in "Add one rule". When a rule lands at rung 1 or rung 2, delete the original instruction line. Leave one pointer in `AGENTS.md` to the rules directory, so a reader knows the rules exist.

## What a check cannot hold

Say plainly which rules stay with the agent: anything met by something absent ("every service has a rate limit"), anything true only at runtime, and anything that needs taste. Those are rung 2 or rung 3, or a criterion the `story` skill writes, or a point for the merge request review.
