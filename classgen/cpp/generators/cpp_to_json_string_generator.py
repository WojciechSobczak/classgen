import jinja2
import os
import textwrap

from classgen.code_generator import CodeGenerator
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_standard_types import is_numerical


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPToJsonStringGenerator(CodeGenerator):

    def __init__(self, function_name: str = "toJsonString") -> None:
        super().__init__()
        self.function_name = function_name

    def generate_code(self, clazz: CPPClass):
        if type(clazz) != CPPClass:
            raise Exception("CPPToJsonStringGenerator only supports code generation for CPPClass")

        with open(f'{_SCRIPT_PATH}/cpp_to_json_string_template.jinja2', "r", encoding="UTF-8") as file:
            text_template = file.read()

        def get_set_value(field: CPPField):
            if is_numerical(field.type):
                return f'std::to_string({field.name})'
            else:
                return f'std::string({field.name})'
            # if type(field.type) == str or type(field.type) == CPPClass:
            #     return f'{field.name}.{self.function_name}()'
            # if type(field.type) == CPPTemplatedType:
            #     return f'{field.name}'
            
            raise Exception("Invalid get_set_value() field type")

        environment = jinja2.Environment()
        environment.globals.update(get_set_value=get_set_value)
        template = environment.from_string(text_template)
        text = template.render(
            clazz = clazz,
            function_name = self.function_name
        )
        return text