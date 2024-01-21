# @computed_property

`@computed_property` is inspired by similar concepts in Vue.js, Svelte, and Laravel Livewire. It aims to introduce computed properties to Python, allowing properties within a class to be automatically recalculated and cached based on their dependencies.

## Concept

A computed property acts like a regular class property but with an underlying method that calculates its value. This value is cached for efficiency. Whenever a "dependency" (an attribute that the computed property relies on) changes, the computed property automatically recalculates and updates its value.

## Example

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

In this example, `my_computed` is a computed property dependent on `x` and `y`. If either `x` or `y` changes, `my_computed` is automatically recalculated and updated.

```python
test = Example(1,2)

print(test.my_computed)
# computed property is calculated
> 2

print(test.my_computed)
# cached version is used
> 2

test.x = 2
print(test.my_computed)
# computed property is re-calculated
> 4
```

## How it Works

The library uses Python's decorators and metaclasses to track dependencies and manage the caching of computed properties. Dependencies are determined automatically through code introspection and looking up the @computed_property function's abstract syntax tree (AST).

## Limitations

- We look for references of 'self' in the method body, so it may not cater for the situation where other methods are updating a dependency.
