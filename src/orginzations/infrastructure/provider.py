from dishka import Provider, Scope, provide, provide_all

from src.buildings.infrastructure.adapters.inbound.http.get_paginated_buildings.presenter import (
    GetPaginatedBuildingsPresenter,
)
from src.orginzations.application.use_cases.get_organization_by_id import (
    GetOrganizationByIdUseCase,
)
from src.orginzations.application.use_cases.get_organizations import (
    GetOrganizationsUseCase,
)
from src.orginzations.application.use_cases.get_paginated_organizations_by_building_id import (
    GetPaginatedOrganizationsByBuildingIdUseCase,
)
from src.orginzations.application.use_cases.search_organization_by_name import (
    SearchOrganizationByNameUseCase,
)
from src.orginzations.application.use_cases.search_organizations_by_activity import (
    SearchOrganizationsByActivityUseCase,
)
from src.orginzations.domain.ports.building_access_port import IBuildingAccessPort
from src.orginzations.domain.ports.activity_access_port import IActivityAccessPort
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_organization_by_id.presenter import (
    GetOrganizationByIdPresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_organizations.presenter import (
    GetOrganizationsPresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_paginated_organizations_by_building_id.presenter import (
    GetPaginatedOrganizationsByBuildingIdPresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organization_by_name.presenter import (
    SearchOrganizationByNamePresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organizations_by_activity.presenter import (
    SearchOrganizationsByActivityPresenter,
)
from src.orginzations.infrastructure.adapters.outbound.postgres.building_access_adapter import (
    PostgresBuildingAccessAdapter,
)
from src.orginzations.infrastructure.adapters.outbound.postgres.activity_access_adapter import (
    PostgresActivityAccessAdapter,
)
from src.orginzations.infrastructure.adapters.outbound.postgres.organization_repo import (
    PostgresOrganizationRepositoryAdapter,
)


class OrganizationsProvider(Provider):
    scope = Scope.REQUEST

    presenters = provide_all(
        GetPaginatedOrganizationsByBuildingIdPresenter,
        GetOrganizationsPresenter,
        GetPaginatedBuildingsPresenter,
        GetOrganizationByIdPresenter,
        SearchOrganizationByNamePresenter,
        SearchOrganizationsByActivityPresenter,
    )

    use_cases = provide_all(
        GetPaginatedOrganizationsByBuildingIdUseCase,
        GetOrganizationByIdUseCase,
        SearchOrganizationByNameUseCase,
        SearchOrganizationsByActivityUseCase,
        GetOrganizationsUseCase,
    )

    repository_adapter = provide(
        PostgresOrganizationRepositoryAdapter,
        provides=IOrganizationRepositoryPort,
    )

    building_access_adapter = provide(
        PostgresBuildingAccessAdapter, provides=IBuildingAccessPort
    )

    activity_access_adapter = provide(
        PostgresActivityAccessAdapter, provides=IActivityAccessPort
    )
