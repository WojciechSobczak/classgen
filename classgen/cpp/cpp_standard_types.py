from dataclasses import dataclass
from classgen.cpp.cpp_templated_type import CPPTemplatedType

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

@dataclass(frozen = True)
class CPPVector(CPPTemplatedType):
    def __init__(self, args: list[CPPType]):
        super().__init__("std::vector", "vector", args) #pylint: disable=too-many-function-args

@dataclass(frozen = True)
class CPPMap(CPPTemplatedType):
    def __init__(self, args: list[CPPType]):
        super().__init__("std::map", "map", args) #pylint: disable=too-many-function-args

    @property
    def key_type(self) -> CPPType:
        return self.args[0]
    
    @property
    def value_type(self) -> CPPType:
        return self.args[1]

@dataclass(frozen = True)
class CPPSet(CPPTemplatedType):
    def __init__(self, args: list[CPPType]):
        super().__init__("std::set", "set", args) #pylint: disable=too-many-function-args

    @property
    def value_type(self) -> CPPType:
        return self.args[0]

def is_numerical_type(_type: type) -> bool:
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
    print(_type)
    return _type in SET

def is_standard_type(_type: type) -> bool:
    if is_numerical_type(_type):
        return True
    SET = {
        CPPBool,
        CPPString,
        CPPStringView,
        CPPVector,
        CPPMap,
        CPPSet
    }
    return _type in SET

def from_python_type(_type: type) -> CPPType:
    value = {
        str: CPPString,
        int: CPPINT64,
        float: CPPDouble
    }.get(_type)

    if value == None:
        raise Exception(f"Python type of: {type(_type).__name__} is not currently supported")
    return value()
        
def is_python_type(_type: type) -> bool:
    SET = {
        str,
        int,
        float
    }
    return _type in SET