import enum
import dataclasses
from classgen.cpp.cpp_templated_type import CPPTemplatedType

from classgen.cpp.cpp_type import CPPType

@dataclasses.dataclass
class CPPINT8(CPPType):
    def __init__(self):
        super().__init__("int8_t", "inttypes.h")

@dataclasses.dataclass
class CPPINT16(CPPType):
    def __init__(self):
        super().__init__("int16_t", "inttypes.h")

@dataclasses.dataclass
class CPPINT32(CPPType):
    def __init__(self):
        super().__init__("int32_t", "inttypes.h")

@dataclasses.dataclass
class CPPINT64(CPPType):
    def __init__(self):
        super().__init__("int64_t", "inttypes.h")

@dataclasses.dataclass
class CPPUINT8(CPPType):
    def __init__(self):
        super().__init__("uint8_t", "inttypes.h")

@dataclasses.dataclass
class CPPUINT16(CPPType):
    def __init__(self):
        super().__init__("uint16_t", "inttypes.h")

@dataclasses.dataclass
class CPPUINT32(CPPType):
    def __init__(self):
        super().__init__("uint32_t", "inttypes.h")

@dataclasses.dataclass
class CPPUINT64(CPPType):
    def __init__(self):
        super().__init__("uint64_t", "inttypes.h")

@dataclasses.dataclass
class CPPFloat(CPPType):
    def __init__(self):
        super().__init__("float")

@dataclasses.dataclass
class CPPDouble(CPPType):
    def __init__(self):
        super().__init__("double")

@dataclasses.dataclass
class CPPString(CPPType):
    def __init__(self):
        super().__init__("std::string", "string")

@dataclasses.dataclass
class CPPStringView(CPPType):
    def __init__(self):
        super().__init__("std::string_view", "string_view")

@dataclasses.dataclass
class CPPVector(CPPTemplatedType):
    def __init__(self, args: list[CPPType]):
        super().__init__("std::vector", "vector", args)

@dataclasses.dataclass
class CPPMap(CPPTemplatedType):
    def __init__(self, args: list[CPPType]):
        super().__init__("std::map", "map", args)

@dataclasses.dataclass
class CPPSet(CPPTemplatedType):
    def __init__(self, args: list[CPPType]):
        super().__init__("std::set", "set", args)


def is_numerical(_type: type) -> bool:
    match _type:
        case CPPINT8(): return True
        case CPPINT16(): return True
        case CPPINT32(): return True
        case CPPINT64(): return True
        case CPPUINT8(): return True
        case CPPUINT16(): return True
        case CPPUINT32(): return True
        case CPPUINT64(): return True
        case CPPFloat(): return True
        case CPPDouble(): return True
    return False

def is_standard(_type: type):
    if is_numerical(_type):
        return True
    match _type:
        case CPPString(): return True
        case CPPStringView(): return True
        case CPPVector(): return True
        case CPPMap(): return True
        case CPPSet(): return True
    return False



_STRINGS = set([
    'CPPINT8',
    'CPPINT16',
    'CPPINT32',
    'CPPINT64',
    'CPPUINT8',
    'CPPUINT16',
    'CPPUINT32',
    'CPPUINT64',
    'CPPFloat',
    'CPPDouble',
    'CPPString',
    'CPPStringView',
    'CPPVector',
    'CPPMap',
    'CPPSet',
])

_CONVERSION_MAP = {
    'CPPINT8': CPPINT8,
    'CPPINT16': CPPINT16,
    'CPPINT32': CPPINT32,
    'CPPINT64': CPPINT64,
    'CPPUINT8': CPPUINT8,
    'CPPUINT16': CPPUINT16,
    'CPPUINT32': CPPUINT32,
    'CPPUINT64': CPPUINT64,
    'CPPFloat': CPPFloat,
    'CPPDouble': CPPDouble,
    'CPPString': CPPString,
    'CPPStringView': CPPStringView,
    'CPPVector': CPPVector,
    'CPPMap': CPPMap,
    'CPPSet': CPPSet,
}

def get_types_as_strings():
    return _STRINGS

def get_type_from_strings(type_name: str) -> type:
    return _CONVERSION_MAP[type_name]