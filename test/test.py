import os
import shutil
import utils
import classgen
import classgen.cpp
from classgen.common import extract_classes
from classgen.cpp.generators.cpp_class_converter import convert_classes_to_cppclasses
from classgen.cpp.generators.to_json_string.cpp_to_json_string_generator import CPPToJsonStringGenerator
from classgen.cpp.generators.to_nlohmann_json.cpp_to_nlohmann_json_generator import CPPToNlohmannJsonGenerator


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = f"{SCRIPT_DIR}/generated/"

classes = extract_classes('./data_classes', SCRIPT_DIR)
classes = convert_classes_to_cppclasses(classes)

all_defined_classes= {clazz.name: clazz for clazz in classes} 

code_generator = classgen.cpp.CPPCodeGenerator([
    CPPToJsonStringGenerator(all_defined_classes = all_defined_classes),
    CPPToNlohmannJsonGenerator(all_defined_classes = all_defined_classes)
])

utils.remove_directory(GENERATED_DIR)
os.makedirs(GENERATED_DIR, exist_ok=True)

for clazz in classes:
    file_path = f"{GENERATED_DIR}/{clazz.include_path}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(code_generator.generate_code(clazz, namespace="Veracruz"))

hash_path = f'{SCRIPT_DIR}/../classgen/cpp/generators/templates/hash.hpp'
dest_path = f'{SCRIPT_DIR}/includes/classgen/hash.hpp'
if os.path.exists(dest_path) == False:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copyfile(hash_path, dest_path)

json_header_path = f'{SCRIPT_DIR}/includes/nlohmann/json.hpp'
if os.path.exists(json_header_path) == False:
    os.makedirs(os.path.dirname(json_header_path), exist_ok=True)
    with open(json_header_path, "w", encoding="UTF-8") as file:
        file.write(utils.download_page("https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp"))

utils.execute_command("clang++ main.cpp -std=c++2b -o main.exe -Iincludes -Igenerated")
utils.execute_command("main.exe")





    
