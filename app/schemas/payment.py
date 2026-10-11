from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.payment import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int
    amount: Decimal = Field(gt=0)
    payment_method: PaymentMethod = PaymentMethod.MOCK


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    status: PaymentStatus
    transaction_id: str | None
    payment_method: PaymentMethod
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)