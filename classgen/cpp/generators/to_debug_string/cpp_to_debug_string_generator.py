import os
from classgen.common import Class

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_standard_types import CPPTemplatedType
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_jinja_code_generator import CPPJinjaCodeGenerator
from classgen.enum import Enum
from classgen.cassert import assert_one_of_types


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/to_debug_string_template.jinja2'
_STD_TEMPLATE_PATH = f'{_SCRIPT_PATH}/to_debug_string_stdtostring_template.jinja2'

class CPPToDebugJsonStringGenerator(CPPJinjaCodeGenerator, CPPCodeFragmentsGenerator):

    def __init__(self, 
        function_name: str = "toDebugJsonString", 
        exclusions: list[Class] = None, 
        inclusions: list[Class] = None, 
        all_defined_classes: dict[str, CPPClass] = None
    )-> None:
        CPPJinjaCodeGenerator.__init__(self)
        CPPCodeFragmentsGenerator.__init__(self, 
            exclusions = exclusions,
            inclusions = inclusions,
            all_defined_classes = all_defined_classes
        )
        self.function_name = function_name
        self.main_template = self.load_template("main", _MAIN_TEMPLATE_PATH)
        self.std_template = self.load_template("std", _STD_TEMPLATE_PATH)

    def generate_fragments(self, clazz: Class | CPPClass | Enum, namespace: str = "") -> CPPCodeFragments:
        assert_one_of_types(clazz, [CPPClass, Enum])
        if not self.is_included(clazz):
            return CPPCodeFragments()
        
        in_class_text = self.main_template.template.render(
            function_name = self.function_name,
            all_fields = clazz.fields,
            default_indent_size = 4,
            class_name = clazz.name
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

        result.dependencies.libraries_includes.append("classgen/classgen.hpp")

        result.in_class_fragments.append(in_class_text)
        result.out_namespace_fragments.append(out_namespace_text)
        return result