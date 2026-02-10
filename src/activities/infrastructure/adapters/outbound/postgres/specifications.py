from dataclasses import dataclass
from typing import Type
from uuid import UUID

from infrastructure.db.specifications import Specification, QueryType
from src.activities.infrastructure.adapters.outbound.postgres.orm import ActivityModel


@dataclass
class GetActivityByIdSpec(Specification[ActivityModel]):
    activity_id: UUID

    def apply(self, query: QueryType, model: Type[ActivityModel]) -> QueryType:
        return query.where(model.id == self.activity_id)


@dataclass
class GetActivityByIdsSpec(Specification[ActivityModel]):
    activity_ids: list[UUID]

    def apply(self, query: QueryType, model: Type[ActivityModel]) -> QueryType:
        return query.where(model.id.in_(self.activity_ids))


@dataclass
class ByPaginationSpec(Specification[ActivityModel]):
    page: int
    size: int

    def apply(self, query: QueryType, model: Type[ActivityModel]) -> QueryType:
        return query.limit(self.size).offset((self.page - 1) * self.size)
