import dataclasses

from classgen.cpp.cpp_type import CPPType
from .cpp_access_modifier import CPPAccessModifier

@dataclasses.dataclass
class CPPField:
    name: str
    type: CPPType
    static: bool
    const: bool
    constexpr: bool
    access_modifier: CPPAccessModifier
    value: str | int | float