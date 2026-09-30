# Step: refute

One `refute` agent, launched in the foreground, judges every candidate row in `findings.md` and, when it exists, `security.md`, including rows a red attack test shows, given the path of each, `done-block.md`'s path, the worktree and the merge target. When no file holds a candidate row, skip it and replace the three `pending refute` lines of `done-block.md` with `none`.

Then run `story.sh next verdicts`.
