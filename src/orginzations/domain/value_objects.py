import re
from dataclasses import dataclass

from src.buildings.domain.exceptions import BuildingValidationError
from src.shared_kernel.exceptions import EntityValidationError
from src.shared_kernel.value_object import ValueObject


@dataclass(slots=True)
class PhoneNumberVO(ValueObject):
    value: str

    def __post_init__(self) -> None:
        self._validate_phone_number()

    def _validate_phone_number(self) -> None:
        if not self.value or not self.value.strip():
            raise BuildingValidationError(
                ru_detail="Номер телефона не может быть пустым"
            )

        # Убираем пробелы и дефисы для проверки
        cleaned = re.sub(r"[\s\-\(\)]", "", self.value)

        # Проверяем, что остались только цифры и знак +
        if not re.match(r"^\+?\d{10,15}$", cleaned):
            raise BuildingValidationError(
                ru_detail="Номер телефона должен содержать от 10 до 15 цифр и может начинаться с +"
            )

        if len(self.value) > 20:
            raise BuildingValidationError(
                ru_detail="Номер телефона не может быть длиннее 20 символов"
            )
