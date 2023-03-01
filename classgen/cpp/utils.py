

from classgen.common import Class, Field
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField
from classgen.cassert import assert_one_of_types


def extract_cpp_fields(clazz: Class | CPPClass) -> list[CPPField]:
    assert_one_of_types(clazz, [Class, CPPClass])

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

    return class_fields

def extract_include_from_class(clazz: Class) -> str:
    include = f"{clazz.class_type.__module__}.{clazz.class_type.__name__}"
    #One for folder scan name, second for file name
    include = include.split('.')[2::]
    return '/'.join(include) + '.hpp'