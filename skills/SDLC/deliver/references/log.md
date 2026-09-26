# Log entry

Load this when writing a story's log comment, a comment on its issue.

* **Write the entry below as a comment on the story's issue when its pull request opens;** at merge it becomes the resolution. The last commit on the story branch rewrites `AGENTS.md` when the story added a noun, crossed a new boundary, changed a process, a module's name or Owns cell, or a flow, turned a non-goal into a goal, or is the first story (the architecture tables); otherwise there is no such commit. Copy each `Proposed refactor:` line from the review's Done block into the entry unchanged, marked "open". A split or new story the story exposed becomes a child issue of the epic and is named in the pull request description.

```text
- Done: <what shipped, one line>
- Learned: **<mechanism, one sentence>**; <the test, ADR or AGENTS.md line that pins it, or "not pinned">
- Not caught by: <bugs only: the gap, and the rule, row or hook now closing it>
- Proposed refactor: <files>; <the duplication or confusion it removes>; <the commit that did it, or "open">
- Feature test: <the feature acceptance test's failure message after this story, and the holdout's "<n> of <m> due pass" when the feature keeps one, one line; omit when it has neither>
- Observed: <seen <date>, <signal> = <value> (was <value> on <date>); appended when seen>
```

Every line is optional except `Done`, and an entry has at most six lines. One line per finding; repeat `Learned`. Nothing else goes in the entry. A finding that needs more than a line is an ADR: write it, leave the path. `Not caught by` is mandatory for a bug: name the gap in the checks `guardrails` set up or in the test table and close it in the same story, or hand it to the `guardrails` skill. When the user found a defect by reading code that the pull request's `Read code:` line did not point to, write `Not caught by: exception list;` and the `CODEOWNERS` line, or the pattern added to `read_by_exception.py`, that now points to it. Never edit or delete an entry, except to write a pin beside a `Learned` or `Proposed refactor` line, or to delete an unpinned line at close-out with the user's agreement, where the tracker allows. A spike's findings are its issue's resolution comment; the `spike` skill writes it, and its every line is a `Learned` line. Write the ADR path beside each of its `Decided alone` lines the user marked `record`.
