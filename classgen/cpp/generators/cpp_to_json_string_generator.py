from classgen.base.base import CodeGenerator
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.standard_type import StandardType
from classgen.cpp.templated_type import TemplatedType
import jinja2
import textwrap
import os

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPToJsonStringGenerator(CodeGenerator):

    def __init__(self, function_name: str = "toJsonString") -> None:
        self.function_name = function_name

    def generate_code(self, clazz: CPPClass, additional_generators: list[CodeGenerator] = None):
        text_template = ""
        with open(f'{_SCRIPT_PATH}/cpp_to_json_string_template.jinja2', "r") as file:
            text_template = file.read()

        def get_set_value(field: CPPField):
            if type(field.type) == StandardType:
                if field.type.is_numerical():
                    return f'std::to_string({field.name})'
                else:
                    return field.name
            if type(field.type) == str or type(field.type) == CPPClass:
                return f'{field.name}.{self.function_name}()'
            if type(field.type) == TemplatedType:
                return f'{field.name}'
            
            raise Exception("Invalid get_set_value() field type")

        environment = jinja2.Environment()
        environment.globals.update(get_set_value=get_set_value)
        template = environment.from_string(text_template)
        text = template.render(
            clazz = clazz,
            function_name = self.function_name
        )
        return textwrap.dedent(text)
    

    def get_types_include_map(self):
        return {
            "Document" : "utilities/bson.hpp"
        }