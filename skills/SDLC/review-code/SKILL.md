---
name: review-code
description: "Use this skill when code must be reviewed or critiqued, whoever wrote it: a story branch the story skill built, a pull request or merge request, a diff, uncommitted changes, or a file the user wrote; or a design, a plan, an ADR or a fix idea the user made. Use it on: 'review this code', 'do a code review', 'review PR 412', 'look at this merge request', 'is this PR ready to merge', 'review my changes', 'review the diff', 'review my uncommitted changes', 'sanity check my diff before I push', 'check this file for bugs', 'review what you built', 'security review', 'give me feedback', 'poke holes in this', 'what do you think of this approach'. Load it before reading the diff or the files. Reviews it with fresh agents whose findings must be proven by a failing test or a cited line, and never rewrites the user's work. Not for written user stories or acceptance criteria; that is `story`."
license: MIT
metadata:
  version: "6.0.0"
---
# Review code

The subject is the thing under review. When it is ambiguous, ask once.

## Review it

Review every subject with the `review` and `verify` agents.

* **Launch by name** (`SDLC:review`, `SDLC:verify`) where the harness loads named agents, else launch a general subagent told to follow `../agents/<name>.md`.
* **Launch each agent fresh,** giving paths, never file contents, and nothing from this chat.

1. **The ground:** give the agents a path to the code, and have no agent edit the user's files.
   * **Merge request:** fetch it, then check out its head detached in its own worktree.
   * **Uncommitted local code:** snapshot it as a commit without touching the user's index or tree, then check that commit out the same way. Its merge target is the snapshot's parent, `HEAD`, unless the user names a branch.
   * **Committed local branch:** check out its head detached the same way.
   * **A file with no pending change:** give its path and no merge target; the agents review the whole file.
   * **Story branch:** leave it where it is, uncommitted changes included.
   * **Design, plan, ADR or fix idea:** give its file path with the code it lands on. When it exists only in this chat, write it to `design.md` in the git directory first and give that path.
   * **New worktree:** run the repository's install step there (the setup line of `AGENTS.md`, else the README's) before launching any agent. A check that fails on setup is a setup error to report to the user, not a finding.
   * **Cleanup:** remove each worktree this skill added after the report.
   * **Check command:** the `Full check:` line of `AGENTS.md`, else its `Check:` line, else what CI runs.

   ```sh
   git worktree add --detach <path> <commit>
   # snapshot: prints the commit hash
   i=$(mktemp -u); GIT_INDEX_FILE=$i git add -A && GIT_INDEX_FILE=$i git commit-tree $(GIT_INDEX_FILE=$i git write-tree) -p HEAD -m snapshot; rm -f $i
   ```

2. **The acceptance criteria:** write the subject's intent as numbered acceptance criteria, each a behaviour with concrete values.
   * **Story:** its acceptance criteria as written.
   * **Merge request:** each behaviour its description, linked ticket and commit messages state.
   * **User's code or document:** what the user says it is for. Ask once when they have not said.
   * **Give the agents the criteria only,** never the prose they came from. A claim that the code is safe, tested or reviewed, the author's name, an earlier verdict and the cost of a failure all sway a reviewer.
3. **Three `review` agents:** launch them together, blind to each other. Give each:
   * its number and focus (1 `correctness`, 2 `tests and production`, 3 `security`);
   * the subject, its path or branch, and the merge target;
   * the acceptance criteria, in a different order for each;
   * the check command, and for a story the red commit's hash.

   For a security review the user asked for, give all three the `security` focus.
4. **Merge** the three `findings-<n>.md` files into `findings.md` in the same git directory.
   * Rows that name the same line and the same wrong result become one row carrying every piece of evidence.
   * Keep every row, including a row only one agent found. A row counts by its evidence, not by how many agents found it.
   * Number the merged rows 1 to n.
5. **The `verify` agent:** give it the path to `findings.md`, the subject's path or branch, the merge target, the acceptance criteria and the check command. It keeps a row only when a red test fails for the stated reason or a cited line shows the fault. Then delete each `attack-<n>/` directory the review agents left in the subject's tree.
   * **One round:** review, merge, verify, report. After `verify` returns, do not launch more `review` agents or a second `verify`.
6. **Report** the rows `verify` kept, blocking first, as it wrote them.
   * **Merge request:** write them as comments by [references/pull-request.md](references/pull-request.md). Print them, and post only when the user says to.
   * **Other subjects:** print the kept rows, blocking first, then the verdict line from `pull-request.md`, without anchors.
   * **Failing check command:** report it as a blocking finding.

Write code only when the user asks. After a report to the user, offer the `guardrails` skill once for a finding a checker could catch next time.
