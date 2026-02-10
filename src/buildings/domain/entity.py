from datetime import datetime
from uuid import UUID

from src.buildings.domain.exceptions import (
    BuildingDoesNotExistError,
    BuildingValidationError,
)
from src.shared_kernel.value_object import LongitudeVO, LatitudeVO
from src.shared_kernel.entities import Entity


class Building(Entity):
    MIN_ADDRESS_LENGTH = 1
    MAX_ADDRESS_LENGTH = 255

    def __init__(
        self,
        *,
        id: UUID | None = None,
        address: str,
        longitude: LongitudeVO,
        latitude: LatitudeVO,
        updated_at: datetime | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self._id = id
        self._address = self._validate_address(address)
        self._latitude = latitude
        self._longitude = longitude
        self._updated_at = updated_at
        self._created_at = created_at

    def _validate_address(self, address: str) -> str:
        if not address or not address.strip():
            raise BuildingValidationError(ru_detail="Адрес здания не может быть пустым")

        normalized = address.strip()
        address_length = len(normalized)

        if address_length < self.MIN_ADDRESS_LENGTH:
            raise BuildingValidationError(
                ru_detail=(
                    f"Адрес здания должен содержать минимум "
                    f"{self.MIN_ADDRESS_LENGTH} символ"
                )
            )

        if address_length > self.MAX_ADDRESS_LENGTH:
            raise BuildingValidationError(
                ru_detail=(
                    f"Адрес здания не может быть длиннее "
                    f"{self.MAX_ADDRESS_LENGTH} символов"
                )
            )

        return normalized

    @property
    def id(self) -> UUID:
        if self._id is None:
            raise BuildingDoesNotExistError
        return self._id

    @property
    def address(self) -> str:
        return self._address

    @property
    def longitude(self) -> LongitudeVO:
        return self._longitude

    @property
    def latitude(self) -> LatitudeVO:
        return self._latitude

    @property
    def updated_at(self) -> datetime:
        if self._updated_at is None:
            raise BuildingDoesNotExistError
        return self._updated_at

    @property
    def created_at(self) -> datetime:
        if self._created_at is None:
            raise BuildingDoesNotExistError
        return self._created_at
