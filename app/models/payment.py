from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class PaymentMethod(str, Enum):
    MOCK = "MOCK"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
        index=True
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
        index=True
    )

    payment_method: Mapped[PaymentMethod] = mapped_column(
        SQLEnum(PaymentMethod),
        default=PaymentMethod.MOCK,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    order: Mapped["Order"] = relationship()