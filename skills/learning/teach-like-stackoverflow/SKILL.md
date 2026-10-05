---
name: teach-like-stackoverflow
description: "Use this skill for every programming or computer-science question of the kind asked on Stack Overflow, even one you could answer in a sentence: load it before answering, not after. That covers how to do something in a language, library or tool ('how do I read a CSV with pandas', 'how do I undo a git commit'), what an error means or why it happens ('why am I getting TypeError', 'what is a segfault'), how a concept, algorithm, data structure or protocol works ('what does yield do', 'how does TCP work', 'what is CORS'), and how two things differ ('let vs var', 'mutex vs semaphore'). Use it whenever the user says they don't understand, don't get, or want explained a technical concept. Teaches it as a mock Stack Overflow thread on one HTML page. Skip it only when the user asks to change code in their own project. Skip it when the user asks for a short or inline answer."
license: MIT
compatibility: Needs code execution and a writable temp directory; falls back to Markdown in chat without them.
metadata:
  version: "0.1.0"
---
# Teach like Stack Overflow

Answer the user's question by writing a mock Stack Overflow thread about it on one HTML page. A fictional asker gets stuck on the topic, and an accepted answer fixes their attempt. Short comment exchanges answer the next questions a reader would have. Further answers solve the same problem with different techniques.

## The thread

[`assets/thread.html`](assets/thread.html) holds the page layout and styles, with one example of every element. Copy it and replace the bracketed content.

* **Title:** Write the question as a searcher would type it, naming the language or library.
* **Question:** Write a fictional asker one step behind the user. They state what they have and what they want in two or three sentences. They show a minimal attempt of under 10 lines and paste the exact error or wrong output it produced. When the user pasted their own code or error, use it as the attempt. When the topic has no error, as with "explain hash maps", show the wrong result or the wrong belief the asker holds. They end with the one or two questions a beginner asks next. Tags name the language, the libraries and the concept.
* **Accepted answer:** Open with one sentence naming what went wrong in the attempt. Follow with working code of 10 to 15 lines, with no comments except on a line whose result is not obvious, such as an array's shape. Then trace one input through the core step with real values in a code block. End with two or three mistakes that will bite the asker, each with the exact warning, error or wrong output it produces, copied from a run. Keep the prose outside code blocks under 120 words.
* **Comments on the accepted answer:** Write three exchanges. Each is a follow-up question and a reply of two or three sentences from the answerer. The asker asks the first; a different user asks each later one, weeks or months apart. Cover what happens to a new input, why the approach works, and what changes in the most common variant (more classes, a larger input, async instead of sync).
* **Further answers:** Write one to three, each a different technique, each opening with when to prefer it. Reuse the accepted answer's problem, data and variable names, so the reader compares the two side by side, and say what the accepted answer's call does that this one does differently. Choose from these kinds:
  * **Beneath the call:** The library call written out one layer lower, such as the loss and update steps a `fit` call performs, written in numpy, so the reader sees what the call does.
  * **Alternative:** Another library, algorithm or language feature, with the trade-off stated in numbers where one can be measured.
  * **Popular but flawed:** A common approach with a flaw, and one comment naming the flaw and the input that exposes it.

Give each further answer a lower score than the accepted answer and at most one comment. Invent every username, score and date.

## Accuracy

The page teaches, so a wrong line is learned as a fact.

* **Run the asker's attempt and every answer's code** on a small made-up input before it goes on the page. Run a Beneath-the-call answer on the accepted answer's input and compare the outputs. State any difference and its cause, such as the L2 penalty `LogisticRegression` applies by default. Copy error messages and warnings from the run, word for word. When a block cannot run here, because a package is missing or no tool executes code, tell the user which blocks were not run.
* **Take every default and version-specific behaviour the page states** from the library's documentation or installed source, not from memory.
* **Escape `&`, `<` and `>`** as `&amp;`, `&lt;` and `&gt;` everywhere in the page's text, including code blocks, inline code and comments, so the page renders them.
* **Keep lines of code you write under 60 characters,** breaking long calls across lines, so blocks fit a phone screen. Leave copied errors and output unwrapped.
* **Explain a mechanism literally,** as code or a traced example, with no analogies or charts.

## Delivering it

* **Write the page** to a scratch directory outside the user's repository, named for the topic, such as `/tmp/so-logistic-regression/index.html`.
* **Serve it when the user reads on another device,** over the local network with any static file server, such as `python3 -m http.server 8000 --bind 0.0.0.0`. Check the URL loads, then give the machine's LAN address, such as `ipconfig getifaddr en0` on macOS, because localhost does not resolve on the phone.
* **Reply in chat** with the path or URL and one sentence naming the technique each further answer uses. Do not repeat the thread in chat.
* **Answer a follow-up on the page.** Add it as a new comment exchange or a new answer, and tell the user to reload.
* **Fall back to Markdown** when the environment cannot write or serve a file: write the same thread in chat.

Run every code block before it goes on the page.
