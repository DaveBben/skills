# Review against the attack surface map

The second of the security review's two subagents. You get the worktree path, the merge target and the branch.

Read `attack-surface.md` in the shared git directory (`git rev-parse --git-common-dir`). Read the paths that pass through a changed file first. For a review of the whole repository, read every path.

For each path, check:

* **At the entry:** the data's type, size, range and allowed values are checked before anything uses it. Most validation guards missing and empty and forgets type and size.
* **At the sink:** the standard defence for that sink is in place, such as a parameterized query, argument arrays instead of a shell string, escaping by the template engine, or a deserializer that refuses unknown types.
* **At each entry and crossing:** who the caller is (authentication) and what that caller may do (authorization) are both checked, on the server side.
* **Sensitive data:** it goes only where a constraint in `AGENTS.md` allows it, is encrypted where one requires it, and never reaches a log line, an error message or a client response it should not.
* **Secrets:** none is written into the source, logged, or returned.
* **Exhaustion:** an entry others can reach has a limit on size, rate or time.
* **Failure:** an error on the path does not reveal internals, or leave a half-written record another caller can see.

Read what the tools already reported first, the dependency audit and the secret scan among them, and never redo their work by hand. A finding names the entry, the path, and the input that breaks it. A finding is blocking when data from outside reaches a sink without its defence, reaches a sensitive store it is not allowed in, or passes an entry or crossing with no authentication or authorization check.

Each finding is a candidate. Append each to `findings.md` in the worktree's git directory (`git -C <worktree> rev-parse --git-dir`) with `security` as its source. For a review of the whole repository, replace `findings.md` instead. When `done-block.md` sits beside it, replace its `Security: pending` line with `Security: reviewed, <n> candidates`.

Delete the map afterwards unless the caller says to keep it. Return the number of candidates and how many are blocking.
