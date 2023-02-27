import os
import jinja2
from classgen.common import ExtractedClass

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_standard_types import CPPSet, CPPString, CPPStringView, is_numerical_type, CPPMap, CPPTemplatedType
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator
from classgen.enum import Enum
from classgen.jinja_code_generator import JinjaCodeGenerator


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_json_string_template.jinja2'
_STD_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_json_string_std_to_string_template.jinja2'

class CPPToJsonStringGenerator(JinjaCodeGenerator, CPPCodeFragmentsGenerator):

    def __init__(self, function_name: str = "toJsonString", all_defined_classes: dict[str, ExtractedClass] = None) -> None:
        super().__init__()
        self.function_name = function_name
        self.main_template = self.load_template("main", _MAIN_TEMPLATE_PATH)
        self.std_template = self.load_template("std", _STD_TEMPLATE_PATH)
        self.all_defined_classes = [] if all_defined_classes is None else all_defined_classes
    
    def setup_environment(self, environment: jinja2.Environment):
        environment.globals.update(
            is_map = lambda _type: type(_type) == CPPMap,
            is_set = lambda _type: type(_type) == CPPSet,
            is_string = lambda _type: type(_type) == CPPString,
            is_str_or_class = lambda _type: type(_type) == str or type(_type) == CPPClass,
            is_string_view = lambda _type: type(_type) == CPPStringView,
            is_numerical = is_numerical_type,
            is_user_defined = lambda _type: self.all_defined_classes.get(str(_type.name)) != None,
        )
        environment.undefined = jinja2.StrictUndefined

    def generate_fragments(self, clazz: CPPClass | Enum, namespace: str) -> CPPCodeFragments:
        if type(clazz) != CPPClass:
            raise Exception("CPPToJsonStringGenerator only supports code generation for CPPClass")
        
        templated_fields = [field for field in clazz.fields if issubclass(type(field.type), CPPTemplatedType) and not field.static]

        in_class_text = self.main_template.template.render(
            function_name = self.function_name,
            templated_fields = templated_fields,
            all_fields = clazz.fields,
            default_indent_size = 4
        )

        out_namespace_text = self.std_template.template.render(
            function_name = self.function_name,
            namespace = namespace,
            class_name = clazz.name,
            default_indent_size = 4
        )

        result = CPPCodeFragments()
        result.dependencies.standard_includes.append("sstream")
        result.in_class_fragments.append(in_class_text)
        result.out_namespace_fragments.append(out_namespace_text)
        return result