from uuid import UUID

from src.shared.web_models import BaseResponseDataModel


class GetOrganizationBuildingCoordinatesWebOutputModel(BaseResponseDataModel):
    latitude: float
    longitude: float


class GetOrganizationBuildingWebOutputModel(BaseResponseDataModel):
    id: UUID
    address: str
    coordinates: GetOrganizationBuildingCoordinatesWebOutputModel


class GetOrganizationActivityWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    level: int


class GetOrganizationWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    phone_number: str
    building: GetOrganizationBuildingWebOutputModel
    activities: list[GetOrganizationActivityWebOutputModel]


class GetOrganizationsResponseWebOutputModel(BaseResponseDataModel):
    organizations: list[GetOrganizationWebOutputModel]