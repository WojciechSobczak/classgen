import ast

class FieldDescriptor:
    def __init__(self, **kwargs) -> None:
        pass
    
class Class:
    def __init__(self, name: str) -> None:
        self.name = name

class Field:
    def __init__(self, name: str) -> None:
        self.name = name

def extract_classes(file_path: str) -> list[ast.ClassDef]:
    classes: list[ast.ClassDef] = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
        for elem in tree.body:
            if type(elem) == ast.ClassDef:
                classes.append(elem)
    return classes
