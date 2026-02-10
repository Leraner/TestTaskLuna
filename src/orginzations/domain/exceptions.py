from src.shared_kernel.exceptions import (
    DomainError,
    EntityNotFoundError,
    EntityValidationError,
)


class OrganizationError(DomainError):
    pass


class OrganizationDoesNotExistError(OrganizationError):
    detail = "Organization doesn't exist"
    ru_detail = "Данная организация не существует"


class OrganizationNotFoundError(EntityNotFoundError, OrganizationError):
    pass


class OrganizationBuildingNotFoundError(OrganizationNotFoundError):
    detail = "Building not found"
    ru_detail = "Здание не найдено"


class OrganizationActivityNotFoundError(OrganizationNotFoundError):
    detail = "One or more activities not found"
    ru_detail = "Одна или несколько деятельностей не найдены"


class OrganizationValidationError(EntityValidationError, OrganizationError):
    pass
