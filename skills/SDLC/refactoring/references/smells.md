# Smell catalogue

Each entry gives the smell, how to see it in code, and the named refactorings that cure it. Confirm a smell costs something (a change it makes harder, a reader it misleads) before curing it. Size thresholds are rough; Python code runs longer methods and shorter parameter lists than Java.

## Bloaters

* **Long Function:** it needs comments to mark its sections, nests more than two levels, or mixes levels of abstraction (SQL beside business rules). Cure: Extract Function, Decompose Conditional, Replace Temp with Query, Split Loop, Replace Function with Command.
* **Deeply Nested Code** (Arrowhead): `with`/`try`/`for`/`if` blocks stack past three levels. Cure: Replace Nested Conditional with Guard Clauses (return or `continue` early so the main path stays at the left margin); Extract Function for a deep block; or let the language flatten it (a comprehension, stacked context managers `with (A, B):`).
* **Large Class:** many fields, or groups of fields sharing a prefix (`mark_read_client`, `mark_read_enabled`). Cure: Extract Class.
* **Long Parameter List:** four or more parameters, or the same ones passed through several layers. Cure: Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query, Remove Flag Argument.
* **Data Clumps:** the same three or more values travel together through several signatures. Cure: Introduce Parameter Object, Extract Class.
* **Primitive Obsession:** money, dates, IDs or ranges held as bare strings and numbers, validated in several places. Cure: Replace Primitive with Object.

## Change preventers

* **Divergent Change:** one module edited for unrelated reasons; `git log` on it shows database fixes and formatting fixes alike. Cure: Split Phase, Extract Class, Move Function.
* **Shotgun Surgery:** one conceptual change needs the same small edit in many files. Cure: Move Function, Move Field, Combine Functions into Class.
* **Scattered Cleanup:** a resource opened in one function and closed in several others, or closed by code that did not open it. Cure: one owner per resource, with a context manager, `try`/`finally` or an exit stack where it is created.
* **Repeated Switches:** the same `if`/`elif` or `match` on one discriminator in two or more places. Cure: Replace Conditional with Polymorphism, or one lookup table.

## Dispensables

* **Duplicated Code:** blocks with the same structure apart from names or literals. Cure: Extract Function, Slide Statements, Pull Up Method; only when the copies change for one reason.
* **Dead Code:** a function, branch, parameter or flag with no caller. Search for callers, reflection, string references, config and public exports before deleting. Cure: Remove Dead Code.
* **Speculative Generality:** an abstract class with one subclass, an unused parameter or hook, a function whose only caller is a test. Cure: Collapse Hierarchy, Inline Function, Inline Class, Change Function Declaration.
* **Lazy Element:** a function or class that holds one trivial line or only forwards a call. Cure: Inline Function, Inline Class.
* **Data Class:** a record with no behaviour while its callers hold the logic about it. Cure: Move Function into it, Encapsulate Record.
* **Comments as deodorant:** a comment that explains what a block does. Cure: Extract Function named for the comment, Rename, Introduce Assertion. A comment that explains why stays.

## Couplers

* **Feature Envy:** a function reads another object's fields more than its own. Cure: Move Function.
* **Insider Trading:** two modules read each other's private fields or internals. Cure: Move Function, Move Field, Hide Delegate.
* **Message Chains:** `a.b().c().d()`, three or more hops through other objects. Cure: Hide Delegate, Extract Function.
* **Middle Man:** a function or class whose work is mostly delegating, such as a wrapper that forwards nine arguments to a constructor and calls one method. Cure: Remove Middle Man, Inline Function.

## Object misuse

* **Temporary Field:** an attribute that is `None` except on some code paths. Cure: Extract Class, Introduce Special Case.
* **Refused Bequest:** a subclass overrides inherited methods to raise or do nothing. Cure: Push Down Method, Replace Subclass with Delegate.
* **Alternative Classes with Different Interfaces:** two classes do the same job under different method names. Cure: Change Function Declaration, Extract Superclass.

## State and side effects

* **Global Data:** module-level mutable state, or a singleton written from several places. Cure: Encapsulate Variable, then pass the value in.
* **Mutable Data:** a variable reassigned for a second purpose, or state changed far from where it was made. Cure: Split Variable, Replace Derived Variable with Query, Change Reference to Value.
* **Hidden Side Effect:** a function whose name promises a query or a build but which also writes, closes or mutates something else. Cure: Separate Query from Modifier, Move the side effect to the caller that owns it.
* **Flag Argument:** a boolean parameter that selects between two behaviours (`book(x, False)`). Cure: Remove Flag Argument into two named functions. A boolean that comes straight from data or a user setting is fine.
* **Mysterious Name:** a single letter, an abbreviation, or `data`, `tmp`, `handle`, `process`, `manager`. Cure: Rename Variable, Rename Field, Change Function Declaration.

## Test smells

* **Eager Test:** one test exercises several behaviours. Cure: one behaviour per test.
* **Assertion Roulette:** several assertions with nothing saying which failed. Cure: one behaviour per test, or a message on each assertion.
* **Mystery Guest:** a test depends on a file, row or service it does not set up. Cure: create the data inside the test.
* **General Fixture:** a shared setup builds more than each test uses. Cure: build only what each test needs.
* **Sensitive Equality:** a test compares string output, such as `str(obj)`, to check state. Cure: assert the fields.
