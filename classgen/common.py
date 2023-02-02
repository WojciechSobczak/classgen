import ast
import dataclasses
import os
class FieldDescriptor:
    def __init__(self, **kwargs) -> None:
        pass
    
class Class:
    def __init__(self, name: str) -> None:
        self.name = name

class Field:
    def __init__(self, name: str) -> None:
        self.name = name
@dataclasses.dataclass
class ExtractedClass:
    class_def: ast.ClassDef
    relative_path: str

def extract_classes(class_path_or_classes_path: str) -> list[ExtractedClass]:
    classes: list[ExtractedClass] = []
    files_to_parse = []
    if os.path.isfile(class_path_or_classes_path):
        files_to_parse.append(class_path_or_classes_path)
    else:
        for directory_path, directory_names, file_names in os.walk(class_path_or_classes_path, topdown=True, followlinks=False):
            for file_name in file_names:
                if file_name.endswith('.py'):
                    files_to_parse.append(os.path.join(directory_path, file_name))

    print("KASZTAŃSTKO")
    for file_path in files_to_parse:
        with open(file_path, mode="r", encoding="utf-8") as file:
            tree = ast.parse(file.read())
            for elem in tree.body:
                if type(elem) == ast.ClassDef:
                    classes.append(ExtractedClass(elem, os.path.relpath(class_path_or_classes_path, file_path)))
    return classes
