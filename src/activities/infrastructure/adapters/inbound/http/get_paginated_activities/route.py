from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query

from src.activities.application.dtos.get_paginated_activities import (
    GetPaginatedActivitiesInputDTO,
)
from src.activities.application.use_cases.get_paginated_activities import (
    GetPaginatedActivitiesUseCase,
)
from src.activities.infrastructure.adapters.inbound.http.get_paginated_activities.presenter import (
    GetPaginatedActivitiesPresenter,
)
from src.activities.infrastructure.adapters.inbound.http.get_paginated_activities.web_models import (
    GetPaginatedActivitiesWebOutputModel,
)
from src.shared.web_models import BaseWebOutputModel

route = APIRouter()


@route.get("/", response_model=BaseWebOutputModel[GetPaginatedActivitiesWebOutputModel])
@inject
async def get_paginated_activities(
    use_case: FromDishka[GetPaginatedActivitiesUseCase],
    presenter: FromDishka[GetPaginatedActivitiesPresenter],
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
) -> BaseWebOutputModel[GetPaginatedActivitiesWebOutputModel]:
    uc_output = await use_case.execute(
        GetPaginatedActivitiesInputDTO(page=page, size=size)
    )
    response_data = presenter.present(uc_output)
    return BaseWebOutputModel(data=response_data)
