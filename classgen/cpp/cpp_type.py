
import dataclasses

@dataclasses.dataclass
class CPPType:
    name: str
    include_path: str | None

    def __init__(self, name: str, include_path: str | None = None) -> None:
        self.name = name
        self.include_path = include_path