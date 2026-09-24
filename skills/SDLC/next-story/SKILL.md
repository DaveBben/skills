---
name: next-story
description: "Use this skill whenever the next piece of work has to be chosen from an epic, a feature log or a list of stories and spikes. Use it on: 'what should I pick up next', 'what's next', 'which story next', 'what is ready', 'what can run in parallel', 'what is blocked', 'plan the order of this epic', and at every story start inside `execute`. Reads what blocks each story, drops the ones not ready, and picks one ready story or spike, saying why it beats the others and what else was ready. Recommends only. Do not use it to split work into stories (`feature`), to write a story's criteria (`story`), or to build the story (`execute`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Next Story

The next story is chosen when the last one finishes, from what is true now. Never follow a list written at the start of the feature.

Inputs: the stories and spikes of one feature, with their blockers. On a tracker they are the epic's children, their rank and their blocking links. Without a tracker they are the `Stories:` list in the feature header of `docs/features/{slug}/feature.md`. Read the feature log's entries too, since a `Learned` line can change what a story needs.

## 1. Find the ready ones

A story or spike is ready when all of these hold:

* **Every blocker is done.** A story it builds on has merged, and a spike it needs has written its findings.
* **No criterion waits on an open decision.** Its `Open` line says "none", or the story's comments hold the owner's answer.
* **Every criterion has its number.** A criterion the card itself marks not testable is not ready.
* **Its comments hold no answer the description has not taken in.** Read them before calling it ready.

Re-read each blocker from the tracker or the log now. A closed decision ticket may have dropped a chain of blockers. Check that each ready story is ready for the right reason.

## 2. Rank the ready ones

Take the customer's order first: the tracker rank, or the order the user gave. Move a story ahead of that order only for one of these reasons, and say which.

* **No story has reached a real deploy yet.** The thinnest story touching every layer goes first.
* **A spike's answer changes what other stories build.** It goes before the stories that depend on it.
* **It unblocks more.** Count the stories each candidate unblocks, directly and through the stories they unblock. A candidate that unblocks several goes ahead of one that unblocks none.
* **It is much cheaper.** A five-minute fix goes ahead of a story that needs a meeting.

## 3. Report

```text
Next:     <story or spike> -> <why it beats the rest: customer order, or the reason from section 2>
Ready:    <the other ready stories, in rank order>
Blocked:  <story> -> <what blocks it>
```

When the user asks what can run at the same time, group the ready and blocked stories into tracks instead. A track is a chain of stories where each one blocks the next. Tracks with no link between them run in parallel. Order stories only inside a track. List the tracks by how many stories each unblocks.

Run alone, recommend and wait for the user to choose. Called from `execute`, return the pick. The loop starts it, and the user can change it at any pause.

When nothing is ready, say which blocker frees the most stories and who can clear it.
