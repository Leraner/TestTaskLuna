from uuid import UUID

from src.shared.web_models import BaseResponseDataModel, PaginatedWebOutputModel


class GetOrganizationBuildingCoordinatesWebOutputModel(BaseResponseDataModel):
    latitude: float
    longitude: float


class GetOrganizationBuildingWebOutputModel(BaseResponseDataModel):
    id: UUID
    address: str
    coordinates: GetOrganizationBuildingCoordinatesWebOutputModel


class SearchedOrganizationsByActivityWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    phone_number: str
    building: GetOrganizationBuildingWebOutputModel


GetPaginatedOrganizationsByActivityWebOutputModel = PaginatedWebOutputModel[
    SearchedOrganizationsByActivityWebOutputModel
]
