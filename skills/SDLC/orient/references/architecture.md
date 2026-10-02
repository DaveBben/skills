# Architecture snapshot

`ARCHITECTURE.md` at the repository root is a one-page overview that a reader with no knowledge of the codebase finishes in about five minutes. It runs from the top down: what the system is for, what surrounds it, what it is made of, how one request moves through it, where things live, and why it is built this way.

Long templates such as arc42 lose this reader. People who explain architectures to newcomers start from the business purpose and context, then show structure and one flow, and answer "why" before they show code. Cut anything the reader does not need to place their first change.

## Refreshing an existing snapshot

The file's first line is `<!-- orient snapshot: <commit sha> <YYYY-MM-DD> -->`, recording the commit it was traced at. The line under the title says the same to the reader: "Snapshot of commit `<sha>`, traced <date>. The code may have changed since; check `git log <sha>..HEAD` before relying on a detail."

* **With the marker:** run `git diff --stat <sha>..HEAD`. Retrace only the entry points, outbound calls and modules whose files changed, then rewrite the file at HEAD. With no change, report that the snapshot is current.
* **Without the marker:** a person wrote the file. Show the user what the snapshot would change and wait for a yes before overwriting it.

## Tracing

Every box, arrow and step on the page comes from a file and line you read, or a search you ran. Record that evidence as you go.

* **Inbound, inside the repository:** find every entry point. These include HTTP routes, RPC or gRPC service definitions, queue and topic consumers, webhooks, scheduled jobs, CLI commands, and a library's exported API in its package manifest.
* **Inbound, outside the repository:** search for who calls those entry points.
  * Search the organization's other repositories for the service's hostname, route paths, topic names and package name, such as `gh search code "<route or host>" --owner <org>`.
  * Read infrastructure configuration: ingress rules, API gateway routes, DNS records, IAM or network policies that grant invoke access, and published OpenAPI or proto files.
  * Check the package registry or GitHub dependency graph for dependents of a published library.
  * When an entry point has no caller that any search found, list it as "caller not found". Name what would establish one, such as gateway access logs or tracing data.
* **Outbound:** find everything the code calls. These include database and cache clients, HTTP clients and their base URLs, cloud SDK clients, topics it publishes to, and environment variables that hold hosts or credentials.
* **Large repositories:** split the trace by top-level module and run the parts in parallel when the agent can, such as one subagent per module. Have each part report its entry points, its outbound calls and its evidence.

## The page

Write the sections in this order. Keep only what will still be true in six months; drop what changes every sprint.

1. **Purpose:** two sentences. Say what the system does, and for whom, in the business's terms.
2. **Context diagram:** one box for this system. Around it, the people who use it and every outside system from the trace. Label each arrow with what flows and how, such as "order events, Kafka". Use at most 12 boxes, and group minor callers into one box when there are more.
3. **Container diagram:** the separately deployed or run parts inside the system, such as the web app, the API, the worker, the database and the queue. Label every arrow with the protocol and the data. Put the technology in each box.
4. **Data model:** each table, file or queue the system keeps its own state in, or reads as its main input. For each, say who writes it, what one row or record means, and the columns or fields the code uses, with their values, such as "`verdict`: true for the 30 picked, false for every other article ranked". Leave out columns the code never reads.
5. **One request, end to end:** choose the action users perform most, or the one the business depends on. Give it as a sequence diagram and as 5 to 8 numbered steps. Each step names the file and function that handles it. After the steps, say what a repeat run does when there is nothing new, when only a little is new, and when there is less input than the system needs. Read the code for each case rather than assuming it.
6. **Codemap:** a table of the top-level directories or modules, each with one line saying what lives there. Answer "where is the thing that does X?" without describing how each module works. Use at most 15 rows.
7. **Decisions and invariants:** 3 to 7 bullets. Each states a rule or a choice and the reason behind it in one clause. Leave measurements, counts and parameters behind the link to the source. An invariant is often an absence, such as "the API never writes to the database directly; every write goes through the worker".
   * Take reasons from ADRs, commit messages (`git log -S`), pull request descriptions and code comments. Link to the source.
   * Never infer a reason. Where none is recorded, write "reason not recorded" and ask the user.
8. **Running it:** the exact commands to install, start, test and deploy it, and where its logs go, taken from the README, the manifest or the CI configuration. Run them when the environment allows. Report the results in chat, not on the page; they go stale with the next commit.
9. **Open questions:** callers not found, reasons not recorded, and behaviour the trace could not establish. A broken link, a failing check or the extent of a search goes in the chat reply, not on the page.

Link to any longer architecture document the repository already has, such as an arc42 file or an ADR folder, instead of repeating it.

## Writing it

* **Write the diagrams in Mermaid,** which renders on GitHub, GitLab and in the HTML template. Use `flowchart LR` for the context and container diagrams and `sequenceDiagram` for the request. Quote every node label that contains punctuation, such as `api["Orders API (Go)"]`, because unquoted parentheses and colons break Mermaid parsing. When `npx` is available, render each diagram once with `npx -y @mermaid-js/mermaid-cli -i <file>.mmd -o /tmp/check.svg` to confirm it parses.
* **Describe the code literally:** say what each part does to the data and when. Use no analogies.
* **Define every name local to the project at first use** in one clause: a database role, an account, a pipeline ID, a story number, an adjective such as "frozen". Cut a reference that needs more than a sentence to explain, such as a file name's history.
* **Name where each number lives:** for each number the page states that the user might change, such as how many items a run picks, give the constant or setting and its location, such as `TOP = 30` at `run.py:49`.
* **Leave out what drifts:** counts of rows or votes, test results, solver parameters and IP addresses repeated across sections.
* **Use the reader's words:** name a component by what it does, then give its name in the code, such as "the worker that charges cards (`billing-worker`)".
* **Keep prose short:** answer each section in the fewest sentences that hold its facts. The diagrams and the codemap carry most of the page.

## Delivering it

* **Markdown, always:** write `ARCHITECTURE.md` at the repository root, marker line first.
* **HTML, when the user asks** for a page, an HTML file, something pretty, or something to share: copy `assets/architecture.html` from this skill's folder, replace the bracketed content with the same sections, and write it to a scratch directory outside the repository, such as `/tmp/<repo>-architecture/index.html`. Escape `&`, `<` and `>` in text outside the Mermaid blocks. When the user reads on another device, serve the directory on the local network, such as with `python3 -m http.server 8000 --bind 0.0.0.0`, and give the machine's LAN address, such as from `ipconfig getifaddr en0` on macOS.
* **Reply in chat** with the file path or URL, the number of inbound callers and outbound systems found, what changed since the last snapshot, the open questions, the results of the commands run, and any broken link or failing check the trace found. Do not repeat the page in chat.
* **Answer a follow-up on the page:** add the answer to the section it belongs to and tell the user to reload.
