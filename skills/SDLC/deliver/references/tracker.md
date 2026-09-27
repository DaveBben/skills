# Where the stories live

Load this before reading or writing any story. The SDLC skills need a project tracker: an epic per feature whose description holds the feature header, its stories and spikes as child issues linked by blocking links, and each issue's comments as its log. The tracker's own words are used throughout: epic, story, bug, spike, rank, status.

## 1. Find the tracker, or set one up

Take the first case that holds.

1. **`AGENTS.md` has a `Backlog:` line.** Use the tracker and the methods it lists. Ask nothing.
2. **The request names an issue key, an epic URL or a tracker.** Use that tracker.
3. **The session can reach a tracker:** an MCP server whose tools read issues, or a tracker CLI that reports a logged-in user (`gh auth status`, `tea login list`). A reachable tracker does not prove it holds this backlog. Name what was found and ask the user once which project holds this work.
4. **Nothing is reachable.** Halt. Help the user pick and connect one: GitHub Issues (sub-issues and dependencies, optionally a Project), Gitea, Jira, Linear, or any tracker that can create epics and stories, link them, and hold a description and comments. Name the connection step for the choice (an MCP server, `gh auth login`, `tea login add`, `acli jira auth login`, or a token the user puts in the environment). Start no work until one read of the project succeeds.

After cases 2 to 4, write the `Backlog:` block into `AGENTS.md` after the Boundaries line, in the next commit the work makes. Record the methods in order of preference, never which one worked in one session, since each teammate's session has different tools connected.

```text
Backlog:   Jira project PAY at https://acme.atlassian.net; Atlassian MCP server, else `acli jira`, else REST
  Types:    Epic, Story, Bug, Spike (issue types; else a `spike` label on a Story)
  Criteria: field "Acceptance criteria", else the top of the description
  Blocks:   link type "Blocks"; read back <date>: `--out PAY-1 --in PAY-2` makes PAY-1 block PAY-2
  Status:   To Do, In Progress, In Review, Done
```

A tracker with no column in section 3, such as an in-house system, gets one line per operation under `Backlog:`: the command or endpoint, with `{epic}`, `{key}` and `{file}` placeholders. Ask the user for them once. An operation with no line is done by hand and listed at story end.

Before the first write, read the epic with the chosen method. That one read proves the method, the credentials and the project key together.

## 2. Reach the tracker

Use, in order, an MCP server the session already has, the tracker's own CLI, then its HTTP API with a token the user has already put in the environment. Never ask for a token in chat, and never write one to a file. Choose per operation: when a method lacks one, use the next method for that operation only. Read each tool's schema or `--help` before its first call, since names and flags change between versions.

## 3. The operations

| Operation | Jira | GitHub Issues | Gitea | Linear |
|---|---|---|---|---|
| Create an epic | issue type Epic | an issue with the Epic issue type, else an `epic` label | an issue with an `epic` label | a parent issue |
| List the epic's children with status, rank, blockers | JQL `parent = {epic} ORDER BY Rank ASC`; blockers are `Blocks` links | the parent's sub-issues in listed order; `blocked_by` dependencies | the epic's dependencies (`GET .../issues/{epic}/dependencies`), each child's own dependencies are its blockers | the parent's children in manual order; `blocks` relations |
| Create a story, bug or spike | create with `parent` = epic, issue type Story, Bug or Spike (else a `spike` label) | create with the issue type, else a `story`, `bug` or `spike` label, then add as sub-issue | create with a `story`, `bug` or `spike` label, then make it block the epic (`POST .../issues/{epic}/dependencies`) | create with the parent and a `spike` label for a spike |
| Read one issue with its comments | issue and comments | issue and comments | `GET .../issues/{index}` and `.../comments` | issue and comments |
| Write description or criteria | edit; criteria in the site's criteria field | edit the body | `PATCH .../issues/{index}` body | edit the description |
| Record a blocker | `Blocks` link | `blocked_by` dependency | `POST .../issues/{blocked}/dependencies` naming the blocker | `blocks` relation |
| Comment | comment | comment | `POST .../issues/{index}/comments` | comment |
| Edit or delete a comment | edit or delete | `PATCH` or `DELETE .../issues/comments/{id}` | `PATCH` or `DELETE .../issues/comments/{id}` | `commentUpdate` or `commentDelete` |
| Set status | a transition, after listing the available ones | open or closed; In Progress and In Review need a project status field or a label | open or closed; In Progress and In Review as labels or a project board column | workflow state |
| Rank | agile rank API, before or after another issue | reorder the sub-issue in its parent | none: the order the user gives when asked | manual sort order |
| Link the pull request | key in branch and title where a code-host integration is installed, else a remote link | `Closes #{n}` in the body | `Closes #{n}` in the body | key in branch or title, or `Fixes {key}` |

* **Jira:** the Atlassian MCP server has no rank tool. Use `PUT /rest/agile/1.0/issue/rank`, which takes at most 50 issues per call. `/rest/api/3/search` is gone; use `/rest/api/3/search/jql`, paged by `nextPageToken`. Jira has no standard criteria field; find the site's in the create metadata.
* **GitHub:** the dependency API takes the blocking issue's numeric `id`, not its `#number`. The GitHub MCP server has no dependency tool; `gh` 2.94 and later has `--add-blocked-by`.
* **Gitea:** the paths are under `/api/v1/repos/{owner}/{repo}`. The dependency endpoints (`.../issues/{index}/dependencies` and `.../blocks`) arrived in Gitea 1.20 (go-gitea/gitea pull request 17935). Gitea has no sub-issues or issue types (go-gitea/gitea issue 36696 is an open proposal), so an epic is an issue labelled `epic` that depends on each of its children. A repository can turn dependencies off, and whether closing keywords close an issue at merge depends on the instance's settings: confirm both on the instance with the first read.
* **Linear:** closing words in a pull request move the issue when it opens and when it merges. Do not also move it by hand.
* **Every tracker:** read one blocking link back after creating it, and write the direction on the `Blocks:` line.

## Where each artifact lives

| In the loop | On the tracker |
|---|---|
| The feature header | The epic's description, in its named lines, `Holdout:` and the feature acceptance test's path included |
| A story, bug or spike | A child issue of the epic. A spike has the spike type or label, and blocks each story that waits on its answer. A story's criteria go in the criteria field, else the top of its description |
| Status | To Do until the branch is cut, In Progress from branch cut, In Review from pull request, Done at merge; a cut story is closed with the reason as its resolution comment. Use the board's own column names |
| A story's log entry | A comment written when its pull request opens, in the form `log.md` gives; at merge it becomes the resolution, with the Done status. `Observed` is a second comment when it arrives later |
| A parked question | A comment on the story starting `Parked:`, edited or deleted once answered where the tracker allows |
| A spike's findings | The spike issue's resolution comment, every line a `Learned` line |
| Architecture tables before `AGENTS.md` exists | A comment on the epic, which the `orient` skill moves into `AGENTS.md` |
| A finding about the system, not one story | A comment on the epic, so close-out finds every one in one place |
| A bug in shipped work | A bug issue under the epic, ranked by the user. `Not caught by` is its resolution comment |

A one-story request or a bug is one issue with no epic, and its comments are its log. A trivial change or a change without new behaviour has the pull request as its record, linked to an issue when one exists.

## When the board is already filled

* **The children are the proposed stories.** Read them in rank order and show them as the story list, each with an outcome line the agent writes from the story's text. The user confirms, rewords, cuts or re-ranks in one turn. Criteria are written with the `define` skill when each story starts. Write each story's confirmed criteria back to its issue before its red commit.
* **Run the `reviewing` skill's epic review on the children** in a subagent before the first story, and take back only its report. Apply what the user accepts on the board.
* **An epic with no description** gets the header written into it after `deliver` sections 0 through 2 run, the same as a new epic.
* **Sprints are not pauses.** The loop runs the epic's children as `references/next.md` picks them and crosses a sprint boundary without stopping. A team that wants the loop to stop at the sprint edge adds that rule to `AGENTS.md`.
* **Several epics are several features.** One epic, one loop each, never interleaved in one session.

## When the tracker cannot be reached

An auth error, a 401 or 403, or a tool that is not connected.

* Say once which method failed and its error text, and name the login step. Try the next method in section 2 before asking. Then ask whether to wait or go on.
* **Going on:** for reads, ask the user to paste the epic and its children with keys, rank and blockers. For writes, append each owed write to an outbox, the file `sdlc-outbox.md` in the shared git directory (`git rev-parse --git-common-dir`), which is never committed. One line per write, with the text it will post: `- comment PAY-12: <the log entry>`, `- status PAY-12: Done`, `- create story under PAY-1: "<title>", ranked after PAY-9`.
* Show the outbox at every story end. When a method works again, ask once, then replay it top down, delete each line as it lands, and delete the file once it is empty.
