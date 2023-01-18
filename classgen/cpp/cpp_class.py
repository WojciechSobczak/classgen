import dataclasses

from ..classgen import CodegenClass

@dataclasses.dataclass
class CPPClass(CodegenClass):
    name: str
    fields: list['CPPField']