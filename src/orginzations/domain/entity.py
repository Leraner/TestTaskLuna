from datetime import datetime
from uuid import UUID

from src.buildings.domain.exceptions import BuildingValidationError
from src.orginzations.domain.activity_ref import ActivityRef
from src.orginzations.domain.building_ref import BuildingRef
from src.orginzations.domain.exceptions import OrganizationDoesNotExistError
from src.orginzations.domain.value_objects import PhoneNumberVO
from src.shared_kernel.entities import Entity


class Organization(Entity):
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 255

    def __init__(
        self,
        *,
        id: UUID | None = None,
        name: str,
        phone_number: PhoneNumberVO,
        building: BuildingRef,
        activities: list[ActivityRef] | None = None,
        updated_at: datetime | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self._id = id
        self._name = self._validate_name(name)
        self._phone_number = phone_number
        self._building = building
        self._activities = activities or []
        self._updated_at = updated_at
        self._created_at = created_at

    def _validate_name(self, name: str) -> str:
        if not name or not name.strip():
            raise BuildingValidationError(
                ru_detail="Название организации не может быть пустым"
            )

        normalized = name.strip()
        name_length = len(normalized)

        if name_length < self.MIN_NAME_LENGTH:
            raise BuildingValidationError(
                ru_detail=(
                    f"Название организации должно содержать минимум "
                    f"{self.MIN_NAME_LENGTH} символ"
                )
            )

        if name_length > self.MAX_NAME_LENGTH:
            raise BuildingValidationError(
                ru_detail=(
                    f"Название организации не может быть длиннее "
                    f"{self.MAX_NAME_LENGTH} символов"
                )
            )

        return normalized

    @property
    def id(self) -> UUID:
        if self._id is None:
            raise OrganizationDoesNotExistError
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def phone_number(self) -> str:
        return self._phone_number.value

    @property
    def building(self) -> BuildingRef:
        return self._building

    @property
    def activities(self) -> list[ActivityRef]:
        return self._activities

    @property
    def updated_at(self) -> datetime:
        if self._updated_at is None:
            raise OrganizationDoesNotExistError
        return self._updated_at

    @property
    def created_at(self) -> datetime:
        if self._created_at is None:
            raise OrganizationDoesNotExistError
        return self._created_at
