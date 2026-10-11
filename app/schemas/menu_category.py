from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MenuCategoryBase(BaseModel):
    name: str
    description: str | None = None


class MenuCategoryCreate(MenuCategoryBase):
    pass


class MenuCategoryResponse(MenuCategoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)