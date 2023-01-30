import ast
import dataclasses

from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_templated_type import CPPTemplatedType
from classgen.cpp.cpp_standard_type import CPPStandardType, CPPStandardCollection
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_class import CPPClass

from classgen.ast_parser import ASTParser
from classgen.enum import Enum
from classgen.enum_ast_parser import EnumASTParser

class CPPASTParser(ASTParser):

    def _try_parse_standard_type(self, expression: ast.expr) -> CPPStandardType | None:
        ###Variables just to catch naming error in match clause
        from classgen import cpp         #pylint: disable=import-outside-toplevel
        long_type: str = CPPStandardType #pylint: disable=unused-variable
        short_type: type = cpp.ST        #pylint: disable=unused-variable

        match expression:
            case ast.Attribute(
                value = ast.Name(
                    id = 'CPPStandardType' | 'ST'
                )
            ): 
                if expression.value.id not in [CPPStandardType.__name__, 'ST']:
                    return None
                
                return CPPStandardType[expression.attr.upper()]
        return None

    def _try_parse_constant(self, expression: ast.expr) -> str | None:
        match expression:
            case ast.Constant:
                return expression.value
        return None
    

    @dataclasses.dataclass
    class _ParseCallResult:
        collection_name: str
        template_args: list[str]

    def _try_parse_templated_collection_call(self, expression: ast.expr) -> _ParseCallResult | None:
        ###Variables just to catch naming error in match clause
        from classgen import cpp                          #pylint: disable=import-outside-toplevel
        template_long_type: str = CPPTemplatedType        #pylint: disable=unused-variable
        template_short_type: type = cpp.TT                #pylint: disable=unused-variable
        collection_long_type: str = CPPStandardCollection #pylint: disable=unused-variable
        collection_short_type: type = cpp.SC              #pylint: disable=unused-variable

        match expression:
            case ast.Call(
                func = ast.Name(
                    id = 'CPPTemplatedType' | 'TT'
                ),
                args = [],
                keywords = [
                    ast.keyword(
                        arg = "type",
                        value = ast.Attribute(
                            value = ast.Name(
                                id = 'CPPStandardCollection' | 'SC',
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
                if expression.func.id not in [CPPTemplatedType.__name__, 'TT']:
                    return None
                if expression.keywords[0].value.value.id not in [CPPStandardCollection.__name__, 'SC']:
                    return None

                parsed_collection_name = expression.keywords[0].value.attr
                parsed_template_args: list[ast.expr] = expression.keywords[1].value.elts

                output_template_args = []
                for arg in parsed_template_args:
                    match arg:
                        case ast.Name(): 
                            output_template_args.append(arg.id) 
                            break
                        case _:
                            raise Exception("_try_parse_call() parsed_template_args wrong type")

                return CPPASTParser._ParseCallResult(parsed_collection_name, output_template_args)
            
        return None

    def _parse_type_expression(self, expression: ast.expr) -> CPPStandardType | CPPTemplatedType | str:
        parse_try = self._try_parse_standard_type(expression)
        if parse_try is not None:
            return parse_try
        
        parse_try = self._try_parse_constant(expression)
        if parse_try is not None:
            return parse_try
                
        if type(expression) == ast.Name:
            expression: ast.Name = expression
            return expression.id
            
        parse_try = self._try_parse_templated_collection_call(expression)
        if parse_try is not None:
            template_target = CPPStandardCollection[parse_try.collection_name.upper()]
            return CPPTemplatedType(template_target, parse_try.template_args)
        
        raise NotImplementedError(f"DIDNT EXPECT _parse_type_expression: {ast.dump(expression)}")
        

    def _parse_access_expression(self, expression: ast.expr) -> CPPAccessModifier:
        match expression:
            case ast.Attribute(
                value = ast.Name(
                    id = 'AccessModifier'
                )
            ):
                return CPPAccessModifier[expression.attr.upper()]
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
        field_type: CPPStandardType | str = ""
        access_modifier = CPPAccessModifier.PUBLIC
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
        assignments = super().extract_fields(class_body)
        fields = []        
        for assignment in assignments:
            field_name = assignment.targets[0].id
            keywords: list[ast.keyword] = assignment.value.keywords
            fields.append(self.extract_field(field_name, keywords))
        return fields
    
    def parse(self, class_def: ast.ClassDef) -> CPPClass | Enum:
        enum_parser = EnumASTParser()
        if enum_parser.is_enum_def(class_def):
            return enum_parser.parse(class_def)
        return CPPClass(
            name=class_def.name, 
            fields=self.extract_fields(class_def.body), 
            include_path=""
        )
