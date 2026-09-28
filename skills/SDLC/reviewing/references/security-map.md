# Map the attack surface

The first of the security review's two subagents. You get the worktree path, the merge target and the branch.

The attack surface is every place data from outside the code's control enters, crosses a boundary, is interpreted, or is stored where it is sensitive.

Read the diff's file list against the merge target, the Critical Constraints of `AGENTS.md`, and the latest architecture snapshot its `Architecture:` line points at. The snapshot's "Who else can reach each crossing" table and the sensitive-data constraints are the starting points; confirm each in the code.

Write `attack-surface.md` in the repository's shared git directory (`git rev-parse --git-common-dir`). That directory is never committed and every worktree sees it. The first line is `Built from <commit>`.

* **A map already exists** and its commit is an ancestor of the merge target: update only the rows for files changed since that commit, and restamp the first line.
* **No map, or its commit is not an ancestor:** traverse the whole repository.

One row per item, each with `<file>:<line>`, at most 150 rows. Where a section would pass the cap, keep the rows the diff touches and those reachable from outside, and say how many were dropped.

```text
Built from <commit>

Entry points: where outside data arrives, who can send it, and the check at the entry
  <file>:<line>  <HTTP route, CLI argument, uploaded or read file, environment variable, queue message, webhook, third-party response, device API, rows another system writes>  from: <who>  check: <file>:<line> or "none found"
Crossings: calls out to another process, machine or service
  <file>:<line>  to: <what>  protocol: <...>  credential: <which, loaded where>  encrypted in transit: <yes | no | unknown>
Sinks: where data is interpreted as instructions
  <file>:<line>  <SQL, shell, HTML or template, deserializer, eval, file path, redirect URL, regular expression, log line>
Sensitive data: what, where stored, where read, how protected
  <what>  stored: <file>:<line> (<table, file, cache, log>)  read: <file>:<line>  at rest: <encrypted | plain | unknown>  who may read: <...>
Secrets: where each is loaded and where it could leak
  <file>:<line>  <secret>  leaks via: <log, error message, client response, or "none found">
Assumptions: trust the code takes for granted
  <file>:<line>  <e.g. "only the home network reaches this port">  stated in: <ADR path, comment, or "implied">
Paths: each entry point to the sink or sensitive store its data reaches
  <entry file:line> -> <file:line> -> <sink or store file:line>
```

The map is never committed and never pasted into a pull request. Return the map's path, a count per section, and how many rows changed since the previous map.
