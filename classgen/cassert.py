import traceback
from typing import Any

def _assert(expectation: bool, message: str = None):
    if expectation == False:
        print(message if message is not None else "ASSERTION FAILED")
        traceback.print_stack()
        exit(0xFFFFFFFF)

def assert_one_of_subclasses(value: Any, types: list[type]) -> bool:
    _assert(value != None, "assert_one_of_subclasses(): value == None")
    for _type in types:
        _assert(_type != None, "assert_one_of_subclasses(). One of 'types' is None")
        if issubclass(type(value), _type):
            return
    _assert(False, f"assert_one_of_subclasses() failed with types: {types} against {type(value)}")

def assert_one_of_types(value: Any, types: list[type]) -> bool:
    _assert(value != None, "assert_one_of_types(): value == None")
    for _type in types:
        _assert(_type != None, "assert_one_of_types(). One of 'types' is None")
        if type(value) == _type:
            return
    _assert(False, f"assert_one_of_types() failed with types: {types} against {type(value)}")

def assert_type(value: Any, desired_type: type) -> bool:
    _assert(value != None, "assert_type(): value != None")
    _assert(desired_type != None, "assert_type(): desired_type != None")
    _assert(type(value) == desired_type, f"assert_type(): {type(value)} != {desired_type}")

def assert_subclass(value: Any, desired_type: type) -> bool:
    _assert(value != None, "assert_subclass(): value != None")
    _assert(desired_type != None, "assert_subclass(): desired_type != None")
    _assert(issubclass(type(value), desired_type), f"assert_subclass(): issubclass({type(value)}, {desired_type})")

