---
name: semgrep-rules
description: "Use this skill whenever a convention, an anti-pattern or a security standard is to be enforced by a pattern-matching rule over source code, in any language. Use it on: 'write a semgrep rule', 'add static analysis', 'ban this pattern in the codebase', 'enforce this convention in CI', 'stop people calling X directly', 'custom lint rule', 'the agent keeps making this mistake', 'catch SQL injection automatically'. Use it when `harness` fills its rules slot, and when a bug review asks which check would have caught the bug. It covers what a rule can and cannot see, where this repository's rules come from, the rule format, the annotated fixture that proves a rule fires before it lands, and how a rule lands on code that already violates it. Do not use it to choose the wider toolchain or wire checks to editor and commit events, which is `harness`, and do not use it to review a diff by hand, which is `review` or `merge-request`."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Semgrep Rules

Write a rule only for what this repository has to enforce itself, and prove it fires before it lands.

Semgrep matches patterns against the syntax tree of a file, in most mainstream languages. Everything below applies to any other pattern engine, such as `ast-grep` or a custom ESLint, Ruff or Checkstyle rule; only the file format changes.

## Before writing anything

Climb this list and stop at the first rung that holds.

1. **A published rule set already covers it.** The registry carries packs per language, framework and topic: `p/javascript`, `p/react`, `p/python`, `p/golang`, `p/sql-injection`, `p/secrets`, `p/owasp-top-ten`. Run the ones that match the stack, read the findings, and adopt them before writing a line of YAML.
2. **Something else already prevents it.** A type checker, a compiler flag, a framework default, or a rule the project's existing linter ships. A rule that duplicates one of those adds a second place to maintain.
3. **The mistake has not happened here.** Show one real violation in this codebase first. A rule with no current violation is a preference, and the user decides whether to take it.

What is left is this repository's own conventions, and those are what you write.

## What a rule can see

* **One file at a time.** The open-source engine analyses each file alone. Following a value from one function to another inside that file is `mode: taint`. Following it across files or through an interface is the paid engine.
* **What is present, not what is missing,** except inside a scope you can name. "This call, without this option" works, because both sit in one expression. "This service, with no rate limit anywhere" does not.
* **Text, where the language is unsupported.** `languages: [generic]` with `pattern-regex` matches configuration files, templates and any language with no parser.

Say plainly which standards stay manual: anything met by something absent, anything that spans files, anything true only at runtime. Those belong in a test, a configuration check, or the merge request review.

## Where this repository's rules come from

In order of what they repay:

* **Every bug that got through.** One rule per bug whose shape a pattern can catch. This is the highest-value source, because the failure already happened.
* **Untrusted input reaching something that interprets it.** Trace each input to the database reading SQL, the browser reading HTML, the shell reading a command, the file system reading a path, the deserializer reading bytes. One sink per rule.
* **The wrapper everyone must use.** Where the repository has its own client with a timeout, its own logger that strips personal data, or its own query builder, the rule bans the raw call and names the wrapper.
* **Every review comment made more than twice,** and every confirmed review finding a pattern could match. A correction anyone repeats is a rule nobody wrote yet.

## Write the rule

Ban a specific call and name its replacement. A rule that tries to recognise a vulnerability in general fires on noise; a rule that bans one call in one repository does not.

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
      exclude:
        - "test/**"
        - "src/http.ts"
```

Where the finding depends on a value flowing from one place to another in the same file, use taint mode. Sources are where untrusted data enters, sinks are what interprets it, sanitizers are the functions that make it safe:

```yaml
rules:
  - id: request-value-reaches-sql-text
    languages: [python]
    severity: ERROR
    mode: taint
    message: >-
      A request value is being interpolated into SQL text. Pass it as a
      parameter: cursor.execute("select ... where id = %s", [value]).
    pattern-sources:
      - pattern: request.$ANYTHING
    pattern-sinks:
      - patterns:
          - pattern: $CURSOR.execute($QUERY, ...)
          - focus-metavariable: $QUERY
    pattern-sanitizers:
      - pattern: quote_identifier(...)
```

Rules that keep a rule useful:

* **One rule per file, named after the mistake.** `no-raw-fetch.yaml`, not `rule-17.yaml`.
* **The message is the fix.** State what is forbidden and what to do instead, with the replacement's real name and path. Never emit a bare identifier.
* **`severity: ERROR` only where violating it is never correct.** Everything else is `WARNING`, and a warning nobody acts on gets deleted.
* **Fewer metavariables.** `$X` and `...` widen the match and every widening costs a false positive. Start from the exact code you saw and generalise one step at a time.
* **Exclude paths in `paths:`,** never by writing exceptions into the pattern.
* **Add `fix:`** where the rewrite is mechanical, so the edit-time layer repairs it without a turn of conversation.

## Prove it fires

A rule nobody watched fail is not installed.

* **Write a fixture beside the rule with the same basename**, so `no-raw-fetch.yaml` gets `no-raw-fetch.js`. Mark each line that must fire with a `ruleid: <id>` comment on the line above, and each near-miss that must stay silent with `ok: <id>`.
* **Put a real violation in it,** copied from this codebase, alongside the corrected form of the same code.
* **Run the rule's tests** with `semgrep --test --config <rules dir>`, and check the syntax with `semgrep --validate --config <rules dir>`. Both belong in the same command list the rest of the checks run from.
* **Break it once.** Change the fixture so the rule should miss, confirm the test fails, and put it back.

## Land it

* **Commit the rules** under `.semgrep/`, one file per rule, unless the project already has a pattern engine with its own directory.
* **Run them at edit time and in CI,** from the same config: `semgrep --config .semgrep/ --error` exits non-zero on a finding. Registry packs are fetched, so vendor a copy where builds must run without a network.
* **Land on code that already violates the rule** with `--baseline-commit <sha>`, which reports only findings on lines changed since that commit. The alternative is to clean the backlog first. Adding a rule and leaving the build red is not an option.
* **Silence with a reason.** `nosemgrep: <rule-id>` on the line, followed by why. A bare silencer is a finding in the next review.
