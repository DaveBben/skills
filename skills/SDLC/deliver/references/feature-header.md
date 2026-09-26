# Feature header and feature acceptance test

Load this for a request sized as several stories, once the `define-work` and `architecture` skills have run, and again at close-out. It holds the rules the record keeps, the feature header's format, the feature acceptance test, the holdout scenarios, and close-out.

## Rules the record keeps

* **Promote into a criterion anything encoding an ADR,** so how a recorded decision was interpreted is never discovered by reading generated code.
* **Defer infrastructure** not required to pass a story's test to a later story. Logging, retries and error handling enter when a story pulls them.

Write the result into the feature header at the top of the log, the `## Feature` block `define-work` wrote, creating the file if absent. Commit it on the plan branch `story/{slug}/0-plan`, the branch the `architecture` skill commits its decisions to, opening it when absent; the first story is set up after its pull request merges. In a repository with no remote, commit on main. Keep the log after the last story ships. The file has at most one `## Feature` heading, above the first dated entry; rewrite it in place and never append a second. Keep it to 40 lines above `Stories:`, with one line per story under 120 characters.

```text
# {slug}

## Feature
Outcome:   <the outcome sentence `define-work` wrote>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <one checkable non-goal per line>
Success:   <the signal that shows the outcome happened; which direction is good; the noise band>
Constraints: <one line per rule every story must keep true>
Context:   <one line per fact every story needs: environment, variables, URLs, test accounts, commands, and where each credential lives, never its value>
Repositories: <one line per repository this feature changes: its name, then its remote URL, its local path when it has no remote, or "new: <name> <directory>" before it exists>
Steps:     <the steps the person takes, in order>
Decided:   <one ADR path per line, or a PRD path and section when the PRD records the decision and its rejected alternative>
Deferred:  <one item per line: the decision, and the number, story or "waits on spike N" that forces it, or "no reasons given"; omit when none>
feature acceptance test: <path, or "after story 1" when the interface the outcome names has no test runner yet>
Holdout:   <the holdout's run command, `~/.holdout/<repository>/<slug>/run`; omit when the user keeps none>
Stories:    <every story and spike, each with its number, title, outcome line, "Blocked by:", and "[walking skeleton]" where marked. A cut story stays as "<n>. cut: <reason>". Numbers never change. This line is written once and edited only to add or cut a story: a story is done when all of its pull requests have merged, and a spike when its findings have merged>
```

Nothing else goes in the feature header. On a tracker it is the epic's description, and stories already on the board are read as the proposed stories.

### The feature acceptance test

The outcome sentence gets one acceptance test of its own, and the user writes it.

* **The agent names, the user writes.** State the file, the runner, and the Given/When/Then the test must assert: the outcome sentence in concrete values, through the interface the user actually uses. The user writes the body. When the user asks the agent to write it, write it; the lock below still applies once it is committed.
* **It lives in a `feature-acceptance` directory inside the repo's test tree,** the directory the harness denies to the agent. When the harness can deny paths but does not, offer the `guardrails` skill once to add it before the commit. When the user declines, or the harness has no deny list, write under Critical Constraints in `AGENTS.md` that the directory is unguarded.
* **It is marked expected-to-fail, strictly,** in the framework's own way (pytest `xfail(strict=True)`, jest `test.failing`, or the nearest equivalent), so the suite stays green while it fails and goes red the moment it passes. That flip is the close-out signal. The user removes the marker at close-out; the agent never touches the file.
* **Commit it on its own on the first story's branch,** before the red commit. The first story's red commit waits for it. When the interface the outcome names has no test runner yet, the first story adds the runner, and the user writes the feature acceptance test after that story merges; the feature header says "after story 1" until then.
* **Locked from the agent for good,** unlike the red-commit guard, which clears at each merge. No subagent edits, moves, deletes, skips or re-marks it either. A wrong feature acceptance test is the user's to change. Before it is committed, run the `reviewing` skill on it once, as work the user made.

### Holdout scenarios

A holdout scenario is an end-to-end check the user writes in the terms of the system and its data: the rows a store holds, the request sent or the screen used, what comes back, and the rows after. No agent that writes criteria, tests or code ever reads one, so the build cannot be fitted to it. They live outside every repository, in `~/.holdout/<repository>/<slug>/`.

* **Offer one per feature, at Record.** When the user takes it, they write 5 to 15 scenarios in a separate session opened in that directory, running the `story` skill's holdout path by name, which writes the `run` command. Add the `Holdout:` line. A scenario runs once its `Due after:` stories have merged and the user has confirmed its first run.
* **Keep it out of reach.** Give no subagent but verify the `Holdout:` line, and never name the directory in `AGENTS.md`, a commit or a prompt. Where the harness can deny paths, offer `guardrails` once to deny it. Where it cannot, tell the user once that nothing but convention keeps agents out, and that the canary in the scenarios catches only copying.
* **A failure goes to the user, never to a builder.** Feeding a hidden check's failures back to the builder turns it into one more test to fit. The user reads `report.md` in the holdout directory, then hands over a bug report in their own words, which spends that scenario, or changes or cuts the scenario. When fewer than five are unspent, ask the user for more.
* **The private-repository alternative.** Where a hard boundary is needed, the holdout is a private repository whose CI runs the scenarios against the story branch's preview deployment and posts the `run` line as a status on the pull request. The token the agent holds has no access to it.

## Close-out

When every story in `Stories:` is done or cut:

* **The feature acceptance test.** Confirm its marker is gone and the suite is green, and go no further while it is red. When it still fails with every story done, give the user its failure message and propose the story that would make it pass.
* **The holdout.** Every scenario is due now. Go no further until the `run` line says every due scenario passes. The user may move spent scenarios into the `feature-acceptance` directory as regression tests.
* **The log,** on one last branch from main. Promote or drop each unpinned `Learned` line, and each spike's `Outcome`, `Approach used` and `Quirks and surprises` lines: turn it into a test, an ADR or an `AGENTS.md` line and write the pin beside it, or delete it with the user's agreement. None survives the feature. A spike's `Open questions` are closed by a story or by the user's decision; its `Dead ends` and `Decided alone` lines stay as a record. Put each `Proposed refactor` line still marked "open" to the user: do it on this branch, or drop it and delete the line. Delete every `Parked:` line and every `Feature test:` line but the last. Then open the pull request.
* **The outcome.** Ask the user whether the `Success` signal moved, and propose a follow-up story or a cut from the answer. Ask which pause or check in this feature cost time without catching anything, and hand the answer to the `guardrails` skill to loosen or delete it. Prompt the user to observe each signal once deployed. Close the epic and keep the log file.
* **When nothing about the user's day changed,** check whether the scope was chosen or inherited. A spike's boundary may have become the project's boundary, or the work that delivers the outcome may sit behind a repository edge with no story. The sign is a feature header precise about internals and silent about the user's day.
