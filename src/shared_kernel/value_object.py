from dataclasses import dataclass
from enum import EnumMeta
from typing import Any, TypeVar

from src.shared_kernel.exceptions import EntityValidationError

ValueObjectType = TypeVar("ValueObjectType", bound="ValueObject")


@dataclass(slots=True)
class ValueObject:
    def __composite_values__(self):
        return (self.value,)

    @classmethod
    def from_value(cls, value: Any) -> ValueObjectType:
        if isinstance(cls, EnumMeta):
            for item in cls:
                if item.value == value:
                    return item
            # raise ValueObjectEnumError

        instance = cls(value=value)
        return instance


@dataclass(slots=True)
class LongitudeVO(ValueObject):
    value: float

    def __post_init__(self) -> None:
        self._validate_longitude()

    def _validate_longitude(self) -> None:
        if not (-180.0 <= self.value <= 180.0):
            raise EntityValidationError(ru_detail="Долгота должна быть в диапазоне [-180, 180]")


@dataclass(slots=True)
class LatitudeVO(ValueObject):
    value: float

    def __post_init__(self) -> None:
        self._validate_latitude()

    def _validate_latitude(self) -> None:
        if not (-90.0 <= self.value <= 90.0):
            raise EntityValidationError(ru_detail="Широта должна быть в диапазоне [-90, 90]")
