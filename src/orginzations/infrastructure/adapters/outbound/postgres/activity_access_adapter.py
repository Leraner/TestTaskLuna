from uuid import UUID

from src.activities.domain.ports.activity_repository import IActivityRepositoryPort
from src.orginzations.domain.activity_ref import ActivityRef
from src.orginzations.domain.ports.activity_access_port import IActivityAccessPort


class PostgresActivityAccessAdapter(IActivityAccessPort):
    def __init__(self, activity_repository: IActivityRepositoryPort) -> None:
        self._activity_repository = activity_repository

    async def get_activities_by_ids(
        self, activity_ids: list[UUID]
    ) -> list[ActivityRef]:
        activities = await self._activity_repository.get_by_ids(
            activity_ids=activity_ids
        )
        return [
            ActivityRef(
                id=activity.id,
                name=activity.name,
                level=activity.level,
            )
            for activity in activities
        ]

    async def get_subtree_ids(self, root_activity_id: UUID) -> list[UUID]:
        return await self._activity_repository.get_subtree_ids(
            root_activity_id=root_activity_id
        )

    async def get_all_activities(self) -> list[ActivityRef]:
        activities = await self._activity_repository.get_all()
        return [
            ActivityRef(
                id=activity.id,
                name=activity.name,
                level=activity.level,
            )
            for activity in activities
        ]
