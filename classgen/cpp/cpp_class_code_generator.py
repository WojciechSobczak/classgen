

from classgen.common.code_generator import CodeGenerator
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.standard_type import StandardType
from classgen.cpp.access_modifier import AccessModifier
from classgen.cpp.utils import is_or_inherit


import textwrap
import jinja2
import os

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPClassCodeGenerator(CodeGenerator):

    def __init__(self, namespace: str = "", class_file_map: dict[CPPClass, str] = None) -> None:
        super().__init__()
        self.namespace = "" if namespace is None else namespace
        self.class_file_map = {} if class_file_map is None else class_file_map

    def generate_code(self, clazz: CPPClass, additional_generators: list['CodeGenerator'] = None) -> str:
        if type(clazz) != CPPClass:
            raise Exception("CPPCodeGenerator requires clazz to be CPPClass")

        with open(f'{_SCRIPT_PATH}/templates/class_template.jinja2', "r") as file:
            text_template = file.read()

        standard_includes = set()
        external_includes = set()

        for field in clazz.fields:
            if type(field.type) == StandardType:
                standard_includes.add(StandardType.get_include(field.type))
            if type(field.type) == CPPClass:
                external_includes.add(self.class_file_map.get(field.type))
            if type(field.type) == str:
                external_includes.add(field.type)

        additional_code = ""
        additional_generators = [] if additional_generators is None else additional_generators
        for generator in additional_generators:
            if is_or_inherit(generator, CodeGenerator):
                additional_code += generator.generate_code(clazz, [])

        environment = jinja2.Environment()
        template = environment.from_string(text_template)
        text = template.render(
            class_name = clazz.name,
            public_fields = [field for field in clazz.fields if field.access_modifier == AccessModifier.PUBLIC],
            private_fields = [field for field in clazz.fields if field.access_modifier == AccessModifier.PRIVATE],
            protected_fields = [field for field in clazz.fields if field.access_modifier == AccessModifier.PROTECTED],
            indent = "    ",
            additional_code = additional_code,
            standard_includes = standard_includes,
            external_includes = external_includes,
            namespace = self.namespace
        )

        return textwrap.dedent(text)