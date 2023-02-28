

import jinja2
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_standard_types import CPPBool, CPPDouble, CPPFloat, CPPMap, CPPSet, CPPString, CPPStringView, CPPTemplatedType, extract_templated_type, is_numerical_type, is_templated_type
from classgen.cpp.cpp_type import CPPType
from classgen.jinja_code_generator import JinjaCodeGenerator


class CPPJinjaCodeGenerator(JinjaCodeGenerator):

    def __init__(self, all_defined_classes: dict[str, CPPClass] = None) -> None:
        super().__init__()
        self.all_defined_classes = None if all_defined_classes == None else all_defined_classes
    
    def setup_environment(self, environment: jinja2.Environment):

        def is_type(_type: type | CPPType, desired_type: type):
            if isinstance(_type, CPPField):
                return type(_type.type) == desired_type
            if isinstance(_type, CPPType):
                return type(_type) == desired_type
            return _type == desired_type

        def is_map(_type: type | CPPType):
            return is_type(_type, CPPMap)
        
        def is_set(_type: type):
            return is_type(_type, CPPSet)
        
        def is_user_defined(_type: CPPType):
            return _type.name in self.all_defined_classes
        
        def is_templated(_type: CPPType) -> bool:
            return issubclass(type(_type), CPPTemplatedType)

        environment.globals.update(
            is_templated = is_templated,
            is_map = is_map,
            is_set = is_set,
            is_string = lambda _type: is_type(_type, CPPString),
            is_bool = lambda _type: is_type(_type, CPPBool),
            is_double = lambda _type: is_type(_type, CPPDouble),
            is_float = lambda _type: is_type(_type, CPPFloat),
            is_floating_point = lambda _type: is_type(_type, CPPFloat) or is_type(_type, CPPDouble),
            is_str_or_class = lambda _type: is_type(_type, str) or is_type(_type, CPPClass),
            is_string_view = lambda _type: is_type(_type, CPPStringView),
            is_numerical = lambda _type: is_numerical_type(type(_type)),
            is_user_defined = is_user_defined
        )
        environment.undefined = jinja2.StrictUndefined