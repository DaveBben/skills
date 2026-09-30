# Review a pull request someone opened

Loaded by the `reviewing` skill for a pull request, a merge request, or a diff an agent built.

The reviewer holds the diff, the description, the reports from whatever ran in the build, and the code at the merge target. It does not hold the conversation that produced the change, or the author.

## Read what it lands on, not only what it adds

```bash
git diff --name-only <target>...HEAD      # what changed
git show <target>:<path>                  # what it lands on top of
git grep -n '<the new name>' <target>     # who already claims it
```

Run it first.

## Read what already ran first

A surviving mutant on a test the description lists is a finding. A mutant that cannot change behaviour is not, such as `>=` for `>` on a value that is never equal.

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

## Security

The security pass runs this section in its own subagent, never the reviewer that reads for the five things above. First map the diff: each entry that takes data from outside, each sink that interprets it or sends it out (a query, a shell, a template, a parser, a log, an error, a response, an outbound request), and each check of who the caller is. Trace each entry to every sink it reaches through the calls in between.

For each place the diff takes data from outside the code's control (a route, an argument, a file, a queue message, a third-party response, rows another system writes), check: its type, size and range are checked at the entry; the sink has its standard defence (a parameterized query, an argument array, template escaping, a strict deserializer); the server checks who the caller is and what it may do; sensitive data goes only where `AGENTS.md` allows and never into a log, an error or a response; no secret is written, logged or returned; an entry others reach has a size, rate or time limit; a failure leaves no half-written record another caller sees. Data from outside reaching a sink without its defence, or passing an entry with no authentication or authorization, is blocking. Check what each dependency the diff calls returns when access is denied or the resource is missing (a secret under a scoped grant, a bucket, a table), and what the code does then: a crash loop or a silent skip is a finding. Run each static analyser the repository has installed (for example Semgrep, Bandit, CodeQL) on the changed files, and raise an alert only when its path traces from an entry to a sink with no guard; most alerts are false. A request for a security review of a whole repository applies this section to every entry point.

## Know who wrote the data

Take the answer from `AGENTS.md` at the repository root, which lists each system this product reads from and who writes the data in it; where that file does not exist, read `CLAUDE.md`. Sort each store the change touches into one of three:

* **Written outside,** where the code that writes it can be pointed at. Every field is untrusted: missing, oversized, hostile, and the wrong type. Most validation guards null and missing and forgets type, so ask what happens when a number arrives as a string.
* **Written by a person through this product's own screens.** Unsanitised text that no outsider can reach.
* **Not established,** because no such file exists, it does not list this store, or the writer is outside this repository. Say so, and name what would settle it: the file to read, or the person to ask.

## Report

Write each finding that survived the refuter as a Conventional Comment: a label, a decoration in parentheses, a one-line subject, then the discussion. The format is published at conventionalcomments.org. Blocking comments come first. Say what each rests on: read this run, inferred from something read this run, or asserted by a tool, a comment or the description. A comment raises a concern and never lowers one.

The comments, and every reply to the author in their threads, go out under the user's name as the user's own words, in their voice. Before drafting them, load any installed skill for writing text in the user's voice, and write the subject and discussion by it. The label, the decoration, the anchor line and the `Rests on:` line keep the format below.

Each comment sits on one line of code:

* **One finding, one comment, one line.** Anchor it to the single line that has to change to fix it. Never anchor a comment to a range of lines, and never gather several findings into one summary comment.
* **A finding that spans lines or files** is anchored to the first line that must change. The discussion names the other lines by `<file>:<line>`.
* **A finding about something missing,** such as a criterion with no test or a query with no limit, is anchored to the changed line whose behaviour is missing the thing.
* **Take the line number from the file at the pull request's head commit,** on the new side of the diff, and check it by reading that line before posting. A code host accepts an inline comment only on a line inside the diff. When the line to fix is outside the diff, anchor to the changed line that causes it and name the other line in the discussion. On GitHub, one way is a review comment with `line` and `side: RIGHT` and no `start_line`.

```
<file>:<line>
<label> (<blocking | non-blocking>[, security]): <subject: what breaks, in one line>

<the concrete case: the input, sequence or caller>. Shows as: <what would show it breaking>.
Rests on: read this run | inferred from <what was read> | asserted by <tool, comment or description>.
<the fix, or the one test that would settle it>
```

Use these labels and no others:

| Label | For |
|---|---|
| `issue` | A finding with a failure behind it: a criterion with no test, behaviour against production data, a name a reader cannot map to a criterion. `blocking` when a caller that exists reaches it under the configuration production runs with, and a person or a caller sees the failure. |
| `question` | A claim that would change a rating and cannot be checked, or a decision the author did not own. Name who answers it and the test that would settle it. |
| `suggestion` | Code no test asked for. Say what to delete. |
| `todo` | A small required change with no failure of its own, such as a missing link to the ticket. Always `blocking`. |
| `praise` | At most one, naming a specific thing to keep, such as a test that pins a hard case. Never generic. |

End the report with the refuted findings and the verdict:

```
Refuted: <file>:<line> — <what was raised> — <the line that stops it>
Refuted by: <model>
Merge. | Changes requested: <n> blocking.
```
