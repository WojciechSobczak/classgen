

import dataclasses

@dataclasses.dataclass
class CPPEnumField:
    name: str
    value: int | str | dict[str, str | int | float] = None

@dataclasses.dataclass
class CPPEnum:
    name: str
    fields: list[CPPEnumField]





