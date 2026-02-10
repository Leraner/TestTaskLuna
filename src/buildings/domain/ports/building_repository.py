from abc import ABC
from uuid import UUID

from src.buildings.domain.entity import Building


class IBuildingRepositoryPort(ABC):
    async def save(self, building: Building) -> None: ...

    async def get_by_id(self, building_id: UUID) -> Building | None: ...

    async def get_paginated(self, page: int, size: int) -> tuple[list[Building], int]: ...

    async def get_all(self) -> list[Building]: ...
