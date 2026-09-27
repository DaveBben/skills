# Resume

Load this when the user asks to pick up where the work left off.

Run Orient. When several features are open, ask which one. Read the epic's description and `Deferred:`, each `Parked:` comment, and the output of [story.sh](../scripts/story.sh) `status` run from the main checkout. It prints one line per story worktree with where it restarts, by the table below, and closes each story whose pull request merged. Where `gh` is not installed it cannot see pull requests, so check them by hand. It cannot see the tracker, so a `Parked:` comment overrides its line. Skip Define and Architecture. Restart each story worktree at the step its state shows:

| State | Restart at |
|---|---|
| A pull request is open | Section 8 of `SKILL.md`, watching it |
| A parked question | Ask it again |
| A Done block file and no pull request | Section 7 of `SKILL.md`, the log comment and the pull request |
| A red commit and no Done block file | Section 5 of [loop.md](loop.md), with a NON-NEGOTIABLE block a setup subagent rebuilds from the red commit |
| No red commit | Section 4 of [loop.md](loop.md), setup |
| A spike branch | The spike subagent, section 0 of [loop.md](loop.md) |

Then continue at section 3 of [loop.md](loop.md).
