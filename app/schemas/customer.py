from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerBase(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)