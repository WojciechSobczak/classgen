

from classgen.classgen import CodeGenerator, Class
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_enum import CPPEnum, CPPEnumField, CPPConstantNumericEnumField, CPPAutoNumericEnumField, CPPComplexEnumField
from classgen.cpp.standard_type import StandardType
from classgen.cpp.access_modifier import AccessModifier
from classgen.cpp.utils import is_or_inherit


import textwrap
import jinja2
import os

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPCodeGenerator(CodeGenerator):

    def __init__(self, namespace: str = "", class_file_map: dict[CPPClass, str] = None) -> None:
        super().__init__()
        self.namespace = "" if namespace is None else namespace
        self.class_file_map = {} if class_file_map is None else class_file_map


    def create_enum_value_struct(self, fields: list[CPPComplexEnumField]) -> dict[str, type]:
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

    def generate_enum_code(self, enum: CPPEnum):
        if type(enum) != CPPEnum:
            raise Exception("generate_enum_code() requires clazz to be CPPEnum")
        with open(f'{_SCRIPT_PATH}/enum_class_template.jinja2', "r") as file:
            text_template = file.read()
        
        simple_fields = [field for field in enum.fields if type(field) != CPPComplexEnumField]
        complex_fields = [field for field in enum.fields if type(field) == CPPComplexEnumField]

        if len(simple_fields) > 0 and len(complex_fields) > 0:
            raise Exception("Complex and non complex fields at the same time are not supported yet")

        def enum_value_to_assignment_string(field: CPPEnumField) -> str:
            if type(field) == CPPAutoNumericEnumField or type(field) == CPPComplexEnumField:
                return ""
            if type(field) == CPPConstantNumericEnumField:
                field: CPPConstantNumericEnumField = field
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
        environment.globals.update(enum_value_to_assignment_string=enum_value_to_assignment_string)
        environment.globals.update(type_to_string=type_to_string)
        environment.globals.update(value_to_string=value_to_string)
        environment.globals.update(get_full_name=get_full_name)
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

    def generate_code(self, clazz: CPPClass | CPPEnum, additional_generators: list['CodeGenerator'] = None) -> str:
        if type(clazz) != CPPClass and type(clazz) != CPPEnum:
            raise Exception("CPPCodeGenerator requires clazz to be CPPClass | CPPEnum")
        
        if type(clazz) == CPPEnum:
            return self.generate_enum_code(clazz)
        raise Exception("NOT NOW")

        with open(f'{_SCRIPT_PATH}/class_template.jinja2', "r") as file:
            text_template = file.read()

        standard_includes = set()
        external_includes = set()

        for field in clazz.fields:
            if type(field.type) == StandardType:
                standard_includes.add(StandardType.get_include(field.type))
            if type(field.type) == CPPClass:
                external_includes.add(self.class_file_map.get(field.type))
            if type(field.type) == str:
                external_includes.add(field.type)

        additional_code = ""
        additional_generators = [] if additional_generators is None else additional_generators
        for generator in additional_generators:
            if is_or_inherit(generator, CodeGenerator):
                additional_code += generator.generate_code(clazz, [])
            #raise Exception("Generator must implement CodeGenerator generate_code()")

        environment = jinja2.Environment()
        template = environment.from_string(text_template)
        text = template.render(
            class_name = clazz.name,
            public_fields = [field for field in clazz.fields if field.access_modifier == AccessModifier.PUBLIC],
            private_fields = [field for field in clazz.fields if field.access_modifier == AccessModifier.PRIVATE],
            protected_fields = [field for field in clazz.fields if field.access_modifier == AccessModifier.PROTECTED],
            indent = "    ",
            additional_code = additional_code,
            standard_includes = standard_includes,
            external_includes = external_includes,
            namespace = self.namespace
        )

        return textwrap.dedent(text)