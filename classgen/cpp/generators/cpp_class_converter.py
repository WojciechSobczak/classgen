from classgen.common import Class
from classgen.cpp.cpp_class import CPPClass
from classgen.utils import extract_cpp_fields, extract_include_from_class

def convert_classes_to_cppclasses(classes: list[Class]) -> list[CPPClass]:
    output_classes: list[CPPClass] = []
    for clazz in classes:
        output_classes.append(CPPClass(
            name = clazz.class_type.__name__,
            include_path = extract_include_from_class(clazz), 
            fields = extract_cpp_fields(clazz)
        ))
    return output_classes
