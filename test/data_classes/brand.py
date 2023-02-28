
from classgen import FieldDescriptor
from classgen import FD
from classgen.cpp.cpp_standard_types import CPPMap, CPPString, CPPVector


class Brand:
    m_Logo = FieldDescriptor(type=CPPString)
    m_Name = FD(type=CPPString)

class ProductCategory:
    m_Name = FD(type=CPPString)

class ConcernCategory:
    m_Name = FD(type=CPPString)

class Catalog:
    m_Brands = FD(type=CPPVector[CPPString])
    m_BrandsMap = FD(type=CPPMap[CPPString, CPPString])
