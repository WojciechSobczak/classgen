from classgen.cpp.cpp_class import CPPClass
from classgen import Enum
from classgen.cpp.generators.cpp_class_code_generator import CPPClassCodeGenerator
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_enum_code_generator import CPPEnumCodeGenerator
class CPPCodeGenerator:

    def __init__(self) -> None:
        super().__init__()
        self.name_to_include_map: dict[str, str] = {}
        self.additional_generators: list[CPPCodeFragmentsGenerator] = []

    def generate_code(self, clazz: CPPClass | Enum) -> str:
        if type(clazz) != CPPClass and type(clazz) != Enum:
            raise Exception("CPPCodeGenerator generate_code() require clazz to be CPPClass | Enum")

        if type(clazz) == CPPClass:
            generator = CPPClassCodeGenerator()
            return generator.generate_code(clazz, self.additional_generators)
        elif type(clazz) == Enum:
            generator = CPPEnumCodeGenerator()
            return generator.generate_code(clazz)
        else:
            raise Exception("Invalid type passed to CPPCodeGenerator.generate_code(): " + type(clazz))





