from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus
from app.schemas.order_item import OrderItemCreate, OrderItemResponse


class OrderCreate(BaseModel):
    customer_id: int
    table_id: int
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    table_id: int
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
    order_items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: OrderStatus