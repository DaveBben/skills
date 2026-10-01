# Write a Semgrep rule

You are given a rule restated so a stranger could check it, one real violation (file and line), and the branch to work on; or a request to wire the registry packs for a stack. Leave every change uncommitted. You cannot ask the user anything; return instead.

## Before writing

* **Semgrep present:** run `semgrep --version` first. When it fails, stop and return `Semgrep missing`.
* **Parser tier:** say which tier each of the repository's languages sits in. An experimental parser silently matches less.
* **Registry packs:** run those that match the stack (`p/python`, `p/react`, `p/secrets`, `p/owasp-top-ten`) before writing any rule. Write none for what a pack already catches.

A rule sees one file at a time. Following a value inside that file is `mode: taint`. A rule sees what is present, not what is missing, except inside a scope a pattern can name.

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

## Writing it

* **Message:** say what is forbidden and what to do instead, never a bare rule identifier.
* **One rule per file,** named after the mistake, under `.semgrep/`.
* **Severity:** `ERROR` only where breaking the rule is never correct.
* **Pattern:** start from the violation's exact code and generalise one step at a time.
* **Exclusions:** put them in `paths:`, never in the pattern.
* **Fix:** add `fix:` where the rewrite is mechanical.

## Prove it fires

* **Fixture:** same basename as the rule, with `// ruleid: <id>` above each line that must fire and `// ok: <id>` above each near miss.
* **Run:** the two commands below.
* **Break the fixture once** and confirm the test fails.

```sh
semgrep --test --config .semgrep/
semgrep --validate
```

## Wire it

* **Into `./check`** at the repository root: `semgrep --config .semgrep/ --error`.
* **Existing code already breaks the rule:** wire nothing for that code and return the count of findings. The user picks new code only (`--baseline-commit <sha>`), a cleanup first, or a ratchet.
* **Silencing a line:** `nosemgrep: <rule-id>` and the reason.

## Return

* Each file written.
* The `semgrep --test` and `--validate` results.
* Each language's parser tier.
* The pack findings.
* The count of existing violations.
