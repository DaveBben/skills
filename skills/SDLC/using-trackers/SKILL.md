---
name: using-trackers
description: "Use this skill for every read or write of an issue tracker (Gitea, GitHub, GitLab, Jira or another): when the story or spike skill files, reads, resumes or updates an issue, or when the user asks to put work on a tracker or a board. Use it on: 'create the issues', 'file these stories', 'put this on the board', 'add it to the project', 'open an issue for this', 'read issue 12', 'update the issue', 'link these issues', 'what is blocking this', 'which issue is next'. Load it before calling a tracker's API or CLI. Finds the tracker and its credentials from the repository, files each story or spike as one labelled issue whose body is its content alone, orders issues by the tracker's own blocking relation with no epic, and reads every write back. Not for what a story or spike says; that is `story` or `spike`."
license: MIT
metadata:
  version: "1.0.0"
---
# Using trackers

The `story` and `spike` skills decide what an issue says. This skill puts it on the tracker, and reads and edits it later.

## Words used here

* **Tracker:** the issue tracker the repository uses, such as Gitea, GitHub, GitLab or Jira.
* **Story, spike:** the text the `story` or `spike` skill wrote; one issue each.
* **Feature:** several stories that share one outcome. On a tracker it is only its issues and their blocking relations.
* **Board:** a tracker's project or board view, showing issues in columns.

## Find the tracker

* **From the repository:** the git remote, a tracker URL in AGENTS.md or the README, and any link the user gave. Ask only when these are empty or disagree.
* **What the API can do:** read its version and API description (swagger, OpenAPI) before promising an operation. Tell the user what it lacks before starting.
* **Reads and writes differ:** reads may work without auth when writes do not. A successful read proves nothing about write access.

## Credentials

* **Never ask the user to paste a token into chat,** and never print one in a command, an output or a reply.
* **Stored auth first:** the CLI's login (`gh auth status`, `glab auth status`, `tea login list`), or an environment variable the CLI or the repository names.
* **macOS Keychain:** read an item only when the user names it or approves it. Load it into a variable the command reads, never into the command text.
* **None found:** say which scope the operation needs (Gitea `write:issue`, GitHub `repo` plus `project` for boards, GitLab `api`) and how the user can store it: the CLI's login command or a Keychain item. Then stop.

## File an issue

* **No epics:** create no epic, parent or tracking issue, on Jira too. A feature is its issues.
* **Title field:** the story's `Title:` text, or the spike's question.
* **Body:** the text as its skill wrote it, minus the `Title:` line. Leave out:
  * `Part of #N` or `Blocked by #N` lines, since relations show them;
  * process notes, such as which skill runs it or where findings go;
  * anything another field shows: labels, assignee, milestone.
* **Feature-level data:** the outcome, the measure and the feature's out-of-scope lines sit on the one story that owns the outcome, as the `story` skill writes it. Add nothing at feature level.
* **Kind label:** `story` or `spike` on each issue. Create the label when the repository lacks it.
* **Order and blocking:** the tracker's own relation, never prose. Each story is blocked by the one before it in the build order, and by any other story it waits on.

Blocking relations, one per tracker:

* **Gitea:** issue dependencies, `POST /repos/{o}/{r}/issues/{n}/dependencies`; issue `n` is blocked by the issue in the body.
* **GitHub:** "blocked by" relationships. Sub-issues need a parent issue, so they never carry order.
* **GitLab:** `blocks` issue links, on Premium and above. Free has only `relates to`: tell the user and ask.
* **Jira:** issue links of type Blocks.

## Boards

A board is not an issue: a new issue is not on a board until something places it there.

* **Gitea:** a separate container. Before v28.0.0 (released 2026-09-29, go-gitea/gitea#38691) it has no project API: tell the user to tick the issues in the Issues tab, then Project, then the board's name.
* **Gitea v28 and later:** `POST /repos/{o}/{r}/projects/{id}/columns/{col}/issues/{issue_id}`, where `issue_id` is the issue's global `id`, not its `#` index.
* **GitHub:** a separate container; `gh project item-add`, or the project's auto-add workflow.
* **GitLab:** a view over labels; the label places the issue.
* **Jira:** the board's filter places the issue.
* **No workaround:** never call a web UI route with session cookies.

## Read and edit later

* **Find a story's issue:** the link or key the user gave, the key in the `story/` branch name, else a search by title among issues labelled `story`.
* **Read it whole:** the body, then every comment, since a comment can change what was agreed. Then its state, labels and relations.
* **A feature's issues:** follow the blocking relations from any one of them, or list the board or milestone the user names.
* **Next story:** the first open issue of the feature with no open blocker and no open pull request.
* **Edit the body** in place with the whole new text. Put findings, a pull request's link or a spike's results in a comment.

## Verify every write

* **Read the issue back** after each write: title, body, labels, relations, and board placement where one was made. Fix a difference before the next write.
* **Report** each issue's URL, and each step left for the user to do by hand.

## Destructive operations

* **Only on the user's explicit request:** deleting an issue, or deleting or renaming a label other issues use.
* **Before deleting an issue,** move any content no other issue holds onto the issue that should hold it.

## Without a tracker

The `story` skill's fallback holds: one story in the red commit's message and the pull request's description, a feature in `docs/stories/<slug>.md` with its stories in build order. No header or container.
