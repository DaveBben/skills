# Holdout scenarios

Load this only when the user asks for holdout scenarios by name, in a session opened in the holdout directory. A holdout scenario is an end-to-end check the user writes in the terms of the system and its data. No agent that writes a feature's criteria, tests or code ever reads it, so the build cannot be fitted to it. The directory is `~/.holdout/<repository>/<slug>/`, outside every repository. The slug is the feature's name on its `story/{slug}/` branches.

This session may read the feature header (the `## Feature` block at the top of `docs/delivery/<slug>.md`, or the epic on the tracker) and the interface a person uses: the routes and their schemas, the command's help, the screens of the running app. It never reads the product's source or tests, and it writes nothing into any repository.

## 1. Write the scenarios with the user

The user writes 5 to 15 scenarios, one per way a person reaches the feature's outcome or fails to. Propose from the feature header's `Steps:` and `Not doing:`, and the user rewrites. `scenarios.md` starts with a canary line, a random ID no one would type (`canary: <uuid>`), then one block per scenario:

```text
## S3 Refund shows on the statement
Due after: 3, 5
Runs: 1
Given customer C-1001 has invoice INV-77 for 120.00 EUR, paid
When  POST /refunds {"invoice": "INV-77", "amount": "20.00"}
Then  GET /statements/C-1001 lists a -20.00 line dated today
And   the refunds table has one row for INV-77 with amount 20.00
```

* **Systems and data only.** Given names the rows a store holds or the state a person is in. When names the request, command or screen action, with values. Then and And name what comes back and the rows after, with values. No class, function or file name.
* **`Due after:`** lists the story numbers on the feature header's `Stories:` line this scenario waits on.
* **`Runs:`** is 1. The user sets more for a path that can vary between runs: a call to a model, two requests racing, a timing-dependent service. The scenario passes only when every run passes.
* **IDs never change.** A cut scenario stays as `## S<n> cut`.

## 2. Set up the runner

Copy [../scripts/holdout_run.py](../scripts/holdout_run.py) into the holdout directory as `run`, make it executable, and run `./run --self-test`. Write `runner.txt`, one line: the command that runs a list of files in the product's end-to-end framework and writes JUnit XML, with `{files}` and `{junit}` placeholders (`pytest -q --tb=short --junitxml={junit} {files}` is one). Give the user the `Holdout:` line for the feature header: the absolute path of `run`.

`run` prints one line naming scenarios by ID only: how many due scenarios pass, which newly fail, which failed again after being spent, which are unconfirmed, how many are unspent, and whether the canary or any scenario value appears in the diff it is given. The values and failure messages go only to `report.md` in this directory.

## 3. Turn each scenario into an executable, and confirm it

Once the interface a scenario uses exists, write one file under `executables/` whose name starts with the scenario's ID (`S3_refund.py`).

* **Drive only the interface a person uses,** and read stores the way an operator would, with a read-only query. Never import the product's code.
* **Assert every Then and And line.** Each assertion's message states the expected and the observed value in the scenario's words: "expected a -20.00 line on the statement, found none".
* **Print the trajectory,** one table: each request sent or action taken, what came back, and each row checked, before and after, with one column per Then and And line.

Run it against the running system and show the user the table. The user confirms that it checks what they meant, reading data, never the file. Then run `./run --lock S3`. An executable edited after its confirmation is reported as unconfirmed and never runs until the user confirms it again.

## 4. When a scenario fails

The user reads `report.md`, then decides:

* **A bug.** The user writes a bug report in their own words for the `deliver` loop, and this session adds `Spent: <date>` to the scenario. A spent scenario keeps running, and the loop now knows its case.
* **A wrong scenario.** Change it and confirm it again, or cut it.

When fewer than five scenarios are unspent, write more with the user. At close-out the user may move spent scenarios into the repository's `feature-acceptance` test directory as regression tests.

## 5. Keep it hidden

* **Never copy scenario text or values into a repository,** a commit message, a ticket or a prompt.
* **The canary catches copying.** Reading without copying leaves no trace. Where the product's agent harness can deny paths, the `guardrails` skill denies this directory and blocks shell commands naming it, except `run`.
* **Where a hard boundary is needed,** keep the holdout in a private repository instead. Its CI runs the scenarios against the story branch's preview deployment and posts the `run` line as a status on the pull request. The token the product's agent holds has no access to it.
