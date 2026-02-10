from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query

from src.orginzations.application.dtos.search_organization_by_name import (
    SearchOrganizationByNameInputDTO,
)
from src.orginzations.application.use_cases.search_organization_by_name import (
    SearchOrganizationByNameUseCase,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organization_by_name.presenter import (
    SearchOrganizationByNamePresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organization_by_name.web_models import (
    GetPaginatedRolesWebOutputModel,
)
from src.shared.web_models import BaseWebOutputModel

route = APIRouter()


@route.get("/search/{organization_name}")
@inject
async def search_organization_by_name(
    organization_name: str,
    use_case: FromDishka[SearchOrganizationByNameUseCase],
    presenter: FromDishka[SearchOrganizationByNamePresenter],
    page: int = Query(ge=1, default=1),
    size: int = Query(default=50, le=50, ge=1),
) -> BaseWebOutputModel[GetPaginatedRolesWebOutputModel]:
    uc_output = await use_case.execute(
        SearchOrganizationByNameInputDTO(
            page=page,
            size=size,
            organization_name=organization_name,
        )
    )
    response_data = presenter.present(uc_output)
    return response_data.as_web_output()
