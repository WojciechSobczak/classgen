from dataclasses import dataclass, field
from classgen.cassert import assert_subclass, assert_type
from classgen.common import Class
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_includes import CPPIncludes
from classgen.enum import Enum



@dataclass
class CPPCodeFragments:
    dependencies: CPPIncludes = field(default_factory=lambda: CPPIncludes())
    before_namespace_fragments: list[str] = field(default_factory=list)
    after_namespace_before_class_fragments: list[str] = field(default_factory=list)
    in_class_fragments: list[str] = field(default_factory=list)
    out_class_in_namespace_fragments: list[str] = field(default_factory=list)
    out_namespace_fragments: list[str] = field(default_factory=list)

    def merge(self, other: 'CPPCodeFragments'):
        self.dependencies.merge(other.dependencies)
        self.before_namespace_fragments += other.before_namespace_fragments
        self.after_namespace_before_class_fragments += other.after_namespace_before_class_fragments
        self.in_class_fragments += other.in_class_fragments
        self.out_class_in_namespace_fragments += other.out_class_in_namespace_fragments
        self.out_namespace_fragments += other.out_namespace_fragments

class CPPCodeFragmentsGenerator:
    def __init__(self, exclusions: set[Class] = None, inclusions: set[Class] = None, all_defined_classes: dict[str, CPPClass] = None) -> None:
        self.exclusions = set() if exclusions is None else set(exclusions)
        self.inclusions = set() if inclusions is None else set(inclusions)
        self.all_defined_classes = {} if all_defined_classes is None else all_defined_classes

    def generate_fragments(self, clazz: CPPClass | Enum, namespace: str = "") -> CPPCodeFragments | None:
        raise Exception("CPPCodeFragmentsGenerator() doesnt generate nothing on its own. Pls override it.")
    
    def is_included(self, clazz: Class) -> bool:
        assert_subclass(clazz, Class)
        if len(self.inclusions) > 0:
            return clazz.class_type in self.inclusions
        if len(self.exclusions) > 0 and clazz.class_type in self.exclusions:
            return False
        return True