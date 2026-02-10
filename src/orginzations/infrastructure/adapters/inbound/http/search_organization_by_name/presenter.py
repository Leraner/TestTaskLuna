from src.orginzations.application.dtos.search_organization_by_name import (
    GetPaginatedSearchedOrganizationsByNameOutputDTO,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organization_by_name.web_models import (
    GetPaginatedRolesWebOutputModel,
    SearchedOrganizationsByNameWebOutputModel,
    SearchedOrganizationByNameBuildingWebOutputModel,
    SearchedOrganizationByNameBuildingCoordinatesWebOutputModel,
    SearchedOrganizationByNameActivityWebOutputModel,
)


class SearchOrganizationByNamePresenter:
    def present(
        self, output_dto: GetPaginatedSearchedOrganizationsByNameOutputDTO
    ) -> GetPaginatedRolesWebOutputModel:
        items = [
            SearchedOrganizationsByNameWebOutputModel(
                id=item.id,
                name=item.name,
                phone_number=item.phone_number,
                building=SearchedOrganizationByNameBuildingWebOutputModel(
                    id=item.building.id,
                    address=item.building.address,
                    coordinates=SearchedOrganizationByNameBuildingCoordinatesWebOutputModel(
                        latitude=item.building.latitude.value,
                        longitude=item.building.longitude.value,
                    ),
                ),
                activities=[
                    SearchedOrganizationByNameActivityWebOutputModel(
                        id=act.id,
                        name=act.name,
                        level=act.level,
                    )
                    for act in item.activities
                ],
            )
            for item in output_dto.items
        ]

        return GetPaginatedRolesWebOutputModel(
            page=output_dto.page,
            size=output_dto.size,
            total_count=output_dto.total_count,
            items=items,
        )
