from dataclasses import dataclass
from uuid import UUID

from src.shared_kernel.value_object import LatitudeVO, LongitudeVO


@dataclass
class SearchOrganizationsByActivityInputDTO:
    activity_id: UUID
    page: int
    size: int


@dataclass
class SearchedOrganizationByActivityBuildingOutputDTO:
    id: UUID
    address: str
    latitude: LatitudeVO
    longitude: LongitudeVO


@dataclass
class SearchedOrganizationByActivityOutputDTO:
    id: UUID
    name: str
    phone_number: str
    building: SearchedOrganizationByActivityBuildingOutputDTO


@dataclass
class GetPaginatedSearchedOrganizationsByActivityOutputDTO:
    page: int
    size: int
    total_count: int
    items: list[SearchedOrganizationByActivityOutputDTO]
