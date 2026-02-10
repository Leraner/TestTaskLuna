from dataclasses import dataclass
from typing import Type
from uuid import UUID

from geoalchemy2 import Geography
from sqlalchemy import func

from infrastructure.db.specifications import Specification, QueryType
from src.activities.infrastructure.adapters.outbound.postgres.orm import ActivityModel
from src.buildings.infrastructure.adapters.outbound.postgres.orm import (
    GEOM_SRID,
    BuildingModel,
)
from src.orginzations.infrastructure.adapters.outbound.postgres.orm import (
    OrganizationModel,
)
from src.shared_kernel.value_object import LatitudeVO, LongitudeVO


@dataclass
class ByIdSpec(Specification[OrganizationModel]):
    organization_id: UUID

    def apply(self, query: QueryType, model: Type[OrganizationModel]) -> QueryType:
        return query.where(model.id == self.organization_id)


@dataclass
class ByPaginationSpec(Specification[OrganizationModel]):
    page: int
    size: int

    def apply(self, query: QueryType, model: Type[OrganizationModel]) -> QueryType:
        offset = (self.page - 1) * self.size
        return query.offset(offset).limit(self.size)


@dataclass
class SearchByNameSpec(Specification[OrganizationModel]):
    organization_name: str

    def apply(self, query: QueryType, model: Type[OrganizationModel]) -> QueryType:
        return query.where(model.name.ilike(f"%{self.organization_name}%"))


@dataclass
class GetByRadiusSpec(Specification[OrganizationModel]):
    latitude: LatitudeVO
    longitude: LongitudeVO
    radius: float

    def apply(self, query: QueryType, model: Type[OrganizationModel]) -> QueryType:
        point = func.ST_SetSRID(
            func.ST_MakePoint(self.longitude.value, self.latitude.value), GEOM_SRID
        )
        return query.join(model.building).where(
            func.ST_DWithin(
                BuildingModel.geom.cast(Geography),
                point.cast(Geography),
                self.radius,
            ),
        )


@dataclass
class GetByBuildingIdSpec(Specification[OrganizationModel]):
    building_id: UUID

    def apply(self, query: QueryType, model: Type[OrganizationModel]) -> QueryType:
        return query.where(model.building_id == self.building_id)


@dataclass
class GetByActivitiesSpec(Specification[OrganizationModel]):
    activity_ids: list[UUID]

    def apply(self, query: QueryType, model: Type[OrganizationModel]) -> QueryType:
        return (
            query.join(model.activities)
            .where(ActivityModel.id.in_(self.activity_ids))
            .distinct()
        )
