from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OrderStatus(str, Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customers.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    table_id: Mapped[int] = mapped_column(
        ForeignKey(
            "restaurant_tables.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PLACED,
        nullable=False,
        index=True
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="orders"
    )

    table: Mapped["RestaurantTable"] = relationship(
        back_populates="orders"
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order"
    )