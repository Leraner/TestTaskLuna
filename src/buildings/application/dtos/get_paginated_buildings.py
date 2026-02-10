from dataclasses import dataclass
from uuid import UUID

from src.shared_kernel.value_object import LatitudeVO, LongitudeVO


@dataclass
class GetBuildingsInputDTO:
    page: int
    size: int


@dataclass
class GetBuildingsOutputDTO:
    id: UUID
    address: str
    latitude: LatitudeVO
    longitude: LongitudeVO


@dataclass
class GetPaginatedBuildingsOutputDTO:
    page: int
    size: int
    total_count: int
    items: list[GetBuildingsOutputDTO]
