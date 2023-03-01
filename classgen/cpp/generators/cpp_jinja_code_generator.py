

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

    def _is_templated(self, _type: CPPType) -> bool:
        return issubclass(type(_type), CPPTemplatedType)
    
    def _is_type(self, _type: type | CPPType, desired_type: type):
        if isinstance(_type, CPPField):
            return type(_type.type) == desired_type
        if isinstance(_type, CPPType):
            return type(_type) == desired_type
        return _type == desired_type

    def _format_field_type(self, field_type: CPPType):
        if self._is_templated(field_type) == False:
            return field_type.name
        field_type: CPPTemplatedType = field_type
        arguments: list[str] = []
        for arg in field_type.args:
            arguments.append(self._format_field_type(arg))

        return f"{field_type.name}<{', '.join(arguments)}>"
    
    def setup_environment(self, environment: jinja2.Environment):
        def is_map(_type: type | CPPType):
            return self._is_type(_type, CPPMap)
        
        def is_set(_type: type):
            return self._is_type(_type, CPPSet)
        
        def is_user_defined(_type: CPPType):
            return _type.name in self.all_defined_classes

        environment.globals.update(
            is_templated = self._is_templated,
            is_map = is_map,
            is_set = is_set,
            is_string = lambda _type: self._is_type(_type, CPPString),
            is_bool = lambda _type: self._is_type(_type, CPPBool),
            is_double = lambda _type: self._is_type(_type, CPPDouble),
            is_float = lambda _type: self._is_type(_type, CPPFloat),
            is_floating_point = lambda _type: self._is_type(_type, CPPFloat) or self._is_type(_type, CPPDouble),
            is_str_or_class = lambda _type: self._is_type(_type, str) or self._is_type(_type, CPPClass),
            is_string_view = lambda _type: self._is_type(_type, CPPStringView),
            is_numerical = lambda _type: is_numerical_type(type(_type)),
            is_user_defined = is_user_defined,
            format_field_type = self._format_field_type
        )
        environment.undefined = jinja2.StrictUndefined