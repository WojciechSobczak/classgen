import dataclasses
from classgen.common import Field, FieldDescriptor
from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_field_descriptor import CPPFieldDescriptor
from classgen.cpp.cpp_type import CPPType
from classgen.cpp.cpp_standard_types import CPPDouble, CPPMap, CPPString, CPPTemplatedType, extract_templated_type, from_python_type, is_python_type, is_standard_type, is_templated_type
from classgen.utils import assert_type

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
        elif is_templated_type(field.field_type):
            _type = extract_templated_type(field.field_type)
        elif is_standard_type(field.field_type): 
            _type = field.field_type()
        else:
            include = field.field_type.__mro__[0].__name__
            include = '/'.join(include.split('.')) + '.hpp'
            _type = CPPType(field.field_type.__name__, include)


        if field.field_descriptor != None:
            field_descriptor = field.field_descriptor
            if type(field_descriptor) == CPPFieldDescriptor:
                field_descriptor: CPPFieldDescriptor = field_descriptor
                return CPPField(
                    name = field.name,
                    type = _type,
                    static = field_descriptor.static,
                    const = field_descriptor.const,
                    constexpr = field_descriptor.constexpr,
                    access_modifier = field_descriptor.access,
                    value = field_descriptor.value
                )
            elif type(field_descriptor) == FieldDescriptor:
                return CPPField(
                    name = field.name,
                    type = _type,
                    static = field_descriptor.get_field('static', False),
                    const = field_descriptor.get_field('const', False),
                    constexpr = field_descriptor.get_field('constexpr', False),
                    access_modifier = field_descriptor.get_field('access', CPPAccessModifier.PUBLIC),
                    value = field_descriptor.get_field('value', None)
                )
            else:
                raise Exception('CPPField can only be created from FieldDescriptor or CPPFieldDescriptor')
            
        return CPPField(
            name = field.name,
            type = _type,
            static = False,
            const = False,
            constexpr = False,
            access_modifier = CPPAccessModifier.PUBLIC,
            value = None
        )
        
    @staticmethod
    def from_basic_fields(fields: list[Field]) -> list['CPPField']:
        return [CPPField.from_basic_field(field) for field in fields]