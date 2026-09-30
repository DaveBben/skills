# Step: adopt a pull request the user authored

Add a worktree for its branch (`git worktree add <path> <branch>`), run `story.sh adopt <key>` there, and skip `story.sh start` for this story. When the branch is checked out in a checkout the agent did not create, park `Parked: switch <checkout> off <branch>` for the user. Never touch uncommitted changes in a checkout the agent did not create.

An adopted story has no red commit: tell the `setup` agent to keep the branch's existing tests as characterization rows, commit the new failing rows, and run `story.sh red` on that commit. Then launch it as the last item of `story.sh next setup` says.
