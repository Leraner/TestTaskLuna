from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from sqlalchemy import Select, Update, Delete, Insert

from infrastructure.db.orm import BaseDBModel

QueryType = TypeVar("QueryType", Select, Update, Delete, Insert)
T = TypeVar("T", bound=BaseDBModel)


class Specification(ABC, Generic[T]):
    @abstractmethod
    def apply(self, query: QueryType, model: Type[T]) -> QueryType: ...
