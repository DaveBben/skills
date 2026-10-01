# Review a pull request someone opened

## Report

Write each kept finding as a Conventional Comment (format at conventionalcomments.org): a label, a decoration in parentheses, a one-line subject, then the discussion.

* **Order:** blocking comments first.
* **Rests on:** say what each comment rests on: read this run, inferred from something read this run, or asserted by a tool, a comment or the description.
* **Claims in the code:** a code comment, a docstring or the description can raise a concern and never settles one.
* **Voice:** the comments, and every reply to the author in their threads, go out under the user's name as the user's own words.
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
Rests on: read this run | inferred from <what was read> | asserted by <tool, comment or description>.
<the fix, or the one test that would settle it>
```

Use these labels and no others:

| Label | For |
|---|---|
| `issue` | A finding with a failure behind it: a criterion with no test, behaviour against production data, a name a reader cannot map to a criterion. `blocking` or `non-blocking` as the kept row says. |
| `question` | A claim that would change a rating and cannot be checked, or a decision the author did not own. Name who answers it and the test that would settle it. |
| `suggestion` | Code no test asked for. Say what to delete. |
| `todo` | A small required change with no failure of its own, such as a missing link to the ticket. Always `blocking`. |
| `praise` | At most one, naming a specific thing to keep, such as a test that pins a hard case. Never generic. |

End the report with the verdict:

```
Merge. | Changes requested: <n> blocking.
```
