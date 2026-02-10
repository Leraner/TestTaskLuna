from src.orginzations.application.dtos.get_paginated_organizations_by_building_id import (
    GetPaginatedOrganizationsByBuildingIdInputDTO,
    GetPaginatedOrganizationsByBuildingIdOutputDTO,
    GetOrganizationByBuildingIdOutputDTO,
    GetOrganizationByBuildingIdActivityOutputDTO,
)
from src.orginzations.domain.exceptions import OrganizationBuildingNotFoundError
from src.orginzations.domain.ports.building_access_port import IBuildingAccessPort
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)


class GetPaginatedOrganizationsByBuildingIdUseCase:
    def __init__(
        self,
        organization_repository: IOrganizationRepositoryPort,
        building_access_port: IBuildingAccessPort,
    ) -> None:
        self._organization_repository = organization_repository
        self._building_access_port = building_access_port

    async def execute(
        self, input_dto: GetPaginatedOrganizationsByBuildingIdInputDTO
    ) -> GetPaginatedOrganizationsByBuildingIdOutputDTO:
        building = await self._building_access_port.get_building_by_id(
            building_id=input_dto.building_id
        )

        if building is None:
            raise OrganizationBuildingNotFoundError

        organizations, total_count = (
            await self._organization_repository.get_organizations_paginated(
                page=input_dto.page,
                size=input_dto.size,
                building_id=building.id,
            )
        )

        return GetPaginatedOrganizationsByBuildingIdOutputDTO(
            page=input_dto.page,
            size=input_dto.size,
            total_count=total_count,
            items=[
                GetOrganizationByBuildingIdOutputDTO(
                    id=organization.id,
                    name=organization.name,
                    phone_number=organization.phone_number,
                    activities=[
                        GetOrganizationByBuildingIdActivityOutputDTO(
                            id=act.id,
                            name=act.name,
                            level=act.level,
                        )
                        for act in organization.activities
                    ],
                )
                for organization in organizations
            ],
        )
