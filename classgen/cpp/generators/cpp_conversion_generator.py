
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField
from classgen.classgen import ConversionGenerator, ConversionMap
import jinja2
import textwrap
import os

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPConversionGenerator(ConversionGenerator):
    def generate_conversion(from_class: CPPClass, to_class: CPPClass) -> str:
        return ""

    def generate_conversion(from_class: CPPClass, to_class: CPPClass, mapping: ConversionMap) -> str:

        conversion_mapping: dict[str, str] = {}

        for from_field in from_class.fields:
            from_field: CPPField = from_field
            for to_field in to_class.fields:
                to_field: CPPField = to_field
                if from_field.name == to_field.name and from_field.type == to_field.type:
                    conversion_mapping[from_field.name] = from_field.name

        for mapped in mapping.fieldMapping.items():
            fromField = mapped[0]
            toField = mapped[1]
            conversion_mapping[fromField.name] = toField.name

        for mapped in mapping.renaming_mapping.items():
            conversion_mapping[mapped[0]] =  mapped[1]


        text_template = ""
        with open(f'{_SCRIPT_PATH}/cpp_to_json_string_template.jinja2', "r") as file:
            text_template = file.read()

        environment = jinja2.Environment()
        template = environment.from_string(text_template)
        text = template.render(
            from_class = from_class,
            to_class = to_class,
            function_name = "convert",
            conversion_mapping = conversion_mapping

        )
        return textwrap.dedent(text)

        return ""