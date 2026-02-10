from uuid import UUID

from src.buildings.domain.ports.building_repository import IBuildingRepositoryPort
from src.orginzations.domain.building_ref import BuildingRef
from src.orginzations.domain.ports.building_access_port import IBuildingAccessPort


class PostgresBuildingAccessAdapter(IBuildingAccessPort):
    def __init__(self, building_repository: IBuildingRepositoryPort) -> None:
        self._building_repository = building_repository

    async def get_building_by_id(self, building_id: UUID) -> BuildingRef | None:
        if building := await self._building_repository.get_by_id(
            building_id=building_id
        ):
            return BuildingRef(
                id=building.id,
                address=building.address,
                latitude=building.latitude,
                longitude=building.longitude,
            )
        return None

    async def get_all_buildings(self) -> list[BuildingRef]:
        buildings = await self._building_repository.get_all()
        return [
            BuildingRef(
                id=building.id,
                address=building.address,
                latitude=building.latitude,
                longitude=building.longitude,
            )
            for building in buildings
        ]
