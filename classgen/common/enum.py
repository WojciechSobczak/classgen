

import dataclasses

@dataclasses.dataclass
class EnumField:
    name: str

@dataclasses.dataclass
class AutoNumericEnumField(EnumField):
    pass
@dataclasses.dataclass
class ConstantNumericEnumField(EnumField):
    value: int

@dataclasses.dataclass
class ComplexEnumField(EnumField):
    value: dict[str, int | str | float]

@dataclasses.dataclass
class Enum:
    name: str
    fields: list[EnumField]





