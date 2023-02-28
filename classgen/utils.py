from typing import Any

from classgen.common import Class, Field
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField

def assert_one_of(value: Any, types: list[type]) -> bool:
    for _type in types:
        if type(value) == _type:
            return True
    raise Exception(f'is_one_of(): type of {value} does not match any of {types}')
