from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing_customer = (
        db.query(Customer)
        .filter(Customer.phone == customer_data.phone)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer with this phone number already exists"
        )

    customer = Customer(
        name=customer_data.name,
        phone=customer_data.phone,
        email=customer_data.email
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return customer