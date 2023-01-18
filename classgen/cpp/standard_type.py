import enum

class StandardType(enum.Enum):
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
            case StandardType.INT8: return "int8_t"
            case StandardType.INT16: return "int16_t"
            case StandardType.INT32: return "int32_t"
            case StandardType.INT64: return "int64_t"
            case StandardType.UINT8: return "uint8_t"
            case StandardType.UINT16: return "uint16_t"
            case StandardType.UINT32: return "uint32_t"
            case StandardType.UINT64: return "uint64_t"
            case StandardType.STRING: return "std::string" 
            case StandardType.STRING_VIEW: return "std::string_view"
            case _: raise Exception("Not handled StandardType::__str__() type")

    def get_include(self) -> str:
        match self:
            case StandardType.INT8: return "inttypes.h"
            case StandardType.INT16: return "inttypes.h"
            case StandardType.INT32: return "inttypes.h"
            case StandardType.INT64: return "inttypes.h"
            case StandardType.UINT8: return "inttypes.h"
            case StandardType.UINT16: return "inttypes.h"
            case StandardType.UINT32: return "inttypes.h"
            case StandardType.UINT64: return "inttypes.h"
            case StandardType.STRING: return "string" 
            case StandardType.STRING_VIEW: return "string_view"
            case _: raise Exception("Not handled StandardType::get_include() type")

    def is_numerical(self) -> bool:
        match self:
            case StandardType.INT8: return True
            case StandardType.INT16: return True
            case StandardType.INT32: return True
            case StandardType.INT64: return True
            case StandardType.UINT8: return True
            case StandardType.UINT16: return True
            case StandardType.UINT32: return True
            case StandardType.UINT64: return True
        return False