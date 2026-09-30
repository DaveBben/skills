# Step: show the criteria

Run this step when the `setup` agent returns a new story's card, not when it only added a red row for a finding or a corrected row.

* **`Not ready:`** run `story.sh close <branch>` from the main checkout and park the story on that line.
* **`Split:`** run `story.sh close <branch>` and split the story as proposed, closing the original as `cut: split into <keys>`; list the split among the choices decided alone.
* **Otherwise show the criteria** in one message: the setup's `Stale:` line when it has one, each criterion that records a product choice, in the user's terms, then the number of other criteria, which stay on the card, accepted unless the user cuts them. Have a `worker` write them on the issue under "PROPOSED, NOT AGREED" and add `Parked: criteria`.

After `Not ready:` or `Split:`, set up the next ready story. Otherwise do not wait for an answer: run `story.sh next` in the worktree.
