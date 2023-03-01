import dataclasses
import os
import jinja2
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_type import CPPType
from classgen.cpp.cpp_standard_types import CPPTemplatedType, is_standard_type, is_templated_type
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator
from classgen.cpp.generators.cpp_jinja_code_generator import CPPJinjaCodeGenerator
from classgen.cassert import assert_type


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

@dataclasses.dataclass
class _CPPClassFields:
    public_fields: list[CPPField]
    private_fields: list[CPPField]
    protected_fields: list[CPPField]

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/templates/class_template.jinja2'

class CPPClassCodeGenerator(CPPJinjaCodeGenerator):

    def __init__(self, all_defined_classes: dict[str, CPPClass] = None, namespace: str = ""):
        super().__init__(all_defined_classes)
        self.namespace = namespace
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

        def extract_all_types(field_or_type: CPPField | CPPType) -> list[CPPType]:
            output: list[CPPType] = []
            if type(field_or_type) == CPPField:
                field: CPPField = field_or_type
                output += extract_all_types(field.type)
                return output
            elif issubclass(type(field_or_type), CPPType):
                cpp_type: CPPType = field_or_type
                if is_templated_type(type(cpp_type)):
                    templated_type: CPPTemplatedType = cpp_type
                    output.append(templated_type)
                    for arg in templated_type.args:
                        output += extract_all_types(arg)
                else:
                    output.append(cpp_type)
                return output
            else:
                raise Exception("extract_all_types(): UNEXPECTED TYPE")


        class_fragments = CPPCodeFragments()
        for field in clazz.fields:
            all_fields_types = extract_all_types(field)
            for field_type in all_fields_types:
                if field_type.include_path is not None:
                    includes = class_fragments.dependencies.quoted_includes
                    if is_standard_type(type(field_type)):
                        includes = class_fragments.dependencies.standard_includes
                    includes.append(field_type.include_path)

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