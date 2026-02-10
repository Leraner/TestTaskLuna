from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query

from src.orginzations.application.dtos.get_organizations import GetOrganizationsInputDTO
from src.orginzations.application.use_cases.get_organizations import (
    GetOrganizationsUseCase,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_organizations.presenter import (
    GetOrganizationsPresenter,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_organizations.web_models import (
    GetOrganizationsResponseWebOutputModel,
)
from src.shared.web_models import BaseWebOutputModel
from src.shared_kernel.value_object import LatitudeVO, LongitudeVO

route = APIRouter()


@route.get("/")
@inject
async def get_organizations(
    use_case: FromDishka[GetOrganizationsUseCase],
    presenter: FromDishka[GetOrganizationsPresenter],
    latitude: float = Query(
        default=59.9311,
        ge=-90,
        le=90,
        description="Широта центральной точки для поиска по радиусу. Используется вместе с longitude и radius",
    ),
    longitude: float = Query(
        default=30.3609,
        ge=-180,
        le=180,
        description="Долгота центральной точки для поиска по радиусу. Используется вместе с latitude и radius",
    ),
    radius: int = Query(
        default=50000,
        ge=50,
        le=50000,
        description="Радиус поиска в метрах. Диапазон: 50-50000м. Обязателен для геопоиска с координатами",
    ),
) -> BaseWebOutputModel[GetOrganizationsResponseWebOutputModel]:
    uc_output = await use_case.execute(
        GetOrganizationsInputDTO(
            latitude=LatitudeVO.from_value(latitude),
            longitude=LongitudeVO.from_value(longitude),
            radius=radius,
        )
    )
    response_data = presenter.present(uc_output)
    return BaseWebOutputModel(data=response_data)
