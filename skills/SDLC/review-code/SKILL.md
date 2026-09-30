---
name: review-code
description: "Use this skill when code must be reviewed or critiqued, whoever wrote it: a pull request or merge request, a diff, or code the user wrote, committed or not; or a design, a plan, an ADR or a fix idea the user made. Use it on: 'review PR 412', 'review this merge request', 'is this PR ready to merge', 'review my code', 'review what you built', 'security review', 'give me feedback', 'poke holes in this', 'what do you think of this approach'. Runs the same review agents deliver runs on its stories, has a second agent on another model try to refute each finding before reporting it, and never rewrites the user's work."
license: MIT
compatibility: any-agent
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

Code gets the same review whoever wrote it: the plugin's shared review agents, which `deliver` also runs on the stories it builds. Each is defined by one file in the plugin's `agents/` folder, beside this skill's folder (`../agents/<name>.md`). Where the harness loads named agents, launch each by name (Claude Code's SDLC plugin installs them as `SDLC:review` and so on); otherwise launch a general subagent told to follow its file. Give each paths, never file contents, and nothing from this chat.

1. **The ground.** Check a merge request's branch out in its own worktree (`git worktree add <path> <branch>`) and give the agents that path; the user's local code stays where it is, uncommitted changes and all. Delete any old `done-block.md`, `findings.md` and `security.md` from that checkout's git directory (`git rev-parse --git-dir`) first. The **check command** is the one `AGENTS.md` names, else what CI runs.
2. **The intent.** For a merge request, read its description, its linked ticket's acceptance criteria and its commit messages; that stated intent is what the code is checked against. For the user's code, it is what the user says the code is for; when they have not said, ask once.
3. **The `review` agent,** given the subject (a merge request or the user's local code), its path or branch, the merge target, the stated intent and the check command. It attacks the stated behaviours with its own tests, mutates the changed logic, assumes every new test is weak until shown otherwise, checks the code against the intent with values the tests never use, and says whether security needs its own review. It changes no code.
4. **The `security` agent,** after it, when the review's `Security:` line says `needed`, or when the user asked for a security review.
5. **The `refute` agent,** on a model other than the reviewers', judges every candidate row in `findings.md` and, when it exists, `security.md`, and fills `done-block.md`. Severity is set by rule: a finding blocks only when a caller that exists reaches it under the configuration production runs with.
6. **Report** only what survives, in the subject's output, reading the `Findings:`, `Questions:`, `Teach:`, `Refuted:` and `Refuted by:` lines of `done-block.md`, the file the review writes in the git directory:

| Output | `confirmed` or `lowered` | `unsettled` | `refuted` |
|---|---|---|---|
| Pull request | `issue` comment | `question` comment with the settling test | `Refuted:` line |
| The user's code | its tier: `Wrong:`, `Unverified:` or `Shape:` point | `Unverified:` point with the settling test | dropped |
| A design, a plan, an ADR or a fix idea | its tier's point | `Unverified:` point with the settling test | dropped |

Never rewrite the code under review: never run the `refactor` agent on it, and write code only when the user asks. After the report, offer the `guardrails` skill once for the surviving findings marked `rule`.
