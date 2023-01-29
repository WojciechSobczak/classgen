import ast
import os

from classgen.cpp.cpp_ast_parser import CPPASTParser
from classgen.classgen import extract_classes
from classgen.cpp.cpp_code_generator import CPPCodeGenerator

import shutil


classes_path = os.path.dirname(os.path.abspath(__file__)) + "/class_templates"
class_files = []
for file in os.listdir(classes_path):
    class_file_path = os.path.join(classes_path, file)
    if os.path.isfile(class_file_path):
        class_files.append(class_file_path)

class_defs: list[ast.ClassDef] = []
for file in class_files:
    class_defs += extract_classes(file)

code_generator = CPPCodeGenerator()
additional_generators = [
    #CPPToJsonStringGenerator(), 
    #BSONGenerator(), 
    #CPPConversionGenerator()
]

parser = CPPASTParser()
classes = [parser.parse(clazz) for clazz in class_defs]

for clazz in classes:
    with open(f"generated/{clazz.name}.hpp", "w") as file:
        file.write(code_generator.generate_code(clazz, additional_generators))

hash_path = 'classgen/cpp/templates/hash.hpp'
dest_path = 'generated/classgen/hash.hpp'
if os.path.exists(dest_path) == False:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copyfile(hash_path, dest_path)
