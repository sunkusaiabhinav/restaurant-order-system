from decimal import Decimal

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    model_config = {
        "from_attributes": True
    }