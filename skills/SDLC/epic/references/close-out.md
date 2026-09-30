# Close out an epic

When every child above the release line is done or cut, in this order. Each story's log comment holds `Learned`, `Proposed refactor` and `Yours:` lines; a `Parked:` comment is a question written on an issue.

1. **The feature test:** its expected-to-fail marker is gone and the suite is green, else give its failure message and propose the story that would pass it. Report each example of a named person's acceptance set with the test that holds it.
2. **What is left:** ask whether the stories below the release line become a new epic or are cut. Turn each unpinned `Learned` line, from the stories' log comments and the comments on the epic, into a test, an ADR or an `AGENTS.md` line on one last branch, or delete it with the user's agreement. Put each open `Proposed refactor` to the user. Delete the `Parked:` comments.
3. **Whether it worked:** ask whether the `Success` signal moved, and which pause cost time without catching anything, for the `guardrails` skill.
4. **The user's model:** when `docs/architecture/summary.md` exists (the one-page summary the user writes in their own words), quote its ranked qualities and its risks and ask which line this feature made wrong; the user edits it or says none. Name one design lesson in four lines: the structural decision the feature's code made (a module boundary, a data shape, where the input and output happen), the pattern it follows by its name, the alternative not taken, and the condition under which that alternative would win.
5. **The user's pattern,** as counts with no judgement, from the stories' `Yours:` log lines and the ADRs: cores written, sketches written and turns skipped; `Read first:` hunks shown; confirmations as shown and edited; ADR reasons the user wrote against ones the agent drafted and the user left.
6. **Close the epic.**
