from access_modifier import AccessModifier
from ..classgen import FieldDescriptor

class CPPFieldDescriptor(FieldDescriptor):
    def __init__(self, **kwargs) -> None:
        super.__init__(kwargs)
        self.static = kwargs.pop('static', False)
        self.access = kwargs.pop('access', AccessModifier.PUBLIC)
        self.type = kwargs.pop('type', None)
        if self.type == None:
            raise Exception("Type must be specified")