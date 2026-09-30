# Enforce one rule

Load this when one rule, convention or recurring mistake must be enforced, when instruction files are audited for rules a check could hold, or when dependency contracts are written.

## Add one rule

1. **Restate it as something a stranger could check,** with one real violation from this codebase. A rule with no current violation is a preference; the user decides.
2. **Try rung 1, cheapest first,** and stop at the first that holds:
   * The language or framework already prevents it: turn on the compiler flag or stricter setting.
   * The linter ships it (ESLint, Ruff, golangci-lint, Clippy, RuboCop, Checkstyle, SwiftLint): search its rule list and enable it at error severity.
   * It is about which module may import which: a dependency contract (below).
   * It is about what the agent runs, not the code ("never force-push"): a hook or deny-list entry, by the guards stage (`scripts/setup-next.sh <repository> guards` prints it).
   * It is a pattern over source no shipped rule matches: a Semgrep rule ("Semgrep rules", below).
   * It is a fact about behaviour ("every endpoint returns JSON errors"): a test. Say which.
3. **Rung 2** when it needs judgment and applies to some paths: one rule file per topic, the glob in its frontmatter, one imperative sentence and the reason. In Claude Code globs, `*` matches within one path segment and `**` matches across directories, so ship `"**/*.py"` to match at every depth, and touch a matching and a non-matching file to confirm.
4. **Rung 3** only when it needs judgment and applies everywhere: one line under Critical Constraints in `AGENTS.md`.
5. **Show the user the rung, the file, the exact text and the violation it catches,** and wait. Write it on a branch of its own with a pull request; handed a rule from inside a story, write it on the story's branch and list it in the pull request. When existing code already breaks it, the user picks one: new code only (for Semgrep, `--baseline-commit <sha>`), a cleanup first as its own change, or a ratchet with `scripts/ratchet.py` and a committed baseline.

## Audit the instruction files

Read `AGENTS.md`, every `CLAUDE.md`, `CONTRIBUTING.md`, `.claude/rules/`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.github/instructions/` and any review checklist. Classify each instruction line: a rung-1 candidate (it names code, a file, a command or a config value), already enforced (confirm by one violation, then delete the line), a rung-2 candidate in a global file, or stays. Report before changing anything:

```text
| # | File:line | Instruction | Move to | Mechanism | Violations today |
```

The user cuts rows by number. Convert each kept row by "Add one rule", delete the original line, and leave one pointer in `AGENTS.md` to the rules directory.

## Defend where input becomes instructions

When setting up checks for code that passes outside input to a query, a shell, a template or a parser, put the standard defence for each such place at rung 1, using Semgrep registry packs such as `p/owasp-top-ten`, run by the Semgrep subagent below: a linter or Semgrep rule, else a framework default or a build check. Skip one a rule already covers. Say plainly what stays with the agent: anything met by something absent ("every service has a rate limit"), anything true only at runtime, anything that needs taste.

## Contracts

* **Read the shape from the latest snapshot** `AGENTS.md` points at. Write one contract per allowed dependency. With no snapshot, fill the language slots now and write contracts once the architecture exists.
* **Brownfield with no snapshot:** derive the current dependency graph, show it, and ask which edges were not expected. Those become the first contracts. Never encode the whole current graph.
* **Forbid everything else explicitly,** each named as its rule in plain English so a broken build prints the sentence that stopped being true.

## Semgrep rules

Semgrep rules repay most when they come from a bug that got through, a sink untrusted input reaches, a wrapper everyone must use, or a review comment made more than twice.

Hand each Semgrep rule, or the registry packs to wire for a stack, to a fresh subagent (in Claude Code, the Agent tool) with the path of `references/semgrep.md`, the branch, and either the rule restated with the violation's file and line or the stack's languages and frameworks. It writes the rule, its fixture and the wiring, uncommitted, and returns the files, the test result and each language's parser tier; show them to the user by step 5 of "Add one rule". When it returns `Semgrep missing`, ask the user to install it (`pipx install semgrep`, `brew install semgrep`, or the `semgrep/semgrep` image) and wait. Where the harness cannot launch a subagent, read `references/semgrep.md` and do its task yourself.
