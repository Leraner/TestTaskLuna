from src.orginzations.application.dtos.get_organization_by_id import (
    GetOrganizationByIdInputDTO,
    GetOrganizationByIdOutputDTO,
    GetOrganizationByIdBuilding,
    GetOrganizationByIdActivityOutputDTO,
)
from src.orginzations.domain.exceptions import OrganizationDoesNotExistError
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)


class GetOrganizationByIdUseCase:
    def __init__(
        self,
        organization_repository: IOrganizationRepositoryPort,
    ) -> None:
        self._organization_repo = organization_repository

    async def execute(
        self, input_dto: GetOrganizationByIdInputDTO
    ) -> GetOrganizationByIdOutputDTO:
        organization = await self._organization_repo.get_by_id(
            organization_id=input_dto.organization_id
        )

        if organization is None:
            raise OrganizationDoesNotExistError

        return GetOrganizationByIdOutputDTO(
            id=organization.id,
            name=organization.name,
            phone_number=organization.phone_number,
            building=GetOrganizationByIdBuilding(
                id=organization.building.id,
                address=organization.building.address,
                longitude=organization.building.longitude,
                latitude=organization.building.latitude,
            ),
            activities=[
                GetOrganizationByIdActivityOutputDTO(
                    id=act.id,
                    name=act.name,
                    level=act.level,
                )
                for act in organization.activities
            ],
            updated_at=organization.updated_at,
            created_at=organization.created_at,
        )
