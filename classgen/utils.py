import traceback
from typing import Any

def assert_one_of(value: Any, types: list[type]) -> bool:
    for _type in types:
        if type(value) == _type:
            return True
    raise Exception(f'is_one_of(): type of {value} does not match any of {types}')

def assert_type(value: Any, desired_type: type) -> bool:
    if value == None:
        print("Bad 'value' argument passed into assert_type(). Must not be None ")
        traceback.print_stack()
        exit(0xFFFFFFFF) 

    if desired_type == None or type(value) != desired_type:
        print("Bad 'desired_type' argument passed into assert_type(). Must not be None and have 'type' type. Current type: ", type(value))
        traceback.print_stack()
        exit(0xFFFFFFFF)
