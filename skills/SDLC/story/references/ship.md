# Ship a story

The pull request is open. Follow it to production and prove the story there.

1. **CI:** read the pull request's pipeline and gates, such as `gh pr checks` or `glab ci status`.
    * **A failure this branch causes:** reproduce it locally, fix it by [implement.md](implement.md)'s steps, with a failing test first where a test can show it, and push.
    * **A failure that also fails on main, or a runner or infrastructure fault:** report it to the user with the failing log lines, and leave it unfixed on this branch.
2. **Watch the pull request** every 15 minutes for up to 8 hours, until it is merged or closed. Use the harness's scheduler, such as Claude Code's `/loop 15m`.
    * **Each check:** read the pipeline as step 1 does, and read the comments that are new since the last check.
    * **A review comment:** check its claim against the code before acting on it. A confirmed defect gets a failing test, then the fix, then a push. A question, or a claim the code does not bear out, goes to the user with its evidence.
    * **Closed without a merge, or 8 hours with none:** report what is pending and stop.
    * **No scheduler:** tell the user, and stop at the open pull request.
3. **The user merges.** Never run a pull request merge or merge into main.
4. **Outcome check:** confirm the story's acceptance criteria hold in production before the story is done.
    * **Wait for the deploy:** a deploy job, a release or a deployment record shows the merge commit in production. When nothing shows it, ask the user.
    * **Observe each example's `then`** in production with a tool: the route, the page, a query, the logs. Only read. An example that needs a write to production data, or one marked `(checked by the user)`, goes to the user.
    * **Not observable yet,** such as a nightly job or a daily total: set a wakeup for when it is, such as a one-time run by Claude Code's `/schedule`. Without a scheduler, give the user the date and stop.
    * **A bug fix:** the reproduction no longer reproduces in production. A change with no behaviour change ends at the merge.
5. **Done or not:**
    * **Every `then` observed:** the story is done. Comment the evidence on its issue and close it by the `using-trackers` skill. Without a tracker, report the evidence.
    * **One is not:** file it by the `bug` skill as a bug linked to the story, which reproduces and fixes it through this path. The story's issue stays open, blocked by the bug's issue, and closes when the fix passes its outcome check.
    * **Report** the result, and tell the user to start the next story in a fresh session.

## Measure the feature

Run this once every story of the feature is merged and the date on the owning story's `Measure:` line has passed, or when the user asks how a feature did. Read the measure with a tool where one reaches it, else ask the user for it. Write the value and the date on its `Result:` line and report whether it met the target. A miss becomes new stories or a decision for the user; no merged story reopens.
