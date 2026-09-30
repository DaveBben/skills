# Step: a wrong row

A **row** is one test in the story's test table in `card.md`. A **wrong row** is one the builder cannot satisfy for a reason that holds against the code, or one the user edits. A **red commit** holds a story's failing tests and stubs only.

Once the user accepts the correction, run `story.sh unred`, have the `setup` agent commit the corrected test as a new red commit, and run `story.sh red <hash>` for it and for every earlier red commit of the story. After the story's pull request opens, a changed or added row is also written into the criteria on its issue, in place; a `Decided:` comment alone leaves the issue stating the old criteria.

Then run `story.sh next`.
