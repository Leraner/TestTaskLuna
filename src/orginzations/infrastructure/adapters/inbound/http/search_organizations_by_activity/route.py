from uuid import UUID

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Query

from src.orginzations.application.dtos.search_organizations_by_activity import (
    SearchOrganizationsByActivityInputDTO,
)
from src.orginzations.application.use_cases.search_organizations_by_activity import (
    SearchOrganizationsByActivityUseCase,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organizations_by_activity.presenter import (
    SearchOrganizationsByActivityPresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organizations_by_activity.web_models import (
    GetPaginatedOrganizationsByActivityWebOutputModel,
)
from src.shared.web_models import BaseWebOutputModel

route = APIRouter()


@route.get("/search/by-activity/{activity_id}")
@inject
async def search_organizations_by_activity(
    use_case: FromDishka[SearchOrganizationsByActivityUseCase],
    presenter: FromDishka[SearchOrganizationsByActivityPresenter],
    activity_id: UUID,
    page: int = Query(ge=1, default=1),
    size: int = Query(default=50, le=50, ge=1),
) -> BaseWebOutputModel[GetPaginatedOrganizationsByActivityWebOutputModel]:
    uc_output = await use_case.execute(
        SearchOrganizationsByActivityInputDTO(
            activity_id=activity_id,
            page=page,
            size=size,
        )
    )
    response_data = presenter.present(uc_output)
    return response_data.as_web_output()
