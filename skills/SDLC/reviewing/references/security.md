# Security review

Loaded for every review of code: code an agent built, a pull request, or code the user made. It runs after the review of the code's behaviour, as two subagents in turn. The first maps the attack surface. The second reviews the code against that map. Neither gets this session's chat.

Where the harness lets only the main session start subagents, the session that called `reviewing` starts both. When `reviewing` itself runs in a subagent, it returns `Security: pending`, and its caller runs this file's two phases.

## 1. Map the attack surface

The attack surface is every place data from outside the code's control enters, crosses a boundary, is interpreted, or is stored where it is sensitive.

Give the mapping subagent the repository path, the merge target, the diff's file list, and the `### Architecture` block and Critical Constraints of `AGENTS.md`. The Flows table's "Who else reaches To" column and the sensitive-data constraints are its starting points; it confirms each in the code.

It writes `attack-surface.md` in the repository's shared git directory (`git rev-parse --git-common-dir`). That directory is never committed and every worktree sees it. The first line is `Built from <commit>`.

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

It returns the map's path, a count per section, and how many rows changed since the previous map.

## 2. Review against the map

Give the security subagent the map's path, the merge target and the branch. It reads the paths that pass through a changed file first. For a request to review the whole repository, it reads every path.

For each path, check:

* **At the entry:** the data's type, size, range and allowed values are checked before anything uses it. Most validation guards missing and empty and forgets type and size.
* **At the sink:** the standard defence for that sink is in place, such as a parameterized query, argument arrays instead of a shell string, escaping by the template engine, or a deserializer that refuses unknown types.
* **At each entry and crossing:** who the caller is (authentication) and what that caller may do (authorization) are both checked, on the server side.
* **Sensitive data:** it goes only where a constraint in `AGENTS.md` allows it, is encrypted where one requires it, and never reaches a log line, an error message or a client response it should not.
* **Secrets:** none is written into the source, logged, or returned.
* **Exhaustion:** an entry others can reach has a limit on size, rate or time.
* **Failure:** an error on the path does not reveal internals, or leave a half-written record another caller can see.

Read what the tools already reported first, the dependency audit and the secret scan among them, and never redo their work by hand. Every rule in the `reviewing` skill's section 2 holds here. A finding names the entry, the path, and the input that breaks it. A finding is blocking when data from outside reaches a sink without its defence, reaches a sensitive store it is not allowed in, or passes an entry or crossing with no authentication or authorization check.

Write findings in the calling review's format:

* **Pull request:** Conventional Comments with the decoration `security` added, such as `issue (blocking, security):`, each on its own line of code.
* **Code an agent built:** append a `Security:` line to the Done block file, one finding per line: `<file>:<line>`, the path, the input that breaks it, and blocking or not; or `none`. A finding no reading confirmed or refuted also goes on its `Exceptions:` line.
* **Code the user made:** Wrong points for confirmed findings, Unverified points for the rest.

Return, in at most ten lines: the number of blocking findings, one line for each, the `Rules:` line for findings a pattern could match, and any `Exceptions:` lines.

## 3. The map is temporary

The map is never committed and never pasted into a pull request. Delete it after a standalone review. Inside `deliver`, it lives for the feature and is deleted at close-out.
