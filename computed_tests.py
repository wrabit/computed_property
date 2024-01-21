import unittest

from computed import HasComputedProperties, computed_property


# Example class using the system for testing
class Example(HasComputedProperties):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.fake_operation_count = 0

    def fake_compute_operation(self):
        self.fake_operation_count += 1

    @computed_property
    def my_computed(self):
        self.fake_compute_operation()
        return self.x * self.y


class ComputedDependents(HasComputedProperties):
    a: int

    @computed_property
    def b(self):
        return self.a + 5

    @computed_property
    def c(self):
        return self.a * self.b


class TestComputedProperty(unittest.TestCase):
    def test_computed_property_evaluation(self):
        example = Example(5, 3)
        self.assertEqual(example.my_computed, 15)

    def test_computed_property_caching(self):
        example = Example(5, 3)
        _ = example.my_computed  # This should use the cache
        _ = example.my_computed  # This should use the cache
        _ = example.my_computed  # This should use the cache
        self.assertEqual(example.fake_operation_count, 1)

    def test_invalidation_on_dependency_change(self):
        example = Example(5, 3)
        self.assertEqual(example.fake_operation_count, 0)
        _ = example.my_computed  # Initial calculation
        self.assertEqual(example.fake_operation_count, 1)
        example.x = 10  # Change a dependency
        self.assertEqual(example.my_computed, 30)  # Recalculation should happen
        self.assertEqual(example.fake_operation_count, 2)

    def test_no_invalidation_on_non_dependency_change(self):
        example = Example(5, 3)
        first_result = example.my_computed  # Initial calculation
        example.z = 100  # Change a non-dependency
        self.assertEqual(example.my_computed, first_result)  # Should use cached value

    def test_computeds_that_depend_on_other_computeds(self):
        so = ComputedDependents()
        so.a = 5
        self.assertEqual(so.b, 10)
        self.assertEqual(so.c, 50)

if __name__ == '__main__':
    unittest.main()
