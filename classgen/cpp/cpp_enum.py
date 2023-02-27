import dataclasses

from classgen.enum import Enum

@dataclasses.dataclass
class CPPEnum(Enum):
    include_path: str