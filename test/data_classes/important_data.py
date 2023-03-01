from classgen import *
from classgen.cpp import *

class DatabaseData:
    id: int = FD(value = 55)
    name: CPPString = FD(value = "")
    country: str = FD(value = "Vinland")

class FocusData:
    focus_group: CPPString
    focus_value: CPPDouble
    focus_checked: CPPBool
    dbData: DatabaseData

#More experimental than normal use case
class TemplateRichData:
    convoluted_unreal: CPPMap[CPPMap[CPPString, CPPDouble], CPPMap[CPPUINT8, CPPSet[CPPString]]]
    convoluted_real: CPPMap[CPPSet[CPPString], CPPMap[CPPUINT8, CPPSet[CPPINT64]]]

class ImportantData:
    id: CPPString = FD(access=CPPAccessModifier.PRIVATE)
    name: CPPStringView = FD(access=CPPAccessModifier.PROTECTED)
    advantage: CPPString = FD(access=CPPAccessModifier.PUBLIC)

    length: CPPFloat
    size: CPPUINT64

    bitmask: CPPINT32 = CPPFD(const=True, value=123)
    bytemask: CPPINT32 = FD(constexpr=True, static=True, value=255)

    private_constant: CPPStringView = FD(access=CPPAccessModifier.PRIVATE, static=True, constexpr = True, value = "IMPORTANT TEXT")
    protected_constant: CPPStringView = FD(access=CPPAccessModifier.PROTECTED, static=True)

    cost_money_map: CPPMap[CPPString, CPPDouble]
    cost_currency_map: CPPMap[CPPString, CPPString]

    countries: CPPSet[CPPString]
    focus_data: FocusData
    













