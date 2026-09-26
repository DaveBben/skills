# Pick the next story

A subagent loads this at every story pick inside the loop, and when the user asks what to pick up next, what is ready, or what is blocked. It returns the report below.

A spike is done when its resolution comment, the findings, is written. Every other rule about a finished spike uses this one.

The next story is chosen when the last one finishes, from what is true now. Never follow a list written at the start of the feature.

Inputs: the stories and spikes of one feature: the epic's child issues on the tracker the `Backlog:` line of `AGENTS.md` names, with their rank and blocking links, read with the access method it lists. Read their comments only by searching for `Parked:` comments, unpinned `Learned` lines, `Observed` lines and `Proposed refactor` lines marked "open". A `Learned` line can change what a story needs. An `Observed` line shows what people did with a shipped story, and can make a later story unneeded or more urgent. Report either beside the pick.

## 1. Find the ready ones

A story or spike is ready when all of these hold:

* **Every blocker is done.** A story it builds on has merged, and a spike it needs is done.
* **No decision is open.** No comment on the story holds a question its owner has not answered, its `Open` line, when criteria exist, says "none", and no `Deferred:` line the story needs waits on a spike that is not done.
* **Every written criterion has its number.** Criteria are usually written after the pick. When they already exist, a criterion the card marks not testable makes the story not ready.
* **Its comments hold no answer the description has not taken in.** Read them before calling it ready.
* **Nobody has started it.** No `story/{slug}/{n}-*` branch exists, and its status is To Do.

Re-read each blocker from the tracker now. A closed decision ticket may have dropped a chain of blockers.

## 2. Rank the ready ones

Take the customer's order first: the tracker rank, or, where the tracker has none, the story the user says matters most when asked. Move a story ahead of that order only for one of these reasons, and say which.

* **No story has reached a real deploy yet.** The story marked `[walking skeleton]` goes first. When none is marked, the thinnest story touching every layer.
* **A spike's answer changes what other stories build.** It goes before the stories that depend on it.
* **It unblocks more.** Count the stories each candidate unblocks, directly and through the stories they unblock. A candidate that unblocks several goes ahead of one that unblocks none.

## 3. Report

```text
Next:     <story or spike> -> <why it beats the rest: customer order, or the reason from "Rank the ready ones">
Ready:    <the other ready stories, in rank order>
Blocked:  <story> -> <what blocks it>
Refactors: <each `Proposed refactor` line in a log comment still marked "open", and the ready story whose code it touches; omit when none>
```

The user can fold a listed refactor into the picked story as its first commit, or run it on its own as a change without new behaviour.

When the user asks what can run at the same time, group the ready and blocked stories into tracks instead. A track is a chain of stories where each one blocks the next. Tracks with no link between them run in parallel. Order stories only inside a track. List the tracks by how many stories each unblocks.

When the user asked what to pick up next, the calling session prints the report, offers to start the pick, and waits for the user to choose. Inside the loop, it takes every ready story in order. The loop starts as many as it may run at once, and lists each departure from rank in its next message to the user, who can reorder.

When nothing is ready, say which blocker frees the most stories and who can clear it.
