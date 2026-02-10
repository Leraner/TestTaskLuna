from src.buildings.application.dtos.get_paginated_buildings import (
    GetPaginatedBuildingsOutputDTO,
)
from src.buildings.infrastructure.adapters.inbound.http.get_paginated_buildings.web_models import (
    GetPaginatedBuildingsOutputWebModel,
    GeBuildingsOutputWebModel,
    GetBuildingCoordinatesOutputWebModel,
)


class GetPaginatedBuildingsPresenter:
    def present(
        self, output_dto: GetPaginatedBuildingsOutputDTO
    ) -> GetPaginatedBuildingsOutputWebModel:
        items = [
            GeBuildingsOutputWebModel(
                id=item.id,
                address=item.address,
                coordinates=GetBuildingCoordinatesOutputWebModel(
                    latitude=item.latitude.value,
                    longitude=item.longitude.value,
                ),
            )
            for item in output_dto.items
        ]

        return GetPaginatedBuildingsOutputWebModel(
            page=output_dto.page,
            size=output_dto.size,
            total_count=output_dto.total_count,
            items=items,
        )
