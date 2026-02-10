from abc import ABC, abstractmethod
from uuid import UUID

from src.activities.domain.entity import Activity


class IActivityRepositoryPort(ABC):
    @abstractmethod
    async def save(self, activity: Activity) -> None: ...

    @abstractmethod
    async def get_by_id(self, activity_id: UUID) -> Activity | None: ...

    @abstractmethod
    async def get_by_ids(self, activity_ids: list[UUID]) -> list[Activity]: ...

    @abstractmethod
    async def get_subtree_ids(self, root_activity_id: UUID) -> list[UUID]: ...

    @abstractmethod
    async def get_all(self) -> list[Activity]: ...

    @abstractmethod
    async def get_paginated(self, page: int, size: int) -> tuple[list[Activity], int]: ...
