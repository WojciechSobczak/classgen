from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen import FieldDescriptor
from classgen.cpp.cpp_type import CPPType

class CPPFieldDescriptor(FieldDescriptor):

    def __init__(self, 
        static: bool = False, 
        const: bool = False,
        constexpr: bool = False,
        access: CPPAccessModifier = CPPAccessModifier.PUBLIC, 
        value: str | int | float | None = None
    ) -> None:
        self.static = static
        self.access = access
        self.const = const
        self.constexpr = constexpr
        self.value = value
