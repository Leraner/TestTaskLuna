from src.orginzations.application.dtos.search_organizations_by_activity import (
    GetPaginatedSearchedOrganizationsByActivityOutputDTO,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organizations_by_activity.web_models import (
    GetPaginatedOrganizationsByActivityWebOutputModel,
    SearchedOrganizationsByActivityWebOutputModel,
    GetOrganizationBuildingWebOutputModel,
    GetOrganizationBuildingCoordinatesWebOutputModel,
)


class SearchOrganizationsByActivityPresenter:
    def present(
        self, output_dto: GetPaginatedSearchedOrganizationsByActivityOutputDTO
    ) -> GetPaginatedOrganizationsByActivityWebOutputModel:
        items = [
            SearchedOrganizationsByActivityWebOutputModel(
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
            )
            for item in output_dto.items
        ]

        return GetPaginatedOrganizationsByActivityWebOutputModel(
            page=output_dto.page,
            size=output_dto.size,
            total_count=output_dto.total_count,
            items=items,
        )
