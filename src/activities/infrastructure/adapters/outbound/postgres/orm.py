from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.orm import BaseDBModel, Timestamp
from src.activities.domain.entity import Activity

if TYPE_CHECKING:
    from src.orginzations.infrastructure.adapters.outbound.postgres.orm import (
        OrganizationModel,
    )


organization_activities = Table(
    "organization_activities",
    BaseDBModel.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activity_id",
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ActivityModel(BaseDBModel, Timestamp):
    __tablename__ = "activities"

    name: Mapped[str] = mapped_column(nullable=False)
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("activities.id", ondelete="RESTRICT"),
        nullable=True,
    )
    level: Mapped[int] = mapped_column(nullable=False, default=0)

    parent: Mapped["ActivityModel | None"] = relationship(
        "ActivityModel",
        remote_side="ActivityModel.id",
        back_populates="children",
        lazy="joined",
    )

    children: Mapped[list["ActivityModel"]] = relationship(
        "ActivityModel",
        back_populates="parent",
        lazy="joined",
        distinct_target_key=True,
    )

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        secondary=organization_activities,
        back_populates="activities",
        lazy="joined",
        distinct_target_key=True,
    )

    def to_entity(self) -> Activity:
        return Activity(
            id=self.id,
            name=self.name,
            parent_id=self.parent_id,
            level=self.level,
            updated_at=self.updated_at,
            created_at=self.created_at,
        )

    @classmethod
    def from_entity(cls, entity: Activity) -> "ActivityModel":
        return cls(
            name=entity.name,
            parent_id=entity.parent_id,
            level=entity.level,
        )
