import ast

from classgen.common import Class
from classgen.enum import Enum

class ASTParser:

    def extract_fields(self, class_body: list[ast.stmt]):
        assignments: list[ast.Assign] = []
        for assign in class_body:
            if type(assign) == ast.Assign:
                assignments.append(assign)
        return assignments

    def parse(self, class_def: ast.ClassDef) -> Class | Enum:
        raise Exception("Bare ASTParser does not parse anything")
    