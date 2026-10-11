from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "menu_categories.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    category: Mapped["MenuCategory"] = relationship(
        back_populates="menu_items"
    )

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="check_menu_item_price_non_negative"
        ),
    )