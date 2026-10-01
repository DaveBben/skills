Let `on_setattr` hooks in attrs run code after the new value has been set.

Today an `on_setattr` hook (on `attr.ib`/`attrs.field`, or class-wide on `@attr.s`/`@attrs.define`) is called as `hook(instance, attribute, new_value)` before the attribute is set, and its return value is what gets set. There is no way to run code after the assignment, for example to recompute a derived attribute from the new value or to notify an observer that the value changed.

I want to be able to write the hook as a generator function:

```python
def hook(instance, attribute, value):
    # runs before the attribute is set; instance still holds the old value
    yield value.strip()      # the yielded value is what gets set
    # runs after the attribute is set; instance now holds the new value
    notify(instance)

@attrs.define
class C:
    x: str = attrs.field(on_setattr=hook)
```

A generator hook must yield exactly once. If it yields more than once, raise `RuntimeError` with the message `Generator on_setattr hook yielded more than once.`

Plain (non-generator) hooks must keep working exactly as they do today, and hooks still do not run during `__init__`. Document the feature where `on_setattr` is documented.
