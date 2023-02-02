

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_class_code_generator import CPPClassCodeGenerator
from classgen.cpp.cpp_enum_code_generator import CPPEnumCodeGenerator
from classgen import CodeGenerator
from classgen import Enum
from classgen.utils import set_if_none
class CPPCodeGenerator(CodeGenerator):

    def __init__(self) -> None:
        super().__init__()
        self.name_to_include_map: dict[str, str] = {}

    def generate_code(self, clazz: CPPClass | Enum) -> str:
        if type(clazz) != CPPClass and type(clazz) != Enum:
            raise Exception("CPPCodeGenerator generate_code() require clazz to be CPPClass | Enum")
        set_if_none(self.additional_generators, [])

        if type(clazz) == CPPClass:
            generator = CPPClassCodeGenerator()
            return generator.generate_code(clazz, self.additional_generators)
        elif type(clazz) == Enum:
            generator = CPPEnumCodeGenerator()
            return generator.generate_code(clazz, self.additional_generators)
        else:
            raise Exception("Invalid type passed to CPPCodeGenerator.generate_code(): " + type(clazz))





