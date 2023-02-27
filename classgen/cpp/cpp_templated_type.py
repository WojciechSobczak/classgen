import dataclasses
from classgen.cpp.cpp_type import CPPType

@dataclasses.dataclass(frozen=True)
class CPPTemplatedType(CPPType):
    args: list[CPPType]
    