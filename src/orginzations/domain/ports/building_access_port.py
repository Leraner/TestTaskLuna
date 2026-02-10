from abc import ABC, abstractmethod
from uuid import UUID

from src.orginzations.domain.building_ref import BuildingRef


class IBuildingAccessPort(ABC):
    @abstractmethod
    async def get_building_by_id(self, building_id: UUID) -> BuildingRef: ...

    @abstractmethod
    async def get_all_buildings(self) -> list[BuildingRef]: ...
