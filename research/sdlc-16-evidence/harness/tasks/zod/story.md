Zod 4: a discriminated union whose members have defaulted discriminators can no longer validate explicitly tagged input.

We build concrete commands with schemas whose tag field has a default, so that the caller who already picked the schema doesn't have to pass the tag:

```ts
const CreateUser = z.object({ type: z.literal("CreateUser").default("CreateUser"), name: z.string() });
const DeleteUser = z.object({ type: z.literal("DeleteUser").default("DeleteUser"), id: z.number() });
CreateUser.parse({ name: "a" }); // { type: "CreateUser", name: "a" }
```

We then validate incoming, explicitly tagged messages with a discriminated union of the same schemas:

```ts
const Command = z.discriminatedUnion("type", [CreateUser, DeleteUser]);
Command.parse({ type: "DeleteUser", id: 1 });
```

Since the recent change that rejects overlapping discriminator values, this throws `Duplicate discriminator value "undefined"`, because both members accept an absent `type`. That rejects the whole union, even for input that carries a unique, explicit tag. It broke working production code within the same major version.

Required behaviour:

- Input with an explicit tag that exactly one member claims selects and validates that member, as before, with sync and async parsing alike.
- When several members accept an absent (undefined) discriminator, input without the tag is not guessed: it fails validation with a normal validation error (a `ZodError` from `parse`, `success: false` from `safeParse`), not a schema-definition error.
- An undefined discriminator that exactly one member accepts still routes to that member.
- Two members that claim the same defined value (for example both `"a"`, or both `null`) remain a schema-definition error, `Duplicate discriminator value ...`, as today.
- `z.getDiscriminatedOption(schema, undefined)` when several members accept undefined throws an error whose message contains `Ambiguous discriminator value "undefined"`.

Keep to the repository's rules in AGENTS.md, including its performance, memory and bundle-size expectations.
