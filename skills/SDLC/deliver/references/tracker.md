# Where the stories live

Load this before reading or writing any story. It decides where this feature's stories live, how each operation reaches them, and what happens when the tracker cannot be reached. The tracker's own words are used throughout: epic, story, bug, spike, rank, status.

## 1. Decide where the stories live

Take the first case that holds.

1. **`AGENTS.md` has a `Backlog:` line.** Use the tracker and the methods it lists. `Backlog: none` means `docs/delivery/{slug}.md`. Ask nothing.
2. **The request names an issue key, an epic URL or a tracker.** Use that tracker.
3. **The session can reach a tracker:** an MCP server whose tools read issues, or a tracker CLI that reports a logged-in user (`gh auth status` and `glab auth status` are examples). A reachable tracker does not prove it holds this backlog. Name what was found and ask the user once which project holds this work.
4. **Nothing is reachable.** Ask the user once where the backlog lives. "Nowhere" is an answer, and means `docs/delivery/{slug}.md`.

After cases 2 to 4, write the `Backlog:` block into `AGENTS.md` after the Boundaries line, committed with the plan or in the first story's log commit. Record the methods in order of preference, never which one worked in one session, since each teammate's session has different tools connected.

```text
Backlog:   Jira project PAY at https://acme.atlassian.net; Atlassian MCP server, else `acli jira`, else REST
  Criteria: field "Acceptance criteria", else the top of the description
  Blocks:   link type "Blocks"; read back <date>: `--out PAY-1 --in PAY-2` makes PAY-1 block PAY-2
  Status:   To Do, In Progress, In Review, Done

Backlog:   none; stories live in docs/delivery/
```

A tracker with no column in section 3, such as an in-house system, gets one line per operation under `Backlog:`: the command or endpoint, with `{epic}`, `{key}` and `{file}` placeholders. Ask the user for them once. An operation with no line is done by hand and listed at story end.

Before the first write, read the epic with the chosen method. That one read proves the method, the credentials and the project key together.

## 2. Reach the tracker

Use, in order, an MCP server the session already has, the tracker's own CLI, then its HTTP API with a token the user has already put in the environment. Never ask for a token in chat, and never write one to a file. Choose per operation: when a method lacks one, use the next method for that operation only. Read each tool's schema or `--help` before its first call, since names and flags change between versions.

## 3. The operations

| Operation | Jira | GitHub Issues | Linear | Log file |
|---|---|---|---|---|
| List the epic's children with status, rank, blockers | JQL `parent = {epic} ORDER BY Rank ASC`; blockers are `Blocks` links | the parent's sub-issues in listed order; `blocked_by` dependencies | the parent's children in manual order; `blocks` relations | `Stories:` lines with `Blocked by`; done when its pull requests have merged |
| Read one story with its comments | issue and comments | issue and comments | issue and comments | its `Stories:` line and entries |
| Create a story, bug or spike | create with `parent` = epic | create, then add as sub-issue | create with the parent | append a numbered `Stories:` line |
| Write description or criteria | edit; criteria in the site's criteria field | edit the body | edit the description | none: criteria live in the red commit and the pull request |
| Record a blocker | `Blocks` link | `blocked_by` dependency | `blocks` relation | `Blocked by` numbers |
| Comment | comment | comment | comment | a dated entry |
| Set status | a transition, after listing the available ones | open or closed; In Progress and In Review need a project status field or a label | workflow state | the story's log entry marks it done |
| Rank | agile rank API, before or after another issue | reorder the sub-issue in its parent | manual sort order | the order the user gives when asked |
| Link the pull request | key in branch and title where a code-host integration is installed, else a remote link | `Closes #{n}` in the body | key in branch or title, or `Fixes {key}` | the entry's `Done` line |

* **Jira:** the Atlassian MCP server has no rank tool. Use `PUT /rest/agile/1.0/issue/rank`, which takes at most 50 issues per call. `/rest/api/3/search` is gone; use `/rest/api/3/search/jql`, paged by `nextPageToken`. Jira has no standard criteria field; find the site's in the create metadata.
* **GitHub:** the dependency API takes the blocking issue's numeric `id`, not its `#number`. The GitHub MCP server has no dependency tool; `gh` 2.94 and later has `--add-blocked-by`.
* **Linear:** closing words in a pull request move the issue when it opens and when it merges. Do not also move it by hand.
* **Every tracker:** read one blocking link back after creating it, and write the direction on the `Blocks:` line.

## Where each artifact lives

| In the loop | On the board |
|---|---|
| Status | To Do until the branch is cut, In Progress from branch cut, In Review from pull request, Done at merge; a cut story is closed with the reason as its resolution comment. Use the board's own column names. |
| The log entry for a story | A comment on the story, written when its pull request opens, in the form `log.md` gives: Done, Learned, Not caught by, Proposed refactor, Feature test, Observed. At merge it becomes the resolution, with the Done status. Observed is a second comment when it arrives later. |
| A finding about the system, not one story | A comment on the epic, so close-out finds every one in one place. |
| A bug in shipped work | A bug issue linked to the epic, ranked by the user. `Not caught by` is its resolution comment. |

The feature is the epic and its key is the slug; the feature header is its description; each story is a child issue whose criteria go in the criteria field.

## When the board is already filled

* **The children are the proposed stories.** Read them in rank order and show them as the story list, each with an outcome line the agent writes from the story's text. The user confirms, rewords, cuts or re-ranks in one turn. Criteria are written with the `story` skill when each story starts. Write each story's confirmed criteria back to its issue before its red commit.
* **Run the `reviewing` skill's epic review on the children** in a subagent before the first story, and take back only its report. Apply what the user accepts on the board.
* **An epic with no description** gets the header written into it after `deliver` sections 0 through 2 run, the same as a new epic.
* **Sprints are not pauses.** The loop runs the epic's children as `references/next.md` picks them and crosses a sprint boundary without stopping. A team that wants the loop to stop at the sprint edge adds that rule to `AGENTS.md`.
* **Several epics are several features.** One slug, one log, one loop each, never interleaved in one session.

## When the tracker cannot be reached

An auth error, a 401 or 403, or a tool that is not connected.

* Say once which method failed and its error text, and name the login step (`gh auth login`, `acli jira auth login`, reconnecting the MCP server are examples). Try the next method in section 2 before asking. Then ask whether to wait or go on.
* **Going on:** for reads, ask the user to paste the epic and its children with keys, rank and blockers. For writes, keep `docs/delivery/{slug}.md` as the log, with the issue key on every story line and entry heading, and append each owed write to an `## Outbox` section at its end, one line each. A line points at the entry above it and never copies it: `- comment PAY-12: entry "2026-09-24 — Refund shows on statement"`, `- status PAY-12: Done`, `- create story under PAY-1: "<title>", ranked after PAY-9`.
* Show the outbox at every story end. When a method works again, ask once, then replay it top down and delete each line as it lands. Delete the file once the board holds everything the file held.

## Moving from the log file to a tracker

When a project with `docs/delivery/{slug}.md` gains a `Backlog:` line, propose the import in one message and wait. It creates the epic from the feature header, one child per `Stories:` line in listed order (that order becomes the rank), a blocking link per `Blocked by` number, and each dated entry as a comment on the story it names, or on the epic when that story has merged. Write each new key beside its number in the log. The tracker is the log from then on, and the file stays as history.
