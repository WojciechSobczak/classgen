



import ast
from classgen.common.ast_parser import ASTParser
from classgen.common.enum import AutoNumericEnumField, ComplexEnumField, ConstantNumericEnumField, Enum, EnumField


class EnumASTParser(ASTParser):
    
    def extract_enum_simple_fields(self, class_body: list[ast.stmt]) -> list[EnumField]:
        fields: list[EnumField] = []
        for assign in class_body:
            match assign:
                case ast.Assign(
                    targets = [
                        ast.Name(id)
                    ],
                    value = ast.Constant()
                ): 
                    constant: ast.Constant = assign.value
                    fields.append(ConstantNumericEnumField(id, constant.value))
                case ast.Assign(
                    targets = [
                        ast.Name(id)
                    ],
                    value = ast.Call(
                        func = ast.Name(
                            id = 'auto'
                        )
                    )
                ): 
                    fields.append(AutoNumericEnumField(id))
                case ast.Assign(
                    targets = [
                        ast.Name(id)
                    ],
                    value = ast.Call(
                        func = ast.Attribute(
                            value = ast.Name(
                                id = 'enum'
                            ),
                            attr = 'auto'
                        )
                    )
                ): 
                    fields.append(AutoNumericEnumField(id))
        return fields
    
    def extract_enum_complex_fields(self, class_body: list[ast.stmt]) -> list[EnumField]:
        fields: list[EnumField] = []
        for assign in class_body:
            match assign:
                case ast.Assign(
                    targets = [
                        ast.Name(id)
                    ],
                    value = ast.Call(
                        func = ast.Name(
                            id = 'object',
                        ),
                        keywords = [
                            ast.keyword(), *_
                        ]
                    )
                ): 
                    keywords: list[ast.keyword] = assign.value.keywords
                    arguments: dict[str, str | int | float] = {}
                    for keyword in keywords:
                        match keyword:
                            case ast.keyword(
                                arg,
                                value = ast.Constant()
                            ):
                                constant: ast.Constant = keyword.value
                                arguments[str(keyword.arg)] = constant.value
                    fields.append(ComplexEnumField(id, arguments))
        return fields

    def extract_enum_field(self, class_body: list[ast.stmt]) -> list[EnumField]:
        simple_fields = self.extract_enum_simple_fields(class_body)
        complex_fields = self.extract_enum_complex_fields(class_body)
        if len(simple_fields) != 0 and len(complex_fields):
            raise Exception("Enum supports only simple or only complex types, not both")
        return simple_fields if len(simple_fields) > 0 else complex_fields
    
    def is_enum_def(self, clazz: ast.ClassDef):
        match clazz:
            case ast.ClassDef(
                bases = [
                    ast.Attribute(
                        value = ast.Name(
                            id = 'enum'
                        ),
                        attr = 'Enum'
                    )
                ]
            ): return True
            case ast.ClassDef(
                bases = [
                    ast.Name(
                        id = 'Enum'
                    )
                ]
            ): return True
        return False
    
    def parse(self, clazz: ast.ClassDef) -> Enum:
        if self.is_enum_def(clazz) != None:
            return Enum(name=clazz.name, fields=self.extract_enum_field(clazz.body))
        else:
            raise Exception("Given ast.ClassDef does not match enum definition")















