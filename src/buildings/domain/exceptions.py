from src.shared_kernel.exceptions import DomainError, EntityValidationError


class BuildingError(DomainError):
    pass


class BuildingDoesNotExistError(BuildingError):
    detail = "Building doesn't exist"
    ru_detail = "Данное здание не существует"


class BuildingValidationError(EntityValidationError, BuildingError):
    pass

