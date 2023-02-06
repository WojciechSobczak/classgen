import jinja2
import os
import textwrap

from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_standard_types import CPPSet, CPPString, is_numerical, CPPMap, CPPTemplatedType
from classgen.cpp.cpp_type import CPPType
from classgen.jinja_code_generator import JinjaCodeGenerator


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
_MAIN_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_json_string_template.jinja2'
_MAP_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_json_string_map_template.jinja2'
_SET_TEMPLATE_PATH = f'{_SCRIPT_PATH}/cpp_to_json_string_set_template.jinja2'

class CPPToJsonStringGenerator(JinjaCodeGenerator):

    def __init__(self, function_name: str = "toJsonString") -> None:
        super().__init__()
        self.function_name = function_name
        self.map_to_json_template = self.load_template("map", _MAP_TEMPLATE_PATH)
        self.main_template = self.load_template("main", _MAIN_TEMPLATE_PATH)
        self.set_to_json_template = self.load_template("set", _SET_TEMPLATE_PATH)
    
    def setup_environment(self, environment: jinja2.Environment):
        environment.globals.update(get_to_string_value_format = self.get_to_string_value_format)

    def get_to_string_value_format(self, _type: CPPType, field_name: str, field_name_prefix: str = "") -> str:
        if is_numerical(_type):
            return f'std::to_string({field_name_prefix}{field_name})'
        elif type(_type) == CPPString:
            return f'{field_name_prefix}{field_name}'
        elif type(_type) == str or type(_type) == CPPClass:
                return f'{field_name_prefix}{field_name}.{self.function_name}()'
        elif type(_type) == CPPMap:
            return self.map_to_json_string(_type, field_name)
        elif type(_type) == CPPSet:
            return self.set_to_json_string(_type, field_name)
        else:
            return f'std::string({field_name_prefix}{field_name})'

    def map_to_json_string(self, _type: CPPType, field_name: str) -> str:
        if type(_type) != CPPMap:
            raise Exception("map_to_json_string() accepts only CPPMap as type")
        text = self.map_to_json_template.template.render(
            map_name = field_name,
            map_type = _type,
        )
        return text
    
    def set_to_json_string(self, _type: CPPType, field_name: str) -> str:
        if type(_type) != CPPSet:
            raise Exception("set_to_json_string() accepts only CPPSet as type")
        text = self.set_to_json_template.template.render(
            set_name = field_name,
            set_type = _type
        )
        return text

    def generate_code(self, clazz: CPPClass):
        if type(clazz) != CPPClass:
            raise Exception("CPPToJsonStringGenerator only supports code generation for CPPClass")
        templated_fields = [field for field in clazz.fields if issubclass(type(field.type), CPPTemplatedType) and not field.static]
        text = self.main_template.template.render(
            function_name = self.function_name,
            templated_fields = templated_fields,
            templated_fields_names = set([field.name for field in templated_fields]),
            all_fields = clazz.fields
        )
        return text