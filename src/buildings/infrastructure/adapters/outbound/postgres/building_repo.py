from uuid import UUID

from infrastructure.db.base_repository import BaseRepository
from src.buildings.domain.entity import Building
from src.buildings.domain.ports.building_repository import IBuildingRepositoryPort
from src.buildings.infrastructure.adapters.outbound.postgres.orm import BuildingModel
from src.buildings.infrastructure.adapters.outbound.postgres.specifications import (
    GetByIdSpec,
    ByPaginationSpec,
)


class PostgresBuildingRepositoryAdapter(
    BaseRepository[BuildingModel],
    IBuildingRepositoryPort,
):
    async def save(self, building: Building) -> None:
        obj = BuildingModel.from_entity(entity=building)
        await self._save(obj=obj)

    async def get_by_id(self, building_id: UUID) -> Building | None:
        specs = [GetByIdSpec(building_id=building_id)]
        return await self._get_one_by_specs(model=BuildingModel, specs=specs)

    async def get_paginated(self, page: int, size: int) -> tuple[list[Building], int]:
        specs = [ByPaginationSpec(page=page, size=size)]

        total_count = await self._get_total_count_with_specs(
            model=BuildingModel, specs=specs
        )
        buildings = await self._get_many_by_specs(model=BuildingModel, specs=specs)

        return buildings, total_count

    async def get_all(self) -> list[Building]:
        return await self._get_many_by_specs(model=BuildingModel, specs=[])
