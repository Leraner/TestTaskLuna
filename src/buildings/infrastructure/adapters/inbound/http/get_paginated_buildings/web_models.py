from uuid import UUID

from src.shared.web_models import BaseResponseDataModel, PaginatedWebOutputModel


class GetBuildingCoordinatesOutputWebModel(BaseResponseDataModel):
    longitude: float
    latitude: float


class GeBuildingsOutputWebModel(BaseResponseDataModel):
    id: UUID
    address: str
    coordinates: GetBuildingCoordinatesOutputWebModel


GetPaginatedBuildingsOutputWebModel = PaginatedWebOutputModel[
    GeBuildingsOutputWebModel
]
