from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import aliased

from infrastructure.db.base_repository import BaseRepository
from src.activities.domain.entity import Activity
from src.activities.domain.ports.activity_repository import IActivityRepositoryPort
from src.activities.infrastructure.adapters.outbound.postgres.orm import ActivityModel
from src.activities.infrastructure.adapters.outbound.postgres.specifications import (
    GetActivityByIdSpec,
    GetActivityByIdsSpec,
    ByPaginationSpec,
)


class PostgresActivityRepositoryAdapter(
    BaseRepository[ActivityModel],
    IActivityRepositoryPort,
):
    async def save(self, activity: Activity) -> None:
        obj = ActivityModel.from_entity(entity=activity)
        await self._save(obj=obj)

    async def get_by_id(self, activity_id: UUID) -> Activity | None:
        specs = [GetActivityByIdSpec(activity_id=activity_id)]
        return await self._get_one_by_specs(model=ActivityModel, specs=specs)

    async def get_by_ids(self, activity_ids: list[UUID]) -> list[Activity]:
        if not activity_ids:
            return []
        specs = [GetActivityByIdsSpec(activity_ids=activity_ids)]
        return await self._get_many_by_specs(model=ActivityModel, specs=specs)

    async def get_subtree_ids(self, root_activity_id: UUID) -> list[UUID]:
        a = aliased(ActivityModel)

        base = (
            select(ActivityModel.id, ActivityModel.parent_id, ActivityModel.level)
            .where(ActivityModel.id == root_activity_id)
        )

        activity_tree = base.cte(name="activity_tree", recursive=True)

        activity_tree = activity_tree.union_all(
            select(a.id, a.parent_id, a.level)
            .join(activity_tree, a.parent_id == activity_tree.c.id)
            .where(a.level <= Activity.MAX_LEVEL)
        )

        query = select(activity_tree.c.id)

        result = await self._execute(query)
        rows = result.fetchall()
        return [row[0] for row in rows]

    async def get_all(self) -> list[Activity]:
        return await self._get_many_by_specs(model=ActivityModel, specs=[])

    async def get_paginated(self, page: int, size: int) -> tuple[list[Activity], int]:
        specs = [ByPaginationSpec(page=page, size=size)]

        total_count = await self._get_total_count_with_specs(
            model=ActivityModel, specs=specs
        )
        activities = await self._get_many_by_specs(model=ActivityModel, specs=specs)

        return activities, total_count

