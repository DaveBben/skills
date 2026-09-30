# Step: show the criteria

Run this step when the `setup` agent returns a new story's card, not when it only added a red row for a finding or a corrected row.

* **`Not ready:`** run `story.sh close <branch>` from the main checkout and park the story on that line.
* **`Split:`** run `story.sh close <branch>` and split the story as proposed, closing the original as `cut: split into <keys>`; list the split among the choices decided alone.
* **Otherwise show the criteria** in one message: the setup's `Stale:` line when it has one, each criterion that records a product choice, in the user's terms, then the number of other criteria, which stay on the card, accepted unless the user cuts them. Have a `worker` write them on the issue under "PROPOSED, NOT AGREED" and add `Parked: criteria`. When the feature header names an `Owner:` and a criterion records a product choice, the worker also adds `Parked: ask <owner>: agree criteria <letters>`, and the message tells the user once to take those criteria to that person, in refinement or on the issue. The owner's agreement is their comment on the issue, or the user's report that they agreed, which a `worker` records as `Agreed: <owner>, <date>, <where>` before deleting the parked line. A criterion the owner changes is a wrong row: run `story.sh next wrong-row`.

After `Not ready:` or `Split:`, set up the next ready story. Otherwise do not wait for an answer: run `story.sh next` in the worktree.
