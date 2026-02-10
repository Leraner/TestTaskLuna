from src.orginzations.application.dtos.get_organizations import (
    GetOrganizationsInputDTO,
    GetOrganizationOutputDTO,
    GetOrganizationBuildingOutputDTO,
    GetOrganizationActivityOutputDTO,
    GetOrganizationsOutputDTO,
)
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)


class GetOrganizationsUseCase:
    def __init__(self, organization_repository: IOrganizationRepositoryPort) -> None:
        self._organization_repository = organization_repository

    async def execute(
        self, input_dto: GetOrganizationsInputDTO
    ) -> GetOrganizationsOutputDTO:
        organizations = await self._organization_repository.get_organizations_by_radius(
            latitude=input_dto.latitude,
            longitude=input_dto.longitude,
            radius=input_dto.radius,
        )

        organization_dtos = [
            GetOrganizationOutputDTO(
                id=organization.id,
                name=organization.name,
                phone_number=organization.phone_number,
                building=GetOrganizationBuildingOutputDTO(
                    id=organization.building.id,
                    address=organization.building.address,
                    longitude=organization.building.longitude,
                    latitude=organization.building.latitude,
                ),
                activities=[
                    GetOrganizationActivityOutputDTO(
                        id=act.id,
                        name=act.name,
                        level=act.level,
                    )
                    for act in organization.activities
                ],
            )
            for organization in organizations
        ]

        return GetOrganizationsOutputDTO(
            organizations=organization_dtos,
        )
