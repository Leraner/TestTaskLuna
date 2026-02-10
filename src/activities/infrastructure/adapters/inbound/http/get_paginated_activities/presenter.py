from src.activities.application.dtos.get_paginated_activities import (
    GetPaginatedActivitiesOutputDTO,
)
from src.activities.infrastructure.adapters.inbound.http.get_paginated_activities.web_models import (
    GetPaginatedActivitiesWebOutputModel,
    GetPaginatedActivityWebOutputModel,
)


class GetPaginatedActivitiesPresenter:
    def present(
        self, output_dto: GetPaginatedActivitiesOutputDTO
    ) -> GetPaginatedActivitiesWebOutputModel:
        items = [
            GetPaginatedActivityWebOutputModel(
                id=item.id,
                name=item.name,
                parent_id=item.parent_id,
                level=item.level,
            )
            for item in output_dto.items
        ]

        return GetPaginatedActivitiesWebOutputModel(
            page=output_dto.page,
            size=output_dto.size,
            total_count=output_dto.total_count,
            items=items,
        )
