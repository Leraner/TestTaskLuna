from uuid import UUID

from sqlalchemy import select

from infrastructure.db.base_repository import BaseRepository
from src.orginzations.domain.entity import Organization
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)
from src.orginzations.infrastructure.adapters.outbound.postgres.orm import (
    OrganizationModel,
)
from src.orginzations.infrastructure.adapters.outbound.postgres.specifications import (
    ByIdSpec,
    ByPaginationSpec,
    SearchByNameSpec,
    GetByRadiusSpec,
    GetByBuildingIdSpec,
    GetByActivitiesSpec,
)
from src.shared_kernel.value_object import LatitudeVO, LongitudeVO
from src.activities.infrastructure.adapters.outbound.postgres.orm import ActivityModel


class PostgresOrganizationRepositoryAdapter(
    BaseRepository[OrganizationModel],
    IOrganizationRepositoryPort,
):
    async def get_organizations_paginated(
        self,
        page: int,
        size: int,
        building_id: UUID,
    ) -> tuple[list[Organization], int]:
        specs = [
            ByPaginationSpec(page=page, size=size),
            GetByBuildingIdSpec(building_id=building_id),
        ]
        total_count = await self._get_total_count_with_specs(
            model=OrganizationModel, specs=specs
        )
        organizations = await self._get_many_by_specs(
            model=OrganizationModel, specs=specs
        )
        return organizations, total_count

    async def get_organizations_by_radius(
        self,
        latitude: LatitudeVO,
        longitude: LongitudeVO,
        radius: float,
    ) -> list[Organization]:
        specs = [GetByRadiusSpec(latitude=latitude, longitude=longitude, radius=radius)]
        return await self._get_many_by_specs(model=OrganizationModel, specs=specs)

    async def search_by_name_paginated(
        self, page: int, size: int, organization_name: str
    ) -> tuple[list[Organization], int]:
        specs = [
            ByPaginationSpec(page=page, size=size),
            SearchByNameSpec(organization_name=organization_name),
        ]
        total_count = await self._get_total_count_with_specs(
            model=OrganizationModel, specs=specs
        )
        organizations = await self._get_many_by_specs(
            model=OrganizationModel, specs=specs
        )
        return organizations, total_count

    async def get_by_id(self, organization_id: UUID) -> Organization | None:
        specs = [ByIdSpec(organization_id)]
        return await self._get_one_by_specs(model=OrganizationModel, specs=specs)

    async def get_by_activities_paginated(
        self,
        activity_ids: list[UUID],
        page: int,
        size: int,
    ) -> tuple[list[Organization], int]:
        if not activity_ids:
            return [], 0

        specs = [
            GetByActivitiesSpec(activity_ids=activity_ids),
            ByPaginationSpec(page=page, size=size),
        ]

        total_count = await self._get_total_count_with_specs(
            model=OrganizationModel, specs=specs
        )
        organizations = await self._get_many_by_specs(
            model=OrganizationModel, specs=specs
        )

        return organizations, total_count

    async def save(self, organization: Organization) -> None:
        obj = OrganizationModel.from_entity(entity=organization)

        if organization.activities:
            activity_ids = [ref.id for ref in organization.activities]
            result = await self._execute(
                select(ActivityModel).where(ActivityModel.id.in_(activity_ids))
            )
            obj.activities = list(result.scalars().unique().all())

        await self._save(obj=obj)
