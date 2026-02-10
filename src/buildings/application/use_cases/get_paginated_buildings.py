from src.buildings.application.dtos.get_paginated_buildings import (
    GetBuildingsInputDTO,
    GetBuildingsOutputDTO,
    GetPaginatedBuildingsOutputDTO,
)
from src.buildings.domain.ports.building_repository import IBuildingRepositoryPort


class GetPaginatedBuildingsUseCase:
    def __init__(
        self,
        building_repository: IBuildingRepositoryPort,
    ) -> None:
        self._building_repository = building_repository

    async def execute(
        self, input_dto: GetBuildingsInputDTO
    ) -> GetPaginatedBuildingsOutputDTO:
        buildings, total_count = await self._building_repository.get_paginated(
            page=input_dto.page, size=input_dto.size
        )

        return GetPaginatedBuildingsOutputDTO(
            page=input_dto.page,
            size=input_dto.size,
            total_count=total_count,
            items=[
                GetBuildingsOutputDTO(
                    id=building.id,
                    address=building.address,
                    longitude=building.longitude,
                    latitude=building.latitude,
                )
                for building in buildings
            ],
        )
