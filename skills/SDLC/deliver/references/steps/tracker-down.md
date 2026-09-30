# Step: the tracker cannot be reached

An auth error, a 401 or 403, or a tool that is not connected.

* Say once which method failed and its error text, and name the login step. Have the `lookup` agent try the next method in `references/tracker.md` before asking. Then ask whether to wait or go on.
* **Going on:** for reads, ask the user to paste the epic and its children with keys, rank and blockers. For writes, append each owed write to an outbox, the file `sdlc-outbox.md` in the shared git directory (`git rev-parse --git-common-dir`), which is never committed. One line per write, with the text it will post: `- comment PAY-12: <the log entry>`, `- status PAY-12: Done`, `- create story under PAY-1: "<title>", ranked after PAY-9`.
* Show the outbox at every story end. When a method works again, ask once, then have a `worker` replay it top down, deleting each line as it lands, and delete the file once it is empty.
