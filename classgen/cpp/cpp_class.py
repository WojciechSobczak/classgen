import dataclasses

from classgen import Class

@dataclasses.dataclass
class CPPClass(Class):
    name: str
    include_path: str
    fields: list['CPPField']