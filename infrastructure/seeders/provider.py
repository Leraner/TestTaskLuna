from dishka import Provider, Scope, provide

from infrastructure.seeders.app_seeder import AppSeeder
from src.activities.infrastructure.seeders.activity_seeder import ActivitySeeder
from src.buildings.infrastructure.seeders.building_seeder import BuildingSeeder
from src.orginzations.infrastructure.seeders.organization_seeder import (
    OrganizationSeeder,
)


class SeederProvider(Provider):
    scope = Scope.REQUEST

    building_seeder = provide(BuildingSeeder)
    activity_seeder = provide(ActivitySeeder)
    organization_seeder = provide(OrganizationSeeder)
    app_seeder = provide(AppSeeder)
