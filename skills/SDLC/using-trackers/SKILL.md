---
name: using-trackers
description: "Use this skill for every read or write of an issue tracker (Gitea, GitHub, GitLab, Jira or another): an issue, ticket, project, backlog or board, whether the user asks or the story or spike skill does. Use it on: 'create a story on gitea', 'create a story in the gitea backlog', 'create a story/bug on the board', 'file these stories in jira', 'open an issue for this', 'log this as an issue', 'put this on the board', 'read issue 12', 'update the issue', 'link these issues', 'what is blocking this', 'which issue is next'. Load it before calling a tracker's API or CLI. Files each story or spike as one labelled issue and reads every write back. Not for what a story says; that is `story`. Not for a git commit or push."
license: MIT
metadata:
  version: "1.3.0"
---
# Using trackers

## Words used here

* **Feature:** several stories that share one outcome. On a tracker it is only its issues and their blocking relations.

## Find the tracker

* **From the repository:** find it from the git remote, a tracker URL in AGENTS.md or the README, and any link the user gave; ask when none names one or they disagree.
* **What the API can do:** read its version and API description (swagger, OpenAPI) before promising an operation. Tell the user what it lacks before starting.
* **Reads and writes differ:** a successful read proves nothing about write access.

## Credentials

* **Never ask the user to paste a token into chat,** and never print one in a command, an output or a reply.
* **Stored auth first:** the CLI's login (`gh auth status`, `glab auth status`, `tea login list`), or an environment variable the CLI or the repository names.
* **macOS Keychain:** read an item only when the user names it or approves it. Load it into a variable the command reads, never into the command text.
* **None found:** say which scope the operation needs (Gitea `write:issue`, GitHub `repo` plus `project` for boards, GitLab `api`) and how the user can store it: the CLI's login command or a Keychain item. Then stop.

## File an issue

* **No epics:** create no epic, parent or tracking issue, on Jira too. A feature is its issues.
* **Title field:** the story's `Title:` text, or the spike's question.
* **Body:** the text as its skill wrote it, minus the `Title:` line. Leave out:
  * `Part of #N` or `Blocked by #N` lines;
  * process notes, such as which skill runs it or where findings go;
  * anything another field shows: labels, assignee, milestone.
* **Feature-level data:** the outcome, the measure and the feature's out-of-scope lines sit on the one story that owns the outcome, as the `story` skill writes it. Add nothing at feature level.
* **Kind label:** `story`, `spike` or `refactor` on each issue. Create the label when the repository lacks it.
* **Order and blocking:** the tracker's own relation, never prose. Each issue is blocked by the one before it in the build order, and by any spike or story it waits on.

Each tracker's blocking relation and board placement: [references/gitea.md](references/gitea.md), [references/github.md](references/github.md), [references/gitlab.md](references/gitlab.md), [references/jira.md](references/jira.md). Read only the one in use.

## Boards

A new issue is on no board until something places it there. Never call a web UI route with session cookies to place it.

## Read and edit later

* **Find a story's issue:** the link or key the user gave, the key in the `story/` branch name, else a search by title among issues labelled `story`.
* **Read it whole:** the body, then every comment, since a later comment can change what was agreed, then its state, labels and relations.
* **A feature's issues:** follow blocking relations in both directions from any one issue, or list the board or milestone the user names.
* **Next story:** the first open issue of the feature with no open blocker and no open pull request. When its body has an `Open questions` section, report that it is not ready.
* **Edit the body** in place with the whole new text. Put findings, a pull request's link or a spike's results in a comment.

## Verify every write

* **Read the issue back** after each write: title, body, labels, relations, and board placement where one was made. Fix a difference before the next write.
* **Report** each issue's URL, and each step left for the user to do by hand.

## Destructive operations

* **Only on the user's explicit request:** deleting an issue, or deleting or renaming a label other issues use.
* **Before deleting an issue,** move any content no other issue holds onto the issue that should hold it.

## Without a tracker

Write one story in the red commit's message and the pull request's description, and a feature in `docs/stories/<slug>.md`, committed on its own branch, with its stories in build order. Add no header or container.
