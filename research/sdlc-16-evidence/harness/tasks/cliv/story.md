No way to mark a single-value argument as required

## Checklist

* [x] Are you running the latest v3 release? The list of releases is [here](https://github.com/urfave/cli/releases).
* [x] Did you check the manual for your release? The v3 manual is [here](https://github.com/urfave/cli/blob/main/docs/v3/index.md).
* [x] Did you perform a search about this feature? Here's the [GitHub guide](https://help.github.com/en/github/managing-your-work-on-github/using-search-to-filter-issues-and-pull-requests) about searching.

## What problem does this solve?

Version: urfave/cli v3.10.1 (also on latest main at commit 4937c16)

There is no way to require a single-value argument (`{Type}Arg`). `ArgumentBase.Parse` falls back to the default value when no argument is given, so a command like `app delete` runs with an empty ID instead of failing.

The closest workaround is the plural type with `Min`/`Max`:

```go
var ids []string

&cli.StringArgs{Name: "id", Min: 1, Max: 1, Destination: &ids}
```

which needs a slice destination for a single value, and shows this when the argument is missing:

```
sufficient count of arg id not provided, given 0 expected 1
```

## Solution description

The same thing flags already have (`FlagBase.Required`):

```go
&cli.StringArg{Name: "id", Required: true, Destination: &id}
```

With `Required: true`, `Parse` returns `Required argument "id" not set` when the argument is missing.

Help output could also follow the bracket convention that `{Type}Args` already uses: `[name]` when optional, `name` when required. Today single args always render as `name` even though they are optional. This changes the expectation in `TestArgUsage` from `ia` to `[ia]`; no other test encodes the current rendering.

## Describe alternatives you've considered

Making `ArgumentBase.Parse` error when the argument is missing, without a new field. That would be a breaking change — the fallback to `Value` is intentional (`TestSingleOptionalArg`).

A `Min` field like the plural type has. On a single value it can only ever be 0 or 1, so a bool seemed like a better fit.
