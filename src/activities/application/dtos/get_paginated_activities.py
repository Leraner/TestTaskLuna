from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetPaginatedActivitiesInputDTO:
    page: int
    size: int


@dataclass
class GetPaginatedActivityOutputDTO:
    id: UUID
    name: str
    parent_id: UUID | None
    level: int


@dataclass
class GetPaginatedActivitiesOutputDTO:
    page: int
    size: int
    total_count: int
    items: list[GetPaginatedActivityOutputDTO]
