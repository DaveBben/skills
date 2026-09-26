# Attack tests

The attack subagent loads this after the review, on the story branch. It starts with a fresh context: it has seen neither the builder's work nor the session's chat. Its inputs are the confirmed criteria, the interface each criterion names (routes and their schemas, the command's help, the screens) and the story's diff against main. It reads nothing else about how the code was built: not the build prompt, the builder's choices, the Done block or the test table.

Its job is to find an input, a sequence or a caller that breaks a criterion. A second reader with the same inputs as the builder repeats the builder's blind spots, so it works from what the person using the system sees.

* **Write tests, never code.** Write each attack as a test in the project's own test framework, through the interface the criterion names. Put them in `attack/` inside the worktree's git directory (`git rev-parse --git-dir`), outside the source tree. Never edit product code, an accepted test or anything under `feature-acceptance`.
* **Attack each criterion where it is weakest.** Try the boundary values the criterion's numbers imply, the empty and the oversized input, the same request twice and at once, a caller who is not who the criterion assumes, a number arriving as a string, and a dependency that is down or slow.
* **Name the criterion.** Each test says which criterion it attacks, and the value it expects comes from the criterion's own words, never from running the code first.
* **Run them on the built code.** An attack counts only when it goes red. Read each red one's failure: when the failure is the test's own mistake, fix or delete the test and run it again.
* **Return at most ten lines:**

```text
Attack: <model>; <n> tests; <n> red
Red: <test file>:<test name> -> criterion <letter>: <what the person would see instead, in one line>
Unstated: <test file>:<test name> -> <the behaviour no criterion states, and the question it raises>
```

`Red` lines attack behaviour a criterion states. `Unstated` lines found behaviour no criterion decides: a timeout, what a repeated action returns, the wording of an error. Delete every green test, and leave the red ones in `attack/` for the build to take.
