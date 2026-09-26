# Feature header and feature acceptance test

Load this for a request sized as several stories, once the `define-work` and `architecture` skills have run. It holds the rules the record keeps, the feature header's format, and the feature acceptance test.

## Rules the record keeps

* **Promote into a criterion anything encoding an ADR,** so how a recorded decision was interpreted is never discovered by reading generated code.
* **Defer infrastructure** not required to pass a story's test to a later story. Logging, retries and error handling enter when a story pulls them, after a run showed the need. When the user can name the moment they wanted a thing, it is story-pulled; when they can only say it is good practice, it is speculation.

Write the result into the feature header at the top of the log, the `## Feature` block `define-work` wrote, creating the file if absent. Commit it on the plan branch `story/{slug}/0-plan`, the branch the `architecture` skill commits its decisions to, opening it when absent; the first story is set up after its pull request merges. In a repository with no remote, commit on main. Keep the log after the last story ships. The file has at most one `## Feature` heading, above the first dated entry; rewrite it in place and never append a second. Keep it to one screen.

```text
# {slug}

## Feature
Outcome:   <the outcome sentence `define-work` wrote>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <one checkable non-goal per line>
Success:   <the signal that shows the outcome happened>
Constraints: <one line per rule every story must keep true>
Context:   <one line per fact every story needs: environment, variables, URLs, test accounts, commands, and where each credential lives, never its value>
Repositories: <one line per repository this feature changes: its name, then its remote URL, its local path when it has no remote, or "new: <name> <directory>" before it exists>
Steps:     <the steps the person takes, in order>
Decided:   <one ADR path per line, or a PRD path and section when the PRD records the decision and its rejected alternative>
Deferred:  <one item per line: the decision, and the number, story or "waits on spike N" that forces it, or "no reasons given"; omit when none>
feature acceptance test: <path, or "after story 1" when the interface the outcome names has no test runner yet>
Stories:    <every story and spike, each with its number, title, outcome line, "Blocked by:", and "[walking skeleton]" where marked. A cut story stays as "<n>. cut: <reason>". Numbers never change. This line is written once and edited only to add or cut a story: a story is done when all of its pull requests have merged, and a spike when its findings have merged>
```

Nothing else goes in the feature header. What the code already settles is stated in chat when the decisions are walked and lives in the code; the architecture tables live in `AGENTS.md`; pins go beside the `Learned` line they pin.

The feature header goes where `references/tracker.md` put the stories: the epic's description on a tracker, the top of `docs/delivery/{slug}.md` otherwise. Stories already on the board are read as the proposed stories.

### The feature acceptance test

The outcome sentence gets one acceptance test of its own, and the user writes it.

* **The agent names, the user writes.** State the file, the runner, and the Given/When/Then the test must assert: the outcome sentence in concrete values, through the interface the user actually uses. The user writes the body. When the user asks the agent to write it, write it; the lock below still applies once it is committed.
* **It lives in a `feature-acceptance` directory inside the repo's test tree,** the directory the harness denies to the agent. When the harness can deny paths but does not, offer the `guardrails` skill once to add it before the commit. When the user declines, or the harness has no deny list, write under Critical Constraints in `AGENTS.md` that the directory is unguarded.
* **It is marked expected-to-fail, strictly,** in the framework's own way (pytest `xfail(strict=True)`, jest `test.failing`, or the nearest equivalent), so the suite stays green while it fails and goes red the moment it passes. That flip is the close-out signal. The user removes the marker at close-out; the agent never touches the file.
* **Commit it on its own on the first story's branch,** before the red commit. The first story's red commit waits for it. When the interface the outcome names has no test runner yet, the first story adds the runner, and the user writes the feature acceptance test after that story merges; the feature header says "after story 1" until then.
* **Locked from the agent for good,** unlike the red-commit guard, which clears at each merge. No subagent edits, moves, deletes, skips or re-marks it either. A wrong feature acceptance test is the user's to change. Before it is committed, run the `reviewing` skill on it once, as work the user made.
