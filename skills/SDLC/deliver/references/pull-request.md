# Pull request description

Load this when a story's pull request opens, or when the user asks for a description of a branch built outside the loop.

Write for a reviewer who has never opened this repository and does not know the feature. Under one screen, in this order.

0. **Read code:** the first line, for the user who reads code only when a
   signal fires. The signals are the lines of `exceptions.txt`, which verify
   writes from the repository's `CODEOWNERS` `# owner reads:` sections and
   the diff, and the Done block's `Exceptions:` line. It says `none`,
   `<n> slices`, or `whole diff of <paths>` when the slices would pass three,
   or 120 lines in all. Until the last ten log entries carry no
   `Not caught by: exception list` line, add "shadow period: read the whole
   diff", since the list is still being tested. Omit the line for a branch
   built outside the loop.

1. **Why,** two or three sentences: what the product is and who uses it; the
   outcome this change serves; where this change sits in it ("two of five
   stories shipped: the upload and the thumbnail").

2. **Criteria,** one table, one row per acceptance criterion: a green check
   mark, the criterion in a few words, and the exact name of the test that
   proves it. This table is the reason the description exists, and it never gets
   summarised.
   - Verify every row. Run the test and read its name out of the passing
     output. Never mark green what you have not seen pass; write what is wrong
     in the row instead of a check mark.
   - A criterion that moved to another change is listed once as out of scope,
     never green.
   - A green mark you cannot reproduce right now says so in the row, with the
     date it passed and what is missing.
   - A branch built outside the loop with no criteria anywhere gets the
     heading "No acceptance criteria found", then one row per test the
     branch adds.
   - Criteria live in the ticket. Do not restate them verbatim here; the table
     names them and the ticket is the text of record. When the stories live in
     `docs/delivery/` and there is no ticket, each row carries the criterion in
     full.

3. **Try it:** the exact command, URL or screen that shows the outcome
   criterion working on this branch, and directly beneath it the result it
   produced — the values, as a table.
   - List every prerequisite whose absence produces a *passing-looking*
     failure: an unset variable, a fixture the command cannot create, a state
     the system must be in. These are the ones that cost hours, because the
     run completes and reports the wrong reason.

4. **What changed,** one paragraph in the domain's nouns, then one line per new
   function, module or branch saying what it is for and which file it is in.

5. **Risk,** one line per fact that changes what a reviewer or merger does:
   what merging itself deploys and where; a guard that is off in the
   environment this ships to; anything a revert cannot undo; a diff touching
   authentication, authorization, secrets, money, health or personal data.
   Name the file. Omit the section only when every line would be empty.
   Each signal is one slice of at most 40 lines of the hunk it names, in
   four lines:
   `Read: <file>:<first>-<last> (<n> lines) — <the signal>`, linked to those
   lines of the diff on the code host, or followed by the code without a remote;
   `Decides:` what that code decides, in the system's terms;
   `Covered by:` the test, and whether its mutation was killed;
   `Question:` the one yes-or-no the user answers after reading.

6. **Assumes,** one line per fact the change rests on that was read from a
   document rather than from the code, and how it was checked. Omit when empty.

7. **Read first:** the first slice, or, when there is none, the one file a
   reviewer opens to understand the change.

8. **The rest,** collapsed where the host supports it: the edge-case rows
   and other tests beyond the criteria table, the rules the `guardrails` skill
   wrote on the branch, what is deliberately deferred and to which change, and
   from the review's Done block only its Correctness, Subtraction, Scars,
   Decided alone and Gate lines, or the feedback points, and the verify's
   `Scenarios:` and the attack's `Attack:` lines, when the change came
   from `deliver`.

9. **Signal:** the event someone reads to know it worked once deployed, and the
   counter-signal that would show it silently not working, with the `Success`
   line's good direction and noise band.
