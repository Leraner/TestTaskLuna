from abc import ABC, abstractmethod
from uuid import UUID

from src.orginzations.domain.entity import Organization
from src.shared_kernel.value_object import LatitudeVO, LongitudeVO


class IOrganizationRepositoryPort(ABC):
    @abstractmethod
    async def get_organizations_paginated(
        self,
        page: int,
        size: int,
        building_id: UUID,
    ) -> tuple[list[Organization], int]: ...

    @abstractmethod
    async def get_organizations_by_radius(
        self,
        latitude: LatitudeVO,
        longitude: LongitudeVO,
        radius: float,
    ) -> list[Organization]: ...

    @abstractmethod
    async def search_by_name_paginated(
        self, page: int, size: int, organization_name: str
    ) -> tuple[list[Organization], int]: ...

    @abstractmethod
    async def get_by_id(self, organization_id: UUID) -> Organization | None: ...

    @abstractmethod
    async def get_by_activities_paginated(
        self,
        activity_ids: list[UUID],
        page: int,
        size: int,
    ) -> tuple[list[Organization], int]: ...

    @abstractmethod
    async def save(self, organization: Organization) -> None: ...

