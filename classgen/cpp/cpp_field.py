import dataclasses
from typing import assert_type
from classgen.common import Field
from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_type import CPPType
from classgen.cpp.cpp_standard_types import CPPDouble, CPPMap, CPPString, CPPTemplatedType, extract_templated_type, from_python_type, is_python_type, is_standard_type, is_templated_type

@dataclasses.dataclass
class CPPField:
    name: str
    type: CPPType
    static: bool
    const: bool
    constexpr: bool
    access_modifier: CPPAccessModifier
    value: str | int | float | None


    @staticmethod
    def from_basic_field(field: Field) -> list['CPPField']:
        assert_type(field, Field)

        _type = None
        if is_python_type(field.field_type):
            _type = from_python_type(field.field_type)
        elif is_standard_type(field.field_type): 
            if is_templated_type(field.field_type):
                _type = extract_templated_type(field.field_type)
            else:
                _type = field.field_type()
        else:
            include = field.field_type.__mro__[0].__name__
            include = '/'.join(include.split('.')) + '.hpp'
            _type = CPPType(field.field_type.__name__, include)

        field_descriptor = field.field_descriptor

        return CPPField(
            name = field.name,
            type = _type,
            static = field_descriptor.static,
            const = field_descriptor.const,
            constexpr = field_descriptor.constexpr,
            access_modifier = field_descriptor.access_modifier,
            value = field_descriptor.value
        )
        
    @staticmethod
    def from_basic_fields(fields: list[Field]) -> list['CPPField']:
        return [CPPField.from_basic_field(field) for field in fields]