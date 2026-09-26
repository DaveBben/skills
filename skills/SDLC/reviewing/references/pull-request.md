# Review a pull request someone opened

Loaded by the `reviewing` skill when the subject is a pull request or merge request someone opened.

The reviewer holds the diff, the description, the reports from whatever ran in the build, and the code at the merge target. It does not hold the conversation that produced the change, or the author.

## Read what it lands on, not only what it adds

Read the target for every name the change claims: a storage key, a route, a database column, an environment variable, a feature flag, an event name, a file path.

```bash
git diff --name-only <target>...HEAD      # what changed
git show <target>:<path>                  # what it lands on top of
git grep -n '<the new name>' <target>     # who already claims it
```

Run it first.

## Read what already ran first

Never redo by hand what a tool reports, and never trust a tool that did not run.

* **Mutation report over the changed lines.** A surviving mutant on a test the description lists is a finding. A mutant that cannot change behaviour is not, such as `>=` for `>` on a value that is never equal.
* **Static analysis.** It reports patterns: SQL built by joining strings, a key written into the source, output rendered without encoding.
* **Formatter and linter.** They report layout, naming conventions and complexity. Never raise by hand what they own.

Where one of these did not run, do its job on the diff and name the tool the review stood in for.

## Then read for the five things no tool reports

* **A criterion with no test.** Check the description's criterion, and each test it lists, against the tests in the diff. Read each test for an assertion that holds whatever the code does: one that checks a fake's return value, one that asserts the order of internal calls, one that replaces the very piece it claims to test.
* **Code no test asked for.** An extra config option, a helper for a case that does not arise, a parameter only ever passed its default, a new dependency. Say what to delete.
* **A decision the author did not own.** Any value or behaviour a person using the system would notice that the criterion does not state: a timeout, a disabled button, what a repeated action returns, the wording of an error. Name each one and send it to whoever owns the criteria.
* **Behaviour against production data and traffic.**
  * A migration that passes on an empty table and fails on the rows already there, such as a unique constraint over existing duplicates.
  * Two identical requests arriving at once, each reading, finding nothing, and writing. Name what stops the second, usually a constraint in the database.
  * A standard met by leaving something out, which no pattern rule can see: no rate limit, no size limit on a request body, no unique constraint.
  * A failure nobody can see: no log at the point it fails, or a log carrying personal data.
* **Names that do not match the criterion.** Code that says `status == 2` where the criterion says confirmed and unconfirmed costs every later reader, whether that reader is a person or an agent. Raise the names and the branches a reader cannot map to a criterion. Raise nothing else about style.

## Know who wrote the data

Take the answer from `AGENTS.md` at the repository root, which lists each system this product reads from and who writes the data in it; where that file does not exist, read `CLAUDE.md`. Sort each store the change touches into one of three:

* **Written outside,** where the code that writes it can be pointed at. Every field is untrusted: missing, oversized, hostile, and the wrong type. Most validation guards null and missing and forgets type, so ask what happens when a number arrives as a string.
* **Written by a person through this product's own screens.** Unsanitised text that no outsider can reach.
* **Not established,** because no such file exists, it does not list this store, or the writer is outside this repository. Say so, and name what would settle it: the file to read, or the person to ask.

## Refute before reporting

Every finding starts as a false positive and is overturned only by reading the code on the path it names, rather than the account of it in the finding. Expect most severity claims to come down.

Say what each finding rests on: read this run, inferred from something read this run, or asserted by a tool, a comment or the description. A comment raises a concern and never lowers one, and two documents by the same author are one source. A claim that would change a rating and cannot be checked ships as a question plus the one test that would settle it.

## Report

One finding per line, blocking findings first, then the rest:

```
<file>:<line> — <what breaks> — shows as: <what would show it breaking> — rests on: read this run | inferred from <what was read> | asserted by <tool, comment or description>
Refuted: <file>:<line> — <what was raised> — <why it does not hold>
Merge. | Changes requested: <n> blocking.
```

A finding with no failure behind it is a preference; leave it out.

Never rewrite the code. Every confirmed finding a pattern could match goes to the `guardrails` skill, so nothing is found by hand twice.
