from dataclasses import dataclass
import jinja2
import os
import textwrap

from classgen.code_generator import CodeGenerator
from classgen.cpp.cpp_class import CPPClass
from classgen.cpp.cpp_field import CPPField
from classgen.cpp.cpp_standard_types import CPPString, is_numerical, CPPMap, CPPTemplatedType
from classgen.cpp.cpp_type import CPPType


_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class CPPConstructorGenerator(CodeGenerator):
    pass