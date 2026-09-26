# Log entry

Load this when writing a story's log commit, the last commit on its branch.

* **Make the last commit on the story branch the log:** append the entry below, and rewrite `AGENTS.md` if the story added a noun, crossed a new boundary, changed a process, a module's name or Owns cell, or a flow, turned a non-goal into a goal, or is the first story (the architecture tables). One commit. On a tracker the entry is a comment on the story's issue, written when the pull request opens, which becomes its resolution at merge; the commit holds only the `AGENTS.md` rewrite, and there is no log commit when none is due. Copy each `Proposed refactor:` line from the review's Done block into the entry unchanged, marked "open". A split or new story the story exposed goes on `Stories:` in this commit and in the pull request description.

```text
## <date> — <story name>
- Done: <what shipped, one line>
- Learned: **<mechanism, one sentence>**; <the test, ADR or AGENTS.md line that pins it, or "not pinned">
- Not caught by: <bugs only: the gap, and the rule, row or hook now closing it>
- Proposed refactor: <files>; <the duplication or confusion it removes>; <the commit that did it, or "open">
- Feature test: <the feature acceptance test's failure message after this story, and the holdout's "<n> of <m> due pass" when the feature keeps one, one line; omit when it has neither>
- Observed: <seen <date>, <signal> = <value> (was <value> on <date>); appended when seen>
```

Every line is optional except `Done`, and an entry has at most six lines. One line per finding; repeat `Learned`. Nothing else goes in the entry. A finding that needs more than a line is an ADR: write it, leave the path. `Not caught by` is mandatory for a bug: name the gap in the checks `guardrails` set up or in the test table and close it in the same story, or hand it to the `guardrails` skill. When the user found a defect by reading code that the pull request's `Read code:` line did not point to, write `Not caught by: exception list;` and the `CODEOWNERS` line, or the pattern added to `read_by_exception.py`, that now points to it. Never edit or delete an entry, except to append its `Observed` line, to write a pin beside a `Learned` or `Proposed refactor` line, or to delete an unpinned line at close-out with the user's agreement. A spike's entry is titled `spike: <the question>`; the `spike` skill writes it, and its every line is a `Learned` line. Write the ADR path beside each of its `Decided alone` lines the user marked `record`.
