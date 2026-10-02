Compatibility reconsideration: defaulted discriminator fields prevent validation of explicitly tagged commands

Reproduction [repository](https://github.com/david-gettins/zod-issue-repro) link.

We are affected in production by the behaviour discussed in #6545. I understand that rejecting overlapping discriminator inputs is intentional; this is a request to reconsider the compatibility impact on applications that reuse concrete construction schemas in discriminated unions.

We use defaulted literal type fields when constructing a known command or event. For example, `CreateUser.parse(...)` supplies "CreateUser" because the caller has already selected the concrete schema.

We then use the discriminated union to validate explicitly tagged messages. We are not asking it to infer a command kind from an omitted discriminator. The problem is that the overlap on undefined prevents validation even when the input already contains a unique, explicit tag.

## Proposal

Could Zod support this composition pattern while continuing to reject ambiguous untagged input?

Our required behaviour is that explicit, unique discriminator values continue to select and validate their corresponding members. When multiple members accept an absent discriminator, we would prefer a normal validation failure for that input rather than rejection of the union for all tagged inputs. Duplicate explicit literal tags could remain schema-definition errors.

We understand that this would relax the current schema-wide uniqueness rule. We are asking whether preserving this existing construction-and-validation pattern warrants that exception, or whether an explicit compatibility option would be acceptable.

We have identified the safeExtend/unwrap workaround. It preserves concrete-schema construction defaults, but requires migration and regression testing at the affected union composition sites.

Regardless of whether the previous behaviour is classified as a bug, the upgrade changes working production behaviour within the same major version. If the current rule is retained, please document the compatibility impact and the recommended migration pattern.

