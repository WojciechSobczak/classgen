from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_standard_type import CPPStandardType
from classgen.cpp.cpp_templated_type import CPPTemplatedType
from classgen import FieldDescriptor

class CPPFieldDescriptor(FieldDescriptor):

    def __init__(self, 
        static: bool = False, 
        access: CPPAccessModifier = CPPAccessModifier.PUBLIC, 
        type: CPPStandardType | CPPTemplatedType | str = None
    ) -> None:
        self.static = static
        self.access = access
        self.type = type
        if self.type == None:
            raise Exception("Type must be specified")