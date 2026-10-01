---
name: review-code
description: "Use this skill when code must be reviewed or critiqued, whoever wrote it: a pull request or merge request, a diff, or code the user wrote, committed or not; or a design, a plan, an ADR or a fix idea the user made. Use it on: 'review PR 412', 'review this merge request', 'is this PR ready to merge', 'review my code', 'review what you built', 'security review', 'give me feedback', 'poke holes in this', 'what do you think of this approach'. Reviews it with attack tests written before reading the code and a second pass that keeps only findings a test or a cited line shows, and never rewrites the user's work."
license: MIT
metadata:
  version: "5.0.0"
---
# Review code

## Pick the review

The subject is the thing under review. When it is ambiguous, ask once.

| Subject | Output |
|---|---|
| A pull request, a merge request or a diff someone opened | Conventional Comments, blocking first, then Merge or Changes requested, by [references/pull-request.md](references/pull-request.md); printed, and posted only when the user says to |
| Code the user wrote, committed or not | Points sorted into Wrong, Unverified, Shape and Preference, by [references/feedback.md](references/feedback.md) |
| A design, a plan, an ADR or a fix idea the user made | Points sorted into Wrong, Unverified, Shape and Preference, by [references/feedback.md](references/feedback.md) |

## Review it

Every subject gets the same review whoever wrote it: the plugin's shared `review` agent, and the `security` agent when it is needed. Each is defined by one file in the plugin's `agents/` folder, beside this skill's folder (`../agents/<name>.md`). Where the harness loads named agents, launch each by name (Claude Code's SDLC plugin installs them as `SDLC:review` and `SDLC:security`); otherwise launch a general subagent told to follow its file. Give each paths, never file contents, and nothing from this chat.

1. **The ground.** Check a merge request's head out detached in its own worktree (`git worktree add --detach <path> <commit>`, after fetching it) and give the agents that path; remove the worktree after the report. The user's local code stays where it is, uncommitted changes and all. The **check command** is the one `AGENTS.md` names, else what CI runs.
2. **The intent.** For a merge request, its description, its linked ticket's acceptance criteria and its commit messages. For the user's code or document, what the user says it is for; when they have not said, ask once.
3. **The `review` agent,** given the subject, its path or branch, the merge target, the stated intent and the check command. It checks each of its own findings in a second pass and returns only those a test or a cited line shows.
4. **The `security` agent,** after it, when the review's `Security:` line says `needed` or the user asked for a security review, given the same inputs and what made it needed.
5. **Report** what the agents kept, in the subject's output: a finding is an `issue` comment or a `Wrong` point; a question is a `question` comment or an `Unverified` point with the test that would settle it; a weak test is an `issue` comment or a `Wrong` point naming what it would miss. A failing check command is a blocking `issue`.

Never rewrite the work under review, and write code only when the user asks. After the report, offer the `guardrails` skill once for a finding a checker could catch next time.
