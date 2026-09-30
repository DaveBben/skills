# Step: resume

`story.sh status` printed a story, or a story carries a `Parked:` comment. Have the `lookup` agent read those comments and the epic's open pull requests, send where things stand, and restart each story at the step its line prints by running `story.sh next` in its worktree. Take the slug from a printed branch name (`story/<slug>/...`); with none, have the `lookup` agent search the tracker for the user's open epics.
