import dataclasses

from classgen import Class
from classgen.cpp.cpp_field import CPPField

class CPPClass(Class):

    def __init__(self, name: str, include_path: str, class_type: type, fields: list[CPPField] = None) -> None:
        super().__init__(class_type, fields)
        self.name = name
        self.include_path = include_path
        self.fields = fields
