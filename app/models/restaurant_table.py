from enum import Enum

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TableStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    table_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[TableStatus] = mapped_column(
        default=TableStatus.AVAILABLE,
        nullable=False
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="table"
    )

    __table_args__ = (
        CheckConstraint(
            "capacity > 0",
            name="check_table_capacity_positive"
        ),
    )