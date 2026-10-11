from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey(
            "menu_items.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    order: Mapped["Order"] = relationship(
        back_populates="order_items"
    )

    menu_item: Mapped["MenuItem"] = relationship()

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="check_order_item_quantity_positive"
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="check_order_item_unit_price_non_negative"
        ),
        CheckConstraint(
            "subtotal >= 0",
            name="check_order_item_subtotal_non_negative"
        ),
    )