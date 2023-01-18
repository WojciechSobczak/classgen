
from ..classgen import ASTParser
from .standard_type import StandardType
from .access_modifier import AccessModifier
from .cpp_field import CPPField
from .cpp_class import CPPClass
import ast
import os

class CPPASTParser(ASTParser):
    def extract_field(self, name: str, keywords: list[ast.keyword]):
        field_type: StandardType | str = ""
        access_modifier = AccessModifier.PUBLIC
        static = False

        for keyword in keywords:
            argument_name = keyword.arg
            if argument_name == "type":
                if type(keyword.value) != ast.Attribute and type(keyword.value) != ast.Constant:
                    raise Exception("Wrong type type")
                argument_value: ast.Attribute = keyword.value
                argument_value_name: ast.Name = argument_value.value
                if type(keyword.value) == ast.Attribute:
                    if argument_value_name.id == 'StandardType':
                        field_type = StandardType[argument_value.attr.upper()]
                    elif argument_value_name.id == 'str':
                        field_type = argument_value.attr
                    else:
                        raise Exception("Wrong type argument_value_name type")
                if type(keyword.value) == ast.Constant:
                    constant_value = argument_value.value
                    if type(constant_value) != str:
                        raise Exception("Wrong type constant_value type")
                    field_type = constant_value
                    
            if argument_name == "access":
                if type(keyword.value) != ast.Attribute:
                    raise Exception("Wrong access type")
                argument_value: ast.Attribute = keyword.value
                argument_value_name: ast.Name = argument_value.value
                if type(keyword.value) == ast.Attribute:
                    if argument_value_name.id == 'AccessModifier':
                        access_modifier = AccessModifier[argument_value.attr.upper()]
                    else:
                        raise Exception("Wrong access argument_value_name type")
                    
            if argument_name == "static":
                if type(keyword.value) != ast.Constant:
                    raise Exception("Wrong static type")
                argument_value: ast.Constant = keyword.value
                constant_value = argument_value.value
                if type(constant_value) != bool:
                    raise Exception("Wrong static constant_value type")
                static = constant_value

        return CPPField(
            name = name,
            type = field_type,
            static = static,
            access_modifier = access_modifier
        )

    def extract_fields(self, class_body: list[ast.stmt]):
        assignments: list[ast.Assign] = []
        for assign in class_body:
            if type(assign) == ast.Assign:
                assignments.append(assign)
        fields = []        
        for assignment in assignments:
            field_name = assignment.targets[0].id
            keywords: list[ast.keyword] = assignment.value.keywords
            fields.append(self.extract_field(field_name, keywords))
        return fields
    
    def parse(self, clazz: ast.ClassDef) -> CPPClass:
        return CPPClass(clazz.name, self.extract_fields(clazz.body))
