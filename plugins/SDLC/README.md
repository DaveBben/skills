# build like an engineer

**Well-understood engineering practice, run *with* you by an agent rather than recited at you.**

None of this is new. Framing the problem before solving it, stating the contract before building against it, walking how a thing breaks by accident and then on purpose, knowing what you cannot undo: this is ordinary engineering discipline and most of it predates the tooling by decades. What is new is an agent that can hold all of it at once and walk it with you.

The workflow is derived from two podcast episodes, and most of what is specific rather than generic in here traces back to one of them:

- **[Florian Buetow on Beyond Coding](https://www.youtube.com/watch?v=W1uG25of2t0)** with Patrick Akil, 10 June 2026. Code review as the bottleneck once agents write the code, and shaping the environment so corrections become rules instead of repeat conversations.
- **[Dex Horthy on The Pragmatic Engineer](https://www.youtube.com/watch?v=Usufn8IQJgw)** with Gergely Orosz, 15 July 2026. Context engineering, why prose specs drift out from under you, and slicing sized to what a human will actually read.

The plugin is nine skills. Plain Markdown, no build step, nothing to compile.

| Skill | Fires on |
|---|---|
| `deliver` | any request to add, change or fix behaviour in an existing app: "add X", "fix the bug where X", "X is broken", "build story X", "work through this epic"; "what should I pick up next"; "write the PR description" |
| `define-work` | "turn this prd into stories", "break this epic down", "plan this feature" |
| `architecture` | "let's build this" in an empty repository, "how should this be structured", "should I use X for storage", "write an adr", "we will accept that risk" |
| `story` | "write the acceptance criteria", "is this story ready", "what tests should this have", "is this covered" |
| `reviewing` | "review what you built", "review PR 412", "review this epic", "give me feedback", "poke holes in this" |
| `orient` | "orient yourself", "setup claude in this repo", "write AGENTS.md", "streamline my CLAUDE.md" |
| `guardrails` | "set up guardrails", "we have no linting", "add a rule", "the agent keeps making this mistake", "write a semgrep rule" |
| `spike` | "prototype this", "let's see if X is feasible", "throwaway" |
| `greenfield` | "python project template", "template project"; usually called by `architecture` |

Session handoff, once part of this plugin, now lives in the separate [context](../context/) plugin. Plugins are independent, so nothing in SDLC calls it; install `context` to have it.

`deliver` carries the whole change loop. It used to be six skills, one per stage, and collapsing them was a bet: that a capable model needs orientation rather than a numbered walk, and that most of the length was telling it things it already knew. The bet paid off. What is left is the part it would get wrong by default.

## Three convictions

**Most things do not need to be built.** Every feature is a permanent liability with a running cost. So framing asks what the user will do differently once this ships, and when the answer is already possible in this system or off the shelf, that is the answer. "Do not build it" is a real outcome, and it is recorded as an ADR, because no later step runs to catch it.

**Most requests are not well thought through, including the ones that sound settled.** A decided-sounding one-liner is the normal shape of an unsettled ask. Requests arrive naming a mechanism instead of a need. So the first move is reading the request, not answering it.

**The failing test is the unit of account.** A settled constraint becomes a complete failing test before any implementation exists, and that does not scale with the size of the change. A one-line fix still gets a test.

---

# The workflow

```mermaid
flowchart TD
    REQ([a request to change something]) --> OR[orient: AGENTS.md, the floor, the log]
    OR --> FR[define-work: outcome, problem, stories with an outcome line and blockers]
    FR --> ARC[architecture: spikes, numbers, processes, modules and flows, each decision an ADR]
    ARC --> REC[record: the feature header and the feature acceptance test]
    REC --> NX[pick the next ready story]
    NX --> CR[criteria subagent: story criteria]
    CR --> OK([you confirm the criteria])
    OK --> SL

    subgraph SL [per story]
      BR[branch from main] --> TT[test table] --> RED[red commit] --> BLD[build subagent] --> REV[review subagent] --> ATK[attack subagent] --> VER[verify the whole feature, holdout, signals] --> LOG[log] --> PR[pull request into main] --> MRG[wait for merge]
    end

    MRG --> NX
    MRG --> OUT[close out: promote learnings, check the success metric]

    SL -. pause .-> USER([the user])
    ARC -. untried crossing .-> SPIKE[spike]
    OR -. no floor .-> HARN[guardrails]
```

Two phases. The first runs with you, once per feature. The second runs once per story: you confirm its criteria, then tests, build, review and a pull request follow, and you answer questions as they come up, and for an epic it keeps going until every story is merged or cut. Every request is sized first, from its outcome and the steps a person takes, never by whether it is called a bug or a feature. A refactor that changes no behaviour needs no criteria: the suite stays green before and after, a review runs, and a pull request opens. A trivial change (copy, layout, colour) is one criterion, a red commit and the fix, on a story branch with a pull request. A single story skips the first phase and runs the per-story loop on a branch from main. Only a request that is several stories, or hides an unknown that changes what gets built, runs the first phase.

## With you, once per feature

**Orient.** The agent reads `AGENTS.md`, checks the repo gives it feedback of its own (a check command, a suite green on main, a mutation runner), and offers `guardrails` when it does not. When a log exists it tells you in one line what the last story changed. The criteria subagent reads the `Learned` lines, the ADRs and the PRD for each story.

**Define.** `define-work` runs with you. One sentence for the outcome: what you do differently once this ships, and where you see it. A sentence naming a table or an endpoint is rejected, since it is true when the work is half done. Then the problem, the non-goals, and the stories and spikes with what blocks each. Only stories and spikes get cards: a non-functional requirement, an enabler or a decision becomes criteria or a comment on the story it belongs to. Each story gets a title, an outcome line and its blockers here. Its criteria wait until it starts, when `story` writes its outcome criterion plus its boundary, failure and abuse criteria, each a Given/When/Then in values a stranger could check, using what the earlier stories taught. It walks the failure paths and the abuse paths so the decisions they hide, what a repeated submit returns, how many requests a minute one source gets, how long a half-finished state lives, are yours rather than the builder's, and it keeps the standards nobody would choose against out of the criteria. There is no feature branch: every story branches from main and merges back into it. A spike runs only when a fact about the world blocks the criterion, and its code is deleted.

**Architecture.** `architecture` runs with you, the XP way: find out what is unknown, take a broad starting shape, record each decision, prove the shape with a walking skeleton, and change it by refactoring. For a new application it owns the path end to end, then runs `greenfield` per new repository and hands the walking skeleton to `deliver`. It lists each crossing the walking skeleton makes, the places its outcome passes from one running piece into another, and runs a spike on each untried one before anything else. Then it asks four numbers: how many at once, how fast, how much downtime, how much data. It asks which data is sensitive and where it may be stored. "Unknown" is an answer. It draws three tables: the processes with how many copies run and what starts each, the modules with what each owns, and the flows between them with what a person sees when the other side fails and who else can reach the other side. Every flow that crosses a process, a machine or a repository, the data's shape (what makes a record unique, the rules it must keep and who enforces them, retention, backup and restore, schema changes) and each repository's language are put to you one per message; each answer becomes an ADR, a deferral with what will force it, or waits on a spike. The tables go into `AGENTS.md`, never a separate document, and every build prompt cites the module the story lives in and the flows it may call. For a third-party service whose sandbox cannot produce the volume or the failures you name (429 after 100 a minute, a webhook delivered twice), it records a twin: a fake of the service whose contract suite also runs against recorded real responses on a schedule. It also asks which modules you read on every change.

**Record.** You confirm, reword, cut or add stories in one turn, by title and outcome line. No estimates. The result is the feature header at the top of `docs/delivery/{slug}.md`, committed with the ADRs on a plan branch whose pull request you merge before the first story. When `AGENTS.md` names a Jira project or another tracker, the board is the backlog instead: the epic is the feature, its children are the stories in rank order, stories already on the board are read as the proposed list, and every log entry is a resolution comment. No `docs/delivery/` file is kept then.

**feature acceptance test.** Every criterion of every story has its acceptance test, written by the agent. You write one more for the outcome sentence itself, through the interface you actually use, marked expected-to-fail so the suite stays green until the feature is whole. The agent names the file and what it must assert, gives feedback on what you wrote, and never touches it again: the harness denies that directory to the agent for good. When it passes, the feature is done; when it passes early, the remaining stories are questioned.

**Holdout scenarios.** Optionally, you also write 5 to 15 end-to-end scenarios in the terms of the system and its data (the rows before, the request, what comes back, the rows after), in a separate session under `~/.holdout/`, outside every repository. No agent that writes criteria, tests or code reads them, so the build cannot be fitted to them. The deny list and a shell hook keep agents out, and a canary string catches any copy into the repository. Only verify runs them, and it gets back one line of counts; a failure goes to you, never to a builder.

## Per story

1. **Criteria and setup.** The loop picks every ready story. For each, the agent cuts `story/{slug}/{n}-{short-name}` from main in its own worktree, one per repository the story changes, and a criteria subagent writes the criteria with `story`. The story waits until you confirm or edit them; on a tracker they then go to the story's issue. A setup subagent then writes the test table with `story` and the red commit. A story that spans repositories merges the called repository's pull request first, compatible with old callers, then the caller's, and removes the old form in a later story.
2. **Table.** `story` proposes one entry per test: an index table with the level, the generator that produced it and the change that must turn it red, then a bold Given/When/Then block per test. The acceptance row runs through the interface you actually use, a browser, an API or a command, and cannot be cut. The agent applies the cut rules itself.
3. **Red.** Every row as a failing test, committed on its own with the criteria and the table in the message. A guardrails hook refuses edits to those files until the merge.
4. **Build.** A subagent with one prompt: the contract, a prohibition list of things models add unasked, an instruction to grep for what exists before writing a helper, and the environment facts it would otherwise improve into something wrong. The agent runs the tests itself afterwards; the builder's report is a claim. A red row or a touched file outside the story resets the tree to the red commit and reissues once, then the story is split. A row the builder shows cannot be satisfied comes back to you to correct instead. A choice the builder meets that changes what a person sees, such as wording, a default or an error message, comes back to you as a question.
5. **Review and attack.** A `reviewing` subagent that saw none of the chat runs three passes: correctness (every mutation applied, every row goes red), subtraction (delete what no row asked for), scars (pinned values unchanged). Then a refactor while green, and a Done block listing every choice made without you and every refactor it proposes but did not make. Then a fresh subagent, given only the criteria, the interface and the diff, writes tests that try to break a criterion, on another model where the harness offers one. An attack counts only when its test goes red on the built code.
6. **Verify.** The story branch rebased on main, the full suite, and the story's acceptance tests through the interface you actually use, against the running system. Every earlier acceptance test runs too, then your holdout scenarios when you keep them. A script lists every signal that you should read code: a change to the checks themselves, a skipped test or silenced check, a test weakened after the red commit, a test value branched on in production code, and any path under the `# owner reads:` sections of `CODEOWNERS` (auth, secrets, money, health data, migrations, deploys, dependencies).
7. **Log.** The log entry marks the story done, and records what shipped, what was learned, any proposed refactor and, for a bug, why nothing caught it. It is the last commit on the story branch.
8. **Pull request** into main. Its first line says `Read code: none` or names the slices to read, each at most 40 lines with what it decides and the one question to answer; for the first ten stories you read every diff anyway, to test the list. Its body is written by `deliver` for a reviewer who has never opened the repo: why, a table of criteria and the tests that prove them, how to try it on the branch with the result it produced, what changed, the risk (auth, money, health data, a migration, anything a revert cannot undo), what it assumes, what to read first, the other tests and the Done block collapsed, and the signal you will read to know it worked. Under one screen.
9. **Merge.** You merge into main, and the story can deploy, behind a flag when it exposes half a feature. The agent polls where it can, otherwise ends the turn with the link. Then the loop picks the next one.

When the story list is empty, the agent promotes what was learned, asks whether the PRD's success metric moved, and asks which pause or check cost time without catching anything. You observe each story's signal once deployed.

**For an epic the loop runs until every story is merged or cut.** Criteria, setup, build, review and verify each run in a subagent, so the main session stays small. While a pull request waits for your review, the loop starts other stories whose blockers have merged, each in its own worktree; a story whose blocker is still in review waits for that merge. The loop splits stories and adds new ones itself, and tells you. It parks one story, and keeps working on the rest, when: its criteria wait for your confirmation; your feature acceptance test is not written yet; the builder asks about a choice a person would see; an accepted test row turns out wrong; a deferred or new architecture decision is forced; a test row exposes a product decision no PRD or ADR records; a criterion cannot be tested or contradicts `AGENTS.md`; the story removes behaviour your feature acceptance test asserts; the feature acceptance test passes; the live PRD contradicts the header; you said you will write the code. It asks each question the moment it arises and keeps working on other stories while it waits. There is no fixed story order. The loop picks from the stories whose blockers have merged, starting from your rank, and names every departure from it. A trivial or single-story request stops after its merge.

---

# What you end up holding

| Artifact | Where | Fate |
|---|---|---|
| Spike findings | the slug's feature log, as `Learned` lines | durable; the code is deleted |
| Feature log: the feature header and one entry per story | `docs/delivery/{slug}.md`, or the tracker epic | durable, kept after the last story |
| ADR | `docs/adr/architecture/` or `docs/adr/{slug}/` | durable, committed before the code that depends on it |
| Architecture tables: processes, modules, flows | `AGENTS.md`, under the Architecture block | durable, rewritten when a story changes the shape |
| feature acceptance test | the test tree's `feature-acceptance` directory | durable; written by the user, denied to the agent for the life of the repo |
| Holdout scenarios | `~/.holdout/<repository>/<slug>/`, outside the repo | the user's; spent ones may become regression tests at close-out |
| `# owner reads:` sections | `CODEOWNERS` | durable; the paths you read on every change |
| Failing tests, then passing | the repo's test tree | durable; the red commit message holds the criteria and the table |
| Rules and contracts | the repo, via `guardrails` | durable, added to when a bug's `Not caught by` names a gap |
| Pull request body | the remote | durable; the one place a stranger can read what a story did and why |

There is no spec and no design document. Those paths are the defaults; tell the agent in conversation if your repo keeps things elsewhere.

## Why the split exists

Everything durable is written in a language that can be checked. Everything written in prose is either thrown away or kept short enough to reread.

Prose and code become two sources of truth and drift apart. A rule that executes cannot drift, because a violation fails the build. So the constraints the conversation carried are promoted into tests, guardrails and architectural tests, and the conversation itself goes.

The ADR is the exception, and it is one for a specific reason: it makes no claim about what the system currently does, so there is nothing for it to drift from. It says what was true at a moment and why a door was closed. What it records, the alternatives that lost and the assumptions the decision rests on, is not recoverable from the code and cannot be regenerated the way research can.

The feature log is the other exception, and it is kept small on purpose: a feature header under one screen and one entry per story. At close-out every unpinned `Learned` line is promoted to a test, an ADR or an `AGENTS.md` line, so nothing the log knows lives only in the log.

This is also why the red commit message carries the criteria and the table verbatim. The reason a number is 100 rather than 150 has to survive the conversation that settled it.

---

# The skills around the loop

**`guardrails` prepares a codebase.** It runs before feature work, not as part of it. It reads what exists rather than assuming a fresh project, then branches on greenfield or brownfield, and the branch is not project age: a two-week-old repo with a thousand lines and no linter is brownfield.

It is language agnostic, and deliberately carries no toolchain. It names thirteen slots, states what a filled slot has to do and which of the three layers it fires in, and leaves the choice of tool to the model, which already knows the ecosystem. What it does carry is the part the model would otherwise get wrong: the placement rule, in seconds, for which layer a check belongs to; the settings that are decisions rather than defaults, each with a silent failure mode; and the requirement to watch a check fail once before trusting it.

Greenfield runs forward: read the dependency shape `architecture` wrote into `AGENTS.md`, encode every in-process flow as an architectural test, then set up the rest of the checks. It does not work out what the system should be, and where the shape is still open it encodes the language-level checks now and comes back for the architectural tests once the first change has settled it. Brownfield runs the same ground in the opposite direction: fill the slots, then have the agent draw the current dependency graph and encode the edges that surprise you, because those are the ones nobody chose, and only then name the anti-patterns already in the code and write rules for them. Encoding the whole current graph makes the mess permanent.

Both paths end at the same place, a feedback loop split across three layers by cost: format and lint on every edit, whole-package checks at turn end, everything at commit and in CI. Each layer is a subset of the same command list, so what gets fixed at edit time is never rediscovered at commit time. The loop safety is wired before the checks: a retry counter, re-verification after each fix, a skip when nothing relevant changed, and failing open when a checker cannot run. A blocking check with no escape traps the agent on an error it cannot fix.

Three things go into the instructions file before any correction has been made, because none of them shows up in a diff. That silencing a check is not passing it, which goes in verbatim, because the pressure to loosen a config is created by the gate this skill just installed. Where a future correction is meant to land: a static check into the rules directory, a dependency direction into the contracts, a file-specific instruction into a path-scoped rule, anything conversational into the root file. And an answer-length rule, offered rather than imposed, since that file is the user's.

An instruction that governs the conversation is never path-scoped, since path frontmatter would load it only when a matching file is touched. The root file is capped at 100 lines, because every line in it costs context on every turn and a bloated one makes the agent ignore the rules that matter.

Brownfield gets one thing greenfield does not, and it is a decision rather than a step. Every rule just added is violated by code that predates it, so enforcement is either scoped to files authored from here on, or the backlog is cleaned up as a change of its own. Both are real answers. Adding rules and leaving them red is not.

**`architecture` also records one decision.** Recording is a moment, not a stage: an expensive or irreversible choice, an accepted hazard, or an explicitly rejected alternative. `architecture` takes that path alone when the request is one decision, and writes the ADR the moment the decision is made rather than batching records at the end, by which time the alternatives that lost are gone. Its template always carries `Alternatives rejected` and `Detector`, because an ADR with no rejected alternative recorded a preference rather than a decision.

**`reviewing` reviews anything already made.** It picks one review by subject: code the agent built (three passes, then a refactor while green), a pull request someone opened (what it lands on, what the tools reported, then the five things no tool reports), an existing epic (it calls `define-work` for the rules the epic is judged against), or work you made (every point sorted into wrong, unverified, shape or preference, with the principle named and the rewrite left to you). Reviewing your own work is the manual-flying practice the loop no longer forces.

**`guardrails` also puts one rule where it will be followed.** A check a program runs is followed every time, and an instruction an agent reads is followed when the agent remembers it. So each rule goes to the first place that holds: a linter setting, a type check, a dependency contract or a Semgrep rule; then a rule file the agent loads only for matching paths; then one line in `AGENTS.md`. A one-rule request loads the rules reference and only the one setup section its rule needs. It also audits the instruction files and deletes each line once its check lands.

**`orient`, `define-work`, `story`, `spike` and `greenfield`** each do one step the loop calls by name, and each runs on its own when asked: write `AGENTS.md`; turn an ask into stories and spikes; write one story's testable acceptance criteria and its test table; answer one question with throwaway code; stand a new repository up from a template, in the language `architecture` recorded.

**Session handoff lives in the [context](../context/) plugin** as the `handing-off` skill. Plugins are independent, so nothing in SDLC calls it; install `context` to have it.

---

# Why not a prose spec

This started as an attempt to address the shortcomings of spec-driven development, where planning and specification are done up front and reviewed before being handed to an agent to implement.

A lot of people call that waterfall in disguise. I don't fully agree, but the pitfalls are real:

- A spec does not guarantee results. Hand the same spec to different models and get different implementations. The spec becomes an aspiration, not a contract.
- Reviewing a spec takes more cognitive effort than reviewing the code it produced. It is easier to read the diff and run the tests than to match every requirement to the code it was supposed to produce.
- A thousand-line Markdown file gets produced for a twenty-line change.
- Specs go stale quickly and confuse the agent. A detail that was relevant at authoring time is still there three features later, and the agent anchors on it as a constraint.
- A hundred specs sitting in a repo have to be read manually to avoid contradicting them.
- Most spec frameworks are heavy on ceremony, unfriendly to brownfield, and awkward to work with in an agile fashion.

We already have specs. They are tests. Deterministic pass or fail, and they do not lie about the code. What they cannot carry is the **why**, and that is what the ADR is for.

## Where tests stop

A behavioural test binds what the system does at one moment. It cannot fail when the design decays, because decay has no wrong answer on the day it is introduced. The imports still resolve, the suite still passes, and the bill arrives three months later as a change that touches nine files instead of one.

So the loop has three places for a constraint rather than one. Behaviour gets a row in the test table. Structure gets a rule that executes: dependency direction, boundary membership, ownership, a budget, wired through whatever the repo already runs by `guardrails`. And what nothing can reach is written down as exactly that, under what the pull request says is deferred or as an ADR, and observed through the story's signal once deployed.

That leaves the decision itself, which neither reaches. The ADR's "What it doesn't buy" section carries it: what must stay true, and what would make this wrong. That is the trigger for revisiting. A test asserts that one hop of delegation works; only the ADR says that one hop was an assumption rather than a requirement.

## What the research says, including where it disagrees

Some of this is better evidenced than I expected, and some of it cuts against the idea. Both are here.

**"Tests don't lie" is too strong.** Tests encode whatever the spec says, *including its errors*, and they do it invisibly. Mund et al. injected one subtly wrong requirement into a real 21-page industrial spec and asked 41 people to derive test cases from it: **zero detected the defect and zero correct test cases were produced**, even in the group given a briefing that stated the correct behaviour. Tests don't lie about the code. They will happily lie about the intent.

**Deriving expected values independently is not a style preference.** It is what aviation certification requires, and DO-248A states the mechanism: "It is a natural tendency to consider outputs of the actual code as the expected results. **This bias cannot occur when expected outputs are determined by analysis of the requirements.**" Using the code as the oracle contaminates the oracle. The same document concedes that requirements-based testing cannot evidence the absence of *unintended function*, which is why the review reads the diff for what crept in rather than trusting a green suite.

**The honest limit on absence.** A test refutes; it cannot confirm. Refuting a safety property ("X never happens") takes one failing execution; confirming it means quantifying over every execution there is. That is a proved result, not a budget problem, and it is why "no unauthorized path" ends up as a permanent gap checked against production rather than a test that pretends to settle it.

**The biggest risk to this approach is staleness, and it has a number.** In a study of Ruby projects, executable scenarios and production code co-evolved in only **~37%** of cases, and where they did, the spec changed *after* the code. A green test suite is indistinguishable from a suite full of requirements that expired. That is what the ADR's "What it doesn't buy" section exists for: a constraint with no recorded invalidation condition dies in silence while the tests keep passing.

**The closest thing to prior art mostly failed, and it is worth knowing why.** Specification by Example is the same bet, and Gojko Adzic's own ten-year retrospective (514 respondents, recruited from his advocacy channels) concluded that "the idea of specifications and tests in a single document didn't really work out." Only 12% kept text files in version control as the source of truth; 26% of business representatives "mostly do not care about the examples"; 61% of BDD practitioners in a separate survey found duplication made specs hard to extend. But read what failed: a **separate natural-language layer** maintained alongside the code for stakeholders who turned out not to read it. That layer is the thing this plugin deletes. The finding that only 12% kept the living document in version control is, if anything, evidence for the choice.

**And the ceiling that applies to everyone.** Naur: "program revival, that is reestablishing the theory of a program merely from the documentation, is strictly impossible." That applies to prose specs exactly as much as to tests. So the claim here is not that tests capture what prose cannot. It is that **these two artifacts fail differently**, tests rotting loudly and prose rotting quietly, and neither one reconstitutes the theory in someone's head. The ADR is a hedge against one failure mode, not a solution to the problem.

**One thing to hold this methodology to.** Every reported failure of BDD gets answered with "that isn't BDD, you did it wrong." A technique whose failures are always the practitioner's fault has no failure conditions, so no evidence can ever count against it. If this approach costs you more than it returns, that is a result about the approach.

## Where the workflow itself comes from

The stage structure is derived in `research/combined-development-strategy.md`, which merges the two episodes linked at the top:

- Florian Buetow on **Beyond Coding**, 10 June 2026: [YouTube](https://www.youtube.com/watch?v=W1uG25of2t0), [Pocket Casts](https://pca.st/episode/ab84ca98-407b-4445-b08b-2d7e31c12a30)
- Dex Horthy on **The Pragmatic Engineer**, 15 July 2026: [YouTube](https://www.youtube.com/watch?v=Usufn8IQJgw)

Every line there states why it is in, and the two conflicts are resolved at the point they arise. Transcripts and derivations live in `research/`, which is never loaded by any skill. Neither guest had anything to do with this plugin, and any misreading of them is mine.

Both arrive independently at the same structural claim, that feature work and environment work are separate projects running in parallel. That is why `guardrails` is a skill of its own rather than a step in the change loop.

The two conflicts are worth naming because the resolutions shaped the skills:

- **Does a human read the code?** Buetow says interrogating the agent can replace reading it. Horthy ran the lights-off version for four months and shut it down, with a specific bug and a recovery cost. Resolved toward Horthy: the interrogation stays as the way new rules get discovered, the substitution does not. This is why every story is one pull request under one screen of description, and why the review is never self-audit.
- **Do the documents persist?** Buetow keeps specs; Horthy throws them out because prose and code become two sources of truth. Resolved toward Horthy on prose and toward Buetow on rules: the prose is deleted and the constraints it carried are promoted into things that execute.

`research/example_artifacts.md` is the companion, showing what each artifact looks like and how long it lives.

Neither source covers what happens when a feature is removed, what to do when a feature needs a boundary you drew wrong, or when to retire a rule that has stopped earning its slot. Those gaps are still open.

## Where the hands go

The split between what the user does and what the agent does follows how an airline crew works with an autopilot. The pilot hand-flies the takeoff and the landing and sets the autopilot's targets for the cruise; the autopilot never chooses the altitude. In the loop, the user confirms the outcome, the story list, the architecture tables and the first decisions up front, confirms each story's criteria before its tests are written, answers the builder's questions about what a person will see, and merges each pull request. Between those points the agent runs the failing tests, the build subagent, the review subagent, the full suite and the pull request. The loop asks each question when it arises and keeps working on other stories while it waits.

Three findings from that field shaped specific rules:

- **Bainbridge, "Ironies of Automation" (1983).** Automation takes the routine part of a task and leaves the human the hard part, with less practice at it. FAA SAFO 13002 (2013) asks airlines to schedule manual flying so the skill stays current. The practice is the user writing code, a design or a fix idea by hand and running `reviewing` on it; the `deliver` loop never forces it, since a forced exercise in the middle of a delivery is an interruption, and the loop is for delivering.
- **Asiana 214 (NTSB, 2013).** The crew flew an approach assuming the autothrottle held speed while it sat in a mode that did not. This is why the proposal lists what it assumes before the build, for the pull request's reviewer to check.
- **The stabilized-approach gate.** An approach that fails fixed criteria at a fixed height is abandoned without debate. This is why a builder that reports red, or touches a path outside its story, is reset to the red commit and reissued once, and the story is split after the second failure.

---

# How it runs

Say what you want in ordinary language.

- **Anything that changes a system**: "add X", "fix this bug", "remove the Y feature".
- **Half-formed**: "I'm thinking about Y", "what's the best way to Z", "should we move to A".
- **When nobody knows yet**: "just build me a quick version", "I want to try something".
- **Mid-flight**: "write the tests for this", "build the next story", "review my diff".
- **After it ships**: "we shipped X, is it working".
- **On a repo with no checks**: "set up guardrails", "we have no linting".
- **At a session boundary**: "write a handoff", "I'm running low on context".

Judgment calls go to you. The skills surface the decision, the failure mode or the coverage gap concretely, and you disposition it. The model does not decide for you, and where you ask it to choose it says what it would pick and marks that as its read rather than the answer.

**Every sentence has to earn its place by one test: does it change what you do next?** That cuts the preamble announcing what is about to happen, the derivation behind a result you can take on trust, the reasons you supplied in the first place, and the second argument for a point the first already carried. The answer leads, the question closes. Several findings arrive as one line each, for you to pick which to open, rather than being worked through in order. A document or a diff that was just written is named and located rather than reproduced. The pictures are the exception to the volume rule: those go up, not down.

**Subagents get the cheapest model that can do the job, named when they are launched.** Bulk mechanical work goes to a small one. The failing tests, the design review and the implementation review do not.

# Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install SDLC@davebben-skills
```

The nine skills surface under their own names.

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add DaveBben/davebben-skills --skill deliver
```

Swap in `guardrails` or `architecture`, or `--all` for every skill in the repo. The canonical `SKILL.md` files live at `skills/SDLC/` in the repo root.

MIT.
