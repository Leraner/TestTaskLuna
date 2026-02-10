from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetPaginatedOrganizationsByBuildingIdInputDTO:
    page: int
    size: int
    building_id: UUID


@dataclass
class GetOrganizationByBuildingIdActivityOutputDTO:
    id: UUID
    name: str
    level: int


@dataclass
class GetOrganizationByBuildingIdOutputDTO:
    id: UUID
    name: str
    phone_number: str
    activities: list[GetOrganizationByBuildingIdActivityOutputDTO]


@dataclass
class GetPaginatedOrganizationsByBuildingIdOutputDTO:
    page: int
    size: int
    total_count: int
    items: list[GetOrganizationByBuildingIdOutputDTO]