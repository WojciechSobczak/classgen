import dataclasses
from .standard_type import StandardType
from .access_modifier import AccessModifier
from .cpp_class import CPPClass

@dataclasses.dataclass
class CPPField:
    name: str
    type: StandardType | CPPClass | str
    static: bool
    access_modifier: AccessModifier