from src.orginzations.application.dtos.get_organizations import GetOrganizationsOutputDTO
from src.orginzations.infrastructure.adapters.inbound.http.get_organizations.web_models import (
    GetOrganizationWebOutputModel,
    GetOrganizationBuildingWebOutputModel,
    GetOrganizationBuildingCoordinatesWebOutputModel,
    GetOrganizationActivityWebOutputModel,
    GetOrganizationsResponseWebOutputModel,
)


class GetOrganizationsPresenter:
    def present(
        self, output_dto: GetOrganizationsOutputDTO
    ) -> GetOrganizationsResponseWebOutputModel:
        organizations = [
            GetOrganizationWebOutputModel(
                id=item.id,
                name=item.name,
                phone_number=item.phone_number,
                building=GetOrganizationBuildingWebOutputModel(
                    id=item.building.id,
                    address=item.building.address,
                    coordinates=GetOrganizationBuildingCoordinatesWebOutputModel(
                        latitude=item.building.latitude.value,
                        longitude=item.building.longitude.value,
                    ),
                ),
                activities=[
                    GetOrganizationActivityWebOutputModel(
                        id=act.id,
                        name=act.name,
                        level=act.level,
                    )
                    for act in item.activities
                ],
            )
            for item in output_dto.organizations
        ]

        return GetOrganizationsResponseWebOutputModel(
            organizations=organizations,
        )
