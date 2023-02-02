from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen import FieldDescriptor
from classgen.cpp.cpp_type import CPPType

class CPPFieldDescriptor(FieldDescriptor):

    def __init__(self, 
        static: bool = False, 
        access: CPPAccessModifier = CPPAccessModifier.PUBLIC, 
        field_type: CPPType = None
    ) -> None:
        self.static = static
        self.access = access
        self.field_type = field_type
        if self.field_type == None:
            raise Exception("Type must be specified")