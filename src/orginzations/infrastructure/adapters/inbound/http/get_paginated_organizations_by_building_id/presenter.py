from src.orginzations.application.dtos.get_paginated_organizations_by_building_id import (
    GetPaginatedOrganizationsByBuildingIdOutputDTO,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_paginated_organizations_by_building_id.web_models import (
    GetPaginatedRolesWebOutputModel,
    GetOrganizationByBuildingIdWebOutputModel,
    GetOrganizationByBuildingIdActivityWebOutputModel,
)


class GetPaginatedOrganizationsByBuildingIdPresenter:
    def present(
        self,
        output_dto: GetPaginatedOrganizationsByBuildingIdOutputDTO,
    ) -> GetPaginatedRolesWebOutputModel:
        items = [
            GetOrganizationByBuildingIdWebOutputModel(
                id=item.id,
                name=item.name,
                phone_number=item.phone_number,
                activities=[
                    GetOrganizationByBuildingIdActivityWebOutputModel(
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
