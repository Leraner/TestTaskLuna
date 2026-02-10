from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ActivityRef:
    id: UUID
    name: str
    level: int
