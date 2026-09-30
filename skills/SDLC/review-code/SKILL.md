---
name: review-code
description: "Use this skill when code must be reviewed or critiqued, whoever wrote it: a pull request or merge request, a diff, or code the user wrote, committed or not; or a design, a plan, an ADR or a fix idea the user made. Use it on: 'review PR 412', 'review this merge request', 'is this PR ready to merge', 'review my code', 'review what you built', 'security review', 'give me feedback', 'poke holes in this', 'what do you think of this approach'. Reviews it with attack tests and a second agent that must disprove each finding, and never rewrites the user's work."
license: MIT
metadata:
  version: "4.0.0"
---
# Review code

## Pick the review

The subject is the thing under review. When it is ambiguous, ask once.

| Subject | How | Output |
|---|---|---|
| A pull request, a merge request or a diff someone opened | "Review code" below, then [references/pull-request.md](references/pull-request.md) for the report | Conventional Comments, blocking first, then Merge or Changes requested, printed; posted only when the user says to |
| Code the user wrote, committed or not | "Review code" below, then [references/feedback.md](references/feedback.md) for the reply | Points sorted into Wrong, Unverified, Shape and Preference |
| A design, a plan, an ADR or a fix idea the user made | [references/feedback.md](references/feedback.md), read inline, then the `refute` agent | Points sorted into Wrong, Unverified, Shape and Preference |

## Review code

Code gets the same review whoever wrote it: the plugin's shared review agents. Each is defined by one file in the plugin's `agents/` folder, beside this skill's folder (`../agents/<name>.md`). Where the harness loads named agents, launch each by name (Claude Code's SDLC plugin installs them as `SDLC:review` and so on); otherwise launch a general subagent told to follow its file. Give each paths, never file contents, and nothing from this chat.

1. **The ground.** Check a merge request's head out detached in its own worktree (`git worktree add --detach <path> <commit>`, after fetching it) and give the agents that path. Do the same for code committed on a branch `deliver` built, so the review's files never replace the story's own. Remove the worktree after the report. The user's other local code stays where it is, uncommitted changes and all. Delete any old `done-block.md`, `findings.md` and `security.md` from the checkout's git directory (`git rev-parse --git-dir`) first. The **check command** is the one `AGENTS.md` names, else what CI runs.
2. **The intent.** For a merge request, read its description, its linked ticket's acceptance criteria and its commit messages; that stated intent is what the code is checked against. When none of them states a behaviour, ask the user once what the change is for. For the user's code, it is what the user says the code is for; when they have not said, ask once.
3. **The `review` agent,** given the subject (a merge request or the user's local code), its path or branch, the merge target, the stated intent and the check command.
4. **The `security` agent,** after it, when the review's `Security:` line says `needed`, or when the user asked for a security review. Give it the same inputs as `review` and the categories the `Security:` line names (or "user asked").
5. **The `refute` agent,** on a model other than the reviewers', given the path of `findings.md`, `security.md` when it exists, and `done-block.md`, the worktree and the merge target. It judges every candidate row and fills `done-block.md`. When no file holds a candidate row, skip it and replace the three `pending refute` lines with `none`.
6. **Report** only what survives, in the subject's output. When the review returns without writing `done-block.md`, report its command, exit status and output, and stop. Otherwise read `done-block.md`, the file the review writes in the git directory, and place each row:

| Output | `Findings:` row | `Questions:` row | `Teach:` row | `Refuted:` row |
|---|---|---|---|---|
| Pull request | `issue` comment, at the row's severity | `question` comment with the settling test | none | `Refuted:` line, then `Refuted by:` |
| The user's code | `Wrong` point | `Unverified` point with the settling test | the point its tier names (`wrong`, `unverified` or `shape`) | dropped |

For a design, a plan, an ADR or a fix idea, the `refute` agent returns each row with its verdict: `confirmed` or `lowered` becomes its tier's point, `unsettled` becomes an `Unverified` point with the settling test, and `refuted` is dropped.

Also read `Gate:`: a failing gate is a blocking `issue`. Read `Design:`: each departure the branch does not record is a non-blocking `issue`, or a `Shape` point on the user's code. Read the `Judgment:` lines of `done-block.md` and `security.md`: each is a `question` comment, or an `Unverified` point.

Never rewrite the code under review: never run the `refactor` agent on it, and write code only when the user asks. After the report, offer the `guardrails` skill once for the surviving findings whose `findings.md` row ends with `rule`.
