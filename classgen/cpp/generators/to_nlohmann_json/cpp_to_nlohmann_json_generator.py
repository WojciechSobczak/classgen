import os
import jinja2

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_standard_types import CPPSet, CPPString, CPPStringView, is_numerical_type, CPPMap, CPPTemplatedType
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator
from classgen.enum import Enum
from classgen.jinja_code_generator import JinjaCodeGenerator


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_nlohmann_json_template.jinja2'

class CPPToNlohmannJsonGenerator(JinjaCodeGenerator, CPPCodeFragmentsGenerator):

    def __init__(self, function_name: str = "toNlohmannJson") -> None:
        super().__init__()
        self.function_name = function_name
        self.main_template = self.load_template("main", _MAIN_TEMPLATE_PATH)
    
    def setup_environment(self, environment: jinja2.Environment):
        environment.globals.update(
            is_map = lambda _type: type(_type) == CPPMap,
            is_set = lambda _type: type(_type) == CPPSet,
            is_string = lambda _type: type(_type) == CPPString,
            is_str_or_class = lambda _type: type(_type) == str or type(_type) == CPPClass,
            is_string_view = lambda _type: type(_type) == CPPStringView,
            is_numerical = is_numerical_type
        )
        environment.undefined = jinja2.StrictUndefined

    def generate_fragments(self, clazz: CPPClass | Enum, namespace: str) -> CPPCodeFragments:
        if type(clazz) != CPPClass:
            raise Exception("CPPToNlohmannJsonGenerator only supports code generation for CPPClass")
        
        templated_fields = [field for field in clazz.fields if issubclass(type(field.type), CPPTemplatedType) and not field.static]

        in_class_text = self.main_template.template.render(
            function_name = self.function_name,
            templated_fields = templated_fields,
            all_fields = clazz.fields,
            default_indent_size = 4
        )

        result = CPPCodeFragments()
        result.dependencies.libraries_includes.append("nlohmann/json.hpp")
        result.in_class_fragments.append(in_class_text)
        return result