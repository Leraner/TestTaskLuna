from src.orginzations.application.dtos.search_organization_by_name import (
    SearchOrganizationByNameInputDTO,
    GetPaginatedSearchedOrganizationsByNameOutputDTO,
    SearchedOrganizationByNameOutputDTO,
)
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)


class SearchOrganizationByNameUseCase:
    def __init__(
        self,
        organization_repository: IOrganizationRepositoryPort,
    ) -> None:
        self._organization_repository = organization_repository

    async def execute(
        self, input_dto: SearchOrganizationByNameInputDTO
    ) -> GetPaginatedSearchedOrganizationsByNameOutputDTO:
        organizations, total_count = (
            await self._organization_repository.search_by_name_paginated(
                page=input_dto.page,
                size=input_dto.size,
                organization_name=input_dto.organization_name,
            )
        )

        return GetPaginatedSearchedOrganizationsByNameOutputDTO(
            page=input_dto.page,
            size=input_dto.size,
            total_count=total_count,
            items=[
                SearchedOrganizationByNameOutputDTO(
                    id=organization.id,
                    name=organization.name,
                )
                for organization in organizations
            ],
        )
