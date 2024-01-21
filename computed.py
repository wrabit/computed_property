import ast
import inspect
import textwrap


class ComputedProperty:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if instance not in self.cache:
            self.cache[instance] = self.func(instance)
        return self.cache[instance]

    def invalidate(self, instance):
        if instance in self.cache:
            del self.cache[instance]


class DependencyExtractor(ast.NodeVisitor):
    """Use AST to extract dependencies from a function, looking specifically for attributes referencing 'self'"""
    def __init__(self):
        self.dependencies = set()

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'self':
            self.dependencies.add(node.attr)
        self.generic_visit(node)


def extract_dependencies(func):
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    extractor = DependencyExtractor()
    extractor.visit(tree)
    return extractor.dependencies


class ComputedPropertyMeta(type):
    def __new__(cls, name, bases, dct):
        computed_properties = []
        for attr_name, attr_value in dct.items():
            if isinstance(attr_value, ComputedProperty):
                computed_properties.append(attr_value)
                attr_value.func.dependencies = extract_dependencies(attr_value.func)
        dct['_computed_properties'] = computed_properties
        return super().__new__(cls, name, bases, dct)


class HasComputedProperties(metaclass=ComputedPropertyMeta):
    def __init__(self):
        super().__init__()

    def __setattr__(self, name, value):
        """Invalidate cached computed properties if their dependencies are changed."""
        super().__setattr__(name, value)
        for prop in self._computed_properties:
            if name in prop.func.dependencies:
                prop.invalidate(self)


def computed_property(func):
    return ComputedProperty(func)