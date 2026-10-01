# Where the stories live

Section 1 connects a tracker when `AGENTS.md` has no `Backlog:` line. Sections 2 and 3 are for whoever runs a tracker operation. The tracker's own words are used throughout: epic, story, bug, spike, rank, status.

## 1. Find the tracker, or set one up

Take the first case that holds.

1. **`AGENTS.md` has a `Backlog:` line.** Use the tracker and the methods it lists. Ask nothing.
2. **The request names an issue key, an epic URL or a tracker.** Use that tracker.
3. **Otherwise,** work without a tracker: stories live in the chat and the feature file, as the `story` skill says. When the session can reach one (an MCP server whose tools read issues, or a tracker CLI that reports a logged-in user, such as `gh auth status` or `tea login list`), mention it once and use it only when the user names the project that holds this work.

After case 2, or once the user names a project under case 3, write the `Backlog:` block into the `AGENTS.md` of each repository the work touches, after the Boundaries line, in the next commit the work makes there; where a repository has no `AGENTS.md`, create one holding its name and the block. Record the methods in order of preference, never which one worked in one session, since each teammate's session has different tools connected.

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
* **Every tracker:** read one blocking link back after creating it, and write the direction on the `Blocks:` line. Set a status the task names (To Do, In Progress, In Review, Done) by the board's own column name on the `Status:` line.
