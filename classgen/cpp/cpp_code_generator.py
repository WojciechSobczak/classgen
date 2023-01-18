

from ..classgen import CodeGenerator, CodegenClass
from .cpp_class import CPPClass
from .standard_type import StandardType
from .access_modifier import AccessModifier
import textwrap
import jinja2
import os

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPCodeGenerator(CodeGenerator):
    def generate_code(self, clazz: CPPClass, additional_generators: list['CodeGenerator'] = None) -> str:
        if type(clazz) != CPPClass or type(clazz).__bases__.__contains__(CodegenClass) == False:
            raise Exception("CPPCodeGenerator requires clazz to be CPPClass and derive from CodegenClass")

        text_template = ""
        with open(f'{_SCRIPT_PATH}/class_template.jinja2', "r") as file:
            text_template = file.read()

        standard_includes = set()
        external_includes = set()

        for field in clazz.fields:
            if type(field.type) == StandardType:
                standard_includes.add(StandardType.get_include(field.type))
            if type(field.type) == CPPClass:
                external_includes.add("CLASS")
            if type(field.type) == str:
                pass

        additional_code = ""
        additional_generators = [] if additional_generators is None else additional_generators
        for generator in additional_generators:
            if type(generator).__bases__.__contains__(CodeGenerator) == False:
                raise Exception("Generator must implement CodeGenerator generate_code()")
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
            external_includes = external_includes
        )

        return textwrap.dedent(text)