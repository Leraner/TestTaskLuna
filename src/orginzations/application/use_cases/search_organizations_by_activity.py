from src.orginzations.application.dtos.search_organizations_by_activity import (
    SearchOrganizationsByActivityInputDTO,
    GetPaginatedSearchedOrganizationsByActivityOutputDTO,
    SearchedOrganizationByActivityOutputDTO,
    SearchedOrganizationByActivityBuildingOutputDTO,
)
from src.orginzations.domain.ports.activity_access_port import IActivityAccessPort
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)


class SearchOrganizationsByActivityUseCase:
    def __init__(
        self,
        organization_repository: IOrganizationRepositoryPort,
        activity_access_port: IActivityAccessPort,
    ) -> None:
        self._organization_repository = organization_repository
        self._activity_access_port = activity_access_port

    async def execute(
        self, input_dto: SearchOrganizationsByActivityInputDTO
    ) -> GetPaginatedSearchedOrganizationsByActivityOutputDTO:
        activity_ids = await self._activity_access_port.get_subtree_ids(
            root_activity_id=input_dto.activity_id
        )

        organizations, total_count = (
            await self._organization_repository.get_by_activities_paginated(
                activity_ids=activity_ids,
                page=input_dto.page,
                size=input_dto.size,
            )
        )

        return GetPaginatedSearchedOrganizationsByActivityOutputDTO(
            page=input_dto.page,
            size=input_dto.size,
            total_count=total_count,
            items=[
                SearchedOrganizationByActivityOutputDTO(
                    id=organization.id,
                    name=organization.name,
                    phone_number=organization.phone_number,
                    building=SearchedOrganizationByActivityBuildingOutputDTO(
                        id=organization.building.id,
                        address=organization.building.address,
                        latitude=organization.building.latitude,
                        longitude=organization.building.longitude,
                    ),
                )
                for organization in organizations
            ],
        )
