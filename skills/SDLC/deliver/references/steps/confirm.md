# Step: confirm and open

The `description` agent, launched in the foreground, given the branch, its target, `done-block.md`, `security.md` when it exists, and the header's `Outcome:` and `Success:` lines, drafts the description, with any installed skill for writing in the user's voice. Then one message: the criteria changes since they were shown and why, the review's result, and the description agent's `Read first:` hunk when it returns one, for the user to read before confirming; nothing else in the diff is asked of them. One question: the user confirms by writing, in one line, what a person can do once this merges. The message shows neither the `Outcome:` line, the story's title nor the description, so the line comes from the user's memory. A bare "confirm" gets the question once more. A line that contradicts the criteria, or an edit to them, is a wrong row: run `story.sh next wrong-row`. Trivial and no-behaviour-change sizes confirm with a plain yes.

On confirmation, put the user's line first in the description's Why section, show the description in the reply that opens the pull request (the user edits it on the host if they want), run `story.sh confirm`, push, and open the pull request with the issue key in the title, e.g. `[PAY-1420]`. The push guard, where `guardrails` installed it, refuses the push until `confirm` has run.

When the change has an issue, hand one `worker` these tracker writes as a numbered list:

1. The confirmed card on the issue in place of the proposed one, and `Parked: criteria` deleted.
2. The issue's status set to In Review.
3. The story's log comment, by the worker's log template, given the issue key, the paths of `card.md` and `done-block.md`, and what only this session holds: the `Learned` mechanism in one sentence and the test, ADR or `AGENTS.md` line that pins it, or "not pinned"; for a bug, the gap that let it through and the rule or row now closing it; and the user's turn (core written, sketch written, skipped or none), whether a `Read first:` hunk was shown, and whether the user confirmed as shown or edited.

A `Learned` fact about the system, not this story, is also a comment on the epic, and one that needs more than a line is an ADR (a decision record under `docs/adr/`). When the tracker outbox `sdlc-outbox.md` exists in the shared git directory, show it. Then run `story.sh next open`, which records the pull request as open, and follow it.
