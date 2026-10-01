---
name: review-code
description: "Use this skill when code must be reviewed or critiqued, whoever wrote it: a story branch the deliver skill built, a pull request or merge request, a diff, or code the user wrote, committed or not; or a design, a plan, an ADR or a fix idea the user made. Use it on: 'review PR 412', 'review this merge request', 'is this PR ready to merge', 'review my code', 'review what you built', 'security review', 'give me feedback', 'poke holes in this', 'what do you think of this approach'. Three fresh agents check each stated case blind to each other, one of them searching hardest for security, and a fourth keeps only the findings a red test or a cited line proves; it never rewrites the user's work."
license: MIT
metadata:
  version: "6.0.0"
---
# Review code

The subject is the thing under review. When it is ambiguous, ask once.

## Review it

Every subject gets the same review whoever wrote it, from the plugin's `review` and `verify` agents. Each is defined by one file in the plugin's `agents/` folder, beside this skill's folder (`../agents/<name>.md`). Where the harness loads named agents, launch each by name (Claude Code's SDLC plugin installs them as `SDLC:review` and `SDLC:verify`); otherwise launch a general subagent told to follow its file. Launch each fresh. Give each paths, never file contents, and nothing from this chat.

1. **The ground.** Check a merge request's head out detached in its own worktree (`git worktree add --detach <path> <commit>`, after fetching it) and give the agents that path; remove the worktree after the report. A story branch and the user's local code stay where they are, uncommitted changes and all. The **check command** is the one `AGENTS.md` names, else what CI runs.
2. **The cases.** Write the subject's intent as numbered cases, each a behaviour with concrete values: a story's cases as written; for a merge request, each behaviour its description, its linked ticket's acceptance criteria and its commit messages state; for the user's code or document, what the user says it is for, and when they have not said, ask once. The agents get the cases and never the prose they came from: a claim that the code is safe, tested or reviewed, the author's name, an earlier review's verdict and what a failure would cost each sway a reviewer's verdict.
3. **Three `review` agents,** launched together, each given its number and focus (1 `correctness`, 2 `tests and production`, 3 `security`), the subject, its path or branch, the merge target, the cases in a different order for each, the check command, and for a story the red commit's hash. They work blind to each other. For a security review the user asked for, give all three the `security` focus.
4. **Merge** the three `findings-<n>.md` files into `findings.md` in the same git directory. Rows that name the same line and the same wrong result become one row carrying every piece of evidence. Keep a row that only one agent found: a row counts by its evidence, not by how many agents found it.
5. **The `verify` agent,** given the path to `findings.md`, the subject's path or branch, the merge target, the cases and the check command, and nothing from the agents that wrote the rows. It keeps a row only when a red test fails for the stated reason or a cited line shows the fault, and drops the rest.
6. **Report** the rows `verify` kept, blocking first, as it wrote them. For a merge request, write them as comments by [references/pull-request.md](references/pull-request.md) instead; print them, and post them only when the user says to. A failing check command is a blocking finding.

Never rewrite the work under review, and write code only when the user asks. After a report to the user, offer the `guardrails` skill once for a finding a checker could catch next time.
