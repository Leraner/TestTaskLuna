from dishka import make_async_container

from infrastructure.db.provider import DatabaseProvider
from infrastructure.seeders.provider import SeederProvider
from src.activities.infrastructure.provider import ActivitiesProvider
from src.buildings.infrastructure.provider import BuildingsProvider
from src.orginzations.infrastructure.provider import OrganizationsProvider

providers = [
    DatabaseProvider(),
    OrganizationsProvider(),
    BuildingsProvider(),
    ActivitiesProvider(),
    SeederProvider(),
]

container = make_async_container(*providers)
