

import jinja2
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_standard_types import CPPBool, CPPMap, CPPSet, CPPString, CPPStringView, is_numerical_type
from classgen.jinja_code_generator import JinjaCodeGenerator


class CPPJinjaCodeGenerator(JinjaCodeGenerator):

    def __init__(self, all_defined_classes: dict[str, CPPClass] = None) -> None:
        super().__init__()
        self.all_defined_classes = None if all_defined_classes == None else all_defined_classes
    
    def setup_environment(self, environment: jinja2.Environment):
        environment.globals.update(
            is_map = lambda _type: type(_type) == CPPMap,
            is_set = lambda _type: type(_type) == CPPSet,
            is_string = lambda _type: type(_type) == CPPString,
            is_bool = lambda _type: type(_type) == CPPBool,
            is_str_or_class = lambda _type: type(_type) == str or type(_type) == CPPClass,
            is_string_view = lambda _type: type(_type) == CPPStringView,
            is_numerical = lambda _type: is_numerical_type(type(_type)),
            is_user_defined = lambda _type: self.all_defined_classes.get(str(_type.name)) != None
        )
        environment.undefined = jinja2.StrictUndefined