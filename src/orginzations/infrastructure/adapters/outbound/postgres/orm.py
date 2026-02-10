from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.orm import BaseDBModel, Timestamp
from src.orginzations.domain.activity_ref import ActivityRef
from src.orginzations.domain.building_ref import BuildingRef
from src.orginzations.domain.entity import Organization
from src.orginzations.domain.value_objects import PhoneNumberVO
from src.shared_kernel.value_object import LongitudeVO, LatitudeVO

if TYPE_CHECKING:
    from src.buildings.infrastructure.adapters.outbound.postgres.orm import (
        BuildingModel,
    )
from src.activities.infrastructure.adapters.outbound.postgres.orm import ActivityModel


class OrganizationModel(BaseDBModel, Timestamp):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)

    building_id: Mapped[UUID] = mapped_column(
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
    )

    building: Mapped["BuildingModel"] = relationship(
        lazy="joined",
        back_populates="organizations",
    )

    activities: Mapped[list[ActivityModel]] = relationship(
        secondary="organization_activities",
        back_populates="organizations",
        lazy="selectin",
    )

    def to_entity(self) -> Organization:
        return Organization(
            id=self.id,
            name=self.name,
            phone_number=PhoneNumberVO.from_value(
                value=self.phone_number,
            ),
            building=BuildingRef(
                id=self.building.id,
                address=self.building.address,
                longitude=LongitudeVO.from_value(self.building.longitude),
                latitude=LatitudeVO.from_value(self.building.latitude),
            ),
            activities=[
                ActivityRef(id=act.id, name=act.name, level=act.level)
                for act in self.activities
            ],
            updated_at=self.updated_at,
            created_at=self.created_at,
        )

    @classmethod
    def from_entity(cls, entity: Organization) -> "OrganizationModel":
        return cls(
            name=entity.name,
            phone_number=entity.phone_number,
            building_id=entity.building.id,
        )
