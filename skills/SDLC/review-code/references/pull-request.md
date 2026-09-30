# Review a pull request someone opened

Loaded by the `review-code` skill to report on a pull request, a merge request or a diff someone opened.

The reviewer holds the diff, the description, the reports from whatever ran in the build, and the code at the merge target. It does not hold the conversation that produced the change, or the author.

The shared `review`, `security` and `refute` agents have already judged the code ("Review code" in the skill). This file turns what survived into the report.

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
