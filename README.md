# @computed_property

An attempt to create computed properties ala vue, svelte, laravel livewire but in python.

Take this class:

```python
class Example(HasComputedProperties):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    @computed_property
    def my_computed(self):
        return self.x * self.y
```

For all intents and purposes, my_computed acts like a cached property but should a dependency of `my_computed` change (x or y) it will automatically be recalculated and cached.
