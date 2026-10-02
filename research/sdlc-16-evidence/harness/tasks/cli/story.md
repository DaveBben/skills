No way to mark a single-value argument as required (urfave/cli v3).

A single-value argument (`StringArg`, `IntArg` and the other `{Type}Arg` types) falls back to its default value when it is not given, so a command like `app delete` runs with an empty ID instead of failing. The closest workaround is the plural type with `Min: 1, Max: 1`, which needs a slice destination for a single value and prints `sufficient count of arg id not provided, given 0 expected 1`.

I want what flags already have with `Required`:

```go
&cli.StringArg{Name: "id", Required: true, Destination: &id}
```

Required behaviour:

- Every single-value argument type gets a `Required` field.
- When a required argument is missing, the command's action does not run and `Run` returns an error with the message `Required argument "id" not set`. When several are missing, the message lists them all: `Required arguments "first, second" not set`.
- A missing required argument is a usage error, handled the same way as a missing required flag: printed as `Incorrect Usage: <message>` followed by the command's help, or passed to the command's `OnUsageError` when one is set.
- A default `Value` does not satisfy `Required`, the same as with flags.
- Help output follows the bracket convention the multi-value `{Type}Args` types already use: an optional single-value argument renders as `[name]` and a required one as `name`. A `UsageText` the user sets still overrides this.
- Document the feature in the v3 docs on arguments.
