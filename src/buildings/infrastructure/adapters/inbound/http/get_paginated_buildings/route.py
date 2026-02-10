from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Query

from src.buildings.application.dtos.get_paginated_buildings import GetBuildingsInputDTO
from src.buildings.application.use_cases.get_paginated_buildings import (
    GetPaginatedBuildingsUseCase,
)
from src.buildings.infrastructure.adapters.inbound.http.get_paginated_buildings.presenter import (
    GetPaginatedBuildingsPresenter,
)
from src.buildings.infrastructure.adapters.inbound.http.get_paginated_buildings.web_models import (
    GetPaginatedBuildingsOutputWebModel,
)
from src.shared.web_models import BaseWebOutputModel

route = APIRouter()


@route.get("/")
@inject
async def get_paginated_buildings(
    use_case: FromDishka[GetPaginatedBuildingsUseCase],
    presenter: FromDishka[GetPaginatedBuildingsPresenter],
    page: int = Query(ge=1, default=1),
    size: int = Query(default=50, le=50, ge=1),
) -> BaseWebOutputModel[GetPaginatedBuildingsOutputWebModel]:
    uc_output = await use_case.execute(
        GetBuildingsInputDTO(
            page=page,
            size=size,
        )
    )
    response_data = presenter.present(uc_output)
    return response_data.as_web_output()
