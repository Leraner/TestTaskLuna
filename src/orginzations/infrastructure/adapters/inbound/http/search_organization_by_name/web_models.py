from uuid import UUID

from src.shared.web_models import BaseResponseDataModel, PaginatedWebOutputModel


class SearchedOrganizationByNameBuildingCoordinatesWebOutputModel(BaseResponseDataModel):
    latitude: float
    longitude: float


class SearchedOrganizationByNameBuildingWebOutputModel(BaseResponseDataModel):
    id: UUID
    address: str
    coordinates: SearchedOrganizationByNameBuildingCoordinatesWebOutputModel


class SearchedOrganizationByNameActivityWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    level: int


class SearchedOrganizationsByNameWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    phone_number: str
    building: SearchedOrganizationByNameBuildingWebOutputModel
    activities: list[SearchedOrganizationByNameActivityWebOutputModel]


GetPaginatedRolesWebOutputModel = PaginatedWebOutputModel[SearchedOrganizationsByNameWebOutputModel]
