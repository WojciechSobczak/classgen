
import dataclasses

@dataclasses.dataclass(frozen = True)
class CPPType:
    name: str
    include_path: str | None