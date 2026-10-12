# Refactoring, code smells and readability: research brief

Source material for the SDLC `refactoring` skill, gathered on 2026-10-11 by four Sonnet research agents and condensed here.
Nothing in this folder loads into an agent.
Labels: **[V]** the agent read the source text, **[S]** a search snippet or secondary summary only, **[U]** unverified or from memory.

## What the skill takes from it

* Refactor code a change touches, code that was hard to understand, and hotspots, because the measured payoff of removing smells is in change-proneness, not faults.
* Name each smell and refactoring explicitly, because LLM detection is weak with a vague prompt and strong with a named one.
* Keep structure and behaviour in separate commits, verify beyond the tests, and read the diff for deletions, because LLM refactorings silently change behaviour in a measurable share of attempts.
* Treat readability metrics as hints, because none predicts understandability reliably.
* Split functions only where the pieces have simple interfaces, because the small-functions rule is contested.

## Smells and their cost

* **Catalogue:** Fowler and Beck, *Refactoring* 2nd edition, 24 smells. Cure lists come from a third-party summary, not the book. [S] <https://gist.github.com/paseaf/dd53cca0cbd9870edfe87738eaba1eac>, <https://martinfowler.com/bliki/CodeSmell.html> [V]
* **Taxonomy:** bloaters, object-orientation abusers, change preventers, dispensables, couplers (Mäntylä et al. 2003; grouping seen only through refactoring.guru). [S] <https://refactoring.guru/refactoring/smells>
* **Palomba et al. 2018,** EMSE 23, 395 releases of 30 projects, 17,350 validated instances of 13 smells. [V] <https://www.iris.unisa.it/bitstream/11386/4708436/2/J9.pdf>
  * Smelly classes: median 32 changes against 12 (Cliff's d 0.68), median 9 bug fixes against 3.
  * With size controlled, smell presence has odds ratio 4.46 for change-proneness; for faults only the smell-by-size interaction is significant (2.11).
  * Removing smells lowers change-proneness (Complex Class median 55 to 34) but not reliably fault-proneness.
* **Khomh et al. 2012,** 54 releases of 4 systems: antipattern classes more change- and fault-prone. [S, abstract only]
* **Weaker effects:** SonarQube smells on 33 Apache projects, small change difference and no fault difference. [S] <https://arxiv.org/abs/1908.11590>
* **Flag arguments:** Fowler, acceptable when the boolean comes straight from data or a UI control. [V] <https://martinfowler.com/bliki/FlagArgument.html>
* **Python calibration:** Python has over 2x the long methods of Java and 7x fewer long parameter lists. [S] <https://programming-journal.org/2017/1/11/>
* **Test smells:** smelly tests more change- and defect-prone (Spadini et al., ICSME 2018). [S]
* **Unsourced additions** the skill keeps as judgement: scattered cleanup, hidden side effects, ordering-constraint comments.

## How to refactor

* **Definition and workflows:** Fowler, two hats, TDD, litter-pickup, comprehension, preparatory, planned (a smell when frequent), long-term. [V] <https://martinfowler.com/bliki/DefinitionOfRefactoring.html>, <https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html>
* **Tidy First?** (Beck 2023): 15 tidyings, structure and behaviour in separate commits, tidy first, after, later or never. [S] <https://henrikwarne.com/2024/01/10/tidy-first/>
* **Legacy code** (Feathers): characterization tests, seams, sprout and wrap. [S] <https://understandlegacycode.com/blog/key-points-of-working-effectively-with-legacy-code/>
* **Large refactorings:** parallel change, branch by abstraction, strangler fig [V, martinfowler.com bliki], Mikado method [S].
* **Google large-scale changes:** over about 500 edits goes to tooling; Rosie shards changes by owner. [V] <https://abseil.io/resources/swe-book/html/ch22.html>
* **Wrong abstraction:** Metz, "duplication is far cheaper than the wrong abstraction"; inline it back, then re-extract. [V] <https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction>
* **Refactoring-induced bugs:** Bavota et al. 2012, 15,008 refactorings in 3 systems, about 15% fix-inducing, hierarchy refactorings riskiest. [S] <https://people.lu.usi.ch/bavotg/papers/scam2012.pdf>
* **Floss refactoring:** most refactoring is mixed into other work (Murphy-Hill et al.). [S] <https://arxiv.org/pdf/1412.6359>

## LLMs and agents refactoring

* **Detection depends on the prompt:** GPT-4 found 15.6% of 180 real refactoring opportunities with a generic prompt and 86.7% with the subcategory named and the search narrowed. 7.4% of its solutions were unsafe, 18 of 22 changing semantics; re-applying them through a refactoring engine caught all 22. [V] <https://arxiv.org/html/2411.04444>
* **Equivalence:** differential fuzzing found 19 to 35% of LLM refactorings not equivalent, about 21% of those missed by the tests. [U] <https://awesomepapers.io/ai-for-code/papers/2602.15761>
* **Semantic drift:** 39.7% of attempts across 11 models on legacy Python traps. [S] <https://www.alphaxiv.org/abs/2605.21537.md>
* **Agents in the wild:** 1,278 agent pull requests; Claude Code averaged 762.7 refactorings per refactoring commit against a developer mean of 15.3, over 91% annotation changes. [V] <https://arxiv.org/html/2601.20160v1>
* **Smells unchanged:** agent refactorings across 12,256 pull requests cut median class size but left design and implementation smell counts flat. [V] <https://arxiv.org/html/2511.04824v1>
* **Benchmarks:** RefactorBench, agents solved about 22% of multi-file tasks against 87% for a time-limited human [S] <https://arxiv.org/html/2503.07832v1>; compound refactorings 39.4% for a Codex agent [S] <https://arxiv.org/html/2602.03712v1>.
* **Tangling:** refactoring tangled into bug-fix patches lowers compilability; removing the unsafe parts raised it from 19.34% to 38.33%. [S] <https://www.alphaxiv.org/abs/2605.22526v1>
* **AI-era duplication:** GitClear, copy-pasted lines rose from 8.3% to 12.3% of changes (2021 to 2024) while moved lines fell from 25% to under 10%. [V] <https://www.gitclear.com/ai_assistant_code_quality_2025_research>

## Readability

* **Names:** full words found defects about 19% faster than letters or abbreviations (Hofmeister et al., 72 developers). [S] <https://neverworkintheory.org/2021/08/09/abbreviated-vs-full-names.html>
* **Case style:** camelCase against snake_case barely matters to experienced developers (Binkley et al.). [S]
* **Atoms of confusion** (Gopstein et al. 2017, 73 participants): octal literals, assignment as value, `&&` as control flow, increments as values, implicit conversion, omitted braces, repurposed variables and implicit predicates each lowered correct answers. [V] <https://ssl.engineering.nyu.edu/papers/gopstein_atoms_fse_2017.pdf>
* **Metrics:** 121 metrics failed to capture understandability (Scalabrino et al. 2017) [S]; cognitive complexity correlates with comprehension time (r 0.54) but not correctness (Muñoz Barón et al. 2020) [V] <https://arxiv.org/pdf/2007.12520>.
* **Function length is contested:** Ousterhout against Martin, 2024 to 2025; over-decomposition gives shallow methods a reader must jump between. [V] <https://github.com/johnousterhout/aposd-vs-clean-code>
* **Deep modules, pass-through methods, comments for the non-obvious:** Ousterhout, *A Philosophy of Software Design*. [U, book not fetched]

## Hotspots and technical debt

* **Hotspots:** change frequency times complexity; 2 to 4% of code drew 20 to 70% of development activity, and in one case 4% of code held 72% of defects (vendor figures). [V] <https://usenix.org/system/files/srecon24emea_slides-tornhill.pdf>
* **Code Red:** low-health code had 15x more defects across 39 proprietary codebases (correlational, vendor metric). [V] <https://arxiv.org/abs/2203.04374>
* **Debt quadrant:** Fowler, prudent or reckless, deliberate or inadvertent; debt in rarely touched code may never need repaying. [V] <https://martinfowler.com/bliki/TechnicalDebtQuadrant.html>
