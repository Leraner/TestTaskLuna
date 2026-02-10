from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query

from src.orginzations.application.dtos.get_paginated_organizations_by_building_id import (
    GetPaginatedOrganizationsByBuildingIdInputDTO,
)
from src.orginzations.application.use_cases.get_paginated_organizations_by_building_id import (
    GetPaginatedOrganizationsByBuildingIdUseCase,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_paginated_organizations_by_building_id.presenter import (
    GetPaginatedOrganizationsByBuildingIdPresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_paginated_organizations_by_building_id.web_models import (
    GetPaginatedRolesWebOutputModel,
)
from src.shared.web_models import BaseWebOutputModel

route = APIRouter()


@route.get("/building/{building_id}")
@inject
async def get_paginated_organizations_by_building_id(
    building_id: UUID,
    use_case: FromDishka[GetPaginatedOrganizationsByBuildingIdUseCase],
    presenter: FromDishka[GetPaginatedOrganizationsByBuildingIdPresenter],
    page: int = Query(ge=1, default=1),
    size: int = Query(default=50, le=50, ge=1),
) -> BaseWebOutputModel[GetPaginatedRolesWebOutputModel]:
    uc_output = await use_case.execute(
        GetPaginatedOrganizationsByBuildingIdInputDTO(
            page=page, size=size, building_id=building_id
        )
    )
    response_data = presenter.present(uc_output)
    return response_data.as_web_output()
