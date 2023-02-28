import ast
import os
import re
from types import ModuleType


class FieldDescriptor:
    def __init__(self, **kwargs) -> None:
        self.arguments = dict(kwargs)

    def __str__(self) -> str:
        return f'FD({self.arguments})'
    
    def get_field(self, name: str, default = None):
        value = self.arguments.get(name)
        if value != None:
            return value
        if value == None and default != None:
            return default
        return None
    
    
class Field:
    def __init__(self, name: str, field_type: type, field_descriptor: FieldDescriptor) -> None:
        self.name = name
        self.field_descriptor = field_descriptor
        self.field_type = field_type

    def __str__(self) -> str:
        return f'{self.name}(): {self.field_type.__name__} = {self.field_descriptor}'
    
    def __repr__(self) -> str:
        return self.__str__()

class Class:
    def __init__(self, class_type: type, fields: list[Field] = None) -> None:
        self.class_type = class_type
        self.fields = [] if fields is None else fields 

    def __str__(self) -> str:
        return f'{self.class_type.__name__}() = {self.fields}'
    
    def __repr__(self) -> str:
        return self.__str__()
    

def extract_classes(classes_directory: str, calling_script_path: str) -> list[Class]:
    classes_directory = os.path.abspath(classes_directory)

    files_to_parse: list[str] = []
    for directory_path, directory_names, file_names in os.walk(classes_directory, topdown=True, followlinks=False):
        for file_name in file_names:
            if file_name.endswith('.py'):
                python_file_path = os.path.join(directory_path, file_name)
                python_file_path = python_file_path.replace('\\', '/')
                python_file_path = re.sub(r'\/+', '/', python_file_path)
                files_to_parse.append(python_file_path)
    
    types_to_create_classes_from: list[type] = []
    calling_script_path = os.path.abspath(calling_script_path)
    for file_path in files_to_parse:
        our_classes: set[str] = set()
        with open(file_path, "r", encoding="UTF-8") as file:
            definitions = ast.parse(file.read())
            for elem in definitions.body:
                if type(elem) == ast.ClassDef:
                    elem: ast.ClassDef = elem
                    our_classes.add(str(elem.name))

        module_path = file_path[len(calling_script_path) + 1::]
        module_path = module_path.replace('.py', '')
        module_path = module_path.replace('/', '.')
        if module_path == 'data_classes.important_data':
            module: ModuleType = __import__(module_path, fromlist=['object'])
            for module_element in dir(module):
                if module_element in our_classes:
                    types_to_create_classes_from.append(getattr(module, module_element))

    
    extracted_classes: list[Class] = []
    for class_type in types_to_create_classes_from:
        class_fields: list[Field] = []
        class_values = class_type.__dict__
        for name, field_type in class_type.__annotations__.items():
            class_value = class_values.get(name)
            if class_value is not None:
                if not issubclass(type(class_value), FieldDescriptor):
                    raise Exception("Class Fields value must be field descriptors")
                class_fields.append(Field(name, field_type, class_value))
            else:
                class_fields.append(Field(name, field_type, FieldDescriptor()))
        extracted_classes.append(Class(class_type, class_fields))
    return extracted_classes