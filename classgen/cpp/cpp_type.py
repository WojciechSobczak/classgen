
import dataclasses

@dataclasses.dataclass
class CPPType:
    name: str
    include_path: str | None
