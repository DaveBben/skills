# Working from a tracker

Load this when `AGENTS.md` Boundaries names a backlog outside the repository ("Backlog: Jira project TAG"). The board is then the backlog, and no `docs/features/{slug}/feature.md` exists.

The tracker's own words are used throughout: epic, story, bug, spike, rank, status. Use whatever tracker tool the session has: an MCP server, a CLI, or an HTTP API with the user's credentials.

## Where each artifact lives

| In the loop | On the board |
|---|---|
| The feature | The epic. Its key is the slug and the branch is `feature/{key}`. |
| The feature header | The epic's description, in the same seven lines: Outcome, Problem, Not doing, Decided (ADR paths), Deferred, feature acceptance test path. `Stories:` is not written; the children are the list. |
| A story and its criterion | A child story. The Given/When/Then goes in its acceptance-criteria field, or at the top of its description when the board has no such field. |
| Story order | Rank. Read at every story start; the first unresolved child by rank is next. |
| A story's branch and pull request | `story/{key}-{short-name}`. The pull request title starts with the key, and the issue carries the pull request link. |
| Status | To Do until the branch is cut, In Progress from branch cut, In Review from pull request, Done at merge. Use the board's own column names. |
| The log entry for a story | The story's resolution comment: Done, Learned, Not caught by, Observed, in that form. Observed is a second comment when it arrives later. |
| A finding about the system, not one story | A comment on the epic, so close-out finds every one in one place. |
| A bug in shipped work | A bug issue linked to the epic, ranked by the user. `Not caught by` is its resolution comment. |
| A spike | A spike issue linked to the epic. The findings log is its resolution comment, every line a `Learned` line. |
| An ADR | Stays in `docs/adr/`. The epic description links it under Decided. |
| The map | Stays in `AGENTS.md`. |
| The feature acceptance test | Stays in the repo. The epic description names its path. |

## When the board is already filled

* **The children are the proposed stories.** Read them in rank order and show them as the story list, each with a Given/When/Then the agent writes from the story's text. The user confirms, rewords, cuts or reorders in one turn, as in section 3. Write each confirmed criterion back to its issue before the first story starts.
* **Flag a story named after a layer or a component.** "Build the endpoint" does not end with something a person can do. Propose the rewording and let the user decide.
* **Split on the board.** A story that crosses more than one seam or workflow step is split into child stories the user confirms, and the original is closed as split or kept as the parent, whichever the board's convention is.
* **An epic with no description** gets the seven-line header written into it after section 0 through 3 run, the same as a new epic.
* **Sprints are not pauses.** The loop runs the epic's children by rank and crosses a sprint boundary without stopping. A team that wants the loop to stop at the sprint edge adds that rule to `AGENTS.md`.
* **Several epics are several features.** One branch, one slug, one loop each, never interleaved in one session.

## Pauses on the board

* A pause that needs a new story or bug proposes it in chat first. The issue is created only after the user confirms, ranked where the user says.
* A forced decision is recorded as an ADR in the repo, and the epic description's Decided line gains the path.
* A story the user cuts during a pause is closed on the board with the reason as its resolution comment.

## Without a tracker tool

When the session has no way to read or write the board, say so once. Ask the user to paste the epic's key, description and child stories with their keys and rank. Keep `docs/features/{slug}/feature.md` as a cache, with the issue key at the start of every story line and every entry heading, and list at the end of every story the comments and status changes the user has to make by hand. Delete the cache when a tool becomes available and the board has been brought up to date.
