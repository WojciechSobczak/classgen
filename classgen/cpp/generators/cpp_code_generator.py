from classgen.common import Class
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_enum import CPPEnum
from classgen.cpp.generators.cpp_class_code_generator import CPPClassCodeGenerator
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_enum_code_generator import CPPEnumCodeGenerator

class CPPCodeGenerator:

    def __init__(self, additional_generators: list[CPPCodeFragmentsGenerator] = None) -> None:
        super().__init__()
        self.additional_generators = [] if additional_generators is None else additional_generators

    def generate_code(self, clazz: Class | CPPClass | CPPEnum) -> str:
        if type(clazz) != CPPClass and type(clazz) != CPPEnum and type(clazz) != Class:
            raise Exception("CPPCodeGenerator generate_code() require clazz to be CPPClass | Enum | Class")

        if type(clazz) == CPPClass or type(clazz) == Class:
            generator = CPPClassCodeGenerator()
            return generator.generate_code(clazz, self.additional_generators)
        elif type(clazz) == CPPEnum:
            generator = CPPEnumCodeGenerator()
            return generator.generate_code(clazz)
        else:
            raise Exception("Invalid type passed to CPPCodeGenerator.generate_code(): " + type(clazz))





