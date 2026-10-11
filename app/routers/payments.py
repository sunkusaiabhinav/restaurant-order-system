import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order, OrderStatus
from app.models.payment import (
    Payment,
    PaymentStatus,
)
from app.models.restaurant_table import (
    RestaurantTable,
    TableStatus,
)
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def process_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    # --------------------------------------------
    # 1. Lock the order
    # --------------------------------------------

    order = (
        db.query(Order)
        .filter(Order.id == payment_data.order_id)
        .with_for_update()
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # --------------------------------------------
    # 2. Order must be completed
    # --------------------------------------------

    if order.status != OrderStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Payment can only be processed "
                "for a completed order"
            )
        )

    # --------------------------------------------
    # 3. Verify payment amount
    # --------------------------------------------

    if payment_data.amount != order.total_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Payment amount must match "
                f"order total: {order.total_amount}"
            )
        )

    # --------------------------------------------
    # 4. Check previous successful payment
    # --------------------------------------------

    successful_payment = (
        db.query(Payment)
        .filter(
            Payment.order_id == order.id,
            Payment.status == PaymentStatus.SUCCESS
        )
        .first()
    )

    if successful_payment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order has already been paid"
        )

    # --------------------------------------------
    # 5. Mock payment
    # --------------------------------------------

    transaction_id = (
        f"MOCK-{uuid.uuid4().hex[:12].upper()}"
    )

    payment = Payment(
        order_id=order.id,
        amount=payment_data.amount,
        status=PaymentStatus.SUCCESS,
        transaction_id=transaction_id,
        payment_method=payment_data.payment_method
    )

    db.add(payment)

    # --------------------------------------------
    # 6. Release restaurant table
    # --------------------------------------------

    table = (
        db.query(RestaurantTable)
        .filter(
            RestaurantTable.id == order.table_id
        )
        .with_for_update()
        .first()
    )

    if table:
        table.status = TableStatus.AVAILABLE

    # --------------------------------------------
    # 7. Commit payment + table release
    # --------------------------------------------

    db.commit()
    db.refresh(payment)

    return payment