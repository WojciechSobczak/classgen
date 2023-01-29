

from classgen.common.code_generator import CodeGenerator
from classgen.common.enum import Enum
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_class_code_generator import CPPClassCodeGenerator
from classgen.cpp.cpp_enum_code_generator import CPPEnumCodeGenerator




class CPPCodeGenerator(CodeGenerator):

    def generate_code(self, clazz: CPPClass | Enum, additional_generators: list['CodeGenerator'] = None) -> str:
        if type(clazz) != CPPClass and type(clazz) != Enum:
            raise Exception("CPPCodeGenerator generate_code() require clazz to be CPPClass | Enum")

        if type(clazz) == CPPClass:
            generator = CPPClassCodeGenerator()
            return generator.generate_code(clazz, additional_generators)
        elif type(clazz) == Enum:
            generator = CPPEnumCodeGenerator()
            return generator.generate_code(clazz, additional_generators)
        else:
            raise Exception("NOT HANDLED TYPE IN CPPCodeGenerator")





