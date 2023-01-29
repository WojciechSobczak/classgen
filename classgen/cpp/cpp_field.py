import dataclasses
from .cpp_standard_type import CPPStandardType
from .cpp_access_modifier import CPPAccessModifier
from .cpp_class import CPPClass

@dataclasses.dataclass
class CPPField:
    name: str
    type: CPPStandardType | CPPClass | str
    static: bool
    access_modifier: CPPAccessModifier