import ast


class FieldDescriptor:
    def __init__(self, **kwargs) -> None:
        pass

    
class Class:
    def __init__(self, name: str) -> None:
        self.name = name

class Enum:
    def __init__(self, name: str) -> None:
        self.name = name


class Field:
    def __init__(self, name: str) -> None:
        self.name = name


class SelfConversionDescriptor:
    def __init__(self, to_class: type) -> None:
        self.to_class = to_class


class ConversionDescriptor:
    def __init__(self, from_class: type, to_class: type) -> None:
        self.from_class = from_class
        self.to_class = to_class


class ASTParser:
    def parse(self, clazz: ast.ClassDef) -> Class:
        return None


class ConversionMap:
    def __init__(self, field_mapping: dict[Field, Field] = None, renaming_mapping: dict[str, str] = None) -> str:
        self.fieldMapping = {} if field_mapping is None else field_mapping
        self.renaming_mapping = {} if renaming_mapping is None else renaming_mapping


class ConversionGenerator:
    def generate_conversion(self, from_class: Class, to_class: Class) -> str:
        return ""

    def generate_conversion(self, from_class: Class, to_class: Class, mapping: ConversionMap) -> str:
        return ""


class CodeGenerator:
    def generate_code(self, clazz: Class | Enum, additional_generators: list['CodeGenerator'] = None) -> str:
        return ""


def extract_classes(file_path: str, parser: ASTParser) -> list[Class]:
    classes: list[Class] = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
        for elem in tree.body:
            if type(elem) == ast.ClassDef:
                classes.append(parser.parse(elem))
    return classes
