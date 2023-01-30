from classgen.common import Class
from classgen.enum import Enum

class CodeGenerator:
    def generate_code(self, clazz: Class | Enum, additional_generators: list['CodeGenerator'] = None) -> str:
        raise Exception("Bare CodeGenerator does not generate any code.")