# Record a decision

Read this for every decision the `architecture` skill records: an answer from the Decide step, an expensive or irreversible choice, an accepted hazard, a rejected alternative, a choice a spike made alone that the user marked `record`, knowledge that cost time to acquire, or a test that a story's test plan listed and then dropped as "no test required" whose absence a later reader would question. Record it when the decision is made, not at the end of the feature.

## Ask before writing

The reasons in the ADR are the user's. Never record one the user has not given or confirmed. When the user deferred to the agent's recommendation, the ADR records the agent's reason, marked as the agent's.

* **From the Decide step, the answer is the reasons.** When the decision came from putting alternatives and a tradeoff to the user, their answer to that message is the reasons. Ask nothing more unless it gives no reason at all.
* **Otherwise draft the three answers** from the conversation, the code and any spike findings, and put them to the user in one message to correct, then wait. Name the obvious route in the third question. Record the answers as the user leaves or rewrites them, and write "unknown" for any the agent could not draft:

```text
Before recording <decision>, correct anything wrong:
1. Why this? <draft>
2. What are the tradeoffs? <draft>
3. Why not <the obvious route>? <draft>
```

* **When the decision was the agent's own choice,** state the agent's reason, the obvious alternative and the tradeoff in the same message, and ask the user to confirm, change or replace the reason.
* **Outside the Decide step, give feedback on the answer before writing, only when there is something to give.** One message: a tradeoff the answer did not name, an alternative nobody considered, a hazard the answer accepts without a test, or a reason that does not hold against the code, each with its mechanism. When the answer holds up, write the file without a feedback message. The user amends the decision or the reason, or says write it.

## Write it

* **The change's own PRD already records the decision** with its rejected alternative: write no ADR, and put the PRD path on the feature header's `Decided:` line.
* **The user gives no reasons:** write no ADR. With a feature open, put the item on the feature header's `Deferred:` line as "no reasons given"; with none, say in chat that the decision is unrecorded. Carry on with the work.
* **Otherwise hand the writing to a fresh subagent that changes no code** (in Claude Code, the `SDLC:worker` agent). Give it the full path of this skill's `references/adr.md`; the decision; the user's reasons quoted word for word, or that the user deferred to the agent and the agent's reason; the agent's feedback, marked as the agent's; the alternatives and why each lost; any hazard it accepts or incident it follows; the path of any ADR it supersedes; the feature slug or "none"; and the checkout and branch to commit in. That is the story's worktree and branch when a story forced the decision, else the repository on the plan branch `story/{slug}/0-plan` before the first story (main in a repository with no remote), or on main when no feature is open.
* **When the decision contradicts a line of `docs/architecture/summary.md`,** quote that line to the user; only the user edits the summary.
* **When it returns the ADR's path,** put that path on the feature header's `Decided:` line when a feature is open.
