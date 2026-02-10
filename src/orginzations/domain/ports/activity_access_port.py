from abc import ABC, abstractmethod
from uuid import UUID

from src.orginzations.domain.activity_ref import ActivityRef


class IActivityAccessPort(ABC):
    @abstractmethod
    async def get_activities_by_ids(self, activity_ids: list[UUID]) -> list[ActivityRef]: ...

    @abstractmethod
    async def get_subtree_ids(self, root_activity_id: UUID) -> list[UUID]: ...

    @abstractmethod
    async def get_all_activities(self) -> list[ActivityRef]: ...
