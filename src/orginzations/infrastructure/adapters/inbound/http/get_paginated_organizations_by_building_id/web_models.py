from uuid import UUID

from src.shared.web_models import BaseResponseDataModel, PaginatedWebOutputModel


class GetOrganizationByBuildingIdActivityWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    level: int


class GetOrganizationByBuildingIdWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    phone_number: str
    activities: list[GetOrganizationByBuildingIdActivityWebOutputModel]


GetPaginatedRolesWebOutputModel = PaginatedWebOutputModel[GetOrganizationByBuildingIdWebOutputModel]
