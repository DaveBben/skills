# Enforce one rule

Load this when one rule, convention or recurring mistake must be enforced, when instruction files are audited for rules a check could hold, or when dependency contracts are written.

## Add one rule

1. **Restate it as something a stranger could check,** with one real violation from this codebase. A rule with no current violation is a preference; the user decides.
2. **Try rung 1, cheapest first,** and stop at the first that holds:
   * The language or framework already prevents it: turn on the compiler flag or stricter setting.
   * The linter ships it (ESLint, Ruff, golangci-lint, Clippy, RuboCop, Checkstyle, SwiftLint): search its rule list and enable it at error severity.
   * It is about which module may import which: a dependency contract (below).
   * It is about what the agent runs, not the code ("never force-push"): a hook or deny-list entry, by the Guards section of `setup.md`.
   * It is a pattern over source no shipped rule matches: a Semgrep rule (below).
   * It is a fact about behaviour ("every endpoint returns JSON errors"): a test. Say which.
3. **Rung 2** when it needs judgment and applies to some paths: one rule file per topic, the glob in its frontmatter, one imperative sentence and the reason. In Claude Code globs, `*` matches within one path segment and `**` matches across directories, so ship `"**/*.py"` to match at every depth, and touch a matching and a non-matching file to confirm.
4. **Rung 3** only when it needs judgment and applies everywhere: one line under Critical Constraints in `AGENTS.md`.
5. **Show the user the rung, the file, the exact text and the violation it catches,** and wait. Write it on a branch of its own with a pull request; handed a rule from inside a story, write it on the story's branch and list it in the pull request. When existing code already breaks it, the user picks one: enforce on new files only, clean up first as its own change, or ratchet with `scripts/ratchet.py` and a committed baseline.

## Audit the instruction files

Read `AGENTS.md`, every `CLAUDE.md`, `CONTRIBUTING.md`, `.claude/rules/`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.github/instructions/` and any review checklist. Classify each instruction line: a rung-1 candidate (it names code, a file, a command or a config value), already enforced (confirm by one violation, then delete the line), a rung-2 candidate in a global file, or stays. Report before changing anything:

```text
| # | File:line | Instruction | Move to | Mechanism | Violations today |
```

The user cuts rows by number. Convert each kept row by "Add one rule", delete the original line, and leave one pointer in `AGENTS.md` to the rules directory.

## Defend where input becomes instructions

When setting up checks for code that passes outside input to a query, a shell, a template or a parser, put the standard defence for each such place at rung 1, using the registry packs in the Semgrep section below (for example `p/owasp-top-ten`): a linter or Semgrep rule, else a framework default or a build check. Skip one a rule already covers. Say plainly what stays with the agent: anything met by something absent ("every service has a rate limit"), anything true only at runtime, anything that needs taste.

## Contracts

* **Read the shape from the latest snapshot** `AGENTS.md` points at. Write one contract per allowed dependency. With no snapshot, fill the language slots now and write contracts once the architecture exists.
* **Brownfield with no snapshot:** derive the current dependency graph, show it, and ask which edges were not expected. Those become the first contracts. Never encode the whole current graph.
* **Forbid everything else explicitly,** each named as its rule in plain English so a broken build prints the sentence that stopped being true.

## Semgrep rules

Run `semgrep --version` first; when it is missing, ask the user to install it (`pipx install semgrep`, `brew install semgrep`, or the `semgrep/semgrep` image) and wait. Say which parser tier each of the repository's languages sits in; an experimental parser silently matches less. Run the registry packs that match the stack (`p/python`, `p/react`, `p/secrets`, `p/owasp-top-ten`) before writing any rule.

A rule sees one file at a time; following a value inside that file is `mode: taint`. It sees what is present, not what is missing, except inside a scope a pattern can name. Rules repay most when they come from a bug that got through, a sink untrusted input reaches, a wrapper everyone must use, or a review comment made more than twice.

```yaml
rules:
  - id: no-raw-fetch
    languages: [javascript, typescript]
    severity: ERROR
    message: >-
      fetch() has no timeout, so a hung server holds the request forever.
      Use httpGet from src/http.ts, which sets one.
    pattern: fetch(...)
    paths:
      exclude: ["test/**", "src/http.ts"]
```

* **One rule per file,** named after the mistake, under `.semgrep/`. `ERROR` only where breaking it is never correct.
* **Start from the violation's exact code** and generalise one step at a time. Exclude paths in `paths:`, never in the pattern. Add `fix:` where the rewrite is mechanical.
* **Prove it fires:** a fixture with the same basename, `// ruleid: <id>` above each line that must fire and `// ok: <id>` above each near miss, run with `semgrep --test --config .semgrep/` and `semgrep --validate`. Break the fixture once and confirm the test fails.
* **Land it** in the command the repository already runs and in a CI job (`semgrep --config .semgrep/ --error`), pinned like the other tools. On code that already breaks it, use `--baseline-commit <sha>` or clean the backlog first. Silence a line with `nosemgrep: <rule-id>` and the reason.
