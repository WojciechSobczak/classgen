import os
import jinja2
from classgen.cassert import assert_type
from classgen.common import Class

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_standard_types import CPPTemplatedType
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_jinja_code_generator import CPPJinjaCodeGenerator
from classgen.enum import Enum


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_nlohmann_json_template.jinja2'

class CPPToNlohmannJsonGenerator(CPPJinjaCodeGenerator, CPPCodeFragmentsGenerator):

    def __init__(self, 
        function_name: str = "toNlohmannJson", 
        exclusions: list[Class] = None, 
        inclusions: list[Class] = None, 
        all_defined_classes: dict[str, CPPClass] = None
    )-> None:
        CPPJinjaCodeGenerator.__init__(self)
        CPPCodeFragmentsGenerator.__init__(self,
            all_defined_classes = all_defined_classes,
            exclusions = exclusions,
            inclusions = inclusions
        )
        self.function_name = function_name
        self.main_template = self.load_template("main", _MAIN_TEMPLATE_PATH)
    
    def generate_fragments(self, clazz: CPPClass | Enum, namespace: str = "") -> CPPCodeFragments:
        assert_type(clazz, CPPClass)
        if not self.is_included(clazz):
            return CPPCodeFragments()
        
        templated_fields = [field for field in clazz.fields if issubclass(type(field.type), CPPTemplatedType) and not field.static]

        in_class_text = self.main_template.template.render(
            function_name = self.function_name,
            namespace = namespace,
            templated_fields = templated_fields,
            all_fields = clazz.fields,
            default_indent_size = 4
        )

        result = CPPCodeFragments()
        result.dependencies.libraries_includes.append("nlohmann/json.hpp")
        result.in_class_fragments.append(in_class_text)
        result.before_namespace_fragments.append('//before_namespace_fragments')
        result.after_namespace_before_class_fragments.append('//after_namespace_before_class_fragments')
        return result