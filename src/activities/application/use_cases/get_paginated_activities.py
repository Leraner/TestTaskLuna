from src.activities.application.dtos.get_paginated_activities import (
    GetPaginatedActivitiesInputDTO,
    GetPaginatedActivitiesOutputDTO,
    GetPaginatedActivityOutputDTO,
)
from src.activities.domain.ports.activity_repository import IActivityRepositoryPort


class GetPaginatedActivitiesUseCase:
    def __init__(self, activity_repository: IActivityRepositoryPort) -> None:
        self._activity_repository = activity_repository

    async def execute(
        self, input_dto: GetPaginatedActivitiesInputDTO
    ) -> GetPaginatedActivitiesOutputDTO:
        activities, total_count = await self._activity_repository.get_paginated(
            page=input_dto.page,
            size=input_dto.size,
        )

        return GetPaginatedActivitiesOutputDTO(
            page=input_dto.page,
            size=input_dto.size,
            total_count=total_count,
            items=[
                GetPaginatedActivityOutputDTO(
                    id=activity.id,
                    name=activity.name,
                    parent_id=activity.parent_id,
                    level=activity.level,
                )
                for activity in activities
            ],
        )
