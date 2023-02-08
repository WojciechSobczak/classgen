import dataclasses
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_includes import CPPIncludes
from classgen.enum import Enum



@dataclasses.dataclass
class CPPCodeFragments:
    dependencies: CPPIncludes
    before_namespace_fragments: list[str]
    after_namespace_before_class_fragments: list[str]
    in_class_fragments: list[str]
    out_class_in_namespace_fragments: list[str]
    out_namespace_fragments: list[str]

    def __init__(self) -> None:
        self.dependencies = CPPIncludes()
        self.before_namespace_fragments = []
        self.after_namespace_before_class_fragments = []
        self.in_class_fragments = []
        self.out_class_in_namespace_fragments = []
        self.out_namespace_fragments = []

    def merge(self, other: 'CPPCodeFragments'):
        self.dependencies.merge(other.dependencies)
        self.before_namespace_fragments += other.before_namespace_fragments
        self.after_namespace_before_class_fragments += other.after_namespace_before_class_fragments
        self.in_class_fragments += other.in_class_fragments
        self.out_class_in_namespace_fragments += other.out_class_in_namespace_fragments
        self.out_namespace_fragments += other.out_namespace_fragments

@dataclasses.dataclass
class CPPCodeFragmentsGenerator:
    def generate_fragments(self, clazz: CPPClass | Enum, namespace: str) -> CPPCodeFragments | None:
        raise Exception("CPPCodeFragmentsGenerator() doesnt generate nothing on its own. Pls override it.")