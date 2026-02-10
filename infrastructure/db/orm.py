from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseDBModel(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4)

    def to_entity(self):
        raise NotImplementedError("to_entity method not implemented in base class")


class Timestamp:
    """
    Model for upgrading application models
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
