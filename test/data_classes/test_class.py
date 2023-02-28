import enum
from enum import Enum
from enum import auto


class TestEnumeration(enum.Enum):
    FIRST_VALUE = object(name="tak", kasztan=2)
    SECOND_VALUE = object(name="ptak", kasztan=3)

class SecondEnumeration(Enum):
    THIRD_VALUE = enum.auto()
    FOURTH_VALUE = auto()
    FIFTH_VALUE = 5
