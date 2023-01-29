import enum

class CPPStandardType(enum.Enum):
    INT8 = enum.auto()
    INT16 = enum.auto()
    INT32 = enum.auto()
    INT64 = enum.auto()
    UINT8 = enum.auto()
    UINT16 = enum.auto()
    UINT32 = enum.auto()
    UINT64 = enum.auto()
    STRING = enum.auto()
    STRING_VIEW = enum.auto()

    def __str__(self) -> str:
        match self:
            case self.INT8: return "int8_t"
            case self.INT16: return "int16_t"
            case self.INT32: return "int32_t"
            case self.INT64: return "int64_t"
            case self.UINT8: return "uint8_t"
            case self.UINT16: return "uint16_t"
            case self.UINT32: return "uint32_t"
            case self.UINT64: return "uint64_t"
            case self.STRING: return "std::string" 
            case self.STRING_VIEW: return "std::string_view"
            case _: raise Exception("Not handled CPPStandardType::__str__() type")

    def get_include(self) -> str:
        match self:
            case self.INT8: return "inttypes.h"
            case self.INT16: return "inttypes.h"
            case self.INT32: return "inttypes.h"
            case self.INT64: return "inttypes.h"
            case self.UINT8: return "inttypes.h"
            case self.UINT16: return "inttypes.h"
            case self.UINT32: return "inttypes.h"
            case self.UINT64: return "inttypes.h"
            case self.STRING: return "string" 
            case self.STRING_VIEW: return "string_view"
            case _: raise Exception("Not handled CPPStandardType::get_include() type")

    def is_numerical(self) -> bool:
        match self:
            case self.INT8: return True
            case self.INT16: return True
            case self.INT32: return True
            case self.INT64: return True
            case self.UINT8: return True
            case self.UINT16: return True
            case self.UINT32: return True
            case self.UINT64: return True
        return False
    

class CPPStandardCollection(enum.Enum):
    VECTOR = enum.auto()
    MAP = enum.auto()
    SET = enum.auto()

    def __str__(self) -> str:
        match self:
            case self.VECTOR: return "std::vector"
            case self.MAP: return "std::map"
            case self.MAP: return "std::set"
            case _: raise Exception("Not handled CPPStandardCollection::__str__() type")

    def get_include(self) -> str:
        match self:
            case self.VECTOR: return "vector"
            case self.MAP: return "map"
            case self.MAP: return "set"
            case _: raise Exception("Not handled CPPStandardCollection::get_include() type")

