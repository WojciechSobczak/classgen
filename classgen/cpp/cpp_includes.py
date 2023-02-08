import dataclasses

@dataclasses.dataclass
class CPPIncludes:
    standard_includes: list[str]
    libraries_includes: list[str]
    quotes_includes: list[str]

    def __init__(self) -> None:
        self.standard_includes = []
        self.libraries_includes = []
        self.quotes_includes = []

    def merge(self, other: 'CPPIncludes'):
        self.standard_includes += other.standard_includes
        self.libraries_includes += other.libraries_includes
        self.quotes_includes += other.quotes_includes

    def remove_duplicates(self):
        def remove_duplicates_preserve_order(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]
        self.standard_includes = remove_duplicates_preserve_order(self.standard_includes)
        self.libraries_includes = remove_duplicates_preserve_order(self.libraries_includes)
        self.quotes_includes = remove_duplicates_preserve_order(self.quotes_includes)