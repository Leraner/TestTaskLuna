from datetime import datetime
from uuid import UUID

from src.activities.domain.exceptions import (
    ActivityDoesNotExistError,
    ActivityMaxLevelExceededError,
    ActivityValidationError,
)
from src.shared_kernel.entities import Entity


class Activity(Entity):
    MAX_LEVEL = 2
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 255

    def __init__(
        self,
        *,
        id: UUID | None = None,
        name: str,
        parent_id: UUID | None = None,
        level: int = 0,
        updated_at: datetime | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self._id = id
        self._name = self._validate_name(name)
        self._validate_level(level)
        self._level = level
        self._parent_id = parent_id
        self._updated_at = updated_at
        self._created_at = created_at

    def _validate_name(self, name: str) -> str:
        if not name or not name.strip():
            raise ActivityValidationError(
                ru_detail="Название деятельности не может быть пустым"
            )

        normalized = name.strip()
        name_length = len(normalized)

        if name_length < self.MIN_NAME_LENGTH:
            raise ActivityValidationError(
                ru_detail=(
                    f"Название деятельности должно содержать минимум "
                    f"{self.MIN_NAME_LENGTH} символ"
                )
            )

        if name_length > self.MAX_NAME_LENGTH:
            raise ActivityValidationError(
                ru_detail=(
                    f"Название деятельности не может быть длиннее "
                    f"{self.MAX_NAME_LENGTH} символов"
                )
            )

        return normalized

    def _validate_level(self, level: int) -> None:
        if level < 0:
            raise ActivityMaxLevelExceededError(
                ru_detail="Уровень деятельности не может быть отрицательным"
            )

        if level > self.MAX_LEVEL:
            raise ActivityMaxLevelExceededError(
                ru_detail="Уровень вложенности деятельности не может превышать 2 (максимум 3 уровня)"
            )

    def calculate_child_level(self) -> int:
        if self._level >= self.MAX_LEVEL:
            raise ActivityMaxLevelExceededError(
                ru_detail="Нельзя создать деятельность глубже третьего уровня"
            )
        return self._level + 1

    @property
    def id(self) -> UUID:
        if self._id is None:
            raise ActivityDoesNotExistError
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent_id(self) -> UUID | None:
        return self._parent_id

    @property
    def level(self) -> int:
        return self._level

    @property
    def updated_at(self) -> datetime:
        if self._updated_at is None:
            raise ActivityDoesNotExistError
        return self._updated_at

    @property
    def created_at(self) -> datetime:
        if self._created_at is None:
            raise ActivityDoesNotExistError
        return self._created_at
