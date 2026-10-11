from pydantic import BaseModel, ConfigDict, Field

from app.models.restaurant_table import TableStatus


class RestaurantTableBase(BaseModel):
    table_number: str
    capacity: int = Field(gt=0)


class RestaurantTableCreate(RestaurantTableBase):
    pass


class RestaurantTableResponse(RestaurantTableBase):
    id: int
    status: TableStatus

    model_config = ConfigDict(from_attributes=True)