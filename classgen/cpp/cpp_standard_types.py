from dataclasses import dataclass
from typing import Generic, TypeVar, assert_type
from classgen.cpp.cpp_type import CPPType

@dataclass(frozen = True)
class CPPINT8(CPPType):
    def __init__(self):
        super().__init__("int8_t", "inttypes.h")

@dataclass(frozen = True)
class CPPINT16(CPPType):
    def __init__(self):
        super().__init__("int16_t", "inttypes.h")

@dataclass(frozen = True)
class CPPINT32(CPPType):
    def __init__(self):
        super().__init__("int32_t", "inttypes.h")

@dataclass(frozen = True)
class CPPINT64(CPPType):
    def __init__(self):
        super().__init__("int64_t", "inttypes.h")

@dataclass(frozen = True)
class CPPUINT8(CPPType):
    def __init__(self):
        super().__init__("uint8_t", "inttypes.h")

@dataclass(frozen = True)
class CPPUINT16(CPPType):
    def __init__(self):
        super().__init__("uint16_t", "inttypes.h")

@dataclass(frozen = True)
class CPPUINT32(CPPType):
    def __init__(self):
        super().__init__("uint32_t", "inttypes.h")

@dataclass(frozen = True)
class CPPUINT64(CPPType):
    def __init__(self):
        super().__init__("uint64_t", "inttypes.h")

@dataclass(frozen = True)
class CPPFloat(CPPType):
    def __init__(self):
        super().__init__("float", None)

@dataclass(frozen = True)
class CPPDouble(CPPType):
    def __init__(self):
        super().__init__("double", None)

@dataclass(frozen = True)
class CPPBool(CPPType):
    def __init__(self):
        super().__init__("bool", None)

@dataclass(frozen = True)
class CPPString(CPPType):
    def __init__(self):
        super().__init__("std::string", "string")

@dataclass(frozen = True)
class CPPStringView(CPPType):
    def __init__(self):
        super().__init__("std::string_view", "string_view")

@dataclass(frozen=True)
class CPPTemplatedType(CPPType):
    args: list[CPPType]


CPPVectorValue = TypeVar("CPPVectorValue")

@dataclass(frozen = True)
class CPPVector(CPPTemplatedType, Generic[CPPVectorValue]):
    def __init__(self, arg: CPPType):
        super().__init__("std::vector", "vector", [arg]) #pylint: disable=too-many-function-args

CPPMapKey = TypeVar("CPPMapKey")
CPPMapValue = TypeVar("CPPMapValue")

@dataclass(frozen = True)
class CPPMap(CPPTemplatedType, Generic[CPPMapKey, CPPMapValue]):
    def __init__(self, key: CPPType, value: CPPType):
        super().__init__("std::map", "map", [key, value]) #pylint: disable=too-many-function-args

    @property
    def key_type(self) -> CPPType:
        return self.args[0]
    
    @property
    def value_type(self) -> CPPType:
        return self.args[1]
    
    def __hash__(self):
        return hash((self.name, self.include_path, tuple(self.args)))

CPPSetValue = TypeVar("CPPSetValue")

@dataclass(frozen = True)
class CPPSet(CPPTemplatedType, Generic[CPPSetValue]):
    def __init__(self, arg: CPPType):
        super().__init__("std::set", "set", [arg]) #pylint: disable=too-many-function-args

    @property
    def value_type(self) -> CPPType:
        return self.args[0]
    
    def __hash__(self):
        return hash((self.name, self.include_path, tuple(self.args)))

def is_numerical_type(_type: type) -> bool:
    assert_type(_type, type)

    SET = {
        CPPINT8,
        CPPINT16,
        CPPINT32,
        CPPINT64,
        CPPUINT8,
        CPPUINT16,
        CPPUINT32,
        CPPUINT64,
        CPPFloat,
        CPPDouble
    }

    return _type in SET

def is_standard_type(_type: type) -> bool:
    assert_type(_type, type)

    if is_numerical_type(_type) or is_templated_type(_type):
        return True
    
    NORMAL_SET = {
        CPPBool,
        CPPString,
        CPPStringView,
    }

    return _type in NORMAL_SET

def is_templated_type(_type: type) -> bool:
    assert_type(_type, type)

    if hasattr(_type, '__origin__') == False or hasattr(_type, '__args__') == False:
        return False

    TEMPLATED_SET = {
        CPPVector,
        CPPMap,
        CPPSet
    }

    return _type.__origin__ in TEMPLATED_SET

def extract_templated_type(_type: type) -> CPPTemplatedType:
    assert_type(_type, type)

    base_class = _type.__origin__
    templated_classes = _type.__args__

    if base_class == CPPMap:
        if len(templated_classes) != 2:
            raise Exception('CPPMap requires 2 arguments')
        return CPPMap(templated_classes[0](), templated_classes[1]())
    
    if base_class == CPPVector:
        if len(templated_classes) != 1:
            raise Exception('CPPVector requires 1 arguments')
        return CPPVector(templated_classes[0]())
    
    if base_class == CPPSet:
        if len(templated_classes) != 1:
            raise Exception('CPPSet requires 1 arguments')
        return CPPSet(templated_classes[0]())

    raise Exception("NOT HANDLED GENERIC") 



def from_python_type(_type: type) -> CPPType:
    value = {
        str: CPPString,
        int: CPPINT64,
        float: CPPDouble,
        bool: CPPBool
    }.get(_type)

    if value == None:
        raise Exception(f"Python type of: {type(_type).__name__} is not currently supported")
    return value()
        
def is_python_type(_type: type) -> bool:
    SET = {
        str,
        int,
        float,
        bool
    }
    return _type in SET