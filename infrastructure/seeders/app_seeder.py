from infrastructure.seeders.base_seeder import BaseSeeder
from src.activities.infrastructure.seeders.activity_seeder import ActivitySeeder
from src.buildings.infrastructure.seeders.building_seeder import BuildingSeeder
from src.orginzations.infrastructure.seeders.organization_seeder import (
    OrganizationSeeder,
)


class AppSeeder(BaseSeeder):
    def __init__(
        self,
        building_seeder: BuildingSeeder,
        activity_seeder: ActivitySeeder,
        organization_seeder: OrganizationSeeder,
    ) -> None:
        self._building_seeder = building_seeder
        self._activity_seeder = activity_seeder
        self._organization_seeder = organization_seeder

    async def seed(self) -> None:
        await self._building_seeder.seed()
        await self._activity_seeder.seed()
        await self._organization_seeder.seed()

    async def clear(self) -> None:
        await self._organization_seeder.clear()
        await self._activity_seeder.clear()
        await self._building_seeder.clear()
