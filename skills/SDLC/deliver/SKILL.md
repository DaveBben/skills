---
name: deliver
description: "Use this skill before touching any file on a request to add, change, fix or remove behaviour in code that exists, or to build stories already mapped. Use it on: 'add X', 'fix the bug where X', 'X is broken', 'refactor X', 'build story X', 'work through this epic', 'write the acceptance criteria', 'pick up where we left off', 'write the PR description'. Use it even when the change looks small. Takes each story through agreed criteria, failing tests, a build, a review and a pull request into main."
license: MIT
metadata:
  version: "20.0.0"
# Claude Code only: registered when the skill runs, for the rest of the session.
# scripts/hook.py says what each handler does; any agent reaches the same rules
# through `story.sh next`. Without the plugin's path or python3, each exits 0.
hooks:
  PreToolUse:
    - matcher: "Bash|Read|Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: 'f="${CLAUDE_PLUGIN_ROOT}/skills/deliver/scripts/hook.py"; [ -f "$f" ] && command -v python3 >/dev/null 2>&1 || exit 0; python3 "$f"'
  PostToolUse:
    - matcher: "Agent|Task|Bash|Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: 'f="${CLAUDE_PLUGIN_ROOT}/skills/deliver/scripts/hook.py"; [ -f "$f" ] && command -v python3 >/dev/null 2>&1 || exit 0; python3 "$f"'
  Stop:
    - hooks:
        - type: command
          command: 'f="${CLAUDE_PLUGIN_ROOT}/skills/deliver/scripts/hook.py"; [ -f "$f" ] && command -v python3 >/dev/null 2>&1 || exit 0; python3 "$f"'
---
# Deliver

Take a request from its outcome to merged pull requests. Every behaviour change starts as failing tests committed before any code, and the user agrees each story's criteria before anything leaves the machine.

## Words used here

* **Tracker:** the project tracker the `Backlog:` line of `AGENTS.md` names, reached by the methods listed under it. An epic per feature, its stories and spikes as child issues with blocking links, each issue's comments as its log. The **slug** is the epic's key, or the issue's key for a one-story request.
* **Feature header:** the epic's description, in named lines such as `Outcome:`, `Success:`, `Context:`, `Release:` and `Decided:`. A one-story request has none; its issue's description stands in.
* **Story:** a change a person outside the system can observe, in one workflow step and one variation.
* **Criterion:** one Given/When/Then statement of what a person sees; the `setup` agent tags each that records a product choice.
* **Feature acceptance test:** the one test the user writes for a feature's outcome, in a `feature-acceptance` directory the agent never edits, marked strictly expected-to-fail until the feature is whole.
* **Parked:** a question written on a story's issue as a comment starting `Parked:`, edited or deleted once answered where the tracker allows. The story keeps going up to the step that needs the answer. **The waiting question** is the oldest parked question only the user can answer that the loop cannot move past; a `Parked: ask <person>` question is not one, and neither are criteria still being built on.
* **[scripts/story.sh](scripts/story.sh):** the git steps of a story. `story.sh next` prints the rules of the step a story is at; `story.sh next <step>` prints a named step. Run it with no arguments for its usage.

## Talking to the user

Sort every question, including each one a subagent returns, before it reaches the user:

* **A fact the agent can reach** (what a table holds, whether a secret exists, what a route returns, what CI runs): look it up with the `lookup` agent given the one question and the paths, and use the answer. Ask only when no tool reaches it, and say where it looked.
* **A fact only a named person knows:** write `Parked: ask <person>: <question>` on the story, tell the user once whom to ask, and work on what the answer does not block. After one failed run against another team's system, do the same with that team's owner.
* **A technical choice a `git revert` undoes, that no person sees and no later story inherits:** decide it and list it among the choices decided alone.
* **A repository setting** (product-choice criteria per story, default 8; stories at once, default 1): use the default here and record it in `AGENTS.md`, else on the feature header.
* **The loop's own next step** (write criteria, run a review, start the next ready story, push a story the user confirmed): take it.
* **Product intent, or a choice expensive to reverse:** ask the user. Branching a story from anything but main is one: another person's branch can be force-pushed or abandoned under it. The question names the function on that branch that calls the story's code, and why main cannot run it yet. Record the answer on the header's `Context:` line.

Then ask:

* **One question per message:** ask only the waiting question, and hold every other until it is answered. Name the repository and the story or feature in plain words inside the question's first sentence. Use the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion), recommended option first, each option with its consequence in one sentence.
* **An answer that fits no option** ("yes" to an either/or) gets the question again, naming the options.
* **Never restate a question.** It lives on its story as a `Parked:` comment. When a subagent returns nothing the user must act on, send nothing.
* **A command the user must run:** write it so that one run prints every step's result. When the harness blocks a command that reads a secret or health data, or that force-pushes, say so and ask whether the user wants to run it.
* **Where things stand.** Open with the `Outcome:` line and one clause per repository saying its part, then any core or sketch (the piece of a story the user writes by hand) waiting for the user, by file and line, then the stories done out of those above the release line (the header's `Release:` list), and how many were added since the map was agreed. Then one line per repository tracing the path one unit of work takes through it today, and the step not yet built, with the story that builds it: "conversion runs in the function; nothing writes the table the engine reads; PAY-12 connects them". Then one line per open story (key, what it does in plain words, and building, in review, or which question it is parked on), each `Parked: ask <person>` with whom to ask, what threatens the `Target:` date, and the waiting question.
* **Overload.** When the user says they are overloaded, send one message: where things stand without the waiting question, opening with "Nothing needs you now" when no question waits for the user. Ask the waiting question in the reply to their next message.

The message that reports an opened or merged pull request also carries whether the last merged story deployed and what its `Success` signal showed, and the splits, new stories and choices the loop decided alone. A signal that moved the wrong way past its noise band goes in the next message, whatever it reports.

## Subagents

Each step runs in its own subagent, defined by one file that holds its whole prompt, in the plugin's shared `agents/` folder beside this skill's folder. The `review`, `security` and `refute` agents are the same ones the `review-code` skill runs, so every code review is the same review:

| Step | Agent | File |
|---|---|---|
| A fact lookup | `lookup` | [../agents/lookup.md](../agents/lookup.md) |
| Setup: criteria, test table, red commit | `setup` | [../agents/setup.md](../agents/setup.md) |
| Every change to source code: a story's build, a change with no behaviour change, a trivial fix, a rebase conflict | `build` | [../agents/build.md](../agents/build.md) |
| Refactor, the last step of test-driven development | `refactor` | [../agents/refactor.md](../agents/refactor.md) |
| Review: attacks, correctness, test strength, stated intent | `review` | [../agents/review.md](../agents/review.md) |
| Security review, after the review when the story needs one | `security` | [../agents/security.md](../agents/security.md) |
| Refute | `refute` | [../agents/refute.md](../agents/refute.md) |
| Pull request description, or a reply to a reviewer | `description` | [../agents/description.md](../agents/description.md) |
| Any other delegated task that changes no code: running a command, reading CI output, a tracker write, a story's log comment | `worker` | [../agents/worker.md](../agents/worker.md) |

Where the harness loads named agents, launch each by its name (Claude Code's SDLC plugin installs them as `SDLC:setup` and so on). Otherwise launch a general subagent told to follow its file. Give it the inputs its step names, and paths in place of file contents. Give each `lookup` or `worker` agent that touches the tracker the path of [references/tracker.md](references/tracker.md) and the `Backlog:` block. An agent stopped at its turn limit returns its work marked partial: resume it once with what remains, and treat a second stop as a split or a question. This session reads `AGENTS.md` itself. The `lookup` agent does every tracker read and returns only what this session asks for: the feature header lines as written, and each issue's key, status, blockers and `Parked:` lines. A whole issue, an API response or a script never enters this session. Hand every tracker write this session has spelled out to a `worker` agent, all the writes ready at the same moment to one worker as a numbered list. This session never reads a diff, a test or source: a change to source goes to the `build` agent, and any other task that needs one to the `worker` agent. Where the harness has no subagents, run each step inline, one story at a time, and say so once.

## Start

* **Read `AGENTS.md`** in each repository the work touches. With no `Backlog:` line, connect a tracker by section 1 of [references/tracker.md](references/tracker.md). When `AGENTS.md` names no check command, the one command that runs every check, use what CI runs, else the test command the README gives; when it records no red-commit command, commit red tests with plain `git commit`. Record both as decided alone. When the user declines red commits, the tests land in the build's first commit and `story.sh red` records that commit. Mention once that the `guardrails` skill sets these up properly; ask nothing.
* **Resume:** run `story.sh status` from each main checkout. When it prints a story, or a story carries a `Parked:` comment, run `story.sh next resume` and follow it.
* **The tracker cannot be reached** (an auth error, a 401 or 403, a tool that is not connected): run `story.sh next tracker-down` and follow it.

## Size the request

Write the outcome in one sentence and the steps a person takes, and size from those, whatever the request calls itself.

| Size | Test | Path |
|---|---|---|
| No behaviour change | A refactor, a dependency bump, a rename, or tests for behaviour that exists | Cut the branch with `story.sh start {key} {key} <name>` when an issue exists, else `git worktree add -b story/<name>/<name> <path>`; the `build` agent makes the change; then `story.sh next confirm`, confirmed with a plain yes. The pull request is the record, linked to the issue when one exists. |
| Trivial | Nobody is harmed before a `git revert` lands: copy, layout, a dev-only tool | One outcome criterion, shown to the user; cut the branch as above; the `build` agent commits one red test and the fix; the check command; then `story.sh next confirm`, confirmed with a plain yes. |
| One story | One step and one variation, nothing unknown | "Each story" below, on one issue with no epic, whose comments are its log. |
| Several stories | More than one step or variation, an unknown that changes what gets built, a PRD or an epic | The `epic` skill first, for the feature header, the story map and the feature acceptance test, then "Each story" for every story. |

A bug is sized like any request; its first criterion is the reproduction. A red CI run is a bug report. A request only for criteria runs the `setup` agent with no worktree, told to stop after its sections 1 and 2, and shows the card; a request only for a pull request description runs the `description` agent on that branch. When a decision that costs more than a day to reverse is open (a library, a data shape, a trust boundary, a new repository), or a fact nobody can supply without building (a library's real behaviour, a throughput number), run the `architecture` skill with the user before the story that needs it.

## Each story

A story moves through set up, show the criteria, build, refactor and review, act on the review, verify, confirm and open, and the open pull request. Start each story with `story.sh next setup`. After every step, run `story.sh next` in the story's worktree and do what it prints: the step's rules, the agents to launch with their inputs, and the step that follows. Launch the `setup`, `refute` and `description` agents in the foreground, since their return starts the next step.

## Park, and decide alone

Also park a story on: a product decision a test row exposes that no PRD or ADR (a decision record under `docs/adr/`) records; a criterion that cannot be written as a test; a `Deferred:` decision the story needs, decided with the `architecture` skill; a change to behaviour the feature acceptance test asserts, since only the user edits it.

A decision on one story that changes another story's criterion writes `Parked: criteria: <letter> changed by <key>` on that other story. When that story has a red commit, the change is a wrong row on it: run `story.sh next wrong-row` there. When it has not started, rewrite the criterion on its issue. Its confirm step shows the change before its push.

Decide these alone and list them in the next pull request message: a split, by the split patterns in section 4 of [../epic/SKILL.md](../epic/SKILL.md), closing the original as `cut: split into <keys>`; a new story for a bug in shipped work (a bug issue under the epic, ranked by the user) or a `Learned` fact that changes what gets built, when a person sees the failure on its own, ranked below the release line unless the user moves it above; a property of open stories (what their log lines hold, a limit they share) is a row on each of them instead, parked as above; a rebase conflict resolved outside test files.

## Merge and next

* **Stories at once.** Set up the next ready story when a pull request opens, up to the number `AGENTS.md` states, else 1. A story counts from setup until its pull request opens. Branch only from main, unless the user chose another base for the story; then run `story.sh start` with `MAIN=<base>`, and the script keeps rebasing that story on it. A story whose blocker is unmerged, or waits on another person's branch, waits for that merge.
* **Deploy from main** by a command committed in the repository, and exercise the rollback once before anything a revert cannot undo.
* **Stop** after the merge for a request that was not an epic. For an epic, close out with the `epic` skill when every child above the release line is done or cut. One epic is one loop; never interleave two in one session. The loop crosses a sprint boundary without stopping unless `AGENTS.md` says to stop there.
* **In a team,** each story has its own branch and worktree per repository and writes only its own comments.

Keep going after showing criteria, after a subagent returns, after a pull request opens while another story is ready, and while a `Parked: ask <person>` question waits; none needs the user. Stop for the waiting question, for the user's one-line confirmation, for a second round of blocking findings, and when nothing is ready and nothing is building. Watch open pull requests with one background command that prints a line only when something changes and wakes the session on it (Claude Code's Monitor tool runs one), never a prompt re-run on an interval.
