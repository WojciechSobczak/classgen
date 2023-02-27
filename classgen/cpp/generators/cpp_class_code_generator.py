import dataclasses
import os
import jinja2
from classgen.common import Class, Field
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_templated_type import CPPTemplatedType
from classgen.cpp.cpp_type import CPPType
from classgen.cpp.cpp_standard_types import is_standard_type
from classgen.cpp.generators.cpp_code_fragments_generator import CPPCodeFragments, CPPCodeFragmentsGenerator


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

@dataclasses.dataclass
class _CPPClassFields:
    public_fields: list[CPPField]
    private_fields: list[CPPField]
    protected_fields: list[CPPField]

class CPPClassCodeGenerator:

    def __init__(self):
        super().__init__()
        self.namespace = ""

    def generate_code(self, clazz: Class | CPPClass, additional_generators: list[CPPCodeFragmentsGenerator]) -> str:
        if type(clazz) != CPPClass and type(clazz) != Class:
            raise Exception("CPPCodeGenerator requires clazz to be CPPClass | Class")

        with open(f'{_SCRIPT_PATH}/templates/class_template.jinja2', "r", encoding="UTF-8") as file:
            text_template = file.read()

        class_fields: list[CPPField] = []
        if type(clazz) == Class:
            for field in clazz.fields:
                if type(field) == Field:
                    class_fields.append(CPPField.from_basic_field(field))
                elif type(field) == CPPField:
                    class_fields.append(field)
                else:
                    raise Exception("NOT SUPPORTED TYPE FIELD")
        else:
            class_fields = clazz.fields

        class_fragments = CPPCodeFragments()
        for field in class_fields:
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
            class_name = clazz.class_type.__name__,
            fields = _CPPClassFields(
                [field for field in class_fields if field.access_modifier == CPPAccessModifier.PUBLIC],
                [field for field in class_fields if field.access_modifier == CPPAccessModifier.PRIVATE],
                [field for field in class_fields if field.access_modifier == CPPAccessModifier.PROTECTED]
            ),
            fragments = class_fragments,
            namespace = self.namespace
        )
        return text