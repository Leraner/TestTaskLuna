from dataclasses import dataclass
from uuid import UUID

from src.shared_kernel.value_object import LatitudeVO, LongitudeVO


@dataclass
class GetOrganizationsInputDTO:
    latitude: LatitudeVO
    longitude: LongitudeVO
    radius: float


@dataclass
class GetOrganizationBuildingOutputDTO:
    id: UUID
    address: str
    latitude: LatitudeVO
    longitude: LongitudeVO


@dataclass
class GetOrganizationActivityOutputDTO:
    id: UUID
    name: str
    level: int


@dataclass
class GetOrganizationOutputDTO:
    id: UUID
    name: str
    phone_number: str
    building: GetOrganizationBuildingOutputDTO
    activities: list[GetOrganizationActivityOutputDTO]


@dataclass
class GetOrganizationsOutputDTO:
    organizations: list[GetOrganizationOutputDTO]