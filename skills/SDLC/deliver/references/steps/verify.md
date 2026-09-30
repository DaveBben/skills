# Step: verify

The `worker` agent runs `story.sh verify '<check command>'` in the worktree, the check command `AGENTS.md` names as one quoted string, and returns the last lines of each failure. A red result is a red story: the failing lines go to the `build` agent.

Run the feature acceptance test last, the one test the user wrote for the feature's outcome, and report its failure message when it changed. When it passes, park the story: the user removes its expected-to-fail marker.

When the check command is green, run `story.sh next confirm`.
