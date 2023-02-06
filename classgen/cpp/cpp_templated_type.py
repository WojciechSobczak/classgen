import dataclasses
from classgen.cpp.cpp_type import CPPType

@dataclasses.dataclass
class CPPTemplatedType(CPPType):
    args: list[CPPType]
    