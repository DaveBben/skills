# Step: security review

The `security` agent, given the card, the branch, the merge target, the check command, the header's `Decided:` line and what made it needed (the `Security:` line of the setup or the review), reviews the story and writes `security.md` in the worktree's git directory. When the review ran short, after a rebase or for a change that adds no criterion, it runs short too, given the same last reviewed commit.

Then run `story.sh next`.
