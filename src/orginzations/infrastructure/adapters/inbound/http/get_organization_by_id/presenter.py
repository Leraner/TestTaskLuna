from src.orginzations.application.dtos.get_organization_by_id import (
    GetOrganizationByIdOutputDTO,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_organization_by_id.web_models import (
    GetOrganizationByIdWebOutputModel,
    GetOrganizationByIdBuildingWebOutputModel,
    GetOrganizationByIdBuildingCoordinatesWebOutputModel,
    GetOrganizationByIdActivityWebOutputModel,
)


class GetOrganizationByIdPresenter:
    def present(
        self, output_dto: GetOrganizationByIdOutputDTO
    ) -> GetOrganizationByIdWebOutputModel:
        return GetOrganizationByIdWebOutputModel(
            id=output_dto.id,
            name=output_dto.name,
            phone_number=output_dto.phone_number,
            building=GetOrganizationByIdBuildingWebOutputModel(
                id=output_dto.building.id,
                address=output_dto.building.address,
                coordinates=GetOrganizationByIdBuildingCoordinatesWebOutputModel(
                    latitude=output_dto.building.latitude.value,
                    longitude=output_dto.building.longitude.value,
                ),
            ),
            activities=[
                GetOrganizationByIdActivityWebOutputModel(
                    id=act.id,
                    name=act.name,
                    level=act.level,
                )
                for act in output_dto.activities
            ],
            updated_at=output_dto.updated_at,
            created_at=output_dto.created_at,
        )
