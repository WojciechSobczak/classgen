import dataclasses
import os
from typing import assert_type
import jinja2
from classgen.common import Class, Field
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_type import CPPType
from classgen.cpp.cpp_standard_types import is_standard_type
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_jinja_code_generator import CPPJinjaCodeGenerator


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

@dataclasses.dataclass
class _CPPClassFields:
    public_fields: list[CPPField]
    private_fields: list[CPPField]
    protected_fields: list[CPPField]

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/templates/class_template.jinja2'

class CPPClassCodeGenerator(CPPJinjaCodeGenerator):

    def __init__(self, all_defined_classes: dict[str, CPPClass] = None):
        super().__init__(all_defined_classes)
        self.namespace = ""
        self.main_template = self.load_template("main", _MAIN_TEMPLATE_PATH)

    def get_field_value_formatted(self, field_value):
        if field_value == None:
            raise Exception("None field value. Cannot be formatted.")
        if type(field_value) in { int, float }:
            return field_value
        else:
            return f'"{field_value}"'

    def setup_environment(self, environment: jinja2.Environment):
        super().setup_environment(environment)
        environment.globals.update(
            get_field_value_formatted = self.get_field_value_formatted,
        )


    def generate_code(self, clazz: CPPClass, additional_generators: list[CPPCodeFragmentsGenerator]) -> str:
        assert_type(clazz, CPPClass)

        class_fragments = CPPCodeFragments()
        for field in clazz.fields:
            field: CPPField = field
            if not issubclass(type(field.type), CPPType):
                raise Exception("ONLY CPP TYPES PLS")
            
            if is_standard_type(field.type) and field.type.include_path is not None:
                class_fragments.dependencies.standard_includes.append(field.type.include_path)
            elif field.type.include_path is not None:
                class_fragments.dependencies.quoted_includes.append(field.type.include_path)

        for generator in additional_generators:
            if not issubclass(type(generator), CPPCodeFragmentsGenerator):
                raise Exception(f"Delivered in class code generator is of type: {type(generator)} and should be {CPPCodeFragmentsGenerator}")
            result = generator.generate_fragments(clazz, self.namespace)
            if result != None:
                class_fragments.merge(result)

        class_fragments.dependencies.remove_duplicates()
       
        text = self.main_template.template.render(
            class_name = clazz.name,
            fields = _CPPClassFields(
                [field for field in clazz.fields if field.access_modifier == CPPAccessModifier.PUBLIC],
                [field for field in clazz.fields if field.access_modifier == CPPAccessModifier.PRIVATE],
                [field for field in clazz.fields if field.access_modifier == CPPAccessModifier.PROTECTED]
            ),
            fragments = class_fragments,
            namespace = self.namespace
        )
        return text