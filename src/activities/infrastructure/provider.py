from dishka import Provider, Scope, provide, provide_all

from src.activities.application.use_cases.get_paginated_activities import (
    GetPaginatedActivitiesUseCase,
)
from src.activities.domain.ports.activity_repository import IActivityRepositoryPort
from src.activities.infrastructure.adapters.inbound.http.get_paginated_activities.presenter import (
    GetPaginatedActivitiesPresenter,
)
from src.activities.infrastructure.adapters.outbound.postgres.activity_repo import (
    PostgresActivityRepositoryAdapter,
)


class ActivitiesProvider(Provider):
    scope = Scope.REQUEST

    presenters = provide_all(GetPaginatedActivitiesPresenter)

    use_cases = provide_all(GetPaginatedActivitiesUseCase)

    repository_adapter = provide(
        PostgresActivityRepositoryAdapter,
        provides=IActivityRepositoryPort,
    )
