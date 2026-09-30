# Step: refactor and review

When `story.sh next` printed `refactored and not reviewed`, the refactor ran: keep `refactor.md` and start at the review. Otherwise start a new round: in each repository's worktree, read the `Reviewed:` hash of any old `done-block.md` in its git directory (`git rev-parse --git-dir`), the **last reviewed commit**, then delete the old `done-block.md`, `refactor.md`, `findings.md` and `security.md`. No agent below gets anything from this chat.

* **Refactor:** the `refactor` agent, given the card, the branch, the merge target, the red commit, the check command, the story's permitted paths and the setup's `Yours:` line, removes what no criterion asked for and improves readability with the suite green, and writes `refactor.md`.
* **Review:** then the `review` agent, given the card, the interfaces its criteria name, the branch, the merge target, the red commit, the check command, the story's permitted paths, the header's `Decided:` line and `refactor.md`'s path when the refactor ran.
* **Short:** after a rebase, or for a change that adds no criterion, skip the refactor agent; the review runs short, given the last reviewed commit, and its file says what.

Then run `story.sh next`: it prints the security review when the setup's or the review's `Security:` line says `needed`, else the refute.
