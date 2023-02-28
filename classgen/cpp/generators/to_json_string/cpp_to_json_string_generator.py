import os
from classgen.common import Class

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_standard_types import CPPTemplatedType
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_jinja_code_generator import CPPJinjaCodeGenerator
from classgen.enum import Enum
from classgen.utils import assert_one_of


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_json_string_template.jinja2'
_STD_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_json_string_std_to_string_template.jinja2'

class CPPToJsonStringGenerator(CPPJinjaCodeGenerator, CPPCodeFragmentsGenerator):

    def __init__(self, function_name: str = "toJsonString", all_defined_classes: dict[str, CPPClass] = None) -> None:
        super().__init__()
        self.function_name = function_name
        self.main_template = self.load_template("main", _MAIN_TEMPLATE_PATH)
        self.std_template = self.load_template("std", _STD_TEMPLATE_PATH)
        self.all_defined_classes = [] if all_defined_classes is None else all_defined_classes

    def generate_fragments(self, clazz: Class | CPPClass | Enum, namespace: str = "") -> CPPCodeFragments:
        assert_one_of(clazz, [CPPClass, Enum])
        
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
        for include in ["sstream", "iomanip"]:
            result.dependencies.standard_includes.append(include)

        result.in_class_fragments.append(in_class_text)
        result.out_namespace_fragments.append(out_namespace_text)
        return result