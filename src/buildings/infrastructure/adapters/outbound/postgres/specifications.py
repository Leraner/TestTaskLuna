from dataclasses import dataclass
from typing import Type
from uuid import UUID

from infrastructure.db.specifications import Specification, QueryType
from src.buildings.infrastructure.adapters.outbound.postgres.orm import BuildingModel


@dataclass
class GetByIdSpec(Specification[BuildingModel]):
    building_id: UUID

    def apply(self, query: QueryType, model: Type[BuildingModel]) -> QueryType:
        return query.where(model.id == self.building_id)


@dataclass
class ByPaginationSpec(Specification[BuildingModel]):
    size: int
    page: int

    def apply(self, query: QueryType, model: type[BuildingModel]) -> QueryType:
        offset = (self.page - 1) * self.size
        return query.limit(self.size).offset(offset)
