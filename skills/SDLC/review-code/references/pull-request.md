# Review a pull request someone opened

## Report

Write each kept finding as a Conventional Comment (format at conventionalcomments.org): a label, a decoration in parentheses, a one-line subject, then the discussion.

* **Order:** blocking comments first.
* **Rests on:** copy each row's `proof:` field: the run, or the traced lines.
* **Voice:** write the comments and every reply in their threads as the user's own words, using the user's writing-voice skill when one is installed.
* **Format:** the label, the decoration, the anchor line and the `Rests on:` line keep the format below.

Each comment sits on one line of code:

* **One finding, one comment, one line:** anchor it to the single line that has to change to fix it. Never anchor to a range, and never gather findings into a summary comment.
* **A finding that spans lines or files:** anchor it to the first line that must change, and name the other lines by `<file>:<line>` in the discussion.
* **A finding about something missing:** anchor it to the changed line whose behaviour lacks the thing, such as a criterion with no test or a query with no limit.
* **Line number:** take it from the file at the pull request's head commit, on the new side of the diff, and read that line before posting.
* **Line outside the diff:** a code host accepts an inline comment only inside the diff. Anchor to the changed line that causes it, and name the other line in the discussion.
* **GitHub:** post a review comment with `line` and `side: RIGHT` and no `start_line`.

```
<file>:<line>
<label> (<blocking | non-blocking>[, security]): <subject: what breaks, in one line>

<the concrete case: the input, sequence or caller>. Shows as: <what would show it breaking>.
Rests on: <the run> | <the traced lines>.
<the fix, or the one test that would settle it>
```

Label each comment by the type of the kept row, and use no other label:

| Row type | Label |
|---|---|
| `finding` or `weak test` | `issue`, `blocking` or `non-blocking` as the row says. |
| `question` | `question`, `non-blocking`. Name who answers it and the test that would settle it. |

End the report with the verdict:

```
Merge. | Changes requested: <n> blocking.
```
