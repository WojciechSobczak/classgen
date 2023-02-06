from typing import Any


def is_or_inherits_from(value, _type: type) -> bool:
    return type(value) == _type or type(value).__bases__.__contains__(_type)

def is_one_of(value: Any, types: list[type]) -> bool:
    for _type in types:
        if type(value) == _type:
            return True
    return False

def set_if_none(value_to_check, value_to_set):
    if value_to_check is None:
        value_to_check = value_to_set
