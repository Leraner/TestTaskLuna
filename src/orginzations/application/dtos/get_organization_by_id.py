from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.shared_kernel.value_object import LatitudeVO, LongitudeVO

@dataclass
class GetOrganizationByIdInputDTO:
    organization_id: UUID


@dataclass
class GetOrganizationByIdBuilding:
    id: UUID
    address: str
    latitude: LatitudeVO
    longitude: LongitudeVO


@dataclass
class GetOrganizationByIdActivityOutputDTO:
    id: UUID
    name: str
    level: int


@dataclass
class GetOrganizationByIdOutputDTO:
    id: UUID
    name: str
    phone_number: str
    building: GetOrganizationByIdBuilding
    activities: list[GetOrganizationByIdActivityOutputDTO]
    updated_at: datetime
    created_at: datetime
