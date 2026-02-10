from dishka import Provider, Scope, provide, provide_all

from src.buildings.application.use_cases.get_paginated_buildings import (
    GetPaginatedBuildingsUseCase,
)
from src.buildings.domain.ports.building_repository import IBuildingRepositoryPort
from src.buildings.infrastructure.adapters.outbound.postgres.building_repo import (
    PostgresBuildingRepositoryAdapter,
)


class BuildingsProvider(Provider):
    scope = Scope.REQUEST

    presenters = provide_all()

    use_cases = provide_all(
        GetPaginatedBuildingsUseCase,
    )

    repository_adapter = provide(
        PostgresBuildingRepositoryAdapter,
        provides=IBuildingRepositoryPort,
    )
