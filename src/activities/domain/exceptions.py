from src.shared_kernel.exceptions import (
    DomainError,
    EntityValidationError,
    EntityNotFoundError,
)

class ActivityError(DomainError):
    pass


class ActivityDoesNotExistError(EntityNotFoundError, ActivityError):
    detail = "Activity doesn't exist"
    ru_detail = "Данная деятельность не существует"


class ActivityValidationError(EntityValidationError, ActivityError):
    pass


class ActivityMaxLevelExceededError(ActivityValidationError):
    detail = "Activity level cannot exceed 2 (max 3 levels)"
    ru_detail = "Уровень вложенности деятельности не может превышать 2 (максимум 3 уровня)"
