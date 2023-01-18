import ast
import os

class FieldDescriptor:
    def __init__(self, **kwargs) -> None:
        pass

class CodegenClass:
    def __init__(self, name: str) -> None:
        self.name = name
        pass

class CodegenField:
    def __init__(self, name: str) -> None:
        self.name = name
        pass

class ASTParser:
    def parse(self, clazz: ast.ClassDef) -> CodegenClass:
        return None

class CodeGenerator:
    def generate_code(self, clazz: CodegenClass, additional_generators: list['CodeGenerator'] = None) -> str:
        return ""
    
def extract_classes(file_path: str, parser: ASTParser) -> list[CodegenClass]:
    classes: list[CodegenClass]= []
    with open(file_path, mode="r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
        for elem in tree.body:
            if type(elem) == ast.ClassDef:
                classes.append(parser.parse(elem))
    return classes



