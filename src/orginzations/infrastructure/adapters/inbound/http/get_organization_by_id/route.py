from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from src.orginzations.application.dtos.get_organization_by_id import (
    GetOrganizationByIdInputDTO,
)
from src.orginzations.application.use_cases.get_organization_by_id import (
    GetOrganizationByIdUseCase,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_organization_by_id.presenter import \
    GetOrganizationByIdPresenter
from src.orginzations.infrastructure.adapters.inbound.http.get_organization_by_id.web_models import \
    GetOrganizationByIdWebOutputModel
from src.shared.web_models import BaseWebOutputModel

route = APIRouter()


@route.get("/{organization_id}")
@inject
async def get_organization_by_id(
    organization_id: UUID,
    use_case: FromDishka[GetOrganizationByIdUseCase],
    presenter: FromDishka[GetOrganizationByIdPresenter],
) -> BaseWebOutputModel[GetOrganizationByIdWebOutputModel]:
    uc_output = await use_case.execute(
        GetOrganizationByIdInputDTO(organization_id=organization_id),
    )
    response_data = presenter.present(uc_output)
    return BaseWebOutputModel(data=response_data)


