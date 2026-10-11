from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MenuItemBase(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    price: Decimal = Field(ge=0)
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemResponse(MenuItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)