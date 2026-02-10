from dataclasses import dataclass
from uuid import UUID

from src.shared_kernel.value_object import LatitudeVO, LongitudeVO


@dataclass
class SearchOrganizationByNameInputDTO:
    page: int
    size: int
    organization_name: str


@dataclass
class SearchedOrganizationByNameBuildingOutputDTO:
    id: UUID
    address: str
    latitude: LatitudeVO
    longitude: LongitudeVO


@dataclass
class SearchedOrganizationByNameActivityOutputDTO:
    id: UUID
    name: str
    level: int


@dataclass
class SearchedOrganizationByNameOutputDTO:
    id: UUID
    name: str
    phone_number: str
    building: SearchedOrganizationByNameBuildingOutputDTO
    activities: list[SearchedOrganizationByNameActivityOutputDTO]


@dataclass
class GetPaginatedSearchedOrganizationsByNameOutputDTO:
    page: int
    size: int
    total_count: int
    items: list[SearchedOrganizationByNameOutputDTO]