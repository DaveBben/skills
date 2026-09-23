---
name: merge-request
description: "Use this skill to write the description for a pull request or merge request, and to review one. Use it on: 'open a pull request', 'write the PR description', 'write the MR body', 'review this PR', 'review this merge request', 'review PR 412', 'is this ready to merge', 'approve or request changes', 'what should I look at in this diff'. The writing half produces a body a reviewer who has never opened the repository can read in one screen: why, the criterion, what changed, what it touches, what to read first. The reviewing half is run by an agent holding the diff, the body, the reports from whatever ran in the build and the code at the merge target, and it reads what the change lands on, then for the five things automation cannot report: a criterion with no test, code no test asked for, a decision the author made that someone else owned, behaviour that differs against production data and traffic, and names that do not match the words in the criterion. Every finding starts as a false positive and is overturned only by reading the code on the path it names. Do not use it to review a diff with the repository open and the test table in hand, which is `review`, and do not use it to define the work, which is `feature`."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Merge Request

Two jobs: write the description that goes with a change, and review a change someone else submitted.

## Write the Description

Write for a reviewer who has never opened this repository and does not know the feature. From the body alone they can say what the product does, what this change adds, and what to look at. Under one screen, in this order.

1. **Why,** two or three sentences: what the product is and who uses it; the outcome this change serves; where this change sits in it ("story 3 of 5; stories 1 and 2 shipped the upload and the thumbnail").
2. **Criterion,** the acceptance criterion this change makes true, verbatim: one Given/When/Then in real values.
3. **What changed,** one paragraph in the domain's nouns, then one line per new function, module or branch saying what it is for and which file it is in.
4. **What it touches,** one line when the diff touches authentication, authorization, secrets, money, health or personal data, a migration, a public contract, or anything a revert cannot undo: what it touches and the file. Omit otherwise.
5. **Assumes,** one line per fact the change rests on that was read from a document rather than from the code, and how it was checked. Omit when empty.
6. **Read first:** the one file a reviewer opens to understand the change, and the test that proves the criterion.
7. **The tests,** listed, and what is deliberately deferred and to which change. Collapse this where the host supports it.
8. **Signal:** the screen, the endpoint or the event someone reads to know it worked once deployed.

Resolve every pointer: no abbreviation, config key or test ID local to this project without a phrase saying what it is. Write what happens before any name for it. Never write a cause the change does not show. Length is capped by the screen rather than by leaving a section out; a body that needs more is a change that is too big.

## Review a Merge Request

The reviewer holds the diff, the body, the reports from whatever ran in the build, and the code at the merge target. It does not hold the conversation that produced the change, or the author.

### Read what it lands on, not only what it adds

A diff shows what is added. A collision lives in what the change merges into, and the diff never shows that. Read the target for every name the change claims: a storage key, a route, a database column, an environment variable, a feature flag, an event name, a file path. Each side can be correct alone while the two together lose data or shadow each other.

```bash
git diff --name-only <target>...HEAD      # what changed
git show <target>:<path>                  # what it lands on top of
git grep -n '<the new name>' <target>     # who already claims it
```

This is the cheapest check that finds what nothing else does. Run it first.

### Read what already ran first

Never redo by hand what a tool reports, and never trust a tool that did not run.

* **Mutation report over the changed lines.** A surviving mutant on a test the body lists is a finding. A mutant that cannot change behaviour is not, such as `>=` for `>` on a value that is never equal.
* **Static analysis.** It reports patterns: SQL built by joining strings, a key written into the source, output rendered without encoding.
* **Formatter and linter.** They report layout, naming conventions and complexity. Never raise by hand what they own.

Where one of these did not run, do its job on the diff yourself and say which one you stood in for.

### Then read for the five things no tool reports

* **A criterion with no test.** Check the body's criterion, and each test it lists, against the tests in the diff. A missing test passes the build, because the build runs the tests that exist, and a mutation runner mutates the code that exists. Read each test for an assertion that holds whatever the code does: one that checks a fake's return value, one that asserts the order of internal calls, one that replaces the very piece it claims to test.
* **Code no test asked for.** An extra config option, a helper for a case that does not arise, a parameter only ever passed its default, a new dependency. None of it is verified, and every later change works around it. Say what to delete.
* **A decision the author did not own.** Any value or behaviour a person using the system would notice that the criterion does not state: a timeout, a disabled button, what a repeated action returns, the wording of an error. Name each one and send it to whoever owns the criteria.
* **Behaviour against production data and traffic.** The build ran on one machine against an empty database.
  * A migration that passes on an empty table and fails on the rows already there, such as a unique constraint over existing duplicates.
  * Two identical requests arriving at once, each reading, finding nothing, and writing. Name what stops the second, usually a constraint in the database.
  * A standard met by leaving something out, which no pattern rule can see: no rate limit, no size limit on a request body, no unique constraint.
  * A failure nobody can see: no log at the point it fails, or a log carrying personal data.
* **Names that do not match the criterion.** The criterion's words are the domain's words. Code that says `status == 2` where the criterion says confirmed and unconfirmed costs every later reader, whether that reader is a person or an agent. Raise the names and the branches a reader cannot map to a criterion. Raise nothing else about style.

### Know who wrote the data

Two reads that look identical carry different risk, and nothing in the source says which is which. `Users.objects.filter(id=x)` over rows a colleague typed into an admin screen is not the same call as `Records.objects.filter(key=x)` over rows a partner system pushed overnight. Take the answer from the repository's root instructions file, usually `AGENTS.md` or `CLAUDE.md`, which lists each system this product reads from and who writes the data in it. Sort each store the change touches into one of three:

* **Written outside,** and you can point at the code that writes it. Every field is untrusted: missing, oversized, hostile, and the wrong type. Most validation guards null and missing and forgets type, so ask what happens when a number arrives as a string.
* **Written by a person through your own screens.** Unsanitised text that no outsider can reach.
* **Not established,** because no such file exists, it does not list this store, or the writer is outside this repository. Say so, and name what would settle it: the file to read, or the person to ask. That beats a confident guess either way.

### Refute before reporting

Every finding starts as a false positive and is overturned only by reading the code on the path it names, rather than the account of it in the finding. Expect most severity claims to come down. Nine false alarms at the top of a report cost the reviewer's trust permanently.

Say what each finding rests on: read this run, inferred from something read this run, or asserted by a tool, a comment or the body. A comment raises a concern and never lowers one, and two documents by the same author are one source. A claim that would change a rating and cannot be checked ships as a question plus the one test that would settle it.

### Report

One finding per line: the file, the line, what breaks, what would show it breaking, and what it rests on. Blocking findings first, then the rest. A finding with no failure behind it is a preference; leave it out. List what was raised and refuted, with the reason, so nobody files it again. End with one line: merge, or changes requested and the count of blocking findings.

Never rewrite the code. The author changes it, and the next review reads the new diff. Every confirmed finding a pattern could match goes to the `semgrep-rules` skill, so nothing is found by hand twice.
