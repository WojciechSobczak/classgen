import textwrap
import jinja2
import os

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_enum import CPPEnum
from classgen.enum import Enum, EnumField, ConstantNumericEnumField, AutoNumericEnumField, ComplexEnumField

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPEnumCodeGenerator:

    def __init__(self, namespace: str = "", class_file_map: dict[CPPClass, str] = None) -> None:
        super().__init__()
        self.namespace = "" if namespace is None else namespace
        self.class_file_map = {} if class_file_map is None else class_file_map


    def create_enum_value_struct(self, fields: list[ComplexEnumField]) -> dict[str, type]:
        struct_fields = set()
        for field in fields:
            if type(field.value) == dict:
                struct_fields.update(field.value.keys())
        if len(struct_fields) > 0:
            for field in fields:
                if type(field.value) == dict:
                    if struct_fields != set(field.value.keys()):
                        raise Exception("No same enum value objects not supported yet")
        
        struct_def: dict[str, type] = {}
        for field in fields:
            for key, value in field.value.items():
                struct_def[key] = type(value)
        return struct_def

    def generate_code(self, enum: CPPEnum) -> str:
        if type(enum) != CPPEnum:
            raise Exception(f"{self.__class__.__name__} requires clazz to be Enum")
        
        with open(f'{_SCRIPT_PATH}/templates/enum_class_template.jinja2', "r", encoding="UTF-8") as file:
            text_template = file.read()
        
        simple_fields = [field for field in enum.fields if type(field) != ComplexEnumField]
        complex_fields = [field for field in enum.fields if type(field) == ComplexEnumField]

        if len(simple_fields) > 0 and len(complex_fields) > 0:
            raise Exception("Complex and non complex fields at the same time are not supported yet")

        def enum_value_to_assignment_string(field: EnumField) -> str:
            if type(field) == AutoNumericEnumField or type(field) == ComplexEnumField:
                return ""
            if type(field) == ConstantNumericEnumField:
                field: ConstantNumericEnumField = field
                return " = " + str(field.value)
            raise Exception(f"enum_value_to_assignment_string NOT IMPLEMENTED TYPE {type(field)}")

        def type_to_string(_type: type) -> str:
            if _type == str:
                return "std::string_view"
            if _type == int:
                return "int64_t"
            if _type == float:
                return "double"
            raise Exception(f"type_to_string NOT IMPLEMENTED TYPE {_type}")
        
        def value_to_string(value) -> str:
            if type(value) == str:
                return f'"{value}"'
            if type(value) == int or type(value) == float:
                return str(value)
            raise Exception(f"value_to_string NOT IMPLEMENTED TYPE {type(value)}")
        
        def get_full_name(name: str) -> str:
            output = self.namespace
            if len(output) != 0:
                output += "::"
            output += name
            return name

        struct_definition: dict[str, type] = {}
        if len(complex_fields) > 0:
            struct_definition = self.create_enum_value_struct(complex_fields)

        environment = jinja2.Environment()
        environment.globals.update(
            enum_value_to_assignment_string=enum_value_to_assignment_string,
            type_to_string=type_to_string,
            value_to_string=value_to_string,
            get_full_name=get_full_name,
        )
        template = environment.from_string(text_template)
        text = template.render(
            enum = enum,
            struct_definition = struct_definition,
            complex_fields = complex_fields,
            indent = "    ",
            additional_code = "",
            namespace = self.namespace
        )

        return textwrap.dedent(text)