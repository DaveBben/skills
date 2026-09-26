# Resume

Load this when the user asks to pick up where the work left off.

Run Orient. When several features are open, ask which one. Read the feature header and `Deferred:`, and list the story worktrees (`git worktree list`) and the open story pull requests. Skip Define and Architecture. Restart each story worktree at the step its state shows:

| State | Restart at |
|---|---|
| A pull request is open | Section 8 of `SKILL.md`, watching it |
| A parked question | Ask it again |
| A log commit and no pull request | Section 7 of `SKILL.md`, the pull request |
| A red commit and no log commit | Section 5 of [loop.md](loop.md), with a NON-NEGOTIABLE block a setup subagent rebuilds from the red commit |
| No red commit | Section 4 of [loop.md](loop.md), setup |
| A spike branch | The spike subagent, section 0 of [loop.md](loop.md) |

Then continue at section 3 of [loop.md](loop.md).
