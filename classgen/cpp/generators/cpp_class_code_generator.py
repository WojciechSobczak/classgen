import dataclasses
import jinja2
import os
from classgen.code_generator import CodeGenerator
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_templated_type import CPPTemplatedType
from classgen.cpp.cpp_type import CPPType
from classgen.cpp.cpp_standard_types import is_standard


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPClassCodeGenerator:
    @dataclasses.dataclass
    class Includes:
        standard_includes: list[str]
        external_includes: list[str]

    def __init__(self):
        super().__init__()
        self.namespace = ""
        self.class_file_map: dict[str, str] = {}

    def extract_includes(self, fields: list[CPPField]) -> Includes:
        standard_includes = set()
        external_includes = set()

        for field in fields:
            if not issubclass(type(field.type), CPPType):
                raise Exception("ONLY CPP TYPES PLS")
            collection = standard_includes if is_standard(field.type) else external_includes
            if field.type.include_path is not None:
                collection.add(field.type.include_path)

        return self.Includes(list(standard_includes), list(external_includes))


    def generate_code(self, clazz: CPPClass, additional_generators: list['CodeGenerator']) -> str:
        if type(clazz) != CPPClass:
            raise Exception("CPPCodeGenerator requires clazz to be CPPClass")

        with open(f'{_SCRIPT_PATH}/templates/class_template.jinja2', "r", encoding="UTF-8") as file:
            text_template = file.read()

        additional_generated_codes = []
        for generator in additional_generators:
            if not issubclass(type(generator), CodeGenerator):
                raise Exception(f"Delivered code generator is of type: {type(generator)} and should be {CodeGenerator}")
            additional_generated_codes.append(generator.generate_code(clazz))

        def get_field_value_formatted(field_value):
            if field_value == None:
                raise Exception("None field value. Cannot be formatted.")
            if type(field_value) in { int, float }:
                return field_value
            else:
                return f'"{field_value}"'
            
        def format_field_type(field_type: CPPType):
            formatted_type = field_type.name
            if issubclass(type(field_type), CPPTemplatedType):
                field_type: CPPTemplatedType = field_type
                args_type_names = []
                for arg in field_type.args:
                    args_type_names.append(arg.name)
                formatted_type +=f'<{", ".join(args_type_names)}>'
            return formatted_type

        environment = jinja2.Environment()
        template = environment.from_string(text_template)
        environment.globals.update(
            get_field_value_formatted = get_field_value_formatted,
            format_field_type = format_field_type
        )
        text = template.render(
            class_name = clazz.name,
            public_fields = [field for field in clazz.fields if field.access_modifier == CPPAccessModifier.PUBLIC],
            private_fields = [field for field in clazz.fields if field.access_modifier == CPPAccessModifier.PRIVATE],
            protected_fields = [field for field in clazz.fields if field.access_modifier == CPPAccessModifier.PROTECTED],
            additional_generated_codes = additional_generated_codes,
            includes = self.extract_includes(clazz.fields),
            namespace = self.namespace
        )

        return text