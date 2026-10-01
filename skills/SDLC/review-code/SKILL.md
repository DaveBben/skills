---
name: review-code
description: "Use this skill when code must be reviewed or critiqued, whoever wrote it: a story branch the story skill built, a pull request or merge request, a diff, or code the user wrote, committed or not; or a design, a plan, an ADR or a fix idea the user made. Use it on: 'review PR 412', 'review this merge request', 'is this PR ready to merge', 'review my code', 'review what you built', 'security review', 'give me feedback', 'poke holes in this', 'what do you think of this approach'. Three fresh agents check each stated acceptance criterion blind to each other, one of them searching hardest for security, and a fourth keeps only the findings a red test or a cited line proves; it never rewrites the user's work."
license: MIT
metadata:
  version: "6.0.0"
---
# Review code

The subject is the thing under review. When it is ambiguous, ask once.

## Review it

Every subject gets the same review, whoever wrote it, from the plugin's `review` and `verify` agents.

* **Agent files:** each agent is one file in `../agents/<name>.md`, beside this skill's folder.
* **Launch by name** where the harness loads named agents (Claude Code's SDLC plugin installs `SDLC:review` and `SDLC:verify`). Otherwise launch a general subagent told to follow the file.
* **Launch each agent fresh,** giving paths, never file contents, and nothing from this chat.

1. **The ground:** give the agents a path to the code, and have no agent edit the user's files.
   * **Merge request:** fetch it, then check out its head detached in its own worktree. Remove the worktree after the report.
   * **Uncommitted local code:** snapshot it as a commit without touching the user's index or tree, then check that commit out the same way.
   * **Story branch:** leave it where it is, uncommitted changes included.
   * **Check command:** the one `AGENTS.md` names, else what CI runs.

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
   * Keep a row only one agent found. A row counts by its evidence, not by how many agents found it.
5. **The `verify` agent:** give it the path to `findings.md`, the subject's path or branch, the merge target, the acceptance criteria and the check command. Give it nothing from the agents that wrote the rows. It keeps a row only when a red test fails for the stated reason or a cited line shows the fault.
6. **Report** the rows `verify` kept, blocking first, as it wrote them.
   * **Merge request:** write them as comments by [references/pull-request.md](references/pull-request.md). Print them, and post only when the user says to.
   * **Failing check command:** report it as a blocking finding.

Never rewrite the work under review, and write code only when the user asks. After a report to the user, offer the `guardrails` skill once for a finding a checker could catch next time.
