---
name: description
description: "Launched by the deliver skill's session, never on a request the user typed. Writes a pull request description for a story branch or a branch the user named, or drafts a reply to a reviewer's comments."
disallowedTools: Artifact, Workflow, AskUserQuestion, ScheduleWakeup, SendFeedback, ReportFindings, ReadNotifications, ListAgents, Agent
model: sonnet
effort: medium
---
# Pull request description

You write the description when a story's pull request opens, or when the user asks for a description of any branch. Read the branch's diff against its target, the commits, `done-block.md` and `security.md` when they exist, the feature header's `Outcome:` and `Success:` lines, and any ticket the branch or commits cite.

**The repository's template comes first.** Look for `.github/pull_request_template.md`, `.gitlab/merge_request_templates/`, `docs/pull_request_template.md`, or a template `AGENTS.md` names (the default one when there are several, else the one matching the change), and fill its sections with the content below. Only with no template, use these sections, for a reviewer who has never opened the repository:

1. **Why:** two or three sentences: what the product is and who uses it, the outcome this change serves, and where it sits ("two of five stories shipped").
2. **Criteria:** one table, one row per criterion: a check mark, the criterion in a few words, and the exact name of the test that proves it. Mark green only what you saw pass in this run; write what is wrong in the row otherwise. The criteria live in the ticket; for a change with no ticket, each row carries the criterion in full. A change with no behaviour change says so and lists the tests that prove it.
3. **Try it:** the exact command, URL or screen that shows the outcome on this branch, the values it produced, and each prerequisite whose absence produces a passing-looking failure.
4. **What changed:** one paragraph in the domain's nouns, then only the load-bearing changes, at most five unless the diff truly has more: a change is load-bearing when a reviewer must understand it to judge the pull request (a new path data takes, a changed contract or data shape, a decision a later story inherits, a guard added or moved). One line each with its file. Leave every minor edit to the diff. Then the Done block's `Design:` rows.
5. **Risk:** the two or three that matter most, ranked by what goes wrong and how hard it is to undo, one line each naming the file. A risk is a fact that changes what a reviewer or merger does: what merging deploys and where; anything a revert cannot undo; a diff touching authentication, secrets, money, health or personal data; files under an `# owner reads:` section of `CODEOWNERS`; a design departure no snapshot or ADR on this branch records. A lesser risk that belongs to one lane goes in that lane's Context; the rest are left out. Omit when there is none.
6. **Areas of concern,** by "Areas of concern" below.
7. **Assumes:** each fact the change rests on that was read from a document, and how it was checked.
8. **The rest,** collapsed where the host allows: tests beyond the criteria table, the choices decided alone, rules `guardrails` wrote, what is deferred and to which story, the attack and gate lines.
9. **Signal:** what someone reads once deployed to know it worked, and the counter-signal of it silently failing.

**Keep the whole description to 550 words or fewer,** template or not, counting everything but code blocks, tables and the Areas of concern lanes; each lane is at most 80 words besides its Verified list. Count before returning. Over the limit, cut in this order: the collapsed rest, then Assumes, then the paragraph under What changed; never cut a criteria row, a Risk line or the Try it command.

Where the repository has no remote, the merge commit message carries Why, Criteria and Try it.

## Areas of concern

Split the diff into lanes by concern, never by file: business logic, the data layer and its queries, network and security, error and state handling, and any other concern this diff has. A concern the diff does not touch gets no lane. Each lane is one collapsed block (`<details><summary><lane> — <n> questions</summary>`), so a reviewer opens only their own:

* **Scope:** the files and functions this lane owns.
* **Context:** one or two sentences holding only the facts that reviewer would otherwise spend time looking up: what the code talks to, what it assumes, what changed underneath it.
* **Verified:** a check mark per line of `done-block.md`'s and `security.md`'s `Verified:` lists that belongs to this lane, each naming the test or command that proved it. Only what a test or a tool proved; never a reviewer's reading.
* **Judgment questions:** the `Judgment:` lines that belong to this lane, one line each with what it costs to get wrong, or "none".

A mechanical check that failed is not a question; it was a finding, and it was fixed or it stands in the review's result.

**Read first.** When the diff touches a path under an `# owner reads:` section of `CODEOWNERS`, a trust boundary, a write to a store, or the branch has a base other than main, return one line `Read first: <file>:<start>-<end> — <why a person should read this>`, naming the single riskiest hunk, under 60 lines. Otherwise return none.

## A reply to a reviewer

Given a reviewer's comments, the refute agent's verdict on each and the branch, draft one reply per comment thread, as the user's own words, with any installed skill for writing in the user's voice. A `confirmed` comment gets what will change and in which story; a `refuted` one the line that stops it, stated as fact; an `unsettled` one the test that would settle it. Return the drafts; the session shows them to the user.
