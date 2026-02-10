from datetime import datetime
from uuid import UUID

from src.shared.web_models import BaseResponseDataModel


class GetOrganizationByIdBuildingCoordinatesWebOutputModel(BaseResponseDataModel):
    latitude: float
    longitude: float


class GetOrganizationByIdBuildingWebOutputModel(BaseResponseDataModel):
    id: UUID
    address: str
    coordinates: GetOrganizationByIdBuildingCoordinatesWebOutputModel


class GetOrganizationByIdActivityWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    level: int


class GetOrganizationByIdWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    phone_number: str
    building: GetOrganizationByIdBuildingWebOutputModel
    activities: list[GetOrganizationByIdActivityWebOutputModel]
    updated_at: datetime
    created_at: datetime
