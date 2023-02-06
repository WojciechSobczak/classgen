import ast
import dataclasses
from classgen.common import ExtractedClass

from classgen.cpp.cpp_access_modifier import CPPAccessModifier
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_class import CPPClass

from classgen.ast_parser import ASTParser
from classgen.cpp.cpp_type import CPPType
from classgen.enum import Enum
from classgen.enum_ast_parser import EnumASTParser
from classgen.cpp.cpp_standard_types import get_types_as_strings, get_type_from_strings
from classgen.cpp.cpp_templated_type import CPPTemplatedType

class CPPASTParser(ASTParser):

    def _try_parse_standard_type(self, expression: ast.expr) -> CPPType | None:
        match expression:
            case ast.Name(): 
                type_name = expression.id
                if type_name not in get_types_as_strings():
                    return None
                return get_type_from_strings(type_name)()
        return None

    def _try_parse_constant(self, expression: ast.expr) -> str | None:
        match expression:
            case ast.Constant:
                return expression.value
        return None
    
    def _try_parse_templated_type(self, expression: ast.expr) -> CPPTemplatedType | None:
        #Subscript(value=Name(id='CPPMap', ctx=Load()), slice=Tuple(elts=[Name(id='CPPString', ctx=Load()), Name(id='CPPDouble', ctx=Load())], ctx=Load()), ctx=Load())
        args_list: list[ast.Name] = None
        match expression:
            case ast.Subscript(
                value = ast.Name(),
                slice = ast.Tuple()
            ):
                args_list = expression.slice.elts
                for arg in args_list:
                    if type(arg) != ast.Name:
                        return None
            case ast.Subscript(
                value = ast.Name(),
                slice = ast.Name()
            ):
                args_list = [expression.slice]
                
        if args_list is None:
            return None        

        template_arguments: list[CPPType | str] = []

        for arg in args_list:
            type_from_string = get_type_from_strings(str(arg.id))
            if type_from_string == None:
                template_arguments.append(str(arg.id))
            else:
                template_arguments.append(type_from_string())

        std_base_type = get_type_from_strings(str(expression.value.id))
        if std_base_type is not None:
            if not issubclass(std_base_type, CPPTemplatedType):
                return None
            return_type: CPPTemplatedType = std_base_type(template_arguments)
            return return_type
        
        class_name = str(expression.value.id)
        return CPPTemplatedType(class_name, class_name, template_arguments)

    def _parse_type_expression(self, expression: ast.expr) -> CPPType | str:
        parse_try = self._try_parse_standard_type(expression)
        if parse_try is not None:
            return parse_try
        
        parse_try = self._try_parse_constant(expression)
        if parse_try is not None:
            return parse_try
        
        parse_try = self._try_parse_templated_type(expression)
        if parse_try is not None:
            return parse_try
        
        raise NotImplementedError(f"DIDNT EXPECT _parse_type_expression: {ast.dump(expression)}")
        

    def _parse_access_expression(self, expression: ast.expr) -> CPPAccessModifier:
        match expression:
            case ast.Attribute(
                value = ast.Name(
                    id = 'CPPAccessModifier'
                )
            ):
                return CPPAccessModifier[expression.attr.upper()]
        raise NotImplementedError("DIDNT EXPECT _parse_access_expression")
    
    def _parse_ast_constant_expression(self, expression: ast.expr, name: str) -> bool:
        match expression:
            case ast.Constant(
                value = bool() | int() | float() | str()
            ):
                return expression.value
        raise Exception(f"Wrong ast type from constant: fieldname: '{name}', AST: {ast.dump(expression)}")

    def _parse_static_expression(self, expression: ast.expr) -> bool:
        result = self._parse_ast_constant_expression(expression, "static")
        if type(result) is not bool:
            raise Exception("'static' argument must be boolean")
        return result
    
    def _parse_const_expression(self, expression: ast.expr) -> bool:
        result = self._parse_ast_constant_expression(expression, "const")
        if type(result) is not bool:
            raise Exception("'const' argument must be boolean")
        return result
    
    def _parse_constexpr_expression(self, expression: ast.expr) -> bool:
        result = self._parse_ast_constant_expression(expression, "constexpr")
        if type(result) is not bool:
            raise Exception("'constexpr' argument must be boolean")
        return result
    
    def _parse_value_expression(self, expression: ast.expr) -> bool:
        return self._parse_ast_constant_expression(expression, "value")

    def extract_field(self, name: str, keywords: list[ast.keyword]):
        field_type: CPPType = None
        static = False
        const = False
        constexpr = False
        access_modifier = CPPAccessModifier.PUBLIC
        value: str | int | float = None

        for keyword in keywords:
            argument_name = keyword.arg
            if argument_name == "type":
                field_type = self._parse_type_expression(keyword.value)
            elif argument_name == "access":
                access_modifier = self._parse_access_expression(keyword.value)
            elif argument_name == "static":
                static = self._parse_static_expression(keyword.value)
            elif argument_name == "const":
                const = self._parse_const_expression(keyword.value)
            elif argument_name == "constexpr":
                constexpr = self._parse_constexpr_expression(keyword.value)
            elif argument_name == "value":
                value = self._parse_value_expression(keyword.value)
            else:
                raise Exception(f"Unexpected FieldDescriptor argument: {argument_name}")

        if (constexpr or (static and constexpr)) and (value is None):
            raise Exception("constexpr and static constexpr fileld must have value set.")

        return CPPField(
            name = name,
            type = field_type,
            static = static,
            const = const,
            constexpr = constexpr,
            access_modifier = access_modifier,
            value = value
        )
    
    def extract_fields(self, class_body: list[ast.stmt]):
        assignments = super().extract_fields(class_body)
        fields = []        
        for assignment in assignments:
            field_name = assignment.targets[0].id
            keywords: list[ast.keyword] = assignment.value.keywords
            fields.append(self.extract_field(field_name, keywords))
        return fields
    
    def parse(self, clazz: ExtractedClass) -> CPPClass | Enum:
        enum_parser = EnumASTParser()
        if enum_parser.is_enum_def(clazz.class_def):
            return enum_parser.parse(clazz.class_def)
        return CPPClass(
            name=clazz.class_def.name, 
            fields=self.extract_fields(clazz.class_def.body), 
            include_path=""
        )
