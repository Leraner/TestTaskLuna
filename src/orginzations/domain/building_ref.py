from dataclasses import dataclass
from uuid import UUID

from src.shared_kernel.value_object import LongitudeVO, LatitudeVO


@dataclass
class BuildingRef:
    id: UUID
    address: str
    latitude: LatitudeVO
    longitude: LongitudeVO
