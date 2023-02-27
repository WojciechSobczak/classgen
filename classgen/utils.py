from typing import Any


def is_or_inherits_from(value, _type: type) -> bool:
    return type(value) == _type or type(value).__bases__.__contains__(_type)

def is_one_of(value: Any, types: list[type]) -> bool:
    for _type in types:
        if type(value) == _type:
            return True
    return False

# def assert_type(value: Any, _type: type) -> bool:
#     if type(_type) != type:
#         raise Exception('check_type() requires type as second argument')
#     if type(value) != _type:
#         raise Exception(f'check_type(): type of {value} does not match {_type.__name__}')

def set_if_none(value_to_check, value_to_set):
    if value_to_check is None:
        value_to_check = value_to_set
