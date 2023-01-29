

import dataclasses

@dataclasses.dataclass
class CPPEnumField:
    name: str

@dataclasses.dataclass
class CPPAutoNumericEnumField(CPPEnumField):
    pass
@dataclasses.dataclass
class CPPConstantNumericEnumField(CPPEnumField):
    value: int

@dataclasses.dataclass
class CPPComplexEnumField(CPPEnumField):
    value: dict[str, int | str | float]

@dataclasses.dataclass
class CPPEnum:
    name: str
    fields: list[CPPEnumField]





