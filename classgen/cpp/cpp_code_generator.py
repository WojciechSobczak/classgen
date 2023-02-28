from classgen.common import Class
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_enum import CPPEnum
from classgen.cpp.generators.cpp_class_code_generator import CPPClassCodeGenerator
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_enum_code_generator import CPPEnumCodeGenerator
from classgen.utils import assert_one_of

class CPPCodeGenerator:

    def __init__(self, additional_generators: list[CPPCodeFragmentsGenerator] = None) -> None:
        super().__init__()
        self.additional_generators = [] if additional_generators is None else additional_generators

    def generate_code(self, clazz: Class | CPPClass | CPPEnum, namespace: str = "") -> str:
        assert_one_of(clazz, [CPPClass, CPPEnum])

        if type(clazz) == CPPClass:
            generator = CPPClassCodeGenerator(namespace=namespace)
            return generator.generate_code(clazz, self.additional_generators)
        elif type(clazz) == CPPEnum:
            generator = CPPEnumCodeGenerator()
            return generator.generate_code(clazz)
        else:
            raise Exception("Invalid type passed to CPPCodeGenerator.generate_code(): " + type(clazz))





