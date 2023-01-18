import os
import subprocess
from classgen.cpp.cpp_ast_parser import CPPASTParser
from classgen.cpp.cpp_ast_parser import CPPASTParser
from classgen.cpp.cpp_code_generator import CPPCodeGenerator
from classgen.classgen import CodegenClass, extract_classes
from classgen.generators.cpp_to_json_string_generator import CPPToJsonStringGenerator


classes_path = os.path.dirname(os.path.abspath(__file__)) + "/class_templates"
class_files = []
for file in os.listdir(classes_path):
    class_file_path = os.path.join(classes_path, file)
    if os.path.isfile(class_file_path):
        class_files.append(class_file_path)

parser = CPPASTParser()
classes: list[CodegenClass] = []
for file in class_files:
    classes += extract_classes(file, parser)

code_generator = CPPCodeGenerator()
additional_generators = [CPPToJsonStringGenerator()]

for clazz in classes:
    class_code = code_generator.generate_code(clazz, additional_generators)
    result = subprocess.check_output(['clang-format', '-style=file'], input=class_code.encode('UTF-8'))
    class_text = result.decode('utf-8')
    with open(f"generated/{clazz.name}.hpp", "w") as file:
        file.write(class_text)
