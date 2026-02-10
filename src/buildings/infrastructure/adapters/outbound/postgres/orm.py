from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship

from infrastructure.db.orm import BaseDBModel, Timestamp
from src.buildings.domain.entity import Building
from src.shared_kernel.value_object import LongitudeVO, LatitudeVO

if TYPE_CHECKING:
    from src.orginzations.infrastructure.adapters.outbound.postgres.orm import (
        OrganizationModel,
    )


GEOM_SRID = 4326


class BuildingModel(BaseDBModel, Timestamp):
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    geom = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=GEOM_SRID,
            spatial_index=True,
        ),
        nullable=False,
    )

    longitude = column_property(func.ST_X(geom))
    latitude = column_property(func.ST_Y(geom))

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        back_populates="building",
        cascade="all, delete-orphan",
    )

    def to_entity(self) -> Building:
        return Building(
            id=self.id,
            address=self.address,
            latitude=LatitudeVO.from_value(self.latitude),
            longitude=LongitudeVO.from_value(self.longitude),
            updated_at=self.updated_at,
            created_at=self.created_at,
        )

    @classmethod
    def from_entity(cls, entity: Building) -> "BuildingModel":
        return cls(
            address=entity.address,
            geom=func.ST_SetSRID(
                func.ST_MakePoint(
                    entity.longitude.value,
                    entity.latitude.value,
                ),
                GEOM_SRID,
            ),
        )
