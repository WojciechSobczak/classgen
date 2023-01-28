import dataclasses
from classgen.cpp.standard_type import StandardCollection, StandardType


@dataclasses.dataclass
class TemplatedType:
    target_type: StandardType | StandardCollection | str
    args: list[StandardType | type | str]

    def __str__(self) -> str:
        return f'{self.target_type}<{",".join(self.args)}>'