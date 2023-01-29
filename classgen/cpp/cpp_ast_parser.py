
from collections import namedtuple
import dataclasses
import sys

from .cpp_enum import CPPAutoNumericEnumField, CPPComplexEnumField, CPPConstantNumericEnumField, CPPEnum, CPPEnumField
from ..classgen import ASTParser
from .standard_type import StandardType, StandardCollection
from .templated_type import TemplatedType
from .access_modifier import AccessModifier
from .cpp_field import CPPField
from .cpp_class import CPPClass
import ast
import os

class CPPASTParser(ASTParser):

    def _try_parse_standard_type(self, expression: ast.expr) -> StandardType | None:
        match expression:
            case ast.Attribute(
                value = ast.Name(
                    id = 'StandardType' | 'ST'
                )
            ): 
                return StandardType[expression.attr.upper()]
        return None

    def _try_parse_constant(self, expression: ast.expr) -> str | None:
        match expression:
            case ast.Constant(
                value = str
            ):
                return expression.value
        return None
    

    @dataclasses.dataclass
    class _ParseCallResult:
        collection_name: str
        template_args: list[str]

    def _try_parse_call(self, expression: ast.expr) -> _ParseCallResult | None:
        match expression:
            case ast.Call(
                func = ast.Name(
                    id = 'TemplatedType' | 'TT'
                ),
                args = [],
                keywords = [
                    ast.keyword(
                        arg="type",
                        value = ast.Attribute(
                            value = ast.Name(
                                id='StandardCollection' | 'SC',
                            )
                        )
                    ),
                    ast.keyword(
                        arg = "args",
                        value = ast.List(
                            elts = [*_]
                        )
                    )
                ]
            ): 
                parsed_collection_name = expression.keywords[0].value.attr
                parsed_template_args: list[ast.expr] = expression.keywords[1].value.elts

                output_template_args = []
                for arg in parsed_template_args:
                    match arg:
                        case ast.Name(id): 
                            output_template_args.append(arg.id) 
                            break
                        case _:
                            raise Exception("_try_parse_call() parsed_template_args wrong type")

                return CPPASTParser._ParseCallResult(parsed_collection_name, output_template_args)
            
        return None

    def _parse_type_expression(self, expression: ast.expr) -> StandardType | TemplatedType | str:
        parse_try = self._try_parse_standard_type(expression)
        if parse_try is not None:
            return parse_try
        
        parse_try = self._try_parse_constant(expression)
        if parse_try is not None:
            return parse_try
                
        if type(expression) == ast.Name:
            expression: ast.Name = expression
            return expression.id
            
        parse_try = self._try_parse_call(expression)
        if parse_try is not None:
            template_target = StandardCollection[parse_try.collection_name.upper()]
            return TemplatedType(template_target, parse_try.template_args)
        
        raise NotImplementedError(f"DIDNT EXPECT _parse_type_expression: {expression}")
        

    def _parse_access_expression(self, expression: ast.expr) -> AccessModifier:
        match expression:
            case ast.Attribute(
                value = ast.Name(
                    id = 'AccessModifier'
                ),
                attr = str
            ):
                return AccessModifier[expression.attr.upper()]
        raise NotImplementedError("DIDNT EXPECT _parse_access_expression")
    
    def _parse_static_expression(self, expression: ast.expr) -> bool:
        if type(expression) != ast.Constant:
            raise Exception("Wrong static type")
        expression: ast.Constant = expression
        constant_value = expression.value
        if type(constant_value) != bool:
            raise Exception("Wrong static constant_value type")
        return constant_value

    def extract_field(self, name: str, keywords: list[ast.keyword]):
        field_type: StandardType | str = ""
        access_modifier = AccessModifier.PUBLIC
        static = False

        for keyword in keywords:
            argument_name = keyword.arg
            if argument_name == "type":
                field_type = self._parse_type_expression(keyword.value)
            if argument_name == "access":
                access_modifier = self._parse_access_expression(keyword.value)
            if argument_name == "static":
                static = self._parse_static_expression(keyword.value)

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
    


    def extract_enum_simple_fields(self, class_body: list[ast.stmt]) -> list[CPPEnumField]:
        fields: list[CPPEnumField] = []
        for assign in class_body:
            match assign:
                case ast.Assign(
                    targets = [
                        ast.Name(id)
                    ],
                    value = ast.Constant()
                ): 
                    constant: ast.Constant = assign.value
                    fields.append(CPPConstantNumericEnumField(id, constant.value))
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
                    fields.append(CPPAutoNumericEnumField(id))
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
                    fields.append(CPPAutoNumericEnumField(id))
        return fields
    
    def extract_enum_complex_fields(self, class_body: list[ast.stmt]) -> list[CPPEnumField]:
        fields: list[CPPEnumField] = []
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
                    fields.append(CPPComplexEnumField(id, arguments))
        return fields

    def extract_enum_field(self, class_body: list[ast.stmt]) -> list[CPPEnumField]:
        simple_fields = self.extract_enum_simple_fields(class_body)
        complex_fields = self.extract_enum_complex_fields(class_body)
        if len(simple_fields) != 0 and len(complex_fields):
            raise Exception("Enum supports only simple or only complex types, not both")
        return simple_fields if len(simple_fields) > 0 else complex_fields
        

        
    
    def parse(self, clazz: ast.ClassDef) -> CPPClass | CPPEnum:
        def enum_match():
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
                ): return clazz
                case ast.ClassDef(
                    bases = [
                        ast.Name(
                            id = 'Enum'
                        )
                    ]
                ): return clazz
            return None
        
        matched = enum_match()
        if matched != None:
            return CPPEnum(name=clazz.name, fields=self.extract_enum_field(clazz.body))
        else:
            return CPPClass(name=clazz.name, fields=self.extract_fields(clazz.body), include_path="")
