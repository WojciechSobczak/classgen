import dataclasses
from classgen.cpp.cpp_standard_type import CPPStandardCollection, CPPStandardType


@dataclasses.dataclass
class CPPTemplatedType:
    target_type: CPPStandardType | CPPStandardCollection | str
    args: list[CPPStandardType | type | str]

    def __str__(self) -> str:
        return f'{self.target_type}<{",".join(self.args)}>'