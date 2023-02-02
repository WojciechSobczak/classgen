from classgen.common import Class
from classgen.enum import Enum

class CodeGenerator:

    def __init__(self) -> None:
        self.additional_generators: list['CodeGenerator'] = []

    def generate_code(self, clazz: Class | Enum) -> str:
        raise Exception("Bare CodeGenerator does not generate any code.")