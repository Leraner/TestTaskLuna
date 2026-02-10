from uuid import UUID

from src.shared.web_models import BaseResponseDataModel, PaginatedWebOutputModel


class GetPaginatedActivityWebOutputModel(BaseResponseDataModel):
    id: UUID
    name: str
    parent_id: UUID | None
    level: int


GetPaginatedActivitiesWebOutputModel = PaginatedWebOutputModel[
    GetPaginatedActivityWebOutputModel
]
