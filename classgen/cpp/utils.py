
def is_or_inherit(value: any, _type: type) -> bool:
    return type(value) == _type or type(value).__bases__.__contains__(_type)

def is_one_of(value: any, types: list[type]) -> bool:
    for _type in types:
        if type(value) == _type:
            return True
    return False
